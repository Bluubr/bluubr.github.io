// No need to install node-fetch if using Node.js 18+ on Netlify
exports.handler = async (event) => {
  // 1. Handle CORS Preflight (Required for GitHub Pages to talk to Netlify)
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST, OPTIONS"
      }
    };
  }

  // 2. Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const { image } = JSON.parse(event.body);
    const apiKey = process.env.IMGBB_API_KEY; // Secret key from Netlify Dashboard

    if (!apiKey) {
      throw new Error("Missing IMGBB_API_KEY in environment variables.");
    }

    // 3. Prepare data for imgBB (they expect 'application/x-www-form-urlencoded')
    const formData = new URLSearchParams();
    formData.append('image', image); // The base64 string

    const response = await fetch(`https://api.imgbb.com{apiKey}`, {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    // 4. Return result with CORS headers
    return {
      statusCode: 200,
      headers: { 
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    };
  } catch (err) {
    console.error("Function Error:", err.message);
    return { 
      statusCode: 500, 
      headers: { "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ error: err.message }) 
    };
  }
};
