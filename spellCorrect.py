##------------- Author: Ankit Sharma, email: 27ankitsharma@gmail.com -------------##

import os
from flask import Flask, render_template, request
import spellCorrect_helper_code as ss


app=Flask(__name__)

@app.route('/')
@app.route('/index')

def index():
    "default page.." 
    return flask.render_template('input.html')

	
@app.route('/index', methods = ['POST'])	

def result():
    if request.method == 'POST':
        
        input_word = request.form["input_string"] 
        suggestions = ss.spell_suggestion(input_word)
        return render_template("input.html", input_word = input_word, suggestions=suggestions)
		
if __name__ == '__main__':
	app.run(debug=False)
