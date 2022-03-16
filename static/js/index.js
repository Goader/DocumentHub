document.getElementById('file-button').addEventListener('click', openDialog);

function openDialog() {
    document.getElementById('file-upload').click();
}

function sendFile() {
    let photo = document.getElementById("file-upload").files[0];
    let formData = new FormData();
        
    formData.append("file", photo);
    fetch('/upload', {method: "POST", body: formData});
}
