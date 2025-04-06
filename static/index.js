// Upload counter functionality
let uploadCount = localStorage.getItem('uploadCount') || 0;
        
function updateCounter() {
	document.querySelector('.counter-number').textContent = uploadCount;
	localStorage.setItem('uploadCount', uploadCount);
	updateRank();
}

function handleFileUpload(input) {
    if (input.files.length > 0) {
        uploadCount++;
        updateCounter();
        document.getElementById('uploadForm').submit();
    }
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
	const files = e.dataTransfer.files;
	if (files.length > 0) {
		fileInput.files = files;
		handleFileUpload(fileInput);
	}
	uploadArea.style.borderColor = '#eee';
});

function getRank(uploadCount) {
    if (uploadCount < 50) return "Unranked";
    if (uploadCount < 200) return "Bronze";
    if (uploadCount < 500) return "Silver";
    if (uploadCount < 1000) return "Platinum";
    if (uploadCount < 2000) return "Diamond";
    if (uploadCount < 3000) return "Trash Titan";
    return "Waste Warden";
}

function updateRank() {
    const rank = getRank(uploadCount);
    document.querySelectorAll('.rank-title').forEach(element => {
        element.textContent = `Rank: ${rank}`;
    });
}

// Update rank on page load
document.addEventListener('DOMContentLoaded', () => {
    updateRank();
});