function addField() {
	var fieldsParent = document.getElementById('text-fields');
	var newDiv = document.createElement('div');
	var newField = document.createElement('input');
	var minusButton = document.createElement('button');
			
	newField.className = 'tag';
	newField.type = 'text';
	minusButton.appendChild(document.createTextNode('-'));
	minusButton.className = 'remove-field';
	minusButton.onclick = removeField;
			
	newDiv.appendChild(newField);
	newDiv.appendChild(minusButton);
	fieldsParent.appendChild(newDiv);
}

function removeField() {
	var buttonParent = this.parentNode;
	var divParent = buttonParent.parentNode;
	
	divParent.removeChild(buttonParent);
}