#!flask/bin/python
import os
import json
import csv
import random
import string
import numpy as np
import cv2
import imutils
from pyimagesearch.shapedetector import ShapeDetector
from flask import Flask, jsonify, send_from_directory, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path

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

# upload sample of the exam paper
@app.route('/api/upload/sample', methods=['POST'])
def upload_sample_file():
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
        page = convert_from_path(file_path, 500)[0]
        sample_path = os.path.join(app.config['UPLOAD_FOLDER'], 'sample')
        page.save(sample_path, 'png')
        PROJECTS_DETAILS[project_id]['coordinates'] = {}
        try:
            result = find_coordinates(sample_path)
            if isinstance(result, dict):
                PROJECTS_DETAILS[project_id]['coordinates'] = result
        except:
            pass
        return jsonify({'msg': 'ok'})
    else:
        return jsonify({'error': 'unknown file type'})

# upload photos
@app.route('/api/upload/photo', methods=['POST'])
def upload_photo_file():
    project_id = str(request.headers['Project-Id'])
    if project_id not in PROJECTS_DETAILS:
        return
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
        coord = PROJECTS_DETAILS[project_id]['coordinates']
        try:
            result = analyse_image(file_path, coord)
            if not isinstance(result, dict):
                PROJECTS_DETAILS[project_id]['errors'].append(file_path)
        except:
            PROJECTS_DETAILS[project_id]['errors'].append(file_path)
        result = analyse_image(file_path)
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

# uploaded files
@app.route('/uploads/<path:path>')
def uploaded_files(path):
    return send_from_directory('uploads', path)

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

# update marks
@app.route('/api/mark/update', methods=['POST'])
def update_mark():
    data = request.get_data()
    data_obj = json.loads(data)
    
    project_id = data_obj['project_id']
    student_number = data_obj['student_number']
    questions = data_obj['questions']

    for i in range(len(PROJECTS_DETAILS[project_id]['users_list'])):
        user = PROJECTS_DETAILS[project_id]['users_list'][i]
        if user['student number'] == student_number:
            PROJECTS_DETAILS[project_id]['users_list'][i]['marks'] = questions

    print(project_id, student_number, questions)
    return jsonify({'status': 'ok'})

# simply check if you can ping the server
@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({'pong': 'ok'})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_users_list_from_csv_file(file_path):
    student_number_index = 0
    username_index = 1
    first_name_index = 2
    last_name_index = 3
    users_list = []
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                is_header = False
                for col in row:
                    col_name = col.strip().lower()
                    if (col_name == 'student number'):
                        student_number_index = row.index(col)
                        is_header = True
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
                'student number': row[student_number_index],
                'username': row[username_index],
                'first name': row[first_name_index],
                'last name': row[last_name_index],
                'coordinates': {},
                'marks': []
            })
            line_count += 1
    return users_list

def random_string(stringLength):
    return ''.join(random.choice(['0','1','2', '3', '4', '5', '6', '7', '8', '9']) for i in range(stringLength))

def find_coordinates(image_path):
    width = 1200
    height = 1600

    result = {}

    orig_image = cv2.imread(image_path)
    image = cv2.resize(orig_image, (width, height))

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    #thresh = cv2.threshold(blurred,127,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
    edged = cv2.Canny(blurred, 75, 200)
    #cv2.imshow("Original", cv2.resize(edged, (600, 800)))

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()

    rectso = []
    for c in cnts:
        M = cv2.moments(c)

        if (M["m00"] == 0):
            continue

        #cv2.drawContours(image, [c], -1, (255, 0, 0), -1)

        cX = int((M["m10"] / M["m00"]))
        cY = int((M["m01"] / M["m00"]))
        shape = sd.detect(c)

        if shape == "rectangle" or shape == "square":
            x,y,w,h = cv2.boundingRect(c)
            if h > 20 and h < 40 and w > 20 and w < 40:
                rectso.append((x, y, w, h))
                cv2.drawContours(image, [c], -1, (255, 0, 0), -1)
                cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
                print(shape, cX, cY)

    print(len(rectso))

    if len(rectso) != 4:
        return "ERROR"

    if len(rectso) == 4:
        top_two_points = []
        bottom_two_points = []
        lowest_y = 12000
        for p in rectso:
            if p[1] < lowest_y:
                lowest_y = p[1]

        for p in rectso:
            if p[1] < lowest_y+100 and p[1] > lowest_y-100:
                top_two_points.append(p)
            else:
                bottom_two_points.append(p)

        if top_two_points[0][0] > top_two_points[1][0]:
            top_two_points[0], top_two_points[1] = top_two_points[1], top_two_points[0]

        if bottom_two_points[0][0] > bottom_two_points[1][0]:
            bottom_two_points[0], bottom_two_points[1] = bottom_two_points[1], bottom_two_points[0]

        print(top_two_points)
        print(bottom_two_points)

        result['tr'] = (top_two_points[0][0] + top_two_points[0][2], top_two_points[0][1])
        result['tl'] = (top_two_points[1][0], top_two_points[1][1])
        result['br'] = (bottom_two_points[0][0] + bottom_two_points[0][2], bottom_two_points[0][1] + bottom_two_points[0][3])
        result['bl'] = (bottom_two_points[1][0], bottom_two_points[1][1] + bottom_two_points[1][3])

        print(result)

    return result

def analyse_image(image_path, coord):
    if not coord:
        return 'NO COORD'

    # global vars
    width = 1200
    height = 1600
    output_path = './output'
    debug_on = True

    result = {}

    print(image_path)

    if (debug_on):
        print("Debug is enabled.")

    orig_image = cv2.imread(image_path)
    image = cv2.resize(orig_image, (width, height))

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    #thresh = cv2.threshold(blurred,127,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
    edged = cv2.Canny(blurred, 75, 200)
    cv2.imwrite(output_path + '/thresh.png', edged)
    #cv2.imshow("Original", cv2.resize(edged, (600, 800)))

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()

    rectso = []
    for c in cnts:
        M = cv2.moments(c)

        if (M["m00"] == 0):
            continue

        #cv2.drawContours(image, [c], -1, (255, 0, 0), -1)

        cX = int((M["m10"] / M["m00"]))
        cY = int((M["m01"] / M["m00"]))
        shape = sd.detect(c)

        if shape == "rectangle" or shape == "square":
            x,y,w,h = cv2.boundingRect(c)
            if h > 20 and h < 40 and w > 20 and w < 40:
                rectso.append((x, y, w, h))
                cv2.drawContours(image, [c], -1, (255, 0, 0), -1)
                cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
                print(shape, cX, cY)

    print(len(rectso))

    if len(rectso) != 4:
        return "ERROR"

    if len(rectso) == 4:
        top_two_points = []
        bottom_two_points = []
        lowest_y = 12000
        for p in rectso:
            if p[1] < lowest_y:
                lowest_y = p[1]

        for p in rectso:
            if p[1] < lowest_y+100 and p[1] > lowest_y-100:
                top_two_points.append(p)
            else:
                bottom_two_points.append(p)

        if top_two_points[0][0] > top_two_points[1][0]:
            top_two_points[0], top_two_points[1] = top_two_points[1], top_two_points[0]

        if bottom_two_points[0][0] > bottom_two_points[1][0]:
            bottom_two_points[0], bottom_two_points[1] = bottom_two_points[1], bottom_two_points[0]

        print(top_two_points)
        print(bottom_two_points)

        p0 = (top_two_points[0][0] + top_two_points[0][2], top_two_points[0][1])
        p2 = (top_two_points[1][0], top_two_points[1][1])
        p1 = (bottom_two_points[0][0] + bottom_two_points[0][2], bottom_two_points[0][1] + bottom_two_points[0][3])
        p3 = (bottom_two_points[1][0], bottom_two_points[1][1] + bottom_two_points[1][3])

        print(p0, p1, p2, p3)

        cv2.circle(image, (int(p0[0]),int(p0[1])), int(4), (0,0,255))
        cv2.circle(image, (int(p1[0]),int(p1[1])), int(4), (0,0,255))
        cv2.circle(image, (int(p2[0]),int(p2[1])), int(4), (0,0,255))
        cv2.circle(image, (int(p3[0]),int(p3[1])), int(4), (0,0,255))

        pts1 = np.float32([[p0[0], p0[1]], [p1[0], p1[1]], [p2[0], p2[1]], [p3[0], p3[1]]])
        pts2 = np.float32([[0, 0], [0, 430], [420, 0], [420, 430]])
        M, status = cv2.findHomography(pts1, pts2)
        dst = cv2.warpPerspective(image, M, (430, 420))

        dst2 = dst
        dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        dst = cv2.GaussisdanBlur(dst, (5, 5), 0)
        dst = cv2.threshold(dst,127,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]

        #cv2.imshow("New Image", dst)

        studentNumber = '_'*10
        def_x = 18
        def_y = 10
        counter_x = def_x
        counter_y = def_y
        for i in range(10):
            counter_x = def_x
            counter_y += 18.5
            for j in range(10):
                avg = np.mean(dst[int(counter_y)-4:int(counter_y)+8,int(counter_x)-4:int(counter_x)+8])
                if avg and avg > 200:
                    print('row:', i, 'col:', j, 'value:', avg)
                    studentNumber = studentNumber[:j] + str(i) + studentNumber[j+1:]
                    cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,0,255))
                else:
                    cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,255,0))
                cv2.rectangle(dst2,(int(counter_x)-4,int(counter_y)-4),(int(counter_x)+8,int(counter_y)+8),(255,0,0))
                counter_x += 19

        print('Student Number: ', studentNumber)
        result['student_id'] = studentNumber

        q1Number = '_'*2
        def_x = 18
        def_y = 210
        counter_x = def_x
        counter_y = def_y
        for i in range(2):
            counter_x = def_x
            counter_y += 18.5
            for j in range(10):
                avg = np.mean(dst[int(counter_y)-4:int(counter_y)+8,int(counter_x)-4:int(counter_x)+8])
                if avg and avg > 200:
                    print('row:', i, 'col:', j, 'value:', avg)
                    q1Number = q1Number[:i] + str(j) + q1Number[i+1:]
                    cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,0,255))
                else:
                    cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,255,0))
                cv2.rectangle(dst2,(int(counter_x)-4,int(counter_y)-4),(int(counter_x)+8,int(counter_y)+8),(255,0,0))
                counter_x += 19

        result['question_marks'] = []
        result['question_marks'].append(q1Number)
        print('Q1: ', q1Number)

        q2Number = '_'*2
        def_x = 18
        def_y = 250
        counter_x = def_x
        counter_y = def_y
        for i in range(2):
            counter_x = def_x
            counter_y += 18.5
            for j in range(10):
                avg = np.mean(dst[int(counter_y)-4:int(counter_y)+8,int(counter_x)-4:int(counter_x)+8])
                if avg and avg > 200:
                    print('row:', i, 'col:', j, 'value:', avg)
                    q2Number = q2Number[:i] + str(j) + q2Number[i+1:]
                    cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,0,255))
                else:
                    cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,255,0))
                cv2.rectangle(dst2,(int(counter_x)-4,int(counter_y)-4),(int(counter_x)+8,int(counter_y)+8),(255,0,0))
                counter_x += 19

        result['question_marks'].append(q2Number)
        print('Q2: ', q2Number)

        def_x = 18
        def_y = 290
        counter_x = def_x
        counter_y = def_y
        for i in range(2):
            counter_x = def_x
            counter_y += 18.5
            for j in range(10):
                avg = np.mean(dst[int(counter_y)-4:int(counter_y)+8,int(counter_x)-4:int(counter_x)+8])
                if avg and avg > 200:
                    print('row:', i, 'col:', j, 'value:', avg)
                    cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,0,255))
                else:
                    cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,255,0))
                cv2.rectangle(dst2,(int(counter_x)-4,int(counter_y)-4),(int(counter_x)+8,int(counter_y)+8),(255,0,0))
                counter_x += 19

        #cv2.imshow("New Image 2", dst2)

    cv2.imwrite(output_path + '/result.png', cv2.resize(image, (600, 800)))
    #cv2.imshow("Image", cv2.resize(image, (600, 800)))

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0')