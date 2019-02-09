var padding = 8;
var bubble_radius = 10;
var student_number_length = 10;
var last_single_digit = 9;
var no_of_questions = 20;
var max_question_mark = 15;

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

function drawBubbleBox(ctx, canvas, x, y, columnCount, rowCount) {
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
    var bubble_height = ((rowCount + 1) * 2 * bubble_radius) + padding * rowCount;
    
    // bubble sheet styling
    ctx.strokeStyle = "#000000";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = "10px Arial";

    for (i = 0; i <= rowCount; i++) {
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

function drawQuestionHeaders(x, y, offset, num_questions) {
    ctx.textAlign = "center";
    var text_x = x;
    var i;
    for (i = 0; i < num_questions; i++) {
        ctx.beginPath();
        ctx.fillText("Q"+(i+1), text_x + offset, y - padding);
        text_x += offset * 2 + padding;
    }
}

var canvas = document.getElementById('bubble_sheet');
var ctx = canvas.getContext('2d');
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.fillStyle = "black";
ctx.beginPath();
ctx.rect(padding, padding, canvas.width - padding * 2, canvas.height - padding * 2);
ctx.stroke();
ctx.font = "10px Arial";

var student_box_x = calculateStartingX(canvas.width, student_number_length);
var question_box_x = calculateStartingX(canvas.width, no_of_questions);

var question_box_y = (padding * 8) + (student_number_length + 1) * (2 * bubble_radius + padding);

ctx.fillText("Student Number", student_box_x, padding * 3);

// draw question headers
drawQuestionHeaders(question_box_x, question_box_y, bubble_radius, no_of_questions);

// draw student number box
drawBubbleBox(ctx, canvas, student_box_x, padding * 4, student_number_length, last_single_digit);

// draw question box
drawBubbleBox(ctx, canvas, question_box_x, question_box_y, no_of_questions, max_question_mark);

