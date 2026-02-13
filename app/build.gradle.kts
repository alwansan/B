plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.alwansan.b"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.alwansan.b"
        minSdk = 26
        targetSdk = 34
        versionCode = 3
        versionName = "3.0-Stable-PC"
    }

    signingConfigs {
        create("release") {
            // نستخدم المفتاح الذي سيتم توليده بواسطة السكربت
            storeFile = file("debug.keystore")
            storePassword = "android"
            keyAlias = "androiddebugkey"
            keyPassword = "android"
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            signingConfig = signingConfigs.getByName("release")
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = "1.8"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.11.0")
    // استخدام نسخة مستقرة 108 لحل مشكلة Val cannot be reassigned
    implementation("org.mozilla.geckoview:geckoview:108.0.20221104105437")
}