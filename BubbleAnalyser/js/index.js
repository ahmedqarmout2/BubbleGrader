'use strict';
let CURRENT_PROJECT = {}
let SELECTED_ERROR_IMAGE_PATH = '';
const marker = document.getElementById('marker');
$(function () {
  get_project_list();
});

function get_project_list() {
  $.ajax({
    url: "/api/projects/list",
    success: function (data) {
      display_project_list(data['projects_list']);
    },
    error: function (data) {
      alert('Failed to get the list of projects, try again later!');
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
      const number_of_questions = data['number_of_questions'];
      let users_table = '';
      users_list.forEach(user_object => {
        const student_number = user_object['student number'];
        let mark_columns = '';
        for (let i = 0; i < number_of_questions; i++) {
          const mark = user_object['marks'][i];
          mark_columns += `<td id="${student_number}_question_${i+1}">${mark ? mark : 0}</td>`;
        }
        users_table += `
          <tr>
            <td id="${student_number}_student_number">${student_number}</td>
            <td id="${student_number}_username">${user_object['username']}</td>
            <td id="${student_number}_first_name">${user_object['first name']}</td>
            <td id="${student_number}_last_name">${user_object['last name']}</td>
            ${mark_columns}
            <td id="${student_number}_total">${user_object['total']}</td>
            <td id="${student_number}_action">
              <button type="button" class="btn btn-primary px-3" data-toggle="modal" data-target="#basicExampleModal3" onClick="edit_error(undefined)"><i class="fas fa-edit" aria-hidden="true"></i></button>
            </td>
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
      let questions_columns = '';
      for (let i = 0; i < number_of_questions; i++) {
        questions_columns += `<th class="th-sm">Question ${i+1}</th>`;
      }
      questions_columns += '<th class="th-sm">Total</th>';
      questions_columns += '<th class="th-sm">Actions</th>';
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
                      <input type="number" id="number_of_questions_number" class="form-control" min="1" max="10" value="${number_of_questions}">
                    </div>
                    <div class="custom-control custom-checkbox">
                      <input type="checkbox" class="custom-control-input" id="show_utorid_check" ${data['show_utorid'] ? 'checked' : ''}>
                      <label class="custom-control-label" for="show_utorid_check">Show UTORID</label>
                    </div>
                    <div class="custom-control custom-checkbox">
                      <input type="checkbox" class="custom-control-input" id="show_signature_check" ${data['show_signature'] ? 'checked' : ''}>
                      <label class="custom-control-label" for="show_signature_check">Show Signature</label>
                    </div>
                    <button type="button" class="btn btn-primary" onClick="update_project();">Update</button>
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
                    <button type="button" class="btn btn-primary" onClick="export_classlist();">Export Classlist</button>
                  </div>
                </div>
                <br />
                <div class="card">
                  <div class="card-header">
                    Error List
                  </div>
                  <div class="card-body" id="errors_table_p">
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
                          ${questions_columns}
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
    },
    error: function (data) {
      alert('Failed to get the details of the project, try again later!');
    }
  });
}

function export_classlist() {
  $.ajax({
    method: 'post',
    url: `/api/export/classlist`,
    data: JSON.stringify({
      project_id: CURRENT_PROJECT['id']
    }),
    success: function (data) {
      const file_path = `http://${window.location.host}/${data['file_name']}`;
      const win = window.open(file_path, '_blank');
      win.focus();
    },
    error: function (data) {
      alert('Failed to export classlist!');
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
    },
    error: function (data) {
      alert('Failed to create the project, try again later!');
    }
  });
}

function edit_error(photo_path) {
  if (!photo_path) {
    $('#edit_img').hide();
  }
  $('#edit_img').attr("src", photo_path);
  SELECTED_ERROR_IMAGE_PATH = photo_path;
  let text = `
    <div class="md-form">
      <i class="fas fa-file prefix"></i>
      <input type="text" id="studentNumberInput" class="form-control">
      <label for="studentNumberInput">Student Number</label>
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
            <label for="questionNumber${i+2}Input">Question ${i+2}</label>
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
            <label for="questionNumber${i+1}Input">Question ${i+1}</label>
          </div>
        </div>
        ${second_col}
      </div>
    `;
  }
  $('#edit_info').html(text);
}

function remove_error(photo_path) {
  SELECTED_ERROR_IMAGE_PATH = photo_path;
  remove_image();
}

function remove_image() {
  $.ajax({
    method: 'post',
    url: `/api/remove/image`,
    data: JSON.stringify({
      project_id: CURRENT_PROJECT['id'],
      photo_path: SELECTED_ERROR_IMAGE_PATH
    }),
    success: function (data) {
      var index = CURRENT_PROJECT['errors'].indexOf(SELECTED_ERROR_IMAGE_PATH);
      if (index > -1) {
        CURRENT_PROJECT['errors'].splice(index, 1);
      }
      let errors_table = '';
      if (CURRENT_PROJECT['errors'].length == 0) {
        errors_table = 'Nothing here yet!';
      } else {
        CURRENT_PROJECT['errors'].forEach(error => {
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
      $('#errors_table_p').html(errors_table);
    },
    error: function (data) {
      alert('Failed to remove the image, try again later!');
    }
  });
}

function update_mark() {
  const student_number = $('#studentNumberInput').val();
  let marks = [];
  for (let i = 0; i < CURRENT_PROJECT['number_of_questions']; i++) {
    marks.push($(`#questionNumber${i+1}Input`).val());
  }
  $.ajax({
    method: 'post',
    url: `/api/mark/update`,
    data: JSON.stringify({
      project_id: CURRENT_PROJECT['id'],
      student_number: student_number,
      marks: marks
    }),
    success: function (data) {
      for (let i = 0; i < CURRENT_PROJECT['number_of_questions']; i++) {
        $(`#${student_number}_question_${i+1}`).html($(`#questionNumber${i+1}Input`).val());
      }

      if (SELECTED_ERROR_IMAGE_PATH) {
        remove_image();
      }
    },
    error: function (data) {
      alert('Failed to update the mark, try again later!');
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
      alert(JSON.stringify(data['responseText']));
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
      alert(JSON.stringify(data['responseText']));
    }
  });
}

function update_project() {
  const student_number_length = $('#student_number_length_number').val();
  const number_of_questions = $('#number_of_questions_number').val();
  const show_utorid = $('#show_utorid_check').is(':checked');
  const show_signature = $('#show_signature_check').is(':checked');
  $.ajax({
    method: 'post',
    url: `/api/project/update`,
    data: JSON.stringify({
      id: CURRENT_PROJECT['id'],
      student_number_length: student_number_length,
      number_of_questions: number_of_questions,
      show_utorid: show_utorid,
      show_signature: show_signature
    }),
    success: function (data) {
      CURRENT_PROJECT['student_number_length'] = student_number_length;
      CURRENT_PROJECT['number_of_questions'] = number_of_questions;
      CURRENT_PROJECT['show_utorid'] = show_utorid;
      CURRENT_PROJECT['show_signature'] = show_signature;
      generate_image();
    },
    error: function (data) {
      alert('Failed to update the project, try again later!');
    }
  });
}

function generate_image() {
  const studentCanvas = document.getElementById('student_number_sheet');
  const ctx = studentCanvas.getContext('2d');
  studentCanvas.width = 880;
  studentCanvas.height = 480;
  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, studentCanvas.width, studentCanvas.height);
  draw_text(ctx, 'First Name: _____________________________', studentCanvas.width - 340, 30);
  draw_text(ctx, 'Last Name: _____________________________', studentCanvas.width - 340, 60);
  if (CURRENT_PROJECT['show_utorid']) {
    draw_text(ctx, 'Utorid: _________________________________', studentCanvas.width - 340, 90);
  }
  if (CURRENT_PROJECT['show_signature']) {
    draw_text(ctx, 'Signature: ______________________________', studentCanvas.width - 340, 120);
  }
  draw_corners(ctx, studentCanvas.width, studentCanvas.height);
  draw_student_number_section(ctx, CURRENT_PROJECT['student_number_length']);
  draw_questions_section(ctx, CURRENT_PROJECT['number_of_questions']);
  $('#student_number_sheet_div').show();
}

function draw_corners(ctx, width, height) {
  ctx.fillStyle = "#000000";
  ctx.lineWidth = 6;
  ctx.beginPath();
  ctx.drawImage(marker, 0, 0);
  ctx.drawImage(marker, width - 50, 0);
  ctx.drawImage(marker, 0, height - 50);
  ctx.drawImage(marker, width - 50, height - 50);
  ctx.stroke();
  ctx.closePath();
}

function draw_text(ctx, text, x, y) {
  ctx.fillStyle = "#000000";
  ctx.lineWidth = 1;
  ctx.font = "12px Arial";
  ctx.fillText(text, x, y);
}

function draw_student_number_section(ctx, student_number_length) {
  const x = 60;
  const y = 30;
  draw_text(ctx, 'Student Number:', x, y);
  for (let i = 0; i < student_number_length; i++) {
    draw_text(ctx, '____', x + i * 30, y + 20);
  }
  const columnCount = student_number_length;
  const rowCount = 10;
  const padding = 2;
  const bubble_radius = 8;
  let i, j;
  let start_x = 60;
  let bubble_x = start_x;
  let bubble_y = 60;
  for (i = 0; i < rowCount; i++) {
    for (j = 0; j < columnCount; j++) {
      const color = (j % 2 == 0) ? '#ffffff' : '#f6f6f6';
      draw_bubble(ctx, bubble_x + 5, bubble_y, bubble_radius, i, color);
      bubble_x += bubble_radius * 2 + 14;
    }
    bubble_x = start_x;
    bubble_y += bubble_radius * 2 + padding;
  }
}

function draw_questions_section(ctx, number_of_questions) {
  const x = 60;
  const y = 260;
  for (let i = 0; i < number_of_questions; i++) {
    draw_text(ctx, `Q${i+1}: _____`, x + i * 68 + 28, y);
    draw_bubbles_vertical(ctx, x + i * 68, y + 12, 2, 10);
    draw_bubble(ctx, x + i * 68 + 40, y + 12, 8, '0.5', '#ffffff');
  }
  draw_text(ctx, `Total: _______`, x + number_of_questions * 68 + 36, y);
  draw_bubbles_vertical(ctx, x + number_of_questions * 68, y + 12, 3, 10);
  draw_bubble(ctx, x + number_of_questions * 68 + 60, y + 12, 8, '0.5', '#f6f6f6');
}

function draw_bubbles_vertical(ctx, x, y, columnCount, rowCount) {
  const padding = 2;
  const bubble_radius = 8;
  let i, j;
  let start_x = x;
  let bubble_x = start_x;
  let bubble_y = y;
  for (i = 0; i < rowCount; i++) {
    for (j = 0; j < columnCount; j++) {
      const color = (j % 2 == 0) ? '#ffffff' : '#f6f6f6';
      draw_bubble(ctx, bubble_x, bubble_y, bubble_radius, i, color);
      bubble_x += bubble_radius * 2 + padding * 2;
    }
    bubble_x = start_x;
    bubble_y += bubble_radius * 2 + padding;
  }
}

function draw_bubble(ctx, x, y, radius, text, color) {
  ctx.beginPath();
  ctx.arc(x + radius, y + radius, radius, 0, 2 * Math.PI);
  ctx.fillStyle = color;
  ctx.fill();
  ctx.strokeStyle = "#f0f0f0";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillStyle = "#d1d1d1";
  ctx.font = "10px Arial";
  ctx.stroke();
  ctx.fillText(text, x + radius, y + radius);
  ctx.closePath();
}