var request = '';
var allImages = '';
var uri = '';

function loadImages(id) {
	var carousel_images = document.getElementById("carousel-images");
	carousel.style.display = 'none';

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
			var jsonResponse = JSON.parse(this.responseText);
			var imageSource = jsonResponse["pictures"];

			openImages(imageSource);
   	}
  };

  xhttp.open("GET","/gallery/listpictures/" + id, true);
  xhttp.send();
}

function openImages(source) {
	var carousel = document.getElementById('carousel-images');

	while (carousel.firstChild) {
		carousel.removeChild(carousel.firstChild);
	}

	var categoryImage = document.createElement('img');
	categoryImage.src = "/" + source;
	categoryImage.onload = centerImage;
	categoryImage.onclick = centerImage;

	fitImageCarousel(categoryImage);
	carousel.appendChild(categoryImage);

	allImages = document.getElementsByTagName('img');
	clickAction(allImages[1]);

	carousel.style.display = 'block';
}
