window.onload = () => {
  const btn = document.getElementById('useDefaultBtn');
  if (btn) {
    btn.click();
  }
};
async function uploadToProxy(base64Image) {
  // MUST include the full path to the function
  const proxyUrl = 'https://your-site-name.netlify.app';

  const response = await fetch(proxyUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ image: base64Image })
  });

  const result = await response.json();
  if (result.success) {
    console.log("Uploaded Image URL:", result.data.url);
    alert("Upload successful!");
  } else {
    console.error("Upload failed", result);
  }
}
