import re

file_path = "b.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old = 'if (url.contains(" ") || !url.contains(".")) url = "https://www.google.com/search?q=$url"'

new = '''if (url.contains(" ")) {
            url = "https://www.google.com/search?q=" +
                    java.net.URLEncoder.encode(url, "UTF-8")
        } else if (!url.startsWith("http") && !url.startsWith("file")) {

            if (url.startsWith("localhost") ||
                url.startsWith("127.0.0.1") ||
                url.contains(":") ||
                Regex("""^\\d{1,3}(\\.\\d{1,3}){3}(:\\d+)?$""").matches(url)) {

                url = "http://$url"

            } else if (url.contains(".")) {

                url = "https://$url"

            } else {

                url = "https://www.google.com/search?q=" +
                        java.net.URLEncoder.encode(url, "UTF-8")
            }
        }'''

content = content.replace(old, new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ b.py updated successfully. Now run python b.py again.")

