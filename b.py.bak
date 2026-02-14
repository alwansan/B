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

    # الكود الجديد الذكي
    new_logic = """
        var url = input.trim()
        if (url.isEmpty()) return

        val isHttp = url.startsWith("http://") || url.startsWith("https://")
        val isLocalhost = url.startsWith("localhost") || url.contains("://localhost")
        val isIP = Regex("^\\\\d{1,3}(\\\\.\\\\d{1,3}){3}(:\\\\d+)?$").matches(url)

        if (isHttp) {
            // use as is
        } else if (isLocalhost) {
            url = "http://$url"
        } else if (isIP) {
            url = "http://$url"
        } else if (url.contains(".")) {
            url = "https://$url"
        } else {
            url = "https://www.google.com/search?q=$url"
        }
    """

    # استبدال الدالة القديمة فقط
    content = re.sub(
        r'var url = input\.trim\(\).*?addToHistoryLog\(url\)',
        new_logic + "\n        addToHistoryLog(url)",
        content,
        flags=re.DOTALL
    )

    with open(KOTLIN_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Localhost/IP fix applied.")

patch()

print("🚀 Pushing fix...")
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Fix: Proper localhost & IP handling in URL bar"], check=False)
    subprocess.run(["git", "push", "-f", "origin", "main"], check=True)
    print("✅ Fix pushed successfully.")
except subprocess.CalledProcessError as e:
    print("❌ Git error:", e)
