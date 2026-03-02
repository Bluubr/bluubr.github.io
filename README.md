# Pezutifier

A browser-based image-processing tool that lets users apply colour effects to images and share the results to a community gallery. The gallery is powered by **ImgBB** (image hosting) and **Firebase Firestore** (metadata storage). No server or build step is required — every file is plain HTML/CSS/JS.

---

## Table of Contents

1. [Running locally](#running-locally)
2. [Gallery Setup](#gallery-setup)
   - [Step 1 — ImgBB (image hosting)](#step-1--imgbb-image-hosting)
   - [Step 2 — Firebase project](#step-2--create-a-firebase-project)
   - [Step 3 — Register a web app inside Firebase](#step-3--register-a-web-app-inside-firebase)
   - [Step 4 — Enable Cloud Firestore](#step-4--enable-cloud-firestore)
   - [Step 5 — Configure the project files](#step-5--configure-the-project-files)
   - [Step 6 — Set Firestore security rules](#step-6--set-firestore-security-rules)
   - [Step 7 — Deploy](#step-7--deploy)
3. [File reference](#file-reference)
4. [Troubleshooting](#troubleshooting)

---

## Running locally

The project is entirely static. Open it directly in a browser:

```sh
# Clone the repository
git clone https://github.com/Bluubr/bluubr.github.io.git
cd bluubr.github.io

# Open the main page — no build step needed
open index.html          # macOS
xdg-open index.html      # Linux
start index.html         # Windows
```

> **Note:** Some browsers block local `file://` requests to external scripts.
> If the page doesn't load correctly, serve the files with any static HTTP server:
> ```sh
> npx serve .
> # then visit http://localhost:3000
> ```

The image-processing features work without any API keys. Only the **Share** and **Gallery** features require the setup below.

---

## Gallery Setup

To enable the **Share** button and the **Community Gallery** page you need two external services: ImgBB (stores the actual image file) and Firebase Firestore (stores the metadata — title, colour, timestamp — that appears in the gallery grid).

### Step 1 — ImgBB (image hosting)

ImgBB provides a free image-hosting API that accepts a single `POST` request with a `FormData` body. No OAuth or special headers are needed.

1. Go to <https://api.imgbb.com/> and create a free account.
2. After signing in, click **Get API key** (or visit <https://api.imgbb.com/> again when logged in).
   - Your key looks like a 32-character hex string, e.g. `a1b2c3d4e5f6...`.
3. Open `index.html` in a text editor and search for `IMGBB_API_KEY`. You will find this line:
   ```js
   const IMGBB_API_KEY = '__IMGBB_API_KEY__';
   ```
   Replace `__IMGBB_API_KEY__` with your actual key:
   ```js
   const IMGBB_API_KEY = 'a1b2c3d4e5f6yourActualKey';
   ```
4. Save the file.

> **Security:** The API key is visible in client-side JavaScript by design. To limit
> abuse, log into your ImgBB account and set a rate limit or allowed-origin restriction
> in the dashboard.

---

### Step 2 — Create a Firebase project

Firebase is Google's backend-as-a-service platform. Firestore is its NoSQL document database that the gallery uses to store image metadata.

1. Open <https://console.firebase.google.com> in your browser and sign in with a Google account.
2. Click **Add project** (or **Create a project** if this is your first time).
3. Enter a **Project name** — e.g. `pezutifier-gallery`. Firebase will auto-generate a unique project ID like `pezutifier-gallery-abc12`.
4. On the next screen, you can leave Google Analytics **enabled or disabled** — it does not affect the gallery. Click **Continue** (and choose an Analytics account if prompted), then click **Create project**.
5. Wait for Firebase to provision the project (takes about 10 seconds), then click **Continue** to open the project console.

---

### Step 3 — Register a web app inside Firebase

Firebase supports multiple app types (iOS, Android, Web). The gallery uses the Web SDK.

1. On the **Project Overview** page, click the **Web** icon — it looks like `</>` — under the heading *"Get started by adding Firebase to your app"*.
2. In the **App nickname** field enter a short label, e.g. `pezutifier`. (This is only for your reference inside the Firebase console.)
3. Leave **"Also set up Firebase Hosting"** unchecked unless you specifically want to use Firebase Hosting.
4. Click **Register app**.
5. Firebase will display a code snippet containing your `firebaseConfig` object:
   ```js
   const firebaseConfig = {
     apiKey:            "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
     authDomain:        "pezutifier-gallery-abc12.firebaseapp.com",
     projectId:         "pezutifier-gallery-abc12",
     storageBucket:     "pezutifier-gallery-abc12.appspot.com",
     messagingSenderId: "123456789012",
     appId:             "1:123456789012:web:abcdef1234567890abcdef"
   };
   ```
   **Copy all six values** — you will paste them into `gallery-config.js` in Step 5.
6. Click **Continue to console**.

What each field means:

| Field | Description |
|---|---|
| `apiKey` | Identifies your Firebase project to Google's servers. It is safe to expose in client-side code. |
| `authDomain` | Used for Firebase Authentication redirects. Required even if you don't use auth. |
| `projectId` | The unique ID of your Firebase project. Used to target the correct Firestore database. |
| `storageBucket` | Firebase Storage bucket hostname. Not used by the gallery but required to initialise the SDK. |
| `messagingSenderId` | Used for Firebase Cloud Messaging (push notifications). Not used by the gallery. |
| `appId` | Uniquely identifies this specific web app registration within your project. |

---

### Step 4 — Enable Cloud Firestore

Firestore is the database that stores gallery entries. It must be explicitly enabled for each Firebase project.

1. In the left sidebar of the Firebase console, click **Build** to expand the menu, then click **Firestore Database**.
2. Click **Create database**.
3. On the *"Secure rules"* screen, choose **Start in test mode**.
   > Test mode allows anyone to read and write to your database for 30 days — ideal for
   > development. You will lock this down in [Step 6](#step-6--set-firestore-security-rules)
   > before going public.
4. Click **Next**.
5. Choose a **Cloud Firestore location** (a geographic region). Pick one close to your users — for example `us-central1` (Iowa) or `europe-west1` (Belgium). **This cannot be changed after creation.**
6. Click **Done** and wait about 30 seconds for Firestore to finish provisioning.

The gallery writes documents to a collection named **`gallery`**. Each document contains:

| Field | Type | Description |
|---|---|---|
| `imageUrl` | string | Public URL of the image on ImgBB |
| `deleteUrl` | string | ImgBB URL to delete the image (stored for moderation) |
| `color` | string | Hex colour used when processing the image |
| `contentType` | string | Type of content (e.g. `photo`, `art`) |
| `timestamp` | string | ISO 8601 date-time string of when the image was shared |
| `title` | string | Optional title entered by the user |

---

### Step 5 — Configure the project files

`gallery-config.js` already exists in the repository with placeholder values. You just need to fill in your real Firebase credentials.

1. Open `gallery-config.js` in a text editor. You will see six placeholder values:
   ```js
   const firebaseConfig = {
     apiKey:            '__FIREBASE_API_KEY__',
     authDomain:        '__FIREBASE_AUTH_DOMAIN__',
     projectId:         '__FIREBASE_PROJECT_ID__',
     storageBucket:     '__FIREBASE_STORAGE_BUCKET__',
     messagingSenderId: '__FIREBASE_MESSAGING_SENDER_ID__',
     appId:             '__FIREBASE_APP_ID__',
   };
   ```
   Replace each placeholder with the exact value from the `firebaseConfig` snippet you copied in Step 3:
   ```js
   const firebaseConfig = {
     apiKey:            'AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
     authDomain:        'pezutifier-gallery-abc12.firebaseapp.com',
     projectId:         'pezutifier-gallery-abc12',
     storageBucket:     'pezutifier-gallery-abc12.appspot.com',
     messagingSenderId: '123456789012',
     appId:             '1:123456789012:web:abcdef1234567890abcdef',
   };
   ```
2. Save the file.

> ⚠️ **Do not commit real Firebase credentials to a public repository.**
> `gallery-config.js` is currently tracked by git with placeholder values. Before
> replacing the placeholders with real credentials, stop git from tracking the file:
> ```sh
> echo "gallery-config.js" >> .gitignore
> git rm --cached gallery-config.js   # stop tracking the file
> git commit -m "untrack gallery-config.js"
> ```
> After that, your local changes to `gallery-config.js` will not be staged or committed.
> Use `gallery-config.example.js` as the committed template reference.

> **How it works:** `gallery-config.js` is loaded by both `index.html` and `gallery.html`
> via `<script src="gallery-config.js">`. It calls `firebase.initializeApp(firebaseConfig)`
> and exposes the Firestore instance as `window._pezFirestore`. If the file is missing or
> still contains placeholder values, the gallery silently falls back to a "not configured"
> message — nothing breaks.

---

### Step 6 — Set Firestore security rules

The default test-mode rules expire after 30 days and allow unrestricted writes. Before making your gallery public, update the rules to allow anyone to read but only authenticated or rate-limited users to write (or simply use the rules below to allow public reads and public writes, which is fine for a hobby project with low traffic).

1. In the Firebase console, go to **Build → Firestore Database → Rules**.
2. Replace the default rules with one of the following options and click **Publish**:

**Option A — Public read, public write (simple hobby setup):**
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /gallery/{docId} {
      allow read: if true;
      allow create: if request.resource.data.keys().hasAll(['imageUrl', 'color', 'contentType', 'timestamp'])
                   && request.resource.data.imageUrl is string
                   && request.resource.data.imageUrl.size() < 2048;
    }
  }
}
```
This allows anyone to add a gallery entry as long as the required fields are present, but it prevents writes to other collections and prevents updating or deleting existing entries.

**Option B — Public read, no writes (read-only / curated gallery):**
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /gallery/{docId} {
      allow read: if true;
      allow write: if false;
    }
  }
}
```
Use this if you want to manually populate the gallery without allowing public submissions.

---

### Step 7 — Deploy

Once both keys are in place (`IMGBB_API_KEY` in `index.html` and the Firebase config in `gallery-config.js`), deploy the static files to any host:

- **GitHub Pages** — push to a `gh-pages` branch or enable Pages from your repo's **Settings → Pages** menu.
- **Firebase Hosting** — run `firebase deploy` after installing the Firebase CLI (`npm install -g firebase-tools`).
- **Any static host** — Netlify, Vercel, Cloudflare Pages, etc. Simply upload the project folder.

After deploying, open `gallery.html` on your live URL — images shared via the **Share** button in `index.html` will appear there within a few seconds.

---

## File reference

| File | Purpose |
|---|---|
| `index.html` | Main Pezutifier app — image upload, colour controls, and the Share button |
| `gallery.html` | Community gallery — reads entries from Firestore and displays them in a grid |
| `gallery-config.js` | Firebase credentials — tracked with placeholder values; replace them or git-ignore before adding real keys |
| `gallery-config.example.js` | Template for `gallery-config.js` — safe to commit |
| `clickdefault.js` | Small utility script used by the main app |

---

## Troubleshooting

**The Share button does nothing / shows an error**
- Check that `IMGBB_API_KEY` in `index.html` has been replaced with your real key (no surrounding underscores).
- Open the browser's developer console (F12 → Console) and look for an error message.

**The Gallery page shows "community gallery is not configured"**
- Verify that `gallery-config.js` exists and that all six values have been replaced (no `__` prefixes remain).
- Make sure `gallery-config.js` is being served alongside the HTML files (it is not bundled — it must be a separate file).

**Firestore permission denied errors in the console**
- Your Firestore security rules are too restrictive. Go to **Firebase console → Firestore Database → Rules** and check the published rules.
- If you set up the database in test mode more than 30 days ago, test mode will have expired — update the rules as shown in [Step 6](#step-6--set-firestore-security-rules).

**Images upload but don't appear in the gallery**
- Confirm that `gallery-config.js` is loaded and Firestore is initialised (`window._pezFirestore` should be truthy in the browser console).
- Check Firestore write rules — the `create` operation must be allowed.
- Open the Firebase console → **Firestore Database** → **Data** and verify that documents are appearing in the `gallery` collection.
