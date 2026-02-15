#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export DEBIAN_FRONTEND=noninteractive

echo "⏳ Starting Linux Setup..." > /opt/status.log

# 1. إصلاح DNS (مهم جداً للإنترنت)
echo "nameserver 8.8.8.8" > /etc/resolv.conf

# 2. تحديث الحزم وتثبيت الأساسيات (X11 + VNC)
if [ ! -f "/usr/bin/Xvnc" ]; then
    echo "📦 Installing Desktop Environment (This takes time)..." >> /opt/status.log
    apt-get update
    # نثبت واجهة خفيفة (Fluxbox) وسيرفر VNC
    apt-get install -y tightvncserver fluxbox xterm libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libnss3 libnspr4 libasound2
fi

# 3. إعداد تشغيل Firefox
echo "🦊 Configuring Firefox..." >> /opt/status.log
export DISPLAY=:1
export HOME=/root

# تنظيف أي قفل سابق
rm -rf /tmp/.X1-lock
rm -rf /tmp/.X11-unix/X1

# تشغيل X Server في الخلفية
echo "🖥️ Starting X Server..." >> /opt/status.log
Xvnc :1 -geometry 1024x600 -depth 24 &
sleep 5

# تشغيل مدير النوافذ
fluxbox &

# تشغيل Firefox
echo "🔥 Launching Firefox..." >> /opt/status.log
/opt/firefox/firefox --no-remote --display=:1 &

# حلقة لا نهائية لمنع إغلاق السكربت
tail -f /opt/status.log