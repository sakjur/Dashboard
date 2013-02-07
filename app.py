"""
Main file of Dashboard, an schedule viewer for ABB Industrigymnasium
developed by Emil Tullstedt as a hobby project.

This project has no affliation with the school to do whatsoever.

(C) 2012-2013 Emil Tullstedt
"""

from flask import Flask, render_template
import os
import scraper
import data

APP = Flask(__name__)
CLASSLIST = sorted(data.classList().keys())


@APP.route('/')
@APP.route('/class/')
def class_list():
    """
    Output: HTML-formatted classlist and main page
    """
    return render_template('classList.html', classList=CLASSLIST)


@APP.route('/<int:classchoice>/')
@APP.route('/<int:classchoice>/<int:datechoice>/')
@APP.route('/class/<int:classchoice>/')
@APP.route('/class/<int:classchoice>/<int:datechoice>/')
def class_choice(classchoice=None, datechoice=None):
    """
    Input: classchoice (4[0-9]) and datechoice (6-8[0-9])
    Output: HTML-formatted single day eventlist
    """
    datechoice = str(datechoice)
    choice = scraper.getClassSchedule(classchoice, datechoice)
    return render_template('scheduleViewer.html', choice=choice,
                           datechoice=datechoice, classchoice=classchoice,
                           classList=CLASSLIST)

if __name__ == '__main__':
    APP.debug = True
    if not APP.debug:
        PORT = int(os.environ.get('PORT', 5000))
        APP.run(host='0.0.0.0', port=PORT)
    else:
        APP.run()
