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
    
    char cmd[4096];
    char proot_bin[512];
    char rootfs[512];
    
    sprintf(proot_bin, "%s/proot", app_path);
    sprintf(rootfs, "%s/rootfs", app_path);
    
    chmod(proot_bin, 0755);
    
    // Test Command
    sprintf(cmd, "%s -S %s -b /dev -b /proc -w /root /usr/bin/env", proot_bin, rootfs);
    
    LOGD("Executing: %s", cmd);
    int ret = system(cmd);
    
    (*env)->ReleaseStringUTFChars(env, app_path_j, app_path);
    return ret;
}