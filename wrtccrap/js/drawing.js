function drawConfi(){	
	canvas = document.getElementById('canvas');
	context = canvas.getContext('2d');

	radius = 3;
	pencilradius = radius;
	pencilcolor = "white";
	dragging = false;

	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight*0.7;

	context.lineWidth = radius*2;

	minRad = 1;
	maxRad = 100;
	defaultRad = 20;
	interval = 1;

	eraser =  document.getElementById('eraser');
	iconEraser =  document.getElementById('erasericon');
	eraser1 =  document.getElementById('eraser1');
	eraser2 =  document.getElementById('eraser2');
	eraser3 =  document.getElementById('eraser3');
	pencil =  document.getElementById('pencil');
	iconPencil =  document.getElementById('pencilicon');
	pencil1 =  document.getElementById('pencil1');
	pencil2 =  document.getElementById('pencil2');
	pencil3 =  document.getElementById('pencil3');
	undo =  document.getElementById('undo');
	redo =  document.getElementById('redo');
	clean =  document.getElementById('clean');

	cPushArray = new Array();
	cStep = -1;
	cPush();
	blank = cPushArray[0];

	eraser1.addEventListener('click', function(){
		// bgColor = window.getComputedStyle(document.body, null).getPropertyValue('backgroundColor');
		pencilcolor = context.fillStyle;
		pencilradius = radius;
		setColor("black");
		setRadius(3);
		iconEraser.style.fontSize = "12px";
	});
	eraser2.addEventListener('click', function(){
		// bgColor = window.getComputedStyle(document.body, null).getPropertyValue('backgroundColor');
		pencilcolor = context.fillStyle;
		pencilradius = radius;
		setColor("black");
		setRadius(12);
		iconEraser.style.fontSize = "18px";
	});
	eraser3.addEventListener('click', function(){
		// bgColor = window.getComputedStyle(document.body, null).getPropertyValue('backgroundColor');
		pencilcolor = context.fillStyle;
		pencilradius = radius;
		setColor("black");
		setRadius(40);
		iconEraser.style.fontSize = "24px";
	});

	pencil1.addEventListener('click', function(){
		setRadius(1);
		setColor(pencilcolor);
		pencilradius=radius;
		iconPencil.style.fontSize = "12px";
	});
	pencil2.addEventListener('click', function(){
		setRadius(2);
		setColor(pencilcolor);
		pencilradius=radius;
		iconPencil.style.fontSize = "18px";
	});
	pencil3.addEventListener('click', function(){
		setRadius(4);
		setColor(pencilcolor);
		pencilradius=radius;
		iconPencil.style.fontSize = "24px";
	});

	clean.addEventListener('click',function(){
		cStep++;
	    if (cStep < cPushArray.length) { cPushArray.length = cStep; }
	    cPushArray.push(blank);
	    context.putImageData(blank,0,0);
		var sender = {"fn":"clearBoard"};
		sendData(JSON.stringify(sender));
	});

	undo.addEventListener('click',function(){
		cUndo();
		var sender = {"fn":"undo"};
		sendData(JSON.stringify(sender));
	})

	redo.addEventListener('click',function(){
		cRedo();
		var sender = {"fn":"redo"};
		sendData(JSON.stringify(sender));
	})

	swatches = document.getElementsByClassName('swatch');

	canvas.addEventListener('mousedown', engage);
	canvas.addEventListener('mouseup', disengage);
	canvas.addEventListener('mousemove', putPoint);

	setColor("white");
	swatches[0].className += ' active';

	for (var i = 0, n = swatches.length; i<n; i++){
		swatches[i].addEventListener('click', setSwatch);
	}
};

var putPoint = function(e){
	if (dragging){
		context.lineTo(e.offsetX, e.offsetY);
		context.stroke();
		context.beginPath();
		context.arc(e.offsetX, e.offsetY, radius, 0, Math.PI*2);
		context.fill();
		context.beginPath();
		context.moveTo(e.offsetX, e.offsetY);
		var sender = {"fn":"putPoint", "putPoint":true, "e":{"offsetX": e.offsetX, "offsetY": e.offsetY, "colorRemote": context.fillStyle, "widthRemote": context.lineWidth}};
		sendData(JSON.stringify(sender));
	}
}

var engage = function(e){
	dragging = true;
	var sender = {"fn":"engage", "engage": true, "e":{"offsetX": e.offsetX, "offsetY": e.offsetY, "colorRemote": context.fillStyle, "widthRemote": context.lineWidth}};
	sendData(JSON.stringify(sender));
	putPoint(e);
	
}

var disengage = function(e, s){
	dragging = false;
	context.beginPath();
	cPush();
	var sender = {"fn":"disengage", "disengage":true};
	sendData(JSON.stringify(sender));
}

var putPointRemote = function(e){
	if (draggingRemote=true){
		var colorBefore = context.fillStyle;
		var widthBefore = context.lineWidth;
		context.fillStyle = e.colorRemote;
		context.strokeStyle = e.colorRemote;
		context.lineWidth = e.widthRemote;
		radius = e.widthRemote/2;

		context.lineTo(e.offsetX, e.offsetY);
		context.stroke();
		context.beginPath();
		context.arc(e.offsetX, e.offsetY, radius, 0, Math.PI*2);
		context.fill();
		context.beginPath();
		context.moveTo(e.offsetX, e.offsetY);

		context.fillStyle = colorBefore;
		context.strokeStyle = colorBefore;
		context.lineWidth = widthBefore;
		radius = widthBefore/2;
	}	
}

var engageRemote = function(e){
	draggingRemote = true;
	putPointRemote(e);
}

var disengageRemote = function(e){
	draggingRemote = false;
	context.beginPath();
	cPush();
}

var setRadius = function(newRadius){
	radius = newRadius;
	context.lineWidth = radius*2;
}

function setColor(color){
	context.fillStyle = color;
	context.strokeStyle = color;
	var active = document.getElementsByClassName('active')[0];
	if(active){
		active.className = 'swatch';
	}
}

function setSwatch(e){
	var swatch = e.target;
	setRadius(pencilradius);
	setColor(swatch.style.backgroundColor);
	swatch.className += ' active';
	pencilcolor = swatch.style.backgroundColor;
	iconPencil.style.color = pencilcolor;
}

function clearRemote(){
	cStep++;
    if (cStep < cPushArray.length) { cPushArray.length = cStep; }
    cPushArray.push(blank);
    context.putImageData(blank,0,0);
}

function cPush() {
	console.log("PUSH");
    cStep++;
    console.log(cStep);
    if (cStep < cPushArray.length) { cPushArray.length = cStep; }
    cPushArray.push(context.getImageData(0,0,canvas.width,canvas.height));
}

function cUndo() {
    if (cStep > 0) {
    	console.log("UNDO");
        cStep--;
        context.putImageData(cPushArray[cStep],0,0);
    }
}

function cRedo() {
    if (cStep < cPushArray.length-1) {
        console.log("REDO");
        cStep++;
        context.putImageData(cPushArray[cStep],0,0);
    }
}
