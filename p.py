#!/usr/bin/env python3
"""
p.py — Firefox PC Builder
المسار: /storage/emulated/0/Download/Games/py/B/p.py
الاستخدام: python3 p.py
"""

import os, sys, subprocess, shutil, hashlib

# ── إعدادات ────────────────────────────────────────────────
BASE_DIR     = "/storage/emulated/0/Download/Games/py/B"
PROJECT_DIR  = os.path.join(BASE_DIR, "FirefoxPC")
ASSETS_DIR   = os.path.join(PROJECT_DIR, "app/src/main/assets")
RES_DIR      = os.path.join(PROJECT_DIR, "app/src/main/res")
SYSTEM_SRC   = os.path.join(BASE_DIR, "system.tar.xz")       # الملف المُصدَّر
SYSTEM_DEST  = os.path.join(ASSETS_DIR, "system")
ICON_SRC     = os.path.join(BASE_DIR, "icon.png")
SPLIT_MB     = 50
REPO_URL     = "https://github.com/alwansan/B"   # ← غيّر هذا
# ───────────────────────────────────────────────────────────

def sh(cmd, check=True):
    print(f"  ▶ {cmd}")
    return subprocess.run(cmd, shell=True, check=check, text=True,
                          capture_output=False)

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")
    print(f"  ✅ {os.path.basename(path)}")

def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

# ── 1. تقسيم system.tar.xz ─────────────────────────────────
def split_system():
    print("\n📦 Step 1: Split system archive")
    if not os.path.exists(SYSTEM_SRC):
        print(f"  ⚠️  لم يُعثر على {SYSTEM_SRC}")
        print("  → شغّل أولاً: proot-distro backup ubuntu --output system.tar.xz")
        return False

    # حذف الأجزاء القديمة
    os.makedirs(SYSTEM_DEST, exist_ok=True)
    for f in os.listdir(SYSTEM_DEST):
        if "system.tar.xz" in f or f == "manifest.txt":
            os.remove(os.path.join(SYSTEM_DEST, f))

    size_mb = os.path.getsize(SYSTEM_SRC) / 1024 / 1024
    print(f"  حجم الأرشيف: {size_mb:.0f} MB")

    sh(f'split -b {SPLIT_MB}M "{SYSTEM_SRC}" "{SYSTEM_DEST}/system.tar.xz.part"')

    parts = sorted(f for f in os.listdir(SYSTEM_DEST)
                   if f.startswith("system.tar.xz.part"))
    print(f"  ✅ {len(parts)} أجزاء × {SPLIT_MB}MB")

    with open(os.path.join(SYSTEM_DEST, "manifest.txt"), "w") as mf:
        mf.write(f"parts={len(parts)}\n")
        mf.write(f"md5={md5(SYSTEM_SRC)}\n")
        for p in parts:
            mf.write(p + "\n")
    return True

# ── 2. نسخ الأيقونة ────────────────────────────────────────
def copy_icon():
    print("\n🖼️  Step 2: Copy icon")
    if not os.path.exists(ICON_SRC):
        print(f"  ⚠️  icon.png غير موجود في {BASE_DIR}")
        return
    for density in ["mipmap-hdpi","mipmap-xhdpi","mipmap-xxhdpi","mipmap-xxxhdpi"]:
        dest = os.path.join(RES_DIR, density)
        os.makedirs(dest, exist_ok=True)
        shutil.copy2(ICON_SRC, os.path.join(dest, "ic_launcher.png"))
        print(f"  ✅ {density}")

# ── 3. Git push ─────────────────────────────────────────────
def git_push():
    print("\n🚀 Step 3: Push to GitHub")
    os.chdir(PROJECT_DIR)
    if not os.path.exists(".git"):
        sh("git init")
        sh(f"git remote add origin {REPO_URL}")
    # تفعيل LFS للملفات الكبيرة
    sh("git lfs install", check=False)
    sh("git lfs track '*.part*'", check=False)
    sh("git lfs track '*.tar.xz'", check=False)

    sh("git add .")
    sh('git commit -m "build: update Firefox PC"', check=False)
    sh("git push -u -f origin main")
    print(f"\n  🔗 تابع البناء: {REPO_URL}/actions")

# ── Main ────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  Firefox PC — APK Builder")
    print("=" * 50)

    if not os.path.isdir(PROJECT_DIR):
        print(f"❌ مجلد المشروع غير موجود: {PROJECT_DIR}")
        sys.exit(1)

    split_system()
    copy_icon()
    git_push()

    print("\n" + "=" * 50)
    print("✅ تم! سيتم بناء APK على GitHub Actions.")
    print("=" * 50)
