# TeXisStudio — Perfiles de comunidad

Repositorio oficial de perfiles para [TeXisStudio](https://github.com/GonzaloAndDev/TeXisStudio).

Cada perfil define la estructura de secciones, estilo bibliografico y configuracion LaTeX
para un tipo de documento academico segun la institucion. Se instalan desde la app en
**Biblioteca > Comunidad**.

---

## Estructura del repositorio

```
TeXisStudio-Profiles/
├── america/
│   ├── mexico/       mx_unam_apa7, mx_unam_vancouver, mx_tec_apa7, mx_ipn_apa7, mx_uanl_apa7, mx_udg_apa7
│   ├── usa/          us_mit_ieee, us_harvard_apa7, us_harvard_chicago17, us_stanford_ieee, us_chicago_chicago17
│   ├── canada/       ca_mcgill_apa7
│   ├── brazil/       br_usp_abnt, br_unicamp_abnt
│   ├── argentina/    ar_uba_apa7
│   └── chile/        cl_uchile_apa7
├── europe/
│   ├── uk/           uk_oxford_mhra, uk_cambridge_ieee, uk_cambridge_apa7
│   ├── germany/      de_lmu_apa7, de_tum_ieee
│   ├── spain/        es_ucm_apa7
│   ├── netherlands/  nl_tudelft_ieee
│   ├── italy/        it_sapienza_apa7
│   └── sweden/       se_kth_ieee
├── asia/
│   ├── china/        cn_tsinghua_gbt, cn_pku_gbt
│   ├── japan/        jp_utokyo_ieee, jp_kyoto_apa7
│   ├── south_korea/  kr_snu_apa7
│   ├── singapore/    sg_nus_ieee
│   └── india/        in_iit_bombay_ieee
├── generic/
│   └── generic/      generic_thesis, generic_tesina
└── citation_styles/  apa7, vancouver, ieee, chicago17_notes, chicago17_authordate, mla9, harvard, mhra, abnt, gb7714
```

---

## Estilos bibliograficos incluidos

| ID | Nombre | Tipo | Uso principal |
|---|---|---|---|
| `apa7` | APA 7 | Author-Date | Universal — psicologia, educacion, ciencias sociales |
| `vancouver` | Vancouver | Numerico | Medicina y ciencias de la salud |
| `ieee` | IEEE | Numerico | Ingenieria, computacion, tecnologia |
| `chicago17_notes` | Chicago 17 (Notas) | Notas-Bibliog. | Humanidades, historia, literatura (EE.UU./UK) |
| `chicago17_authordate` | Chicago 17 (A-D) | Author-Date | Economia, ciencias sociales |
| `mla9` | MLA 9 | Author-Page | Literatura, linguistica (EE.UU.) |
| `harvard` | Harvard | Author-Date | Negocios, UK, Australia |
| `mhra` | MHRA | Notas-Bibliog. | Humanidades Reino Unido (Oxford) |
| `abnt` | ABNT | Author-Date | Brasil — obligatorio por ley |
| `gb7714` | GB/T 7714 | Numerico | China — norma nacional obligatoria |

---

## Instalar un perfil en TeXisStudio

### Desde la app (recomendado)

1. Abre TeXisStudio > **Biblioteca** > pestana **Comunidad**
2. Navega: Continente > Pais > Institucion
3. Haz clic en **Instalar**

### URL directa de un perfil

```
https://github.com/GonzaloAndDev/TeXisStudio-Profiles/releases/latest/download/<profile_id>.zip
```

Ejemplos:
```
.../download/mx_unam_apa7.zip
.../download/us_mit_ieee.zip
.../download/uk_oxford_mhra.zip
.../download/br_usp_abnt.zip
```

### Catalogo completo (JSON)

La app descarga este archivo para mostrar todos los perfiles y estilos:

```
https://github.com/GonzaloAndDev/TeXisStudio-Profiles/releases/latest/download/catalog.json
```

---

## Contribuir un perfil

1. **Fork** de este repositorio
2. Crea la carpeta con la jerarquia correcta: `<continente>/<pais>/<id>/`
   Ejemplo: `europe/france/fr_sorbonne_chicago17/`
3. Agrega `profile.yaml` y `manifest.yaml` (ver esquemas abajo)
4. Abre un **Pull Request**

### `manifest.yaml` minimo

```yaml
id: fr_sorbonne_chicago17
name: "Sorbonne - These (Chicago 17)"
version: "1.0.0"
author: "Tu Nombre"
license: "CC-BY-4.0"
description: "These de l'Universite Paris-Sorbonne, Chicago 17."
tags: [sorbonne, france, chicago17, humanites]
texis_min_version: "1.0.0"
continent: "europe"
country: "france"
institution: "Universite Paris-Sorbonne"
city: "Paris"
```

### `profile.yaml` minimo

```yaml
id: fr_sorbonne_chicago17
name: "Sorbonne - These (Chicago 17)"
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

---

## Licencia

Los perfiles se distribuyen bajo **CC-BY-4.0** salvo indicacion contraria en `manifest.yaml`.

Los perfiles son independientes de la licencia del software TeXisStudio (AGPL v3 + Commons Clause).
