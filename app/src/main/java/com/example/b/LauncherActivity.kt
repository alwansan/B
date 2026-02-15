package com.example.b

import android.app.Activity
import android.os.Bundle
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
        statusText.text = "📦 Initializing..."
        statusText.setBackgroundColor(0xFF000000.toInt())
        statusText.setTextColor(0xFF00FF00.toInt())
        
        webView = WebView(this)
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.allowFileAccess = true
        webView.visibility = View.GONE
        
        val layout = android.widget.FrameLayout(this)
        layout.addView(webView)
        layout.addView(statusText)
        setContentView(layout)

        val appPath = filesDir.absolutePath
        val systemDir = File(appPath, "system")

        Executors.newSingleThreadExecutor().execute {
            try {
                if (!File(systemDir, "proot").exists()) {
                    runOnUiThread { statusText.text = "📦 Extracting System (One Time)..." }
                    systemDir.mkdirs()
                    extractTarGz("system.tar.gz", systemDir)
                }
                
                runOnUiThread { statusText.text = "🚀 Launching Linux..." }
                Executors.newSingleThreadExecutor().execute { startLinux(appPath) }
                
                for (i in 15 downTo 1) {
                    runOnUiThread { statusText.text = "⏳ Waiting... $i" }
                    Thread.sleep(1000)
                }
                
                runOnUiThread {
                    statusText.visibility = View.GONE
                    webView.visibility = View.VISIBLE
                    webView.loadUrl("http://localhost:6080/vnc.html?autoconnect=true")
                }

            } catch (e: Exception) {
                runOnUiThread { statusText.text = "❌ Error: " + e.message }
            }
        }
    }

    private fun extractTarGz(asset: String, dest: File) {
        assets.open(asset).use { ais ->
            GZIPInputStream(ais).use { gzip ->
                TarArchiveInputStream(gzip).use { tar ->
                    var entry: TarArchiveEntry?
                    while (tar.nextTarEntry.also { entry = it } != null) {
                        val f = File(dest, entry!!.name)
                        if (entry!!.isDirectory) f.mkdirs()
                        else {
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