#!/bin/bash
# setup.sh — First-time Ubuntu setup

LOGF="/storage/emulated/0/Download/FirefoxPC_Logs/setup.log"
mkdir -p "$(dirname "$LOGF")" 2>/dev/null || LOGF="$HOME/setup.log"
SETUP_DONE="$HOME/.setup_complete"

L() { echo "[$(date +%T)] $1" | tee -a "$LOGF" 2>/dev/null; }

L "====== setup.sh start ======"
L "HOME=$HOME  PREFIX=$PREFIX"
L "bash=$(which bash 2>/dev/null || echo MISSING)"
L "proot-distro=$(which proot-distro 2>/dev/null || echo MISSING)"
L "Already done file: $([ -f $SETUP_DONE ] && echo YES || echo NO)"

[ -f "$SETUP_DONE" ] && { L "Already done. Starting..."; exec "$HOME/scripts/start.sh"; }

# تثبيت الحزم المطلوبة
L "--- Updating packages ---"
pkg update -y >> "$LOGF" 2>&1 && L "pkg update OK" || L "pkg update failed (non-fatal)"

for pkg in x11-repo tur-repo; do
    pkg install -y "$pkg" >> "$LOGF" 2>&1
    L "  $pkg: installed"
done

pkg update -y >> "$LOGF" 2>&1

for pkg in termux-x11-nightly pulseaudio proot-distro; do
    if command -v "$pkg" > /dev/null 2>&1; then
        L "  ✓ $pkg (already installed)"
    else
        L "  Installing: $pkg ..."
        pkg install -y "$pkg" >> "$LOGF" 2>&1
        L "  $pkg exit=$?"
    fi
done

# تجميع أجزاء النظام
L "--- Assembling Ubuntu archive ---"
SYS_DIR="$HOME/assets/system"
FULL="$HOME/ubuntu_full.tar.xz"

if [ -f "$FULL" ]; then
    L "Archive already assembled: $(du -sh $FULL | cut -f1)"
elif ls "$SYS_DIR"/system.tar.xz.part* > /dev/null 2>&1; then
    COUNT=$(ls "$SYS_DIR"/system.tar.xz.part* | wc -l)
    L "Joining $COUNT parts..."
    cat "$SYS_DIR"/system.tar.xz.part* > "$FULL"
    L "Joined: $(du -sh $FULL | cut -f1)"
elif [ -f "$SYS_DIR/system.tar.xz" ]; then
    ln -sf "$SYS_DIR/system.tar.xz" "$FULL"
    L "Using single archive"
else
    L "ERROR: No system archive found in $SYS_DIR"
    ls -la "$SYS_DIR" >> "$LOGF" 2>&1
    exit 1
fi

# استعادة Ubuntu
L "--- Restoring Ubuntu ---"
ROOTFS="$PREFIX/var/lib/proot-distro/installed-rootfs"
L "ROOTFS: $ROOTFS"
L "Ubuntu exists: $([ -d $ROOTFS/ubuntu ] && echo YES || echo NO)"

if [ ! -d "$ROOTFS/ubuntu" ]; then
    L "Running proot-distro restore..."
    proot-distro restore "$FULL" >> "$LOGF" 2>&1
    RC=$?
    L "proot-distro restore exit=$RC"

    if [ $RC -ne 0 ] || [ ! -d "$ROOTFS/ubuntu" ]; then
        L "Fallback: manual tar extract..."
        mkdir -p "$ROOTFS/ubuntu"
        tar -xJf "$FULL" -C "$ROOTFS/ubuntu" >> "$LOGF" 2>&1
        L "tar exit=$?"
    fi
else
    L "Ubuntu already installed: $(du -sh $ROOTFS/ubuntu | cut -f1)"
fi

[ -d "$ROOTFS/ubuntu" ] && L "✅ Ubuntu OK" || { L "❌ Ubuntu MISSING!"; exit 1; }

# حذف الأرشيف لتوفير المساحة
rm -f "$FULL" 2>/dev/null

touch "$SETUP_DONE"
L "====== setup.sh DONE ======"
exec "$HOME/scripts/start.sh"
