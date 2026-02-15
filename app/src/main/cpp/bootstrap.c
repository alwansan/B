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
    char init_script[512];
    char cmd[4096];

    // النظام سيتم فكه في app_path/system
    // prepare.py وضع proot داخل المجلد المضغوط، لذا سنجده هناك بعد الفك
    sprintf(proot_bin, "%s/system/proot", app_path);
    sprintf(init_script, "%s/system/init.sh", app_path);

    // نمنح صلاحيات التنفيذ احتياطياً
    chmod(proot_bin, 0755);
    chmod(init_script, 0755);

    // الأمر: تشغيل Proot مباشرة
    // -r: RootFS
    // -w: Workdir
    // /bin/sh /opt/init.sh: تشغيل سكربت الإقلاع الذي وضعناه في prepare.py
    
    sprintf(cmd, 
        "%s -r %s/system "  // RootFS هو المجلد system نفسه لأننا ضغطنا محتويات المجلد
        "-b /dev -b /proc -b /sys "
        "-w /root "
        "/bin/sh /opt/init.sh", 
        proot_bin, app_path
    );

    LOGD("Executing Kernel: %s", cmd);
    return system(cmd);
}