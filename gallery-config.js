/**
 * gallery-config.js
 *
 * Fill in your Firebase project values below, then deploy.
 * See README.md § Gallery Setup for step-by-step instructions.
 */

const firebaseConfig = {
  apiKey:            'YOUR_API_KEY',
  authDomain:        'YOUR_PROJECT_ID.firebaseapp.com',
  projectId:         'YOUR_PROJECT_ID',
  storageBucket:     'YOUR_PROJECT_ID.appspot.com',
  messagingSenderId: 'YOUR_SENDER_ID',
  appId:             'YOUR_APP_ID',
};

// Only initialise Firebase when all placeholder values have been replaced
const _required = ['apiKey', 'authDomain', 'projectId', 'storageBucket', 'messagingSenderId', 'appId'];
if (_required.every(k => !String(firebaseConfig[k]).startsWith('YOUR_'))) {
  firebase.initializeApp(firebaseConfig);
  window._pezFirestore = firebase.firestore();
}
