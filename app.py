"""
Main file of Dashboard, an schedule viewer for ABB Industrigymnasium
developed by Emil Tullstedt as a hobby project.

This project has no affliation with the school to do whatsoever.

(C) 2012-2013 Emil Tullstedt
"""

from flask import Flask, render_template
import os

APP = Flask(__name__)


@APP.route('/')
def class_list():
    """
    Output: HTML-formatted classlist and main page
    """
    return render_template('classList.html', classList=CLASSLIST)


@APP.route('/c/<int:classchoice>/')
@APP.route('/c/<int:classchoice>/<int:datechoice>/')
def class_choice(classchoice=None, datechoice=None):
    """
    Input: classchoice (4[0-9]) and datechoice (6-8[0-9])
    Output: HTML-formatted single day eventlist
    """
    return "TBD" + str(classchoice) + str(datechoice)

if __name__ == '__main__':
    APP.debug = True
    if not APP.debug:
        PORT = int(os.environ.get('PORT', 5000))
        APP.run(host='0.0.0.0', port=PORT)
    else:
        APP.run()
