import os
import click
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import User, Role, Permission


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission)


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
    '''Run scheduled task.'''
    # Schedule task to update Notes Fields table
    from app import models
    from app import downloadData
    downloadData.download_doping_substances()
    downloadData.download_register()
    models.NotesFields.update_notes(
        'HumanProducts.xml', 'antidopinga_vielas.csv')


@app.cli.command()
def deploy():
    '''Run deployment tasks'''
    # migrate database to the latest version
    upgrade()
    # create or update user roles
    Role.insert_roles()
