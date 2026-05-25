"""Calcula SHA256 de cada ZIP en dist/ y escribe dist/SHA256SUMS.json."""
import hashlib
import json
import os


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


sums: dict[str, str] = {}
for fname in sorted(os.listdir("dist")):
    if fname.endswith(".zip"):
        digest = sha256_file(os.path.join("dist", fname))
        sums[fname] = digest
        print(f"{digest}  {fname}")

with open("dist/SHA256SUMS.json", "w", encoding="utf-8") as f:
    json.dump(sums, f, indent=2)

print(f"SHA256SUMS.json: {len(sums)} entradas")
