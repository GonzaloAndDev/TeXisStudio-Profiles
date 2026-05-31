# TeXisStudio — Community Profiles / Perfiles de Comunidad

> **ES** — Perfiles institucionales y de disciplina para TeXisStudio.  
> Define márgenes, estilo bibliográfico, estructura de secciones y tipografía para cada institución académica.  
> **EN** — Institutional and discipline profiles for TeXisStudio.  
> Defines margins, bibliography style, section structure, and typography for each academic institution.

Part of / Parte del ecosistema **[TeXisStudio](../TeXisStudio/README.md)**  
Also / También: [TeXisStudio-Plugins](../TeXisStudio-Plugins/README.md) · [TeXisStudio-Languages](../TeXisStudio-Languages/README.md)

---

## ES — ¿Qué es un perfil?

Un perfil define todo lo que es específico de una institución o disciplina:
- Márgenes, papel, interlineado y fuente tipográfica
- Clase de documento LaTeX (`book`, `article`, `report`…)
- Estilo bibliográfico (APA7, Vancouver, IEEE, Chicago…)
- Estructura de secciones requeridas (portada, resumen, introducción, conclusiones…)
- Idioma y configuración babel/polyglossia

El usuario selecciona un perfil al crear un proyecto. A partir de ahí, TeXisStudio genera el LaTeX correcto para esa institución automáticamente.

## EN — What is a profile?

A profile defines everything specific to an institution or discipline:
- Margins, paper size, line spacing, and typography
- LaTeX document class (`book`, `article`, `report`…)
- Bibliography style (APA7, Vancouver, IEEE, Chicago…)
- Required section structure (cover, abstract, introduction, conclusions…)
- Language and babel/polyglossia configuration

The user selects a profile when creating a project. From then on, TeXisStudio automatically generates the correct LaTeX for that institution.

---

## Repository structure / Estructura del repositorio

```
<continent>/<country>/<institution>/
  _institution.yaml          ← shared institution format / formato compartido
  <style-or-variant>/
    profile.yaml             ← full profile definition / definición completa
    manifest.yaml            ← catalog metadata / metadatos para la biblioteca

citation_styles/             ← bibliography style definitions / estilos bibliográficos
generic/                     ← generic profiles (no specific institution) / perfiles genéricos
```

Real example / Ejemplo real:
```
america/mexico/unam/
  _institution.yaml
  apa7/
    profile.yaml
    manifest.yaml
  vancouver/
    profile.yaml
    manifest.yaml
europe/uk/oxford/
  _institution.yaml
  mhra/
    profile.yaml
    manifest.yaml
```

---

## Available regions / Regiones disponibles

| Continent / Continente | Countries / Países |
|---|---|
| `america` | mexico, usa, canada, brazil, argentina, chile |
| `europe` | uk, germany, spain, netherlands, italy, sweden |
| `asia` | china, japan, south_korea, singapore, india |
| `generic` | generic (no specific institution / sin institución específica) |

**México (available now / disponibles ahora):** UNAM, IPN, UAM, UANL, UDG, Tec de Monterrey

---

## Bibliography styles included / Estilos bibliográficos incluidos

| ID | Name / Nombre | Type / Tipo | Main use / Uso principal |
|---|---|---|---|
| `apa7` | APA 7 | Author-Date | Universal — psychology, education, social sciences |
| `vancouver` | Vancouver | Numeric | Medicine and health sciences |
| `ieee` | IEEE | Numeric | Engineering, CS, technology |
| `chicago17_notes` | Chicago 17 (Notes) | Notes-Bibliog. | Humanities, history, literature |
| `chicago17_authordate` | Chicago 17 (A-D) | Author-Date | Economics, social sciences |
| `mla9` | MLA 9 | Author-Page | Literature, linguistics |
| `harvard` | Harvard | Author-Date | Business, UK, Australia |
| `mhra` | MHRA | Notes-Bibliog. | UK Humanities |
| `abnt` | ABNT | Author-Date | Brazil — mandatory / Brasil — obligatorio |
| `gb7714` | GB/T 7714 | Numeric | China — national standard |

---

## Editorial taxonomy / Taxonomía editorial recomendada

**ES:** La regla es: no especializar si no hay una diferencia real de formato.

- **`institutional`** — el mismo formato para toda la institución (regla general)
- **`degree_specific`** — cuando el contrato cambia entre licenciatura/maestría/doctorado
- **`program_specific`** — cuando una facultad o programa exige diferencias formales
- **`discipline_specific`** — cuando el área (ingeniería, humanidades) exige formato diferente

**EN:** The rule is: do not specialise if there is no real format difference.

- **`institutional`** — same format for the entire institution (general rule)
- **`degree_specific`** — when the contract changes between bachelor/master/doctoral
- **`program_specific`** — when a faculty or programme requires formal differences
- **`discipline_specific`** — when the area (engineering, humanities) requires a different format

---

## Contributing a profile / Cómo contribuir un perfil

### Case 1 — Institution already exists / Caso 1 — Institución ya existe

```
america/mexico/unam/
  _institution.yaml          ← already exists, do not modify / ya existe, no tocar
  apa7/                      ← existing / ya existe
  derecho_chicago17/         ← YOUR NEW FOLDER / TU NUEVA CARPETA
    profile.yaml
    manifest.yaml
```

### Case 2 — New institution / Caso 2 — Institución nueva

```
europe/france/sorbonne/
  _institution.yaml          ← NEW — institution shared format / NUEVO — formato compartido
  chicago17/
    profile.yaml
    manifest.yaml
```

### `_institution.yaml` — shared institution format

```yaml
id: sorbonne
name: "Université Paris-Sorbonne"
acronym: "Sorbonne"
continent: "europe"
country: "france"
website: "https://www.sorbonne-universite.fr"
default_format:
  paper: a4paper
  margins:
    top: 25mm
    bottom: 25mm
    left: 35mm
    right: 25mm
  line_spacing: 2.0
  font_main: "Times New Roman"
  font_size: 12pt
notes: |
  Guidelines from the Direction des études doctorales.
```

### `manifest.yaml` — catalog metadata

```yaml
id: fr_sorbonne_chicago17
name: "Sorbonne — Thèse (Chicago 17)"
version: "1.0.0"
author: "Your Name / Tu Nombre"
license: "CC-BY-4.0"
description: "Thèse de doctorat Sorbonne Université, Chicago 17 Notes-Bibliography."
tags: [sorbonne, france, chicago17, humanities, doctorat]
texis_min_version: "1.0.0"
institution_id: "sorbonne"
continent: "europe"
country: "france"
academic_level: "doctorado"
profile_scope: "discipline_specific"
```

### `profile.yaml` — full profile definition

```yaml
id: fr_sorbonne_chicago17
name: "Sorbonne — Thèse (Chicago 17)"
latex_engine: xelatex
document_class:
  name: book
  options: [12pt, a4paper, oneside]
bibliography_backend: biber
bibliography_style: chicago-notes
page_layout:
  paper: a4paper
  margins: { top: 25mm, bottom: 25mm, left: 35mm, right: 25mm }
  line_spacing: 2.0
sections:
  - { id: title_page, element_id: cover,        placement: front_matter, required: true }
  - { id: abstract,   element_id: abstract,     placement: front_matter, required: true }
  - { id: intro,      element_id: chapter,      placement: body,         required: true }
  - { id: biblio,     element_id: bibliography, placement: back_matter,  required: true }
```

### Steps / Pasos

1. **Fork** this repository / este repositorio
2. Find or create your institution folder / Encuentra o crea la carpeta de tu institución
3. Create `_institution.yaml` if new / Crea `_institution.yaml` si es nueva
4. Create style folder with `profile.yaml` + `manifest.yaml` / Crea la carpeta con los archivos
5. Open a **Pull Request** — verified profiles are added to the catalog  
   Abre un **Pull Request** — los perfiles verificados se agregan al catálogo

---

## Installing a profile / Instalar un perfil

### From the app / Desde la app

1. Open TeXisStudio → **Library / Biblioteca** → **Community / Comunidad**
2. Browse: Continent → Country → Institution → style  
   Navega: Continente → País → Institución → estilo
3. Click **Install / Instalar**

### Direct URL / URL directa

```
https://github.com/GonzaloAndDev/TeXisStudio-Profiles/releases/latest/download/<manifest_id>.zip
```

Examples / Ejemplos:
```
.../download/mx_unam_apa7.zip
.../download/us_mit_ieee.zip
.../download/uk_oxford_mhra.zip
```

### Full catalog JSON (used by the app / usado por la app)

```
https://github.com/GonzaloAndDev/TeXisStudio-Profiles/releases/latest/download/catalog.json
```

---

## License / Licencia

Profiles are distributed under **CC-BY-4.0** unless otherwise indicated in `manifest.yaml`.  
Los perfiles se distribuyen bajo **CC-BY-4.0** salvo indicación contraria en `manifest.yaml`.

Independent of / Independientes de la licencia del software TeXisStudio (AGPL v3 + Commons Clause).
