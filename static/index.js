// Upload counter functionality
let uploadCount = localStorage.getItem('uploadCount') || 0;
        
function updateCounter() {
	document.querySelector('.counter-number').textContent = uploadCount;
	localStorage.setItem('uploadCount', uploadCount);
}

function handleFileUpload(input) {
	uploadCount++;
	updateCounter();
	input.form.submit();
}

// Initialize counter on page load
document.addEventListener('DOMContentLoaded', () => {
	uploadCount = parseInt(localStorage.getItem('uploadCount')) || 0;
	updateCounter();
});

// Drag & drop functionality
const uploadArea = document.getElementById('fileInput');
const fileInput = document.getElementById('file');

uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
	e.preventDefault();
	uploadArea.style.borderColor = '#4ecdc4';
});

uploadArea.addEventListener('dragleave', () => {
	uploadArea.style.borderColor = '#eee';
});

uploadArea.addEventListener('drop', (e) => {
	e.preventDefault();
	fileInput.files = e.dataTransfer.files;
	handleFileUpload(fileInput);
	uploadArea.style.borderColor = '#eee';
});