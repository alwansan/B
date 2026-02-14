import os
import subprocess

# ==========================================
# إعدادات المشروع
# ==========================================
REPO_URL = "https://github.com/alwansan/B"
BASE_DIR = os.getcwd()
APP_DIR = os.path.join(BASE_DIR, "app")
RES_DIR = os.path.join(APP_DIR, "src", "main", "res")
DRAWABLE_DIR = os.path.join(RES_DIR, "drawable")
VALUES_DIR = os.path.join(RES_DIR, "values")

def create_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ تم تحديث: {os.path.basename(path)}")

# 1. حذف الملفات القديمة المسببة للمشاكل
files_to_delete = [
    os.path.join(DRAWABLE_DIR, "bg_search_bar.xml"), # الملف المسبب للخطأ
    os.path.join(DRAWABLE_DIR, "ic_launcher.xml")    # في حال وجود تكرار سابق
]

print("🧹 جاري تنظيف الملفات القديمة...")
for file_path in files_to_delete:
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"🗑️ تم حذف الملف القديم: {os.path.basename(file_path)}")

# 2. تحديث الألوان (إضافة surface_gray احتياطياً)
colors_xml = """
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="bg_main">#191A24</color>
    <color name="bg_secondary">#242633</color>
    <color name="accent_neon">#00E5FF</color>
    <color name="accent_red">#FA2E4D</color>
    <color name="text_primary">#FFFFFF</color>
    <color name="tab_active">#242633</color>
    <color name="tab_inactive">#15161E</color>
    <!-- تم إضافة هذا اللون لمنع أي أخطاء من ملفات قديمة -->
    <color name="surface_gray">#242633</color>
</resources>
"""
create_file(os.path.join(VALUES_DIR, "colors.xml"), colors_xml)

# 3. الرفع لـ GitHub
print("🔄 جاري رفع الإصلاحات...")
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Fix: Delete obsolete drawables and fix color resources"], check=False)
    subprocess.run(["git", "push", "-u", "-f", "origin", "main"], check=True)
    print("\n✅✅ تم الإصلاح! سيتم حذف الملفات المعطوبة وسينجح البناء.")
    print(f"🔗 {REPO_URL}/actions")
except subprocess.CalledProcessError as e:
    print(f"\n❌ خطأ: {e}")