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

1. Go to <https://console.firebase.google.com> and click **Add project**.
   - Enter a project name, click **Continue**, then **Create project**.

2. Inside the project, click the **Web** icon (`</>`) to add a web app.
   - Enter a nickname (e.g. `pezutifier`), then click **Register app**.
   - Firebase will show you a `firebaseConfig` object — **copy it**, you'll need it shortly.
   - Click **Continue to console**.

3. Enable Cloud Firestore:
   - In the left sidebar, click **Build → Firestore Database**.
   - Click **Create database**.
   - Choose **Start in test mode** (allows public reads and writes while you develop).
   - Pick a region near your users and click **Done**.

4. Copy `gallery-config.example.js` to `gallery-config.js`:
   ```sh
   cp gallery-config.example.js gallery-config.js
   ```

5. Open `gallery-config.js` and replace every `YOUR_…` placeholder with the
   matching value from the `firebaseConfig` object Firebase gave you in step 2:
   ```js
   const firebaseConfig = {
     apiKey:            'AIzaSy…',          // apiKey
     authDomain:        'my-project.firebaseapp.com',
     projectId:         'my-project',
     storageBucket:     'my-project.appspot.com',
     messagingSenderId: '123456789012',
     appId:             '1:123456789012:web:abc123…',
   };
   ```

6. Deploy — shared images will automatically appear in the Gallery page.

> **Security note:** When you're ready to go public, set proper Firestore security rules
> (e.g. public read, authenticated write) in the Firebase console under
> **Firestore Database → Rules**.
