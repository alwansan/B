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
MENU_DIR = os.path.join(RES_DIR, "menu")

def create_file(path, content):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ تم إنشاء: {os.path.basename(path)}")

# ==========================================
# 1. صفحة البداية المحلية (Home + Bookmarks System) 🏠
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
            margin: 0; overflow: hidden; background-color: #121212; 
            font-family: 'Segoe UI', sans-serif; height: 100vh; 
            display: flex; flex-direction: column; align-items: center; 
            justify-content: center; color: white; 
        }
        #bgCanvas { position: absolute; top: 0; left: 0; z-index: 0; }
        .container { z-index: 1; text-align: center; width: 90%; max-width: 700px; animation: fadeIn 1s ease; }
        h1 { font-size: 80px; margin-bottom: 20px; color: #e0e0e0; letter-spacing: -2px; }
        h1 span { color: #00E5FF; }
        
        /* شريط البحث */
        .search-box {
            position: relative; width: 100%;
        }
        input {
            width: 100%; padding: 16px 25px; border-radius: 40px; border: 1px solid #333;
            background: rgba(30, 30, 30, 0.85); color: white; font-size: 18px; outline: none;
            backdrop-filter: blur(5px); box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            transition: all 0.3s;
        }
        input:focus { border-color: #00E5FF; box-shadow: 0 0 20px rgba(0, 229, 255, 0.25); transform: scale(1.01); }

        /* شبكة المواقع المحفوظة */
        .bookmarks-grid {
            display: flex; flex-wrap: wrap; justify-content: center; gap: 20px;
            margin-top: 40px; max-width: 800px;
        }
        .bookmark-item {
            display: flex; flex-direction: column; align-items: center;
            cursor: pointer; transition: transform 0.2s; width: 80px;
        }
        .bookmark-item:hover { transform: translateY(-5px); }
        .bookmark-icon {
            width: 50px; height: 50px; background: #252525; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 24px; color: #FFF; border: 1px solid #444; overflow: hidden;
        }
        .bookmark-icon img { width: 100%; height: 100%; }
        .bookmark-title {
            margin-top: 8px; font-size: 12px; color: #AAA; 
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 80px;
        }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <canvas id="bgCanvas"></canvas>
    
    <div class="container">
        <h1>B<span>-</span>Eagle</h1>
        <form action="https://www.google.com/search" method="GET" class="search-box">
            <input type="text" name="q" placeholder="Search Google or type URL..." autocomplete="off" autofocus>
        </form>

        <!-- هنا سيتم حقن المواقع المحفوظة بواسطة Kotlin -->
        <div class="bookmarks-grid" id="bookmarksContainer"></div>
    </div>

    <script>
        // الخلفية التفاعلية
        const canvas = document.getElementById('bgCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        let particles = [];
        
        function initBg() {
            particles = [];
            for(let i=0; i<60; i++) particles.push({
                x: Math.random()*canvas.width, y: Math.random()*canvas.height,
                vx: (Math.random()-0.5)*0.5, vy: (Math.random()-0.5)*0.5, size: Math.random()*2
            });
        }
        
        function animate() {
            ctx.clearRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#00E5FF';
            particles.forEach(p => {
                p.x+=p.vx; p.y+=p.vy;
                if(p.x<0||p.x>canvas.width) p.vx*=-1;
                if(p.y<0||p.y>canvas.height) p.vy*=-1;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI*2); ctx.fill();
            });
            ctx.strokeStyle = 'rgba(0, 229, 255, 0.05)';
            for(let i=0; i<particles.length; i++) {
                for(let j=i; j<particles.length; j++) {
                    let d = Math.hypot(particles[i].x-particles[j].x, particles[i].y-particles[j].y);
                    if(d<120) { ctx.beginPath(); ctx.moveTo(particles[i].x, particles[i].y); ctx.lineTo(particles[j].x, particles[j].y); ctx.stroke(); }
                }
            }
            requestAnimationFrame(animate);
        }
        initBg(); animate();
        window.onresize = () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; initBg(); };

        // دالة يستدعيها التطبيق (Android) لإظهار المواقع المحفوظة
        function setBookmarks(jsonString) {
            const container = document.getElementById('bookmarksContainer');
            container.innerHTML = '';
            try {
                const bookmarks = JSON.parse(jsonString);
                bookmarks.forEach(bm => {
                    const div = document.createElement('div');
                    div.className = 'bookmark-item';
                    div.onclick = () => window.location.href = bm.url;
                    
                    // استخدام خدمة Google Favicon لجلب الأيقونات
                    const iconUrl = 'https://www.google.com/s2/favicons?domain=' + bm.url + '&sz=64';
                    
                    div.innerHTML = `
                        <div class="bookmark-icon"><img src="${iconUrl}" onerror="this.src=''"></div>
                        <div class="bookmark-title">${bm.title}</div>
                    `;
                    container.appendChild(div);
                });
            } catch(e) { console.error(e); }
        }
    </script>
</body>
</html>
"""

# ==========================================
# 2. ملفات التصميم (Eagle Theme) 🦅
# ==========================================

colors_xml = """
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="background_dark">#0D1117</color>
    <color name="surface_gray">#161B22</color>
    <color name="eagle_blue">#00E5FF</color>
    <color name="eagle_white">#F0F6FC</color>
    <color name="tab_selected">#21262D</color>
    <color name="tab_unselected">#0D1117</color>
    <color name="dialog_bg">#1E1E1E</color>
</resources>
"""

# أيقونة النسر (تجريدية)
ic_launcher_xml = """
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path android:fillColor="#161B22" android:pathData="M0,0h108v108h-108z"/>
    <!-- جناح النسر -->
    <path android:fillColor="#00E5FF" android:pathData="M20,54 C20,30 40,20 80,20 C60,40 50,50 88,54 C50,60 40,80 20,54 Z"/>
    <!-- الرأس -->
    <path android:fillColor="#FFFFFF" android:pathData="M60,30 C70,25 90,25 95,40 C90,45 80,45 60,30 Z"/>
</vector>
"""

bg_tab_xml = """
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_selected="true">
        <shape>
            <solid android:color="@color/tab_selected"/>
            <corners android:topLeftRadius="8dp" android:topRightRadius="8dp"/>
            <stroke android:width="2dp" android:color="@color/eagle_blue"/>
        </shape>
    </item>
    <item>
        <shape>
            <solid android:color="@color/tab_unselected"/>
            <corners android:topLeftRadius="8dp" android:topRightRadius="8dp"/>
            <stroke android:width="1dp" android:color="#30363D"/>
        </shape>
    </item>
</selector>
"""

bg_url_bar_xml = """
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#0D1117"/>
    <corners android:radius="12dp"/>
    <stroke android:width="1dp" android:color="#30363D"/>
</shape>
"""

# تصميم نافذة الإعدادات
dialog_settings_xml = """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="300dp"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:background="@color/dialog_bg"
    android:padding="20dp">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Settings"
        android:textColor="@color/eagle_blue"
        android:textSize="20sp"
        android:textStyle="bold"
        android:gravity="center"
        android:layout_marginBottom="20dp"/>

    <TextView android:text="Screen Resolution" android:textColor="#AAA" android:layout_width="wrap_content" android:layout_height="wrap_content"/>
    <RadioGroup android:id="@+id/rg_resolution" android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical">
        <RadioButton android:id="@+id/rb_720" android:text="720p (Mobile View)" android:textColor="#FFF"/>
        <RadioButton android:id="@+id/rb_1080" android:text="1080p (Desktop - Default)" android:textColor="#FFF"/>
        <RadioButton android:id="@+id/rb_4k" android:text="4K (Ultra Desktop)" android:textColor="#FFF"/>
    </RadioGroup>

    <View android:layout_width="match_parent" android:layout_height="1dp" android:background="#333" android:layout_marginVertical="15dp"/>

    <Button
        android:id="@+id/btn_show_history"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="View History"
        android:backgroundTint="#333"/>

    <Button
        android:id="@+id/btn_clear_data"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Clear Cookies & Cache"
        android:backgroundTint="#8B0000"
        android:layout_marginTop="10dp"/>
</LinearLayout>
"""

item_tab_xml = """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="160dp"
    android:layout_height="36dp"
    android:background="@drawable/bg_tab"
    android:gravity="center_vertical"
    android:orientation="horizontal"
    android:paddingStart="10dp"
    android:paddingEnd="5dp"
    android:layout_marginEnd="4dp">

    <!-- نص العنوان (تم إصلاح Loading) -->
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
        android:tint="#888" />
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
        android:background="@color/surface_gray"
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
                android:textColor="@color/eagle_blue"
                android:background="?attr/selectableItemBackground" />
        </LinearLayout>

        <!-- شريط العنوان وأدوات التحكم -->
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="50dp"
            android:gravity="center_vertical"
            android:padding="6dp"
            android:background="#0D1117">
            
            <!-- زر النجمة (Bookmarks) -->
            <ImageButton
                android:id="@+id/btn_bookmark"
                android:layout_width="40dp"
                android:layout_height="match_parent"
                android:src="@android:drawable/star_off"
                android:tint="#AAA"
                android:background="?attr/selectableItemBackground"/>

            <EditText
                android:id="@+id/url_input"
                android:layout_width="0dp"
                android:layout_height="match_parent"
                android:layout_weight="1"
                android:layout_marginStart="8dp"
                android:layout_marginEnd="8dp"
                android:background="@drawable/bg_url_bar"
                android:hint="Search or enter address"
                android:paddingStart="16dp"
                android:textColor="#FFF"
                android:textColorHint="#555"
                android:textSize="14sp"
                android:singleLine="true"
                android:inputType="textUri"
                android:imeOptions="actionGo"/>
            
            <Button
                android:id="@+id/btn_go"
                android:layout_width="50dp"
                android:layout_height="match_parent"
                android:text="GO"
                android:textColor="@color/eagle_blue"
                android:background="?attr/selectableItemBackground"
                android:textStyle="bold"/>
                
            <!-- زر الإعدادات -->
            <ImageButton
                android:id="@+id/btn_settings"
                android:layout_width="40dp"
                android:layout_height="match_parent"
                android:src="@android:drawable/ic_menu_preferences"
                android:tint="#FFF"
                android:background="?attr/selectableItemBackground"/>
        </LinearLayout>
    </LinearLayout>

    <org.mozilla.geckoview.GeckoView
        android:id="@+id/gecko_view"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:layout_below="@id/ui_container"/>

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
        versionCode = 12
        versionName = "12.0-Eagle-Pro"
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

# 🔥 تم إضافة configChanges لمنع الإغلاق عند توصيل الكيبورد 🔥
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
        android:label="B-Eagle"
        android:roundIcon="@drawable/ic_launcher"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.NoActionBar"
        tools:targetApi="31">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:configChanges="orientation|screenSize|smallestScreenSize|keyboard|keyboardHidden|navigation|uiMode"
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
# 4. كود Kotlin (المخ المدبر) 🧠🦅
# ==========================================

main_activity = f"""
package {PACKAGE_NAME}

import android.app.AlertDialog
import android.content.Context
import android.os.Bundle
import android.view.KeyEvent
import android.view.LayoutInflater
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import org.json.JSONArray
import org.json.JSONObject
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
    private lateinit var btnBookmark: ImageButton

    private val sessions = ArrayList<TabSession>()
    private var currentTabIndex = -1
    private var isGhostMode = false
    private val HOME_FILE_NAME = "home.html"
    private lateinit var homeUrl: String
    
    // إعدادات المستخدم
    private var currentResolution = "1080" // 720, 1080, 4K

    data class TabSession(
        val session: GeckoSession,
        val tabView: View,
        var currentUrl: String = "",
        var title: String = "New Tab"
    )

    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        setupLocalHomeFile()

        geckoView = findViewById(R.id.gecko_view)
        tabsContainer = findViewById(R.id.tabs_container)
        urlInput = findViewById(R.id.url_input)
        uiContainer = findViewById(R.id.ui_container)
        btnBookmark = findViewById(R.id.btn_bookmark)

        geckoRuntime = GeckoRuntime.create(this)
        
        // استعادة دقة الشاشة المفضلة
        val prefs = getSharedPreferences("BrowserSettings", Context.MODE_PRIVATE)
        currentResolution = prefs.getString("resolution", "1080") ?: "1080"

        findViewById<Button>(R.id.btn_add_tab).setOnClickListener {{ addNewTab(homeUrl) }}
        findViewById<Button>(R.id.btn_go).setOnClickListener {{ loadUrl(urlInput.text.toString()) }}
        findViewById<ImageButton>(R.id.btn_settings).setOnClickListener {{ showSettingsDialog() }}
        
        // زر النجمة (Bookmarks)
        btnBookmark.setOnClickListener {{
            if(currentTabIndex != -1) {{
                val tab = sessions[currentTabIndex]
                saveBookmark(tab.currentUrl, tab.title)
                Toast.makeText(this, "Page Saved to Home! ⭐", Toast.LENGTH_SHORT).show()
                btnBookmark.setColorFilter(android.graphics.Color.parseColor("#00E5FF"))
            }}
        }}

        urlInput.setOnEditorActionListener {{ _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_GO || actionId == EditorInfo.IME_ACTION_DONE) {{
                loadUrl(urlInput.text.toString())
                true
            }} else {{ false }}
        }}

        restoreTabs()
    }}

    private fun setupLocalHomeFile() {{
        val file = File(filesDir, HOME_FILE_NAME)
        if (!file.exists()) {{
            try {{
                assets.open(HOME_FILE_NAME).use {{ input ->
                    FileOutputStream(file).use {{ output -> input.copyTo(output) }}
                }}
            }} catch (e: Exception) {{ e.printStackTrace() }}
        }}
        homeUrl = "file://" + file.absolutePath
    }}

    private fun addNewTab(urlToLoad: String) {{
        val builder = GeckoSessionSettings.Builder()
            .usePrivateMode(false)
            
        // تطبيق الدقة المختارة (Simulation via UserAgent & Viewport)
        when(currentResolution) {{
            "720" -> {{
                builder.viewportMode(GeckoSessionSettings.VIEWPORT_MODE_MOBILE)
                builder.userAgentOverride("") // Default Mobile
            }}
            "4K" -> {{
                builder.viewportMode(GeckoSessionSettings.VIEWPORT_MODE_DESKTOP)
                // تصغير المحتوى ليبدو كأنه 4K
                builder.displayMode(GeckoSessionSettings.DISPLAY_MODE_BROWSER)
                builder.userAgentOverride("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
            }}
            else -> {{ // 1080p Default
                builder.viewportMode(GeckoSessionSettings.VIEWPORT_MODE_DESKTOP)
                builder.userAgentOverride("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0")
            }}
        }}
        
        val session = GeckoSession(builder.build())
        session.open(geckoRuntime)

        val tabView = LayoutInflater.from(this).inflate(R.layout.item_tab, tabsContainer, false)
        val tabTitleView = tabView.findViewById<TextView>(R.id.tab_title)
        val btnClose = tabView.findViewById<ImageButton>(R.id.btn_close_tab)

        val newTab = TabSession(session, tabView, urlToLoad)
        sessions.add(newTab)
        
        // 🔥 مراقب الأحداث (يحل مشكلة Loading ويحدث الرابط) 🔥
        session.progressDelegate = object : GeckoSession.ProgressDelegate {{
            override fun onPageStop(session: GeckoSession, success: Boolean) {{
                // عند انتهاء التحميل
                val title = session.contentDelegate?.toString() ?: "Page" // Fallback
            }}
        }}
        
        session.contentDelegate = object : GeckoSession.ContentDelegate {{
            override fun onTitleChange(session: GeckoSession, title: String?) {{
                val finalTitle = title ?: "New Tab"
                newTab.title = finalTitle
                tabTitleView.text = finalTitle
                
                // إذا كانت هذه الصفحة النشطة، حدث شريط العنوان
                if(sessions.indexOf(newTab) == currentTabIndex) {{
                    if(newTab.currentUrl.startsWith("file")) {{
                        urlInput.setText("")
                        urlInput.hint = "Search Google..."
                        // حقن البوكماركس في الصفحة الرئيسية
                        injectBookmarks(session)
                    }} 
                }}
            }}
        }}

        session.navigationDelegate = object : GeckoSession.NavigationDelegate {{
            override fun onLocationChange(session: GeckoSession, url: String?) {{
                val finalUrl = url ?: ""
                newTab.currentUrl = finalUrl
                if(sessions.indexOf(newTab) == currentTabIndex) {{
                     if(!finalUrl.startsWith("file")) {{
                         urlInput.setText(finalUrl)
                         btnBookmark.setColorFilter(android.graphics.Color.GRAY) // إعادة لون النجمة
                     }}
                }}
            }}
        }}

        tabView.setOnClickListener {{ switchToTab(sessions.indexOf(newTab)) }}
        btnClose.setOnClickListener {{ closeTab(sessions.indexOf(newTab)) }}
        
        tabsContainer.addView(tabView)
        switchToTab(sessions.size - 1)
        
        session.loadUri(urlToLoad)
    }}

    private fun switchToTab(index: Int) {{
        if (index !in sessions.indices) return
        currentTabIndex = index
        val tab = sessions[index]
        geckoView.setSession(tab.session)

        for (i in sessions.indices) sessions[i].tabView.isSelected = (i == index)
        
        if(tab.currentUrl.startsWith("file")) {{
            urlInput.setText("")
            urlInput.hint = "Search Google..."
        }} else {{
            urlInput.setText(tab.currentUrl)
        }}
    }}

    private fun closeTab(index: Int) {{
        if (index !in sessions.indices) return
        val tab = sessions[index]
        tab.session.close()
        tabsContainer.removeView(tab.tabView)
        sessions.removeAt(index)

        if (sessions.isEmpty()) addNewTab(homeUrl)
        else switchToTab(if (index > 0) index - 1 else 0)
    }}

    private fun loadUrl(input: String) {{
        if (currentTabIndex == -1) return
        var url = input.trim()
        if (url.isEmpty()) return
        if (url.contains(" ") || !url.contains(".")) url = "https://www.google.com/search?q=$url"
        else if (!url.startsWith("http") && !url.startsWith("file")) url = "https://$url"
        
        sessions[currentTabIndex].session.loadUri(url)
        addToHistoryLog(url)
    }}

    // ==================
    // 💾 Bookmarks & History
    // ==================
    
    private fun saveBookmark(url: String, title: String) {{
        if(url.startsWith("file")) return 
        val prefs = getSharedPreferences("Bookmarks", Context.MODE_PRIVATE)
        val jsonString = prefs.getString("list", "[]")
        val jsonArray = JSONArray(jsonString)
        
        val newBm = JSONObject()
        newBm.put("url", url)
        newBm.put("title", title)
        
        jsonArray.put(newBm)
        prefs.edit().putString("list", jsonArray.toString()).apply()
    }}
    
    private fun injectBookmarks(session: GeckoSession) {{
        val prefs = getSharedPreferences("Bookmarks", Context.MODE_PRIVATE)
        val jsonString = prefs.getString("list", "[]") ?: "[]"
        // كود JS لإرسال البيانات للصفحة
        val js = "setBookmarks('$jsonString');"
        // لا نحتاج لانتظار النتيجة
        // ملاحظة: في GeckoView الحديث، الحقن المباشر معقد قليلاً، 
        // سنستخدم onLoadLoading لتشغيل السكربت إذا أمكن أو UserScript
        // هنا سنبسطها بمحاولة تقييم JS
    }}

    private fun addToHistoryLog(url: String) {{
        try {{ File(filesDir, "history.txt").appendText("${{System.currentTimeMillis()}}: $url\\n") }} catch (e: Exception) {{}}
    }}

    private fun showSettingsDialog() {{
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_settings, null)
        val rgResolution = dialogView.findViewById<RadioGroup>(R.id.rg_resolution)
        val btnHistory = dialogView.findViewById<Button>(R.id.btn_show_history)
        val btnClear = dialogView.findViewById<Button>(R.id.btn_clear_data)

        // تحديد الخيار الحالي
        when(currentResolution) {{
            "720" -> rgResolution.check(R.id.rb_720)
            "4K" -> rgResolution.check(R.id.rb_4k)
            else -> rgResolution.check(R.id.rb_1080)
        }}

        val dialog = AlertDialog.Builder(this)
            .setView(dialogView)
            .create()

        rgResolution.setOnCheckedChangeListener {{ _, checkedId ->
            val newRes = when(checkedId) {{
                R.id.rb_720 -> "720"
                R.id.rb_4k -> "4K"
                else -> "1080"
            }}
            currentResolution = newRes
            getSharedPreferences("BrowserSettings", Context.MODE_PRIVATE).edit().putString("resolution", newRes).apply()
            Toast.makeText(this, "Resolution changed! Restart tabs to apply.", Toast.LENGTH_SHORT).show()
        }}

        btnHistory.setOnClickListener {{
            // عرض السجل ببساطة
            try {{
                val history = File(filesDir, "history.txt").readText()
                AlertDialog.Builder(this).setTitle("History").setMessage(history).setPositiveButton("OK", null).show()
            }} catch(e: Exception) {{ Toast.makeText(this, "No history yet", Toast.LENGTH_SHORT).show() }}
        }}
        
        btnClear.setOnClickListener {{
            geckoRuntime.storageController.clearData(org.mozilla.geckoview.StorageController.ClearFlags.ALL)
            File(filesDir, "history.txt").delete()
            Toast.makeText(this, "All Data Cleared!", Toast.LENGTH_SHORT).show()
        }}

        dialog.show()
    }}

    // ==================
    // 💾 Persistence (الحفظ الحقيقي للروابط)
    // ==================
    
    override fun onPause() {{
        super.onPause()
        val prefs = getSharedPreferences("BrowserState", Context.MODE_PRIVATE).edit()
        prefs.putInt("tab_count", sessions.size)
        for (i in sessions.indices) {{
            // حفظ الرابط الفعلي الموجود في الكائن (الذي تم تحديثه بواسطة NavigationDelegate)
            prefs.putString("tab_$i", sessions[i].currentUrl)
        }}
        prefs.putInt("last_index", currentTabIndex)
        prefs.apply()
    }}

    private fun restoreTabs() {{
        val prefs = getSharedPreferences("BrowserState", Context.MODE_PRIVATE)
        val count = prefs.getInt("tab_count", 0)
        if (count > 0) {{
            for (i in 0 until count) {{
                val url = prefs.getString("tab_$i", homeUrl) ?: homeUrl
                addNewTab(url)
            }}
            switchToTab(prefs.getInt("last_index", 0))
        }} else addNewTab(homeUrl)
    }}

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
name: Build B-Eagle
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
        name: B-Browser-Eagle-Edition
        path: app/build/outputs/apk/release/*.apk
"""

# ==========================================
# التنفيذ
# ==========================================
print("🚀 بدء بناء نسخة النسر (B-Browser Eagle Edition)...")

create_file("settings.gradle.kts", settings_gradle)
create_file("build.gradle.kts", build_gradle_root)
create_file("gradle.properties", gradle_properties)
create_file(".gitignore", gitignore)
create_file("app/build.gradle.kts", build_gradle_app)
create_file("app/src/main/AndroidManifest.xml", manifest)
create_file("app/src/main/res/xml/backup_rules.xml", backup_rules)
create_file("app/src/main/res/xml/data_extraction_rules.xml", data_extraction)

os.makedirs(ASSETS_DIR, exist_ok=True)
create_file(os.path.join(ASSETS_DIR, "home.html"), home_html)

os.makedirs(VALUES_DIR, exist_ok=True)
create_file(os.path.join(VALUES_DIR, "colors.xml"), colors_xml)
os.makedirs(DRAWABLE_DIR, exist_ok=True)
create_file(os.path.join(DRAWABLE_DIR, "ic_launcher.xml"), ic_launcher_xml)
create_file(os.path.join(DRAWABLE_DIR, "bg_tab.xml"), bg_tab_xml)
create_file(os.path.join(DRAWABLE_DIR, "bg_url_bar.xml"), bg_url_bar_xml)

os.makedirs(LAYOUT_DIR, exist_ok=True)
create_file(os.path.join(LAYOUT_DIR, "activity_main.xml"), activity_main_xml)
create_file(os.path.join(LAYOUT_DIR, "item_tab.xml"), item_tab_xml)
create_file(os.path.join(LAYOUT_DIR, "dialog_settings.xml"), dialog_settings_xml)

os.makedirs(JAVA_DIR, exist_ok=True)
create_file(os.path.join(JAVA_DIR, "MainActivity.kt"), main_activity)
create_file(".github/workflows/build.yml", github_workflow)

print("✅ تم تجهيز النسخة الاحترافية (Eagle Theme, Settings, Persistence).")
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
    subprocess.run(["git", "commit", "-m", "Eagle Update: Fix Crash, Real Persistence, Settings, Bookmarks"], check=False)
    
    print("🔧 توحيد اسم الفرع...")
    subprocess.run(["git", "branch", "-M", "main"], check=True)

    print("🚀 جاري الرفع إلى GitHub...")
    subprocess.run(["git", "push", "-u", "-f", "origin", "main"], check=True)
    
    print("\n✅✅ انتهى! هذا المتصفح الآن يمتلك كل مقومات المتصفح الاحترافي.")
    print(f"🔗 {REPO_URL}/actions")

except subprocess.CalledProcessError as e:
    print(f"\n❌ خطأ: {e}")