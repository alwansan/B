import os
import subprocess
import shutil

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
# 1. معالجة الأيقونة 🦅
# ==========================================
def setup_icon():
    # تنظيف أيقونات قديمة لتجنب duplicate resources
    xml_icon = os.path.join(DRAWABLE_DIR, "ic_launcher.xml")
    png_icon = os.path.join(DRAWABLE_DIR, "ic_launcher.png")
    
    custom_icon = "icon.png"
    
    if os.path.exists(custom_icon):
        print("🦅 استخدام الصورة المخصصة icon.png...")
        if os.path.exists(xml_icon): os.remove(xml_icon)
        shutil.copy(custom_icon, png_icon)
        return True
    else:
        print("🦅 استخدام أيقونة النسر الافتراضية...")
        if os.path.exists(png_icon): os.remove(png_icon)
        create_file(xml_icon, vector_eagle_xml)
        return False

# تصميم النسر (Default)
vector_eagle_xml = """
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
    <path android:fillColor="#151515" android:pathData="M0,0h24v24h-24z"/>
    <path android:fillColor="#00E5FF" android:pathData="M12,2L2,12h3v8h6v-6h2v6h6v-8h3L12,2z"/>
</vector>
"""

# ==========================================
# 2. واجهة المستخدم (Opera GX Style) 🎨
# ==========================================

colors_xml = """
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="bg_main">#0d0e12</color>
    <color name="bg_secondary">#181920</color>
    <color name="accent_neon">#00E5FF</color>
    <color name="accent_red">#FA2E4D</color>
    <color name="text_primary">#FFFFFF</color>
    <color name="tab_active">#1F2029</color>
    <color name="tab_inactive">#0d0e12</color>
</resources>
"""

bg_tab_xml = """
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_selected="true">
        <shape>
            <solid android:color="@color/tab_active"/>
            <corners android:topLeftRadius="8dp" android:topRightRadius="8dp"/>
        </shape>
    </item>
    <item>
        <shape>
            <solid android:color="@color/tab_inactive"/>
            <corners android:topLeftRadius="8dp" android:topRightRadius="8dp"/>
        </shape>
    </item>
</selector>
"""

bg_url_bar_xml = """
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#1F2029"/>
    <corners android:radius="6dp"/>
    <stroke android:width="1dp" android:color="#333"/>
</shape>
"""

# تصميم القائمة المنبثقة (Bookmarks/History)
dialog_bookmarks_xml = """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="450dp"
    android:layout_height="350dp"
    android:orientation="vertical"
    android:background="@color/bg_secondary"
    android:padding="16dp">

    <TextView
        android:id="@+id/dialog_title"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Library"
        android:textColor="@color/accent_neon"
        android:textSize="20sp"
        android:textStyle="bold"
        android:gravity="center"
        android:paddingBottom="12dp"/>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:weightSum="2"
        android:layout_marginBottom="10dp">
        
        <Button
            android:id="@+id/btn_view_bookmarks"
            android:layout_width="0dp"
            android:layout_height="45dp"
            android:layout_weight="1"
            android:text="⭐ Bookmarks"
            android:backgroundTint="#2A2B36"
            android:textColor="#FFF"
            android:layout_marginEnd="5dp"/>
            
        <Button
            android:id="@+id/btn_view_history"
            android:layout_width="0dp"
            android:layout_height="45dp"
            android:layout_weight="1"
            android:text="🕒 History"
            android:backgroundTint="#2A2B36"
            android:textColor="#FFF"
            android:layout_marginStart="5dp"/>
    </LinearLayout>

    <ListView
        android:id="@+id/list_data"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:divider="#2A2B36"
        android:dividerHeight="1dp"
        android:background="@color/bg_main"/>

    <Button
        android:id="@+id/btn_clear_history"
        android:layout_width="match_parent"
        android:layout_height="40dp"
        android:text="Clear History"
        android:textColor="#FFF"
        android:backgroundTint="@color/accent_red"
        android:visibility="gone"
        android:layout_marginTop="10dp"/>
</LinearLayout>
"""

# تصميم نافذة الإعدادات
dialog_settings_xml = """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="350dp"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:background="@color/bg_secondary"
    android:padding="20dp">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Settings"
        android:textColor="@color/accent_neon"
        android:textSize="22sp"
        android:textStyle="bold"
        android:gravity="center"
        android:layout_marginBottom="20dp"/>

    <TextView android:text="Viewport Mode" android:textColor="#888" android:layout_width="wrap_content" android:layout_height="wrap_content"/>
    
    <RadioGroup android:id="@+id/rg_resolution" android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:layout_marginTop="10dp">
        <RadioButton android:id="@+id/rb_1080" android:text="Desktop (1080p)" android:textColor="#FFF" android:buttonTint="@color/accent_neon"/>
        <RadioButton android:id="@+id/rb_4k" android:text="Ultra (4K)" android:textColor="#FFF" android:buttonTint="@color/accent_neon"/>
        <RadioButton android:id="@+id/rb_720" android:text="Mobile (720p)" android:textColor="#FFF" android:buttonTint="@color/accent_neon"/>
    </RadioGroup>

    <View android:layout_width="match_parent" android:layout_height="1dp" android:background="#333" android:layout_marginVertical="20dp"/>

    <Button
        android:id="@+id/btn_clear_data"
        android:layout_width="match_parent"
        android:layout_height="50dp"
        android:text="Clear All Data"
        android:backgroundTint="@color/accent_red"/>
</LinearLayout>
"""

item_list_row_xml = """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="12dp">
    <TextView
        android:id="@+id/row_title"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Title"
        android:textColor="#FFF"
        android:textStyle="bold"
        android:singleLine="true"/>
    <TextView
        android:id="@+id/row_url"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="url"
        android:textColor="#888"
        android:textSize="12sp"
        android:singleLine="true"/>
</LinearLayout>
"""

item_tab_xml = """
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="180dp"
    android:layout_height="38dp"
    android:background="@drawable/bg_tab"
    android:layout_marginEnd="2dp">
    
    <!-- مؤشر النيون -->
    <View
        android:id="@+id/tab_indicator"
        android:layout_width="match_parent"
        android:layout_height="2dp"
        android:layout_alignParentBottom="true"
        android:background="@color/accent_neon"
        android:visibility="invisible"/>
        
    <TextView
        android:id="@+id/tab_title"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_centerVertical="true"
        android:layout_toStartOf="@id/btn_close_tab"
        android:layout_marginStart="12dp"
        android:text="New Tab"
        android:textColor="#EEE"
        android:textSize="13sp"
        android:singleLine="true" />
        
    <ImageButton
        android:id="@+id/btn_close_tab"
        android:layout_width="30dp"
        android:layout_height="30dp"
        android:layout_alignParentEnd="true"
        android:layout_centerVertical="true"
        android:layout_marginEnd="4dp"
        android:background="?attr/selectableItemBackgroundBorderless"
        android:src="@android:drawable/ic_menu_close_clear_cancel"
        android:tint="#888" />
</RelativeLayout>
"""

activity_main_xml = """
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/bg_main">

    <!-- الواجهة العلوية -->
    <LinearLayout
        android:id="@+id/ui_container"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:background="@color/bg_secondary"
        android:elevation="4dp">

        <!-- شريط التبويبات -->
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
                android:layout_width="45dp"
                android:layout_height="match_parent"
                android:text="+"
                android:textSize="24sp"
                android:textColor="@color/accent_neon"
                android:background="?attr/selectableItemBackground"
                android:gravity="center"/>
        </LinearLayout>

        <!-- شريط العنوان والأدوات -->
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="50dp"
            android:gravity="center_vertical"
            android:padding="6dp"
            android:background="@color/bg_secondary">
            
            <!-- زر القوائم (مجلد) -->
            <ImageButton
                android:id="@+id/btn_menu"
                android:layout_width="45dp"
                android:layout_height="match_parent"
                android:src="@android:drawable/ic_menu_sort_by_size"
                android:tint="#AAA"
                android:background="?attr/selectableItemBackground"/>

            <!-- زر النجمة -->
            <ImageButton
                android:id="@+id/btn_bookmark"
                android:layout_width="45dp"
                android:layout_height="match_parent"
                android:src="@android:drawable/star_off"
                android:tint="#AAA"
                android:background="?attr/selectableItemBackground"/>

            <!-- شريط العنوان (إصلاح الشاشة البيضاء) -->
            <EditText
                android:id="@+id/url_input"
                android:layout_width="0dp"
                android:layout_height="38dp"
                android:layout_weight="1"
                android:layout_marginStart="8dp"
                android:layout_marginEnd="8dp"
                android:background="@drawable/bg_url_bar"
                android:hint="Type URL or search..."
                android:paddingStart="16dp"
                android:textColor="#FFF"
                android:textColorHint="#666"
                android:textSize="15sp"
                android:singleLine="true"
                android:inputType="textUri"
                android:imeOptions="actionGo|flagNoExtractUi"/>
            
            <!-- زر GO -->
            <ImageButton
                android:id="@+id/btn_go"
                android:layout_width="45dp"
                android:layout_height="match_parent"
                android:src="@android:drawable/ic_menu_send"
                android:tint="@color/accent_neon"
                android:background="?attr/selectableItemBackground"/>
                
            <!-- زر الإعدادات (ترس) -->
            <ImageButton
                android:id="@+id/btn_settings"
                android:layout_width="45dp"
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
# 3. إعدادات Gradle والمانيفست
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
        versionCode = 17
        versionName = "17.0-Ultra-Fix"
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

# 🔥 إصلاح الحواف الرمادية (max_aspect) + التدوير الأفقي الإجباري 🔥
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
        android:label="B-Ultra"
        android:roundIcon="@drawable/ic_launcher"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.NoActionBar"
        android:resizeableActivity="true"
        tools:targetApi="31">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="sensorLandscape" 
            android:configChanges="orientation|screenSize|smallestScreenSize|keyboard|keyboardHidden|navigation|uiMode"
            android:windowSoftInputMode="adjustResize|stateAlwaysHidden">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <!-- هذا السطر يحل مشكلة الحواف الرمادية في الشاشات الطويلة -->
            <meta-data android:name="android.max_aspect" android:value="2.4" />
        </activity>
    </application>
</manifest>
"""

backup_rules = """<?xml version="1.0" encoding="utf-8"?><full-backup-content />"""
data_extraction = """<?xml version="1.0" encoding="utf-8"?><data-extraction-rules />"""

# ==========================================
# 4. كود Kotlin (إصلاح الروابط + البحث) 🧠
# ==========================================

main_activity = f"""
package {PACKAGE_NAME}

import android.app.AlertDialog
import android.content.Context
import android.graphics.Color
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
import org.mozilla.geckoview.BasicSelectionActionDelegate
import java.io.File
import java.io.FileOutputStream
import java.net.URLEncoder

class MainActivity : AppCompatActivity() {{

    private lateinit var geckoView: GeckoView
    private lateinit var geckoRuntime: GeckoRuntime
    private lateinit var tabsContainer: LinearLayout
    private lateinit var urlInput: EditText
    private lateinit var uiContainer: LinearLayout
    private lateinit var btnBookmark: ImageButton
    private lateinit var btnMenu: ImageButton

    private val sessions = ArrayList<TabSession>()
    private var currentTabIndex = -1
    private var isGhostMode = false
    private val HOME_FILE_NAME = "home.html"
    private lateinit var homeUrl: String
    private var currentResolution = "1080" 

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
        btnMenu = findViewById(R.id.btn_menu)

        // تحسين التركيز للماوس والكيبورد
        geckoView.isFocusable = true
        geckoView.isFocusableInTouchMode = true
        
        geckoRuntime = GeckoRuntime.create(this)
        
        val prefs = getSharedPreferences("BrowserSettings", Context.MODE_PRIVATE)
        currentResolution = prefs.getString("resolution", "1080") ?: "1080"

        findViewById<Button>(R.id.btn_add_tab).setOnClickListener {{ addNewTab(homeUrl) }}
        findViewById<ImageButton>(R.id.btn_go).setOnClickListener {{ loadUrl(urlInput.text.toString()) }}
        findViewById<ImageButton>(R.id.btn_settings).setOnClickListener {{ showSettingsDialog() }}
        btnMenu.setOnClickListener {{ showBookmarksDialog() }}

        btnBookmark.setOnClickListener {{
            if(currentTabIndex != -1) {{
                val tab = sessions[currentTabIndex]
                saveBookmark(tab.currentUrl, tab.title)
                Toast.makeText(this, "Saved! ⭐", Toast.LENGTH_SHORT).show()
                btnBookmark.setColorFilter(Color.parseColor("#00E5FF"))
            }}
        }}

        // منع الشاشة البيضاء عند الكتابة
        urlInput.imeOptions = EditorInfo.IME_ACTION_GO or EditorInfo.IME_FLAG_NO_EXTRACT_UI
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
        // نسخ الملف دائماً للتحديث
        try {{
            assets.open(HOME_FILE_NAME).use {{ input ->
                FileOutputStream(file).use {{ output -> input.copyTo(output) }}
            }}
        }} catch (e: Exception) {{ e.printStackTrace() }}
        homeUrl = "file://" + file.absolutePath
    }}

    private fun addNewTab(urlToLoad: String) {{
        val builder = GeckoSessionSettings.Builder()
            .usePrivateMode(false)
            
        when(currentResolution) {{
            "720" -> {{
                builder.viewportMode(GeckoSessionSettings.VIEWPORT_MODE_MOBILE)
                builder.userAgentOverride("") 
            }}
            "4K" -> {{
                builder.viewportMode(GeckoSessionSettings.VIEWPORT_MODE_DESKTOP)
                builder.displayMode(GeckoSessionSettings.DISPLAY_MODE_BROWSER)
                builder.userAgentOverride("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
            }}
            else -> {{ 
                builder.viewportMode(GeckoSessionSettings.VIEWPORT_MODE_DESKTOP)
                builder.userAgentOverride("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0")
            }}
        }}
        
        val settings = builder.build()
        val session = GeckoSession(settings)
        session.open(geckoRuntime)

        val tabView = LayoutInflater.from(this).inflate(R.layout.item_tab, tabsContainer, false)
        val tabTitleView = tabView.findViewById<TextView>(R.id.tab_title)
        val tabIndicator = tabView.findViewById<View>(R.id.tab_indicator)
        val btnClose = tabView.findViewById<ImageButton>(R.id.btn_close_tab)

        val newTab = TabSession(session, tabView, urlToLoad)
        sessions.add(newTab)
        
        // 🔥 تفعيل القوائم المنبثقة (نسخ/لصق) 🔥
        session.selectionActionDelegate = BasicSelectionActionDelegate(this)

        session.progressDelegate = object : GeckoSession.ProgressDelegate {{
            override fun onPageStart(session: GeckoSession, url: String) {{
                newTab.currentUrl = url
                if(sessions.indexOf(newTab) == currentTabIndex) {{
                     if(!url.startsWith("file")) {{
                         urlInput.setText(url)
                         btnBookmark.setColorFilter(Color.GRAY)
                     }} else {{
                         urlInput.setText("")
                     }}
                }}
            }}
            override fun onPageStop(session: GeckoSession, success: Boolean) {{ }}
        }}
        
        session.contentDelegate = object : GeckoSession.ContentDelegate {{
            override fun onTitleChange(session: GeckoSession, title: String?) {{
                val finalTitle = title ?: "New Tab"
                newTab.title = finalTitle
                tabTitleView.text = finalTitle
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
        geckoView.requestFocus() 

        for (i in sessions.indices) {{
            val view = sessions[i].tabView
            val indicator = view.findViewById<View>(R.id.tab_indicator)
            if (i == index) {{
                view.isSelected = true
                indicator.visibility = View.VISIBLE
            }} else {{
                view.isSelected = false
                indicator.visibility = View.INVISIBLE
            }}
        }}
        
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

    // 🔥 إصلاح منطق الروابط (Regex-Free Logic) 🔥
    private fun loadUrl(input: String) {{
        if (currentTabIndex == -1) return
        var url = input.trim()
        if (url.isEmpty()) return

        // 1. هل هو رابط صريح؟
        val hasScheme = url.startsWith("http://") || 
                        url.startsWith("https://") || 
                        url.startsWith("file://") ||
                        url.startsWith("about:")

        // 2. هل هو لوكال هوست أو آي بي؟
        val isLocalhost = url.startsWith("localhost") || url.startsWith("127.0.0.1")
        // فحص بسيط للآي بي (أرقام ونقاط)
        val isIP = url.replace(".", "").replace(":", "").all {{ it.isDigit() }} && url.contains(".")

        // 3. هل يبدو كدومين؟ (يحتوي نقطة ولا يحتوي مسافة)
        val isDomain = url.contains(".") && !url.contains(" ")

        when {{
            hasScheme -> {{ 
                // الرابط جاهز
            }}
            isLocalhost || isIP -> {{
                url = "http://$url"
            }}
            isDomain -> {{
                url = "https://$url"
            }}
            else -> {{
                // بحث جوجل
                url = "https://www.google.com/search?q=" + URLEncoder.encode(url, "UTF-8")
            }}
        }}
        
        sessions[currentTabIndex].session.loadUri(url)
        addToHistoryLog(url)
        geckoView.requestFocus()
    }}

    private fun showBookmarksDialog() {{
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_bookmarks, null)
        val btnBookmarks = dialogView.findViewById<Button>(R.id.btn_view_bookmarks)
        val btnHistory = dialogView.findViewById<Button>(R.id.btn_view_history)
        val listView = dialogView.findViewById<ListView>(R.id.list_data)
        val btnClearHistory = dialogView.findViewById<Button>(R.id.btn_clear_history)
        val dialogTitle = dialogView.findViewById<TextView>(R.id.dialog_title)

        val dialog = AlertDialog.Builder(this).setView(dialogView).create()

        fun loadList(type: String) {{
            val listData = ArrayList<Map<String, String>>()
            if (type == "bookmarks") {{
                val prefs = getSharedPreferences("Bookmarks", Context.MODE_PRIVATE)
                val jsonArray = JSONArray(prefs.getString("list", "[]"))
                for(i in 0 until jsonArray.length()) {{
                    val item = jsonArray.getJSONObject(i)
                    listData.add(mapOf("title" to item.getString("title"), "url" to item.getString("url")))
                }}
                dialogTitle.text = "⭐ Saved Bookmarks"
                btnClearHistory.visibility = View.GONE
            }} else {{
                try {{
                    val lines = File(filesDir, "history.txt").readLines().reversed()
                    for(line in lines) {{
                        if(line.contains(": ")) {{
                            val parts = line.split(": ", limit = 2)
                            listData.add(mapOf("title" to "Visited", "url" to parts[1]))
                        }}
                    }}
                }} catch(e: Exception) {{}}
                dialogTitle.text = "🕒 Browsing History"
                btnClearHistory.visibility = View.VISIBLE
            }}
            val adapter = object : SimpleAdapter(
                this, listData, R.layout.item_list_row,
                arrayOf("title", "url"), intArrayOf(R.id.row_title, R.id.row_url)
            ) {{}}
            listView.adapter = adapter
            listView.setOnItemClickListener {{ _, _, position, _ ->
                val url = listData[position]["url"]
                if(url != null) loadUrl(url)
                dialog.dismiss()
            }}
        }}
        loadList("bookmarks")
        btnBookmarks.setOnClickListener {{ loadList("bookmarks") }}
        btnHistory.setOnClickListener {{ loadList("history") }}
        btnClearHistory.setOnClickListener {{
            File(filesDir, "history.txt").delete()
            loadList("history")
            Toast.makeText(this, "History Cleared", Toast.LENGTH_SHORT).show()
        }}
        dialog.show()
    }}

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

    private fun addToHistoryLog(url: String) {{
        try {{ File(filesDir, "history.txt").appendText("${{System.currentTimeMillis()}}: $url\\n") }} catch (e: Exception) {{}}
    }}
    
    private fun showSettingsDialog() {{
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_settings, null)
        val rgResolution = dialogView.findViewById<RadioGroup>(R.id.rg_resolution)
        val btnClear = dialogView.findViewById<Button>(R.id.btn_clear_data)
        when(currentResolution) {{
            "720" -> rgResolution.check(R.id.rb_720)
            "4K" -> rgResolution.check(R.id.rb_4k)
            else -> rgResolution.check(R.id.rb_1080)
        }}
        val dialog = AlertDialog.Builder(this).setView(dialogView).create()
        rgResolution.setOnCheckedChangeListener {{ _, checkedId ->
            val newRes = when(checkedId) {{ R.id.rb_720 -> "720" ; R.id.rb_4k -> "4K" ; else -> "1080" }}
            currentResolution = newRes
            getSharedPreferences("BrowserSettings", Context.MODE_PRIVATE).edit().putString("resolution", newRes).apply()
            Toast.makeText(this, "Restart tabs to apply.", Toast.LENGTH_SHORT).show()
        }}
        btnClear.setOnClickListener {{
            geckoRuntime.storageController.clearData(org.mozilla.geckoview.StorageController.ClearFlags.ALL)
            File(filesDir, "history.txt").delete()
            Toast.makeText(this, "All Data Cleared!", Toast.LENGTH_SHORT).show()
        }}
        dialog.show()
    }}

    // 🔥 وضع الشبح المطور (Immersive Sticky) 🔥
    override fun dispatchKeyEvent(event: KeyEvent): Boolean {{
        if (event.action == KeyEvent.ACTION_DOWN && event.isCtrlPressed && event.keyCode == KeyEvent.KEYCODE_G) {{
            isGhostMode = !isGhostMode
            if (isGhostMode) {{
                uiContainer.visibility = View.GONE
                window.decorView.systemUiVisibility = (
                        View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                        or View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                        or View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                        or View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                        or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        or View.SYSTEM_UI_FLAG_FULLSCREEN)
            }} else {{
                uiContainer.visibility = View.VISIBLE
                window.decorView.systemUiVisibility = View.SYSTEM_UI_FLAG_VISIBLE
            }}
            return true
        }}
        return super.dispatchKeyEvent(event)
    }}

    override fun onPause() {{
        super.onPause()
        val prefs = getSharedPreferences("BrowserState", Context.MODE_PRIVATE).edit()
        prefs.putInt("tab_count", sessions.size)
        for (i in sessions.indices) prefs.putString("tab_$i", sessions[i].currentUrl)
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
}}
"""

# ==========================================
# التنفيذ
# ==========================================
print("🚀 بدء بناء نسخة B-Ultra النهائية...")

create_file("settings.gradle.kts", settings_gradle)
create_file("build.gradle.kts", build_gradle_root)
create_file("gradle.properties", gradle_properties)
create_file(".gitignore", gitignore)
create_file("app/build.gradle.kts", build_gradle_app)
create_file("app/src/main/AndroidManifest.xml", manifest)
create_file("app/src/main/res/xml/backup_rules.xml", backup_rules)
create_file("app/src/main/res/xml/data_extraction_rules.xml", data_extraction)

# الأيقونات
has_custom = setup_icon()
if not has_custom:
    os.makedirs(DRAWABLE_DIR, exist_ok=True)
    create_file(os.path.join(DRAWABLE_DIR, "ic_launcher.xml"), vector_eagle_xml)

# الصفحة الرئيسية الجديدة (Dark Particle)
home_html_fixed = """
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>New Tab</title><style>body{margin:0;overflow:hidden;background-color:#0d0e12;font-family:'Segoe UI',sans-serif;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;color:white}h1{font-size:90px;margin-bottom:20px;color:#fff;letter-spacing:-3px;font-weight:bold}h1 span{color:#00E5FF}input{width:600px;padding:20px 30px;border-radius:50px;border:none;background:#1F2029;color:white;font-size:20px;outline:none;box-shadow:0 10px 40px rgba(0,0,0,0.4);transition:0.3s}input:focus{box-shadow:0 0 0 2px #00E5FF;transform:scale(1.02)}</style></head><body><h1>B<span>-</span>Ultra</h1><form action="https://www.google.com/search" method="GET"><input type="text" name="q" placeholder="Search web..." autofocus autocomplete="off"></form></body></html>
"""
os.makedirs(ASSETS_DIR, exist_ok=True)
create_file(os.path.join(ASSETS_DIR, "home.html"), home_html_fixed)

os.makedirs(VALUES_DIR, exist_ok=True)
create_file(os.path.join(VALUES_DIR, "colors.xml"), colors_xml)

os.makedirs(DRAWABLE_DIR, exist_ok=True)
create_file(os.path.join(DRAWABLE_DIR, "bg_tab.xml"), bg_tab_xml)
create_file(os.path.join(DRAWABLE_DIR, "bg_url_bar.xml"), bg_url_bar_xml)

os.makedirs(LAYOUT_DIR, exist_ok=True)
create_file(os.path.join(LAYOUT_DIR, "activity_main.xml"), activity_main_xml)
create_file(os.path.join(LAYOUT_DIR, "item_tab.xml"), item_tab_xml)
create_file(os.path.join(LAYOUT_DIR, "dialog_settings.xml"), dialog_settings_xml)
create_file(os.path.join(LAYOUT_DIR, "dialog_bookmarks.xml"), dialog_bookmarks_xml)
create_file(os.path.join(LAYOUT_DIR, "item_list_row.xml"), item_list_row_xml)

os.makedirs(JAVA_DIR, exist_ok=True)
create_file(os.path.join(JAVA_DIR, "MainActivity.kt"), main_activity)
#create_file(".github/workflows/build.yml", github_workflow)

print("✅ تم بناء جميع الملفات.")
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
    subprocess.run(["git", "commit", "-m", "B-Ultra Final: Fix URL Logic, Keyboard, and UI"], check=False)
    subprocess.run(["git", "branch", "-M", "main"], check=True)
    subprocess.run(["git", "push", "-u", "-f", "origin", "main"], check=True)
    print("\n✅✅ انتهى! هذا المتصفح جاهز ليكون أسطورياً.")
    print(f"🔗 {REPO_URL}/actions")
except subprocess.CalledProcessError as e:
    print(f"\n❌ خطأ: {e}")