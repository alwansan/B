import os
import subprocess

# ==========================================
# إعدادات المشروع
# ==========================================
PROJECT_NAME = "B-Browser"
PACKAGE_NAME = "com.alwansan.b"
REPO_URL = "https://github.com/alwansan/B"
GECKO_VERSION = "121.0.20240213" 

# تعريف المسارات
BASE_DIR = os.getcwd() # سيتم استخدامه لحل مشكلة Git
APP_DIR = os.path.join(BASE_DIR, "app")
SRC_MAIN = os.path.join(APP_DIR, "src", "main")
JAVA_DIR = os.path.join(SRC_MAIN, "java", "com", "alwansan", "b")
RES_LAYOUT = os.path.join(SRC_MAIN, "res", "layout")

# ==========================================
# دالة مساعدة لإنشاء الملفات
# ==========================================
def create_file(path, content):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ تم إنشاء: {os.path.basename(path)}")

# ==========================================
# محتوى الملفات
# ==========================================

settings_gradle = """
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven { url = uri("https://maven.mozilla.org/maven2/") }
    }
}
rootProject.name = "B-Browser"
include(":app")
"""

build_gradle_root = """
plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.20" apply false
}
"""

gradle_properties = """
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.enableJetifier=true
"""

gitignore = """
.gradle
build/
app/build/
local.properties
.idea/
.DS_Store
"""

build_gradle_app = f"""
plugins {{
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}}

android {{
    namespace = "{PACKAGE_NAME}"
    compileSdk = 34

    defaultConfig {{
        applicationId = "{PACKAGE_NAME}"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }}

    buildTypes {{
        release {{
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }}
    }}
    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }}
    kotlinOptions {{
        jvmTarget = "1.8"
    }}
}}

dependencies {{
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("org.mozilla.geckoview:geckoview:{GECKO_VERSION}")
}}
"""

manifest = f"""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="B Browser"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.NoActionBar"
        tools:targetApi="31">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:configChanges="orientation|screenSize|keyboard|keyboardHidden|smallestScreenSize|screenLayout|uiMode"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""

backup_rules = """<?xml version="1.0" encoding="utf-8"?><full-backup-content />"""
data_extraction = """<?xml version="1.0" encoding="utf-8"?><data-extraction-rules />"""

layout_main = """
<?xml version="1.0" encoding="utf-8"?>
<org.mozilla.geckoview.GeckoView
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/gecko_view"
    android:layout_width="match_parent"
    android:layout_height="match_parent" />
"""

main_activity = f"""
package {PACKAGE_NAME}

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import org.mozilla.geckoview.GeckoRuntime
import org.mozilla.geckoview.GeckoSession
import org.mozilla.geckoview.GeckoView

class MainActivity : AppCompatActivity() {{

    private lateinit var geckoView: GeckoView
    private lateinit var geckoSession: GeckoSession
    private lateinit var geckoRuntime: GeckoRuntime

    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        geckoView = findViewById(R.id.gecko_view)
        geckoRuntime = GeckoRuntime.create(this)
        geckoSession = GeckoSession()
        
        val settings = geckoSession.settings
        settings.userAgentOverride = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
        settings.usePrivateMode = false 
        settings.displayMode = GeckoSession.Settings.DISPLAY_MODE_BROWSER
        
        geckoSession.open(geckoRuntime)
        geckoView.setSession(geckoSession)
        geckoSession.loadUri("https://www.google.com")
    }}
}}
"""

github_workflow = """
name: Build B Browser
on:
  push:
    branches: [ "main" ]
  workflow_dispatch:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
    - name: Setup Android SDK
      uses: android-actions/setup-android@v3
    - name: Build APK using Gradle
      run: gradle assembleRelease --no-daemon
    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: B-Browser-APK
        path: app/build/outputs/apk/release/*.apk
"""

# ==========================================
# التنفيذ
# ==========================================

print("🚀 بدء بناء مشروع B-Browser...")

# 1. إنشاء الملفات
create_file("settings.gradle.kts", settings_gradle)
create_file("build.gradle.kts", build_gradle_root)
create_file("gradle.properties", gradle_properties)
create_file(".gitignore", gitignore)
create_file("app/build.gradle.kts", build_gradle_app)
create_file("app/src/main/AndroidManifest.xml", manifest)
create_file("app/src/main/res/xml/backup_rules.xml", backup_rules)
create_file("app/src/main/res/xml/data_extraction_rules.xml", data_extraction)
create_file("app/src/main/res/layout/activity_main.xml", layout_main)
os.makedirs(JAVA_DIR, exist_ok=True)
create_file(os.path.join(JAVA_DIR, "MainActivity.kt"), main_activity)
create_file(".github/workflows/build.yml", github_workflow)

print("✅ تم بناء هيكلة الملفات.")

# 2. عمليات Git
print("🔄 جاري إعداد Git والرفع...")

try:
    # 🔴🔴 الحل لمشكلة الصلاحيات (Dubious Ownership) 🔴🔴
    print("🔧 تطبيق استثناء الأمان للمجلد الحالي...")
    subprocess.run(["git", "config", "--global", "--add", "safe.directory", BASE_DIR], check=True)

    # التحقق من التهيئة
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)
        # إعادة تسمية الفرع فوراً لتجنب المشاكل
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        try:
            subprocess.run(["git", "remote", "add", "origin", REPO_URL], check=True)
        except subprocess.CalledProcessError:
            # إذا كان الريموت موجوداً نحدثه فقط للتأكد
            subprocess.run(["git", "remote", "set-url", "origin", REPO_URL], check=True)

    # تنفيذ الأوامر بالترتيب
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Auto-Build Update"], check=False) # check=False لعدم التوقف إذا لم يكن هناك تغييرات
    
    # الرفع بقوة
    print("🚀 جاري الرفع إلى GitHub...")
    subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
    
    print("\n✅✅ تم بنجاح! راجع Actions الآن:")
    print(f"🔗 {REPO_URL}/actions")

except subprocess.CalledProcessError as e:
    print(f"\n❌ خطأ في Git: {e}")
    print("تأكد أنك قمت بتسجيل الدخول لـ Git مسبقاً.")