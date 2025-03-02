document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    let fileInput = document.getElementById("fileInput");
    let statusText = document.getElementById("status");
    let downloadLink = document.getElementById("downloadLink");
  
    if (!fileInput.files.length) {
        statusText.innerText = "Please select a file.";
        return;
    }
  
    let file = fileInput.files[0];
    let formData = new FormData();
    formData.append("file", file);
  
    statusText.innerText = "Uploading and converting...";
  
    try {
        let response = await fetch("http://127.0.0.1:5000/convert", {
            method: "POST",
            body: formData
        });
  
        let result = await response.json();
  
        if (response.ok) {
            statusText.innerText = "Conversion successful!";
            downloadLink.href = `http://127.0.0.1:5000${result.download_url}`;
            downloadLink.style.display = "block";
            downloadLink.innerText = "Download Converted File";
        } else {
            statusText.innerText = "Error: " + result.error;
            downloadLink.style.display = "none";
        }
    } catch (error) {
        statusText.innerText = "Failed to connect to the server.";
    }
  });
  