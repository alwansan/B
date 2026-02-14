import os
import subprocess

KOTLIN_FILE = "app/src/main/java/com/alwansan/b/MainActivity.kt"

def patch():
    if not os.path.exists(KOTLIN_FILE):
        print("❌ MainActivity.kt not found")
        return

    with open(KOTLIN_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_key = "var url = input.trim()"
    end_key = "addToHistoryLog(url)"

    start = content.find(start_key)
    end = content.find(end_key)

    if start == -1 or end == -1:
        print("❌ URL logic block not found")
        return

    end += len(end_key)

    new_logic = """
        var url = input.trim()
        if (url.isEmpty()) return

        val isHttp = url.startsWith("http://") || url.startsWith("https://")
        val hasSpace = url.contains(" ")
        val looksLikeDomain = url.contains(".") || url.contains(":") || url.startsWith("localhost")

        if (isHttp) {
            // open as is
        } else if (hasSpace) {
            url = "https://www.google.com/search?q=$url"
        } else if (looksLikeDomain) {
            url = "http://$url"
        } else {
            url = "https://www.google.com/search?q=$url"
        }

        addToHistoryLog(url)
    """

    content = content[:start] + new_logic + content[end:]

    with open(KOTLIN_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ URL system fully repaired.")

patch()

print("🚀 Pushing final fix...")
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Fix: Stable URL handling (localhost + search + domains)"], check=False)
    subprocess.run(["git", "push", "-f", "origin", "main"], check=True)
    print("✅ Should work correctly now.")
except subprocess.CalledProcessError as e:
    print("❌ Git error:", e)
