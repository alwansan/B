#include <jni.h>
#include <string.h>
#include <android/log.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <stdio.h>

#define TAG "B_Native"
#define LOGD(...) __android_log_print(ANDROID_LOG_DEBUG, TAG, __VA_ARGS__)

JNIEXPORT jint JNICALL
Java_com_example_b_LauncherActivity_startLinux(JNIEnv *env, jobject thiz, jstring app_path_j) {
    const char *app_path = (*env)->GetStringUTFChars(env, app_path_j, 0);
    
    char proot_bin[512];
    char rootfs[512];
    char setup_script[512];
    char cmd[4096];

    sprintf(proot_bin, "%s/proot", app_path);
    sprintf(rootfs, "%s/rootfs", app_path);
    sprintf(setup_script, "%s/setup.sh", app_path);

    chmod(proot_bin, 0755);
    chmod(setup_script, 0755);

    // الأمر السحري: تشغيل Proot مع ربط الشبكة DNS
    // -b /dev -b /proc -b /sys : روابط النظام
    // -0 : تشغيل كـ Root
    sprintf(cmd, 
        "%s -S %s "
        "-b /dev -b /proc -b /sys "
        "-b %s/firefox:/opt/firefox "
        "-b %s:/opt/setup.sh "
        "-w /root "
        "/bin/bash /opt/setup.sh", 
        proot_bin, rootfs, app_path, setup_script
    );

    LOGD("Executing Linux Setup: %s", cmd);
    int ret = system(cmd);
    
    (*env)->ReleaseStringUTFChars(env, app_path_j, app_path);
    return ret;
}