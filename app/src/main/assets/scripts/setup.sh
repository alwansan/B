#!/data/data/com.firefoxpc.app/files/usr/bin/bash
# ============================================================
# setup.sh — First Launch Setup
# يُشغَّل مرة واحدة فقط عند أول فتح للتطبيق
# ============================================================

SETUP_DONE="/data/data/com.firefoxpc.app/files/home/.setup_complete"
HOME_DIR="/data/data/com.firefoxpc.app/files/home"
PREFIX="/data/data/com.firefoxpc.app/files/usr"
SYSTEM_PARTS_DIR="$HOME_DIR/assets/system"
PROOT_ROOTFS="$PREFIX/var/lib/proot-distro/installed-rootfs"
LOG="$HOME_DIR/setup.log"

log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG"; }

# إذا الإعداد منجز، شغّل Firefox مباشرة
if [ -f "$SETUP_DONE" ]; then
  log "Setup already done. Launching..."
  exec "$HOME_DIR/scripts/start.sh"
  exit 0
fi

mkdir -p "$HOME_DIR/scripts" "$HOME_DIR/assets/system"
log "🚀 First launch setup starting..."

# --- 1. تثبيت الحزم المطلوبة ---
log "📦 Installing required packages..."

for pkg in x11-repo tur-repo; do
  pkg install "$pkg" -y 2>>"$LOG" || true
done

apt-get update -y 2>>"$LOG" || true

for pkg in termux-x11-nightly pulseaudio proot-distro wget git; do
  if ! command -v "$pkg" &>/dev/null && ! dpkg -s "$pkg" &>/dev/null 2>&1; then
    log "  Installing $pkg..."
    pkg install "$pkg" -y 2>>"$LOG" || \
    apt-get install -y "$pkg" 2>>"$LOG" || \
    log "  ⚠️ Could not install $pkg"
  else
    log "  ✅ $pkg already present"
  fi
done

# --- 2. استعادة نظام Ubuntu ---
log "🐧 Restoring Ubuntu system..."

if [ ! -d "$PROOT_ROOTFS/ubuntu" ]; then
  FULL_ARCHIVE="/tmp/ubuntu_system.tar.xz"

  # تجميع الأجزاء المقسّمة
  if ls "$SYSTEM_PARTS_DIR"/system.tar.xz.part* &>/dev/null 2>&1; then
    log "  Reassembling split archive..."
    cat "$SYSTEM_PARTS_DIR"/system.tar.xz.part* > "$FULL_ARCHIVE"
    log "  ✅ Archive ready ($(du -sh "$FULL_ARCHIVE" | cut -f1))"
  elif [ -f "$SYSTEM_PARTS_DIR/system.tar.xz" ]; then
    cp "$SYSTEM_PARTS_DIR/system.tar.xz" "$FULL_ARCHIVE"
  else
    log "  ❌ No system archive found!"
    exit 1
  fi

  log "  Restoring (this takes 2-4 minutes)..."
  proot-distro restore "$FULL_ARCHIVE" 2>>"$LOG" || {
    log "  Fallback: manual extraction..."
    mkdir -p "$PROOT_ROOTFS/ubuntu"
    tar -xJf "$FULL_ARCHIVE" -C "$PROOT_ROOTFS/ubuntu" 2>>"$LOG"
  }

  rm -f "$FULL_ARCHIVE"
  log "  ✅ Ubuntu restored!"
else
  log "  ✅ Ubuntu already installed"
fi

# --- 3. نسخ سكريبت التشغيل ---
cp "$HOME_DIR/assets/scripts/start.sh" "$HOME_DIR/scripts/start.sh"
chmod +x "$HOME_DIR/scripts/start.sh"

# --- اكتمل الإعداد ---
touch "$SETUP_DONE"
log "✅ Setup complete! Starting Firefox..."
exec "$HOME_DIR/scripts/start.sh"
