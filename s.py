import os

# الملفات التي نريد قراءتها (الأكواد)
ALLOWED_EXTENSIONS = {
    '.kt', '.java', '.xml', '.kts', '.gradle', 
    '.properties', '.py', '.html', '.txt', '.md', '.json'
}

# المجلدات التي سنتجاهلها (ملفات النظام والبناء)
IGNORED_DIRS = {
    '.git', '.gradle', '.idea', 'build', 'gradle', 
    'captures', 'cxx', 'output', 'release', 'debug'
}

OUTPUT_FILE = "all.txt"

def is_text_file(filename):
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)

def scan_project():
    project_root = os.getcwd()
    print(f"🕵️‍♂️ جاري فحص المشروع في: {project_root}")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        # كتابة مقدمة
        outfile.write(f"=== PROJECT STRUCTURE & CODE DUMP ===\n")
        outfile.write(f"Project Name: {os.path.basename(project_root)}\n")
        outfile.write("=======================================\n\n")

        # 1. طباعة هيكلية المجلدات (Tree Structure)
        outfile.write("--- DIRECTORY STRUCTURE ---\n")
        for root, dirs, files in os.walk(project_root):
            # استبعاد المجلدات غير المهمة
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            level = root.replace(project_root, '').count(os.sep)
            indent = ' ' * 4 * (level)
            outfile.write(f"{indent}{os.path.basename(root)}/\n")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                outfile.write(f"{subindent}{f}\n")
        outfile.write("\n=======================================\n\n")

        # 2. طباعة محتوى الملفات
        outfile.write("--- FILE CONTENTS ---\n\n")
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

            for file in files:
                if is_text_file(file) and file != OUTPUT_FILE and file != "s.py":
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, project_root)
                    
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                            content = infile.read()
                            
                            outfile.write(f"START OF FILE: {relative_path}\n")
                            outfile.write("="*50 + "\n")
                            outfile.write(content + "\n")
                            outfile.write("="*50 + "\n")
                            outfile.write(f"END OF FILE: {relative_path}\n\n")
                            print(f"📄 تمت قراءة: {relative_path}")
                    except Exception as e:
                        print(f"⚠️ تعذرت قراءة: {relative_path} ({e})")

    print(f"\n✅✅ تم الحفظ بنجاح في الملف: {OUTPUT_FILE}")
    print("يمكنك الآن إرسال هذا الملف لأي ذكاء اصطناعي ليفهم المشروع بالكامل.")

if __name__ == "__main__":
    scan_project()