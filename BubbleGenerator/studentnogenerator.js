var student_number_length = 20;
var num_single_digits = 10;
// var marker_size = 15

var studentCanvas = document.getElementById('student_number_sheet');
var ctx = studentCanvas.getContext('2d');
var dimensions = preCalculateVerticalBubbleBox(padding * 4 + marker_size , padding * 8, student_number_length, num_single_digits)
studentCanvas.width = dimensions['width'] + 20
studentCanvas.height = dimensions['height'] + 10
ctx.fillStyle = "white";
ctx.fillRect(0, 0, studentCanvas.width, studentCanvas.height);
ctx.fillStyle = "black";
ctx.lineWidth = 6;
ctx.beginPath();
ctx.fillRect(0, 0, 14, studentCanvas.height);
ctx.fillRect(studentCanvas.width-14, 0, 14, studentCanvas.height);
//ctx.rect(0, 0, studentCanvas.width, studentCanvas.height);
ctx.stroke();
ctx.lineWidth = 1;
ctx.font = "12px Arial";

// ctx.fillRect(padding * 2 + 2, padding * 8, marker_size, marker_size)
// ctx.fillRect(padding * 2 + 2, padding * 8 + marker_size + padding + 10, marker_size, marker_size)
// ctx.fillRect(padding * 2, padding * 8 + (marker_size + padding) * 2, marker_size, marker_size)

ctx.fillText("Student Number: ", padding * 2 + 20, padding * 6 + 4);

// draw student number box
drawBubbleBoxVertical(ctx, studentCanvas, padding * 8 + 8, padding * 8 + 6, student_number_length, num_single_digits);
