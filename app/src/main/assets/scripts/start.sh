#!/data/data/com.firefoxpc.app/files/usr/bin/bash
# ============================================================
# start.sh — Firefox PC Startup Script
# نسخة محسّنة من سكريبت التشغيل الأصلي
# ============================================================

# --- 1. تنظيف العمليات القديمة ---
pkill -f "termux.x11"   2>/dev/null
pkill -f "pulseaudio"   2>/dev/null
pkill -f "xfce4-session" 2>/dev/null
sleep 1

# --- 2. تشغيل PulseAudio ---
pulseaudio --start \
  --load="module-native-protocol-tcp auth-ip-acl=127.0.0.1 auth-anonymous=1" \
  --exit-idle-time=-1 \
  --daemon 2>/dev/null

# --- 3. إعداد X11 ---
export XDG_RUNTIME_DIR="${TMPDIR:-/tmp}"
export DISPLAY=:0

# --- 4. تشغيل Termux-X11 ---
termux-x11 :0 -xstartup '' >/dev/null 2>&1 &

# انتظار ذكي حتى يكون X11 جاهزاً (بدل sleep ثابت)
WAIT=0
while [ ! -S "/tmp/.X11-unix/X0" ] && [ $WAIT -lt 12 ]; do
  sleep 1
  WAIT=$((WAIT + 1))
done

# --- 5. فتح نافذة Termux-X11 ---
am start --user 0 \
  -n com.termux.x11/com.termux.x11.MainActivity \
  > /dev/null 2>&1
sleep 1

# --- 6. الدخول إلى Ubuntu وتشغيل XFCE + Firefox ---
proot-distro login ubuntu --shared-tmp -- /bin/bash -c '

  export DISPLAY=:0
  export PULSE_SERVER=127.0.0.1
  export XDG_RUNTIME_DIR="${TMPDIR:-/tmp}"
  export HOME=/root
  export USER=root
  export NO_AT_BRIDGE=1

  # إصلاح DBus (يمنع التحذيرات الكثيرة)
  eval $(dbus-launch --sh-syntax 2>/dev/null) || true

  # إصلاح مجلدات /tmp
  mkdir -p /tmp/.ICE-unix /tmp/.X11-unix
  chmod 1777 /tmp/.ICE-unix /tmp/.X11-unix 2>/dev/null || true

  # حذف ملفات القفل القديمة التي تسبب الشاشة السوداء
  rm -f /tmp/.xfsm-ICE-* 2>/dev/null
  rm -f /root/.cache/xfce4/xfwm4/xfwm4-crashlog 2>/dev/null

  # تعطيل system bus المكسور داخل proot
  export DBUS_SYSTEM_BUS_ADDRESS="unix:path=/dev/null"

  # تشغيل XFCE
  env DISPLAY=:0 startxfce4 &
  XFCE_PID=$!

  # انتظار XFCE ثم فتح Firefox تلقائياً
  sleep 6
  MOZ_FAKE_NO_SANDBOX=1 /opt/firefox/firefox \
    --display=:0 \
    --kiosk \
    --no-remote \
    2>/tmp/firefox.log &

  wait $XFCE_PID
'

exit 0
