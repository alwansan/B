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
# 1. الموارد (Resources)
# ==========================================

# تصميم النسر الفيكتور (الاحتياطي)
vector_eagle_xml = """
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
    <path android:fillColor="#1a1f2c" android:pathData="M0,0h24v24h-24z"/>
    <path android:fillColor="#00E5FF" android:pathData="M12,2 C6.48,2 2,6.48 2,12 C2,17.52 6.48,22 12,22 C17.52,22 22,17.52 22,12 C22,6.48 17.52,2 12,2 Z M12,20 C7.59,20 4,16.41 4,12 C4,7.59 7.59,4 12,4 C16.41,4 20,7.59 20,12 C20,16.41 16.41,20 12,20 Z"/>
    <path android:fillColor="#FFFFFF" android:pathData="M12,6 L9,14 L12,18 L15,14 L12,6 Z"/>
</vector>
"""

colors_xml = """
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="bg_main">#191A24</color>
    <color name="bg_secondary">#242633</color>
    <color name="accent_neon">#00E5FF</color>
    <color name="accent_red">#FA2E4D</color>
    <color name="text_primary">#FFFFFF</color>
    <color name="tab_active">#242633</color>
    <color name="tab_inactive">#15161E</color>
</resources>
"""

bg_tab_xml = """
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_selected="true">
        <shape>
            <solid android:color="@color/tab_active"/>
            <corners android:topLeftRadius="12dp" android:topRightRadius="12dp"/>
        </shape>
    </item>
    <item>
        <shape>
            <solid android:color="@color/tab_inactive"/>
            <corners android:topLeftRadius="12dp" android:topRightRadius="12dp"/>
        </shape>
    </item>
</selector>
"""

bg_tab_indicator_xml = """
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/accent_neon"/>
    <corners android:radius="2dp"/>
</shape>
"""

bg_url_bar_xml = """
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#15161E"/>
    <corners android:radius="8dp"/>
    <stroke android:width="1dp" android:color="#333"/>
</shape>
"""

dialog_bookmarks_xml = """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="400dp"
    android:layout_height="300dp"
    android:orientation="vertical"
    android:background="@color/bg_secondary"
    android:padding="16dp">
    <TextView
        android:id="@+id/dialog_title"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Bookmarks &amp; History"
        android:textColor="@color/accent_neon"
        android:textSize="18sp"
        android:textStyle="bold"
        android:gravity="center"
        android:paddingBottom="10dp"/>
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:weightSum="2">
        <Button
            android:id="@+id/btn_view_bookmarks"
            android:layout_width="0dp"
            android:layout_height="40dp"
            android:layout_weight="1"
            android:text="Bookmarks"
            android:backgroundTint="@color/bg_main"
            android:textColor="#FFF"/>
        <Button
            android:id="@+id/btn_view_history"
            android:layout_width="0dp"
            android:layout_height="40dp"
            android:layout_weight="1"
            android:text="History"
            android:backgroundTint="@color/bg_main"
            android:textColor="#FFF"
            android:layout_marginStart="5dp"/>
    </LinearLayout>
    <ListView
        android:id="@+id/list_data"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:layout_marginTop="10dp"
        android:divider="#333"
        android:dividerHeight="1dp"
        android:background="@color/bg_main"/>
    <Button
        android:id="@+id/btn_clear_history"
        android:layout_width="match_parent"
        android:layout_height="36dp"
        android:text="Clear History"
        android:textColor="#FFF"
        android:textSize="12sp"
        android:backgroundTint="#FA2E4D"
        android:visibility="gone"
        android:layout_marginTop="8dp"/>
</LinearLayout>
"""

dialog_settings_xml = """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="300dp"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:background="@color/bg_secondary"
    android:padding="20dp">
    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Settings"
        android:textColor="@color/accent_neon"
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
        android:id="@+id/btn_clear_data"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Clear Cookies &amp; Cache"
        android:backgroundTint="#FA2E4D"
        android:layout_marginTop="10dp"/>
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
    android:layout_marginEnd="4dp">
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
        android:textColor="#E0E0E0"
        android:textSize="13sp"
        android:singleLine="true" />
    <ImageButton
        android:id="@+id/btn_close_tab"
        android:layout_width="28dp"
        android:layout_height="28dp"
        android:layout_alignParentEnd="true"
        android:layout_centerVertical="true"
        android:layout_marginEnd="4dp"
        android:background="?attr/selectableItemBackgroundBorderless"
        android:src="@android:drawable/ic_menu_close_clear_cancel"
        android:tint="#777" />
</RelativeLayout>
"""

activity_main_xml = """
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/bg_main">
    <LinearLayout
        android:id="@+id/ui_container"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:background="@color/bg_secondary"
        android:elevation="8dp">
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="40dp"
            android:orientation="horizontal"
            android:paddingTop="4dp"
            android:paddingStart="4dp">
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
                android:layout_width="44dp"
                android:layout_height="match_parent"
                android:text="+"
                android:textSize="20sp"
                android:textColor="@color/accent_neon"
                android:background="?attr/selectableItemBackground"
                android:gravity="center"/>
        </LinearLayout>
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="50dp"
            android:gravity="center_vertical"
            android:padding="6dp"
            android:background="@color/bg_secondary">
            <ImageButton
                android:id="@+id/btn_menu"
                android:layout_width="40dp"
                android:layout_height="match_parent"
                android:src="@android:drawable/ic_menu_sort_by_size"
                android:tint="#AAA"
                android:background="?attr/selectableItemBackground"/>
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
                android:layout_height="40dp"
                android:layout_weight="1"
                android:layout_marginStart="8dp"
                android:layout_marginEnd="8dp"
                android:background="@drawable/bg_url_bar"
                android:hint="Search or enter address"
                android:paddingStart="16dp"
                android:textColor="#FFF"
                android:textColorHint="#666"
                android:textSize="14sp"
                android:singleLine="true"
                android:inputType="textUri"
                android:imeOptions="actionGo|flagNoExtractUi"/>
            <ImageButton
                android:id="@+id/btn_go"
                android:layout_width="40dp"
                android:layout_height="match_parent"
                android:src="@android:drawable/ic_menu_send"
                android:tint="@color/accent_neon"
                android:background="?attr/selectableItemBackground"/>
            <ImageButton
                android:id="@+id/btn_settings"
                android:layout_width="40dp"
                android:layout_height="match_parent"
                android:src="@android:drawable/ic_menu_manage"
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
        versionCode = 16
        versionName = "16.0-Fix-Duplicate"
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
        android:label="B-Eagle"
        android:roundIcon="@drawable/ic_launcher"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.NoActionBar"
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
        </activity>
    </application>
</manifest>
"""

backup_rules = """<?xml version="1.0" encoding="utf-8"?><full-backup-content />"""
data_extraction = """<?xml version="1.0" encoding="utf-8"?><data-extraction-rules />"""

# ==========================================
# 4. كود Kotlin
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
import java.io.File
import java.io.FileOutputStream

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
                Toast.makeText(this, "Saved to Bookmarks! ⭐", Toast.LENGTH_SHORT).show()
                btnBookmark.setColorFilter(Color.parseColor("#00E5FF"))
            }}
        }}

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
        
        val session = GeckoSession(builder.build())
        session.open(geckoRuntime)

        val tabView = LayoutInflater.from(this).inflate(R.layout.item_tab, tabsContainer, false)
        val tabTitleView = tabView.findViewById<TextView>(R.id.tab_title)
        val tabIndicator = tabView.findViewById<View>(R.id.tab_indicator)
        val btnClose = tabView.findViewById<ImageButton>(R.id.btn_close_tab)

        val newTab = TabSession(session, tabView, urlToLoad)
        sessions.add(newTab)
        
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

    private fun loadUrl(input: String) {{
        if (currentTabIndex == -1) return
        var url = input.trim()
        if (url.isEmpty()) return
        if (url.contains(" ") || !url.contains(".")) url = "https://www.google.com/search?q=$url"
        else if (!url.startsWith("http") && !url.startsWith("file")) url = "https://$url"
        
        sessions[currentTabIndex].session.loadUri(url)
        addToHistoryLog(url)
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
        name: B-Browser-Opera-Eagle
        path: app/build/outputs/apk/release/*.apk
"""

# ==========================================
# التنفيذ
# ==========================================
print("🚀 بدء بناء نسخة B-Eagle (Fixed Duplicate Resources)...")

create_file("settings.gradle.kts", settings_gradle)
create_file("build.gradle.kts", build_gradle_root)
create_file("gradle.properties", gradle_properties)
create_file(".gitignore", gitignore)
create_file("app/build.gradle.kts", build_gradle_app)
create_file("app/src/main/AndroidManifest.xml", manifest)
create_file("app/src/main/res/xml/backup_rules.xml", backup_rules)
create_file("app/src/main/res/xml/data_extraction_rules.xml", data_extraction)

# الأيقونات (تم تعديل المنطق ليمنع التكرار) 🦅🔥
custom_icon_source = "icon.png"
png_target = os.path.join(DRAWABLE_DIR, "ic_launcher.png")
xml_target = os.path.join(DRAWABLE_DIR, "ic_launcher.xml")

os.makedirs(DRAWABLE_DIR, exist_ok=True)

if os.path.exists(custom_icon_source):
    print("🦅 تم العثور على صورة مخصصة! استخدام icon.png...")
    # حذف الـ XML القديم إذا وجد لمنع التكرار
    if os.path.exists(xml_target):
        os.remove(xml_target)
    shutil.copy(custom_icon_source, png_target)
else:
    print("🦅 استخدام أيقونة النسر الافتراضية (Vector)...")
    # حذف الـ PNG القديم إذا وجد لمنع التكرار
    if os.path.exists(png_target):
        os.remove(png_target)
    create_file(xml_target, vector_eagle_xml)

# الصفحة الرئيسية الجديدة
home_html_fixed = """
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>New Tab</title><style>body{margin:0;overflow:hidden;background-color:#191A24;font-family:'Segoe UI',sans-serif;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;color:white}h1{font-size:90px;margin-bottom:20px;color:#fff;letter-spacing:-3px;font-weight:bold}h1 span{color:#00E5FF}input{width:600px;padding:20px 30px;border-radius:50px;border:none;background:#242633;color:white;font-size:20px;outline:none;box-shadow:0 10px 40px rgba(0,0,0,0.4);transition:0.3s}input:focus{box-shadow:0 0 0 2px #00E5FF;transform:scale(1.02)}</style></head><body><h1>B<span>-</span>Eagle</h1><form action="https://www.google.com/search" method="GET"><input type="text" name="q" placeholder="Search web..." autofocus autocomplete="off"></form></body></html>
"""
os.makedirs(ASSETS_DIR, exist_ok=True)
create_file(os.path.join(ASSETS_DIR, "home.html"), home_html_fixed)

os.makedirs(VALUES_DIR, exist_ok=True)
create_file(os.path.join(VALUES_DIR, "colors.xml"), colors_xml)

# ملفات التصميم الأخرى
create_file(os.path.join(DRAWABLE_DIR, "bg_tab.xml"), bg_tab_xml)
create_file(os.path.join(DRAWABLE_DIR, "bg_url_bar.xml"), bg_url_bar_xml)
create_file(os.path.join(DRAWABLE_DIR, "bg_tab_indicator.xml"), bg_tab_indicator_xml)

os.makedirs(LAYOUT_DIR, exist_ok=True)
create_file(os.path.join(LAYOUT_DIR, "activity_main.xml"), activity_main_xml)
create_file(os.path.join(LAYOUT_DIR, "item_tab.xml"), item_tab_xml)
create_file(os.path.join(LAYOUT_DIR, "dialog_settings.xml"), dialog_settings_xml)
create_file(os.path.join(LAYOUT_DIR, "dialog_bookmarks.xml"), dialog_bookmarks_xml)
create_file(os.path.join(LAYOUT_DIR, "item_list_row.xml"), item_list_row_xml)

os.makedirs(JAVA_DIR, exist_ok=True)
create_file(os.path.join(JAVA_DIR, "MainActivity.kt"), main_activity)
create_file(".github/workflows/build.yml", github_workflow)

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
    subprocess.run(["git", "commit", "-m", "Final Fix: Resolve Duplicate Icon Resources"], check=False)
    subprocess.run(["git", "branch", "-M", "main"], check=True)
    subprocess.run(["git", "push", "-u", "-f", "origin", "main"], check=True)
    print("\n✅✅ تم حل مشكلة تكرار الموارد! البناء سينجح الآن.")
    print(f"🔗 {REPO_URL}/actions")
except subprocess.CalledProcessError as e:
    print(f"\n❌ خطأ: {e}")