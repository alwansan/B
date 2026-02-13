package com.alwansan.b

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import org.mozilla.geckoview.GeckoRuntime
import org.mozilla.geckoview.GeckoSession
import org.mozilla.geckoview.GeckoSessionSettings 
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
        
        // استخدام الإعدادات الافتراضية بدون تعديل القيم المقفلة
        geckoSession = GeckoSession()
        
        val settings = geckoSession.settings
        // settings.usePrivateMode = false 
        
        // التصحيح: استخدام اسم الكلاس الصحيح GeckoSessionSettings
        settings.displayMode = GeckoSessionSettings.DISPLAY_MODE_BROWSER
        
        geckoSession.open(geckoRuntime)
        geckoView.setSession(geckoSession)
        
        // تحميل موقع يدعم الماوس والكيبورد
        geckoSession.loadUri("https://www.google.com")
    }
}