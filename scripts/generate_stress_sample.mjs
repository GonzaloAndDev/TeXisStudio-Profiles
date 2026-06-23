import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { deflateSync } from "node:zlib";

const root = new URL("..", import.meta.url).pathname;
const sampleRoot = join(root, "profile_samples", "stress_professional_thesis");
const projectRoot = join(sampleRoot, "project.texis");

function ensureDir(path) {
  mkdirSync(path, { recursive: true });
}

function write(path, content) {
  ensureDir(dirname(path));
  writeFileSync(path, content);
}

function crc32(buffer) {
  let crc = 0xffffffff;
  for (const byte of buffer) {
    crc ^= byte;
    for (let i = 0; i < 8; i += 1) {
      crc = (crc >>> 1) ^ (0xedb88320 & -(crc & 1));
    }
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function pngChunk(type, data) {
  const typeBuffer = Buffer.from(type, "ascii");
  const length = Buffer.alloc(4);
  length.writeUInt32BE(data.length, 0);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(Buffer.concat([typeBuffer, data])), 0);
  return Buffer.concat([length, typeBuffer, data, crc]);
}

function makeArchitecturePng(width = 960, height = 540) {
  const raw = Buffer.alloc((width * 3 + 1) * height);
  for (let y = 0; y < height; y += 1) {
    const row = y * (width * 3 + 1);
    raw[row] = 0;
    for (let x = 0; x < width; x += 1) {
      const offset = row + 1 + x * 3;
      const lane = Math.floor(x / (width / 5));
      const band = Math.floor(y / (height / 3));
      const active = (lane + band) % 2 === 0;
      raw[offset] = active ? 55 + lane * 30 : 235;
      raw[offset + 1] = active ? 95 + band * 35 : 240;
      raw[offset + 2] = active ? 160 + lane * 12 : 245;
      if (x % Math.floor(width / 5) < 8 || y % Math.floor(height / 3) < 8) {
        raw[offset] = 38;
        raw[offset + 1] = 48;
        raw[offset + 2] = 64;
      }
    }
  }

  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(width, 0);
  ihdr.writeUInt32BE(height, 4);
  ihdr[8] = 8;
  ihdr[9] = 2;
  ihdr[10] = 0;
  ihdr[11] = 0;
  ihdr[12] = 0;

  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    pngChunk("IHDR", ihdr),
    pngChunk("IDAT", deflateSync(raw)),
    pngChunk("IEND", Buffer.alloc(0)),
  ]);
}

const citations = [
  "lamport1994latex",
  "knuth1984texbook",
  "mittelbach2004latex",
  "kottwitz2015latex",
  "bringhurst2012elements",
  "creswell2018research",
  "yin2018case",
  "wacker1998definition",
  "gelman2013bayesian",
  "tufte2001visual",
  "few2012show",
  "montgomery2017design",
  "box1976science",
  "wilkinson2005grammar",
  "mckinney2010data",
  "harris2020array",
  "hunter2007matplotlib",
  "wickham2016ggplot2",
  "wilson2014best",
  "sandve2013ten",
  "smith2020reproducibility",
  "perkel2020challenge",
  "borrego2014engineering",
  "prince2004inductive",
  "biggs2011teaching",
  "apa2020manual",
  "ieee2023editorial",
  "iso1900522020",
  "springer2022latex",
  "overleaf2024guide",
];

function paragraph(id, content, verbatim = false) {
  return { type: "paragraph", id, content, verbatim };
}

function heading(id, content, level = "section") {
  return { type: "heading", id, level, content };
}

function citation(id, key, citation_type = "parenthetical", suffix = undefined) {
  return {
    type: "citation",
    id,
    citation_key: key,
    citation_type,
    page: null,
    prefix: null,
    suffix: suffix ?? null,
  };
}

function equation(id, latex, label, numbered = true) {
  return { type: "equation", id, latex_content: latex, label, numbered };
}

function table(id, caption, label, headers, rows, table_style = "booktabs") {
  return {
    type: "table",
    id,
    caption,
    source: "Elaboracion propia para fixture de estres",
    label,
    include_in_list: true,
    raw_headers: true,
    raw_cells: true,
    verbatim_caption: true,
    headers,
    rows,
    table_style,
  };
}

function section(id, element_id, title, placement, blocks, required = true) {
  return {
    id,
    element_id,
    title,
    placement,
    required,
    enabled: true,
    label: placement === "body" ? `cap:${id}` : null,
    blocks,
    fields: {},
    children: [],
  };
}

function longAcademicParagraph(chapter, idx) {
  const phase = [
    "levantamiento de requisitos institucionales",
    "normalizacion semantica del manuscrito",
    "validacion cruzada de fuentes oficiales",
    "generacion controlada de artefactos LaTeX",
    "revision editorial asistida",
    "exportacion reproducible del expediente final",
  ][idx % 6];
  const metric = ["trazabilidad", "consistencia", "mantenibilidad", "claridad", "replicabilidad"][idx % 5];
  return [
    `En el capitulo ${chapter}, la fase de ${phase} se analiza como un componente operativo del flujo academico profesional.`,
    `El criterio de ${metric} se evalua mediante listas de verificacion, evidencia documental y pruebas de compilacion que reducen la ambiguedad entre lo que la institucion solicita y lo que el documento realmente produce.`,
    `La decision metodologica principal consiste en separar el contenido intelectual del estudiante de las reglas mecanicas de formato, de modo que portada, margenes, bibliografia, anexos y metadatos puedan auditarse sin reescribir el texto central.`,
    `Esta separacion tambien permite que usuarios de instituciones distintas construyan perfiles propios a partir de ejemplos confiables sin asumir que un perfil generico resuelve todas las obligaciones locales.`,
  ].join(" ");
}

function makeNarrativeBlocks(chapterId, chapterNumber, count) {
  const blocks = [];
  for (let i = 1; i <= count; i += 1) {
    if (i % 5 === 1) blocks.push(heading(`${chapterId}-h-${i}`, `Analisis ${chapterNumber}.${Math.ceil(i / 5)}`, i % 10 === 1 ? "section" : "subsection"));
    blocks.push(paragraph(`${chapterId}-p-${i}`, longAcademicParagraph(chapterNumber, i)));
    if (i % 4 === 0) blocks.push(citation(`${chapterId}-c-${i}`, citations[(chapterNumber * 3 + i) % citations.length]));
  }
  return blocks;
}

function pluginFigure() {
  return {
    type: "plugin_figure",
    id: "pf-quality-dashboard",
    figureId: "fig_quality_dashboard",
    pluginId: "pgfplots-bar",
    latexBlock: [
      "% texisstudio-figure-id: fig_quality_dashboard",
      "\\begin{figure}[htbp]",
      "  \\centering",
      "  \\begin{tikzpicture}",
      "    \\begin{axis}[",
      "      ybar,",
      "      width=0.82\\textwidth,",
      "      height=7cm,",
      "      ymin=0, ymax=100,",
      "      ylabel={Cobertura (\\%)},",
      "      symbolic x coords={Fuentes,Portada,Margenes,Bibliografia,Anexos,Export},",
      "      xtick=data,",
      "      x tick label style={rotate=35,anchor=east},",
      "      nodes near coords,",
      "      grid=major",
      "    ]",
      "      \\addplot[fill=blue!45] coordinates {(Fuentes,96) (Portada,92) (Margenes,98) (Bibliografia,94) (Anexos,89) (Export,97)};",
      "    \\end{axis}",
      "  \\end{tikzpicture}",
      "  \\caption{Panel sintetico de cobertura del perfil profesional usado en la tesis de estres.}",
      "  \\label{fig:quality-dashboard}",
      "\\end{figure}",
      "% /texisstudio-figure-id",
    ].join("\n"),
    caption: "Panel sintetico de cobertura del perfil profesional usado en la tesis de estres.",
    label: "fig:quality-dashboard",
    requiredPackages: ["pgfplots", "tikz"],
    sourceJson: JSON.stringify({ engineId: "pgfplots-bar", version: "1.0.0", fixture: true }),
    warnings: [],
  };
}

const sections = [
  section("title_page", "title_page", "Portada", "front_matter", []),
  section("dedication", "dedication", "Dedicatoria", "front_matter", [
    paragraph("ded-p1", "A quienes convierten reglas confusas en herramientas claras y confiables."),
  ], false),
  section("acknowledgements", "acknowledgements", "Agradecimientos", "front_matter", [
    paragraph("ack-p1", "Se agradece al equipo de revision, a las personas usuarias que prueban perfiles institucionales y a quienes documentan lineamientos oficiales de manera publica y verificable."),
  ], false),
  section("abstract_es", "abstract_es", "Resumen", "front_matter", [
    paragraph("abs-es-p1", "Esta tesis de prueba evalua un flujo profesional para construir, validar y exportar documentos academicos largos con TeXisStudio. El caso de estudio combina perfil institucional, checklist de evidencia, fuentes oficiales, configuracion tipografica, bibliografia, figuras, tablas, ecuaciones, algoritmos, glosario y anexos. La metodologia se disena como una prueba de estres reproducible: cada capitulo introduce bloques heterogeneos y referencias cruzadas, mientras el proyecto conserva compatibilidad con la generacion LaTeX automatica y la exportacion final. Los resultados esperados son un PDF extenso, estable y auditable, junto con archivos fuente suficientes para detectar regresiones en perfiles, plugins visuales y validadores."),
  ]),
  section("abstract_en", "abstract_en", "Abstract", "front_matter", [
    paragraph("abs-en-p1", "This stress thesis evaluates a professional workflow for building, validating, and exporting long academic documents with TeXisStudio. The case study combines institutional profiles, evidence checklists, official sources, typographic configuration, bibliography, figures, tables, equations, algorithms, glossary entries, and appendices. The methodology is reproducible: each chapter introduces heterogeneous blocks and cross references while preserving compatibility with automatic LaTeX generation and final delivery export."),
  ], false),
  section("table_of_contents", "table_of_contents", "Indice General", "front_matter", []),
  section("list_of_figures", "list_of_figures", "Lista de Figuras", "front_matter", [], false),
  section("list_of_tables", "list_of_tables", "Lista de Tablas", "front_matter", [], false),
];

const introBlocks = [
  ...makeNarrativeBlocks("intro", 1, 16),
  {
    type: "figure",
    id: "fig-architecture",
    file: "arquitectura_validacion.png",
    caption: "Arquitectura conceptual del flujo de validacion profesional de perfiles.",
    source: "Fixture generado automaticamente",
    width: "full",
    label: "fig:architecture",
    include_in_list: true,
  },
  paragraph("intro-ref-fig", "La Figura~\\ref{fig:architecture} resume el flujo de evidencia desde fuentes oficiales hasta exportacion final.", true),
];

const theoryBlocks = [
  ...makeNarrativeBlocks("theory", 2, 18),
  equation("eq-confidence", "C_p = 0.35S + 0.25R + 0.20B + 0.10L + 0.10E", "eq:confidence"),
  equation("eq-risk", "R_f = \\sum_{i=1}^{n} w_i \\cdot p_i \\cdot I_i", "eq:risk"),
  paragraph("theory-eq-ref", "Las ecuaciones~\\eqref{eq:confidence} y~\\eqref{eq:risk} formalizan la confianza editorial y el riesgo residual de formato que se usa para priorizar revisiones.", true),
  table("tab-profile-dimensions", "Dimensiones de calidad verificadas por el perfil profesional", "tab:profile-dimensions", ["Dimension", "Evidencia", "Validacion", "Riesgo cubierto"], [
    ["Fuente oficial", "URL institucional", "HTTPS + revision humana", "Reglas obsoletas"],
    ["Portada", "Campos de grado y comite", "Checklist estructural", "Rechazo administrativo"],
    ["Margenes", "Layout declarado", "Comparacion YAML", "Formato inconsistente"],
    ["Bibliografia", "Backend y estilo", "Compilacion biber", "Citas rotas"],
    ["Entrega", "PDF y paquete exportado", "CI + artifact", "Entrega incompleta"],
  ]),
  paragraph("theory-tab-ref", "La Tabla~\\ref{tab:profile-dimensions} resume las dimensiones minimas que un perfil profesional debe cubrir antes de considerarse confiable.", true),
  {
    type: "theorem",
    id: "thm-traceability",
    kind: "proposition",
    title: "Trazabilidad minima de un perfil revisado",
    content: "Si un perfil declara estado revisado, entonces debe existir al menos una fuente institucional HTTPS, una fecha de revision y una correspondencia verificable entre reglas declaradas y estructura generada.",
    verbatim: false,
    numbered: true,
  },
];

const methodBlocks = [
  ...makeNarrativeBlocks("method", 3, 18),
  {
    type: "algorithm",
    id: "alg-review-flow",
    caption: "Promocion controlada de perfil desde borrador hasta verificado",
    label: "alg:review-flow",
    input: "Perfil $P$, fuentes $F$, muestra compilable $M$",
    output: "Estado final $draft$, $reviewed$ o $verified$",
    body: [
      "\\State Validar estructura minima de $P$",
      "\\State Verificar que cada fuente en $F$ use HTTPS institucional",
      "\\State Comparar portada, margenes, secciones y bibliografia contra checklist",
      "\\If{faltan fuentes o fecha de revision}",
      "  \\State Mantener $P$ como borrador",
      "\\ElsIf{compila $M$ y existe evidencia CI}",
      "  \\State Promover $P$ a verificado",
      "\\Else",
      "  \\State Promover $P$ solamente a revisado",
      "\\EndIf",
    ].join("\n"),
  },
  {
    type: "code",
    id: "code-quality-score",
    language: "Python",
    caption: "Calculo reproducible de confianza del perfil",
    label: "lst:quality-score",
    content: [
      "weights = {'sources': 0.35, 'review': 0.25, 'build': 0.20, 'layout': 0.10, 'export': 0.10}",
      "signals = {'sources': 0.96, 'review': 0.91, 'build': 1.00, 'layout': 0.98, 'export': 0.97}",
      "score = sum(weights[k] * signals[k] for k in weights)",
      "print(f'profile confidence = {score:.3f}')",
    ].join("\n"),
    show_line_numbers: true,
  },
  pluginFigure(),
];

const resultsBlocks = [
  ...makeNarrativeBlocks("results", 4, 22),
  table("tab-long-matrix", "Matriz extendida de pruebas por modulo", "tab:long-matrix", ["Modulo", "Caso", "Entrada", "Salida esperada", "Estado"], Array.from({ length: 28 }, (_, i) => [
    ["Perfil", "Wizard", "Editor", "Compilador", "Exportador", "i18n", "Plugin"][i % 7],
    `Caso ${i + 1}`,
    ["YAML", "Figura", "Tabla", "Cita", "Glosario", "PDF/A", "ZIP"][i % 7],
    ["Sin errores", "Advertencia clara", "Artifact generado", "Chunk separado"][i % 4],
    "OK",
  ]), "long"),
  paragraph("results-table-ref", "La Tabla~\\ref{tab:long-matrix} funciona como una matriz larga para presionar el render de tablas extensas, listas y paginacion.", true),
  {
    type: "raw_latex",
    id: "raw-landscape-note",
    content: "\\noindent\\textbf{Nota tecnica:} este bloque LaTeX manual esta confirmado y se usa para comprobar que las inserciones avanzadas no rompen el documento cuando el usuario sabe exactamente lo que esta integrando.",
    user_confirmed: true,
  },
  equation("eq-throughput", "T = \\frac{N_{bloques}}{t_{generacion} + t_{compilacion} + t_{exportacion}}", "eq:throughput"),
  paragraph("results-eq-ref", "La ecuacion~\\eqref{eq:throughput} permite interpretar el rendimiento del flujo como una relacion entre volumen documental y costo de procesamiento.", true),
];

const discussionBlocks = [
  ...makeNarrativeBlocks("discussion", 5, 20),
  table("tab-latex-boundaries", "Limites profesionales de LaTeX y alternativas integrables", "tab:latex-boundaries", ["Necesidad", "LaTeX directo", "Alternativa", "Integracion recomendada"], [
    ["Graficas estadisticas complejas", "PGFPlots posible pero costoso", "Python/R", "Exportar PDF/PNG y registrar fuente"],
    ["Diagramas CAD", "No recomendable", "Herramienta CAD externa", "Incluir vector final"],
    ["Quimica avanzada", "mhchem/chemfig parcial", "Editor especializado", "Importar resultado revisado"],
    ["Datos masivos", "Tablas largas limitadas", "CSV procesado", "Resumen + anexo externo"],
    ["Revision institucional", "No automatizable al 100\\%", "Checklist humano", "Status reviewed/verified"],
  ]),
  paragraph("discussion-tab-ref", "La Tabla~\\ref{tab:latex-boundaries} explicita los limites que no deben prometerse desde la app aunque LaTeX sea potente.", true),
  citation("discussion-extra-c1", "gelman2013bayesian"),
  citation("discussion-extra-c2", "bringhurst2012elements"),
  citation("discussion-extra-c3", "box1976science"),
  citation("discussion-extra-c4", "tufte2001visual"),
];

const conclusionBlocks = [
  ...makeNarrativeBlocks("conclusion", 6, 12),
  {
    type: "list",
    id: "conc-list",
    list_type: "enumerate",
    items: [
      "El perfil debe ensenar a construir perfiles propios, no prometer cobertura universal.",
      "La evidencia institucional debe ser trazable y separada de la evidencia tecnica de CI.",
      "Los plugins visuales son utiles cuando reducen complejidad, pero deben permitir integrar resultados externos.",
      "Una tesis larga revela errores que no aparecen en documentos pequenos.",
    ],
  },
];

const glossaryBlocks = [
  { type: "glossary_entry", id: "g-profile", term: "Perfil institucional", definition: "Conjunto versionado de reglas, fuentes y decisiones de formato que guian la generacion de un documento academico.", verbatim: false },
  { type: "glossary_entry", id: "g-ci", term: "Evidencia CI", definition: "Ejecucion automatizada que valida estructura, compila el documento y conserva artefactos de entrega.", verbatim: false },
  { type: "glossary_entry", id: "g-fixture", term: "Fixture de estres", definition: "Proyecto sintetico pero realista usado para detectar regresiones en modulos complejos.", verbatim: false },
  { type: "acronym_entry", id: "acr-pdfa", acronym: "PDF/A", full_form: "Portable Document Format Archival", description: "Familia de estandares ISO para preservacion documental." },
  { type: "acronym_entry", id: "acr-ci", acronym: "CI", full_form: "Continuous Integration", description: "Integracion continua usada para validar perfiles y muestras." },
  { type: "acronym_entry", id: "acr-yaml", acronym: "YAML", full_form: "YAML Ain't Markup Language", description: "Formato legible para configuracion estructurada." },
];

sections.push(
  section("introduction", "introduction", "Introduccion", "body", introBlocks),
  section("theoretical_framework", "theoretical_framework", "Marco teorico y criterios de calidad", "body", theoryBlocks),
  section("methodology", "methodology", "Metodologia de validacion", "body", methodBlocks),
  section("results", "results", "Resultados de la prueba de estres", "body", resultsBlocks),
  section("discussion", "discussion", "Discusion profesional y limites de LaTeX", "body", discussionBlocks),
  section("conclusions", "conclusions", "Conclusiones", "body", conclusionBlocks),
  section("glossary", "glossary_section", "Glosario", "back_matter", glossaryBlocks, false),
  section("references", "references", "Referencias", "back_matter", [], true),
  section("appendix_a", "appendix", "Apendice A: Matriz de evidencia", "appendix", [
    ...makeNarrativeBlocks("appendix-a", 7, 14),
    table("tab-appendix-evidence", "Registro de evidencia por requisito", "tab:appendix-evidence", ["ID", "Requisito", "Fuente", "Decision"], Array.from({ length: 24 }, (_, i) => [`REQ-${String(i + 1).padStart(2, "0")}`, `Requisito documental ${i + 1}`, `Fuente oficial ${1 + (i % 5)}`, i % 3 === 0 ? "Automatizado" : "Revision humana"]), "long"),
    paragraph("appendix-a-table-ref", "La Tabla~\\ref{tab:appendix-evidence} conserva la trazabilidad granular entre requisito, fuente y decision de implementacion.", true),
  ], false),
  section("appendix_b", "appendix_b", "Apendice B: Configuraciones alternativas", "appendix", [
    ...makeNarrativeBlocks("appendix-b", 8, 12),
    equation("eq-appendix-cost", "K = C_m + C_r + C_e + C_s", "eq:appendix-cost"),
    paragraph("appendix-b-eq-ref", "La ecuacion~\\eqref{eq:appendix-cost} resume el costo total de mantenimiento como suma de cambios mecanicos, revision, exportacion y soporte.", true),
  ], false),
);

const project = {
  schema_version: "1.0.0",
  id: "stress-professional-thesis-001",
  created_at: "2026-06-23T00:00:00Z",
  updated_at: "2026-06-23T00:00:00Z",
  profile_id: "mx_unam_apa7",
  metadata: {
    title: "Diseno y validacion de perfiles academicos profesionales para documentos largos reproducibles",
    document_kind: "tesis",
    academic_level: "doctorado",
    language: "es",
    city: "Ciudad de Mexico",
    year: 2026,
    keywords: ["perfiles academicos", "LaTeX", "validacion", "reproducibilidad", "TeXisStudio"],
  },
  institution: {
    name: "Universidad Nacional Autonoma de Mexico",
    faculty: "Posgrado en Ingenieria",
    department: "Laboratorio de Documentos Academicos Reproducibles",
    country: "Mexico",
  },
  student: {
    full_name: "Valeria Mariana Rios Salgado",
    email: "valeria.rios@example.edu",
    advisors: ["Dra. Elena Torres Aguilar", "Dr. Martin Cardenas Vega"],
    committee: [
      { full_name: "Dra. Elena Torres Aguilar", role: "Directora de tesis" },
      { full_name: "Dr. Martin Cardenas Vega", role: "Codirector" },
      { full_name: "Dra. Lucia Hernandez Soto", role: "Presidenta del jurado" },
      { full_name: "Dr. Rafael Nunez Ibarra", role: "Vocal" },
      { full_name: "Dra. Paola Medina Cruz", role: "Secretaria" },
    ],
  },
  latex_config: {
    document_class: { name: "book", options: ["12pt", "letterpaper", "oneside"] },
    engine: "xelatex",
    compiler: "latexmk",
    bibliography_backend: "biber",
    bibliography_style: "apa",
    packages_required: [],
    typography: {},
    page_layout: {
      paper: "letterpaper",
      margins: { top: "25mm", bottom: "25mm", left: "30mm", right: "20mm" },
      line_spacing: 1.5,
    },
  },
  sections,
  file_states: {},
};

const bib = citations.map((key, index) => {
  const year = 1994 + (index % 31);
  const title = key
    .replace(/[0-9]/g, "")
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace(/[-_]/g, " ");
  return `@article{${key},
  author = {Autor ${index + 1} and Colaborador ${index + 1}},
  title = {${title.charAt(0).toUpperCase() + title.slice(1)} applied to reproducible academic documents},
  journal = {Journal of Professional Document Engineering},
  year = {${year}},
  volume = {${1 + (index % 12)}},
  number = {${1 + (index % 4)}},
  pages = {${10 + index}--${24 + index}},
  doi = {10.5555/texis.${String(index + 1).padStart(4, "0")}}
}`;
}).join("\n\n");


const checklist = {
  schema_version: "1.0.0",
  profile_id: "mx_unam_apa7",
  description: "Stress fixture for a long professional thesis with heterogeneous blocks, plugin figures, bibliography, glossary, appendices, export, and a target around 50 PDF pages.",
  expected: {
    validation_errors: 0,
    required_sections_present: ["title_page", "abstract_es", "abstract_en", "table_of_contents", "introduction", "theoretical_framework", "methodology", "results", "discussion", "conclusions", "references", "appendix"],
    max_abstract_words_limit: 350,
    page_layout: {
      paper: "letterpaper",
      margins: { top: "25mm", bottom: "25mm", left: "30mm", right: "20mm" },
      line_spacing: 1.5,
    },
    latex_engine: "xelatex",
    bibliography_backend: "biber",
    bibliography_style: "apa",
  },
  notes: "Includes 150+ narrative blocks, 30 citations, long tables, equations, theorem, algorithm, code, raw LaTeX, regular figure, plugin PGFPlots figure, glossary/acronyms, and appendices.",
};

ensureDir(projectRoot);
write(join(sampleRoot, ".gitignore"), "delivery/\n");
write(join(projectRoot, ".gitignore"), "build/\ndelivery/\n");
write(join(projectRoot, "README-compilacion.txt"), "Stress thesis sample generated by scripts/generate_stress_sample.mjs.\nUse texis validate, texis compile --backend latexmk, and texis export-delivery.\n");
write(join(projectRoot, "tesis.project.yaml"), `${JSON.stringify(project, null, 2)}\n`);
write(join(projectRoot, "content", "bibliography", "references.bib"), `${bib}\n`);
write(join(projectRoot, "content", "figures", "arquitectura_validacion.png"), makeArchitecturePng());
write(join(sampleRoot, "expected_checklist.json"), `${JSON.stringify(checklist, null, 2)}\n`);

console.log(`Generated ${sampleRoot}`);
console.log(`Sections: ${sections.length}`);
console.log(`Blocks: ${sections.reduce((sum, s) => sum + s.blocks.length, 0)}`);
