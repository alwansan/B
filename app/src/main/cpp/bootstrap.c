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
    char novnc_tar[512];
    char cmd[4096];

    sprintf(proot_bin, "%s/proot", app_path);
    sprintf(rootfs, "%s/rootfs", app_path);
    sprintf(setup_script, "%s/setup.sh", app_path);
    sprintf(novnc_tar, "%s/novnc.tar.gz", app_path);

    chmod(proot_bin, 0755);
    chmod(setup_script, 0755);

    // نمرر novnc.tar.gz إلى داخل النظام أيضاً
    sprintf(cmd, 
        "%s -S %s "
        "-b /dev -b /proc -b /sys "
        "-b %s/firefox:/opt/firefox "
        "-b %s:/opt/setup.sh "
        "-b %s:/opt/novnc.tar.gz "
        "-w /root "
        "/bin/bash /opt/setup.sh", 
        proot_bin, rootfs, app_path, setup_script, novnc_tar
    );

    LOGD("Executing Linux: %s", cmd);
    return system(cmd);
}