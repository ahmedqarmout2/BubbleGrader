#!flask/bin/python
import os
import json
import csv
import random
import string
import numpy as np
import cv2
from flask import Flask, jsonify, send_from_directory, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

app = Flask(__name__)
app.secret_key = 'super secret key lol'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

PROJECTS_DETAILS = {}

# get projects list
@app.route('/api/projects/list')
def get_projects_list():
    project_list = []
    for key in PROJECTS_DETAILS:
        project_info = PROJECTS_DETAILS[key]
        project_list.append({
            'id': project_info['id'],
            'name': project_info['name']
        })
    return jsonify({'projects_list': project_list})

# upload class list files
@app.route('/api/upload/classlist', methods=['POST'])
def upload_classlist_file():
    if 'file' not in request.files:
        flash('No file part')
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    project_id = request.form['id']
    if file.filename == '':
        flash('No selected file')
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        users_list = get_users_list_from_csv_file(file_path)
        PROJECTS_DETAILS[project_id]['users_list'] = users_list
        return jsonify({'msg': 'ok'})
    else:
        return jsonify({'error': 'unknown file type'})

# upload photos
@app.route('/api/upload/photo', methods=['POST'])
def upload_photo_file():
    if 'photo' not in request.files:
        flash('No file part')
        return jsonify({'error': 'No file part'})
    file = request.files['photo']
    if file.filename == '':
        flash('No selected file')
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'msg': 'ok'})
    else:
        return jsonify({'error': 'unknown file type'})

#serve home page
@app.route('/')
def home_page():
    return send_from_directory('.', 'index.html')

#serve fav icon
@app.route('/favicon.ico')
def fav_icon():
    return send_from_directory('.', 'favicon.ico')

# serve fonts files
@app.route('/mdb/<path:path>')
def mdb_files(path):
    return send_from_directory('mdb', path)

# serve mdb files
@app.route('/webfonts/<path:path>')
def fonts_files(path):
    return send_from_directory('fonts', path)

# serve js files
@app.route('/js/<path:path>')
def js_files(path):
    return send_from_directory('js', path)

# serve css files
@app.route('/css/<path:path>')
def css_files(path):
    return send_from_directory('css', path)

# get the data for a project
@app.route('/api/project/data/<project_id>')
def project_data(project_id):
    return jsonify(PROJECTS_DETAILS[project_id])

# create a new project
@app.route('/api/project/create', methods=['POST'])
def create_project():
    data = request.get_data()
    data_obj = json.loads(data)
    project_id = random_string(6).lower()
    project = {
        'id': project_id,
        'name': data_obj['project_name'],
        'users_list': [],
        'marks': [],
        'errors': [],
        'student_number_length': 10,
        'number_of_questions': 5
    }
    PROJECTS_DETAILS[project_id] = project
    return jsonify({'status': 'ok'})

# update project details
@app.route('/api/project/update', methods=['POST'])
def update_project():
    data = request.get_data()
    data_obj = json.loads(data)
    project_id = data_obj['id']
    PROJECTS_DETAILS[project_id]['student_number_length'] = data_obj['student_number_length']
    PROJECTS_DETAILS[project_id]['number_of_questions'] = data_obj['number_of_questions']
    return jsonify({'status': 'ok'})

# simply check if you can ping the server
@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({'pong': 'ok'})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_users_list_from_csv_file(file_path):
    username_index = 0
    first_name_index = 1
    last_name_index = 2
    users_list = []
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                is_header = False
                for col in row:
                    col_name = col.strip().lower()
                    if (col_name == 'username'):
                        username_index = row.index(col)
                        is_header = True
                    if (col_name == 'first name'):
                        first_name_index = row.index(col)
                        is_header = True
                    if (col_name == 'last name'):
                        last_name_index = row.index(col)
                        is_header = True
                if is_header:
                    continue
            users_list.append({
                'username': row[username_index],
                'first name': row[first_name_index],
                'last name': row[last_name_index]
            })
            print(", ".join(row))
            line_count += 1
        print('Processed lines: ', line_count)
    return users_list

def random_string(stringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def analyse_image(path):
    # global vars
    WIDTH = 1200
    HEIGHT = 1600
    OUTPUT_PATH = './output'
    image_path = path
    debug_on = True

    if (debug_on):
        print("Debug is enabled.")

    # read original image into an array
    orig_image = cv2.imread(image_path)

    # resize image. Full size image will have too much details and noise
    # resizing the image helps the detection of circles and other shapes
    image = cv2.resize(orig_image, (WIDTH, HEIGHT))

    # apply filters to help the detection process
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred,127,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
    edged = cv2.Canny(thresh, 75, 200)

    img = cv2.imread(image_path,0)
    img = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=30) 
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        avg = np.mean(img[i[1]-10:i[1]+10,i[0]-10:i[0]+10])
        if avg and avg < 100:
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

    # display the original image after applying the filter
    # used for debugging
    if (debug_on):
        print(circles)
        cv2.imwrite(OUTPUT_PATH + '/thresh.png', cimg)
        cv2.imshow("Original Image", cv2.resize(cimg, (600, 800)))
        cv2.waitKey(0)

if __name__ == '__main__':
    app.run(host='0.0.0.0')