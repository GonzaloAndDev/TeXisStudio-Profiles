"""Empaqueta cada perfil como ZIP individual y genera citation_styles.zip.

Estructura esperada (profundidad 4):
  <continent>/<country>/<institution>/<style_id>/profile.yaml
  <continent>/<country>/<institution>/<style_id>/manifest.yaml
"""
import os
import sys
import zipfile

import yaml

os.makedirs("dist", exist_ok=True)

packed = 0
for root, dirs, files in os.walk("."):
    dirs.sort()
    if "manifest.yaml" not in files or "profile.yaml" not in files:
        continue
    norm = root.replace("\\", "/").lstrip("./")
    parts = [p for p in norm.split("/") if p]
    if len(parts) != 4:
        continue

    with open(os.path.join(root, "manifest.yaml"), encoding="utf-8") as f:
        m = yaml.safe_load(f)

    pid = m.get("id")
    if not pid:
        print(f"WARN: {root}/manifest.yaml no tiene campo 'id' — omitiendo", file=sys.stderr)
        continue

    zip_path = f"dist/{pid}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in sorted(files):
            fpath = os.path.join(root, fname)
            arcname = os.path.join(norm, fname)
            zf.write(fpath, arcname)
    size_kb = os.path.getsize(zip_path) // 1024
    print(f"ok  {pid}.zip  ({norm})  {size_kb} KB")
    packed += 1

# Empaqueta citation_styles/ como ZIP independiente
if os.path.isdir("citation_styles"):
    with zipfile.ZipFile("dist/citation_styles.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in sorted(os.listdir("citation_styles")):
            fpath = os.path.join("citation_styles", fname)
            if os.path.isfile(fpath):
                zf.write(fpath, os.path.join("citation_styles", fname))
    print("ok  citation_styles.zip")

print(f"---\n{packed} perfiles empaquetados")
