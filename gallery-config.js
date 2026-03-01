/**
 * gallery-config.js
 *
 * Fill in your Firebase project values below, then deploy.
 * See README.md § Gallery Setup for step-by-step instructions.
 */

const firebaseConfig = {
  apiKey:            '__FIREBASE_API_KEY__',
  authDomain:        '__FIREBASE_PROJECT_ID__.firebaseapp.com',
  projectId:         '__FIREBASE_PROJECT_ID__',
  storageBucket:     '__FIREBASE_PROJECT_ID__.appspot.com',
  messagingSenderId: '__FIREBASE_SENDER_ID__',
  appId:             '__FIREBASE_APP_ID__',
};

// Only initialise Firebase when all placeholder values have been replaced
const _required = ['apiKey', 'authDomain', 'projectId', 'storageBucket', 'messagingSenderId', 'appId'];
if (_required.every(k => {
  const v = String(firebaseConfig[k]);
  return !v.startsWith('YOUR_') && !v.startsWith('__');
})) {
  firebase.initializeApp(firebaseConfig);
  window._pezFirestore = firebase.firestore();
}
