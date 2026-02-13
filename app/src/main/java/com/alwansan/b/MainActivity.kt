package com.alwansan.b

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import org.mozilla.geckoview.GeckoRuntime
import org.mozilla.geckoview.GeckoSession
import org.mozilla.geckoview.GeckoView
import org.mozilla.geckoview.GeckoSessionSettings

class MainActivity : AppCompatActivity() {

    private lateinit var geckoView: GeckoView
    private lateinit var geckoSession: GeckoSession
    private lateinit var geckoRuntime: GeckoRuntime

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        geckoView = findViewById(R.id.gecko_view)
        
        // إعداد المحرك
        geckoRuntime = GeckoRuntime.create(this)
        
        // إعداد الجلسة مع إجبار وضع سطح المكتب
        val settings = GeckoSessionSettings.Builder()
            .usePrivateMode(false)
            .viewportMode(GeckoSessionSettings.VIEWPORT_MODE_DESKTOP) // 🔥 السر هنا
            .userAgentOverride("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36") // 🔥 هوية ويندوز
            .build()

        geckoSession = GeckoSession(settings)
        geckoSession.open(geckoRuntime)
        geckoView.setSession(geckoSession)
        
        // فتح الموقع العنيد
        geckoSession.loadUri("https://www.matecat.com/")
    }
}