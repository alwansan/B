#!/system/bin/sh

# تحديد المسارات
APP_HOME="/data/data/com.example.b/files"
SYSTEM_FILE="$APP_HOME/system.tar.gz"
ROOTFS="$APP_HOME/rootfs"
PROOT="$APP_HOME/proot"
LOG="$APP_HOME/boot.log"

# دالة اللوج
log() {
    echo "$(date): $1" >> $LOG
}

# 1. التثبيت (إذا لم يتم من قبل)
if [ ! -f "$PROOT" ]; then
    log "📦 First run detected. Installing system..."
    
    # التأكد من وجود الملف
    if [ ! -f "$SYSTEM_FILE" ]; then
        log "❌ CRITICAL: System archive not found at $SYSTEM_FILE"
        exit 1
    fi
    
    # فك الضغط باستخدام tar (أسرع بـ 100 مرة من Java)
    cd "$APP_HOME"
    log "   -> Extracting tarball..."
    tar -xf system.tar.gz 2>> $LOG
    
    if [ $? -ne 0 ]; then
        log "❌ Extraction failed."
        exit 1
    fi
    
    # تصحيح الصلاحيات (مثل XoDos)
    log "   -> Setting permissions..."
    chmod 755 proot
    chmod 755 init.sh
    chmod -R 755 rootfs/bin rootfs/usr/bin rootfs/sbin
    
    # تنظيف لتقليل المساحة
    # rm system.tar.gz (اختياري، نتركه للنسخ الاحتياطي)
    log "✅ Installation complete."
fi

# 2. التشغيل
log "🚀 Starting Environment..."

# إعداد المتغيرات
export PROOT_TMP_DIR="$APP_HOME/tmp"
mkdir -p "$PROOT_TMP_DIR"

# تشغيل Proot
log "   -> Executing Proot..."
"$PROOT" -S "$ROOTFS" \
    -b /dev -b /proc -b /sys \
    -w /root \
    /usr/bin/env \
    HOME=/root \
    DISPLAY=:1 \
    /bin/sh /opt/init.sh >> $LOG 2>&1