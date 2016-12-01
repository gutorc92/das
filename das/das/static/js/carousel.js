var previousImage = '';
var images;
var currentImage;

function centerImage(event) {
	var image = event.srcElement || event.target;	
	var innerLeft = image.offsetLeft;
	
	var halfOuterWidth = document.getElementById('carousel').offsetWidth / 2;
	var halfImageWidth = image.offsetWidth / 2;
	
	var outerLeft = halfOuterWidth - halfImageWidth; 
	
	document.getElementById('carousel-images').style.left = (outerLeft - innerLeft) + 'px';
	
	if(previousImage != '') {
		animation();
	}
	
	changeOpacity(image);
	
	setTimeout(function() {
		displayImage(image);
	}, 1000);

	currentImage = image;
}

function animation() {
	document.getElementById('carousel-images').style.WebkitTransition = 'left 1s ease-in-out';
	document.getElementById('carousel-images').style.transition = 'left 1s ease-in-out';
}

function changeOpacity(image) {	
	if(previousImage != '') {
		previousImage.classList.remove('active');
	}
	
	image.className = 'active';
	
	previousImage = image;
}

function changeMainImage(arrow_position) {
	images = document.getElementsByTagName('img'); 
	var i = currentImageIndex = 1;
	
	while(i < images.length - 1) {
		if(images[i].className == 'active') {
			currentImageIndex = i;
			break;
		}
		
		else {
			i++;
		}
	}
	
	if(arrow_position == 'left') {
		// If the previous image is not the left arrow (images[0]), the new main image is the previous of the current one
		if(currentImageIndex-1 != 0) {
			clickAction(images[currentImageIndex-1]);
		}
		// If previous image is the left arrow, the new main image is the last one
		else {
			clickAction(images[images.length-3]);
		}
	}
	
	else {
		// If the next image is not the right arrow (images[lenght-1]), the new main image is the next of the current one
		if(currentImageIndex+1 != images.length-2) {
			clickAction(images[currentImageIndex+1]);
		}
		// If the next image is the right arrow, the new main image is the first one
		else {
			clickAction(images[1]);
		}
	}
}

function clickAction(element) {
	var event = document.createEvent("MouseEvents");
	event.initEvent("click", true, true);
	element.dispatchEvent(event);
}

document.onkeydown = keyboardArrows;
function keyboardArrows(e){    
	e = e || window.event;
	var key = e.which || e.keyCode;

    switch(key) {
        case 37:
			changeMainImage('left');
            break;
			
        case 39:
            changeMainImage('right');
            break;
    }   
}

window.onresize = centerImageOnResize;
function centerImageOnResize(e) {	
	clickAction(currentImage);
}

var carousel = document.getElementById('carousel-images');
function fitImageCarousel(image){

	var aspectRatio = image.height / image.width;

	if(image.width >= image.height){
		image.width = 150;
		image.height = 100;
	} 
	
	else {
		image.height = 100;
		image.width = image.height / aspectRatio;
	}
}