from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash
import datetime, os
import scraper, dateparser

app = Flask(__name__)
now = datetime.datetime.now()

@app.route('/')
def hello_world():
	return render_template('layout.html')

@app.route('/class/')
def class_list():
	classList = scraper.classList()
	return render_template('classList.html', classList=classList)

@app.route('/class/<int:classchoice>/')
@app.route('/class/<int:classchoice>/<int:datechoice>/')
def class_choice(classchoice=None, datechoice=None):
	datechoice = dateparser.parseDate(str(datechoice))
	choice = scraper.getClassSchedule(classchoice, datechoice)
	return render_template('scheduleViewer.html', choice=choice, datechoice=datechoice, classchoice=classchoice)

@app.route('/teacher/<teacherchoice>')
def teacher_choice(teacherchoice):
	return render_template('scheduleViewer.html', choice=teacherchoice)

if __name__ == '__main__':
	app.debug = False
	if app.debug == False:
		port = int(os.environ.get('PORT', 5000))
		app.run(host='0.0.0.0', port=port)
	else:
		app.run()