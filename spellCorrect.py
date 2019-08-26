import os
import numpy as np
import flask
import pickle
from flask import Flask, render_template, request
import spellCorrect_helper_code as ss
from wtforms import Form, FloatField, validators


app=Flask(__name__)

@app.route('/')
@app.route('/index')

def index():
    return flask.render_template('input.html')

	
@app.route('/index', methods = ['POST'])	

def result():
    #form = InputForm(request.form)
    if request.method == 'POST':
        
        input_word = request.form["input_string"] 
        
        suggestions = ss.spell_suggestion(input_word)
        return render_template("input.html", input_word = input_word, suggestions=suggestions)
		
if __name__ == '__main__':
	app.run(debug=False)
