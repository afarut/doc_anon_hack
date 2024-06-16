document.addEventListener("DOMContentLoaded", function() {
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-theme");
        document.getElementById("themeIcon").classList.remove("fa-sun");
        document.getElementById("themeIcon").classList.add("fa-moon");
        document.getElementById("themeSwitch").checked = true;
    }
});

function toggleTheme() {
    document.body.classList.toggle("dark-theme");

    const themeIcon = document.getElementById("themeIcon");
    if (document.body.classList.contains("dark-theme")) {
        themeIcon.classList.remove("fa-sun");
        themeIcon.classList.add("fa-moon");
        localStorage.setItem("theme", "dark");
    } else {
        themeIcon.classList.remove("fa-moon");
        themeIcon.classList.add("fa-sun");
        localStorage.setItem("theme", "light");
    }
}

const dropzoneOverlay = document.getElementById('dropzone-overlay');
    const formUpload = document.querySelector('.form-upload');
    const fileInput = document.getElementById('file-upload');
    const fileUploadLabel = document.querySelector('.custom-file-upload');

document.addEventListener('dragenter', function(event) {
    if (!isDescendant(dropzoneOverlay, event.target) && event.target !== dropzoneOverlay) {
        return;
    }
    event.preventDefault();
    dropzoneOverlay.style.display = 'block';
});

document.addEventListener('dragleave', function(event) {
    if (!isDescendant(dropzoneOverlay, event.relatedTarget) && event.relatedTarget !== dropzoneOverlay) {
        return;
    }
    event.preventDefault();
    dropzoneOverlay.style.display = 'none';
});

document.addEventListener('dragover', function(event) {
    event.preventDefault();
});

document.addEventListener('drop', function(event) {
    event.preventDefault();
    dropzoneOverlay.style.display = 'none';

    const files = event.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        fileUploadLabel.textContent = files[0].name;
    }
});
function isDescendant(parent, child) {
    let node = child.parentNode;
    while (node != null) {
        if (node === parent) {
            return true;
        }
        node = node.parentNode;
    }
    return false;
}

fileInput.addEventListener('change', function(event) {
    if (fileInput.files.length > 0) {
        fileUploadLabel.textContent = fileInput.files[0].name;
    }
});