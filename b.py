import os
import subprocess

# ==========================================
# إعدادات المشروع
# ==========================================
PROJECT_NAME = "B-Browser"
PACKAGE_NAME = "com.alwansan.b"
REPO_URL = "https://github.com/alwansan/B"
GECKO_VERSION = "121.+" 

# تعريف المسارات
BASE_DIR = os.getcwd()
APP_DIR = os.path.join(BASE_DIR, "app")
SRC_MAIN = os.path.join(APP_DIR, "src", "main")
JAVA_DIR = os.path.join(SRC_MAIN, "java", "com", "alwansan", "b")
RES_DIR = os.path.join(SRC_MAIN, "res")
ASSETS_DIR = os.path.join(SRC_MAIN, "assets") 
DRAWABLE_DIR = os.path.join(RES_DIR, "drawable")
LAYOUT_DIR = os.path.join(RES_DIR, "layout")
VALUES_DIR = os.path.join(RES_DIR, "values")

def create_file(path, content):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ تم إنشاء: {os.path.basename(path)}")

# ==========================================
# 1. صفحة البداية المحلية (Home Page) 
# ==========================================
home_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Start</title>
    <style>
        body { margin: 0; overflow: hidden; background-color: #121212; font-family: sans-serif; height: 100vh; display: flex; align-items: center; justify-content: center; color: white; }
        #bgCanvas { position: absolute; top: 0; left: 0; z-index: 0; }
        .container { z-index: 1; text-align: center; width: 90%; max-width: 600px; }
        h1 { font-size: 80px; margin-bottom: 20px; color: #e0e0e0; }
        h1 span { color: #00E5FF; }
        input {
            width: 100%; padding: 15px 25px; border-radius: 30px; border: 1px solid #444;
            background: rgba(30, 30, 30, 0.9); color: white; font-size: 18px; outline: none;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        input:focus { border-color: #00E5FF; box-shadow: 0 0 15px rgba(0, 229, 255, 0.4); }
    </style>
</head>
<body>
    <canvas id="bgCanvas"></canvas>
    <div class="container">
        <h1>B<span>-</span>Browser</h1>
        <form action="https://www.google.com/search" method="GET">
            <input type="text" name="q" placeholder="Search or type URL..." autocomplete="off" autofocus>
        </form>
    </div>
    <script>
        const canvas = document.getElementById('bgCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        let particles = [];
        for(let i=0; i<80; i++) particles.push({
            x: Math.random()*canvas.width, y: Math.random()*canvas.height,
            vx: (Math.random()-0.5)*1, vy: (Math.random()-0.5)*1, size: Math.random()*2
        });
        function animate() {
            ctx.clearRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#00E5FF';
            particles.forEach(p => {
                p.x+=p.vx; p.y+=p.vy;
                if(p.x<0||p.x>canvas.width) p.vx*=-1;
                if(p.y<0||p.y>canvas.height) p.vy*=-1;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI*2); ctx.fill();
            });
            // Lines
            ctx.strokeStyle = 'rgba(0, 229, 255, 0.1)';
            for(let i=0; i<particles.length; i++) {
                for(let j=i; j<particles.length; j++) {
                    let dx = particles[i].x - particles[j].x;
                    let dy = particles[i].y - particles[j].y;
                    if(Math.sqrt(dx*dx+dy*dy) < 100) {
                        ctx.beginPath(); ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y); ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(animate);
        }
        animate();
    </script>
</body>
</html>
"""

# ==========================================
# 2. ملفات التصميم
# ==========================================

colors_xml = """
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="background_dark">#121212</color>
    <color name="surface_gray">#1E1E1E</color>
    <color name="tab_selected">#323232</color>
    <color name="tab_unselected">#121212</color>
    <color name="neon_blue">#00E5FF</color>
    <color name="text_white">#FFFFFF</color>
</resources>
"""

bg_tab_xml = """
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_selected="true">
        <shape>
            <solid android:color="@color/tab_selected"/>
            <corners android:topLeftRadius="8dp" android:topRightRadius="8dp"/>
            <stroke android:width="2dp" android:color="@color/neon_blue"/>
        </shape>
    </item>
    <item>
        <shape>
            <solid android:color="@color/tab_unselected"/>
            <corners android:topLeftRadius="8dp" android:topRightRadius="8dp"/>
            <stroke android:width="1dp" android:color="#33FFFFFF"/>
        </shape>
    </item>
</selector>
"""

bg_url_bar_xml = """
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#2C2C2C"/>
    <corners android:radius="20dp"/>
    <stroke android:width="1dp" android:color="#444"/>
</shape>
"""

item_tab_xml = """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="150dp"
    android:layout_height="38dp"
    android:background="@drawable/bg_tab"
    android:gravity="center_vertical"
    android:orientation="horizontal"
    android:paddingStart="10dp"
    android:paddingEnd="5dp"
    android:layout_marginEnd="2dp">

    <TextView
        android:id="@+id/tab_title"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_weight="1"
        android:text="Loading..."
        android:textColor="#FFFFFF"
        android:textSize="12sp"
        android:singleLine="true"
        android:ellipsize="end" />

    <ImageButton
        android:id="@+id/btn_close_tab"
        android:layout_width="28dp"
        android:layout_height="28dp"
        android:background="?attr/selectableItemBackgroundBorderless"
        android:src="@android:drawable/ic_menu_close_clear_cancel"
        android:tint="#AAAAAA" />
</LinearLayout>
"""

activity_main_xml = """
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/background_dark">

    <!-- شريط الأدوات العلوي -->
    <LinearLayout
        android:id="@+id/ui_container"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:background="#121212"
        android:elevation="6dp">

        <!-- منطقة التبويبات -->
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="40dp"
            android:orientation="horizontal"
            android:paddingTop="2dp">
            
            <HorizontalScrollView
                android:layout_width="0dp"
                android:layout_height="match_parent"
                android:layout_weight="1"
                android:fillViewport="true"
                android:scrollbars="none">
                <LinearLayout
                    android:id="@+id/tabs_container"
                    android:layout_width="wrap_content"
                    android:layout_height="match_parent"
                    android:orientation="horizontal"/>
            </HorizontalScrollView>

            <Button
                android:id="@+id/btn_add_tab"
                android:layout_width="40dp"
                android:layout_height="40dp"
                android:text="+"
                android:textSize="22sp"
                android:textColor="@color/neon_blue"
                android:background="?attr/selectableItemBackground" />
        </LinearLayout>

        <!-- شريط العنوان -->
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="50dp"
            android:gravity="center_vertical"
            android:padding="6dp"
            android:background="#1E1E1E">
            
            <EditText
                android:id="@+id/url_input"
                android:layout_width="0dp"
                android:layout_height="match_parent"
                android:layout_weight="1"
                android:background="@drawable/bg_url_bar"
                android:hint="Search or enter address"
                android:paddingStart="16dp"
                android:textColor="#FFF"
                android:textColorHint="#888"
                android:textSize="14sp"
                android:singleLine="true"
                android:inputType="textUri"
                android:imeOptions="actionGo"/>
            
            <Button
                android:id="@+id/btn_go"
                android:layout_width="50dp"
                android:layout_height="match_parent"
                android:text="GO"
                android:textColor="@color/neon_blue"
                android:background="?attr/selectableItemBackground"
                android:textStyle="bold"/>
        </LinearLayout>
    </LinearLayout>

    <org.mozilla.geckoview.GeckoView
        android:id="@+id/gecko_view"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:layout_below="@id/ui_container"/>

</RelativeLayout>
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

# ==========================================
# 3. إعدادات Gradle
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
        versionCode = 11
        versionName = "11.0-Persistent"
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
            isMinifyEnabled = false
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
    implementation("org.mozilla.geckoview:geckoview:{GECKO_VERSION}")
}}
"""

manifest = f"""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@drawable/ic_launcher"
        android:label="B Browser"
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
# 4. كود Kotlin (المنطق الكامل) 🧠
# ==========================================

main_activity = f"""
package {PACKAGE_NAME}

import android.content.Context
import android.os.Bundle
import android.view.KeyEvent
import android.view.LayoutInflater
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import org.mozilla.geckoview.GeckoRuntime
import org.mozilla.geckoview.GeckoSession
import org.mozilla.geckoview.GeckoSessionSettings
import org.mozilla.geckoview.GeckoView
import java.io.File
import java.io.FileOutputStream

class MainActivity : AppCompatActivity() {{

    private lateinit var geckoView: GeckoView
    private lateinit var geckoRuntime: GeckoRuntime
    private lateinit var tabsContainer: LinearLayout
    private lateinit var urlInput: EditText
    private lateinit var uiContainer: LinearLayout

    private val sessions = ArrayList<TabSession>()
    private var currentTabIndex = -1
    private var isGhostMode = false
    private val HOME_FILE_NAME = "home.html"
    private lateinit var homeUrl: String

    data class TabSession(
        val session: GeckoSession,
        val tabView: View,
        var currentUrl: String = ""
    )

    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // 1. تجهيز ملف الواجهة محلياً (حل مشكلة File Not Found)
        setupLocalHomeFile()

        geckoView = findViewById(R.id.gecko_view)
        tabsContainer = findViewById(R.id.tabs_container)
        urlInput = findViewById(R.id.url_input)
        uiContainer = findViewById(R.id.ui_container)

        // 2. إعداد المحرك
        geckoRuntime = GeckoRuntime.create(this)

        findViewById<Button>(R.id.btn_add_tab).setOnClickListener {{ addNewTab(homeUrl) }}
        findViewById<Button>(R.id.btn_go).setOnClickListener {{ loadUrl(urlInput.text.toString()) }}

        urlInput.setOnEditorActionListener {{ _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_GO || actionId == EditorInfo.IME_ACTION_DONE) {{
                loadUrl(urlInput.text.toString())
                true
            }} else {{ false }}
        }}

        // 3. استعادة التبويبات السابقة (Persistent Tabs)
        restoreTabs()
    }}

    private fun setupLocalHomeFile() {{
        // نسخ ملف home.html من assets إلى الذاكرة الداخلية للهاتف
        val file = File(filesDir, HOME_FILE_NAME)
        if (!file.exists()) {{
            try {{
                assets.open(HOME_FILE_NAME).use {{ input ->
                    FileOutputStream(file).use {{ output ->
                        input.copyTo(output)
                    }}
                }}
            }} catch (e: Exception) {{
                e.printStackTrace()
            }}
        }}
        homeUrl = "file://" + file.absolutePath
    }}

    private fun addNewTab(urlToLoad: String) {{
        val settings = GeckoSessionSettings.Builder()
            .usePrivateMode(false) // حفظ الكوكيز والبيانات
            .viewportMode(GeckoSessionSettings.VIEWPORT_MODE_DESKTOP)
            // 🔥 تغيير UserAgent إلى Firefox Desktop (يحل مشكلة Google Captcha) 🔥
            .userAgentOverride("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0")
            .build()

        val session = GeckoSession(settings)
        session.open(geckoRuntime)

        val tabView = LayoutInflater.from(this).inflate(R.layout.item_tab, tabsContainer, false)
        val tabTitle = tabView.findViewById<TextView>(R.id.tab_title)
        val btnClose = tabView.findViewById<ImageButton>(R.id.btn_close_tab)

        val newTab = TabSession(session, tabView, urlToLoad)
        sessions.add(newTab)
        
        val newIndex = sessions.size - 1

        tabView.setOnClickListener {{ switchToTab(sessions.indexOf(newTab)) }}
        btnClose.setOnClickListener {{ closeTab(sessions.indexOf(newTab)) }}
        
        tabsContainer.addView(tabView)
        switchToTab(newIndex)
        
        session.loadUri(urlToLoad)
    }}

    private fun switchToTab(index: Int) {{
        if (index !in sessions.indices) return
        currentTabIndex = index
        val tab = sessions[index]
        geckoView.setSession(tab.session)

        for (i in sessions.indices) {{
            sessions[i].tabView.isSelected = (i == index)
        }}
        
        // تحديث شريط العنوان (بدون بروتوكول للتجميل)
        // في التطبيق الحقيقي سنستمع لتغيرات الرابط
    }}

    private fun closeTab(index: Int) {{
        if (index !in sessions.indices) return
        val tab = sessions[index]
        tab.session.close()
        tabsContainer.removeView(tab.tabView)
        sessions.removeAt(index)

        if (sessions.isEmpty()) {{
            addNewTab(homeUrl)
        }} else {{
            switchToTab(if (index > 0) index - 1 else 0)
        }}
    }}

    private fun loadUrl(input: String) {{
        if (currentTabIndex == -1) return
        val session = sessions[currentTabIndex].session
        var url = input.trim()
        if (url.isEmpty()) return

        if (url.contains(" ") || !url.contains(".")) {{
            url = "https://www.google.com/search?q=$url"
        }} else if (!url.startsWith("http") && !url.startsWith("file")) {{
            url = "https://$url"
        }}
        
        // تحديث الرابط الحالي في الذاكرة للحفظ
        sessions[currentTabIndex].currentUrl = url
        session.loadUri(url)
        
        // 🔥 تسجيل في السجل (History Log) 🔥
        addToHistoryLog(url)
    }}

    // ==================
    // 💾 نظام الحفظ والاستعادة
    // ==================
    
    override fun onPause() {{
        super.onPause()
        saveTabsState()
    }}

    private fun saveTabsState() {{
        val prefs = getSharedPreferences("BrowserState", Context.MODE_PRIVATE)
        val editor = prefs.edit()
        
        // حفظ عدد التبويبات
        editor.putInt("tab_count", sessions.size)
        
        // حفظ رابط كل تبويب (نحاول جلب الرابط الحقيقي من المحرك)
        for (i in sessions.indices) {{
            // ملاحظة: loader.uri قد لا يكون محدثاً فوراً، لذا نعتمد على ما طلبناه مبدئياً
            // أو يمكن تحسينه لاحقاً بـ ProgressDelegate
            var url = sessions[i].currentUrl
            if (url.isEmpty()) url = homeUrl
            editor.putString("tab_$i", url)
        }}
        editor.putInt("last_index", currentTabIndex)
        editor.apply()
    }}

    private fun restoreTabs() {{
        val prefs = getSharedPreferences("BrowserState", Context.MODE_PRIVATE)
        val count = prefs.getInt("tab_count", 0)
        
        if (count > 0) {{
            for (i in 0 until count) {{
                val url = prefs.getString("tab_$i", homeUrl) ?: homeUrl
                addNewTab(url)
            }}
            val lastIndex = prefs.getInt("last_index", 0)
            switchToTab(lastIndex)
        }} else {{
            // فتح صفحة واحدة افتراضية
            addNewTab(homeUrl)
        }}
    }}

    private fun addToHistoryLog(url: String) {{
        // حفظ بسيط في ملف نصي
        try {{
            val file = File(filesDir, "history.txt")
            file.appendText(System.currentTimeMillis().toString() + ": " + url + "\\n")
        }} catch (e: Exception) {{}}
    }}

    // ==================
    // 👻 وضع الشبح (Ctrl+G)
    // ==================
    override fun dispatchKeyEvent(event: KeyEvent): Boolean {{
        if (event.action == KeyEvent.ACTION_DOWN && event.isCtrlPressed && event.keyCode == KeyEvent.KEYCODE_G) {{
            isGhostMode = !isGhostMode
            if (isGhostMode) {{
                uiContainer.visibility = View.GONE
                window.decorView.systemUiVisibility = (View.SYSTEM_UI_FLAG_FULLSCREEN or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION or View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY)
            }} else {{
                uiContainer.visibility = View.VISIBLE
                window.decorView.systemUiVisibility = View.SYSTEM_UI_FLAG_VISIBLE
            }}
            return true
        }}
        return super.dispatchKeyEvent(event)
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
        cache: gradle
        
    - name: Setup Android SDK
      uses: android-actions/setup-android@v3
      
    - name: Setup Gradle
      uses: gradle/actions/setup-gradle@v3
      with:
        gradle-version: '8.5'
    
    - name: Generate Keystore
      run: |
        keytool -genkey -v -keystore app/debug.keystore -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=Android Debug,O=Android,C=US"
    
    - name: Build APK (Release)
      run: gradle assembleRelease
      
    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: B-Browser-Persistent
        path: app/build/outputs/apk/release/*.apk
"""

# ==========================================
# التنفيذ
# ==========================================
print("🚀 بدء بناء النسخة النهائية (إصلاح شامل: Google + الملفات + الحفظ)...")

create_file("settings.gradle.kts", settings_gradle)
create_file("build.gradle.kts", build_gradle_root)
create_file("gradle.properties", gradle_properties)
create_file(".gitignore", gitignore)
create_file("app/build.gradle.kts", build_gradle_app)
create_file("app/src/main/AndroidManifest.xml", manifest)
create_file("app/src/main/res/xml/backup_rules.xml", backup_rules)
create_file("app/src/main/res/xml/data_extraction_rules.xml", data_extraction)

# صفحة الواجهة
os.makedirs(ASSETS_DIR, exist_ok=True)
create_file(os.path.join(ASSETS_DIR, "home.html"), home_html)

# الموارد
os.makedirs(VALUES_DIR, exist_ok=True)
create_file(os.path.join(VALUES_DIR, "colors.xml"), colors_xml)
os.makedirs(DRAWABLE_DIR, exist_ok=True)
create_file(os.path.join(DRAWABLE_DIR, "ic_launcher.xml"), ic_launcher_xml)
create_file(os.path.join(DRAWABLE_DIR, "bg_tab.xml"), bg_tab_xml)
create_file(os.path.join(DRAWABLE_DIR, "bg_url_bar.xml"), bg_url_bar_xml)

os.makedirs(LAYOUT_DIR, exist_ok=True)
create_file(os.path.join(LAYOUT_DIR, "activity_main.xml"), activity_main_xml)
create_file(os.path.join(LAYOUT_DIR, "item_tab.xml"), item_tab_xml)

os.makedirs(JAVA_DIR, exist_ok=True)
create_file(os.path.join(JAVA_DIR, "MainActivity.kt"), main_activity)
create_file(".github/workflows/build.yml", github_workflow)

print("✅ تم تجهيز الكود: UserAgent جديد، نظام حفظ التبويبات، وإصلاح assets.")
print("🔄 جاري الرفع إلى GitHub...")

try:
    subprocess.run(["git", "config", "--global", "--add", "safe.directory", BASE_DIR], check=True)
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)

    try:
        subprocess.run(["git", "remote", "add", "origin", REPO_URL], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(["git", "remote", "set-url", "origin", REPO_URL], check=True)

    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Fix: Google Captcha, Missing File, and Tab Persistence"], check=False)
    
    print("🔧 توحيد اسم الفرع...")
    subprocess.run(["git", "branch", "-M", "main"], check=True)

    print("🚀 جاري الرفع إلى GitHub...")
    subprocess.run(["git", "push", "-u", "-f", "origin", "main"], check=True)
    
    print("\n✅✅ الحلول المطبقة:")
    print("1. تغيير الهوية إلى Firefox Desktop لمنع حظر جوجل.")
    print("2. نسخ home.html للذاكرة الداخلية لحل مشكلة 'File not found'.")
    print("3. نظام حفظ تلقائي للتبويبات عند الخروج.")
    print(f"🔗 {REPO_URL}/actions")

except subprocess.CalledProcessError as e:
    print(f"\n❌ خطأ: {e}")