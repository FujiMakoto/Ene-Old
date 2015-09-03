from setuptools import setup, find_packages

setup(
    name='Ene',
    version='0.1.0',
    description='Ene',
    long_description='Ene',
    author='Makoto Fujimoto',
    author_email='makoto@makoto.io',
    url='https://github.com/FujiMakoto/Ene',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
    ],
    packages=find_packages(),
    entry_points={
        'ene.interfaces.languages': ['agentml = agentml:AgentMlLanguage']
    },
    requires=['agentml']
)