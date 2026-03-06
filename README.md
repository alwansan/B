# Firefox PC for Android 🦊

Full Firefox Desktop (Linux ARM64) running inside a Termux/PRoot environment as an Android APK.

---

## 📋 What This Is

This APK embeds a complete Debian Linux system with Firefox Desktop (ARM64), displayed via Termux X11. It gives you a real desktop browser experience on Android.

**Features:**
- Firefox Desktop running fullscreen on Android
- Full DevTools support
- Desktop extensions supported
- No mobile browser limitations
- Works offline after installation

---

## 🏗️ Build Steps (Step by Step)

### Phase 1: Prepare Debian System (on your Android phone with Termux)

#### 1.1 — Install proot-distro on your phone
```bash
pkg install proot-distro -y
proot-distro install debian
proot-distro login debian
```

#### 1.2 — Inside Debian, run the preparation script
```bash
# Copy prepare_debian.sh into the distro
cp /storage/emulated/0/Download/Games/py/B/FirefoxPC/scripts/prepare_debian.sh /root/
chmod +x /root/prepare_debian.sh
bash /root/prepare_debian.sh
```

This script will:
- Install XFCE4 (minimal)
- Download Firefox Desktop ARM64 from Mozilla
- Install Firefox to `/opt/firefox`
- Disable auto-updates
- Strip all unnecessary packages
- Clean up to minimize size

#### 1.3 — Export the Debian system
```bash
# Exit proot first
exit

# Export (creates system.tar.xz)
proot-distro backup debian --output /storage/emulated/0/Download/Games/py/B/system.tar.xz

# Check size
ls -lh /storage/emulated/0/Download/Games/py/B/system.tar.xz
```

---

### Phase 2: Prepare APK Project

#### 2.1 — Clone this project
```bash
cd /storage/emulated/0/Download/Games/py/B/
git clone https://github.com/YOUR_USERNAME/FirefoxPC
cd FirefoxPC
```

#### 2.2 — Add your icon
```bash
cp /path/to/your/icon.png /storage/emulated/0/Download/Games/py/B/icon.png
```

#### 2.3 — Run p.py to split system and push to GitHub
```bash
cd /storage/emulated/0/Download/Games/py/B/
# Edit p.py and set your REPO_URL first!
nano scripts/p.py

python3 scripts/p.py
```

This will:
1. Split `system.tar.xz` into 50MB parts → `app/src/main/assets/system/`
2. Update colors, strings, styles
3. Copy icon to all densities
4. Push everything to GitHub

---

### Phase 3: Build APK on GitHub Actions

1. Go to your repo: `https://github.com/YOUR_USERNAME/FirefoxPC`
2. Click **Actions** tab
3. Click **Build Firefox PC APK**
4. Click **Run workflow**
5. Wait ~10-15 minutes
6. Download APK from **Releases** or **Artifacts**

---

## 📱 Installation on Phone

1. Download the APK from GitHub Actions
2. Enable **Install from Unknown Sources** in Android Settings
3. Install the APK
4. Also install **Termux X11** from F-Droid: `https://f-droid.org/packages/com.termux.x11/`
5. Open Firefox PC
6. **First launch:** wait 2-3 minutes for setup
7. Firefox Desktop appears fullscreen ✅

---

## 🗂️ Project Structure

```
FirefoxPC/
├── app/
│   └── src/main/
│       ├── AndroidManifest.xml        # App manifest
│       ├── java/com/firefoxpc/app/
│       │   └── MainActivity.java      # Main app code + service
│       ├── res/
│       │   ├── layout/activity_main.xml   # Loading screen UI
│       │   ├── values/colors.xml          # Color theme
│       │   ├── values/strings.xml         # App strings
│       │   ├── values/styles.xml          # App theme
│       │   └── mipmap-*/ic_launcher.png   # App icon
│       └── assets/
│           ├── scripts/
│           │   ├── first_launch.sh    # First-run setup
│           │   └── start_firefox.sh  # Firefox launcher
│           └── system/
│               ├── system.tar.xz.partaa  # Debian system (split)
│               ├── system.tar.xz.partab  # ...
│               └── manifest.txt           # Parts list + checksum
├── scripts/
│   ├── prepare_debian.sh  # Prepare Debian before export
│   └── p.py               # Main automation script
├── .github/workflows/
│   └── build.yml          # GitHub Actions CI/CD
├── build.gradle
├── settings.gradle
└── gradle.properties
```

---

## 🔧 How It Works

```
Android App Opens
      │
      ▼
MainActivity.java
      │
      ├─► First Launch? ──Yes──► Extract assets from APK
      │                          Reassemble system.tar.xz parts
      │                          proot-distro restore debian
      │                          Configure PulseAudio
      │
      └─► start_firefox.sh
              │
              ├─► Start PulseAudio
              ├─► Start termux-x11 :0
              ├─► Launch Termux X11 Activity (fullscreen)
              └─► proot-distro login debian
                        └─► xfwm4 (minimal WM)
                        └─► /opt/firefox/firefox --kiosk
```

---

## 🔄 Updating Firefox

To update Firefox version:
1. Re-run `prepare_debian.sh` inside Debian with new Firefox version
2. Re-export: `proot-distro backup debian --output system.tar.xz`
3. Run `python3 scripts/p.py` again
4. Rebuild APK on GitHub Actions

---

## ⚙️ Customization

- **Change package name:** Edit `AndroidManifest.xml` and `build.gradle` (change `com.firefoxpc.app`)
- **Change app name:** Edit `app/src/main/res/values/strings.xml`
- **Change colors:** Edit `app/src/main/res/values/colors.xml`
- **Firefox preferences:** Edit `prepare_debian.sh` → user.js section

---

## ❓ Troubleshooting

| Issue | Fix |
|-------|-----|
| Black screen after launch | Wait 30s, Termux X11 is starting |
| "Setup failed" | Check internet connection for fallback downloads |
| APK too large for GitHub | system.tar.xz is split into 50MB parts automatically |
| Firefox crashes | Check `/tmp/firefox.log` inside Debian |
| No sound | PulseAudio starts automatically; try reopening app |

---

## 📝 Notes

- APK size will be **large** (depends on Debian system size, typically 1-3GB)
- GitHub Actions can handle large repos with **Git LFS** if needed
- The app uses package ID `com.firefoxpc.app` — different from official Termux
- Tested on ARM64 Android devices (Snapdragon/MediaTek)
