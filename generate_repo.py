import os
import hashlib
import zipfile
import re

# Configuratie
REPO_URL = "https://raw.githubusercontent.com/SamDW96/repository.samdw96/main/"

def get_addon_xml(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as z:
        # Zoek naar addon.xml in de zip (kan in een submap zitten)
        for name in z.namelist():
            if name.endswith('addon.xml'):
                return z.read(name).decode('utf-8')
    return None

def generate_md5(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def main():
    addons_xml_content = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '<addons>']
    
    # Loop door alle zip bestanden in de 'zips' map
    zips_dir = "zips"
    if not os.path.exists(zips_dir):
        print("Geen 'zips' map gevonden!")
        return

    for root, dirs, files in os.walk(zips_dir):
        for file in files:
            if file.endswith(".zip"):
                # We pakken alleen de nieuwste zip van elke addon is eigenlijk beter, 
                # maar Kodi leest alles. Voor nu simpel: scan alles.
                path = os.path.join(root, file)
                try:
                    xml = get_addon_xml(path)
                    if xml:
                        # Strip de XML header om duplicaten te voorkomen
                        xml = re.sub(r'<\?xml.*?\?>', '', xml).strip()
                        addons_xml_content.append(xml)
                        print(f"Toegenomen: {file}")
                except Exception as e:
                    print(f"Fout bij lezen {file}: {e}")

    addons_xml_content.append('</addons>')
    
    # Schrijf addons.xml
    with open("addons.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(addons_xml_content))
    
    # Schrijf addons.xml.md5
    md5 = generate_md5("addons.xml")
    with open("addons.xml.md5", "w", encoding="utf-8") as f:
        f.write(md5)
    
    print("addons.xml en md5 succesvol gegenereerd!")

if __name__ == "__main__":
    main()