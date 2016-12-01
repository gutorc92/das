var displayArea = document.getElementById('photos');

function displayImage(image) {
	displayArea.removeChild(displayArea.firstChild);
	
	var originalImage = document.createElement('img');
	var oldSrc = image.src.split('_t.jpg');
	var newSrc = oldSrc[0] + '_b.jpg';
	originalImage.src = newSrc;

	displayArea.innerHTML = '<img id="loading" src="/static/images/loading.gif">';
	
	originalImage.onload = function() {
		if(originalImage.complete) {
			displayArea.innerHTML = '';
			fitImageDisplayArea(originalImage);
			displayArea.appendChild(originalImage);
		}
	}	
}

function fitImageDisplayArea(image){
	var aspectRatio = image.height / image.width;

	if(image.width && aspectRatio <= 1){
		image.width = displayArea.offsetWidth - 32;
		image.height = image.width * aspectRatio - 32;
		
		if(image.height > displayArea.offsetHeight) {
			image.height = displayArea.offsetHeight - 32;
		}
	} 

	else if(image.height >= displayArea.offsetHeight){
		image.height = displayArea.offsetHeight - 32;
		image.width = image.height / aspectRatio - 32;
		
		if(image.width > displayArea.offsetWidth) {
			image.width = displayArea.offsetWidth - 32;
		}
	}
	
	displayArea.style.marginTop = (displayArea.offsetHeight - image.height)/2 + 'px';
}