TeXisStudio — Compilación manual
=================================

Generado con TeXisStudio
https://github.com/GonzaloAndDev/TeXisStudio
Autor original: Gonzalo Andrade Estrella

Para compilar el PDF manualmente sin la app:

  cd build
  latexmk -xelatex main.tex

O desde el directorio raíz del proyecto:

  latexmk -xelatex -cd build/main.tex

Requisitos:
  - TeX Live completo o MiKTeX
  - latexmk
  - xelatex
  - biber (para bibliografía)

Fuente de verdad del proyecto:
  tesis.project.yaml
  content/

El directorio build/ es generado automáticamente.
No es necesario versionarlo.
