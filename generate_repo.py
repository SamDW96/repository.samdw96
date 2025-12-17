import os
import hashlib
import zipfile
import re

def get_addon_xml(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as z:
        for name in z.namelist():
            if name.endswith('addon.xml') and '/' not in name: # Alleen root addon.xml
                 return z.read(name).decode('utf-8')
            elif name.endswith('addon.xml'): # Fallback voor submappen
                 return z.read(name).decode('utf-8')
    return None

def generate_md5(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def main():
    # Start XML
    xml_content = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '<addons>']
    
    # Zoek zips
    zips_path = "zips"
    if os.path.exists(zips_path):
        for root, dirs, files in os.walk(zips_path):
            for file in files:
                if file.endswith(".zip"):
                    full_path = os.path.join(root, file)
                    try:
                        addon_xml = get_addon_xml(full_path)
                        if addon_xml:
                            # Strip de XML header van de individuele addon om duplicaten te voorkomen
                            clean_xml = re.sub(r'<\?xml.*?\?>', '', addon_xml).strip()
                            xml_content.append(clean_xml)
                            print(f"Toegevoegd: {file}")
                    except Exception as e:
                        print(f"Fout bij {file}: {e}")

    xml_content.append('</addons>')
    
    # Schrijf addons.xml
    with open("addons.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml_content))
    
    # Schrijf md5
    md5 = generate_md5("addons.xml")
    with open("addons.xml.md5", "w", encoding="utf-8") as f:
        f.write(md5)
        
    print("Klaar! addons.xml en md5 bijgewerkt.")

if __name__ == "__main__":
    main()
