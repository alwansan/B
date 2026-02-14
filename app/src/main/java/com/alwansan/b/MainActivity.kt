package com.alwansan.b

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

class MainActivity : AppCompatActivity() {

    private lateinit var geckoView: GeckoView
    private lateinit var geckoSession: GeckoSession
    private lateinit var geckoRuntime: GeckoRuntime
    private lateinit var urlInput: EditText
    private lateinit var btnGo: Button
    private lateinit var topBar: LinearLayout
    private var isUiHidden = false

    override fun onCreate(savedInstanceState: Bundle?) {
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

        btnGo.setOnClickListener {
            loadUrl(urlInput.text.toString())
        }

        urlInput.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_GO || actionId == EditorInfo.IME_ACTION_DONE) {
                loadUrl(urlInput.text.toString())
                true
            } else {
                false
            }
        }
    }

    private fun loadUrl(url: String) {
        var finalUrl = url.trim()
        if (finalUrl.isNotEmpty()) {
            if (!finalUrl.startsWith("http") && !finalUrl.startsWith("file")) {
                finalUrl = "https://$finalUrl"
            }
            geckoSession.loadUri(finalUrl)
        }
    }

    // ⚡ التعامل مع اختصارات الكيبورد (Ctrl + G) ⚡
    override fun dispatchKeyEvent(event: KeyEvent): Boolean {
        if (event.action == KeyEvent.ACTION_DOWN) {
            // التحقق من ضغط Ctrl + G
            if (event.keyCode == KeyEvent.KEYCODE_G && event.isCtrlPressed) {
                toggleUi()
                return true
            }
        }
        return super.dispatchKeyEvent(event)
    }

    private fun toggleUi() {
        isUiHidden = !isUiHidden
        if (isUiHidden) {
            // إخفاء كل شيء والبقاء على المتصفح فقط
            topBar.visibility = View.GONE
            // إخفاء شريط الحالة العلوي (Full Screen)
            window.decorView.systemUiVisibility = (View.SYSTEM_UI_FLAG_FULLSCREEN
                    or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                    or View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY)
        } else {
            // إظهار الشريط
            topBar.visibility = View.VISIBLE
            window.decorView.systemUiVisibility = View.SYSTEM_UI_FLAG_VISIBLE
        }
    }
}