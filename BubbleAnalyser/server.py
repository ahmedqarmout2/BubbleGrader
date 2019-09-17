#!flask/bin/python
import os
import json
import csv
import random
import string
import numpy as np
import cv2
import imutils
import datetime

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

epsilon = 10 #image error sensitivity
scaling = [605.0, 835.0] #scaling factor for 8.5in. x 11in. paper

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
        return 'No file part!', 400
    file = request.files['file']
    project_id = request.form['id']
    if file.filename == '':
        return 'No selected file!', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        users_list = get_users_list_from_csv_file(file_path)
        PROJECTS_DETAILS[project_id]['users_list'] = users_list
        save_to_file()
        return jsonify({'msg': 'ok'})
    else:
        return 'Unknown file type!', 400

# upload sample of the exam paper
@app.route('/api/upload/sample', methods=['POST'])
def upload_sample_file():
    if 'file' not in request.files:
        return 'No file part!', 400
    file = request.files['file']
    project_id = request.form['id']
    if file.filename == '':
        return 'No selected file!', 400
    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], project_id + '_sample.pdf')
        file.save(file_path)
        page = convert_from_path(file_path, 500)[0]
        sample_path = os.path.join(app.config['UPLOAD_FOLDER'], project_id + '_sample.png')
        page.save(sample_path, 'png')
        PROJECTS_DETAILS[project_id]['coordinates'] = {}
        try:
            result = find_coordinates(sample_path)
            if isinstance(result, dict):
                PROJECTS_DETAILS[project_id]['coordinates'] = result
            else:
                return 'Invalid Sample. Could not locate the 4 markers, please try again!', 400
        except:
            return 'Invalid Sample. Could not locate the 4 markers, please try again!', 400
        save_to_file()
        return jsonify({'msg': 'ok'})
    else:
        return 'Unknown file type!', 400

# upload photos
@app.route('/api/upload/photo', methods=['POST'])
def upload_photo_file():
    project_id = str(request.headers['Project-Id'])
    if project_id not in PROJECTS_DETAILS:
        return 'Invalid project id!', 400
    if 'photo' not in request.files:
        return 'No file part!', 400
    file = request.files['photo']
    if file.filename == '':
        flash('No selected file')
        return 'No selected file!', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        try:
            result = analyse_image(project_id, file_path, filename.replace('.png', ''))
            if isinstance(result, dict):
                user_found = False
                for i in range(len(PROJECTS_DETAILS[project_id]['users_list'])):
                    user = PROJECTS_DETAILS[project_id]['users_list'][i]
                    if user['student number'] == result['student number']:
                        user_found = True
                        PROJECTS_DETAILS[project_id]['users_list'][i]['marks'] = result['marks']
                        PROJECTS_DETAILS[project_id]['users_list'][i]['total'] = result['total']
                        break
                if not user_found:
                    PROJECTS_DETAILS[project_id]['errors'].append(file_path)
            else:
                PROJECTS_DETAILS[project_id]['errors'].append(file_path)
        except:
            PROJECTS_DETAILS[project_id]['errors'].append(file_path)
        save_to_file()
        return jsonify({'msg': 'ok'})
    else:
        return 'Unknown file type!', 400

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

# serve marker files
@app.route('/marker/<path:path>')
def marker_files(path):
    return send_from_directory('markers', path)

# get the data for a project
@app.route('/api/project/data/<project_id>')
def project_data(project_id):
    return jsonify(PROJECTS_DETAILS[project_id])

# download exported files
@app.route('/exports/<file_name>')
def export_list(file_name):
    return send_from_directory('exports', file_name)

# create a new project
@app.route('/api/project/create', methods=['POST'])
def create_project():
    data = request.get_data()
    data_obj = json.loads(data)
    project_id = random_string(4).lower()
    project = {
        'id': project_id,
        'name': data_obj['project_name'],
        'users_list': [],
        'errors': [],
        'student_number_length': 10,
        'number_of_questions': 5,
        'show_utorid': False,
        'show_signature': False
    }
    PROJECTS_DETAILS[project_id] = project
    save_to_file()
    return jsonify({'status': 'ok'})

# update project details
@app.route('/api/project/update', methods=['POST'])
def update_project():
    data = request.get_data()
    data_obj = json.loads(data)
    project_id = data_obj['id']
    PROJECTS_DETAILS[project_id]['student_number_length'] = int(data_obj['student_number_length'])
    PROJECTS_DETAILS[project_id]['number_of_questions'] = int(data_obj['number_of_questions'])
    PROJECTS_DETAILS[project_id]['show_utorid'] = data_obj['show_utorid']
    PROJECTS_DETAILS[project_id]['show_signature'] = data_obj['show_signature']
    save_to_file()
    return jsonify({'status': 'ok'})

# update marks
@app.route('/api/mark/update', methods=['POST'])
def update_mark():
    data = request.get_data()
    data_obj = json.loads(data)
    
    project_id = data_obj['project_id']
    try:
        student_number = int(data_obj['student_number'])
    except:
        return 'Invalid student number!', 400
    
    marks = data_obj['marks']

    total = 0.0
    float_marks = []
    try:
        for mark in marks:
            float_mark = float(mark)
            float_marks.append(float_mark)
            total += float_mark
    except:
        return 'Invalid marks!', 400

    user_found = False
    for i in range(len(PROJECTS_DETAILS[project_id]['users_list'])):
        user = PROJECTS_DETAILS[project_id]['users_list'][i]
        if user['student number'] == student_number:
            user_found = True
            PROJECTS_DETAILS[project_id]['users_list'][i]['marks'] = float_marks
            PROJECTS_DETAILS[project_id]['users_list'][i]['total'] = total

    if not user_found:
        return 'User not found!', 400

    save_to_file()
    return jsonify({'status': 'ok'})

# remove image
@app.route('/api/remove/image', methods=['POST'])
def remove_image():
    data = request.get_data()
    data_obj = json.loads(data)
    
    project_id = data_obj['project_id']
    photo_path = data_obj['photo_path']

    PROJECTS_DETAILS[project_id]['errors'].remove(photo_path)
    save_to_file()
    return jsonify({'status': 'ok'})

# export class list to csv
@app.route('/api/export/classlist', methods=['POST'])
def export_csv():
    data = request.get_data()
    data_obj = json.loads(data)
    
    project_id = str(data_obj['project_id'])
    users_list = PROJECTS_DETAILS[project_id]['users_list']
    export_file_name = 'exports/' + project_id + '_' + str(datetime.datetime.now()).replace(' ', '_') + '.csv'
    number_of_questions = int(PROJECTS_DETAILS[project_id]['number_of_questions'])
    with open(export_file_name, 'w') as file:
        header = ''
        header += 'Student Number,'
        header += 'Username,'
        header += 'First Name,'
        header += 'Last Name,'
        for i in range(number_of_questions):
            header += 'Question ' + str(i + 1) + ','
        header += 'Total,'
        header = header[:-1] + '\n'
        file.write(header)
        for user in users_list:
            line = ''
            line += str(user['student number']) + ','
            line += user['username'] + ','
            line += user['first name'] + ','
            line += user['last name'] + ','
            for i in range(number_of_questions):
                if i < len(user['marks']):
                    line += str(user['marks'][i]) + ','
                else:
                    line += '0,'
            line += str(user['total']) + ','       
            line = line[:-1] + '\n'
            file.write(line)
    return jsonify({'file_name': export_file_name})

# simply check if you can ping the server
@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({'pong': 'ok'})

# checked if the file type is allowed by its extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# read the csv into an array of student objects
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
                'student number': int(row[student_number_index]),
                'username': row[username_index],
                'first name': row[first_name_index],
                'last name': row[last_name_index],
                'marks': [],
                'total': 0
            })
            line_count += 1
    return users_list

# generate a random string that consists of numbers only
def random_string(stringLength):
    return ''.join(random.choice(['0','1','2', '3', '4', '5', '6', '7', '8', '9']) for i in range(stringLength))

# find coordinates or markers in an image
def find_coordinates(image_path):
    width = int(scaling[0])
    height = int(scaling[1])

    result = {}

    orig_image = cv2.imread(image_path)
    image = cv2.resize(orig_image, (width, height))

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()

    rectso = []
    for c in cnts:
        M = cv2.moments(c)

        if (M["m00"] == 0):
            continue

        shape = sd.detect(c)

        if shape == "rectangle" or shape == "square":
            x,y,w,h = cv2.boundingRect(c)
            if h > 20 and h < 40 and w > 20 and w < 40:
                rectso.append((x, y, w, h))
                cv2.drawContours(image, [c], -1, (255, 0, 0), -1)
                cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)

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

        result['tl'] = (top_two_points[0][0] + top_two_points[0][2], top_two_points[0][1])
        result['tr'] = (top_two_points[1][0], top_two_points[1][1])
        result['bl'] = (bottom_two_points[0][0] + bottom_two_points[0][2], bottom_two_points[0][1] + bottom_two_points[0][3])
        result['br'] = (bottom_two_points[1][0], bottom_two_points[1][1] + bottom_two_points[1][3])

    return result

# locate the marking section, then look for highlighted bubbles
def analyse_image(project_id, image_path, image_name):
    if 'coordinates' not in PROJECTS_DETAILS[project_id] or not isinstance(PROJECTS_DETAILS[project_id]['coordinates'], dict):
        return "Invalid coord"

    coord = PROJECTS_DETAILS[project_id]['coordinates']

    width = int(scaling[0])
    height = int(scaling[1])

    orig_image = cv2.imread(image_path)
    image = cv2.resize(orig_image, (width, height))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    cv2.imwrite('./processing/' + image_name + '_filtered.png', edged)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    p0 = coord['tl']
    p1 = coord['tr']
    p2 = coord['bl']
    p3 = coord['br']

    cv2.circle(image, (int(p0[0]),int(p0[1])), int(4), (0,0,255))
    cv2.circle(image, (int(p1[0]),int(p1[1])), int(4), (0,0,255))
    cv2.circle(image, (int(p2[0]),int(p2[1])), int(4), (0,0,255))
    cv2.circle(image, (int(p3[0]),int(p3[1])), int(4), (0,0,255))

    cv2.imwrite('./processing/' + image_name + '_original_markers.png', image)

    piece0_dxl, piece0_dxr, piece0_dyu, piece0_dyd = calculate_marker_area(p0, width, height)
    piece1_dxl, piece1_dxr, piece1_dyu, piece1_dyd = calculate_marker_area(p1, width, height)
    piece2_dxl, piece2_dxr, piece2_dyu, piece2_dyd = calculate_marker_area(p2, width, height)
    piece3_dxl, piece3_dxr, piece3_dyu, piece3_dyd = calculate_marker_area(p3, width, height)
    
    p0_piece = gray[p0[1] - piece0_dyu : p0[1] + piece0_dyd, p0[0] - piece0_dxl : p0[0] + piece0_dxr]
    p1_piece = gray[p1[1] - piece1_dyu : p1[1] + piece1_dyd, p1[0] - piece1_dxl : p1[0] + piece1_dxr]
    p2_piece = gray[p2[1] - piece2_dyu : p2[1] + piece2_dyd, p2[0] - piece2_dxl : p2[0] + piece2_dxr]
    p3_piece = gray[p3[1] - piece3_dyu : p3[1] + piece3_dyd, p3[0] - piece3_dxl : p3[0] + piece3_dxr]

    cv2.imwrite('./processing/' + image_name + '_p0_piece.png', p0_piece)
    cv2.imwrite('./processing/' + image_name + '_p1_piece.png', p1_piece)
    cv2.imwrite('./processing/' + image_name + '_p2_piece.png', p2_piece)
    cv2.imwrite('./processing/' + image_name + '_p3_piece.png', p3_piece)

    found_p0 = find_marker('./processing/' + image_name + '_p0_piece.png', './processing/' + image_name + '_p0_piece_result.png')
    found_p1 = find_marker('./processing/' + image_name + '_p1_piece.png', './processing/' + image_name + '_p1_piece_result.png')
    found_p2 = find_marker('./processing/' + image_name + '_p2_piece.png', './processing/' + image_name + '_p2_piece_result.png')
    found_p3 = find_marker('./processing/' + image_name + '_p3_piece.png', './processing/' + image_name + '_p3_piece_result.png')

    updated_p0 = (p0[0] - piece0_dxl + found_p0[0], p0[1] - piece0_dyu + found_p0[1])
    updated_p1 = (p1[0] - piece1_dxl + found_p1[0], p1[1] - piece1_dyu + found_p1[1])
    updated_p2 = (p2[0] - piece2_dxl + found_p2[0], p2[1] - piece2_dyu + found_p2[1])
    updated_p3 = (p3[0] - piece3_dxl + found_p3[0], p3[1] - piece3_dyu + found_p3[1])

    orig_image = cv2.imread(image_path)
    image = cv2.resize(orig_image, (width, height))
    cv2.circle(image, (int(updated_p0[0]),int(updated_p0[1])), int(4), (0,0,255))
    cv2.circle(image, (int(updated_p1[0]),int(updated_p1[1])), int(4), (0,0,255))
    cv2.circle(image, (int(updated_p2[0]),int(updated_p2[1])), int(4), (0,0,255))
    cv2.circle(image, (int(updated_p3[0]),int(updated_p3[1])), int(4), (0,0,255))
    cv2.imwrite('./processing/' + image_name + '_updated_markers.png', image)

    pts1 = np.float32([
        [updated_p0[0], updated_p0[1]],
        [updated_p1[0], updated_p1[1]],
        [updated_p2[0], updated_p2[1]],
        [updated_p3[0], updated_p3[1]]])
    pts2 = np.float32([
        [0, 0],
        [880, 0],
        [0, 480],
        [880, 480]])
    M = cv2.findHomography(pts1, pts2)[0]
    dst = cv2.warpPerspective(image, M, (880, 480))
    cv2.imwrite('./processing/' + image_name + '_marks_section.png', dst)
    
    dst2 = dst
    dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    dst = cv2.GaussianBlur(dst, (5, 5), 0)
    dst = cv2.threshold(dst, 127, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
    cv2.imwrite('./processing/' + image_name + '_marks_section_filtered.png', dst)

    valid_image = True

    student_number = 0
    try:
        student_number = int(mark_student_number(dst, dst2, PROJECTS_DETAILS[project_id]['student_number_length']))
    except:
        valid_image = False
    
    marks = []
    for i in range(PROJECTS_DETAILS[project_id]['number_of_questions']):
        try:
            marks.append(float(mark_question(i, dst, dst2)))
        except:
            valid_image = False
    
    actual_total = 0.0
    try:
        actual_total = float(mark_total(PROJECTS_DETAILS[project_id]['number_of_questions'], dst, dst2))
    except:
        valid_image = False

    expected_total = 0.0
    for mark in marks:
        expected_total += mark
    
    cv2.imwrite('./processing/' + image_name + '_marks_section_marked.png', dst2)

    result = {
        'student number': student_number,
        'marks': marks,
        'total': actual_total
    }

    return result if valid_image else None

# detect the hightlighted bubbles in the student number section. if the hightlighting is not proper, then flag the msg
def mark_student_number(dst, dst2, student_number_length):
    studentNumber = '_' * student_number_length
    def_x = 52
    def_y = 44
    counter_x = def_x
    counter_y = def_y
    for j in range(student_number_length):
        counter_y = def_y 
        for i in range(10):
            avg = np.mean(dst[int(counter_y)-6:int(counter_y)+12, int(counter_x)-6:int(counter_x)+12])
            if avg and avg > 80:
                if studentNumber[j] != '_':
                    return 'Invalid student number!'
                studentNumber = studentNumber[:j] + str(i) + studentNumber[j+1:]
                cv2.circle(dst2, (int(counter_x)+3, int(counter_y)+3), int(6), (0, 255, 0))
            else:
                cv2.circle(dst2, (int(counter_x)+3, int(counter_y)+3), int(6), (0, 0, 255))
            cv2.rectangle(dst2, (int(counter_x)-6, int(counter_y)-6), (int(counter_x)+12, int(counter_y)+12), (255, 0, 0))
            counter_y += 20
        counter_x += 31.5

    return studentNumber

# detect the hightlighted bubbles in the questions section. if the hightlighting is not proper, then flag the msg
def mark_question(index, dst, dst2):
    mark = '_' * 2
    def_x = 46 + index * 21.5 * 3 + index * 7
    def_y = 280
    counter_x = def_x
    counter_y = def_y
    for j in range(3):
        counter_y = def_y
        y_range = 1 if j == 2 else 10
        for i in range(y_range):
            avg = np.mean(dst[int(counter_y)-6:int(counter_y)+12, int(counter_x)-6:int(counter_x)+12])
            if avg and avg > 80:
                if j == 2:
                    mark += '.5'
                else:
                    if mark[j] != '_':
                        return 'Invalid mark!'
                    mark = mark[:j] + str(i) + mark[j+1:]
                cv2.circle(dst2, (int(counter_x)+3, int(counter_y)+3), int(6), (0, 255, 0))
            else:
                cv2.circle(dst2, (int(counter_x)+3, int(counter_y)+3), int(6), (0, 0, 255))
            cv2.rectangle(dst2, (int(counter_x)-6, int(counter_y)-6), (int(counter_x)+12, int(counter_y)+12), (255, 0, 0))
            counter_y += 20
        counter_x += 21.5

    return mark

# detect the hightlighted bubbles in the questions section. if the hightlighting is not proper, then flag the msg
def mark_total(index, dst, dst2):
    mark = '_' * 3
    def_x = 46 + index * 21.5 * 3 + index * 7
    def_y = 280
    counter_x = def_x
    counter_y = def_y
    for j in range(4):
        counter_y = def_y
        y_range = 1 if j == 3 else 10
        for i in range(y_range):
            avg = np.mean(dst[int(counter_y)-6:int(counter_y)+12, int(counter_x)-6:int(counter_x)+12])
            if avg and avg > 80:
                if j == 3:
                    mark += '.5'
                else:
                    if mark[j] != '_':
                        return 'Invalid mark!'
                    mark = mark[:j] + str(i) + mark[j+1:]
                cv2.circle(dst2, (int(counter_x)+3, int(counter_y)+3), int(6), (0, 255, 0))
            else:
                cv2.circle(dst2, (int(counter_x)+3, int(counter_y)+3), int(6), (0, 0, 255))
            cv2.rectangle(dst2, (int(counter_x)-6, int(counter_y)-6), (int(counter_x)+12, int(counter_y)+12), (255, 0, 0))
            counter_y += 20
        counter_x += 21.5

    return mark

# find the boundries of where the marker could be located based on the optimal location
def calculate_marker_area(point, width, height):
    delta = 80
    point_x = point[0]
    point_y = point[1]
    piece_dxl = delta if point_x - delta > 0 else point_x
    piece_dxr = delta if point_x + delta < width else width - point_x
    piece_dyd = delta if point_y + delta < height else height - point_y
    piece_dyu = delta if point_y - delta > 0 else point_y
    return (piece_dxl, piece_dxr, piece_dyu, piece_dyd)

# use convolution to find the area that is similar to the marker
def find_marker(input_path, result_path):
    marker_path = './markers/marker.png'
    ratio = 32.0/50.0
    paper = cv2.imread(input_path)
    tag = cv2.resize(cv2.imread(marker_path, cv2.IMREAD_GRAYSCALE), (0,0), fx=ratio, fy=ratio)
    convimg = (cv2.filter2D(np.float32(cv2.bitwise_not(paper)), -1, np.float32(cv2.bitwise_not(tag))))
    corner = np.unravel_index(convimg.argmax(), convimg.shape)
    corner = (corner[1], corner[0])
    cv2.rectangle(paper, (corner[0] - int(ratio * 25), corner[1] - int(ratio * 25)),
        (corner[0] + int(ratio * 25), corner[1] + int(ratio * 25)), (0, 255, 0), thickness=2, lineType=8, shift=0)
    cv2.imwrite(result_path, paper)
    return corner

# save a dump of the object that holds the information about all projects
def save_to_file():
    with open('db/db.txt', 'w') as file:
        file.write(json.dumps(PROJECTS_DETAILS))

# read the database dump into an object
def read_from_file():
    global PROJECTS_DETAILS 
    try:
        with open('db/db.txt', 'r') as file:
            PROJECTS_DETAILS = json.load(file)
    except Exception:
        print('Failed to load the db, creating a new one!')

if __name__ == '__main__':
    read_from_file()
    app.run(host='0.0.0.0')