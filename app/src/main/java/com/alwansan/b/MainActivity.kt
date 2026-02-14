package com.alwansan.b

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
import org.mozilla.geckoview.WebExtension
import org.mozilla.geckoview.WebExtensionController
import org.mozilla.geckoview.BasicSelectionActionDelegate
import java.io.File
import java.io.FileOutputStream

class MainActivity : AppCompatActivity() {

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

    override fun onCreate(savedInstanceState: Bundle?) {
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

        // 🔒 Disable double tap & pinch zoom at View level
        geckoView.setOnTouchListener { _, event ->
            if (event.pointerCount > 1) {
                true
            } else {
                false
            }
        }
        
        
        // 🔥 تثبيت الإضافات تلقائياً (Extensions) 🔥
        installBuiltInExtensions()

        val prefs = getSharedPreferences("BrowserSettings", Context.MODE_PRIVATE)
        currentResolution = prefs.getString("resolution", "1080") ?: "1080"

        findViewById<Button>(R.id.btn_add_tab).setOnClickListener { addNewTab(homeUrl) }
        findViewById<ImageButton>(R.id.btn_go).setOnClickListener { loadUrl(urlInput.text.toString()) }
        findViewById<ImageButton>(R.id.btn_settings).setOnClickListener { showSettingsDialog() }
        btnMenu.setOnClickListener { showBookmarksDialog() }

        btnBookmark.setOnClickListener {
            if(currentTabIndex != -1) {
                val tab = sessions[currentTabIndex]
                saveBookmark(tab.currentUrl, tab.title)
                Toast.makeText(this, "Saved! ⭐", Toast.LENGTH_SHORT).show()
                btnBookmark.setColorFilter(Color.parseColor("#00E5FF"))
            }
        }

        urlInput.imeOptions = EditorInfo.IME_ACTION_GO or EditorInfo.IME_FLAG_NO_EXTRACT_UI
        urlInput.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_GO || actionId == EditorInfo.IME_ACTION_DONE) {
                loadUrl(urlInput.text.toString())
                true
            } else { false }
        }

        restoreTabs()
    }

    // 🔥 دالة تثبيت الإضافات من مجلد assets/extensions 🔥
    private fun installBuiltInExtensions() {
        try {
            val extensions = assets.list("extensions") ?: return
            for (extFile in extensions) {
                if (extFile.endsWith(".xpi")) {
                    geckoRuntime.webExtensionController.install(
                        "resource://android/assets/extensions/$extFile"
                    )
                }
            }
        } catch (e: Exception) { e.printStackTrace() }
    }

    private fun setupLocalHomeFile() {
        val file = File(filesDir, HOME_FILE_NAME)
        try {
            assets.open(HOME_FILE_NAME).use { input ->
                FileOutputStream(file).use { output -> input.copyTo(output) }
            }
        } catch (e: Exception) { e.printStackTrace() }
        homeUrl = "file://" + file.absolutePath
    }

    private fun addNewTab(urlToLoad: String) {
        val builder = GeckoSessionSettings.Builder()
            .usePrivateMode(false)
            // 🔥 أهم سطر: هذا يمنع التكبير عند النقر المزدوج (يثبت الشاشة) 🔥
            .suspendMediaWhenInactive(false)
            
        // إعدادات الشاشة
        when(currentResolution) {
            "720" -> {
                builder.viewportMode(GeckoSessionSettings.VIEWPORT_MODE_MOBILE)
                builder.userAgentOverride("") 
            }
            "4K" -> {
                builder.viewportMode(GeckoSessionSettings.VIEWPORT_MODE_DESKTOP)
                builder.displayMode(GeckoSessionSettings.DISPLAY_MODE_BROWSER)
                builder.userAgentOverride("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
            }
            else -> { 
                builder.viewportMode(GeckoSessionSettings.VIEWPORT_MODE_DESKTOP)
                builder.userAgentOverride("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0")
            }
        }
        
        val settings = builder.build()
        // 🔥 إلغاء التكبير المزدوج المزعج 🔥
        // Removed invalid USE_DOUBLE_TAP_ZOOM (not supported in Gecko 121+)
        
        val session = GeckoSession(settings)
        session.open(geckoRuntime)

        val tabView = LayoutInflater.from(this).inflate(R.layout.item_tab, tabsContainer, false)
        val tabTitleView = tabView.findViewById<TextView>(R.id.tab_title)
        val btnClose = tabView.findViewById<ImageButton>(R.id.btn_close_tab)

        val newTab = TabSession(session, tabView, urlToLoad)
        sessions.add(newTab)
        
        // 🔥 تفعيل القوائم المنبثقة (Right Click / Context Menu) 🔥
        session.selectionActionDelegate = BasicSelectionActionDelegate(this)

        session.progressDelegate = object : GeckoSession.ProgressDelegate {
            override fun onPageStart(session: GeckoSession, url: String) {
                newTab.currentUrl = url
                if(sessions.indexOf(newTab) == currentTabIndex) {
                     if(!url.startsWith("file")) {
                         urlInput.setText(url)
                         btnBookmark.setColorFilter(Color.GRAY)
                     } else {
                         urlInput.setText("")
                     }
                }
            }
            override fun onPageStop(session: GeckoSession, success: Boolean) { }
        }
        
        session.contentDelegate = object : GeckoSession.ContentDelegate {
            override fun onTitleChange(session: GeckoSession, title: String?) {
                val finalTitle = title ?: "New Tab"
                newTab.title = finalTitle
                tabTitleView.text = finalTitle
            }
        }

        tabView.setOnClickListener { switchToTab(sessions.indexOf(newTab)) }
        btnClose.setOnClickListener { closeTab(sessions.indexOf(newTab)) }
        
        tabsContainer.addView(tabView)
        switchToTab(sessions.size - 1)
        
        session.loadUri(urlToLoad)
    }

    private fun switchToTab(index: Int) {
        if (index !in sessions.indices) return
        currentTabIndex = index
        val tab = sessions[index]
        geckoView.setSession(tab.session)
        geckoView.requestFocus() // إعادة التركيز

        for (i in sessions.indices) {
            val view = sessions[i].tabView
            val indicator = view.findViewById<View>(R.id.tab_indicator)
            if (i == index) {
                view.isSelected = true
                indicator.visibility = View.VISIBLE
            } else {
                view.isSelected = false
                indicator.visibility = View.INVISIBLE
            }
        }
        
        if(tab.currentUrl.startsWith("file")) {
            urlInput.setText("")
            urlInput.hint = "Search Google..."
        } else {
            urlInput.setText(tab.currentUrl)
        }
    }

    private fun closeTab(index: Int) {
        if (index !in sessions.indices) return
        val tab = sessions[index]
        tab.session.close()
        tabsContainer.removeView(tab.tabView)
        sessions.removeAt(index)

        if (sessions.isEmpty()) addNewTab(homeUrl)
        else switchToTab(if (index > 0) index - 1 else 0)
    }

    private fun loadUrl(input: String) {
        if (currentTabIndex == -1) return
        
        
        
        var url = input.trim()
        if (url.isEmpty()) return

        val isHttp = url.startsWith("http://") || url.startsWith("https://")
        val hasSpace = url.contains(" ")
        val looksLikeDomain = url.contains(".") || url.contains(":") || url.startsWith("localhost")

        if (isHttp) {
            // open as is
        } else if (hasSpace) {
            url = "https://www.google.com/search?q=$url"
        } else if (looksLikeDomain) {
            url = "http://$url"
        } else {
            url = "https://www.google.com/search?q=$url"
        }

        addToHistoryLog(url)
    
    
        geckoView.requestFocus()
    }

    // ==================
    // 💾 Bookmarks & History & Settings (نفس الكود السابق، يعمل بكفاءة)
    // ==================
    
    private fun showBookmarksDialog() {
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_bookmarks, null)
        val btnBookmarks = dialogView.findViewById<Button>(R.id.btn_view_bookmarks)
        val btnHistory = dialogView.findViewById<Button>(R.id.btn_view_history)
        val listView = dialogView.findViewById<ListView>(R.id.list_data)
        val btnClearHistory = dialogView.findViewById<Button>(R.id.btn_clear_history)
        val dialogTitle = dialogView.findViewById<TextView>(R.id.dialog_title)

        val dialog = AlertDialog.Builder(this).setView(dialogView).create()

        fun loadList(type: String) {
            val listData = ArrayList<Map<String, String>>()
            if (type == "bookmarks") {
                val prefs = getSharedPreferences("Bookmarks", Context.MODE_PRIVATE)
                val jsonArray = JSONArray(prefs.getString("list", "[]"))
                for(i in 0 until jsonArray.length()) {
                    val item = jsonArray.getJSONObject(i)
                    listData.add(mapOf("title" to item.getString("title"), "url" to item.getString("url")))
                }
                dialogTitle.text = "⭐ Saved Bookmarks"
                btnClearHistory.visibility = View.GONE
            } else {
                try {
                    val lines = File(filesDir, "history.txt").readLines().reversed()
                    for(line in lines) {
                        if(line.contains(": ")) {
                            val parts = line.split(": ", limit = 2)
                            listData.add(mapOf("title" to "Visited", "url" to parts[1]))
                        }
                    }
                } catch(e: Exception) {}
                dialogTitle.text = "🕒 Browsing History"
                btnClearHistory.visibility = View.VISIBLE
            }
            val adapter = object : SimpleAdapter(
                this, listData, R.layout.item_list_row,
                arrayOf("title", "url"), intArrayOf(R.id.row_title, R.id.row_url)
            ) {}
            listView.adapter = adapter
            listView.setOnItemClickListener { _, _, position, _ ->
                val url = listData[position]["url"]
                if(url != null) loadUrl(url)
                dialog.dismiss()
            }
        }
        loadList("bookmarks")
        btnBookmarks.setOnClickListener { loadList("bookmarks") }
        btnHistory.setOnClickListener { loadList("history") }
        btnClearHistory.setOnClickListener {
            File(filesDir, "history.txt").delete()
            loadList("history")
            Toast.makeText(this, "History Cleared", Toast.LENGTH_SHORT).show()
        }
        dialog.show()
    }

    private fun saveBookmark(url: String, title: String) {
        if(url.startsWith("file")) return 
        val prefs = getSharedPreferences("Bookmarks", Context.MODE_PRIVATE)
        val jsonString = prefs.getString("list", "[]")
        val jsonArray = JSONArray(jsonString)
        val newBm = JSONObject()
        newBm.put("url", url)
        newBm.put("title", title)
        jsonArray.put(newBm)
        prefs.edit().putString("list", jsonArray.toString()).apply()
    }

    private fun addToHistoryLog(url: String) {
        try { File(filesDir, "history.txt").appendText("${System.currentTimeMillis()}: $url\n") } catch (e: Exception) {}
    }
    
    private fun showSettingsDialog() {
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_settings, null)
        val rgResolution = dialogView.findViewById<RadioGroup>(R.id.rg_resolution)
        val btnClear = dialogView.findViewById<Button>(R.id.btn_clear_data)
        when(currentResolution) {
            "720" -> rgResolution.check(R.id.rb_720)
            "4K" -> rgResolution.check(R.id.rb_4k)
            else -> rgResolution.check(R.id.rb_1080)
        }
        val dialog = AlertDialog.Builder(this).setView(dialogView).create()
        rgResolution.setOnCheckedChangeListener { _, checkedId ->
            val newRes = when(checkedId) { R.id.rb_720 -> "720" ; R.id.rb_4k -> "4K" ; else -> "1080" }
            currentResolution = newRes
            getSharedPreferences("BrowserSettings", Context.MODE_PRIVATE).edit().putString("resolution", newRes).apply()
            Toast.makeText(this, "Restart tabs to apply.", Toast.LENGTH_SHORT).show()
        }
        btnClear.setOnClickListener {
            geckoRuntime.storageController.clearData(org.mozilla.geckoview.StorageController.ClearFlags.ALL)
            File(filesDir, "history.txt").delete()
            Toast.makeText(this, "All Data Cleared!", Toast.LENGTH_SHORT).show()
        }
        dialog.show()
    }

    override fun dispatchKeyEvent(event: KeyEvent): Boolean {
        if (event.action == KeyEvent.ACTION_DOWN && event.isCtrlPressed && event.keyCode == KeyEvent.KEYCODE_G) {
            isGhostMode = !isGhostMode
            if (isGhostMode) {
                uiContainer.visibility = View.GONE
                // 🔥 وضع ملء الشاشة الحقيقي (شبح كامل) 🔥
                window.decorView.systemUiVisibility = (
                        View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                        or View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                        or View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                        or View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                        or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        or View.SYSTEM_UI_FLAG_FULLSCREEN)
            } else {
                uiContainer.visibility = View.VISIBLE
                window.decorView.systemUiVisibility = View.SYSTEM_UI_FLAG_VISIBLE
            }
            return true
        }
        return super.dispatchKeyEvent(event)
    }

    override fun onPause() {
        super.onPause()
        val prefs = getSharedPreferences("BrowserState", Context.MODE_PRIVATE).edit()
        prefs.putInt("tab_count", sessions.size)
        for (i in sessions.indices) prefs.putString("tab_$i", sessions[i].currentUrl)
        prefs.putInt("last_index", currentTabIndex)
        prefs.apply()
    }

    private fun restoreTabs() {
        val prefs = getSharedPreferences("BrowserState", Context.MODE_PRIVATE)
        val count = prefs.getInt("tab_count", 0)
        if (count > 0) {
            for (i in 0 until count) {
                val url = prefs.getString("tab_$i", homeUrl) ?: homeUrl
                addNewTab(url)
            }
            switchToTab(prefs.getInt("last_index", 0))
        } else addNewTab(homeUrl)
    }
}