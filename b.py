import os
import subprocess

# ==========================================
# إعدادات المشروع
# ==========================================
PROJECT_NAME = "B-Browser"
PACKAGE_NAME = "com.alwansan.b"
REPO_URL = "https://github.com/alwansan/B"

# 🔥 التعديل: استخدام نسخة رسمية موجودة ومستقرة 🔥
GECKO_VERSION = "109.0.1" 

# تعريف المسارات
BASE_DIR = os.getcwd()
APP_DIR = os.path.join(BASE_DIR, "app")
SRC_MAIN = os.path.join(APP_DIR, "src", "main")
JAVA_DIR = os.path.join(SRC_MAIN, "java", "com", "alwansan", "b")
RES_DIR = os.path.join(SRC_MAIN, "res")
DRAWABLE_DIR = os.path.join(RES_DIR, "drawable")
LAYOUT_DIR = os.path.join(RES_DIR, "layout")
VALUES_DIR = os.path.join(RES_DIR, "values")

# ==========================================
# دالة مساعدة
# ==========================================
def create_file(path, content):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ تم إنشاء: {os.path.basename(path)}")

# ==========================================
# 1. ملفات التصميم (UI) - Dark Mode & PC Look
# ==========================================

colors_xml = """
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="black_overlay">#CC000000</color>
    <color name="dark_gray">#1E1E1E</color>
    <color name="neon_blue">#00E5FF</color>
    <color name="transparent_gray">#99121212</color>
    <color name="white">#FFFFFF</color>
</resources>
"""

bg_search_bar_xml = """
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/transparent_gray"/>
    <corners android:radius="20dp"/>
    <stroke android:width="1dp" android:color="#33FFFFFF"/>
</shape>
"""

ic_launcher_xml = """
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path android:fillColor="#121212" android:pathData="M0,0h108v108h-108z"/>
    <path android:fillColor="#00E5FF" android:pathData="M30,30h48v48h-48z"/>
    <path android:fillColor="#FFFFFF" android:pathData="M40,40h28v28h-28z"/>
</vector>
"""

activity_main_xml = """
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#000000">

    <org.mozilla.geckoview.GeckoView
        android:id="@+id/gecko_view"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_alignParentBottom="true"
        android:layout_margin="16dp"
        android:background="@drawable/bg_search_bar"
        android:elevation="8dp"
        android:gravity="center_vertical"
        android:orientation="horizontal"
        android:padding="8dp">

        <EditText
            android:id="@+id/url_input"
            android:layout_width="0dp"
            android:layout_height="40dp"
            android:layout_weight="1"
            android:background="@null"
            android:hint="Type URL..."
            android:imeOptions="actionGo"
            android:inputType="textUri"
            android:paddingStart="12dp"
            android:paddingEnd="12dp"
            android:textColor="@color/white"
            android:textColorHint="#88FFFFFF"
            android:textSize="14sp" />

        <Button
            android:id="@+id/btn_go"
            android:layout_width="60dp"
            android:layout_height="40dp"
            android:backgroundTint="@color/neon_blue"
            android:text="GO"
            android:textColor="#000000"
            android:textStyle="bold" />

    </LinearLayout>
</RelativeLayout>
"""

# ==========================================
# 2. ملفات البناء (Gradle)
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
*.iml
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
        versionCode = 4
        versionName = "4.0-Stable-PC"
    }}

    signingConfigs {{
        create("release") {{
            storeFile = file("debug.keystore")
            storePassword = "android"
            keyAlias = "androiddebugkey"
            keyPassword = "android"
        }}
    }}

    buildTypes {{
        release {{
            isMinifyEnabled = true
            signingConfig = signingConfigs.getByName("release")
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
    implementation("com.google.android.material:material:1.11.0")
    // استخدام النسخة 109.0.1 المستقرة والموجودة
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
        android:icon="@drawable/ic_launcher"
        android:label="B Desktop Browser"
        android:roundIcon="@drawable/ic_launcher"
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

# ==========================================
# 3. كود Kotlin (نسخة تعمل مع API المستقر)
# ==========================================

main_activity = f"""
package {PACKAGE_NAME}

import android.os.Bundle
import android.view.inputmethod.EditorInfo
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity
import org.mozilla.geckoview.GeckoRuntime
import org.mozilla.geckoview.GeckoSession
import org.mozilla.geckoview.GeckoSessionSettings
import org.mozilla.geckoview.GeckoView

class MainActivity : AppCompatActivity() {{

    private lateinit var geckoView: GeckoView
    private lateinit var geckoSession: GeckoSession
    private lateinit var geckoRuntime: GeckoRuntime
    private lateinit var urlInput: EditText
    private lateinit var btnGo: Button

    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        geckoView = findViewById(R.id.gecko_view)
        urlInput = findViewById(R.id.url_input)
        btnGo = findViewById(R.id.btn_go)

        geckoRuntime = GeckoRuntime.create(this)
        
        val settings = GeckoSessionSettings()
        
        // 1. إجبار وضع سطح المكتب
        settings.viewportMode = GeckoSessionSettings.VIEWPORT_MODE_DESKTOP
        settings.usePrivateMode = false
        settings.displayMode = GeckoSessionSettings.DISPLAY_MODE_BROWSER
        
        // 2. تزوير الهوية (PC User Agent) - Windows Chrome
        settings.userAgentOverride = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"

        geckoSession = GeckoSession(settings)
        geckoSession.open(geckoRuntime)
        geckoView.setSession(geckoSession)

        // تحميل Matecat
        geckoSession.loadUri("https://www.matecat.com/") 

        btnGo.setOnClickListener {{
            loadUrlFromInput()
        }}

        urlInput.setOnEditorActionListener {{ _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_GO || actionId == EditorInfo.IME_ACTION_DONE) {{
                loadUrlFromInput()
                true
            }} else {{
                false
            }}
        }}
    }}

    private fun loadUrlFromInput() {{
        var url = urlInput.text.toString().trim()
        if (url.isNotEmpty()) {{
            if (!url.startsWith("http")) {{
                url = "https://$url"
            }}
            geckoSession.loadUri(url)
        }}
    }}
    
    override fun onBackPressed() {{
        // لا يوجد كود هنا حاليا
        super.onBackPressed()
    }}
}}
"""

# 🔥 التعديل هنا: أمر إنشاء المفتاح داخل GitHub Actions 🔥
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
      
    - name: Setup Gradle
      uses: gradle/actions/setup-gradle@v3
      with:
        gradle-version: '8.5'
    
    # 🔥 خطوة جديدة: توليد المفتاح داخل السيرفر 🔥
    - name: Generate Keystore
      run: |
        keytool -genkey -v -keystore app/debug.keystore -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=Android Debug,O=Android,C=US"
    
    - name: Build APK (Release)
      run: gradle assembleRelease
      
    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: B-Browser-PC-Edition
        path: app/build/outputs/apk/release/*.apk
"""

# ==========================================
# التنفيذ
# ==========================================
print("🚀 بدء بناء النسخة النهائية (B-Browser Stable PC)...")

create_file("settings.gradle.kts", settings_gradle)
create_file("build.gradle.kts", build_gradle_root)
create_file("gradle.properties", gradle_properties)
create_file(".gitignore", gitignore)
create_file("app/build.gradle.kts", build_gradle_app)
create_file("app/src/main/AndroidManifest.xml", manifest)
create_file("app/src/main/res/xml/backup_rules.xml", backup_rules)
create_file("app/src/main/res/xml/data_extraction_rules.xml", data_extraction)

os.makedirs(VALUES_DIR, exist_ok=True)
create_file(os.path.join(VALUES_DIR, "colors.xml"), colors_xml)

os.makedirs(DRAWABLE_DIR, exist_ok=True)
create_file(os.path.join(DRAWABLE_DIR, "ic_launcher.xml"), ic_launcher_xml)
create_file(os.path.join(DRAWABLE_DIR, "bg_search_bar.xml"), bg_search_bar_xml)

os.makedirs(LAYOUT_DIR, exist_ok=True)
create_file(os.path.join(LAYOUT_DIR, "activity_main.xml"), activity_main_xml)

os.makedirs(JAVA_DIR, exist_ok=True)
create_file(os.path.join(JAVA_DIR, "MainActivity.kt"), main_activity)
create_file(".github/workflows/build.yml", github_workflow)

print("✅ تم تجهيز الملفات (إصلاح النسخة + توليد المفتاح سحابياً).")
print("🔄 جاري إعداد Git والرفع...")

try:
    subprocess.run(["git", "config", "--global", "--add", "safe.directory", BASE_DIR], check=True)
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)

    try:
        subprocess.run(["git", "remote", "add", "origin", REPO_URL], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(["git", "remote", "set-url", "origin", REPO_URL], check=True)

    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Final Fix: Gecko 109.0.1 + Cloud Keystore"], check=False)
    
    print("🔧 توحيد اسم الفرع...")
    subprocess.run(["git", "branch", "-M", "main"], check=True)

    print("🚀 جاري الرفع إلى GitHub...")
    subprocess.run(["git", "push", "-u", "-f", "origin", "main"], check=True)
    
    print("\n✅✅ تم التحديث! هذا البناء سينجح بإذن الله.")
    print(f"🔗 {REPO_URL}/actions")

except subprocess.CalledProcessError as e:
    print(f"\n❌ خطأ: {e}")