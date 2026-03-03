const fetch = require('node-fetch');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    // 2. Get your Secret Key from Netlify Environment Variables
    const apiKey = process.env.IMGBB_API_KEY;
    const body = JSON.parse(event.body);
    
    // 3. Send the image to imgBB with your hidden key
    const response = await fetch(`https://api.imgbb.com{apiKey}`, {
      method: 'POST',
      body: new URLSearchParams({
        image: body.image, // Base64 string of the image
      }),
    });

    const data = await response.json();

    // 4. Return the result back to your GitHub Page
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*", // Allows your GitHub Page to talk to this
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data),
    };
  } catch (error) {
    return { statusCode: 500, body: JSON.stringify({ error: error.message }) };
  }
};
