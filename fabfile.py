"""

  RadioX

  Copyright 2012 - Rob Cakebread <cakebread@gmail.com>
  License: BSD

  git://github.com/cakebread/radiox.git

  RadioX is an internet radio station broadcasting Icecast2 or Shoutcast.

  The goal of the RadioX project is to make an easily deployable, fully
  featured internet radio station with live on-air conferencing requiring
  no special hardware - callers dial in with regular phones.

  The public facing website for displaying show schedules and what
  is currently being played is powered by Django, Mezzanine and
  Bootstrap for a modern look and feel in browsers and on phones.

  Airtime can be used for the web interface to schedule shows by DJs and
  station managers. If you don't need scheduling, RadioX can be controlled by 
  any mpd client. This allows DJing from phones without needing to worry
  about dropped connections. The media is stored on the RadioX server.

  heduling of shows. Liquidsoap is an audio programming language developed 
  to mix audio sources and stream to an Icecast or Shoutcast server.

  RadioX can be put into request mode where listeners cand send SMS
  text messages or Jabber IMs to search for and request songs.

  RadioX will act as a SIP endpoint or Google Voice endpoint and uses Twilio
  for conference calls and purchasing phone numbers.

This is a Cuisine Fabric file. It will take a freshly installed
Ubuntu 12.04 LTS box and turn it into an Icecast radio station.

The scheduling is controlled by the powerful Airtime software.

The backend and most of the scripting is in Python.  For the public facing
website, Django is git://github.com/cakebread/radiox.gitused to show schedules.

To get a fully functioning radio station streaming on port 9999 on
your local Linux box using Vagrant:

    Put this fab file inside a Python virtualenv, then:

    $ vagrant up
    $ fab vagrant setup

A few sample songs are in the library and your radio station is now
streaming music!

Accessing the Radio Staion running in the Vagrant VirtualBox:

    Stream:

        http://localhost:9999/airtime_128
        (Icecast2 URL for phones, media players etc.)

    Airtime Admin Web Interface for Djs :

        http://localhost:9080   (Airtime admin interface)


"""


from cuisine import *
from fabric.api import *


#############################################################################
# Define your deployment hosts here
#############################################################################

def vagrant():
    """Use Vagrant VirtualBox as host"""
    env.user = 'vagrant'
    env.hosts = ['127.0.0.1:2222']
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.lstrip('IdentityFile').strip()


def production():
    """Define your production host(s) you want to deploy to"""

    #WARNING:
    #
    #   ** This has only been tested with Vagrant / VirtualBox **
    #
    #   ** Don't use on existing production sites unless you're familiar **
    #   ** with what the Airtime .deb does to your Apache config! **
    #   ** TODO: Don't use Airtime .deb, use nginx, no apache2 **
    #
    # Use on a fresh installation of Ubuntu 12.04 LTS
    # (Airtime's .deb will clobber your existing Apache config)

    env.user = 'pollard'
    env.hosts = ['gbvdb.com', 'i-am-a-scientist.com']


#############################################################################
# Deployment functions
#############################################################################

def install_airtime():
    '''Install Airtime .deb'''
    run('wget http://apt.sourcefabric.org/misc/airtime-easy-setup.deb')
    sudo('dpkg -i ./airtime-easy-setup.deb')
    sudo('apt-get update')
    sudo('apt-get --yes install airtime')


def install_pg_utf8():
    with prefix('export LC_ALL=en_US.UTF-8'):
        sudo('apt-get --yes install libossp-uuid16')
        sudo('apt-get --yes install postgresql')
        sudo('apt-get --yes install postgresql-client-9.1')
        sudo('apt-get --yes install postgresql-9.1')
        sudo('apt-get --yes install postgresql-contrib-9.1')


def setup_locale():
    '''Set UTF-8 locale'''
    sudo('echo "en_US.UTF-8 UTF-8" > /var/lib/locales/supported.d/local')
    sudo('echo "############################" >> /etc/bash.bashrc')
    sudo('echo "#Added by RadioX for sanity:\n" >> /etc/bash.bashrc')
    sudo('echo "LANGUAGE=en_US.UTF-8" >> /etc/bash.bashrc')
    sudo('echo "LANG=en_US.UTF-8" >> /etc/bash.bashrc')
    sudo('echo "LC_ALL=en_US.UTF-8" >> /etc/bash.bashrc')
    sudo('echo "LC_ALL=en_US.UTF-8" > /etc/default/locale')
    sudo('echo "LANG=en_US.UTF-8" >> /etc/default/locale')
    sudo('locale-gen en_US.UTF-8')
    sudo('dpkg-reconfigure locales')


def upgrade():
    sudo('apt-get update')
    sudo('apt-get --yes upgrade')


def setup():
    '''Deploy basic packages'''
    # Ensure postgresql database encoding is UTF-8
    setup_locale()
    upgrade()
    install_pg_utf8()

    server = ['pgbouncer', 'supervisor']
    dev = ['tmux', 'vim', 'git-core', 'build-essential', 'gettext',
           'apache2-utils', 'phppgadmin']
    py = ['python2.7', 'python2.7-dev', 'python-setuptools', 'python-pip',
          'python-dev', 'python-virtualenv']

    airtime = ['apache2', 'apache2-mpm-prefork',
               'apache2.2-bin', 'apache2.2-common', 'autoconf',
               'automake', 'autotools-dev', 'binutils', 'cpp', 'cpp-4.6', 'curl',
               'debconf-utils', 'ecasound', 'erlang-asn1', 'erlang-base',
               'erlang-corba', 'erlang-crypto', 'erlang-dev', 'erlang-diameter',
               'erlang-docbuilder', 'erlang-edoc', 'erlang-erl-docgen',
               'erlang-eunit', 'erlang-ic', 'erlang-inets', 'erlang-inviso',
               'erlang-mnesia', 'erlang-nox', 'erlang-odbc', 'erlang-os-mon',
               'erlang-parsetools', 'erlang-percept', 'erlang-public-key',
               'erlang-runtime-tools', 'erlang-snmp', 'erlang-ssh', 'erlang-ssl',
               'erlang-syntax-tools', 'erlang-tools', 'erlang-webtool',
               'erlang-xmerl', 'esound-common', 'faad', 'fontconfig-config',
               'freepats', 'gcc', 'gcc-4.6', 'icecast2', 'lame', 'libao-common',
               'libao-ocaml', 'libao4', 'libapache2-mod-php5', 'libapr1',
               'libaprutil1', 'libaprutil1-dbd-sqlite3', 'libaprutil1-ldap',
               'libasound2', 'libasyncns0', 'libaudio2', 'libaudiofile1',
               'libc-dev-bin', 'libc6-dev', 'libcamomile-ocaml-data', 'libesd0',
               'libfaad2', 'libflac8', 'libfontconfig1', 'libgd2-xpm', 'libgomp1',
               'libice6', 'libjack-jackd2-0', 'libjpeg-turbo8', 'libjpeg8',
               'libjson0', 'libkvutils4', 'liblo7', 'libltdl-dev', 'libltdl7',
               'libmad-ocaml', 'libmad0', 'libmikmod2', 'libmp3lame0', 'libmpc2',
               'libmpfr4', 'libmpg123-0', 'libodbc1', 'libogg0', 'liboil0.3',
               'libportaudio2', 'libpq5', 'libpulse0', 'libquadmath0',
               'libsamplerate0', 'libsctp1', 'libsm6', 'libsndfile1',
               'libsoundtouch-ocaml', 'libsoundtouch0', 'libspeex1', 'libssl-dev',
               'libssl-doc', 'libt1-5', 'libtag1-vanilla', 'libtag1c2a',
               'libtaglib-ocaml', 'libtheora0', 'libtool', 'libvorbis0a',
               'libvorbisenc2', 'libvorbisfile3', 'libx11-6', 'libx11-data',
               'libxaw7', 'libxext6', 'libxmu6', 'libxpm4', 'libxslt1.1', 'libxt6',
               'linux-libc-dev', 'lksctp-tools', 'm4', 'manpages-dev', 'mikmod',
               'monit', 'mpg123', 'multitail', 'ocaml-base-nox', 'odbc-postgresql',
               'odbcinst', 'odbcinst1debian2', 'oss-compat', 'php-pear', 'php5-cli',
               'php5-common', 'php5-curl', 'php5-dev', 'php5-gd', 'php5-pgsql',
               'rabbitmq-server', 'shtool', 'ssl-cert', 'timidity', 'unzip',
               'timidity-daemon', 'ttf-dejavu-core', 'vorbis-tools',
               'x11-common', 'zlib1g-dev']

    for pkg in server + dev + py + airtime:
        package_ensure(pkg)

    sudo('pip install virtualenvwrapper')
    install_airtime()
    add_songs()
    update_liquidsoap_script()
    print("You can listen to the stream with: mplayer http://localhost:9999/airtime_128")
    print("The Airtime web interface: at: http://localhost:9080")
    print("Public facing web interface coming soon in Django.")


def update_liquidsoap_script():
    """Replace default Airtime liquidsoap script with RadioX"""
    radiox = 'liquidsoap/ls_script.liq'
    file_upload(
        '/usr/lib/airtime/pypo/bin/liquidsoap_scripts/ls_script.liq',
        radiox,
        sudo='pypo')
    sudo('service airtime-liquidsoap restart')


def add_songs():
    sudo('mkdir tmp')
    with cd('tmp'):
        sudo('wget -q http://www.robertpollard.net/sounds/tabbyandlucy.mp3')
        sudo('wget -q http://www.robertpollard.net/sounds/Come%20On%20Baby%20Grace.mp3')
        sudo('wget -q http://www.robertpollard.net/sounds/questiongirlallright.mp3')
        sudo('wget -q http://www.robertpollard.net/sounds/jimmy.mp3')
        sudo('wget -q http://www.robertpollard.net/sounds/imaginaryqueenanne.mp3')
        sudo('wget -q http://www.robertpollard.net/sounds/loveyourspaceman.mp3')
        sudo('airtime-import -m ./*mp3')

def install_mezzanine_dev():
    """Install local copy of Mezzanine for developer

    Mezzanine isn't deployed on the vagrant box when Airtime is deployed.

    The developer will want to modify the Django site locally then deploy.
    The Django front-end is not required to stream music,
    it's purely informational, public-facing. You can reach
    it at http://localhost:8000/

    """
    local('pip install -r requires.txt')
    local('mezzanine-project radiox')
    with lcd('radiox'):
        local('python manage.py createdb')
        local('python manage.py runserver')



#############################################################################
#Use these functions to diagnose problems. They are non-destructive.
#############################################################################


def show_sudo_locale():
    sudo('locale')


def show_pg_locale():
    sudo('sudo -u postgres locale')


def show_pg_encoding():
    sudo('sudo -u postgres psql -c "SHOW SERVER_ENCODING"')


def show_airtime_status():
    sudo('service airtime-media-monitor status')
    print('After port forwarding:')
    print('AIRTIME_STATUS_URL = http://localhost:9080/api/status/format/json/api_key/%%api_key%%')
