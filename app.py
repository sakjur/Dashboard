from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash
import datetime, os
import scraper, dateparser, data

app = Flask(__name__)
now = datetime.datetime.now()

@app.route('/')
@app.route('/class/')
def class_list():
	classList = sorted(data.classList().keys())
	return render_template('classList.html', classList=classList)

@app.route('/<int:classchoice>/')
@app.route('/<int:classchoice>/<int:datechoice>/')
@app.route('/class/<int:classchoice>/')
@app.route('/class/<int:classchoice>/<int:datechoice>/')
def class_choice(classchoice=None, datechoice=None):
	datechoice = str(datechoice)
	classList = sorted(data.classList().keys())
	choice = scraper.getClassSchedule(classchoice, datechoice)
	return render_template('scheduleViewer.html', choice=choice, \
		datechoice=datechoice, classchoice=classchoice, classList=classList)

if __name__ == '__main__':
	app.debug = True
	if app.debug == False:
		port = int(os.environ.get('PORT', 5000))
		app.run(host='0.0.0.0', port=port)
	else:
		app.run()