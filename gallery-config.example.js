/**
 * gallery-config.example.js
 *
 * To enable the community gallery and ImgBB sharing:
 *
 * 1. Copy this file to `gallery-config.js` (git-ignored by default).
 * 2. Create a free Firebase project at https://console.firebase.google.com
 *    - Add a web app and copy the firebaseConfig values below.
 *    - Enable Cloud Firestore (start in "test mode" for quick setup).
 * 3. Get a free ImgBB API key at https://api.imgbb.com/
 *    and set IMGBB_API_KEY in index.html.
 */

const firebaseConfig = {
  apiKey:            'YOUR_API_KEY',
  authDomain:        'YOUR_PROJECT_ID.firebaseapp.com',
  projectId:         'YOUR_PROJECT_ID',
  storageBucket:     'YOUR_PROJECT_ID.appspot.com',
  messagingSenderId: 'YOUR_SENDER_ID',
  appId:             'YOUR_APP_ID',
};

// Initialise Firebase and expose Firestore globally for index.html / gallery.html
firebase.initializeApp(firebaseConfig);
window._pezFirestore = firebase.firestore();
