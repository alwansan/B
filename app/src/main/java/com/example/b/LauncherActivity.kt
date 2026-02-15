package com.example.b

import android.app.Activity
import android.os.Bundle
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
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
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        webView = WebView(this)
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.allowFileAccess = true
        webView.settings.builtInZoomControls = true
        webView.settings.displayZoomControls = false
        
        setContentView(webView)

        val appPath = filesDir.absolutePath
        val statusFile = File(appPath, "rootfs/opt/status.html")

        // 1. إنشاء ملف الحالة فوراً لتجنب ERR_FILE_NOT_FOUND
        createInitialStatusPage(statusFile)
        
        // 2. تحميل الصفحة المحلية
        webView.loadUrl("file://" + statusFile.absolutePath)

        Executors.newSingleThreadExecutor().execute {
            try {
                installAssets(appPath)
                
                // بدء تشغيل النظام
                startLinux(appPath)

            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    private fun createInitialStatusPage(file: File) {
        file.parentFile?.mkdirs()
        try {
            // نستخدم دمج النصوص لتجنب أخطاء بايثون
            val html = "<html><body style='background:black;color:white;padding:20px;font-family:monospace;'>" +
                       "<h2>🚀 System Initializing...</h2>" +
                       "<p>Please wait while we unpack the system resources.</p>" +
                       "<script>setInterval(function(){window.location.reload();}, 3000);</script>" +
                       "</body></html>"
            
            FileOutputStream(file).use { it.write(html.toByteArray()) }
        } catch (e: Exception) { e.printStackTrace() }
    }

    private fun installAssets(appPath: String) {
        copyAsset("proot", File(appPath, "proot"))
        copyAsset("setup.sh", File(appPath, "setup.sh"))
        copyAsset("novnc.tar.gz", File(appPath, "novnc.tar.gz"))
        
        if (!File(appPath, "rootfs").exists()) {
            extractTarXz("rootfs.tar.xz", File(appPath, "rootfs"))
        }
        
        if (!File(appPath, "firefox").exists()) {
            extractFirefoxDoubleLayer(appPath)
        }
    }
    
    private fun copyAsset(name: String, dest: File) {
        if (dest.exists()) return
        assets.open(name).use { i -> FileOutputStream(dest).use { o -> i.copyTo(o) } }
    }
    
    private fun extractTarXz(asset: String, dest: File) {
        dest.mkdirs()
        XZCompressorInputStream(assets.open(asset)).use { xz ->
            TarArchiveInputStream(xz).use { tar ->
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
        } catch (e: Exception) {}
    }
}