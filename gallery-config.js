/**
 * gallery-config.js
 *
 * Fill in your Firebase project values below, then deploy.
 * See README.md § Gallery Setup for step-by-step instructions.
 */

const firebaseConfig = {
  apiKey:            '__YOUR_API_KEY__',
  authDomain:        '__YOUR_PROJECT_ID__.firebaseapp.com',
  projectId:         '__YOUR_PROJECT_ID__',
  storageBucket:     '__YOUR_PROJECT_ID__.appspot.com',
  messagingSenderId: '__YOUR_SENDER_ID__',
  appId:             '__YOUR_APP_ID__',
};

// Only initialise Firebase when all placeholder values have been replaced
const _required = ['apiKey', 'authDomain', 'projectId', 'storageBucket', 'messagingSenderId', 'appId'];
if (_required.every(k => !String(firebaseConfig[k]).startsWith('YOUR_'))) {
  firebase.initializeApp(firebaseConfig);
  window._pezFirestore = firebase.firestore();
}
