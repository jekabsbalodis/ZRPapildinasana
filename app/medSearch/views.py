from flask_login import login_required
from flask import render_template
from . import medSearch
from .forms import AtcSearchForm


@medSearch.route('/start', methods=['GET', 'POST'])
@login_required
def start():
    form = AtcSearchForm()
    return render_template('medSearch/start.html', form=form)
