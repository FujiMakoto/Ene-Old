import time
import asyncio
import venusian
from collections import deque
from ipaddress import ip_address
from .dcc import DCCManager
from .dcc import DCCChat
from . import config
from . import utils
from . import base
# from .dec import dcc_event
# from .dec import event
# from .dec import extend
# from .dec import plugin


class IrcProtocol(asyncio.Protocol):
    """
    IRC Connection handler
    """
    def __init__(self):
        """
        Initialize a new IRC connection
        """
        self.transport = None
        self.closed = True
        self.queue = None

    def connection_made(self, transport):
        """
        AsyncIO connection made event
        @type   transport:  asyncio.selector_events._SelectorSocketTransport
        """
        self.transport = transport
        self.closed = False
        self.queue = deque()

    def decode(self, data):
        """
        Decode data with bot's encoding
        @type   data:   bytes
        @rtype:         str
        """
        """Decode data with bot's encoding"""
        encoding = getattr(self, 'encoding', 'ascii')
        return data.decode(encoding, 'ignore')

    def data_received(self, data):
        """
        AsyncIO data received event
        @param  data:   bytes
        """
        data = self.decode(data)

        if self.queue:
            data = self.queue.popleft() + data
        lines = data.split('\r\n')
        self.queue.append(lines.pop(-1))

        for line in lines:
            self.factory.dispatch(line)

    def encode(self, data):
        """
        Encode data with bot's encoding
        @param  data:   str or bytes
        """
        if isinstance(data, str):
            data = data.encode(self.encoding)
        return data

    def write(self, data):
        """
        Write data to the transport stream
        @param  data:   str or bytes
        """
        if data is not None:
            data = self.encode(data)
            if not data.endswith(b'\r\n'):
                data = data + b'\r\n'
            self.transport.write(data)

    def connection_lost(self, exc):
        """
        AsyncIO connection lost event
        """
        self.factory.log.critical('connection lost (%s): %r',
                                  id(self.transport),
                                  exc)
        self.factory.notify('connection_lost')
        if not self.closed:
            self.closed = True
            self.close()
            # wait a few before reconnect
            self.factory.loop.call_later(
                2, self.factory.create_connection)

    def close(self):
        """
        Close transport stream
        """
        if not self.closed:
            self.factory.log.critical('closing old transport (%r)',
                                      id(self.transport))
            try:
                self.transport.close()
            finally:
                self.closed = True


class Irc(base.IrcObject):
    """
    Primary IRC class
    """
    # _pep8 = [dcc_event, event, extend, plugin, rfc, config]
    venusian = venusian
    venusian_categories = [
        'ene.interfaces.protocols.irc',
        'ene.interfaces.protocols.irc.dcc',
        'ene.interfaces.protocols.irc.extend',
        'ene.interfaces.protocols.irc.rfc1459',
        'ene.interfaces.protocols.irc.plugins.cron',
        'ene.interfaces.protocols.irc.plugins.command',
    ]

    logging_config = config.LOGGING

    defaults = dict(
        base.IrcObject.defaults,
        nick='Ene',
        realname='Takane',
        userinfo='Irc bot based on irc3 http://irc3.readthedocs.org',
        host='192.168.0.230',
        url='https://github.com/FujiMakoto/Ene',
        passwords={},
        ctcp=dict(
            version='Ene {version} - {url}',
            userinfo='{userinfo}',
            time='{now:%c}',
        ),
        # freenode config as default for testing
        server_config=dict(
            STATUSMSG='+@',
            PREFIX='(ov)@+',
            CHANTYPES='#',
            CHANMODES='eIbq,k,flj,CFLMPQScgimnprstz',
        ),
        connection=IrcProtocol,
    )

    def __init__(self, *ini, **config):
        """
        Initialize a new IRC instance
        """
        super(Irc, self).__init__(*ini, **config)
        self._ip = self._dcc = None
        self.protocol = None

    @property
    def server_config(self):
        """
        return server configuration (rfc rpl 005)::
            >>> bot = Irc()
            >>> print(bot.server_config['STATUSMSG'])
            +@
        The real values are only available after the server sent them.
        """
        return self.config.server_config

    def connection_made(self, f):
        """
        Connection made event
        @type   f:  asyncio.tasks.Task
        """
        # Do we need to close a previous connection?
        if getattr(self, 'protocol'):
            self.protocol.close()

        # Try and set our transport and protocol and re-connect if there is an issue
        try:
            transport, protocol = f.result()
        except Exception as e:
            self.log.exception(e)
            self.loop.call_later(3, self.create_connection)
        else:
            self.log.debug('Connected')
            self.protocol = protocol
            self.protocol.queue = deque()
            self.protocol.factory = self
            self.protocol.encoding = self.encoding

            # Do we need to send a server password?
            if self.config.get('password'):
                self._send('PASS {password}'.format(**self.config))

            # Set our identity and nick information
            self.send((
                'USER {realname} {host} {host} :{userinfo}\r\n'
                'NICK {nick}\r\n'
            ).format(**self.config))

            self.notify('connection_made')  # fire connection made events
            self.join('#homestead')
            self.privmsg('#homestead', 'Hello, world!')

    def send_line(self, data):
        """
        Send a line to the server, replacing any CR's with spaces beforehand
        @param  data:   str
        """
        self.send(data.replace('\n', ' ').replace('\r', ' '))

    def send(self, data):
        """
        Send RAW data to the server
        @param  data:   str
        """
        self.protocol.write(data)
        self.dispatch(data, iotype='out')

    # def _send(self, data):
    #     self.protocol.write(data)
    #     self.dispatch(data, iotype='out')

    def privmsg(self, target, message):
        """
        Send a PRIVMSG
        @type   target:     str
        @type   message:    str
        """
        if message:
            messages = utils.split_message(message, self.config.max_length)
            if isinstance(target, DCCChat):
                for message in messages:
                    target.send_line(message)
            elif target:
                for message in messages:
                    self.send_line(u'PRIVMSG {0:s} :{1:s}'.format(target, message))

    def notice(self, target, message):
        """
        Send a NOTICE
        @type   target:     str
        @type   message:    str
        """
        if message:
            messages = utils.split_message(message, self.config.max_length)
            if isinstance(target, DCCChat):
                for message in messages:
                    target.action(message)
            elif target:
                for message in messages:
                    self.send_line(u'NOTICE {0:s} :{1:s}'.format(target, message))

    def ctcp(self, target, message):
        """
        Send a CTCP
        @type   target:     str
        @type   message:    str
        """
        if target and message:
            messages = utils.split_message(message, self.config.max_length)
            for message in messages:
                self.send_line(u'PRIVMSG {0:s} :\x01{1:s}\x01'.format(target, message))

    def ctcp_reply(self, target, message):
        """
        Respond to a CTCP sent to us
        @type   target:     str
        @type   message:    str
        """
        if target and message:
            messages = utils.split_message(message, self.config.max_length)
            for message in messages:
                self.send_line(u'NOTICE {0:s} :\x01{1:s}\x01'.format(target, message))

    def mode(self, target, *data):
        """
        Set a user or channel MODE
        @param  target: User or channel to set a mode on
        @type   target: str
        """
        self.send_line(u'MODE {0:s} {1:s}'.format(target, ' '.join(data)))

    def join(self, target):
        """
        Join a channel
        @param  target: Channel to join (including prefix)
        @type   target: str
        """
        password = self.config.passwords.get(
            target.strip(self.server_config['CHANTYPES']))
        if password:
            target += ' ' + password
        self.send_line(u'JOIN {0:s}'.format(target))

    def part(self, target, reason=None):
        """
        Part a channel
        @param  target: Channel to part (including prefix)
        @type   target: str
        """
        if reason:
            target += ' :' + reason
        self.send_line(u'PART {0:s}'.format(target))

    def kick(self, channel, target, reason=None):
        """
        Kick someone from a channel
        @param  target: User to kick
        @type   target: str
        """
        if reason:
            target += ' :' + reason
        self.send_line(u'KICK {0:s} {1:s}'.format(channel, target))

    def invite(self, target, channel):
        """
        Invite someone to join a channel
        @param  target: User to invite
        @type   target: str
        """
        self.send_line(u'INVITE {0:s} {1:s}'.format(target, channel))

    def topic(self, channel, topic=None):
        """
        Change or request the topic of a channel
        @type   channel:    str
        @param  topic:      Either the topic to set, or NONE to request the current topic
        @type   topic:      str or None
        """
        if topic:
            channel += ' :' + topic
        self.send_line(u'TOPIC {0:s}'.format(channel))

    def away(self, message):
        """
        Mark ourselves as away
        @param  message:    Away message
        @type   message:    str or None
        """
        cmd = u'AWAY :{0:s}'.format(message)
        self.send_line(cmd)

    def back(self):
        """
        Mark ourselves as no longer away
        """
        self.send_line('AWAY')

    def quit(self, reason=None):
        """
        Disconnect from the server
        @param  reason: An optional reason for quitting
        @type   reason: str
        """
        if not reason:
            reason = 'Quitting'

        self.send_line(u'QUIT :{0:s}'.format(reason))

    def get_nick(self):
        """
        Get our current nick
        @rtype: str
        """
        return self.config.nick

    def set_nick(self, nick):
        """
        Set our nick
        @type   nick:   str
        """
        self.send_line('NICK ' + nick)

    nick = property(get_nick, set_nick, doc='nickname get/set')

    @property
    def ip(self):
        """
        Return our IP as an ip_address object
        @rtype: ip_address
        """
        if not self._ip:
            if 'ip' in self.config:
                ip = self.config['ip']
            else:
                ip = self.protocol.transport.get_extra_info('sockname')[0]
            self._ip = ip_address(ip)

        return self._ip

    @property
    def dcc(self):
        """
        Return the DCCManager instance
        @rtype: DCCManager
        """
        if self._dcc is None:
            self._dcc = DCCManager(self)
        return self._dcc

    @asyncio.coroutine
    def dcc_chat(self, mask, host=None, port=None):
        """
        Open a DCC CHAT. If host/port are specified then connect to a server, otherwise create a server
        @type   mask:   str
        @type   host:   str or None
        @type   port:   int or None
        """

        return self.dcc.create('chat', mask, host=host, port=port).ready

    @asyncio.coroutine
    def dcc_get(self, mask, host, port, filepath, filesize=None):
        """
        DCC GET a file from mask.
        @type   mask:       str
        @type   host:       str
        @type   port:       int
        @param  filepath:   Absolute path to an existing directory
        @type   filepath:   str
        @param  filesize:   The expected file size
        @type   filesize:   int or None
        """
        return self.dcc.create('get', mask, filepath=filepath, filesize=filesize).ready

    @asyncio.coroutine
    def dcc_send(self, mask, filepath):
        """
        DCC SEND a file to mask.
        @type   mask:       str
        @param  filepath:   Absolute path to the file to send
        @type   filepath:   str
        """
        return self.dcc.create('send', mask, filepath=filepath).ready

    @asyncio.coroutine
    def dcc_accept(self, mask, filepath, port, pos):
        """
        Accept a DCC RESUME for an existing DCC SEND.
        @type   mask:       str
        @type   filepath:   str
        @type   port:       int
        @param  pos:        File transfer offset
        @type   pos:        int
        """
        return self.dcc.resume(mask, filepath, port, pos)

    def SIGHUP(self):
        self.reload()

    def SIGINT(self):
        self.notify('SIGINT')
        if getattr(self, 'protocol', None):
            self.quit('INT')
            time.sleep(1)
        self.loop.stop()
