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
import org.apache.commons.compress.archivers.tar.TarArchiveEntry
import org.apache.commons.compress.archivers.tar.TarArchiveInputStream
import org.apache.commons.compress.compressors.xz.XZCompressorInputStream
import java.util.zip.GZIPInputStream

class LauncherActivity : Activity() {

    companion object { init { System.loadLibrary("bootstrap") } }
    external fun startLinux(appPath: String): Int

    private lateinit var webView: WebView
    private lateinit var logView: TextView
    private lateinit var container: FrameLayout
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        container = FrameLayout(this)
        
        // 1. شاشة السجلات (تظهر أولاً)
        logView = TextView(this)
        logView.text = "🚀 Initializing B Browser...\n"
        logView.setTextColor(0xFF00FF00.toInt())
        logView.setBackgroundColor(0xFF000000.toInt())
        logView.setPadding(30, 30, 30, 30)
        
        // 2. المتصفح (يظهر لاحقاً)
        webView = WebView(this)
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.allowFileAccess = true
        webView.webViewClient = WebViewClient()
        webView.visibility = View.GONE // مخفي في البداية
        
        container.addView(webView)
        container.addView(logView)
        setContentView(container)

        val appPath = filesDir.absolutePath

        Executors.newSingleThreadExecutor().execute {
            try {
                installAssets(appPath)
                
                log("✅ Starting Linux Engine...")
                
                // تشغيل Linux في خيط منفصل (Thread)
                Executors.newSingleThreadExecutor().execute {
                    startLinux(appPath)
                }
                
                // مراقبة التشغيل والتحويل إلى WebView
                monitorAndSwitch()

            } catch (e: Exception) {
                log("❌ Error: ${e.message}")
            }
        }
    }

    private fun monitorAndSwitch() {
        // ننتظر حتى يعمل السيرفر (نفحص المنفذ أو ننتظر وقتاً)
        // للتبسيط سننتظر 15 ثانية ثم نحاول الاتصال بـ noVNC
        for (i in 15 downTo 1) {
            log("⏳ Waiting for X11 System... $i")
            Thread.sleep(1000)
        }
        
        runOnUiThread {
            logView.visibility = View.GONE
            webView.visibility = View.VISIBLE
            // الرابط السحري: noVNC يتصل بـ VNC ويعرضه كصفحة ويب
            webView.loadUrl("http://localhost:6080/vnc.html?autoconnect=true&reconnect=true")
        }
    }

    private fun log(msg: String) {
        runOnUiThread { logView.append("\n$msg") }
    }

    private fun installAssets(appPath: String) {
        copyAsset("proot", File(appPath, "proot"))
        copyAsset("setup.sh", File(appPath, "setup.sh"))
        copyAsset("novnc.tar.gz", File(appPath, "novnc.tar.gz"))
        
        if (!File(appPath, "rootfs").exists()) {
            log("📦 Extracting RootFS...")
            extractTarGz("rootfs.tar.gz", File(appPath, "rootfs"))
        }
        
        if (!File(appPath, "firefox").exists()) {
            log("🦊 Extracting Firefox...")
            extractFirefoxDoubleLayer(appPath)
        }
    }
    
    // دوال النسخ والفك (نفس السابقة)
    private fun copyAsset(name: String, dest: File) {
        if (dest.exists()) return
        assets.open(name).use { i -> FileOutputStream(dest).use { o -> i.copyTo(o) } }
    }
    
    private fun extractTarGz(asset: String, dest: File) {
        dest.mkdirs()
        GZIPInputStream(assets.open(asset)).use { gzip ->
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
    
    private fun TarArchiveInputStream.copy(out: OutputStream) {
        val buf = ByteArray(8192)
        var len: Int
        while (read(buf).also { len = it } != -1) out.write(buf, 0, len)
    }

    private fun extractFirefoxDoubleLayer(appPath: String) {
        val temp = File(appPath, "temp.txz")
        val finalDir = File(appPath, "firefox")
        
        // التحقق من وجود الملف أولاً
        try {
            assets.open("firefox.tar.xz.tar").use { i -> 
                TarArchiveInputStream(BufferedInputStream(i)).use { tar ->
                    var e: TarArchiveEntry?
                    while (tar.nextTarEntry.also { e = it } != null) {
                        if (e!!.name.endsWith(".tar.xz")) {
                            FileOutputStream(temp).use { out -> tar.copy(out) }
                            break
                        }
                    }
                }
            }
            
            XZCompressorInputStream(BufferedInputStream(FileInputStream(temp))).use { xz ->
                TarArchiveInputStream(xz).use { tar ->
                    var e: TarArchiveEntry?
                    while (tar.nextTarEntry.also { e = it } != null) {
                        val f = File(finalDir.parent, e!!.name)
                        if (e!!.isDirectory) f.mkdirs()
                        else {
                            f.parentFile?.mkdirs()
                            FileOutputStream(f).use { out -> tar.copy(out) }
                        }
                    }
                }
            }
            temp.delete()
        } catch (e: Exception) {
            log("⚠️ Warning: Firefox extraction failed or file missing. Skipping.")
        }
    }
}