// bubble sheet global variables
var padding = 4;
var bubble_radius = 10;
var marker_size = 20;

function drawBubble(ctx, x, y, radius, text) {
    ctx.beginPath();
    ctx.fillText(text, x + radius, y + radius);
    ctx.arc(x + radius, y + radius, radius, 0, 2 * Math.PI);
    ctx.stroke();
    ctx.closePath();
}

function drawBubbleBoxHorizontal(ctx, canvas, x, y, columnCount, rowCount) {
    var i, j;
    
    // starting x coordinate
    var start_x = x;
    
    // keep track of current bubble coordinates
    var bubble_x = start_x;
    var bubble_y = y;
    
    // bubble sheet styling
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = "10px Arial";
    
    var coordinateJson = []

    for (i = 0; i < rowCount; i++) {
        for (j = 0; j < columnCount; j++) {
            drawBubble(ctx, bubble_x, bubble_y, bubble_radius, j);
            coordinateJson.push({"x": bubble_x + bubble_radius, "y":bubble_y + bubble_radius})
            bubble_x += bubble_radius * 2 + padding;
        }
        bubble_x = start_x;
        bubble_y += bubble_radius * 2 + padding;
    }
    return coordinateJson
}

function drawBubbleBoxVertical(ctx, canvas, x, y, columnCount, rowCount) {
    var i, j;
    
    // starting x coordinate
    var start_x = x;
    
      // keep track of divider line coordinates
    var line_x = start_x + (bubble_radius * 2) + padding
    var line_y = y;
    
    // keep track of current bubble coordinates
    var bubble_x = start_x;
    var bubble_y = y;
    
    // bubble box height for divider generation
    var bubble_height = (rowCount * 2 * bubble_radius) + padding * rowCount;
    
    // bubble sheet styling
    ctx.strokeStyle = "#000000";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = "10px Arial";

    var coordinateJson = []
    for (i = 0; i < rowCount; i++) {
        for (j = 0; j < columnCount; j++) {
            drawBubble(ctx, bubble_x, bubble_y, bubble_radius, i);
            coordinateJson.push({"x": bubble_x + bubble_radius, "y":bubble_y + bubble_radius})
            bubble_x += bubble_radius * 2 + padding * 2;
        }
        bubble_x = start_x;
        bubble_y += bubble_radius * 2 + padding;
    }
    
    ctx.strokeStyle = "#999999";
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (i = 0; i < columnCount - 1; i++) {
        ctx.moveTo(line_x, line_y);
        ctx.lineTo(line_x, line_y + bubble_height);
        ctx.stroke();
        line_x += bubble_radius * 2 + padding * 2;
    }
    
    return coordinateJson
}

function preCalculateVerticalBubbleBox(x, y, columnCount, rowCount) {
    var width = x + (bubble_radius * 2) + padding + ((columnCount-1) * (bubble_radius * 2 + padding * 2))
    var height = (rowCount * 2 * bubble_radius) + padding * rowCount;
    
    return {"width": width+padding, "height": height+y+padding};
}

function precalculateHorizontalBubbleBox(x, y, columnCount, rowCount) {
    var i, j;
    
    var width = x;
    var height = y;
    
    for (j = 0; j < columnCount; j++) {
        width += bubble_radius * 2 + padding;
    }
    
    for (i = 0; i < rowCount; i++) {
        height += bubble_radius * 2 + padding;
    }
    
    return {"width": width+padding, "height": height+padding};
}
