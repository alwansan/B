package com.example.b

import android.app.Activity
import android.os.Bundle
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.TextView
import android.widget.FrameLayout
import android.view.View
import java.io.*
import java.util.concurrent.Executors

class LauncherActivity : Activity() {

    companion object { init { System.loadLibrary("bootstrap") } }
    external fun startLinux(appPath: String): Int

    private lateinit var webView: WebView
    private lateinit var statusText: TextView
    private lateinit var container: FrameLayout
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        container = FrameLayout(this)
        
        // شاشة الحالة (نصية)
        statusText = TextView(this)
        statusText.text = "⏳ Initializing..."
        statusText.setTextColor(0xFF00FF00.toInt())
        statusText.setBackgroundColor(0xFF000000.toInt())
        statusText.setPadding(20, 20, 20, 20)
        
        // المتصفح
        webView = WebView(this)
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.allowFileAccess = true
        webView.webViewClient = object : WebViewClient() {
            override fun onReceivedError(view: WebView?, errorCode: Int, description: String?, failingUrl: String?) {
                // إذا فشل تحميل noVNC، نعرض ملف اللوج بدلاً من شاشة بيضاء
                view?.loadUrl("file://" + filesDir.absolutePath + "/rootfs/opt/status.html")
            }
        }
        
        container.addView(webView)
        container.addView(statusText)
        setContentView(container)

        val appPath = filesDir.absolutePath

        Executors.newSingleThreadExecutor().execute {
            try {
                // 1. تشغيل Linux
                runOnUiThread { statusText.text = "🚀 Booting Linux Kernel..." }
                Executors.newSingleThreadExecutor().execute {
                    startLinux(appPath)
                }
                
                // 2. الانتظار الذكي
                for (i in 30 downTo 1) {
                    runOnUiThread { statusText.text = "⏳ Waiting for Desktop... $i" }
                    Thread.sleep(1000)
                }
                
                // 3. محاولة العرض
                runOnUiThread {
                    statusText.visibility = View.GONE
                    // نحاول فتح noVNC
                    webView.loadUrl("http://localhost:6080/vnc.html?autoconnect=true")
                }

            } catch (e: Exception) {
                runOnUiThread { statusText.text = "❌ Error: ${e.message}" }
            }
        }
    }
}