from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash
from bs4 import BeautifulSoup
import datetime
import scraper

app = Flask(__name__)
now = datetime.datetime.now()

@app.route('/')
def hello_world():
	return render_template('layout.html')

@app.route('/class/<int:classchoice>')
def class_choice(classchoice):
	choice = scraper.getClassSchedule(classchoice)
	return render_template('scheduleViewer.html', choice=choice, now=now, classchoice=classchoice)

@app.route('/teacher/<teacherchoice>')
def teacher_choice(teacherchoice):
	return render_template('scheduleViewer.html', choice=teacherchoice)

if __name__ == '__main__':
	app.debug = True
	app.run()