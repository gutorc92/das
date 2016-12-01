var displayArea = document.getElementById('photos');

function displayImage(image) {
	while(displayArea.firstChild) {
		displayArea.removeChild(displayArea.firstChild);
	}

	var originalImage = document.createElement('img');
	originalImage.src = image.src;

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

	if(image.width && aspectRatio < 1) {
		image.width = displayArea.offsetWidth - 32;
		image.height = image.width * aspectRatio - 32;

		if(image.height > displayArea.offsetHeight) {
			image.height = displayArea.offsetHeight - 32;
		}
	}

	else if(image.width && aspectRatio == 1) {
		image.height = image.width * aspectRatio - 32;
		image.width = image.height;
	}

	else if(image.height >= displayArea.offsetHeight) {
		image.height = displayArea.offsetHeight - 32;
		image.width = image.height / aspectRatio - 32;

		if(image.width > displayArea.offsetWidth) {
			image.width = displayArea.offsetWidth - 32;
		}
	}

	displayArea.style.marginTop = (displayArea.offsetHeight - image.height)/2 + 'px';
}
