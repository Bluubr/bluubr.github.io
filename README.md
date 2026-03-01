# Pezutifier
PEZUT

## Gallery Setup

To enable the **community gallery** and **image sharing** features:

### 1. ImgBB (image hosting)

ImgBB has the simplest possible API — one POST request with a `FormData` body, no OAuth or special headers.

1. Create a free account and get an API key at <https://api.imgbb.com/>.
2. In `index.html`, replace `YOUR_IMGBB_API_KEY` with your key:
   ```js
   const IMGBB_API_KEY = 'abc123yourApiKey';
   ```

### 2. Firebase (community gallery)

1. Create a free project at <https://console.firebase.google.com>.
2. Add a **Web** app to the project and copy the `firebaseConfig` object.
3. Enable **Cloud Firestore** (start in *test mode* while developing).
4. Copy `gallery-config.example.js` to `gallery-config.js` (this file is git-ignored):
   ```sh
   cp gallery-config.example.js gallery-config.js
   ```
5. Fill in your Firebase values in `gallery-config.js`.
6. Deploy — shared images will automatically appear in the Gallery page.

> **Security note:** When you're ready to go public, set proper Firestore security rules
> (e.g. public read, authenticated write) in the Firebase console.
