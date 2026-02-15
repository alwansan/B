#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export DEBIAN_FRONTEND=noninteractive
export HOME=/root
export USER=root

LOG=/opt/status.log
echo "🚀 Starting Linux Boot..." > $LOG

# 1. إصلاح الشبكة
echo "nameserver 8.8.8.8" > /etc/resolv.conf

# 2. تثبيت الحزم (فقط إذا لم تكن موجودة)
if [ ! -f "/usr/bin/Xvnc" ]; then
    echo "📦 Installing Desktop Environment (This may take 10 mins)..." >> $LOG
    apt-get update
    apt-get install -y tightvncserver fluxbox xterm libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libnss3 libnspr4 libasound2 python3 python3-numpy net-tools
fi

# 3. إعداد noVNC (إذا لم يكن مثبتاً)
if [ ! -d "/opt/novnc" ]; then
    echo "📦 Extracting noVNC..." >> $LOG
    mkdir -p /opt/novnc
    tar -xf /opt/novnc.tar.gz -C /opt/novnc --strip-components=1
fi

# 4. تنظيف الأقفال القديمة
rm -rf /tmp/.X1-lock /tmp/.X11-unix/X1

# 5. تشغيل الخدمات
echo "🖥️ Starting X Server (VNC)..." >> $LOG
# تشغيل VNC على الشاشة :1
Xvnc :1 -geometry 1280x720 -depth 24 -rfbport 5901 -SecurityTypes None &
sleep 5

echo "🕸️ Starting noVNC Web Bridge..." >> $LOG
# تحويل VNC إلى HTML5 على المنفذ 6080
/opt/novnc/utils/novnc_proxy --vnc localhost:5901 --listen 6080 &
sleep 2

echo "🪟 Starting Window Manager..." >> $LOG
export DISPLAY=:1
fluxbox &

echo "🔥 Launching Firefox..." >> $LOG
# تشغيل فايرفوكس بملف تعريف جديد لتجنب الأخطاء
/opt/firefox/firefox --no-remote --display=:1 --profile /root/.mozilla/firefox/newprofile &

echo "✅ SYSTEM READY! Open http://localhost:6080/vnc.html" >> $LOG

# إبقاء الحاوية تعمل
tail -f $LOG