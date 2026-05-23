// static/upload-handler.js

document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("fileInput");
  const predictBtn = document.getElementById("predictBtn");
  const uploadText = document.querySelector(".upload-text");
  const uploadSubtext = document.querySelector(".upload-subtext");
  const uploadFormat = document.querySelector(".upload-format");

  if (fileInput) {
    fileInput.addEventListener("change", function () {
      const file = this.files[0];

      if (!file) {
        uploadText.innerHTML = "Drag & Drop File Here";
        uploadSubtext.innerHTML = "or click to browse CSV / XLSX file";
        uploadFormat.innerHTML = "Shape Required : (1 × 30 × 5)";
        predictBtn.disabled = true;
        return;
      }

      const fileName = file.name;
      const fileSize = (file.size / 1024).toFixed(2); // Menggunakan satuan KB
      const fileExtension = fileName.split(".").pop().toLowerCase();
      const allowedExtensions = ["csv", "xlsx", "xls"];

      if (!allowedExtensions.includes(fileExtension)) {
        uploadText.innerHTML = "Unsupported File";
        uploadSubtext.innerHTML = "Please upload CSV or Excel file";
        uploadFormat.innerHTML = "Allowed: CSV, XLSX, XLS";
        this.value = "";
        predictBtn.disabled = true;
        return;
      }

      uploadText.innerHTML = fileName;
      uploadSubtext.innerHTML = `File size : ${fileSize} KB`;
      uploadFormat.innerHTML = "Ready for prediction";
      predictBtn.disabled = false;
    });
  }
});

// Fungsi Global untuk menutup Box Error Alert
function closeError() {
  const box = document.getElementById("errorBox");
  if (box) {
    box.style.display = "none";
  }
}