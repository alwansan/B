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

        geckoView = findViewById(R.id.gecko_view)
        urlInput = findViewById(R.id.url_input)
        btnGo = findViewById(R.id.btn_go)

        // إعداد المحرك
        geckoRuntime = GeckoRuntime.create(this)
        
        // إعدادات الجلسة لخداع Matecat
        val settings = GeckoSessionSettings.Builder()
            .usePrivateMode(false)
            // 1. هوية ويندوز 10 (كروم)
            .userAgentOverride("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
            // 2. تفعيل وضع سطح المكتب (يجعل العرض يبدو عريضاً)
            .viewportMode(GeckoSessionSettings.VIEWPORT_MODE_DESKTOP)
            // 3. وضع التصفح العادي
            .displayMode(GeckoSessionSettings.DISPLAY_MODE_BROWSER)
            .build()

        geckoSession = GeckoSession(settings)
        geckoSession.open(geckoRuntime)
        geckoView.setSession(geckoSession)

        // فتح Matecat مباشرة للتجربة
        loadUrl("https://www.matecat.com/")

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
            if (!finalUrl.startsWith("http")) {
                finalUrl = "https://$finalUrl"
            }
            geckoSession.loadUri(finalUrl)
        }
    }
}