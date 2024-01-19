'''Application for preparing the necessary file
containing information about medications' use in sports'''
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


import click
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import User, Role, Permission


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role, 'Permission': Permission}


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    '''Run the unit tests.'''
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def scheduled():
    '''Run scheduled tasks'''
    # Schedule task to update Notes Fields table
    from app import models
    from app import download_data
    download_data.download_doping_substances()
    download_data.download_register()
    models.NotesFields.update_notes(
        'HumanProducts.xml', 'antidopinga_vielas.csv')


@app.cli.command()
def deploy():
    '''Run deployment tasks'''
    # migrate database to the latest version
    upgrade()
    # create or update user roles
    Role.insert_roles()