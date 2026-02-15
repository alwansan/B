#include <jni.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <stdio.h>
#include <android/log.h>

#define TAG "B_Native"
#define LOGD(...) __android_log_print(ANDROID_LOG_DEBUG, TAG, __VA_ARGS__)

JNIEXPORT jint JNICALL
Java_com_example_b_LauncherActivity_startLinux(JNIEnv *env, jobject thiz, jstring app_path_j) {
    const char *app_path = (*env)->GetStringUTFChars(env, app_path_j, 0);
    
    char proot_bin[512];
    char cmd[4096];

    sprintf(proot_bin, "%s/system/proot", app_path);
    chmod(proot_bin, 0755);
    chmod(app_path, 0755); // Ensure app dir is executable

    // تشغيل Proot
    sprintf(cmd, 
        "%s -r %s/system "
        "-b /dev -b /proc -b /sys "
        "-w /root "
        "/bin/sh /opt/init.sh", 
        proot_bin, app_path
    );

    LOGD("Executing: %s", cmd);
    return system(cmd);
}