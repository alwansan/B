package com.example.b

import android.app.Activity
import android.os.Bundle
import android.webkit.WebView
import android.widget.TextView
import java.io.*
import java.util.concurrent.Executors
import org.apache.commons.compress.archivers.tar.TarArchiveEntry
import org.apache.commons.compress.archivers.tar.TarArchiveInputStream
import org.apache.commons.compress.compressors.xz.XZCompressorInputStream
import java.util.zip.GZIPInputStream

class LauncherActivity : Activity() {

    companion object { init { System.loadLibrary("bootstrap") } }
    external fun startLinux(appPath: String): Int

    private lateinit var logView: TextView
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // 1. واجهة بسيطة لعرض الحالة (سنستبدلها بالمتصفح لاحقاً)
        logView = TextView(this)
        logView.text = "🚀 Preparing Firefox Environment...\n"
        logView.setTextColor(0xFF00FF00.toInt())
        logView.setBackgroundColor(0xFF000000.toInt())
        logView.textSize = 14f
        logView.setPadding(30, 30, 30, 30)
        setContentView(logView)

        // 2. مانع الانهيار (Crash Handler)
        Thread.setDefaultUncaughtExceptionHandler { _, e ->
            runOnUiThread {
                logView.append("\n❌ CRASH DETECTED:\n${e.message}\n")
                e.printStackTrace()
            }
        }

        val appPath = filesDir.absolutePath

        Executors.newSingleThreadExecutor().execute {
            try {
                installAssets(appPath)
                
                log("✅ Assets Ready. Installing Linux Packages (Internet Required)...")
                log("⚠️ This step needs 5-10 minutes on first run.")
                
                // تشغيل النظام
                startLinux(appPath)

            } catch (e: Exception) {
                log("❌ Error: ${e.message}")
            }
        }
    }

    private fun log(msg: String) {
        runOnUiThread { logView.append("\n$msg") }
    }

    private fun installAssets(appPath: String) {
        copyAsset("proot", File(appPath, "proot"))
        copyAsset("setup.sh", File(appPath, "setup.sh"))
        
        if (!File(appPath, "rootfs").exists()) {
            log("📦 Extracting RootFS...")
            extractTarGz("rootfs.tar.gz", File(appPath, "rootfs"))
        }
        
        if (!File(appPath, "firefox").exists()) {
            log("🦊 Extracting Firefox...")
            extractFirefoxDoubleLayer(appPath)
        }
    }

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
    }
}