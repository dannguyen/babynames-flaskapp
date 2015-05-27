from flask import Flask
from flask_frozen import Freezer

from flask import render_template
from flask import request
from flask import redirect
from urllib.parse import quote_plus, unquote_plus

import csv
from data_scripts.settings import get_all_names_by_sex, load_data_by_sex_and_name, make_image_uri

app = Flask(__name__)



@app.route("/")
def index():
    return render_template('index.html', names_by_sex = get_all_names_by_sex())

@app.route('/<sex>/<name>/')
def sex_name(sex, name):
    history = load_data_by_sex_and_name(sex, name)
    years = [h['year'] for h in history]
    counts = [h['per_100k'] for h in history]
    return render_template('sex_name.html', name = name, sex = sex,
                                history = history,
                                chart_url = make_image_uri(years, counts)

                                )



if __name__ == '__main__':
    app.run(debug = True, use_reloader = True)


