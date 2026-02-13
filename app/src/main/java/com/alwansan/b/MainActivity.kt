package com.alwansan.b

import android.os.Bundle
import android.view.inputmethod.EditorInfo
import android.widget.Button
import android.widget.EditText
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

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // ربط الواجهة
        geckoView = findViewById(R.id.gecko_view)
        urlInput = findViewById(R.id.url_input)
        btnGo = findViewById(R.id.btn_go)

        // إعداد المحرك
        geckoRuntime = GeckoRuntime.create(this)
        
        // إعدادات الجلسة (السر هنا!)
        val settings = GeckoSessionSettings()
        
        // 1. إجبار وضع سطح المكتب (الشاشة العريضة)
        settings.viewportMode = GeckoSessionSettings.VIEWPORT_MODE_DESKTOP
        settings.usePrivateMode = false
        settings.displayMode = GeckoSessionSettings.DISPLAY_MODE_BROWSER
        
        // 2. تزوير الهوية لتكون Windows 10 Chrome (لأنه الأكثر قبولاً)
        settings.userAgentOverride = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

        geckoSession = GeckoSession(settings)
        geckoSession.open(geckoRuntime)
        geckoView.setSession(geckoSession)

        // تحميل الصفحة الافتراضية
        geckoSession.loadUri("https://www.matecat.com/") 

        // برمجة زر الذهاب
        btnGo.setOnClickListener {
            loadUrlFromInput()
        }

        // برمجة زر Enter في الكيبورد
        urlInput.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_GO || actionId == EditorInfo.IME_ACTION_DONE) {
                loadUrlFromInput()
                true
            } else {
                false
            }
        }
    }

    private fun loadUrlFromInput() {
        var url = urlInput.text.toString().trim()
        if (url.isNotEmpty()) {
            if (!url.startsWith("http")) {
                url = "https://$url"
            }
            geckoSession.loadUri(url)
            // إخفاء الكيبورد (اختياري، يمكن إضافته لاحقاً)
        }
    }

    override fun onBackPressed() {
        // دعم زر الرجوع داخل المتصفح
        super.onBackPressed()
    }
}