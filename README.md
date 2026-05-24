# TeXisStudio — Perfiles de comunidad

Repositorio oficial de perfiles para [TeXisStudio](https://github.com/GonzaloAndDev/TeXisStudio).

Cada perfil define la estructura de secciones, estilo bibliografico y configuracion LaTeX
para un tipo de documento academico. Se instalan desde la app en **Biblioteca > Comunidad**.

---

## Estructura del repositorio

```
<continente>/<pais>/<institucion>/
  _institution.yaml          ← configuracion compartida de la institucion
  <estilo>/
    profile.yaml             ← definicion completa del perfil
    manifest.yaml            ← metadata para la biblioteca
```

Ejemplo real:
```
europe/uk/oxford/
  _institution.yaml          ← margenes, fuente, papel de Oxford
  mhra/
    profile.yaml
    manifest.yaml
europe/uk/cambridge/
  _institution.yaml
  ieee/
    profile.yaml
    manifest.yaml
  apa7/
    profile.yaml
    manifest.yaml
```

---

## Continentes y paises disponibles

| Continente | Paises |
|---|---|
| `america` | mexico, usa, canada, brazil, argentina, chile |
| `europe` | uk, germany, spain, netherlands, italy, sweden |
| `asia` | china, japan, south_korea, singapore, india |
| `generic` | generic (sin institucion especifica) |

---

## Estilos bibliograficos incluidos (`citation_styles/`)

| ID | Nombre | Tipo | Uso principal |
|---|---|---|---|
| `apa7` | APA 7 | Autor-Fecha | Universal — psicologia, educacion, ciencias sociales |
| `vancouver` | Vancouver | Numerico | Medicina y ciencias de la salud |
| `ieee` | IEEE | Numerico | Ingenieria, computacion, tecnologia |
| `chicago17_notes` | Chicago 17 (Notas) | Notas-Bibliog. | Humanidades, historia, literatura |
| `chicago17_authordate` | Chicago 17 (A-D) | Autor-Fecha | Economia, ciencias sociales |
| `mla9` | MLA 9 | Autor-Pagina | Literatura, linguistica |
| `harvard` | Harvard | Autor-Fecha | Negocios, UK, Australia |
| `mhra` | MHRA | Notas-Bibliog. | Humanidades Reino Unido |
| `abnt` | ABNT | Autor-Fecha | Brasil — obligatorio |
| `gb7714` | GB/T 7714 | Numerico | China — norma nacional |

---

## Como contribuir un perfil

### Caso 1 — La institucion ya existe

Solo necesitas crear la carpeta del nuevo estilo/carrera:

```
america/mexico/unam/
  _institution.yaml          ← ya existe, no tocar
  apa7/                      ← ya existe
  vancouver/                 ← ya existe
  derecho_chicago17/         ← TU NUEVA CARPETA
    profile.yaml
    manifest.yaml
```

### Caso 2 — La institucion no existe

Crea la carpeta de la institucion con `_institution.yaml` y tu perfil:

```
europe/france/sorbonne/
  _institution.yaml          ← NUEVO: formato de la institucion
  chicago17/
    profile.yaml
    manifest.yaml
```

### `_institution.yaml` — formato compartido de la institucion

```yaml
id: sorbonne
name: "Universite Paris-Sorbonne"
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
  Lineamientos de la Direction des etudes doctorales.
```

### `manifest.yaml` de tu perfil

```yaml
id: fr_sorbonne_chicago17
name: "Sorbonne — These (Chicago 17)"
version: "1.0.0"
author: "Tu Nombre"
license: "CC-BY-4.0"
description: "These de doctorat Sorbonne Universite, Chicago 17 Notes-Bibliography."
tags: [sorbonne, france, chicago17, humanites, doctorat]
texis_min_version: "1.0.0"
institution_id: "sorbonne"
continent: "europe"
country: "france"
```

### `profile.yaml` de tu perfil

Solo especifica lo que es especifico de esta carrera/programa.
Los margenes, papel y fuente se heredan de `_institution.yaml`.

```yaml
id: fr_sorbonne_chicago17
name: "Sorbonne — These (Chicago 17)"
latex_engine: xelatex
document_class:
  name: book
  options: [12pt, a4paper, oneside]
bibliography_backend: biber
bibliography_style: chicago-notes
page_layout:
  paper: a4paper
  margins:
    top: 25mm
    bottom: 25mm
    left: 35mm
    right: 25mm
  line_spacing: 2.0
sections:
  - id: title_page
    element_id: cover
    placement: front_matter
    required: true
    title: "Page de titre"
  - id: abstract
    element_id: abstract
    placement: front_matter
    required: true
    title: "Resume"
  - id: introduction
    element_id: chapter
    placement: body
    required: true
    title: Introduction
  - id: bibliography
    element_id: bibliography
    placement: back_matter
    required: true
    title: Bibliographie
```

### Pasos para contribuir

1. **Fork** del repositorio
2. Encuentra o crea la carpeta de tu institucion
3. Crea `_institution.yaml` si la institucion es nueva
4. Crea la carpeta del estilo/carrera con `profile.yaml` + `manifest.yaml`
5. Abre un **Pull Request** — los perfiles verificados se agregan al catalogo

---

## Instalar un perfil en TeXisStudio

### Desde la app

1. Abre TeXisStudio > **Biblioteca** > **Comunidad**
2. Navega: Continente > Pais > Institucion > estilo
3. Haz clic en **Instalar**

### URL directa

```
https://github.com/GonzaloAndDev/TeXisStudio-Profiles/releases/latest/download/<manifest_id>.zip
```

Ejemplos:
```
.../download/mx_unam_apa7.zip
.../download/us_mit_ieee.zip
.../download/uk_oxford_mhra.zip
```

### Catalogo completo (JSON para la app)

```
https://github.com/GonzaloAndDev/TeXisStudio-Profiles/releases/latest/download/catalog.json
```

---

## Licencia

Los perfiles se distribuyen bajo **CC-BY-4.0** salvo indicacion contraria en `manifest.yaml`.

Independientes de la licencia del software TeXisStudio (AGPL v3 + Commons Clause).
