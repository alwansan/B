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
ASSETS_DIR = os.path.join(SRC_MAIN, "assets") # مجلد ملفات الويب المحلية
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
# 1. الصفحة الرئيسية التفاعلية (HTML/JS) 🎨
# ==========================================
# هذه الصفحة ستعمل كـ "Local Home Page" مع تأثيرات جافا سكريبت
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
            padding: 0;
            overflow: hidden;
            background-color: #121212; /* رمادي داكن جداً */
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        
        #canvas-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
        }

        .content {
            z-index: 1;
            text-align: center;
            width: 100%;
            max-width: 600px;
            animation: fadeIn 1.5s ease-in-out;
        }

        h1 {
            color: #E0E0E0; /* رمادي فاتح */
            font-size: 80px;
            margin-bottom: 20px;
            letter-spacing: -2px;
            font-weight: bold;
            text-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }

        .search-box {
            display: flex;
            background: rgba(255, 255, 255, 0.1); /* شفاف */
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 30px;
            padding: 5px 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            transition: all 0.3s ease;
        }

        .search-box:hover, .search-box:focus-within {
            background: rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(0, 229, 255, 0.2); /* توهج نيون خفيف */
            transform: scale(1.02);
        }

        input {
            flex: 1;
            background: transparent;
            border: none;
            color: #FFFFFF;
            font-size: 18px;
            padding: 10px;
            outline: none;
        }

        button {
            background: transparent;
            border: none;
            color: #00E5FF;
            font-size: 18px;
            cursor: pointer;
            font-weight: bold;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

    <div id="canvas-container"><canvas id="bgCanvas"></canvas></div>

    <div class="content">
        <h1>Google</h1>
        <form action="https://www.google.com/search" method="GET" class="search-box">
            <input type="text" name="q" placeholder="Search the web..." autocomplete="off" autofocus>
            <button type="submit">🔍</button>
        </form>
    </div>

    <script>
        // تأثير الخلفية التفاعلية (Particles)
        const canvas = document.getElementById('bgCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        let particlesArray;

        // تفاعل الماوس
        let mouse = {
            x: null,
            y: null,
            radius: (canvas.height/80) * (canvas.width/80)
        }

        window.addEventListener('mousemove', function(event) {
            mouse.x = event.x;
            mouse.y = event.y;
        });
        
        // دعم اللمس للهاتف
        window.addEventListener('touchmove', function(event) {
            mouse.x = event.touches[0].clientX;
            mouse.y = event.touches[0].clientY;
        });

        class Particle {
            constructor(x, y, directionX, directionY, size, color) {
                this.x = x;
                this.y = y;
                this.directionX = directionX;
                this.directionY = directionY;
                this.size = size;
                this.color = color;
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
                ctx.fillStyle = '#00E5FF'; // لون النيون
                ctx.fill();
            }
            update() {
                if (this.x > canvas.width || this.x < 0) this.directionX = -this.directionX;
                if (this.y > canvas.height || this.y < 0) this.directionY = -this.directionY;

                // تفاعل الماوس
                let dx = mouse.x - this.x;
                let dy = mouse.y - this.y;
                let distance = Math.sqrt(dx*dx + dy*dy);
                
                if (distance < mouse.radius + this.size) {
                    if (mouse.x < this.x && this.x < canvas.width - this.size * 10) this.x += 10;
                    if (mouse.x > this.x && this.x > this.size * 10) this.x -= 10;
                    if (mouse.y < this.y && this.y < canvas.height - this.size * 10) this.y += 10;
                    if (mouse.y > this.y && this.y > this.size * 10) this.y -= 10;
                }
                
                this.x += this.directionX;
                this.y += this.directionY;
                this.draw();
            }
        }

        function init() {
            particlesArray = [];
            let numberOfParticles = (canvas.height * canvas.width) / 9000;
            for (let i = 0; i < numberOfParticles; i++) {
                let size = (Math.random() * 3) + 1;
                let x = (Math.random() * ((innerWidth - size * 2) - (size * 2)) + size * 2);
                let y = (Math.random() * ((innerHeight - size * 2) - (size * 2)) + size * 2);
                let directionX = (Math.random() * 2) - 1;
                let directionY = (Math.random() * 2) - 1;
                let color = '#8C5523';

                particlesArray.push(new Particle(x, y, directionX, directionY, size, color));
            }
        }

        function connect() {
            let opacityValue = 1;
            for (let a = 0; a < particlesArray.length; a++) {
                for (let b = a; b < particlesArray.length; b++) {
                    let distance = ((particlesArray[a].x - particlesArray[b].x) * (particlesArray[a].x - particlesArray[b].x)) + 
                                   ((particlesArray[a].y - particlesArray[b].y) * (particlesArray[a].y - particlesArray[b].y));
                    if (distance < (canvas.width/7) * (canvas.height/7)) {
                        opacityValue = 1 - (distance/20000);
                        ctx.strokeStyle = 'rgba(150, 150, 150,' + opacityValue + ')'; // خطوط رمادية
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                        ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                        ctx.stroke();
                    }
                }
            }
        }

        function animate() {
            requestAnimationFrame(animate);
            ctx.clearRect(0, 0, innerWidth, innerHeight);
            for (let i = 0; i < particlesArray.length; i++) {
                particlesArray[i].update();
            }
            connect();
        }

        window.addEventListener('resize', function() {
            canvas.width = innerWidth;
            canvas.height = innerHeight;
            mouse.radius = (canvas.height/80) * (canvas.width/80);
            init();
        });

        init();
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
    <color name="neon_blue">#00E5FF</color>
    <color name="text_white">#FFFFFF</color>
</resources>
"""

ic_launcher_xml = """
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path android:fillColor="#1F1F1F" android:pathData="M0,0h108v108h-108z"/>
    <path android:fillColor="#00E5FF" android:pathData="M30,30h48v48h-48z"/>
    <path android:fillColor="#FFFFFF" android:pathData="M40,40h28v28h-28z"/>
</vector>
"""

# خلفية شريط العنوان الأصلي (للبحث الثانوي)
bg_search_bar_xml = """
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/surface_gray"/>
    <corners android:radius="12dp"/>
    <stroke android:width="1dp" android:color="#33FFFFFF"/>
</shape>
"""

# تصميم الواجهة (مع الشريط القابل للإخفاء)
activity_main_xml = """
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/background_dark">

    <org.mozilla.geckoview.GeckoView
        android:id="@+id/gecko_view"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />

    <!-- الشريط العلوي الذي سيختفي عند ضغط Ctrl+G -->
    <LinearLayout
        android:id="@+id/top_bar"
        android:layout_width="match_parent"
        android:layout_height="50dp"
        android:layout_alignParentTop="true"
        android:layout_margin="10dp"
        android:background="@drawable/bg_search_bar"
        android:elevation="8dp"
        android:gravity="center_vertical"
        android:orientation="horizontal"
        android:paddingStart="12dp"
        android:paddingEnd="12dp"
        android:visibility="visible">

        <EditText
            android:id="@+id/url_input"
            android:layout_width="0dp"
            android:layout_height="match_parent"
            android:layout_weight="1"
            android:background="@null"
            android:hint="Ctrl+G to hide this bar..."
            android:textColor="@color/text_white"
            android:textColorHint="#80FFFFFF"
            android:inputType="textUri"
            android:imeOptions="actionGo"
            android:textSize="14sp"
            android:singleLine="true" />
            
        <Button
            android:id="@+id/btn_go"
            android:layout_width="wrap_content"
            android:layout_height="40dp"
            android:text="GO"
            android:textColor="#000000"
            android:backgroundTint="@color/neon_blue"/>
    </LinearLayout>

</RelativeLayout>
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
        versionCode = 9
        versionName = "9.0-Ghost-Mode"
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

    <!-- السماح بتدوير الشاشة -->
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
# 4. كود Kotlin (المنطق: اختصارات الكيبورد + الصفحة الرئيسية)
# ==========================================

main_activity = f"""
package {PACKAGE_NAME}

import android.os.Bundle
import android.view.KeyEvent
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
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
    private lateinit var topBar: LinearLayout
    private var isUiHidden = false

    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        geckoView = findViewById(R.id.gecko_view)
        urlInput = findViewById(R.id.url_input)
        btnGo = findViewById(R.id.btn_go)
        topBar = findViewById(R.id.top_bar)

        geckoRuntime = GeckoRuntime.create(this)
        
        val settings = GeckoSessionSettings.Builder()
            .usePrivateMode(false)
            // إجبار المتصفح على دقة سطح المكتب (تقريباً 1080p عرض)
            .viewportMode(GeckoSessionSettings.VIEWPORT_MODE_DESKTOP)
            .userAgentOverride("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
            .build()

        geckoSession = GeckoSession(settings)
        geckoSession.open(geckoRuntime)
        geckoView.setSession(geckoSession)

        // 🔥 تحميل الصفحة المحلية التفاعلية (Google + Particles) 🔥
        geckoSession.loadUri("file:///android_asset/home.html")

        btnGo.setOnClickListener {{
            loadUrl(urlInput.text.toString())
        }}

        urlInput.setOnEditorActionListener {{ _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_GO || actionId == EditorInfo.IME_ACTION_DONE) {{
                loadUrl(urlInput.text.toString())
                true
            }} else {{
                false
            }}
        }}
    }}

    private fun loadUrl(url: String) {{
        var finalUrl = url.trim()
        if (finalUrl.isNotEmpty()) {{
            if (!finalUrl.startsWith("http") && !finalUrl.startsWith("file")) {{
                finalUrl = "https://$finalUrl"
            }}
            geckoSession.loadUri(finalUrl)
        }}
    }}

    // ⚡ التعامل مع اختصارات الكيبورد (Ctrl + G) ⚡
    override fun dispatchKeyEvent(event: KeyEvent): Boolean {{
        if (event.action == KeyEvent.ACTION_DOWN) {{
            // التحقق من ضغط Ctrl + G
            if (event.keyCode == KeyEvent.KEYCODE_G && event.isCtrlPressed) {{
                toggleUi()
                return true
            }}
        }}
        return super.dispatchKeyEvent(event)
    }}

    private fun toggleUi() {{
        isUiHidden = !isUiHidden
        if (isUiHidden) {{
            // إخفاء كل شيء والبقاء على المتصفح فقط
            topBar.visibility = View.GONE
            // إخفاء شريط الحالة العلوي (Full Screen)
            window.decorView.systemUiVisibility = (View.SYSTEM_UI_FLAG_FULLSCREEN
                    or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                    or View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY)
        }} else {{
            // إظهار الشريط
            topBar.visibility = View.VISIBLE
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
        name: B-Browser-Ultimate
        path: app/build/outputs/apk/release/*.apk
"""

# ==========================================
# التنفيذ
# ==========================================
print("🚀 بدء بناء النسخة التفاعلية (Interactive + Ghost Mode)...")

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
create_file(os.path.join(DRAWABLE_DIR, "bg_search_bar.xml"), bg_search_bar_xml)
os.makedirs(LAYOUT_DIR, exist_ok=True)
create_file(os.path.join(LAYOUT_DIR, "activity_main.xml"), activity_main_xml)

os.makedirs(JAVA_DIR, exist_ok=True)
create_file(os.path.join(JAVA_DIR, "MainActivity.kt"), main_activity)
create_file(".github/workflows/build.yml", github_workflow)

print("✅ تم إضافة الصفحة التفاعلية واختصار Ctrl+G.")
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
    subprocess.run(["git", "commit", "-m", "New Feature: Interactive Home + Ghost Mode (Ctrl+G)"], check=False)
    
    print("🔧 توحيد اسم الفرع...")
    subprocess.run(["git", "branch", "-M", "main"], check=True)

    print("🚀 جاري الرفع إلى GitHub...")
    subprocess.run(["git", "push", "-u", "-f", "origin", "main"], check=True)
    
    print("\n✅✅ استمتع بالمتصفح الجديد! الصفحة الرئيسية ستكون مذهلة.")
    print(f"🔗 {REPO_URL}/actions")

except subprocess.CalledProcessError as e:
    print(f"\n❌ خطأ: {e}")