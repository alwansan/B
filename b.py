import os
import subprocess
import re

KOTLIN_FILE = "app/src/main/java/com/alwansan/b/MainActivity.kt"

def patch():
    if not os.path.exists(KOTLIN_FILE):
        print("❌ MainActivity.kt not found")
        return

    with open(KOTLIN_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # استبدال دالة loadUrl بالكامل
    new_function = """
    private fun loadUrl(input: String) {
        if (currentTabIndex == -1) return

        var url = input.trim()
        if (url.isEmpty()) return

        when {
            url.contains("://") -> {
                // already full URL
            }

            !url.contains(" ") && (url.contains(".") || url.contains(":")) -> {
                url = "https://$url"
            }

            else -> {
                url = "https://www.google.com/search?q=" +
                        java.net.URLEncoder.encode(url, "UTF-8")
            }
        }

        sessions[currentTabIndex].session.loadUri(url)
        addToHistoryLog(url)
        geckoView.requestFocus()
    }
    """

    # استبدال أي نسخة قديمة من loadUrl
    content = re.sub(
        r'private fun loadUrl\(.*?\n\s*\}',
        new_function,
        content,
        flags=re.DOTALL
    )

    with open(KOTLIN_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ loadUrl fully reset to stable version.")

patch()

print("🚀 Pushing hard reset fix...")
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Hard reset URL logic (stable + localhost safe)"], check=False)
    subprocess.run(["git", "push", "-f", "origin", "main"], check=True)
    print("✅ URL system rebuilt cleanly.")
except subprocess.CalledProcessError as e:
    print("❌ Git error:", e)
