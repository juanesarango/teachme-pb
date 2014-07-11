function drawConfi(){	
	canvas = document.getElementById('canvas');
	context = canvas.getContext('2d');

	radius = 10;
	dragging = false;

	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight*0.7;

	context.lineWidth = radius*2;

	minRad = 1,
	maxRad = 100,
	defaultRad = 20,
	interval = 2,
	radSpan = document.getElementById('radval'),
	decRad = document.getElementById('decrad'),
	incRad = document.getElementById('incrad');

	decRad.addEventListener('click', function(){
		setRadius(radius-interval);
	});
	incRad.addEventListener('click', function(){
		setRadius(radius+interval);
	});

	swatches = document.getElementsByClassName('swatch');

	canvas.addEventListener('mousedown', engage);
	canvas.addEventListener('mouseup', disengage)
	canvas.addEventListener('mousemove', putPoint);

	context.fillStyle = "white";
	context.strokeStyle = "white";

	for (var i = 0, n = swatches.length; i<n; i++){
	swatches[i].addEventListener('click', setSwatch);
}
};
var putPoint = function(e){
	if (dragging){
		if (!e.which){
			var colorBefore = context.fillStyle;
			var widthBefore = context.lineWidth;
			context.fillStyle = e.colorRemote;
			context.strokeStyle = e.colorRemote;
			context.lineWidth = e.widthRemote;
			radius = e.widthRemote/2;
		}
		context.lineTo(e.offsetX, e.offsetY);
		context.stroke();
		context.beginPath();
		context.arc(e.offsetX, e.offsetY, radius, 0, Math.PI*2);
		context.fill();
		context.beginPath();
		context.moveTo(e.offsetX, e.offsetY);
		if (e.which){
			var sender = {"fn":"putPoint", "putPoint":true, "e":{"offsetX": e.offsetX, "offsetY": e.offsetY, "colorRemote": context.fillStyle, "widthRemote": context.lineWidth}};
			sendData(JSON.stringify(sender));
		}else{
			context.fillStyle = colorBefore;
			context.strokeStyle = colorBefore;
			context.lineWidth = widthBefore;
			radius = widthBefore/2;
		}
	}
}

var engage = function(e){
	dragging = true;
	if(e.which){
		var sender = {"fn":"engage", "engage": true, "e":{"offsetX": e.offsetX, "offsetY": e.offsetY, "colorRemote": context.fillStyle, "widthRemote": context.lineWidth}};
		sendData(JSON.stringify(sender));
	}
	e.which = false;
	putPoint(e);
	
}

var disengage = function(e, s){
	dragging = false;
	context.beginPath();
	if (!s){
		var sender = {"fn":"disengage", "disengage":true};
		sendData(JSON.stringify(sender));
	}
}



var setRadius = function(newRadius){
	if(newRadius<minRad)
		newRadius = minRad;
	else if(newRadius>maxRad)
		newRadius = maxRad;
	radius = newRadius
	context.lineWidth = radius*2
	radSpan.innerHTML = radius;
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
	setColor(swatch.style.backgroundColor);
	swatch.className += ' active';
}