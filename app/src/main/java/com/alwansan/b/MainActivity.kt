package com.alwansan.b

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import org.mozilla.geckoview.GeckoRuntime
import org.mozilla.geckoview.GeckoSession
import org.mozilla.geckoview.GeckoView

class MainActivity : AppCompatActivity() {

    private lateinit var geckoView: GeckoView
    private lateinit var geckoSession: GeckoSession
    private lateinit var geckoRuntime: GeckoRuntime

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        geckoView = findViewById(R.id.gecko_view)
        geckoRuntime = GeckoRuntime.create(this)
        geckoSession = GeckoSession()
        
        val settings = geckoSession.settings
        // تزوير الهوية لتظهر كويندوز
        settings.userAgentOverride = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
        settings.usePrivateMode = false 
        settings.displayMode = GeckoSession.Settings.DISPLAY_MODE_BROWSER
        
        geckoSession.open(geckoRuntime)
        geckoView.setSession(geckoSession)
        geckoSession.loadUri("https://www.google.com")
    }
}