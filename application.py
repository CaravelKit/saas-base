import click
from flask import send_from_directory
from flask.cli import with_appcontext
from app import create_app, init_db

application = create_app()


@application.cli.command()
@with_appcontext
@click.option('-u', 'dboption', flag_value='upgrade',
              default='')
@click.option('-c', 'dboption', flag_value='create',
              default='')
def dbinit(dboption):
    print('init db', dboption)
    init_db(dboption, application)

@application.cli.command()
@with_appcontext
@click.argument('interface_element')
@click.option('-u', 'option', flag_value='update',
              default='')
def scaffold(interface_element, option):
    from scaffold.generators.interface import generate
    generate(interface_element, option)

# to-do:
# To make it work with application.py I need to change set FLASK_APP=main to set FLASK_APP=application in venv