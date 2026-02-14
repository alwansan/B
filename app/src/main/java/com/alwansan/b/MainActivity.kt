package com.alwansan.b

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

class MainActivity : AppCompatActivity() {

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

    override fun onCreate(savedInstanceState: Bundle?) {
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

        findViewById<Button>(R.id.btn_add_tab).setOnClickListener { addNewTab(homeUrl) }
        findViewById<Button>(R.id.btn_go).setOnClickListener { loadUrl(urlInput.text.toString()) }

        urlInput.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_GO || actionId == EditorInfo.IME_ACTION_DONE) {
                loadUrl(urlInput.text.toString())
                true
            } else { false }
        }

        // 3. استعادة التبويبات السابقة (Persistent Tabs)
        restoreTabs()
    }

    private fun setupLocalHomeFile() {
        // نسخ ملف home.html من assets إلى الذاكرة الداخلية للهاتف
        val file = File(filesDir, HOME_FILE_NAME)
        if (!file.exists()) {
            try {
                assets.open(HOME_FILE_NAME).use { input ->
                    FileOutputStream(file).use { output ->
                        input.copyTo(output)
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        homeUrl = "file://" + file.absolutePath
    }

    private fun addNewTab(urlToLoad: String) {
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

        tabView.setOnClickListener { switchToTab(sessions.indexOf(newTab)) }
        btnClose.setOnClickListener { closeTab(sessions.indexOf(newTab)) }
        
        tabsContainer.addView(tabView)
        switchToTab(newIndex)
        
        session.loadUri(urlToLoad)
    }

    private fun switchToTab(index: Int) {
        if (index !in sessions.indices) return
        currentTabIndex = index
        val tab = sessions[index]
        geckoView.setSession(tab.session)

        for (i in sessions.indices) {
            sessions[i].tabView.isSelected = (i == index)
        }
        
        // تحديث شريط العنوان (بدون بروتوكول للتجميل)
        // في التطبيق الحقيقي سنستمع لتغيرات الرابط
    }

    private fun closeTab(index: Int) {
        if (index !in sessions.indices) return
        val tab = sessions[index]
        tab.session.close()
        tabsContainer.removeView(tab.tabView)
        sessions.removeAt(index)

        if (sessions.isEmpty()) {
            addNewTab(homeUrl)
        } else {
            switchToTab(if (index > 0) index - 1 else 0)
        }
    }

    private fun loadUrl(input: String) {
        if (currentTabIndex == -1) return
        val session = sessions[currentTabIndex].session
        var url = input.trim()
        if (url.isEmpty()) return

        if (url.contains(" ") || !url.contains(".")) {
            url = "https://www.google.com/search?q=$url"
        } else if (!url.startsWith("http") && !url.startsWith("file")) {
            url = "https://$url"
        }
        
        // تحديث الرابط الحالي في الذاكرة للحفظ
        sessions[currentTabIndex].currentUrl = url
        session.loadUri(url)
        
        // 🔥 تسجيل في السجل (History Log) 🔥
        addToHistoryLog(url)
    }

    // ==================
    // 💾 نظام الحفظ والاستعادة
    // ==================
    
    override fun onPause() {
        super.onPause()
        saveTabsState()
    }

    private fun saveTabsState() {
        val prefs = getSharedPreferences("BrowserState", Context.MODE_PRIVATE)
        val editor = prefs.edit()
        
        // حفظ عدد التبويبات
        editor.putInt("tab_count", sessions.size)
        
        // حفظ رابط كل تبويب (نحاول جلب الرابط الحقيقي من المحرك)
        for (i in sessions.indices) {
            // ملاحظة: loader.uri قد لا يكون محدثاً فوراً، لذا نعتمد على ما طلبناه مبدئياً
            // أو يمكن تحسينه لاحقاً بـ ProgressDelegate
            var url = sessions[i].currentUrl
            if (url.isEmpty()) url = homeUrl
            editor.putString("tab_$i", url)
        }
        editor.putInt("last_index", currentTabIndex)
        editor.apply()
    }

    private fun restoreTabs() {
        val prefs = getSharedPreferences("BrowserState", Context.MODE_PRIVATE)
        val count = prefs.getInt("tab_count", 0)
        
        if (count > 0) {
            for (i in 0 until count) {
                val url = prefs.getString("tab_$i", homeUrl) ?: homeUrl
                addNewTab(url)
            }
            val lastIndex = prefs.getInt("last_index", 0)
            switchToTab(lastIndex)
        } else {
            // فتح صفحة واحدة افتراضية
            addNewTab(homeUrl)
        }
    }

    private fun addToHistoryLog(url: String) {
        // حفظ بسيط في ملف نصي
        try {
            val file = File(filesDir, "history.txt")
            file.appendText(System.currentTimeMillis().toString() + ": " + url + "\n")
        } catch (e: Exception) {}
    }

    // ==================
    // 👻 وضع الشبح (Ctrl+G)
    // ==================
    override fun dispatchKeyEvent(event: KeyEvent): Boolean {
        if (event.action == KeyEvent.ACTION_DOWN && event.isCtrlPressed && event.keyCode == KeyEvent.KEYCODE_G) {
            isGhostMode = !isGhostMode
            if (isGhostMode) {
                uiContainer.visibility = View.GONE
                window.decorView.systemUiVisibility = (View.SYSTEM_UI_FLAG_FULLSCREEN or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION or View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY)
            } else {
                uiContainer.visibility = View.VISIBLE
                window.decorView.systemUiVisibility = View.SYSTEM_UI_FLAG_VISIBLE
            }
            return true
        }
        return super.dispatchKeyEvent(event)
    }
}