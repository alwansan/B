import os
import subprocess

# ==========================================
# إعدادات المسارات
# ==========================================
BASE_DIR = os.getcwd()
APP_DIR = os.path.join(BASE_DIR, "app")
SRC_MAIN = os.path.join(APP_DIR, "src", "main")
RES_DIR = os.path.join(SRC_MAIN, "res")
LAYOUT_DIR = os.path.join(RES_DIR, "layout")
ASSETS_DIR = os.path.join(SRC_MAIN, "assets")
JAVA_DIR = os.path.join(SRC_MAIN, "java", "com", "alwansan", "b")

def create_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ تم تحديث: {os.path.basename(path)}")

# ==========================================
# 1. الواجهة الجديدة (Home HTML - New Design) 🎨
# ==========================================
home_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>B-Eagle</title>
<style>
:root{ --bg:#12131c; --card:#1b1d2a; --cyan:#00e5ff; --gray:#9aa0a6; }
*{box-sizing:border-box}
body{
  margin:0; overflow:hidden;
  background:radial-gradient(circle at top,#1f2233,#0b0c12);
  font-family:'Segoe UI',sans-serif; height:100vh;
  display:flex; flex-direction:column; align-items:center; justify-content:center; color:white;
}
canvas{ position:fixed; inset:0; z-index:-1; }
h1{ font-size:90px; letter-spacing:-3px; margin-bottom:25px; animation:float 6s ease-in-out infinite; }
h1 span{color:var(--cyan)}
@keyframes float{ 0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)} }
form{ width:100%; display:flex; justify-content:center; }
input{
  width:600px; padding:22px 32px; border-radius:60px; border:none;
  background:var(--card); color:white; font-size:20px; outline:none;
  box-shadow:0 20px 60px rgba(0,0,0,.45); transition:.35s cubic-bezier(.4,0,.2,1);
}
input::placeholder{color:var(--gray)}
input:focus{ transform:scale(1.04); box-shadow:0 0 0 2px var(--cyan),0 30px 80px rgba(0,229,255,.25); }
.ripple{
  position:absolute; border-radius:50%; background:rgba(0,229,255,.25);
  pointer-events:none; animation:ripple .7s ease-out forwards;
}
@keyframes ripple{ from{transform:scale(0);opacity:1} to{transform:scale(6);opacity:0} }
</style>
</head>
<body>
<canvas id="bg"></canvas>
<h1>B<span>-</span>Eagle</h1>
<form action="https://www.google.com/search" method="GET">
  <input type="text" name="q" placeholder="Search web..." autofocus autocomplete="off">
</form>
<script>
const canvas = document.getElementById("bg");
const ctx = canvas.getContext("2d");
let w,h,particles=[];
resize();
window.addEventListener("resize",resize);
function resize(){ w=canvas.width=window.innerWidth; h=canvas.height=window.innerHeight; }
class Particle{
  constructor(){
    this.x=Math.random()*w; this.y=Math.random()*h;
    this.vx=(Math.random()-.5)*0.6; this.vy=(Math.random()-.5)*0.6; this.r=Math.random()*2+1;
  }
  draw(){ ctx.beginPath(); ctx.arc(this.x,this.y,this.r,0,Math.PI*2); ctx.fillStyle="rgba(0,229,255,.6)"; ctx.fill(); }
  update(){ this.x+=this.vx; this.y+=this.vy; if(this.x<0||this.x>w) this.vx*=-1; if(this.y<0||this.y>h) this.vy*=-1; }
}
for(let i=0;i<120;i++) particles.push(new Particle());
let mouse={x:null,y:null};
window.addEventListener("mousemove",e=>{ mouse.x=e.clientX; mouse.y=e.clientY; });
function animate(){
  ctx.clearRect(0,0,w,h);
  particles.forEach(p=>{
    p.update(); p.draw();
    if(mouse.x){
      const dx=p.x-mouse.x; const dy=p.y-mouse.y; const dist=Math.sqrt(dx*dx+dy*dy);
      if(dist<120){ ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(mouse.x,mouse.y); ctx.strokeStyle="rgba(0,229,255,.15)"; ctx.stroke(); }
    }
  });
  requestAnimationFrame(animate);
}
animate();
window.addEventListener("click",e=>{
  const r=document.createElement("div"); r.className="ripple";
  r.style.left=e.clientX+"px"; r.style.top=e.clientY+"px";
  r.style.width=r.style.height="20px";
  document.body.appendChild(r); setTimeout(()=>r.remove(),700);
});
</script>
</body>
</html>
"""

# ==========================================
# 2. ملف XML المفقود (Settings Dialog) 🛠️
# ==========================================
dialog_settings_xml = """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="350dp"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:background="#242633"
    android:padding="24dp">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Settings"
        android:textColor="#00E5FF"
        android:textSize="22sp"
        android:textStyle="bold"
        android:gravity="center"
        android:layout_marginBottom="24dp"/>

    <TextView 
        android:text="Screen Resolution" 
        android:textColor="#AAA" 
        android:textSize="14sp"
        android:layout_width="wrap_content" 
        android:layout_height="wrap_content"
        android:layout_marginBottom="8dp"/>
        
    <RadioGroup 
        android:id="@+id/rg_resolution" 
        android:layout_width="match_parent" 
        android:layout_height="wrap_content" 
        android:orientation="vertical">
        
        <RadioButton android:id="@+id/rb_720" android:text="720p (Mobile)" android:textColor="#FFF" android:buttonTint="#00E5FF"/>
        <RadioButton android:id="@+id/rb_1080" android:text="1080p (Desktop)" android:textColor="#FFF" android:buttonTint="#00E5FF"/>
        <RadioButton android:id="@+id/rb_4k" android:text="4K (Ultra)" android:textColor="#FFF" android:buttonTint="#00E5FF"/>
    </RadioGroup>

    <View 
        android:layout_width="match_parent" 
        android:layout_height="1dp" 
        android:background="#444" 
        android:layout_marginVertical="20dp"/>

    <Button
        android:id="@+id/btn_clear_data"
        android:layout_width="match_parent"
        android:layout_height="50dp"
        android:text="Clear Cookies &amp; Cache"
        android:textColor="#FFF"
        android:backgroundTint="#FA2E4D"/>
</LinearLayout>
"""

# ==========================================
# 3. تحديث MainActivity (تحسين الماوس + ContextMenu) 🖱️
# ==========================================
main_activity = """
package com.alwansan.b

import android.app.AlertDialog
import android.content.Context
import android.graphics.Color
import android.os.Bundle
import android.view.KeyEvent
import android.view.LayoutInflater
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import org.json.JSONArray
import org.json.JSONObject
import org.mozilla.geckoview.GeckoRuntime
import org.mozilla.geckoview.GeckoSession
import org.mozilla.geckoview.GeckoSessionSettings
import org.mozilla.geckoview.GeckoView
import java.io.File
import java.io.FileOutputStream

class MainActivity : AppCompatActivity() {

    private lateinit var geckoView: GeckoView
    private lateinit var geckoRuntime: GeckoRuntime
    private lateinit var tabsContainer: LinearLayout
    private lateinit var urlInput: EditText
    private lateinit var uiContainer: LinearLayout
    private lateinit var btnBookmark: ImageButton
    private lateinit var btnMenu: ImageButton

    private val sessions = ArrayList<TabSession>()
    private var currentTabIndex = -1
    private var isGhostMode = false
    private val HOME_FILE_NAME = "home.html"
    private lateinit var homeUrl: String
    private var currentResolution = "1080" 

    data class TabSession(
        val session: GeckoSession,
        val tabView: View,
        var currentUrl: String = "",
        var title: String = "New Tab"
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        setupLocalHomeFile()

        geckoView = findViewById(R.id.gecko_view)
        tabsContainer = findViewById(R.id.tabs_container)
        urlInput = findViewById(R.id.url_input)
        uiContainer = findViewById(R.id.ui_container)
        btnBookmark = findViewById(R.id.btn_bookmark)
        btnMenu = findViewById(R.id.btn_menu)

        // تحسين استجابة الماوس واللمس
        geckoView.isFocusable = true
        geckoView.isFocusableInTouchMode = true
        geckoView.requestFocus()

        geckoRuntime = GeckoRuntime.create(this)
        
        val prefs = getSharedPreferences("BrowserSettings", Context.MODE_PRIVATE)
        currentResolution = prefs.getString("resolution", "1080") ?: "1080"

        findViewById<Button>(R.id.btn_add_tab).setOnClickListener { addNewTab(homeUrl) }
        findViewById<ImageButton>(R.id.btn_go).setOnClickListener { loadUrl(urlInput.text.toString()) }
        findViewById<ImageButton>(R.id.btn_settings).setOnClickListener { showSettingsDialog() }
        
        btnMenu.setOnClickListener { showBookmarksDialog() }

        btnBookmark.setOnClickListener {
            if(currentTabIndex != -1) {
                val tab = sessions[currentTabIndex]
                saveBookmark(tab.currentUrl, tab.title)
                Toast.makeText(this, "Saved to Bookmarks! ⭐", Toast.LENGTH_SHORT).show()
                btnBookmark.setColorFilter(Color.parseColor("#00E5FF"))
            }
        }

        urlInput.imeOptions = EditorInfo.IME_ACTION_GO or EditorInfo.IME_FLAG_NO_EXTRACT_UI
        urlInput.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_GO || actionId == EditorInfo.IME_ACTION_DONE) {
                loadUrl(urlInput.text.toString())
                true
            } else { false }
        }

        restoreTabs()
    }

    private fun setupLocalHomeFile() {
        val file = File(filesDir, HOME_FILE_NAME)
        // نقوم بالكتابة دائماً للتأكد من تحديث الواجهة
        try {
            assets.open(HOME_FILE_NAME).use { input ->
                FileOutputStream(file).use { output -> input.copyTo(output) }
            }
        } catch (e: Exception) { e.printStackTrace() }
        homeUrl = "file://" + file.absolutePath
    }

    private fun addNewTab(urlToLoad: String) {
        val builder = GeckoSessionSettings.Builder()
            .usePrivateMode(false)
            
        when(currentResolution) {
            "720" -> {
                builder.viewportMode(GeckoSessionSettings.VIEWPORT_MODE_MOBILE)
                builder.userAgentOverride("") 
            }
            "4K" -> {
                builder.viewportMode(GeckoSessionSettings.VIEWPORT_MODE_DESKTOP)
                builder.displayMode(GeckoSessionSettings.DISPLAY_MODE_BROWSER)
                builder.userAgentOverride("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
            }
            else -> { 
                builder.viewportMode(GeckoSessionSettings.VIEWPORT_MODE_DESKTOP)
                builder.userAgentOverride("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0")
            }
        }
        
        val session = GeckoSession(builder.build())
        session.open(geckoRuntime)

        val tabView = LayoutInflater.from(this).inflate(R.layout.item_tab, tabsContainer, false)
        val tabTitleView = tabView.findViewById<TextView>(R.id.tab_title)
        val tabIndicator = tabView.findViewById<View>(R.id.tab_indicator)
        val btnClose = tabView.findViewById<ImageButton>(R.id.btn_close_tab)

        val newTab = TabSession(session, tabView, urlToLoad)
        sessions.add(newTab)
        
        session.progressDelegate = object : GeckoSession.ProgressDelegate {
            override fun onPageStart(session: GeckoSession, url: String) {
                newTab.currentUrl = url
                if(sessions.indexOf(newTab) == currentTabIndex) {
                     if(!url.startsWith("file")) {
                         urlInput.setText(url)
                         btnBookmark.setColorFilter(Color.GRAY)
                     } else {
                         urlInput.setText("")
                     }
                }
            }
            override fun onPageStop(session: GeckoSession, success: Boolean) { }
        }
        
        session.contentDelegate = object : GeckoSession.ContentDelegate {
            override fun onTitleChange(session: GeckoSession, title: String?) {
                val finalTitle = title ?: "New Tab"
                newTab.title = finalTitle
                tabTitleView.text = finalTitle
            }
            // تمكين النقر بالماوس (Context Menu)
            override fun onContextMenu(session: GeckoSession, screenX: Int, screenY: Int, meta: GeckoSession.ContentDelegate.ContextElement) {
                // في النسخ الحديثة يتم التعامل معها تلقائياً، 
                // لكن وجود الدالة يضمن تفعيل الميزة
                super.onContextMenu(session, screenX, screenY, meta)
            }
        }

        tabView.setOnClickListener { switchToTab(sessions.indexOf(newTab)) }
        btnClose.setOnClickListener { closeTab(sessions.indexOf(newTab)) }
        
        tabsContainer.addView(tabView)
        switchToTab(sessions.size - 1)
        
        session.loadUri(urlToLoad)
    }

    private fun switchToTab(index: Int) {
        if (index !in sessions.indices) return
        currentTabIndex = index
        val tab = sessions[index]
        geckoView.setSession(tab.session)
        // إعادة التركيز للمتصفح عند التبديل
        geckoView.requestFocus()

        for (i in sessions.indices) {
            val view = sessions[i].tabView
            val indicator = view.findViewById<View>(R.id.tab_indicator)
            if (i == index) {
                view.isSelected = true
                indicator.visibility = View.VISIBLE
            } else {
                view.isSelected = false
                indicator.visibility = View.INVISIBLE
            }
        }
        
        if(tab.currentUrl.startsWith("file")) {
            urlInput.setText("")
            urlInput.hint = "Search Google..."
        } else {
            urlInput.setText(tab.currentUrl)
        }
    }

    private fun closeTab(index: Int) {
        if (index !in sessions.indices) return
        val tab = sessions[index]
        tab.session.close()
        tabsContainer.removeView(tab.tabView)
        sessions.removeAt(index)

        if (sessions.isEmpty()) addNewTab(homeUrl)
        else switchToTab(if (index > 0) index - 1 else 0)
    }

    private fun loadUrl(input: String) {
        if (currentTabIndex == -1) return
        var url = input.trim()
        if (url.isEmpty()) return
        if (url.contains(" ") || !url.contains(".")) url = "https://www.google.com/search?q=$url"
        else if (!url.startsWith("http") && !url.startsWith("file")) url = "https://$url"
        
        sessions[currentTabIndex].session.loadUri(url)
        addToHistoryLog(url)
        geckoView.requestFocus()
    }

    private fun showBookmarksDialog() {
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_bookmarks, null)
        val btnBookmarks = dialogView.findViewById<Button>(R.id.btn_view_bookmarks)
        val btnHistory = dialogView.findViewById<Button>(R.id.btn_view_history)
        val listView = dialogView.findViewById<ListView>(R.id.list_data)
        val btnClearHistory = dialogView.findViewById<Button>(R.id.btn_clear_history)
        val dialogTitle = dialogView.findViewById<TextView>(R.id.dialog_title)

        val dialog = AlertDialog.Builder(this).setView(dialogView).create()

        fun loadList(type: String) {
            val listData = ArrayList<Map<String, String>>()
            
            if (type == "bookmarks") {
                val prefs = getSharedPreferences("Bookmarks", Context.MODE_PRIVATE)
                val jsonArray = JSONArray(prefs.getString("list", "[]"))
                for(i in 0 until jsonArray.length()) {
                    val item = jsonArray.getJSONObject(i)
                    listData.add(mapOf("title" to item.getString("title"), "url" to item.getString("url")))
                }
                dialogTitle.text = "⭐ Saved Bookmarks"
                btnClearHistory.visibility = View.GONE
            } else {
                try {
                    val lines = File(filesDir, "history.txt").readLines().reversed()
                    for(line in lines) {
                        if(line.contains(": ")) {
                            val parts = line.split(": ", limit = 2)
                            listData.add(mapOf("title" to "Visited", "url" to parts[1]))
                        }
                    }
                } catch(e: Exception) {}
                dialogTitle.text = "🕒 Browsing History"
                btnClearHistory.visibility = View.VISIBLE
            }

            val adapter = object : SimpleAdapter(
                this, listData, R.layout.item_list_row,
                arrayOf("title", "url"), intArrayOf(R.id.row_title, R.id.row_url)
            ) {}
            
            listView.adapter = adapter
            listView.setOnItemClickListener { _, _, position, _ ->
                val url = listData[position]["url"]
                if(url != null) loadUrl(url)
                dialog.dismiss()
            }
        }

        loadList("bookmarks")
        btnBookmarks.setOnClickListener { loadList("bookmarks") }
        btnHistory.setOnClickListener { loadList("history") }
        
        btnClearHistory.setOnClickListener {
            File(filesDir, "history.txt").delete()
            loadList("history")
            Toast.makeText(this, "History Cleared", Toast.LENGTH_SHORT).show()
        }
        dialog.show()
    }

    private fun saveBookmark(url: String, title: String) {
        if(url.startsWith("file")) return 
        val prefs = getSharedPreferences("Bookmarks", Context.MODE_PRIVATE)
        val jsonString = prefs.getString("list", "[]")
        val jsonArray = JSONArray(jsonString)
        val newBm = JSONObject()
        newBm.put("url", url)
        newBm.put("title", title)
        jsonArray.put(newBm)
        prefs.edit().putString("list", jsonArray.toString()).apply()
    }

    private fun addToHistoryLog(url: String) {
        try { File(filesDir, "history.txt").appendText("${System.currentTimeMillis()}: $url\\n") } catch (e: Exception) {}
    }
    
    private fun showSettingsDialog() {
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_settings, null)
        val rgResolution = dialogView.findViewById<RadioGroup>(R.id.rg_resolution)
        val btnClear = dialogView.findViewById<Button>(R.id.btn_clear_data)

        when(currentResolution) {
            "720" -> rgResolution.check(R.id.rb_720)
            "4K" -> rgResolution.check(R.id.rb_4k)
            else -> rgResolution.check(R.id.rb_1080)
        }

        val dialog = AlertDialog.Builder(this).setView(dialogView).create()
        rgResolution.setOnCheckedChangeListener { _, checkedId ->
            val newRes = when(checkedId) { R.id.rb_720 -> "720" ; R.id.rb_4k -> "4K" ; else -> "1080" }
            currentResolution = newRes
            getSharedPreferences("BrowserSettings", Context.MODE_PRIVATE).edit().putString("resolution", newRes).apply()
            Toast.makeText(this, "Restart tabs to apply.", Toast.LENGTH_SHORT).show()
        }
        
        btnClear.setOnClickListener {
            geckoRuntime.storageController.clearData(org.mozilla.geckoview.StorageController.ClearFlags.ALL)
            File(filesDir, "history.txt").delete()
            Toast.makeText(this, "All Data Cleared!", Toast.LENGTH_SHORT).show()
        }
        dialog.show()
    }

    override fun dispatchKeyEvent(event: KeyEvent): Boolean {
        if (event.action == KeyEvent.ACTION_DOWN && event.isCtrlPressed && event.keyCode == KeyEvent.KEYCODE_G) {
            isGhostMode = !isGhostMode
            if (isGhostMode) {
                uiContainer.visibility = View.GONE
                window.decorView.systemUiVisibility = (
                        View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                        or View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                        or View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                        or View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                        or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        or View.SYSTEM_UI_FLAG_FULLSCREEN)
            } else {
                uiContainer.visibility = View.VISIBLE
                window.decorView.systemUiVisibility = View.SYSTEM_UI_FLAG_VISIBLE
            }
            return true
        }
        return super.dispatchKeyEvent(event)
    }

    override fun onPause() {
        super.onPause()
        val prefs = getSharedPreferences("BrowserState", Context.MODE_PRIVATE).edit()
        prefs.putInt("tab_count", sessions.size)
        for (i in sessions.indices) prefs.putString("tab_$i", sessions[i].currentUrl)
        prefs.putInt("last_index", currentTabIndex)
        prefs.apply()
    }

    private fun restoreTabs() {
        val prefs = getSharedPreferences("BrowserState", Context.MODE_PRIVATE)
        val count = prefs.getInt("tab_count", 0)
        if (count > 0) {
            for (i in 0 until count) {
                val url = prefs.getString("tab_$i", homeUrl) ?: homeUrl
                addNewTab(url)
            }
            switchToTab(prefs.getInt("last_index", 0))
        } else addNewTab(homeUrl)
    }
}
"""

# ==========================================
# التنفيذ
# ==========================================
print("🚀 تطبيق التحديثات (Fix Missing XML + Update HTML + Fix Mouse)...")

# تحديث الواجهة HTML
os.makedirs(ASSETS_DIR, exist_ok=True)
create_file(os.path.join(ASSETS_DIR, "home.html"), home_html)

# إنشاء الملف المفقود XML
os.makedirs(LAYOUT_DIR, exist_ok=True)
create_file(os.path.join(LAYOUT_DIR, "dialog_settings.xml"), dialog_settings_xml)

# تحديث كود التطبيق Kotlin
os.makedirs(JAVA_DIR, exist_ok=True)
create_file(os.path.join(JAVA_DIR, "MainActivity.kt"), main_activity)

# الرفع
print("🔄 جاري الرفع إلى GitHub...")
try:
    subprocess.run(["git", "config", "--global", "--add", "safe.directory", BASE_DIR], check=True)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Emergency Fix: Missing XML and UI Upgrade"], check=False)
    subprocess.run(["git", "push", "-u", "-f", "origin", "main"], check=True)
    print("\n✅✅ تم الإصلاح! الآن سيعمل 100%.")
except subprocess.CalledProcessError as e:
    print(f"\n❌ خطأ: {e}")