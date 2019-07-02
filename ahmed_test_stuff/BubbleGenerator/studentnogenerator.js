var student_number_length = 10;
var num_single_digits = 10;
// var marker_size = 15

var studentCanvas = document.getElementById('student_number_sheet');
var ctx = studentCanvas.getContext('2d');
var dimensions = preCalculateVerticalBubbleBox(padding * 4 + marker_size , padding * 8, student_number_length, num_single_digits)
studentCanvas.width = 470
studentCanvas.height = 420
ctx.fillStyle = "white";
ctx.fillRect(0, 0, studentCanvas.width, studentCanvas.height);
ctx.fillStyle = "black";
ctx.lineWidth = 6;
ctx.beginPath();
ctx.fillRect(0, 0, 20, 20);
ctx.fillRect(0, studentCanvas.height-20, 20, 20);
ctx.fillRect(studentCanvas.width-20, 0, 20, 20);
ctx.fillRect(studentCanvas.width-20, studentCanvas.height-20, 20, 20);
//ctx.rect(0, 0, studentCanvas.width, studentCanvas.height);
ctx.stroke();
ctx.lineWidth = 1;
ctx.font = "12px Arial";

// ctx.fillRect(padding * 2 + 2, padding * 8, marker_size, marker_size)
// ctx.fillRect(padding * 2 + 2, padding * 8 + marker_size + padding + 10, marker_size, marker_size)
// ctx.fillRect(padding * 2, padding * 8 + (marker_size + padding) * 2, marker_size, marker_size)

ctx.fillText("Student Number: ", padding * 2 + 30, padding * 6 + 4);

// draw student number box
drawBubbleBoxVertical(ctx, studentCanvas, padding * 8 + 14, padding * 8 + 6, student_number_length, num_single_digits);

drawBubbleBoxVertical(ctx, studentCanvas, 30, 220, 10, 2);
drawBubbleBoxVertical(ctx, studentCanvas, 30, 260, 10, 2);
drawBubbleBoxVertical(ctx, studentCanvas, 30, 300, 10, 2);
drawBubbleBoxVertical(ctx, studentCanvas, 30, 340, 10, 2);
drawBubbleBoxVertical(ctx, studentCanvas, 30, 380, 10, 2);

drawBubbleBoxVertical(ctx, studentCanvas, 240, 220, 10, 2);
drawBubbleBoxVertical(ctx, studentCanvas, 240, 260, 10, 2);
drawBubbleBoxVertical(ctx, studentCanvas, 240, 300, 10, 2);
drawBubbleBoxVertical(ctx, studentCanvas, 240, 340, 10, 2);
drawBubbleBoxVertical(ctx, studentCanvas, 240, 380, 10, 2);

console.log("studentCanvas.width" + studentCanvas.width);
console.log("studentCanvas.height" + studentCanvas.height);
