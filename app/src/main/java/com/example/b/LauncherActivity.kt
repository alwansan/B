package com.example.b

import android.app.Activity
import android.os.Bundle
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.TextView
import java.io.*
import java.util.concurrent.Executors
import org.apache.commons.compress.archivers.tar.TarArchiveEntry
import org.apache.commons.compress.archivers.tar.TarArchiveInputStream
import java.util.zip.GZIPInputStream
import android.view.View

class LauncherActivity : Activity() {

    companion object { init { System.loadLibrary("bootstrap") } }
    external fun startLinux(appPath: String): Int

    private lateinit var webView: WebView
    private lateinit var statusText: TextView
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        statusText = TextView(this)
        statusText.text = "📦 Initializing First Run...\nExtracting System..."
        statusText.setBackgroundColor(0xFF000000.toInt())
        statusText.setTextColor(0xFF00FF00.toInt())
        statusText.textSize = 16f
        statusText.setPadding(40, 40, 40, 40)
        
        webView = WebView(this)
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.allowFileAccess = true
        webView.settings.builtInZoomControls = true
        webView.settings.displayZoomControls = false
        webView.visibility = View.GONE
        
        // حاوية لعرض النصوص أو الويب
        val layout = android.widget.FrameLayout(this)
        layout.addView(webView)
        layout.addView(statusText)
        setContentView(layout)

        val appPath = filesDir.absolutePath
        val systemDir = File(appPath, "system")

        Executors.newSingleThreadExecutor().execute {
            try {
                // 1. فك ضغط النظام (مرة واحدة فقط)
                if (!File(systemDir, "proot").exists()) {
                    runOnUiThread { statusText.text = "📦 Unpacking System Bundle (Please Wait)..." }
                    systemDir.mkdirs()
                    extractTarGz("system.tar.gz", systemDir)
                }
                
                // 2. التشغيل
                runOnUiThread { statusText.text = "🚀 Launching Linux Environment..." }
                
                // تشغيل النواة في الخلفية
                Executors.newSingleThreadExecutor().execute {
                    startLinux(appPath)
                }
                
                // 3. الانتظار حتى يجهز السيرفر (30 ثانية)
                for (i in 15 downTo 1) {
                    runOnUiThread { statusText.append("\n⏳ Starting Display... $i") }
                    Thread.sleep(1000)
                }
                
                // 4. عرض المتصفح
                runOnUiThread {
                    statusText.visibility = View.GONE
                    webView.visibility = View.VISIBLE
                    // noVNC يعمل على المنفذ 6080 (أو VNC المباشر إذا استخدمنا Alpine)
                    // في init.sh نحن نشغل Xvfb و Fluxbox، ونحتاج noVNC لربطهم بالويب
                    // إذا لم يكن noVNC مثبتاً في init.sh، قد نحتاج لإضافته
                    webView.loadUrl("http://localhost:6080/vnc.html?autoconnect=true&reconnect=true")
                }

            } catch (e: Exception) {
                runOnUiThread { statusText.text = "❌ Error: " + e.message + "\n" + e.stackTraceToString() }
            }
        }
    }

    private fun extractTarGz(asset: String, dest: File) {
        // نستخدم GZIP + Tar لفك الضغط
        assets.open(asset).use { ais ->
            GZIPInputStream(ais).use { gzip ->
                TarArchiveInputStream(gzip).use { tar ->
                    var entry: TarArchiveEntry?
                    while (tar.nextTarEntry.also { entry = it } != null) {
                        val f = File(dest, entry!!.name)
                        if (entry!!.isDirectory) {
                            f.mkdirs()
                        } else {
                            f.parentFile?.mkdirs()
                            FileOutputStream(f).use { out -> tar.copy(out) }
                        }
                    }
                }
            }
        }
    }

    private fun TarArchiveInputStream.copy(out: OutputStream) {
        val buf = ByteArray(8192)
        var len: Int
        while (read(buf).also { len = it } != -1) out.write(buf, 0, len)
    }
}