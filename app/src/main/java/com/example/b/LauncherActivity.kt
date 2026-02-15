package com.example.b

import android.app.Activity
import android.os.Bundle
import android.widget.TextView
import java.io.File
import java.io.FileOutputStream
import java.util.concurrent.Executors
import org.apache.commons.compress.archivers.tar.TarArchiveInputStream
import org.apache.commons.compress.compressors.xz.XZCompressorInputStream
import java.io.BufferedInputStream
import java.io.FileInputStream
import java.util.zip.GZIPInputStream

class LauncherActivity : Activity() {

    companion object { init { System.loadLibrary("bootstrap") } }
    external fun startLinux(appPath: String): Int

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val tv = TextView(this)
        tv.text = "Initializing System..."
        tv.setTextColor(0xFF00FF00.toInt())
        tv.setBackgroundColor(0xFF000000.toInt())
        setContentView(tv)

        val appPath = filesDir.absolutePath

        Executors.newSingleThreadExecutor().execute {
            try {
                // 1. نسخ PRoot & RootFS
                installAsset("proot", "$appPath/proot")
                if (!File("$appPath/rootfs.tar.gz").exists()) {
                     installAsset("rootfs.tar.gz", "$appPath/rootfs.tar.gz")
                }

                // 2. نسخ وفك ضغط Firefox
                // الملف هو .tar.xz.tar (tar يحتوي على tar.xz)
                if (!File("$appPath/firefox_archive.tar").exists()) {
                    runOnUiThread { tv.text = "Copying Firefox Archive..." }
                    installAsset("firefox.tar.xz.tar", "$appPath/firefox_archive.tar")
                }
                
                // سنقوم بفك الضغط في المرحلة القادمة باستخدام مكتبات Java أو System Tar
                // للمرحلة الحالية، تأكدنا أن الملف وصل للجهاز
                
                runOnUiThread { tv.text = "System Ready. Launching..." }
                startLinux(appPath)

            } catch (e: Exception) {
                runOnUiThread { tv.text = "Error: ${e.message}" }
            }
        }
    }

    private fun installAsset(name: String, path: String) {
        if (File(path).exists()) return
        assets.open(name).use { inp ->
            FileOutputStream(path).use { out -> inp.copyTo(out) }
        }
    }
}