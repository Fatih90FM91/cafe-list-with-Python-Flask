from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Length
import csv

# app = Flask(__name__)
# app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# Bootstrap(app)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
    Bootstrap(app)

    return app

app = create_app()



class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired(), Length(min=6, max=200)])
    location = StringField(label='Cafe Location', validators=[DataRequired(), URL(require_tld=False, message='please enter valid URL!')])
    time = StringField('Opening Time', validators=[DataRequired()])
    close = StringField('Closing Time', validators=[DataRequired()])
    coffee_rate = StringField('Coffee Rating', validators=[DataRequired()])
    wifi_rating = StringField('Wifi Strength Rating', validators=[DataRequired()])
    power_socket = StringField('Power Socket Availability', validators=[DataRequired()]) #label='Email',


    submit = SubmitField(label='submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/table")
def table():
    return render_template("table.html")




@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()

    print(request.method)

    if request.method == 'POST':
        if 'submit' in request.form:
            if form.validate_on_submit():

                print(request.form['cafe'])

                print(form.cafe.data)
                context = form.cafe.data + ',' + form.location.data + ',' + form.time.data + ',' + form.close.data + \
                ',' + form.coffee_rate.data + ',' + form.wifi_rating.data + ',' + form.power_socket.data

                with open(r"cafe-data.csv", "a", newline='', encoding="utf8") as csv_file:
                    csv_data = csv_file.write(context)

                with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
                    csv_data = csv.reader(csv_file, delimiter=',')
                    list_of_rows = []
                    for row in csv_data:
                        list_of_rows.append(row)

                    print(list_of_rows[0])
                    length_of_list = len(list_of_rows)
                return render_template('cafes.html', cafes=list_of_rows, length_list=length_of_list)





    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)

        print(list_of_rows[0])
        length_of_list = len(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows, length_list=length_of_list)


if __name__ == '__main__':
    app.run(debug=True)
