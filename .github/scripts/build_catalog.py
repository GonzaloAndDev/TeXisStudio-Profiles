"""Genera dist/catalog.json con metadatos de perfiles, instituciones y estilos.

Estructura esperada del repo (profundidad 4):
  <continent>/<country>/<institution>/<style_id>/profile.yaml
  <continent>/<country>/<institution>/<style_id>/manifest.yaml
  <continent>/<country>/<institution>/_institution.yaml
"""
import hashlib
import json
import os

import yaml


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


catalog: dict = {"profiles": [], "citation_styles": [], "institutions": {}}

# Metadata de instituciones (_institution.yaml)
for root, dirs, files in os.walk("."):
    dirs.sort()
    if "_institution.yaml" in files:
        norm = root.replace("\\", "/").lstrip("./")
        parts = [p for p in norm.split("/") if p]
        if len(parts) == 3:
            inst_key = "/".join(parts)
            with open(os.path.join(root, "_institution.yaml"), encoding="utf-8") as f:
                inst_data = yaml.safe_load(f)
            catalog["institutions"][inst_key] = inst_data

# Perfiles a profundidad 4: continent/country/institution/style_id/
for root, dirs, files in os.walk("."):
    dirs.sort()
    if "manifest.yaml" in files and "profile.yaml" in files:
        norm = root.replace("\\", "/").lstrip("./")
        parts = [p for p in norm.split("/") if p]
        if len(parts) == 4:
            continent, country, institution, style_id = parts
            inst_key = "/".join([continent, country, institution])
            inst_data = catalog["institutions"].get(inst_key, {})
            with open(os.path.join(root, "manifest.yaml"), encoding="utf-8") as f:
                m = yaml.safe_load(f)
            with open(os.path.join(root, "profile.yaml"), encoding="utf-8") as f:
                p = yaml.safe_load(f)
            pid = m.get("id", style_id)
            zip_path = f"dist/{pid}.zip"
            m["download_url"] = (
                "https://github.com/GonzaloAndDev/TeXisStudio-Profiles"
                f"/releases/latest/download/{pid}.zip"
            )
            m["sha256"] = sha256_file(zip_path) if os.path.exists(zip_path) else None
            m["continent"] = continent
            m["country"] = country
            m["institution_id"] = m.get("institution_id", institution)
            manifest_institution = m.get("institution")
            if not manifest_institution or manifest_institution == institution:
                m["institution"] = inst_data.get("name", manifest_institution or institution)
            else:
                m["institution"] = manifest_institution
            m["style_id"] = m.get("style_id", style_id)
            if not m.get("status") and p.get("status"):
                m["status"] = p.get("status")
            verification = p.get("verification") or {}
            for key in ["reviewed_at", "reviewed_by", "verified_at", "verified_by", "source_urls", "review_interval_days", "ci_evidence"]:
                if key not in m and key in verification:
                    m[key] = verification[key]
            catalog["profiles"].append(m)

# Estilos bibliograficos
styles_dir = "citation_styles"
if os.path.isdir(styles_dir):
    for fname in sorted(os.listdir(styles_dir)):
        if fname.endswith(".yaml"):
            with open(os.path.join(styles_dir, fname), encoding="utf-8") as f:
                s = yaml.safe_load(f)
            catalog["citation_styles"].append(s)

catalog["citation_styles"].sort(key=lambda s: s.get("sort_order", 99))
catalog["profiles"].sort(key=lambda p: (
    p.get("continent", ""), p.get("country", ""), p.get("institution", ""), p.get("name", "")
))

with open("dist/catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

n_p = len(catalog["profiles"])
n_i = len(catalog["institutions"])
n_s = len(catalog["citation_styles"])
print(f"Catalogo: {n_p} perfiles, {n_i} instituciones, {n_s} estilos")
