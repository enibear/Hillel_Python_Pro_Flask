from flask import Flask, render_template, request
from faker import Faker
import csv
import requests
import json


app = Flask(__name__)
fake = Faker()


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/requirements')
def requirements():
    return render_template("requirements.html")


@app.route('/requirements/', methods=['POST'])
def open_file():
    file = request.files['file']
    if file:
        content = [line.decode() for line in file]
        return render_template('requirements.html', file_content=content)
    else:
        return render_template('requirements.html', file_content='')


@app.route('/generate-users')
def generate_users():
    return render_template("generate_users.html")


@app.route('/generate-users/', methods=['GET'])
def process_form():
    input_data = request.args.get("count")
    data_user = []
    if int(input_data) > 0:
        for i in range(int(input_data)):
            record = fake.name() + " - " + fake.email()
            data_user.append(record)
    return render_template('generate_users.html', content=data_user)


@app.route('/mean')
def mean():
    return render_template('mean.html')


@app.route('/mean/', methods=['POST'])
def open_mean_file():
    total_height = 0
    total_weight = 0
    with open("hw.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                height_value = float(row[1])
                weight_value = float(row[2])
                total_height += height_value
                total_weight += weight_value
            except (ValueError, IndexError):
                pass
    total_height = total_height*2.54
    total_weight = total_weight*0.45359237
    total = str(total_height) + " sm / " + str(total_weight) + " kg"
    return render_template('mean.html', content=total)


@app.route('/space')
def space():
    return render_template('space.html')

@app.route('/space/', methods=['POST'])
def space_people():
    response = requests.get('http://api.open-notify.org/astros.json')
    data = response.text
    data_dict = json.loads(data)
    people = data_dict["number"]
    print(people)
    return render_template('space.html', content=people)

if __name__ == "__main__":
    app.run(debug=True)
