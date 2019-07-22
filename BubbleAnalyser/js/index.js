'use strict';

let CURRENT_PROJECT = {}

$(function () {
  get_project_list();
});

function get_project_list() {
  $.ajax({
    url: "/api/projects/list",
    success: function (data) {
      display_project_list(data['projects_list']);
    }
  });
}

function get_project_data(project_id) {
  $.ajax({
    url: `/api/project/data/${project_id}`,
    success: function (data) {
      CURRENT_PROJECT = data;
      const users_list = data['users_list'];
      const errors_list = data['errors'];

      let users_table = '';
      users_list.forEach(user_object => {
        users_table += `
          <tr>
            <td>${user_object['student number']}</td>
            <td>${user_object['username']}</td>
            <td>${user_object['first name']}</td>
            <td>${user_object['last name']}</td>
            <td>${JSON.stringify(user_object['marks'])}</td>
          </tr>
        `;
      });

      let errors_table = '';
      if (errors_list.length == 0) {
        errors_table = 'Nothing here yet!';
      } else {
        errors_list.forEach(error => {
          const name_list = error.split('/');
          const name = name_list[name_list.length - 1];
          errors_table += `
          <ul class="list-group">
            <li class="list-group-item d-flex justify-content-between align-items-center" style="align-items: baseline!important; padding: 0!important;">
              <p>${name}</p>
              <div style="justify-content: flex-end!important;">
                <button type="button" class="btn btn-primary px-3" data-toggle="modal" data-target="#basicExampleModal3" onClick="edit_error('${error}')"><i class="fas fa-edit" aria-hidden="true"></i></button>
                <button type="button" class="btn btn-danger px-3" onClick="remove_error('${error}')"><i class="fas fa-times" aria-hidden="true"></i></button>
              </div>
              </li>
          </ul>
        `;
        });
      }

      $('#nav-tabContent').html(
        `
          <div class="tab-pane fade show active" id="list-home" role="tabpanel" aria-labelledby="list-home-list">
            <ul class="nav nav-tabs" id="myTab" role="tablist">
              <li class="nav-item">
                <a class="nav-link active" id="description-tab" data-toggle="tab" href="#description" role="tab" aria-controls="description" aria-selected="true">Description</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" id="home-tab" data-toggle="tab" href="#home" role="tab" aria-controls="home" aria-selected="true">Class List</a>
              </li>
            </ul>
            <div class="tab-content" id="myTabContent">
              <div class="tab-pane fade show active" id="description" role="tabpanel" aria-labelledby="description-tab">
                <br />
                <div class="card">
                  <div class="card-header">
                    Project Details
                  </div>
                  <div class="card-body">
                    <div class="input-group mb-3">
                      <div class="input-group-prepend">
                        <p><b>Project Token:</b> ${data['id'].toUpperCase()}</p>
                      </div>
                    </div>
                    <div class="input-group mb-3">
                      <div class="input-group-prepend">
                        <span class="input-group-text" id="basic-addon1">Student Number Length</span>
                      </div>
                      <input type="number" id="student_number_length_number" class="form-control" min="1" max="10" value="${data['student_number_length']}">
                    </div>
                    <div class="input-group mb-3">
                      <div class="input-group-prepend">
                        <span class="input-group-text" id="basic-addon1">Number Of Questions</span>
                      </div>
                      <input type="number" id="number_of_questions_number" class="form-control" min="1" max="15" value="${data['number_of_questions']}">
                    </div>
                    <button type="button" class="btn btn-primary" onClick="update_project();">Generate</button>
                    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#basicExampleModal4">Upload Sample</button>
                    <br />
                    <br />
                    <div class="text-center" id="student_number_sheet_div" style="display: none;">
                      <canvas id="student_number_sheet"></canvas>
                    </div>
                  </div>
                </div>
              </div>
              <div class="tab-pane fade" id="home" role="tabpanel" aria-labelledby="home-tab">
                <br />
                <div class="card">
                  <div class="card-header">
                    Class List
                  </div>
                  <div class="card-body">
                    <p class="card-text">Upload your class list. The list should contain username, first name, last name.</p>
                    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#basicExampleModal2">Upload</button>
                  </div>
                </div>
                <br />
                <div class="card">
                  <div class="card-header">
                    Error List
                  </div>
                  <div class="card-body">
                    <p>${errors_table}</p>
                  </div>
                </div>
                <br />
                <div class="card">
                  <div class="card-header">
                    Class List
                  </div>
                  <div class="card-body">
                    <table id="dtBasicExample" class="table table-striped table-bordered table-sm" cellspacing="0" width="100%">
                      <thead>
                        <tr>
                          <th class="th-sm">Student Number</th>
                          <th class="th-sm">Username</th>
                          <th class="th-sm">First Name</th>
                          <th class="th-sm">Last Name</th>
                          <th class="th-sm">Marks</th>
                        </tr>
                      </thead>
                      <tbody>
                        ${users_table}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `
      );
      $('#dtBasicExample').DataTable();
      $('.dataTables_length').addClass('bs-select');
    }
  });
}

function create_project() {
  let project_name = $('#inputIconEx1').val();

  $.ajax({
    method: 'post',
    url: `/api/project/create`,
    data: JSON.stringify({
      project_name: project_name
    }),
    success: function (data) {
      get_project_list();
      $('#inputIconEx1').val('');
    }
  });
}

function edit_error(photo_path) {
  $('#edit_img').attr("src", photo_path);

  let text = `
    <div class="md-form">
      <i class="fas fa-file prefix"></i>
      <input type="text" id="studentNumberInput" class="form-control">
      <label for="studentNumberInput">Student Number: </label>
    </div>
  `;

  for (let i = 0; i < CURRENT_PROJECT['number_of_questions']; i += 2) {
    let second_col = ``;
    if (i + 1 < CURRENT_PROJECT['number_of_questions']) {
      second_col += `
        <div class="col">
          <div class="md-form">
            <i class="fas fa-question prefix"></i>
            <input type="number" min="1" id="questionNumber${i+2}Input" class="form-control">
            <label for="questionNumber${i+2}Input">Question ${i+2}: </label>
          </div>
        </div>
      `;
    }

    text += `
      <div class="form-row">
        <div class="col">
          <div class="md-form">
            <i class="fas fa-question prefix"></i>
            <input type="number" min="1" id="questionNumber${i+1}Input" class="form-control">
            <label for="questionNumber${i+1}Input">Question ${i+1}: </label>
          </div>
        </div>
        ${second_col}
      </div>
    `;
  }
  $('#edit_info').html(text);
}

function remove_error(photo_path) {
  alert(photo_path);
}

function update_mark() {
  const student_number = $('#studentNumberInput').val();
  let questions = [];
  for (let i = 0; i < CURRENT_PROJECT['number_of_questions']; i++) {
    questions.push($(`#questionNumber${i+1}Input`).val());
  }

  $.ajax({
    method: 'post',
    url: `/api/mark/update`,
    data: JSON.stringify({
      project_id: CURRENT_PROJECT['id'],
      student_number: student_number,
      questions: questions
    }),
    success: function (data) {

    }
  });
}

function display_project_list(project_list) {
  let list_tab = '';
  project_list.forEach(project_info => {
    list_tab += `<a onClick="get_project_data('${project_info["id"]}');" class="list-group-item list-group-item-action" id="list-home-list" data-toggle="list"
        href="#list-home" role="tab" aria-controls="${project_info["name"]}">${project_info["name"]}</a>`;
  });
  $('#list-tab').html(list_tab);
}

function upload_file() {
  const file_info = $('#inputGroupFile01');
  const files = file_info.get(0).files;
  let formData = new FormData();

  if (files.length !== 1) {
    alert('You can only upload one file at a time!');
    return;
  }

  let fileNameSplit = files[0].name.split('.');
  if (fileNameSplit[fileNameSplit.length - 1] !== 'csv') {
    alert('Only csv files are accepted!');
    return;
  }

  formData.append('file', files[0]);
  formData.append('id', CURRENT_PROJECT['id']);

  $.ajax({
    type: 'POST',
    url: '/api/upload/classlist',
    processData: false,
    contentType: false,
    data: formData,
    success: function (data) {
      get_project_data(CURRENT_PROJECT['id']);
    },
    error: function (data) {
      alert(JSON.stringify(data));
    }
  });
}

function upload_sample() {
  const file_info = $('#inputGroupFile02');
  const files = file_info.get(0).files;
  let formData = new FormData();

  if (files.length !== 1) {
    alert('You can only upload one file at a time!');
    return;
  }

  let fileNameSplit = files[0].name.split('.');
  if (fileNameSplit[fileNameSplit.length - 1] !== 'pdf') {
    alert('Only csv files are accepted!');
    return;
  }

  formData.append('file', files[0]);
  formData.append('id', CURRENT_PROJECT['id']);

  $.ajax({
    type: 'POST',
    url: '/api/upload/sample',
    processData: false,
    contentType: false,
    data: formData,
    success: function (data) {
      // get_project_data(CURRENT_PROJECT['id']);
    },
    error: function (data) {
      alert(JSON.stringify(data));
    }
  });
}

function update_project() {
  const student_number_length = $('#student_number_length_number').val();
  const number_of_questions = $('#number_of_questions_number').val()
  $.ajax({
    method: 'post',
    url: `/api/project/update`,
    data: JSON.stringify({
      id: CURRENT_PROJECT['id'],
      student_number_length: student_number_length,
      number_of_questions: number_of_questions
    }),
    success: function (data) {
      CURRENT_PROJECT['student_number_length'] = student_number_length;
      CURRENT_PROJECT['number_of_questions'] = number_of_questions;
      generate_image();
    }
  });
}

function generate_image() {
  const padding = 2;
  const studentCanvas = document.getElementById('student_number_sheet');
  const ctx = studentCanvas.getContext('2d');

  studentCanvas.width = 700;
  studentCanvas.height = 420;

  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, studentCanvas.width, studentCanvas.height);
  ctx.fillStyle = "black";
  ctx.lineWidth = 6;
  ctx.beginPath();
  ctx.fillRect(0, 0, 20, 20);
  ctx.fillRect(0, studentCanvas.height - 20, 20, 20);
  ctx.fillRect(studentCanvas.width - 20, 0, 20, 20);
  ctx.fillRect(studentCanvas.width - 20, studentCanvas.height - 20, 20, 20);
  ctx.stroke();
  ctx.lineWidth = 1;
  ctx.font = "12px Arial";
  ctx.fillText("Student Number: ", padding * 2 + 30, padding * 6 + 4);

  draw_bubble_box_vertical(ctx, 30, 22, CURRENT_PROJECT['student_number_length'], 10);

  for (let i = 0; i < CURRENT_PROJECT['number_of_questions']; i++) {
    draw_bubble_box_vertical(ctx, 30 + i * 44, 220, 2, 10);
  }

  $('#student_number_sheet_div').show();
}

function draw_bubble_box_vertical(ctx, x, y, columnCount, rowCount) {
  const padding = 2;
  const bubble_radius = 8;
  let i, j;
  let start_x = x;
  let bubble_x = start_x;
  let bubble_y = y;
  ctx.strokeStyle = "#999999";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillStyle = "#999999";
  ctx.font = "10px Arial";

  let coordinateJson = []
  for (i = 0; i < rowCount; i++) {
    for (j = 0; j < columnCount; j++) {
      draw_bubble(ctx, bubble_x, bubble_y, bubble_radius, i);
      coordinateJson.push({
        "x": bubble_x + bubble_radius,
        "y": bubble_y + bubble_radius
      })
      bubble_x += bubble_radius * 2 + padding * 2;
    }
    bubble_x = start_x;
    bubble_y += bubble_radius * 2 + padding;
  }

  return coordinateJson;
}

function draw_bubble(ctx, x, y, radius, text) {
  ctx.beginPath();
  ctx.fillText(text, x + radius, y + radius);
  ctx.arc(x + radius, y + radius, radius, 0, 2 * Math.PI);
  ctx.stroke();
  ctx.closePath();
}