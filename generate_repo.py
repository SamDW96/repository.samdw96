import os
import hashlib
import zipfile
import re

# Hoeveel versies wil je bewaren per addon?
MAX_VERSIONS = 5

def get_addon_xml(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as z:
        for name in z.namelist():
            if name.endswith('addon.xml') and '/' not in name:
                 return z.read(name).decode('utf-8')
            elif name.endswith('addon.xml'):
                 return z.read(name).decode('utf-8')
    return None

def generate_md5(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def clean_old_versions(zips_dir):
    """Verwijdert oude zips zodat de repo niet dichtslibt"""
    # Loop door elke addon-map in de zips folder
    for addon_id in os.listdir(zips_dir):
        addon_path = os.path.join(zips_dir, addon_id)
        
        if not os.path.isdir(addon_path):
            continue

        # Vind alle zipjes
        zips = [f for f in os.listdir(addon_path) if f.endswith(".zip")]
        
        # Als we er meer hebben dan toegestaan
        if len(zips) > MAX_VERSIONS:
            # Sorteer op 'laatst gewijzigd' (oudste eerst)
            full_paths = [os.path.join(addon_path, f) for f in zips]
            full_paths.sort(key=os.path.getmtime)
            
            # Bereken hoeveel we er moeten verwijderen
            to_delete = full_paths[:-MAX_VERSIONS]
            
            for f in to_delete:
                print(f"Oude versie opruimen: {os.path.basename(f)}")
                os.remove(f)

def main():
    zips_dir = "zips"
    if not os.path.exists(zips_dir):
        print("Geen 'zips' map gevonden, stop.")
        return

    # STAP 1: Eerst opruimen
    clean_old_versions(zips_dir)

    # STAP 2: Daarna de XML genereren met wat overblijft
    xml_content = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '<addons>']
    
    for root, dirs, files in os.walk(zips_dir):
        for file in files:
            if file.endswith(".zip"):
                full_path = os.path.join(root, file)
                try:
                    addon_xml = get_addon_xml(full_path)
                    if addon_xml:
                        clean_xml = re.sub(r'<\?xml.*?\?>', '', addon_xml).strip()
                        xml_content.append(clean_xml)
                        print(f"In catalogus: {file}")
                except Exception as e:
                    print(f"Fout bij {file}: {e}")

    xml_content.append('</addons>')
    
    with open("addons.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml_content))
    
    md5 = generate_md5("addons.xml")
    with open("addons.xml.md5", "w", encoding="utf-8") as f:
        f.write(md5)
        
    print("Klaar! Repo is opgeschoond en bijgewerkt.")

if __name__ == "__main__":
    main()
