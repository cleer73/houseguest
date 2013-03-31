from fabric.api import *

@task
def vagrant(boot=True, destroy=False):
    if destroy: local('vagrant destroy')
    if boot: local('vagrant up')

    # change from the default user to 'vagrant'
    env.user = 'vagrant'

    # connect to the port-forwarded ssh
    env.hosts = ['127.0.0.1:2222']

    # Disable cached host keys
    env.disable_known_hosts = True

    # use vagrant ssh key
    env.key_filename = '~/.vagrant.d/insecure_private_key'

@task
def build(db='mysql', http='nginx', lang='php'):
    # Update our apt repos, they could REALLY old.
    system_update()

    # Install the Database server
    if db == 'mysql':
        mysql()
    else:
        abort('Database Server Selected is Unavailable: %s', database)

    # Install the http server
    if http == 'nginx':
        nginx()
    else:
        abort('Http Server Selected is Unavailable: %s', http)

    # Install the dev language of choice
    if lang == 'php':
        php5(http)
    else:
        abort('Developement Language Selected is Unavailable: %s', lang)

@task
def config(db='mysql', http='nginx', lang='php'):
    if http == 'nginx' and lang == 'php':
        # Stop Services
        sudo('service php5-fpm stop')
        sudo('service nginx stop')

        # Upload Nginx conf
        put('./configs/nginx.php.conf', '/etc/nginx/sites-available/default', use_sudo=True)
        sudo('chmod 0644 /etc/nginx/sites-available/default')

        # Upload PHP5-FPM conf
        put('./configs/php-fpm.conf', '/etc/php5/fpm/pool.d/www.conf', use_sudo=True)
        sudo('chmod 0644 /etc/php5/fpm/pool.d/www.conf')

        # Start Services
        sudo('service nginx start')
        sudo('service php5-fpm start', pty=False)

        # Show Service Status
        sudo('service nginx status')
        sudo('service php5-fpm status')
    else:
        abort('Unknown configuration (db:%s, http:%s, lang:%s)', db, http, lang)

def mysql():
    # Set the MySQL root password
    mysql_password = prompt('MySQL root Password?', default='')
    sudo('echo "mysql-server-5.5 mysql-server/root_password password %s" | debconf-set-selections' % mysql_password)
    sudo('echo "mysql-server-5.5 mysql-server/root_password_again password %s" | debconf-set-selections' % mysql_password)

    # Install mysql server & client
    system_install('mysql-server')

def maria():
    # Set the MySQL root password
    mysql_password = prompt('MySQL root Password?', default='')
    sudo('echo "mysql-server-5.5 mysql-server/root_password password %s" | debconf-set-selections' % mysql_password)
    sudo('echo "mysql-server-5.5 mysql-server/root_password_again password %s" | debconf-set-selections' % mysql_password)

    system_install('python-software-properties')
    sudo('apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db')
    sudo('add-apt-repository \'deb http://ftp.osuosl.org/pub/mariadb/repo/5.5/ubuntu precise main\'')

    system_update();
    system_install('mariadb-server')

def nginx():
    system_install('nginx')

def php5(http):
    if http == 'nginx':
        system_install('php5-fpm', 'php5-mysql', 'php5-xcache')

def system_install(*packages):
    sudo('apt-get -yq install %s' % ' '.join(packages), shell=False)

def system_update():
    sudo('apt-get -yq update')
    # sudo('apt-get -yq upgrade')
