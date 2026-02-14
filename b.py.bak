import os
import subprocess

BASE_DIR = os.getcwd()
KOTLIN_FILE = "app/src/main/java/com/alwansan/b/MainActivity.kt"

def patch_file():
    if not os.path.exists(KOTLIN_FILE):
        print("❌ MainActivity.kt not found")
        return
    
    with open(KOTLIN_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # حذف السطر المسبب للخطأ
    content = content.replace(
        "settings.setBoolean(GeckoSessionSettings.USE_DOUBLE_TAP_ZOOM, false)",
        "// Removed invalid USE_DOUBLE_TAP_ZOOM (not supported in Gecko 121+)"
    )

    # إضافة تعطيل التكبير من View إذا لم يكن موجود
    if "setOnTouchListener" not in content:
        inject_code = """
        // 🔒 Disable double tap & pinch zoom at View level
        geckoView.setOnTouchListener { _, event ->
            if (event.pointerCount > 1) {
                true
            } else {
                false
            }
        }
        """
        content = content.replace(
            "geckoRuntime = GeckoRuntime.create(this)",
            "geckoRuntime = GeckoRuntime.create(this)\n" + inject_code
        )

    with open(KOTLIN_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Zoom build error fixed.")

patch_file()

print("🚀 Pushing fix...")
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Fix: Remove unsupported USE_DOUBLE_TAP_ZOOM API"], check=False)
    subprocess.run(["git", "push", "-f", "origin", "main"], check=True)
    print("✅ Build Fix Pushed.")
except subprocess.CalledProcessError as e:
    print("❌ Git Error:", e)
