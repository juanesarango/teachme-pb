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
	eraser1 =  document.getElementById('eraser1');
	eraser2 =  document.getElementById('eraser2');
	eraser3 =  document.getElementById('eraser3');
	pencil =  document.getElementById('pencil');
	pencil1 =  document.getElementById('pencil1');
	pencil2 =  document.getElementById('pencil2');
	pencil3 =  document.getElementById('pencil3');
	backstep =  document.getElementById('backstep');
	clean =  document.getElementById('clean');

	eraser1.addEventListener('click', function(){
		// bgColor = window.getComputedStyle(document.body, null).getPropertyValue('backgroundColor');
		pencilcolor = context.fillStyle;
		pencilradius = radius;
		setColor("black");
		setRadius(3);
		eraser.style.fontSize = 12;
	});
	eraser2.addEventListener('click', function(){
		// bgColor = window.getComputedStyle(document.body, null).getPropertyValue('backgroundColor');
		pencilcolor = context.fillStyle;
		pencilradius = radius;
		setColor("black");
		setRadius(12);
		eraser.style.fontSize = 18;
	});
	eraser3.addEventListener('click', function(){
		// bgColor = window.getComputedStyle(document.body, null).getPropertyValue('backgroundColor');
		pencilcolor = context.fillStyle;
		pencilradius = radius;
		setColor("black");
		setRadius(40);
		eraser.style.fontSize = 24;
	});

	pencil1.addEventListener('click', function(){
		setRadius(1);
		setColor(pencilcolor);
		pencil.style.fontSize = 12;
	});
	pencil2.addEventListener('click', function(){
		setRadius(2);
		setColor(pencilcolor);
		pencil.style.fontSize = 18;
	});
	pencil3.addEventListener('click', function(){
		setRadius(4);
		setColor(pencilcolor);
		pencil.style.fontSize = 24;
	});

	clean.addEventListener('click',function(){
		// Store the current transformation matrix
		context.save();
		// Use the identity matrix while clearing the canvas
		context.setTransform(1, 0, 0, 1, 0, 0);
		context.clearRect(0, 0, canvas.width, canvas.height);
		// Restore the transform
		context.restore();
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
}

// var setRadius = function(newRadius){
// 	if(newRadius<minRad)
// 		newRadius = minRad;
// 	else if(newRadius>maxRad)
// 		newRadius = maxRad;
// 	radius = newRadius;
// 	context.lineWidth = radius*2;
// 	radSpan.innerHTML = radius;
// }

var setRadius = function(newRadius){
	radius = newRadius;
	context.lineWidth = radius*2;
}

function setColor(color){
	context.fillStyle = color;
	context.strokeStyle = color;
	setRadius(pencilradius);
	var active = document.getElementsByClassName('active')[0];
	if(active){
		active.className = 'swatch';
	}
}

function setSwatch(e){
	var swatch = e.target;
	setColor(swatch.style.backgroundColor);
	swatch.className += ' active';
	pencilcolor = swatch.style.backgroundColor;
}