from flask_login import login_required
from flask import render_template
from . import medSearch
from .forms import AtcSearchForm
from ..models import SearchedMedication
from ..downloadData import download_register, download_doping_substances


@medSearch.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = AtcSearchForm()
    download_doping_substances()
    if form.validate_on_submit():
        SearchedMedication.insert_medication(download_register(), form.atcCode.data)
    return render_template('medSearch/search.html', form=form)
