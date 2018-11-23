import click

from app import db
from app import alembic

from app.units.auth.models.user_module import User
from app.units.auth.models.role_module import Role
from app.utils.guid_module import GUID


# Does upgrade or create (NOT both!)

def reinit_db(db_option=''):
    if db_option == 'update':
        print('updating database')
        alembic.revision('made changes')
        alembic.upgrade()
    elif db_option == 'create': 
        print('dropping all')
        db.drop_all() 
        print('recreating all')
        db.create_all()
 
        admin_role = Role(name = 'Admin')
        user_role = Role(name = 'User', is_default = True)
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()