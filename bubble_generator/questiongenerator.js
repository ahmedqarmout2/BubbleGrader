var no_of_questions = 7;

function precalculateQuestionBox(x, y, offset, num_questions) {
    var text_y = y;
    var i;
    var rowCount = 2;
    var bubble_height = (rowCount * 2 * bubble_radius) + padding * rowCount;
    for (i = 0; i < num_questions; i++) {
        var dimensions = precalculateHorizontalBubbleBox(x + padding * 6, text_y, num_single_digits, 2);
        text_y += bubble_height + padding * 2;
    }
    return dimensions
}

function drawQuestions(ctx, canvas, x, y, offset, num_questions) {
    var text_y = y;
    var i;
    var rowCount = 2;
    var bubble_height = (rowCount * 2 * bubble_radius) + padding * rowCount;
    
    var coordinateJson = []
    for (i = 0; i < num_questions; i++) {
        var coordinates = drawBubbleBoxHorizontal(ctx, canvas, x + padding * 6, text_y, num_single_digits, 2);
        ctx.textAlign = "center";
        ctx.font = "12px Arial"
        ctx.fillStyle = "black";
        ctx.beginPath();
        ctx.fillText((i + 1) + ")", x, text_y + offset);
        ctx.fillText("___", x, text_y + offset * 3);
        coordinateJson.push(coordinates)
        text_y += bubble_height + padding * 2;
    }
    console.log(JSON.stringify(coordinateJson))
}

var questionCanvas = document.getElementById('question_sheet')
var ctx = questionCanvas.getContext('2d');
var dimensions = precalculateQuestionBox(padding * 4, padding * 4 + marker_size, bubble_radius, no_of_questions);
questionCanvas.width = dimensions['width']
questionCanvas.height = dimensions['height']

ctx.fillStyle = "white";
ctx.fillRect(0, 0, questionCanvas.width, questionCanvas.height);
ctx.fillStyle = "black";
ctx.beginPath();
ctx.rect(0, 0, questionCanvas.width, questionCanvas.height);
ctx.stroke();
ctx.font = "12px Arial";

ctx.fillRect(padding * 10, padding * 2, marker_size, marker_size)
ctx.fillRect(padding * 10 + marker_size + padding + 10, padding * 2, marker_size, marker_size)
// ctx.fillRect(padding * 10 + marker_size + padding + 20, padding * 2, marker_size, marker_size)

// draw questions
drawQuestions(ctx, questionCanvas, padding * 4, padding * 4 + marker_size, bubble_radius, no_of_questions);
