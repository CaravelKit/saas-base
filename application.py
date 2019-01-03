import click
from flask import send_from_directory, current_app
from flask.cli import with_appcontext
from app import create_app, init_db, init_app_path

application = create_app()

@application.cli.command()
@with_appcontext
def dbupdate():
    print('update db')
    init_db('update', application)

@application.cli.command()
@with_appcontext
def dbcreate():
    print('create db')
    init_db('create', application)


@application.cli.command()
@with_appcontext
@click.argument('interface_element')
@click.option('-u', 'option', flag_value='update',
              default='')
def scaffold(interface_element, option):
    from scaffold.generators.interface import generate
    init_app_path(current_app.root_path)
    generate(interface_element, option)


# to-do:
# To make it work with application.py I need to change set FLASK_APP=main to set FLASK_APP=application in venv