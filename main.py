from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '777777777777777'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Location', validators=[URL()])
    open_time = StringField('Open Time', validators=[DataRequired()])
    closing_time = StringField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField(
        'Coffee Rating',
        choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕']
    )
    wifi_rating = SelectField(
        'Wifi Rating',
        choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'])
    power_outlet_rating = SelectField(
        'Power Rating',
        choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌']
    )
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe_data = [
            form.cafe.data,
            form.location_url.data,
            form.open_time.data,
            form.closing_time.data,
            form.coffee_rating.data,
            form.wifi_rating.data,
            form.power_outlet_rating.data
        ]
        f = open('cafe-data.csv', "a", encoding="utf8")
        f.write('\n')
        f.write(','.join(cafe_data))
        f.close()
        return redirect(url_for('add_cafe'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        count_row = len(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows, len=count_row)


if __name__ == '__main__':
    app.run(debug=True)
