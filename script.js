const baseFileInput = document.getElementById('baseFileInput');
const useDefaultBtn = document.getElementById('useDefaultBtn');
const colorPicker = document.getElementById('colorPicker');
const processBtn = document.getElementById('processBtn');
const outputCanvas = document.getElementById('outputCanvas');
const resultSection = document.getElementById('resultSection');
const downloadLink = document.getElementById('downloadLink');

let selectedImage = null;

// Handle File Uploads
baseFileInput.onchange = (e) => {
  const file = e.target.files[0];
  if (file) {
    document.getElementById('baseName').innerText = file.name;
    const reader = new FileReader();
    reader.onload = (event) => {
      const img = new Image();
      img.onload = () => selectedImage = img;
      img.src = event.target.result;
    };
    reader.readAsDataURL(file);
  }
};

// Use Default Base.png
useDefaultBtn.onclick = () => {
  const img = new Image();
  img.crossOrigin = "anonymous";
  img.onload = () => {
    selectedImage = img;
    document.getElementById('baseName').innerText = "Base.png Loaded";
  };
  img.src = "Base.png"; // Ensure this file exists in your folder!
};

// Update Color Text
colorPicker.oninput = (e) => {
  document.getElementById('colorMeta').innerText = `Hex: ${e.target.value.toUpperCase()}`;
};

// The "Pezutify" Core Logic
processBtn.onclick = () => {
  if (!selectedImage) return alert("Please select an image first!");

  const ctx = outputCanvas.getContext('2d');
  outputCanvas.width = selectedImage.width;
  outputCanvas.height = selectedImage.height;

  // 1. Draw base image
  ctx.drawImage(selectedImage, 0, 0);

  // 2. Apply color overlay using "multiply" or "source-atop"
  ctx.globalCompositeOperation = 'source-atop'; 
  ctx.fillStyle = colorPicker.value;
  ctx.fillRect(0, 0, outputCanvas.width, outputCanvas.height);

  // 3. Reset operation to default
  ctx.globalCompositeOperation = 'source-over';

  // Show results
  resultSection.classList.remove('hidden');
  downloadLink.href = outputCanvas.toDataURL("image/png");
  downloadLink.download = "pezutified-image.png";
};
