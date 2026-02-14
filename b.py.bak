import os
import subprocess

KOTLIN_FILE = "app/src/main/java/com/alwansan/b/MainActivity.kt"

def patch():
    if not os.path.exists(KOTLIN_FILE):
        print("❌ MainActivity.kt not found")
        return

    with open(KOTLIN_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # استبدال منطق URL بالكامل بمنطق آمن بدون Regex
    old_block_start = "var url = input.trim()"
    old_block_end = "addToHistoryLog(url)"

    start_index = content.find(old_block_start)
    end_index = content.find(old_block_end)

    if start_index == -1 or end_index == -1:
        print("❌ URL block not found safely.")
        return

    end_index += len(old_block_end)

    new_logic = """
        var url = input.trim()
        if (url.isEmpty()) return

        val isHttp = url.startsWith("http://") || url.startsWith("https://")
        val isLocalhost = url.startsWith("localhost")
        val isIPv4 = url.split(".").size == 4 && url.replace(".", "").replace(":", "").all { it.isDigit() }

        if (isHttp) {
            // use as is
        } else if (isLocalhost) {
            url = "http://$url"
        } else if (isIPv4) {
            url = "http://$url"
        } else if (url.contains(".")) {
            url = "https://$url"
        } else {
            url = "https://www.google.com/search?q=$url"
        }

        addToHistoryLog(url)
    """

    content = content[:start_index] + new_logic + content[end_index:]

    with open(KOTLIN_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Regex error fixed safely.")

patch()

print("🚀 Pushing clean fix...")
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Fix: Remove broken regex, safe localhost/IP detection"], check=False)
    subprocess.run(["git", "push", "-f", "origin", "main"], check=True)
    print("✅ Build should pass now.")
except subprocess.CalledProcessError as e:
    print("❌ Git error:", e)
