package com.alwansan.b

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

class MainActivity : AppCompatActivity() {

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

    override fun onCreate(savedInstanceState: Bundle?) {
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
        btnAddTab.setOnClickListener {
            addNewTab()
        }

        // زر البحث
        btnGo.setOnClickListener {
            loadUrl(urlInput.text.toString())
        }

        urlInput.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_SEARCH || actionId == EditorInfo.IME_ACTION_GO) {
                loadUrl(urlInput.text.toString())
                true
            } else {
                false
            }
        }

        // إضافة التبويب الأول تلقائياً
        addNewTab()
    }

    private fun addNewTab() {
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
        tabView.setOnClickListener {
            switchToTab(sessions.indexOf(newTabSession))
        }

        // برمجة زر الإغلاق (x)
        btnClose.setOnClickListener {
            closeTab(sessions.indexOf(newTabSession))
        }

        // إضافة التبويب للشريط
        tabsContainer.addView(tabView)

        // الانتقال للتبويب الجديد
        switchToTab(newIndex)

        // تحميل الصفحة الرئيسية
        // استخدام file:///android_asset/ هو الصحيح لـ GeckoView
        session.loadUri("file:///android_asset/home.html")
    }

    private fun switchToTab(index: Int) {
        if (index !in sessions.indices) return

        currentTabIndex = index
        val tabSession = sessions[index]

        // ربط الجلسة بالمتصفح (هذا لا يغلق الجلسات الأخرى، فقط يخفيها)
        geckoView.setSession(tabSession.session)

        // تحديث تصميم الشريط (تمييز التبويب النشط)
        for (i in sessions.indices) {
            sessions[i].tabView.isSelected = (i == index)
        }

        // تحديث شريط العنوان (إذا لم تكن الصفحة الرئيسية)
        // (يمكن تطوير هذا الجزء لاحقاً لجلب العنوان الحقيقي)
        urlInput.setText("") 
        urlInput.hint = "Search Google..."
    }

    private fun closeTab(index: Int) {
        if (index !in sessions.indices) return

        val tabSession = sessions[index]
        
        // إغلاق الجلسة لتوفير الذاكرة
        tabSession.session.close()
        
        // حذف من الواجهة والقائمة
        tabsContainer.removeView(tabSession.tabView)
        sessions.removeAt(index)

        if (sessions.isEmpty()) {
            // إذا أغلق آخر تبويب، افتح واحداً جديداً
            addNewTab()
        } else {
            // الانتقال للتبويب السابق
            val nextIndex = if (index > 0) index - 1 else 0
            switchToTab(nextIndex)
        }
    }

    private fun loadUrl(input: String) {
        if (currentTabIndex == -1) return
        val session = sessions[currentTabIndex].session
        
        var url = input.trim()
        if (url.isEmpty()) return

        // التحقق هل هو رابط أم بحث
        if (url.contains(" ") || !url.contains(".")) {
            // بحث جوجل
            url = "https://www.google.com/search?q=$url"
        } else if (!url.startsWith("http")) {
            // إضافة https
            url = "https://$url"
        }
        
        session.loadUri(url)
    }

    // اختصار Ctrl+G
    override fun dispatchKeyEvent(event: KeyEvent): Boolean {
        if (event.action == KeyEvent.ACTION_DOWN && event.isCtrlPressed && event.keyCode == KeyEvent.KEYCODE_G) {
            toggleGhostMode()
            return true
        }
        return super.dispatchKeyEvent(event)
    }

    private fun toggleGhostMode() {
        isGhostMode = !isGhostMode
        if (isGhostMode) {
            uiContainer.visibility = View.GONE
            window.decorView.systemUiVisibility = (View.SYSTEM_UI_FLAG_FULLSCREEN
                    or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                    or View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY)
        } else {
            uiContainer.visibility = View.VISIBLE
            window.decorView.systemUiVisibility = View.SYSTEM_UI_FLAG_VISIBLE
        }
    }
}