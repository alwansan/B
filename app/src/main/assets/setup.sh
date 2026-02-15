#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export HOME=/root
export USER=root

# لوج للمتابعة
LOG=/opt/status.html
echo "<html><body style='background:black;color:green;font-family:monospace;'>" > $LOG
echo "<h3>🚀 Linux Boot Started...</h3><pre>" >> $LOG

# 1. إصلاح الشبكة
echo "nameserver 8.8.8.8" > /etc/resolv.conf

# 2. محاولة التثبيت (مع تجاهل الأخطاء لكي لا يتوقف)
if [ ! -f "/usr/bin/Xvnc" ]; then
    echo "📦 Installing Packages (Internet Needed)..." >> $LOG
    apt-get update >> $LOG 2>&1
    apt-get install -y tightvncserver fluxbox xterm libx11-6 libnss3 libasound2 python3 >> $LOG 2>&1
fi

# 3. تشغيل VNC (الشاشة)
echo "🖥️ Starting Xvnc..." >> $LOG
rm -rf /tmp/.X1-lock
Xvnc :1 -geometry 1280x720 -depth 24 -rfbport 5901 -SecurityTypes None >> $LOG 2>&1 &
sleep 5

# 4. تشغيل noVNC (الجسر)
echo "🕸️ Starting noVNC..." >> $LOG
/opt/novnc/utils/novnc_proxy --vnc localhost:5901 --listen 6080 >> $LOG 2>&1 &

# 5. تشغيل Firefox
echo "🔥 Launching Firefox..." >> $LOG
export DISPLAY=:1
fluxbox &
/opt/firefox/firefox --no-remote --display=:1 --profile /root/.mozilla/firefox/newprofile >> $LOG 2>&1 &

echo "</pre><h2 style='color:white;'>✅ READY! Connecting...</h2>" >> $LOG
# حلقة لا نهائية
tail -f /dev/null