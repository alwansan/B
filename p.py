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
SYSTEM_SRC   = os.path.join(BASE_DIR, "system.tar.xz")
SYSTEM_DEST  = os.path.join(ASSETS_DIR, "system")
ICON_SRC     = os.path.join(BASE_DIR, "icon.png")
SPLIT_MB     = 45       # أصغر من 50MB لضمان قبول GitHub (حد 100MB لكل ملف)
REPO_URL     = "https://github.com/alwansan/B"
# ───────────────────────────────────────────────────────────

def sh(cmd, check=True):
    print(f"  ▶ {cmd}")
    result = subprocess.run(cmd, shell=True, check=check, text=True)
    return result

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
        print(f"  ⚠️  لم يُعثر على system.tar.xz")
        print(f"  → شغّل: proot-distro backup ubuntu --output {SYSTEM_SRC}")
        return False

    os.makedirs(SYSTEM_DEST, exist_ok=True)

    # حذف الأجزاء القديمة
    for f in os.listdir(SYSTEM_DEST):
        if "system.tar.xz" in f or f == "manifest.txt":
            os.remove(os.path.join(SYSTEM_DEST, f))
            print(f"  🗑 Removed old: {f}")

    size_mb = os.path.getsize(SYSTEM_SRC) / 1024 / 1024
    print(f"  📏 حجم الأرشيف: {size_mb:.0f} MB")

    # تقسيم — بدون LFS، مباشرة كملفات عادية
    sh(f'split -b {SPLIT_MB}M "{SYSTEM_SRC}" "{SYSTEM_DEST}/system.tar.xz.part"')

    parts = sorted(f for f in os.listdir(SYSTEM_DEST)
                   if f.startswith("system.tar.xz.part"))

    # تحقق أن كل جزء < 100MB (حد GitHub)
    for p in parts:
        size = os.path.getsize(os.path.join(SYSTEM_DEST, p)) / 1024 / 1024
        if size > 99:
            print(f"  ❌ {p} حجمه {size:.0f}MB — يتجاوز حد GitHub 100MB!")
            print("  → قلّل SPLIT_MB إلى 40 وأعد التشغيل")
            return False
        print(f"  ✅ {p} ({size:.0f}MB)")

    print(f"  ✅ {len(parts)} أجزاء × {SPLIT_MB}MB")

    # كتابة ملف manifest
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

# ── 3. إزالة LFS من الريبو إذا كان مُفعّلاً ───────────────
def remove_lfs():
    print("\n🔧 Step 3: Disable Git LFS (fix GitHub error)")
    os.chdir(PROJECT_DIR)
    sh("git lfs uninstall", check=False)

    # إعادة كتابة .gitattributes بدون LFS
    gitattr = os.path.join(PROJECT_DIR, ".gitattributes")
    with open(gitattr, "w") as f:
        f.write("# No LFS — all files committed directly\n")
        f.write("*.tar.xz -text\n")
        f.write("*.part*  -text\n")
    print("  ✅ .gitattributes updated (no LFS)")

    # إزالة تتبع LFS من الملفات
    sh("git rm -r --cached . 2>/dev/null || true", check=False)

# ── 4. Git push ─────────────────────────────────────────────
def git_push():
    print("\n🚀 Step 4: Push to GitHub")
    os.chdir(PROJECT_DIR)

    if not os.path.exists(".git"):
        sh("git init")
        sh(f"git remote add origin {REPO_URL}")
    else:
        # تأكد أن remote صحيح
        sh(f"git remote set-url origin {REPO_URL}", check=False)

    # تأكد أن LFS غير مُفعّل
    sh("git lfs uninstall 2>/dev/null || true", check=False)

    sh("git add -A")
    sh('git commit -m "fix: remove LFS, embed system parts directly"', check=False)
    sh("git push -u -f origin main")
    print(f"\n  🔗 تابع البناء: {REPO_URL}/actions")

# ── Main ────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  Firefox PC — APK Builder (LFS-free)")
    print("=" * 55)

    if not os.path.isdir(PROJECT_DIR):
        print(f"❌ مجلد المشروع غير موجود: {PROJECT_DIR}")
        sys.exit(1)

    split_system()
    copy_icon()
    remove_lfs()
    git_push()

    print("\n" + "=" * 55)
    print("✅ تم! سيتم بناء APK على GitHub Actions.")
    print("=" * 55)
