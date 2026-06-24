#!/usr/bin/env python3
"""Project legacy profiles to contract 2.0 and validate without writing artifacts."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/profile-2.schema.json").read_text(encoding="utf-8"))


def preliminary(element_id: str) -> str | None:
    element = element_id.lower()
    mapping = (
        (("dedicat",), "dedication"),
        (("agradec", "acknowledg"), "acknowledgements"),
        (("original", "declarac"), "originality_statement"),
        (("autoriz",), "authorization"),
        (("resumen", "abstract"), "abstract"),
        (("epigraf", "epigraph"), "epigraph"),
        (("nomenclat",), "nomenclature"),
        (("glosar", "glossary"), "glossary"),
    )
    for needles, result in mapping:
        if any(needle in element for needle in needles):
            return result
    return None


def project(profile: dict, manifest: dict) -> dict:
    status = profile.get("status", "experimental")
    trust = {
        "verified": "verified",
        "reviewed": "community",
    }.get(status, "draft")
    verification = profile.get("verification") or {}
    evidence = list(dict.fromkeys([
        *(verification.get("source_urls") or []),
        *([verification["ci_evidence"]] if verification.get("ci_evidence") else []),
    ]))

    required_preliminaries: list[str] = []
    require_keywords = False
    require_toc = False
    for section in profile.get("sections") or []:
        element = str(section.get("element_id", "")).lower()
        if any(token in element for token in ("toc", "indice", "contents")):
            require_toc = True
        if not section.get("required"):
            continue
        if any(token in element for token in ("keyword", "palabras_clave", "palabras-clave")):
            require_keywords = True
            continue
        mapped = preliminary(element)
        if mapped and mapped not in required_preliminaries:
            required_preliminaries.append(mapped)

    style = str(profile.get("bibliography_style") or "").lower()
    if style == "apa":
        style = "apa7"
    pdf = profile.get("pdf_requirements") or {}
    pdfa = pdf.get("pdfa") or {}

    return {
        "contract_version": {"major": 2, "minor": 0},
        "identity": {
            "id": profile["id"],
            "name": profile["name"],
            "institution": manifest.get("institution"),
            "country": manifest.get("country"),
            "trust": trust,
            "revised_at": verification.get("reviewed_at") or verification.get("verified_at"),
            "evidence": evidence,
        },
        "policy": {
            "required_preliminaries": required_preliminaries,
            "recommended_preliminaries": [],
            "require_keywords": require_keywords,
            "cover": {
                "require_logo": profile.get("title_page_template") is not None,
                "require_signatures": False,
                "require_orcid": False,
                "max_title_chars": None,
            },
            "bibliography": {
                "allowed_styles": [style] if style else [],
                "required_backend": (
                    str(profile["bibliography_backend"]).lower()
                    if profile.get("bibliography_backend")
                    else None
                ),
            },
            "indexes": {
                "require_toc": require_toc,
                "max_toc_depth": None,
            },
            "delivery": {
                "require_pdf_metadata": bool(pdf),
                "require_pdfa": bool(pdfa.get("required")),
                "pdfa_level": pdfa.get("level"),
                "required_abstract_languages": [],
            },
        },
    }


def main() -> int:
    errors: list[str] = []
    count = 0
    for profile_path in sorted(ROOT.glob("*/*/*/*/profile.yaml")):
        manifest_path = profile_path.with_name("manifest.yaml")
        if not manifest_path.exists():
            errors.append(f"{profile_path}: manifest.yaml missing")
            continue
        profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        try:
            projected = project(profile, manifest)
            jsonschema.validate(projected, SCHEMA)
            identity = projected["identity"]
            if identity["trust"] == "verified":
                if not identity["revised_at"]:
                    raise ValueError("verified profile has no revision date")
                if not identity["evidence"]:
                    raise ValueError("verified profile has no official/CI evidence")
        except Exception as error:
            errors.append(f"{profile_path}: {error}")
        count += 1

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(f"OK: {count} profiles project cleanly to contract 2.0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
