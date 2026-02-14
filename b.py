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
ASSETS_DIR = os.path.join(SRC_MAIN, "assets") # مجلد الأصول
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
# 1. صفحة البداية المحلية (Home Page) 🏠
# ==========================================
home_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Tab</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background-color: #121212;
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            color: white;
        }
        #bgCanvas { position: absolute; top: 0; left: 0; z-index: 0; }
        .content { z-index: 1; text-align: center; width: 100%; max-width: 700px; animation: popIn 0.8s ease; }
        h1 { font-size: 90px; margin: 0; letter-spacing: -3px; color: #e0e0e0; text-shadow: 0 0 20px rgba(255,255,255,0.1); }
        h1 span { color: #00E5FF; }
        .search-container {
            margin-top: 30px;
            position: relative;
            width: 100%;
        }
        input {
            width: 100%;
            padding: 18px 30px;
            border-radius: 50px;
            border: 2px solid #333;
            background: rgba(30, 30, 30, 0.8);
            color: white;
            font-size: 20px;
            outline: none;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            transition: 0.3s;
        }
        input:focus {
            border-color: #00E5FF;
            box-shadow: 0 0 30px rgba(0, 229, 255, 0.3);
            background: #1E1E1E;
        }
        @keyframes popIn { 0% { opacity: 0; transform: scale(0.9); } 100% { opacity: 1; transform: scale(1); } }
    </style>
</head>
<body>
    <canvas id="bgCanvas"></canvas>
    <div class="content">
        <h1>G<span>oo</span>gle</h1>
        <div class="search-container">
            <form action="https://www.google.com/search" method="GET">
                <input type="text" name="q" placeholder="Search Google or type URL..." autofocus autocomplete="off">
            </form>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('bgCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        let particles = [];
        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2;
                this.speedX = Math.random() * 1 - 0.5;
                this.speedY = Math.random() * 1 - 0.5;
            }
            update() {
                this.x += this.speedX; this.y += this.speedY;
                if (this.x > canvas.width || this.x < 0) this.speedX *= -1;
                if (this.y > canvas.height || this.y < 0) this.speedY *= -1;
            }
            draw() {
                ctx.fillStyle = '#00E5FF'; ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2); ctx.fill();
            }
        }
        function init() { for (let i = 0; i < 100; i++) particles.push(new Particle()); }
        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particles.length; i++) {
                particles[i].update(); particles[i].draw();
                for (let j = i; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    if (distance < 100) {
                        ctx.strokeStyle = `rgba(0, 229, 255, ${1 - distance/100})`;
                        ctx.lineWidth = 0.5; ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y); ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(animate);
        }
        init(); animate();
        window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; });
    </script>
</body>
</html>
"""

# ==========================================
# 2. ملفات التصميم (UI)
# ==========================================

colors_xml = """
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="background_dark">#000000</color>
    <color name="surface_gray">#1E1E1E</color>
    <color name="tab_selected">#333333</color>
    <color name="tab_unselected">#121212</color>
    <color name="neon_blue">#00E5FF</color>
    <color name="text_white">#FFFFFF</color>
</resources>
"""

# خلفية التبويب (Tab Background)
bg_tab_xml = """
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_selected="true">
        <shape>
            <solid android:color="@color/tab_selected"/>
            <corners android:topLeftRadius="12dp" android:topRightRadius="12dp"/>
            <stroke android:width="2dp" android:color="@color/neon_blue"/>
        </shape>
    </item>
    <item>
        <shape>
            <solid android:color="@color/tab_unselected"/>
            <corners android:topLeftRadius="12dp" android:topRightRadius="12dp"/>
            <stroke android:width="1dp" android:color="#33FFFFFF"/>
        </shape>
    </item>
</selector>
"""

# شكل شريط العنوان
bg_url_bar_xml = """
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#2C2C2C"/>
    <corners android:radius="8dp"/>
</shape>
"""

# تصميم العنصر الواحد في شريط التبويبات (Item Tab)
item_tab_xml = """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="160dp"
    android:layout_height="40dp"
    android:background="@drawable/bg_tab"
    android:gravity="center_vertical"
    android:orientation="horizontal"
    android:paddingStart="8dp"
    android:paddingEnd="4dp"
    android:layout_marginEnd="4dp">

    <TextView
        android:id="@+id/tab_title"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_weight="1"
        android:text="New Tab"
        android:textColor="#FFFFFF"
        android:textSize="12sp"
        android:singleLine="true"
        android:ellipsize="end" />

    <ImageButton
        android:id="@+id/btn_close_tab"
        android:layout_width="24dp"
        android:layout_height="24dp"
        android:background="?attr/selectableItemBackgroundBorderless"
        android:src="@android:drawable/ic_menu_close_clear_cancel"
        android:tint="#88FFFFFF" />
</LinearLayout>
"""

# الواجهة الرئيسية
activity_main_xml = """
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/background_dark">

    <!-- حاوية عناصر التحكم العلوية (تختفي بـ Ctrl+G) -->
    <LinearLayout
        android:id="@+id/ui_container"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:background="#121212"
        android:elevation="4dp">

        <!-- شريط التبويبات -->
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="44dp"
            android:orientation="horizontal"
            android:gravity="center_vertical">
            
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
                    android:orientation="horizontal"
                    android:paddingTop="4dp"/>
            </HorizontalScrollView>

            <!-- زر إضافة تبويب -->
            <Button
                android:id="@+id/btn_add_tab"
                android:layout_width="44dp"
                android:layout_height="40dp"
                android:text="+"
                android:textSize="20sp"
                android:background="?attr/selectableItemBackground"
                android:textColor="@color/neon_blue" />
        </LinearLayout>

        <!-- شريط العنوان -->
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="50dp"
            android:padding="8dp"
            android:background="#1E1E1E"
            android:gravity="center_vertical">
            
            <EditText
                android:id="@+id/url_input"
                android:layout_width="0dp"
                android:layout_height="match_parent"
                android:layout_weight="1"
                android:background="@drawable/bg_url_bar"
                android:hint="Search Google or enter URL..."
                android:paddingStart="12dp"
                android:textColor="#FFF"
                android:textColorHint="#888"
                android:textSize="14sp"
                android:singleLine="true"
                android:imeOptions="actionSearch"/>

            <Button
                android:id="@+id/btn_go"
                android:layout_width="60dp"
                android:layout_height="match_parent"
                android:text="GO"
                android:textColor="@color/neon_blue"
                android:background="?attr/selectableItemBackground"
                android:textStyle="bold"/>
        </LinearLayout>
    </LinearLayout>

    <!-- منطقة عرض المتصفح -->
    <org.mozilla.geckoview.GeckoView
        android:id="@+id/gecko_view"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:layout_below="@id/ui_container"/>

</RelativeLayout>
"""

# أيقونة التطبيق (محدثة)
ic_launcher_xml = """
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path android:fillColor="#000000" android:pathData="M0,0h108v108h-108z"/>
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
        versionCode = 10
        versionName = "10.0-MultiTab"
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
# 4. كود Kotlin (إدارة التبويبات المعقدة)
# ==========================================

main_activity = f"""
package {PACKAGE_NAME}

import android.graphics.Color
import android.os.Bundle
import android.view.KeyEvent
import android.view.LayoutInflater
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.Button
import android.widget.EditText
import android.widget.ImageButton
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import org.mozilla.geckoview.GeckoRuntime
import org.mozilla.geckoview.GeckoSession
import org.mozilla.geckoview.GeckoSessionSettings
import org.mozilla.geckoview.GeckoView

class MainActivity : AppCompatActivity() {{

    private lateinit var geckoView: GeckoView
    private lateinit var geckoRuntime: GeckoRuntime
    private lateinit var tabsContainer: LinearLayout
    private lateinit var urlInput: EditText
    private lateinit var uiContainer: LinearLayout

    // قائمة الجلسات (التبويبات)
    private val sessions = ArrayList<TabSession>()
    private var currentTabIndex = -1
    private var isGhostMode = false

    // كلاس لتخزين بيانات كل تبويب
    data class TabSession(
        val session: GeckoSession,
        val tabView: View,
        var title: String = "New Tab"
    )

    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        geckoView = findViewById(R.id.gecko_view)
        tabsContainer = findViewById(R.id.tabs_container)
        urlInput = findViewById(R.id.url_input)
        uiContainer = findViewById(R.id.ui_container)
        
        val btnAddTab: Button = findViewById(R.id.btn_add_tab)
        val btnGo: Button = findViewById(R.id.btn_go)

        // إعداد المحرك مرة واحدة
        geckoRuntime = GeckoRuntime.create(this)

        // زر إضافة تبويب جديد
        btnAddTab.setOnClickListener {{
            addNewTab()
        }}

        // زر البحث
        btnGo.setOnClickListener {{
            loadUrl(urlInput.text.toString())
        }}

        urlInput.setOnEditorActionListener {{ _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_SEARCH || actionId == EditorInfo.IME_ACTION_GO) {{
                loadUrl(urlInput.text.toString())
                true
            }} else {{
                false
            }}
        }}

        // إضافة التبويب الأول تلقائياً
        addNewTab()
    }}

    private fun addNewTab() {{
        // إعدادات الجلسة (Desktop Mode)
        val settings = GeckoSessionSettings.Builder()
            .usePrivateMode(false)
            .viewportMode(GeckoSessionSettings.VIEWPORT_MODE_DESKTOP)
            .userAgentOverride("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
            .build()

        val session = GeckoSession(settings)
        session.open(geckoRuntime)

        // إنشاء زر التبويب في الشريط
        val tabView = LayoutInflater.from(this).inflate(R.layout.item_tab, tabsContainer, false)
        val tabTitle = tabView.findViewById<TextView>(R.id.tab_title)
        val btnClose = tabView.findViewById<ImageButton>(R.id.btn_close_tab)

        val newTabSession = TabSession(session, tabView)
        sessions.add(newTabSession)
        val newIndex = sessions.size - 1

        // برمجة الضغط على التبويب
        tabView.setOnClickListener {{
            switchToTab(sessions.indexOf(newTabSession))
        }}

        // برمجة زر الإغلاق (x)
        btnClose.setOnClickListener {{
            closeTab(sessions.indexOf(newTabSession))
        }}

        // إضافة التبويب للشريط
        tabsContainer.addView(tabView)

        // الانتقال للتبويب الجديد
        switchToTab(newIndex)

        // تحميل الصفحة الرئيسية
        // استخدام file:///android_asset/ هو الصحيح لـ GeckoView
        session.loadUri("file:///android_asset/home.html")
    }}

    private fun switchToTab(index: Int) {{
        if (index !in sessions.indices) return

        currentTabIndex = index
        val tabSession = sessions[index]

        // ربط الجلسة بالمتصفح (هذا لا يغلق الجلسات الأخرى، فقط يخفيها)
        geckoView.setSession(tabSession.session)

        // تحديث تصميم الشريط (تمييز التبويب النشط)
        for (i in sessions.indices) {{
            sessions[i].tabView.isSelected = (i == index)
        }}

        // تحديث شريط العنوان (إذا لم تكن الصفحة الرئيسية)
        // (يمكن تطوير هذا الجزء لاحقاً لجلب العنوان الحقيقي)
        urlInput.setText("") 
        urlInput.hint = "Search Google..."
    }}

    private fun closeTab(index: Int) {{
        if (index !in sessions.indices) return

        val tabSession = sessions[index]
        
        // إغلاق الجلسة لتوفير الذاكرة
        tabSession.session.close()
        
        // حذف من الواجهة والقائمة
        tabsContainer.removeView(tabSession.tabView)
        sessions.removeAt(index)

        if (sessions.isEmpty()) {{
            // إذا أغلق آخر تبويب، افتح واحداً جديداً
            addNewTab()
        }} else {{
            // الانتقال للتبويب السابق
            val nextIndex = if (index > 0) index - 1 else 0
            switchToTab(nextIndex)
        }}
    }}

    private fun loadUrl(input: String) {{
        if (currentTabIndex == -1) return
        val session = sessions[currentTabIndex].session
        
        var url = input.trim()
        if (url.isEmpty()) return

        // التحقق هل هو رابط أم بحث
        if (url.contains(" ") || !url.contains(".")) {{
            // بحث جوجل
            url = "https://www.google.com/search?q=$url"
        }} else if (!url.startsWith("http")) {{
            // إضافة https
            url = "https://$url"
        }}
        
        session.loadUri(url)
    }}

    // اختصار Ctrl+G
    override fun dispatchKeyEvent(event: KeyEvent): Boolean {{
        if (event.action == KeyEvent.ACTION_DOWN && event.isCtrlPressed && event.keyCode == KeyEvent.KEYCODE_G) {{
            toggleGhostMode()
            return true
        }}
        return super.dispatchKeyEvent(event)
    }}

    private fun toggleGhostMode() {{
        isGhostMode = !isGhostMode
        if (isGhostMode) {{
            uiContainer.visibility = View.GONE
            window.decorView.systemUiVisibility = (View.SYSTEM_UI_FLAG_FULLSCREEN
                    or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                    or View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY)
        }} else {{
            uiContainer.visibility = View.VISIBLE
            window.decorView.systemUiVisibility = View.SYSTEM_UI_FLAG_VISIBLE
        }}
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
        name: B-Browser-MultiTab
        path: app/build/outputs/apk/release/*.apk
"""

# ==========================================
# التنفيذ
# ==========================================
print("🚀 بدء بناء المتصفح متعدد التبويبات (B-Browser Multi-Tab)...")

create_file("settings.gradle.kts", settings_gradle)
create_file("build.gradle.kts", build_gradle_root)
create_file("gradle.properties", gradle_properties)
create_file(".gitignore", gitignore)
create_file("app/build.gradle.kts", build_gradle_app)
create_file("app/src/main/AndroidManifest.xml", manifest)
create_file("app/src/main/res/xml/backup_rules.xml", backup_rules)
create_file("app/src/main/res/xml/data_extraction_rules.xml", data_extraction)

# إنشاء صفحة الويب المحلية
os.makedirs(ASSETS_DIR, exist_ok=True)
create_file(os.path.join(ASSETS_DIR, "home.html"), home_html)

# ملفات التصميم
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

print("✅ تم بناء نظام التبويبات بالكامل وإصلاح ملف الـ assets.")
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
    subprocess.run(["git", "commit", "-m", "Feature: Multi-Tabs, Google Search, Asset Fix"], check=False)
    
    print("🔧 توحيد اسم الفرع...")
    subprocess.run(["git", "branch", "-M", "main"], check=True)

    print("🚀 جاري الرفع إلى GitHub...")
    subprocess.run(["git", "push", "-u", "-f", "origin", "main"], check=True)
    
    print("\n✅✅ مبروك! التطبيق الآن متصفح حقيقي (Tabs + PC Mode).")
    print(f"🔗 {REPO_URL}/actions")

except subprocess.CalledProcessError as e:
    print(f"\n❌ خطأ: {e}")