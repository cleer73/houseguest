from fabric.api import *

remove_packages_updated = False

@task
def vagrant():
    # change from the default user to 'vagrant'
    env.user = 'vagrant'

    # connect to the port-forwarded ssh
    env.hosts = ['127.0.0.1:2222']

    # Disable cached host keys
    env.disable_known_hosts = False

    # use vagrant ssh key
    env.key_filename = '~/.vagrant.d/insecure_private_key'

@task
def lamp(database='mysql', http='nginx', language='php5'):
    # Update our apt repos, they could REALLY old.
    sudo('apt-get update')

    # Install the Database server
    if database == 'mysql':
        mysql()
    else:
        abort('Database Server Selected is Unavailable: %s', database)

    # Install the http server
    if http == 'nginx':
        nginx()
    else:
        abort('Http Server Selected is Unavailable: %s', http)

    # Install the dev language of choice
    if language == 'php5':
        php5(http)
    else:
        abort('Developement Language Selected is Unavailable: %s', language)

def mysql():
    sudo('apt-get install mysql-server')
    sudo('apt-get install mysql-client')

def nginx():
    sudo('apt-get install nginx')

def php5(http):
    if http == 'nginx':
        sudo('apt-get install php5-fpm')