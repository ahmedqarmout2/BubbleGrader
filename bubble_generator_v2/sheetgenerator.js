var padding = 4;
var bubble_radius = 10;
var student_number_length = 10;
var num_single_digits = 10;
var no_of_questions = 5;

function drawBubble(ctx, x, y, radius, text) {
    ctx.beginPath();
    ctx.fillText(text, x + radius, y + radius);
    ctx.arc(x + radius, y + radius, radius, 0, 2 * Math.PI);
    ctx.stroke();
    ctx.closePath();
}

function calculateStartingX(width, numOfColumns) {
    return (width - ((numOfColumns - 1) * padding + numOfColumns * bubble_radius * 2)) / 2;
}

function drawBubbleBoxVertical(ctx, canvas, x, y, columnCount, rowCount) {
    var i, j;
    
    // starting x coordinate
    var start_x = x;
    
    // keep track of current bubble coordinates
    var bubble_x = start_x;
    var bubble_y = y;
    
    // keep track of divider line coordinates
    var line_x = start_x + (bubble_radius * 2) + (padding / 2);
    var line_y = y;
    
    // bubble box height for divider generation
    var bubble_height = (rowCount * 2 * bubble_radius) + padding * rowCount;
    
    // bubble sheet styling
    ctx.strokeStyle = "#000000";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = "10px Arial";

    for (i = 0; i < rowCount; i++) {
        for (j = 0; j < columnCount; j++) {
            drawBubble(ctx, bubble_x, bubble_y, bubble_radius, i);
            bubble_x += bubble_radius * 2 + padding;
        }
        bubble_x = start_x;
        bubble_y += bubble_radius * 2 + padding;
    }
    
    ctx.strokeStyle = "#999999";
    ctx.beginPath();
    for (i = 0; i < columnCount - 1; i++) {
        ctx.moveTo(line_x, line_y);
        ctx.lineTo(line_x, line_y + bubble_height);
        ctx.stroke();
        line_x += bubble_radius * 2 + padding;
    }
}

function drawBubbleBoxHorizontal(ctx, canvas, x, y, columnCount, rowCount) {
      var i, j;
    
    // starting x coordinate
    var start_x = x;
    
    // keep track of current bubble coordinates
    var bubble_x = start_x;
    var bubble_y = y;
    
//    // keep track of divider line coordinates
//    var line_x = start_x + (bubble_radius * 2) + (padding / 2);
//    var line_y = y;
//    
//    // bubble box height for divider generation
//    var bubble_height = (rowCount * 2 * bubble_radius) + padding * rowCount;
    
    // bubble sheet styling
    ctx.strokeStyle = "#000000";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = "10px Arial";

    for (i = 0; i < rowCount; i++) {
        for (j = 0; j < columnCount; j++) {
            drawBubble(ctx, bubble_x, bubble_y, bubble_radius, j);
            bubble_x += bubble_radius * 2 + padding;
        }
        bubble_x = start_x;
        bubble_y += bubble_radius * 2 + padding;
    }
    
//    ctx.strokeStyle = "#999999";
//    ctx.beginPath();
//    for (i = 0; i < columnCount - 1; i++) {
//        ctx.moveTo(line_x, line_y);
//        ctx.lineTo(line_x, line_y + bubble_height);
//        ctx.stroke();
//        line_x += bubble_radius * 2 + padding;
//    }
}

function drawQuestions(x, y, offset, num_questions) {
    var text_y = y;
    var i;
    for (i = 0; i < num_questions; i++) {
        var rowCount = 2;
        var bubble_height = (rowCount * 2 * bubble_radius) + padding * rowCount;
        drawBubbleBoxHorizontal(ctx, canvas, x + padding * 4, text_y, num_single_digits, 2);
        ctx.textAlign = "center";
        ctx.font = "12px Arial"
        ctx.beginPath();
        ctx.fillText("Q" + (i + 1), x, text_y + offset * 2);
        text_y += bubble_height + padding;
    }
}

var canvas = document.getElementById('bubble_sheet');
var ctx = canvas.getContext('2d');
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.fillStyle = "black";
ctx.beginPath();
ctx.rect(0, 0, canvas.width, canvas.height);
ctx.stroke();
ctx.font = "12px Arial";

var student_box_x = calculateStartingX(canvas.width, student_number_length);

var question_box_y = (padding * 24) + (student_number_length + 1) * (2 * bubble_radius + padding);

ctx.fillText("Student Number: ", student_box_x - padding * 24, padding * 6);
ctx.beginPath();
ctx.moveTo(student_box_x, padding * 6);
ctx.lineTo(student_box_x + 10 * (bubble_radius * 2 + padding), padding * 6);
ctx.stroke();

// draw questions
drawQuestions(32, question_box_y, bubble_radius, no_of_questions);
drawQuestions(312, question_box_y, bubble_radius, no_of_questions);

// draw student number box
drawBubbleBoxVertical(ctx, canvas, student_box_x, padding * 8, student_number_length, num_single_digits);

var img = new Image();
img.onload = function () {
    ctx.drawImage(img, student_box_x - 70, padding * 8, 60, 60);
    ctx.drawImage(img, 48, question_box_y - 65, 60, 60);
    ctx.drawImage(img, 328, question_box_y - 65, 60, 60);
}
img.src = "images/qrcode.png";