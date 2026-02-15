package com.example.b

import android.app.Activity
import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.TextView
import java.io.*
import java.util.concurrent.Executors

class LauncherActivity : Activity() {

    private lateinit var webView: WebView
    private lateinit var statusText: TextView
    private val appPath by lazy { filesDir.absolutePath }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val layout = android.widget.FrameLayout(this)
        webView = WebView(this).apply {
            settings.javaScriptEnabled = true
            settings.domStorageEnabled = true
            visibility = android.view.View.GONE
        }
        statusText = TextView(this).apply {
            text = "🚀 Initializing XoDos-Style Boot..."
            setTextColor(0xFF00FF00.toInt())
            setBackgroundColor(0xFF000000.toInt())
            setPadding(40, 40, 40, 40)
        }
        
        layout.addView(webView)
        layout.addView(statusText)
        setContentView(layout)

        Executors.newSingleThreadExecutor().execute {
            try {
                // 1. نقل الملفات (إذا لم تكن موجودة)
                installAsset("system.tar.gz")
                installAsset("install.sh")
                installAsset("novnc.tar.gz") // احتياط

                // 2. منح صلاحية التنفيذ للسكربت
                val installScript = File(appPath, "install.sh")
                installScript.setExecutable(true)

                // 3. تشغيل السكربت عبر Shell
                runOnUiThread { statusText.text = "⚙️ Executing Native Installer (Fast)..." }
                
                val pb = ProcessBuilder("sh", installScript.absolutePath)
                pb.directory(filesDir)
                pb.redirectErrorStream(true)
                val process = pb.start()
                
                // قراءة المخرجات لعرضها
                val reader = BufferedReader(InputStreamReader(process.inputStream))
                var line: String?
                while (reader.readLine().also { line = it } != null) {
                    val log = line
                    runOnUiThread { statusText.append("\n$log") }
                }
                process.waitFor()

                // 4. الانتقال للمتصفح
                runOnUiThread {
                    statusText.text = "✅ Booting UI..."
                    statusText.visibility = android.view.View.GONE
                    webView.visibility = android.view.View.VISIBLE
                    webView.loadUrl("http://localhost:6080/vnc.html?autoconnect=true")
                }

            } catch (e: Exception) {
                runOnUiThread { statusText.text = "❌ Error: ${e.message}" }
            }
        }
    }

    private fun installAsset(name: String) {
        val destFile = File(appPath, name)
        if (destFile.exists()) return // تخطي إذا موجود

        runOnUiThread { statusText.text = "📦 Copying $name..." }
        
        assets.open(name).use { input ->
            FileOutputStream(destFile).use { output ->
                input.copyTo(output)
            }
        }
    }
}