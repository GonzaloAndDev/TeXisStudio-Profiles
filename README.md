# TeXisStudio — Perfiles de comunidad

Repositorio oficial de perfiles para [TeXisStudio](https://github.com/GonzaloAndDev/TeXisStudio).

Cada perfil define la estructura de secciones, estilo de bibliografía y configuración LaTeX
para un tipo de documento académico. Se pueden instalar desde la app en **Biblioteca → Comunidad**.

---

## Perfiles disponibles

| Perfil | Descripción | Bibliografía |
|---|---|---|
| `generic.thesis` | Tesis genérica — estructura completa para cualquier disciplina | APA |
| `generic.tesina` | Tesina — versión compacta para trabajos monográficos | APA |
| `apa.basic` | Tesis APA 7 — IMRyD estándar con portada y resumen | APA 7 |
| `vancouver.health` | Tesis ciencias de la salud — IMRyD con estilo Vancouver | Vancouver |
| `engineering.basic` | Reporte de ingeniería — memorias técnicas y reportes de laboratorio | IEEE |
| `company.internship` | Reporte de prácticas profesionales / estadía | APA |

---

## Instalar un perfil en TeXisStudio

### Desde la app (recomendado)

1. Abre TeXisStudio → **Biblioteca** → pestaña **Comunidad**
2. Haz clic en **Instalar** en el perfil que quieras
3. O pega la URL de descarga directa en el campo personalizado

### Descarga directa (URL para usar en la app)

```
https://github.com/GonzaloAndDev/TeXisStudio-Profiles/releases/latest/download/<perfil>.zip
```

Ejemplos:
```
https://github.com/GonzaloAndDev/TeXisStudio-Profiles/releases/latest/download/generic.thesis.zip
https://github.com/GonzaloAndDev/TeXisStudio-Profiles/releases/latest/download/apa.basic.zip
```

---

## Contribuir un perfil

1. **Fork** de este repositorio
2. Crea una carpeta con el id de tu perfil: `mi-universidad.tesis/`
3. Añade `profile.yaml` y `manifest.yaml` (ver estructura abajo)
4. Abre un **Pull Request** — los perfiles verificados se añaden a la lista curada en la app

### Estructura de un perfil

```
mi-universidad.tesis/
├── profile.yaml      ← configuración principal (obligatorio)
└── manifest.yaml     ← metadata para la biblioteca (obligatorio)
```

### `manifest.yaml` mínimo

```yaml
id: mi-universidad.tesis
name: "Tesis — Mi Universidad"
version: "1.0.0"
author: "Tu Nombre"
license: "CC-BY-4.0"
description: "Descripción breve del perfil."
tags: [tesis, licenciatura]
texis_min_version: "1.0.0"
```

### `profile.yaml` mínimo

```yaml
id: mi-universidad.tesis
name: "Tesis — Mi Universidad"
latex_engine: xelatex
document_class:
  name: book
  options: [12pt, letterpaper, oneside]
bibliography_backend: biber
bibliography_style: apa
sections:
  - id: portada
    element_id: cover
    placement: front_matter
    required: true
    title: Portada
  - id: introduccion
    element_id: chapter
    placement: body
    required: true
    title: Introducción
```

---

## Licencia

Los perfiles de este repositorio se distribuyen bajo **CC-BY-4.0** salvo indicación contraria
en el `manifest.yaml` de cada perfil.

Los perfiles son independientes de la licencia del software TeXisStudio (AGPL v3 + Commons Clause).
