#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export HOME=/root
export USER=root
export TMPDIR=/tmp

# ملف الحالة
LOG=/opt/status.html

# دالة تحديث الحالة
update_status() {
    echo "<html><body style='background-color:black; color:#00ff00; font-family:monospace; padding:20px;'>" > $LOG
    echo "<h2>🚀 B Browser System Boot</h2>" >> $LOG
    echo "<p><b>STATUS:</b> $1</p>" >> $LOG
    echo "<div style='border:1px solid #333; padding:10px; color:#ccc;'><pre>" >> $LOG
    tail -n 10 /opt/boot.log >> $LOG
    echo "</pre></div>" >> $LOG
    echo "<script>setTimeout(function(){window.location.reload();}, 2000);</script>" >> $LOG
    echo "</body></html>" >> $LOG
}

echo "Booting..." > /opt/boot.log
update_status "Initializing Kernel..."

# 1. إصلاح DNS
echo "nameserver 8.8.8.8" > /etc/resolv.conf

# 2. التثبيت (إذا لزم الأمر)
if [ ! -f "/usr/bin/Xvnc" ]; then
    update_status "Installing Desktop Environment (Might take time)..."
    echo "Installing packages..." >> /opt/boot.log
    apt-get update -y >> /opt/boot.log 2>&1
    apt-get install -y tightvncserver fluxbox xterm libx11-6 libnss3 libasound2 python3 net-tools procps >> /opt/boot.log 2>&1
fi

# 3. إعداد noVNC
if [ ! -d "/opt/novnc" ]; then
    update_status "Extracting noVNC..."
    mkdir -p /opt/novnc
    tar -xf /opt/novnc.tar.gz -C /opt/novnc --strip-components=1 >> /opt/boot.log 2>&1
fi

# 4. تشغيل الخدمات
update_status "Starting X11 Display Server..."
rm -rf /tmp/.X1-lock /tmp/.X11-unix
Xvnc :1 -geometry 1280x720 -depth 24 -rfbport 5901 -SecurityTypes None >> /opt/boot.log 2>&1 &
sleep 3

update_status "Starting Web Bridge..."
/opt/novnc/utils/novnc_proxy --vnc localhost:5901 --listen 6080 >> /opt/boot.log 2>&1 &
sleep 2

update_status "Launching Firefox..."
export DISPLAY=:1
fluxbox >> /opt/boot.log 2>&1 &
/opt/firefox/firefox --no-remote --display=:1 --profile /root/.mozilla/firefox/newprofile >> /opt/boot.log 2>&1 &

# النجاح
echo "<html><body style='background-color:black; display:flex; justify-content:center; align-items:center; height:100vh;'>" > $LOG
echo "<h1 style='color:white;'>✅ SYSTEM READY</h1>" >> $LOG
echo "<script>window.location.href='http://localhost:6080/vnc.html?autoconnect=true&reconnect=true';</script>" >> $LOG
echo "</body></html>" >> $LOG

# منع الإغلاق
tail -f /opt/boot.log