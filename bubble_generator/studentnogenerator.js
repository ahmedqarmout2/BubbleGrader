var student_number_length = 10;
var num_single_digits = 10;

var studentCanvas = document.getElementById('student_number_sheet');
var ctx = studentCanvas.getContext('2d');
var dimensions = preCalculateVerticalBubbleBox(padding * 4 + marker_size , padding * 8, student_number_length, num_single_digits)
studentCanvas.width = dimensions['width']
studentCanvas.height = dimensions['height']
ctx.fillStyle = "white";
ctx.fillRect(0, 0, studentCanvas.width, studentCanvas.height);
ctx.fillStyle = "black";
ctx.beginPath();
ctx.rect(0, 0, studentCanvas.width, studentCanvas.height);
ctx.stroke();
ctx.font = "12px Arial";

ctx.fillRect(padding * 2, padding * 8, marker_size, marker_size)
ctx.fillRect(padding * 2, padding * 8 + marker_size + padding, marker_size, marker_size)
ctx.fillRect(padding * 2, padding * 8 + (marker_size + padding) * 2, marker_size, marker_size)

ctx.fillText("Student Number: ", padding * 2, padding * 6);

// draw student number box
drawBubbleBoxVertical(ctx, studentCanvas, padding * 4 + marker_size, padding * 8, student_number_length, num_single_digits);