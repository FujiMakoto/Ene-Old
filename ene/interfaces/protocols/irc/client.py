import logging
import irc.client


# noinspection PyMethodMayBeStatic
class IrcClient:
    """
    Establishes a new connection to an IRC server
    """
    def __init__(self, network, channel):
        """
        Initialize a new IRC instance

        Args:
            network(database.models.Network): The IRC Network to connect to
            channel(database.models.channel): The channel to join
        """
        self.log = logging.getLogger('ene.protocol.irc')

        # Set up the client Reactor
        self.log.debug('Setting up the IRC Reactor')
        self.reactor = irc.client.Reactor()

        try:
            self.connection = self.reactor.server().connect(network.host, network.port, network.nick)
        except irc.client.ServerConnectionError as e:
            print(e)
            exit()

        # Assign handlers
        self.log.debug('Assigning connection event handlers')
        self.connection.add_global_handler('nicknameinuse', self.on_nick_in_use)
        self.connection.add_global_handler('erroneusnickname', self.on_erroneous_nick)
        self.connection.add_global_handler('serviceinfo', self.on_service_info)
        self.connection.add_global_handler('featurelist', self.on_welcome)
        self.connection.add_global_handler('cannotsendtochan', self.on_cannot_send_to_channel)
        self.connection.add_global_handler('toomanychannels', self.on_too_many_channels)
        self.connection.add_global_handler('unavailresource', self.on_unavailable_resource)
        self.connection.add_global_handler('channelisfull', self.on_channel_is_full)
        self.connection.add_global_handler('keyset', self.on_key_set)
        self.connection.add_global_handler('badchannelkey', self.on_bad_channel_key)
        self.connection.add_global_handler('inviteonlychan', self.on_invite_only_channel)
        self.connection.add_global_handler('bannedfromchan', self.on_banned_from_channel)
        self.connection.add_global_handler('banlistfull', self.on_ban_list_full)
        self.connection.add_global_handler('chanoprivsneeded', self.on_chanop_privs_needed)
        self.connection.add_global_handler('pubmsg', self.on_public_message)
        self.connection.add_global_handler('pubnotice', self.on_public_notice)
        self.connection.add_global_handler('privmsg', self.on_private_message)
        self.connection.add_global_handler('privnotice', self.on_private_notice)
        self.connection.add_global_handler('action', self.on_action)
        self.connection.add_global_handler('join', self.on_join)
        self.connection.add_global_handler('part', self.on_part)
        self.connection.add_global_handler('quit', self.on_quit)
        self.connection.add_global_handler('kick', self.on_kick)

    def start(self):
        """
        Initialize and start processing the IRC connection
        """
        self.log.info('Initializing a new IRC connection')
        self.reactor.process_forever()

    def on_nick_in_use(self, connection, event):        
        """
        433: nicknameinuse
        
        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_erroneous_nick(self, connection, event):
        """
        432: erroneusnickname

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_service_info(self, connection, event):
        """
        231: serviceinfo

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_welcome(self, connection, event):
        """
        001: welcome

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_feature_list(self, connection, event):
        """
        005: featurelist

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_cannot_send_to_channel(self, connection, event):
        """
        404: cannotsendtochan

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_too_many_channels(self, connection, event):
        """
        405: toomanychannels

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_unavailable_resource(self, connection, event):
        """
        437: unavailresource

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_channel_is_full(self, connection, event):
        """
        471: channelisfull

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_key_set(self, connection, event):
        """
        467: keyset

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_bad_channel_key(self, connection, event):
        """
        475: badchannelkey

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_invite_only_channel(self, connection, event):
        """
        473: inviteonlychan

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_banned_from_channel(self, connection, event):
        """
        474: bannedfromchan

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_ban_list_full(self, connection, event):
        """
        478: banlistfull

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_chanop_privs_needed(self, connection, event):
        """
        482: chanoprivsneeded

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_public_message(self, connection, event):
        """
        pubmsg

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_public_notice(self, connection, event):
        """
        pubnotice

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_private_message(self, connection, event):
        """
        privmsg

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_private_notice(self, connection, event):
        """
        privnotice

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_action(self, connection, event):
        """
        action

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_join(self, connection, event):
        """
        join

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_part(self, connection, event):
        """
        part

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_quit(self, connection, event):
        """
        quit

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass

    def on_kick(self, connection, event):
        """
        kick

        :param  connection: The active IRC connection
        :type   connection: irc.client.connection
        :param  event:      The event response data
        :type   event:      irc.client.Event
        """
        pass
