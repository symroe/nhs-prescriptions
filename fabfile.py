import sys

from fabric.api import *
from fabric.colors import red, green
import requests

web = ['openhealthcare.org.uk']
serves = [
    'http://openhealthcare.org.uk',
    'http://prescriptions.openhealthcare.org.uk'
    ]

def manage(what):
    """
    Run a manage.py command

    Return: None
    Exceptions: None
    """
    with cd('/var/apps/nhs-prescriptions/nhs-prescriptions/nhs'):
        run('./venv/bin/python manage.py {0}'.format(what))


@hosts(web)
def deploy():
    """
    Make it so!

    Return: None
    Exceptions: None
    """
    # FIXME stop deploying out of git for atomicity.
    with cd('/var/apps/nhs-prescriptions/nhs-prescriptions'):
        sudo('git pull github master') #not ssh - key stuff
        sudo('chown ross:ross .') # !!! FIXME
        sudo('/etc/init.d/apache2 reload')
    for site in serves:
        req = requests.get(site)
        if req.status_code != 200:
            print red("Cripes! something just blew up Larry! ({0})".format(site))
            sys.exit(1)
    print green("Deploy-o-rama!")



@hosts(web)
def migrate():
    """
    Update to latest please

    Return: None
    Exceptions: None
    """
    manage('syncdb')
    manage('migrate')
    manage('create_groups')
