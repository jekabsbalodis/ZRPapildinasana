'''Application for preparing the necessary file
containing information about medications' use in sports'''
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


import sys
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
@click.option('--coverage/--no-coverage', default=False, help='Run tests under code coverage.')
@click.argument('test_names', nargs=-1)
def test(coverage, test_names):
    '''Run the unit tests.'''
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@app.cli.command()
def scheduled():
    '''Run scheduled tasks'''
    # Schedule task to update Notes Fields table
    from app import models
    from app import download_data
    models.NotesFields.update_notes(
        download_data.download_register(),
        download_data.download_doping_substances())


@app.cli.command()
def deploy():
    '''Run deployment tasks'''
    # migrate database to the latest version
    upgrade()
    # create or update user roles
    Role.insert_roles()


@app.cli.command()
def unchecked():
    '''Task to search for unchecked medication'''
    import pandas as pd
    from app import download_data
    # Import register of human medicines
    df_products = pd.read_json(
        download_data.download_register(), encoding='utf-8-sig')
    df_products.drop_duplicates(  # pylint: disable=E1101
        subset=['authorisation_no'], ignore_index=True, inplace=True)
    df_products_columns = ['medicine_name',
                           'authorisation_no',
                           'pharmaceutical_form_lv',
                           'active_substance']
    df_products.drop(columns=[  # pylint: disable=E1101
                     col for col in df_products if col not in df_products_columns], inplace=True)
    df_products.fillna('', inplace=True)  # pylint: disable=E1101

    # Import file with information with use in sports
    df_doping = pd.read_csv(download_data.download_doping_substances())

    # Return dataframe with products that do not have information about use in sports
    matching_rows = df_products[df_products['authorisation_no'].isin(
        df_doping['authorisation_no'])]
    df_filtered = df_products[~df_products.index.isin(  # pylint: disable=E1101
        matching_rows.index)]

    # Write information to csv file
    df_filtered.to_csv('unchecked.csv', index=False)
