import click
from flask import send_from_directory
from flask.cli import with_appcontext
from app import create_app, init_db

app = create_app()


@app.cli.command()
@with_appcontext
@click.option('-u', 'dboption', flag_value='upgrade',
              default='')
@click.option('-c', 'dboption', flag_value='create',
              default='')
def dbinit(dboption):
    print('init db', dboption)
    init_db(dboption, app)