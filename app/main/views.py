'''View functions for start page'''
from flask import render_template
from . import main


@main.route('/', methods=['GET'])
def index():
    '''View function for start page'''
    return render_template('index.html')
