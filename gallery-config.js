/**
 * gallery-config.js
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
  apiKey:            'AIzaSyBRj4N7uLOs6PrlrjxpJ8BchmlkLz3cmuk',
  authDomain:        'pezut-17f8c.firebaseapp.com',
  projectId:         'pezut-17f8c',
  storageBucket:     'pezut-17f8c.firebasestorage.app',
  messagingSenderId: '968084696936',
  appId:             '1:968084696936:web:fdbb88b2b21697b03d30dd',
};

// Initialise Firebase and expose Firestore globally for index.html / gallery.html
firebase.initializeApp(firebaseConfig);
window._pezFirestore = firebase.firestore();
