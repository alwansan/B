package com.example.b

import android.app.Activity
import android.os.Bundle
import android.widget.ScrollView
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
    private lateinit var scrollView: ScrollView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // واجهة بسيطة لعرض السجلات (Logs)
        scrollView = ScrollView(this)
        logView = TextView(this)
        logView.text = "🚀 B Browser Launcher\nInitializing...\n"
        logView.setTextColor(0xFF00FF00.toInt()) // Green
        logView.setBackgroundColor(0xFF000000.toInt()) // Black
        logView.textSize = 12f
        logView.setPadding(20, 20, 20, 20)
        scrollView.addView(logView)
        setContentView(scrollView)

        val appPath = filesDir.absolutePath

        Executors.newSingleThreadExecutor().execute {
            try {
                // 1. استخراج PRoot
                extractAsset("proot", File(appPath, "proot"))
                
                // 2. استخراج RootFS (tar.gz)
                if (!File(appPath, "rootfs").exists()) {
                    log("📦 Extracting RootFS (Ubuntu)...")
                    extractTarGz("rootfs.tar.gz", File(appPath, "rootfs"))
                }

                // 3. استخراج Firefox (Double Compression Logic)
                if (!File(appPath, "firefox").exists()) {
                    log("🦊 Extracting Firefox (This is huge, wait)...")
                    extractFirefoxDoubleLayer(appPath)
                }

                log("✅ System Ready. Starting Engine...")
                Thread.sleep(1000) // راحة صغيرة
                
                // تشغيل المحرك
                val code = startLinux(appPath)
                log("🔄 Engine exited with code: $code")
                log("Check Logcat for 'B_Native' details.")

            } catch (e: Exception) {
                log("❌ CRITICAL ERROR: ${e.message}")
                e.printStackTrace()
            }
        }
    }

    private fun log(msg: String) {
        runOnUiThread {
            logView.append("\n$msg")
            scrollView.fullScroll(ScrollView.FOCUS_DOWN)
        }
    }

    private fun extractAsset(assetName: String, destFile: File) {
        if (destFile.exists()) return
        log("-> Copying $assetName...")
        assets.open(assetName).use { inp ->
            FileOutputStream(destFile).use { out -> inp.copyTo(out) }
        }
    }

    // فك ضغط .tar.gz (للـ RootFS)
    private fun extractTarGz(assetName: String, destDir: File) {
        destDir.mkdirs()
        try {
            val inputStream = GZIPInputStream(assets.open(assetName))
            val tarInput = TarArchiveInputStream(inputStream)
            var entry: TarArchiveEntry?
            while (tarInput.nextTarEntry.also { entry = it } != null) {
                val outputFile = File(destDir, entry!!.name)
                if (entry!!.isDirectory) {
                    outputFile.mkdirs()
                } else {
                    outputFile.parentFile?.mkdirs()
                    FileOutputStream(outputFile).use { out -> tarInput.copy(out, outputFile) }
                }
            }
        } catch (e: Exception) {
            log("Error extracting tar.gz: ${e.message}")
            throw e
        }
    }
    
    // دالة مساعدة لنسخ البيانات من TarStream إلى ملف
    private fun TarArchiveInputStream.copy(out: OutputStream, file: File) {
        val buffer = ByteArray(8192)
        var len: Int
        while (read(buffer).also { len = it } != -1) {
            out.write(buffer, 0, len)
        }
    }

    // فك ضغط Firefox المعقد (.tar.xz.tar)
    private fun extractFirefoxDoubleLayer(appPath: String) {
        val tempTarXz = File(appPath, "firefox_temp.tar.xz")
        val finalDir = File(appPath, "firefox")
        finalDir.mkdirs()

        // الطبقة الأولى: .tar -> .tar.xz
        log("   Step 1/2: Extracting outer TAR...")
        val assetStream = assets.open("firefox.tar.xz.tar")
        val outerTar = TarArchiveInputStream(BufferedInputStream(assetStream))
        var entry: TarArchiveEntry?
        
        // نبحث عن ملف firefox...tar.xz داخل الـ Tar الأول
        var found = false
        while (outerTar.nextTarEntry.also { entry = it } != null) {
            if (entry!!.name.endsWith(".tar.xz")) {
                log("   -> Found inner archive: ${entry!!.name}")
                FileOutputStream(tempTarXz).use { out -> 
                    val buffer = ByteArray(32768) // 32KB buffer for speed
                    var len: Int
                    while (outerTar.read(buffer).also { len = it } != -1) {
                        out.write(buffer, 0, len)
                    }
                }
                found = true
                break
            }
        }
        outerTar.close()
        
        if (!found) throw Exception("Inner firefox.tar.xz not found in asset!")

        // الطبقة الثانية: .tar.xz -> Folder
        log("   Step 2/2: Decompressing XZ & Untarring (Slow)...")
        val fin = FileInputStream(tempTarXz)
        val xzIn = XZCompressorInputStream(BufferedInputStream(fin))
        val innerTar = TarArchiveInputStream(xzIn)
        
        while (innerTar.nextTarEntry.also { entry = it } != null) {
            // إزالة المجلد العلوي إذا وجد (strip first component logic if needed)
            // هنا سنفترض أن الهيكل هو firefox/file...
            val outputFile = File(finalDir.parent, entry!!.name) // parent because archive likely contains 'firefox' folder
            
            if (entry!!.isDirectory) {
                outputFile.mkdirs()
            } else {
                outputFile.parentFile?.mkdirs()
                FileOutputStream(outputFile).use { out -> 
                    val buffer = ByteArray(8192)
                    var len: Int
                    while (innerTar.read(buffer).also { len = it } != -1) {
                        out.write(buffer, 0, len)
                    }
                }
            }
        }
        innerTar.close()
        tempTarXz.delete() // تنظيف
        log("✅ Firefox extracted successfully!")
    }
}