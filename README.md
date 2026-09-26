# Phone-as-Mouse-Keyboard

Turn your Android smartphone into a wireless mouse and keyboard for your PC using Wi-Fi.

## 📌 Overview

**Phone-as-Mouse-Keyboard** is a lightweight Android application that allows you to control a Windows PC using an Android smartphone.

The project uses:

- An Android app for the phone-side interface
- A Python WebSocket server running on the PC
- Wi-Fi for communication between the phone and PC
- `pyautogui` to control the PC mouse and keyboard

The phone works as a wireless:

- 🖱️ Mouse
- ⌨️ Keyboard
- 🔘 Left / Double / Right mouse buttons
- ↕️ Scroll controller
- ⎋ Ctrl / Alt / Esc / Tab / Arrow keys
- 😀 Emoji keyboard

---

## ✨ Features

### 🖱️ Touchpad

The touchpad supports:

- One-finger movement → Move mouse pointer
- Single tap → Left click
- Double tap → Double click
- Two-finger tap → Right click
- Two-finger swipe → Scroll

Dedicated buttons are also available for:

- Left Click
- Double Click
- Right Click

### ⌨️ Android-style Keyboard

The application includes a touch keyboard with:

- Alphabet keys
- Number row
- Shift
- Backspace
- Enter
- Space
- Symbols
- Ctrl
- Alt
- Esc
- Tab
- Arrow keys
- Emoji keyboard
- Continuous Backspace when the Backspace key is held

### 😀 Emoji Keyboard

The app includes a large emoji pad with multiple emoji categories.

Users can switch between the normal keyboard and emoji keyboard from the keyboard interface.

### ⚙️ Settings

The application provides settings for:

- PC IP address
- Pointer sensitivity
- Scroll speed
- Connection management

Only the PC IP address needs to be entered manually. The application automatically creates:

```
ws://PC-IP:5000/ws
```

---

## 🏗️ Project Architecture

The project consists of two main parts.

```
Android Phone
     │
     │ Wi-Fi / WebSocket
     ▼
Python WebSocket Server
     │
     ▼
Windows PC
     │
     └── pyautogui
             │
             ├── Mouse
             └── Keyboard
```

**Communication Flow**

```
Phone UI
   ↓
WebSocket
   ↓
Python server.py
   ↓
pyautogui
   ↓
Windows Mouse & Keyboard
```

---

## 🛠️ Technologies Used

### Android

- Java
- Android SDK
- WebView
- HTML
- CSS
- JavaScript

The Android application loads the web interface locally from:

```
app/src/main/assets/index.html
```

### PC Server

- Python
- websockets
- pyautogui

The server receives commands from the Android app and converts them into mouse and keyboard actions.

---

## 📁 Project Structure

```
Phone-as-Mouse-Keyboard/
│
├── app/
│   ├── build.gradle
│   └── src/
│       └── main/
│           ├── AndroidManifest.xml
│           │
│           ├── assets/
│           │   ├── index.html
│           │   └── emoji-data.js
│           │
│           ├── java/
│           │   └── com/
│           │       └── remotepad/
│           │           └── app/
│           │               └── MainActivity.java
│           │
│           └── res/
│               ├── drawable/
│               │   └── mouse.jpg
│               │
│               └── values/
│                   └── styles.xml
│
├── gradle/
│   └── wrapper/
│
├── index.html
├── server.py
├── gradlew
├── gradlew.bat
├── settings.gradle
├── .gitignore
└── README.md
```

---

## 💻 Requirements

### PC

- Windows PC
- Python 3
- Wi-Fi connection
- Python packages:
  - `websockets`
  - `pyautogui`

### Android

- Android smartphone
- Android 6.0 or newer
- Wi-Fi connection

---

## 📦 PC Server Setup

### 1. Install Python

Install Python 3 on your Windows PC if it is not already installed.

Check Python:

```
python --version
```

### 2. Install Required Packages

Open Command Prompt and run:

```
pip install websockets pyautogui
```

### 3. Download the Project

Clone the repository:

```
git clone https://github.com/raju-prajapat/Phone-as-Mouse-Keyboard.git
```

Open the project folder:

```
cd Phone-as-Mouse-Keyboard
```

### 4. Start the Server

Run:

```
python server.py
```

Keep this terminal window open while using the application.

---

## 🌐 Find Your PC IP Address

The phone and PC must be connected to the same Wi-Fi network or hotspot.

On Windows:

1. Open Command Prompt
2. Run:

```
ipconfig
```

3. Find the Wi-Fi adapter
4. Look for **IPv4 Address**

Example:

```
192.168.1.25
```

Use this IP in the Android application.

---

## 📱 Using the Android App

1. **Install the APK** — Install the provided APK on your Android phone.
2. **Start the PC Server** — On the PC, run `python server.py`.
3. **Connect Phone and PC** — Make sure both devices are connected to the same network.
4. **Open the App** — Open Phone-as-Mouse-Keyboard.
5. **Enter PC IP** — Enter only the PC IP address, e.g. `192.168.1.25`.

   You do not need to enter `:5000` or `/ws` — the app automatically creates:

   ```
   ws://192.168.1.25:5000/ws
   ```

6. **Connect** — Tap **Connect**.

After a successful connection, the phone can be used as a mouse and keyboard.

---

## 🖱️ Mouse Controls

| Gesture | Action |
|---|---|
| One finger move | Move cursor |
| Single tap | Left click |
| Double tap | Double click |
| Two-finger tap | Right click |
| Two-finger swipe | Scroll |

Mouse sensitivity and scroll speed can be changed from Settings.

---

## ⌨️ Keyboard Controls

The keyboard provides commonly used PC keys such as:

`Esc` `Ctrl` `Alt` `Tab` `←` `↑` `↓` `→`

It also includes:

`Shift` `Backspace` `Enter` `Space` `Numbers` `Symbols` `Emoji`

Holding the Backspace key continuously deletes characters.

---

## 😀 Emoji Mode

Tap the emoji button on the keyboard to open the emoji panel. The emoji panel contains a large collection of emojis. Use the keyboard/emoji toggle to return to the normal keyboard.

---

## 📱 Building the Android APK

The Android application is built using Gradle.

From the project root:

```
./gradlew assembleDebug
```

For Windows:

```
gradlew.bat assembleDebug
```

After a successful build, the APK is generated at:

```
app/build/outputs/apk/debug/app-debug.apk
```

---

## 🔧 How the Android App Works

The Android application uses a WebView to load the local HTML interface.

Main activity:

```
app/src/main/java/com/remotepad/app/MainActivity.java
```

Web interface:

```
app/src/main/assets/index.html
```

The Java activity loads:

```
file:///android_asset/index.html
```

JavaScript handles the touchpad, keyboard, settings and WebSocket communication.

---

## 🐍 How the Python Server Works

`server.py` runs a WebSocket server on:

```
0.0.0.0:5000
```

The Android application connects using:

```
ws://PC-IP:5000/ws
```

The server receives commands from the phone and uses `pyautogui` to perform the corresponding action on the PC.

Examples of supported commands include:

- Mouse movement
- Left click
- Double click
- Right click
- Scrolling
- Key press
- Key release

---

## 🔒 Network & Security

This project is designed for use on a trusted local network.

The Android application communicates with the PC using WebSocket (`ws://`). It is intended for local Wi-Fi / hotspot communication.

**Do not** expose the Python server directly to the public internet without adding proper authentication and security controls.

---

## 🧪 Troubleshooting

### App says "Not connected"

Check:

1. PC server is running.
2. Phone and PC are on the same Wi-Fi/hotspot.
3. The correct PC IPv4 address is entered.
4. Windows Firewall is not blocking Python or port 5000.

### IP address changed

Your PC IP may change when you connect to a different network. Run `ipconfig` again and enter the new IPv4 address in the app. The server port remains `5000`.

### Server does not start

Make sure the required packages are installed:

```
pip install websockets pyautogui
```

Then run:

```
python server.py
```

---

## 🚀 Future Improvements

Possible future improvements include:

- Secure WebSocket connection
- Authentication / pairing
- Automatic PC discovery
- QR-code based connection
- Multiple device support
- Custom keyboard layouts
- Dark/light themes
- File transfer
- Media controls
- Power controls
- Clipboard synchronization

---

## 👨‍💻 Author

**Raju Prajapat**

Electronics & Communication Engineering Student.

**Connect**

- GitHub: https://github.com/raju-prajapat
- LinkedIn: https://www.linkedin.com/in/raju-prajapat-839b49394

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
