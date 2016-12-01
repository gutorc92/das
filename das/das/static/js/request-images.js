var request = '';
var allImages = '';
var uri = '';

function findImages() {
	var carousel_images = document.getElementById("carousel-images");
	carousel.style.display = 'none';
	
	while (carousel_images.firstChild) {
		carousel_images.removeChild(carousel_images.firstChild);
	}
	
	var tags = document.getElementsByTagName('input');
	
	uri = "https://www.flickr.com/services/rest/?";
	uri += "method=flickr.photos.search";
	uri += "&api_key=f2d3e882afae6220e175c126c6b971ed";
	
	var tagsString = '';
	var emptyTag = 0;
	for(var i = 0; i < tags.length; i++) {
		if(i+1 < tags.length) {
			if(tags[i+1].value != '') {
				tagsString += tags[i].value + ',';
			}

			else {
				emptyTag++;
			}
		}
		
		else {
			if(tags[i].value != '') {
				tagsString += tags[i].value;
			}

			else {
				emptyTag++;
			}
		}
	}
	
	uri += "&tags=" + tagsString;
	uri += "&tag_mode=all";
	uri += "&format=json";
	
	if(emptyTag == 0) {
		request = encodeURI(uri);
		sendRequest(request);
		
		document.getElementById('find-images').innerHTML = '<img id="loading" src="/static/images/loading.gif">';
		document.getElementById('photos').innerHTML = '<img id="loading" src="/static/images/loading.gif">';
	}
	
	else {
		document.getElementById('photos').innerHTML = 'Empty Tag Detected';
	}
}

function sendRequest(url) {
	var head = document.getElementsByTagName('head')[0];
	var newScript = document.createElement('script');
	newScript.setAttribute('src', url);

	head.appendChild(newScript);
}