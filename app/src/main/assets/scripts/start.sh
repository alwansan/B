#!/bin/bash
# start.sh — Launch X11 + Firefox

LOGF="/storage/emulated/0/Download/FirefoxPC_Logs/start.log"
mkdir -p "$(dirname "$LOGF")" 2>/dev/null || LOGF="$HOME/start.log"
L() { echo "[$(date +%T)] $1" | tee -a "$LOGF" 2>/dev/null; }

L "====== start.sh ======"
L "PREFIX=$PREFIX  HOME=$HOME"

# أوقف العمليات القديمة
pkill -f "termux.x11" 2>/dev/null; sleep 0.3
pkill -f "pulseaudio"  2>/dev/null; sleep 0.3

# PulseAudio
L "Starting PulseAudio..."
pulseaudio --start \
    --load="module-native-protocol-tcp auth-ip-acl=127.0.0.1 auth-anonymous=1" \
    --exit-idle-time=-1 >> "$LOGF" 2>&1
L "PulseAudio: $?"

# X11
export XDG_RUNTIME_DIR="${TMPDIR:-$PREFIX/tmp}"
export DISPLAY=:0
L "Starting termux-x11..."
termux-x11 :0 > "$LOGF.x11" 2>&1 &
X11_PID=$!
L "termux-x11 PID=$X11_PID"

# انتظر X11
for i in $(seq 1 20); do
    [ -S /tmp/.X11-unix/X0 ] && break; sleep 0.5
done
L "X11 socket: $([ -S /tmp/.X11-unix/X0 ] && echo READY || echo TIMEOUT)"

# فتح X11 activity
am start --user 0 -n com.termux.x11/com.termux.x11.MainActivity 2>/dev/null
L "X11 activity started: $?"
sleep 1

# Ubuntu session
L "Starting Ubuntu proot..."
proot-distro login ubuntu --shared-tmp -- /bin/bash -c '
    ULOG="/storage/emulated/0/Download/FirefoxPC_Logs/ubuntu.log"
    mkdir -p "$(dirname $ULOG)" 2>/dev/null || ULOG="/tmp/ubuntu.log"
    UL() { echo "[$(date +%T)] $1" | tee -a "$ULOG"; }
    UL "=== Ubuntu session ==="

    export DISPLAY=:0
    export PULSE_SERVER=127.0.0.1
    export HOME=/root
    export NO_AT_BRIDGE=1
    export MESA_GL_VERSION_OVERRIDE=4.0
    export DBUS_SYSTEM_BUS_ADDRESS="unix:path=/dev/null"
    export XDG_RUNTIME_DIR=/tmp

    mkdir -p /tmp/.ICE-unix /tmp/.X11-unix
    chmod 1777 /tmp/.ICE-unix /tmp/.X11-unix 2>/dev/null

    eval $(dbus-launch --sh-syntax 2>/dev/null) || true
    UL "XFCE4 starting..."
    startxfce4 >> "$ULOG" 2>&1 &
    XFCE_PID=$!
    UL "XFCE4 PID=$XFCE_PID"
    sleep 4

    UL "Firefox starting..."
    MOZ_FAKE_NO_SANDBOX=1 /opt/firefox/firefox --display=:0 \
        --kiosk --no-remote >> "$ULOG" 2>&1 &
    UL "Firefox PID=$!"

    wait $XFCE_PID
    UL "Session ended"
'
L "proot exit=$?"
