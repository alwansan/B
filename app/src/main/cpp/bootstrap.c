#include <jni.h>
#include <string.h>
#include <android/log.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <stdio.h>
#include <errno.h>

#define TAG "B_Native"
#define LOGD(...) __android_log_print(ANDROID_LOG_DEBUG, TAG, __VA_ARGS__)
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, TAG, __VA_ARGS__)

JNIEXPORT jint JNICALL
Java_com_example_b_LauncherActivity_startLinux(JNIEnv *env, jobject thiz, jstring app_path_j) {
    const char *app_path = (*env)->GetStringUTFChars(env, app_path_j, 0);
    
    LOGD("Initializing Linux Environment...");

    char proot_bin[512];
    char rootfs[512];
    char firefox_dir[512];
    char cmd[8192]; // حجم كبير للأوامر الطويلة

    sprintf(proot_bin, "%s/proot", app_path);
    sprintf(rootfs, "%s/rootfs", app_path);
    sprintf(firefox_dir, "%s/firefox", app_path);

    // 1. منح صلاحيات التنفيذ لـ Proot
    if (chmod(proot_bin, 0755) != 0) {
        LOGE("Failed to chmod proot: %s", strerror(errno));
    }

    // 2. إعداد متغيرات البيئة (Environment Variables)
    // هذه المتغيرات ضرورية لكي يعمل Linux بشكل صحيح
    setenv("PROOT_TMP_DIR", app_path, 1);
    setenv("HOME", "/root", 1);
    setenv("PATH", "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", 1);
    setenv("TERM", "xterm-256color", 1);
    
    // 3. بناء أمر التشغيل
    // proot -S rootfs -b /dev -b /proc -w /root /bin/bash -c "command"
    
    // للتجربة في المرحلة 3: سنقوم بطباعة إصدار النظام
    sprintf(cmd, 
        "%s "
        "-S %s "                // RootFS path
        "-b /dev "              // Bind /dev
        "-b /proc "             // Bind /proc
        "-b %s:/opt/firefox "   // Bind Firefox directory inside Linux
        "-w /root "             // Workdir
        "/usr/bin/env bash -c 'echo \"🔥 HELLO FROM LINUX BUBBLE! 🔥\"; uname -a; ls -la /opt/firefox'", 
        proot_bin, rootfs, firefox_dir
    );

    LOGD("Executing Command: %s", cmd);
    
    int ret = system(cmd);
    
    if (ret != 0) {
        LOGE("Linux command failed with code: %d", ret);
    } else {
        LOGD("Linux command executed successfully!");
    }

    (*env)->ReleaseStringUTFChars(env, app_path_j, app_path);
    return ret;
}