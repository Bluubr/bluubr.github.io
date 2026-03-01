# Pezutifier
PEZUT

## Gallery Setup

To enable the **community gallery** and **image sharing** features:

### 1. Imgur (image hosting)

1. Register a free app at <https://api.imgur.com/oauth2/addclient> (choose *OAuth 2 authorization without a callback URL*).
2. Copy your **Client ID**.
3. In `index.html`, replace `YOUR_IMGUR_CLIENT_ID` with your Client ID:
   ```js
   const IMGUR_CLIENT_ID = 'abc123yourClientId';
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
