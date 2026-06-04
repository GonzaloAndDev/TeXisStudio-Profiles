"""Build locale JSON files for profile metadata and guidance text.

The profiles repo owns its product text because profile names, institution
descriptions, section titles, and guidance are part of each profile package.
This script extracts the current Spanish/source strings into i18n/es.json so
the app can resolve localized text without depending on TeXisStudio-Languages.
"""
import json
import os
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(".")
OUT_DIR = ROOT / "i18n"
ES_OUT_PATH = OUT_DIR / "es.json"
EN_OUT_PATH = OUT_DIR / "en.json"

TITLE_EN = {
    "Agradecimientos": "Acknowledgements",
    "Anexos": "Appendices",
    "Análisis y Resultados": "Analysis and Results",
    "Apéndices": "Appendices",
    "Bibliografía": "Bibliography",
    "Capa": "Cover",
    "Capitulos": "Chapters",
    "Conclusao": "Conclusion",
    "Conclusiones": "Conclusions",
    "Conclusiones y Perspectivas": "Conclusions and Outlook",
    "Conclusiones y Recomendaciones": "Conclusions and Recommendations",
    "Conclusiones y Trabajo Futuro": "Conclusions and Future Work",
    "Declaración Jurada de Autoría": "Sworn Authorship Statement",
    "Declaración de Autenticidad": "Authenticity Statement",
    "Declaración de Autoría": "Authorship Statement",
    "Declaración de Autoría y Originalidad": "Authorship and Originality Statement",
    "Declaración de Integridad Académica": "Academic Integrity Statement",
    "Declaración de Originalidad": "Originality Statement",
    "Dedicatoria": "Dedication",
    "Desarrollo": "Development",
    "Discusión": "Discussion",
    "Estado del Arte": "State of the Art",
    "Folha de Rosto": "Title Page",
    "Fuentes de Consulta": "Sources Consulted",
    "Glosario": "Glossary",
    "Introducao": "Introduction",
    "Introducción": "Introduction",
    "Introducción y Antecedentes": "Introduction and Background",
    "Lista de Abreviaturas y Acrónimos": "List of Abbreviations and Acronyms",
    "Lista de Cuadros": "List of Tables",
    "Lista de Figuras": "List of Figures",
    "Lista de Tablas": "List of Tables",
    "Marco Conceptual": "Conceptual Framework",
    "Marco Referencial": "Reference Framework",
    "Marco Teórico": "Theoretical Framework",
    "Marco Teórico y Estado del Arte": "Theoretical Framework and State of the Art",
    "Marco Teórico y Revisión de Literatura": "Theoretical Framework and Literature Review",
    "Marco Teórico y Revisión de la Literatura": "Theoretical Framework and Literature Review",
    "Marco Teórico-Conceptual": "Theoretical and Conceptual Framework",
    "Material y Métodos": "Materials and Methods",
    "Metodología": "Methodology",
    "Metodología / Intervención": "Methodology / Intervention",
    "Metodología y Desarrollo Experimental": "Methodology and Experimental Development",
    "Portada": "Title Page",
    "Referencias": "References",
    "Resultados": "Results",
    "Resultados y Análisis": "Results and Analysis",
    "Resultados y Discusión": "Results and Discussion",
    "Resumen": "Abstract",
    "Resumo": "Abstract",
    "Sumario": "Table of Contents",
    "Tabla de Contenido": "Table of Contents",
    "Índice": "Table of Contents",
    "Índice General": "Table of Contents",
    "Índice de Figuras": "List of Figures",
    "Índice de Tablas": "List of Tables",
}

TITLE_ES = {
    "Abstract": "Resumen",
    "Abstract (in English)": "Resumen en inglés",
    "Acknowledgements": "Agradecimientos",
    "Acknowledgements / Danksagung": "Agradecimientos / Danksagung",
    "Acknowledgements / Dankwoord": "Agradecimientos / Dankwoord",
    "Appendices": "Apéndices",
    "Background": "Antecedentes",
    "Background and Literature Review": "Antecedentes y revisión de literatura",
    "Background and Related Work": "Antecedentes y trabajo relacionado",
    "Bibliography": "Bibliografía",
    "Chapter 1": "Capítulo 1",
    "Chapter 2": "Capítulo 2",
    "Chapter 3": "Capítulo 3",
    "Chapter 4": "Capítulo 4",
    "Chapter Two": "Capítulo dos",
    "Chapter Three": "Capítulo tres",
    "Conclusion": "Conclusión",
    "Conclusion and Future Work": "Conclusión y trabajo futuro",
    "Conclusion and Outlook": "Conclusión y perspectivas",
    "Conclusions and Future Work": "Conclusiones y trabajo futuro",
    "Conclusions and Recommendations": "Conclusiones y recomendaciones",
    "Copyright": "Derechos de autor",
    "Declaration": "Declaración",
    "Dedication": "Dedicatoria",
    "Discussion": "Discusión",
    "Empirical Analysis": "Análisis empírico",
    "Experimental Evaluation": "Evaluación experimental",
    "Experimental Results": "Resultados experimentales",
    "General Conclusions": "Conclusiones generales",
    "Historiography / State of the Field": "Historiografía / estado del campo",
    "Introduction": "Introducción",
    "List of Abbreviations": "Lista de abreviaturas",
    "List of Figures": "Lista de figuras",
    "List of Figures / Illustrations": "Lista de figuras / ilustraciones",
    "List of Tables": "Lista de tablas",
    "Literature Review": "Revisión de literatura",
    "Method and Sources": "Método y fuentes",
    "Methodology": "Metodología",
    "Methodology and Sources": "Metodología y fuentes",
    "Proposed Approach": "Enfoque propuesto",
    "Proposed Approach / Methodology": "Enfoque propuesto / metodología",
    "Proposed Methodology": "Metodología propuesta",
    "References": "Referencias",
    "Research Design": "Diseño de investigación",
    "Results": "Resultados",
    "Results / Findings": "Resultados / hallazgos",
    "Summary": "Resumen",
    "Summary (Abstract in English)": "Resumen en inglés",
    "Table of Contents": "Índice",
    "Theoretical Background and Literature Review": "Antecedentes teóricos y revisión de literatura",
    "Theoretical Framework": "Marco teórico",
    "Theory and Literature": "Teoría y literatura",
    "Title Page": "Portada",
}

PHRASE_EN = [
    ("Tesis Genérica", "Generic Thesis"),
    ("Tesina Genérica", "Generic Short Thesis"),
    ("Trabajo de Especialidad Genérico", "Generic Specialty Project"),
    ("Tesis/Disertación", "Thesis/Dissertation"),
    ("Tesis Doctoral", "Doctoral Thesis"),
    ("Tesis", "Thesis"),
    ("Tesina", "Short Thesis"),
    ("Dissertacao", "Dissertation"),
    ("Dissertação", "Dissertation"),
    ("Declaración Jurada", "Sworn Statement"),
    ("Declaración de Integridad Académica", "Academic Integrity Statement"),
    ("Declaración de Autoría y Originalidad", "Authorship and Originality Statement"),
    ("Declaración de Autoría", "Authorship Statement"),
    ("Declaración de Originalidad", "Originality Statement"),
    ("guidance completa en español", "complete guidance in English"),
    ("guidance en español", "guidance in English"),
    ("lineamientos", "guidelines"),
    ("Lineamientos", "Guidelines"),
    ("perfil politécnico/ingeniería", "polytechnic/engineering profile"),
    ("Declaración de Integridad Académica", "Academic Integrity Statement"),
    ("doble espacio", "double spacing"),
    ("estilo APA 7ª edición", "APA 7th edition style"),
    ("estructura completa", "complete structure"),
    ("estructura IMRD", "IMRaD structure"),
    ("Plantilla genérica para", "Generic template for"),
    ("trabajos académicos", "academic papers"),
    ("tesis de licenciatura, maestría o doctorado", "bachelor's, master's, or doctoral theses"),
    ("tesinas y trabajos académicos", "short theses and academic papers"),
    ("español", "English"),
    ("Español", "English"),
    ("Universidad Nacional Autonoma de Mexico", "National Autonomous University of Mexico"),
    ("Universidad Autonoma de Nuevo Leon", "Autonomous University of Nuevo Leon"),
    ("Universidad de Buenos Aires", "University of Buenos Aires"),
    ("Universidad de Chile", "University of Chile"),
    ("Universidad de Guadalajara", "University of Guadalajara"),
    ("Instituto Politecnico Nacional", "National Polytechnic Institute"),
    ("Tecnologico de Monterrey", "Tecnologico de Monterrey"),
    ("Universidade Estadual de Campinas", "State University of Campinas"),
    ("Universidade de Sao Paulo", "University of Sao Paulo"),
    ("Generado automáticamente", "Generated automatically"),
    ("Números de página exactos", "Exact page numbers"),
    ("Activa si tienes", "Enable it if you have"),
    ("o más figuras", "or more figures"),
    ("o más tablas", "or more tables"),
    ("Resumen en español", "Abstract in English"),
    ("Abstract en inglés", "English abstract"),
    ("Recomendado para visibilidad internacional", "Recommended for international visibility"),
    ("Máximo", "Maximum"),
    ("palabras", "words"),
    ("Palabras clave", "Keywords"),
    ("Problema, objetivos, metodología, resultados y conclusiones", "Problem, objectives, methodology, results, and conclusions"),
    ("Reconoce al director/a", "Acknowledge the advisor"),
    ("comisión evaluadora", "review committee"),
    ("fuentes", "sources"),
    ("Incluye número de proyecto o beca", "Include the project or scholarship number"),
    ("Contextualización", "Context"),
    ("planteamiento del problema", "problem statement"),
    ("justificación", "rationale"),
    ("preguntas de investigación", "research questions"),
    ("objetivos", "objectives"),
    ("hipótesis", "hypotheses"),
    ("Estructura", "Structure"),
    ("Revisión crítica", "Critical review"),
    ("fundamentos conceptuales", "conceptual foundations"),
    ("Organiza por corrientes teóricas", "Organize by theoretical approaches"),
    ("Identifica el vacío de la tesis", "Identify the thesis gap"),
    ("Diseño, muestra, instrumentos, procedimiento, análisis", "Design, sample, instruments, procedure, and analysis"),
    ("Aprobación del Comité de Ética institucional si involucra seres humanos", "Institutional ethics committee approval if human participants are involved"),
    ("Hallazgos objetivos", "Objective findings"),
    ("Tablas y figuras", "Tables and figures"),
    ("Sin interpretación", "No interpretation"),
    ("Interpretación", "Interpretation"),
    ("comparación con literatura", "comparison with the literature"),
    ("implicaciones y limitaciones", "implications and limitations"),
    ("Responde objetivos", "Answer the objectives"),
    ("resume aportaciones", "summarize contributions"),
    ("limitaciones y trabajo futuro", "limitations and future work"),
    ("lista alfabética", "alphabetical list"),
    ("sangría francesa", "hanging indent"),
    ("Instrumentos, datos adicionales, dictamen ético", "Instruments, additional data, ethics approval"),
    ("Apéndice", "Appendix"),
    ("La portada oficial", "The official title page"),
    ("La portada", "The title page"),
    ("portada oficial", "official title page"),
    ("portada", "title page"),
    ("incluye", "includes"),
    ("Incluye", "Include"),
    ("Logotipo", "Logo"),
    ("logotipo", "logo"),
    ("nombre de la universidad", "name of the university"),
    ("nombre de la institución", "name of the institution"),
    ("nombre de la Facultad", "name of the Faculty"),
    ("Nombre de la Facultad", "Faculty name"),
    ("Nombre completo", "Full name"),
    ("nombre completo", "full name"),
    ("Nombre del autor", "Author name"),
    ("Nombre completo del autor", "Author's full name"),
    ("Nombre completo del autor/a", "Author's full name"),
    ("Título completo", "Full title"),
    ("título completo", "full title"),
    ("Título de la tesis", "Thesis title"),
    ("título de la tesis", "thesis title"),
    ("Título completo de la tesis", "Full thesis title"),
    ("Nombre del programa de doctorado", "Doctoral program name"),
    ("programa de doctorado", "doctoral program"),
    ("Facultad", "Faculty"),
    ("facultad", "faculty"),
    ("Departamento", "Department"),
    ("departamento", "department"),
    ("Escuela", "School"),
    ("escuela", "school"),
    ("Centro Universitario", "University Center"),
    ("Centro", "Center"),
    ("centro", "center"),
    ("División", "Division"),
    ("división", "division"),
    ("unidad académica", "academic unit"),
    ("Cada", "Each"),
    ("cada", "each"),
    ("tiene un formato", "has a format"),
    ("formato específico", "specific format"),
    ("formato de title page específico", "specific title page format"),
    ("descárgalo", "download it"),
    ("Descarga", "Download"),
    ("Verifica", "Check"),
    ("verifica", "check"),
    ("Consulta", "Consult"),
    ("consulta", "consult"),
    ("Secretaría de Posgrado", "Graduate Office"),
    ("Coordinación de Doctorado", "Doctoral Coordination Office"),
    ("Coordinación de Posgrado", "Graduate Coordination Office"),
    ("Dirección de Posgrado", "Graduate Office"),
    ("programa de posgrado", "graduate program"),
    ("posgrado", "graduate studies"),
    ("licenciatura", "bachelor's degree"),
    ("maestría", "master's degree"),
    ("doctorado", "doctoral degree"),
    ("Doctor/a", "Doctor"),
    ("director/a", "advisor"),
    ("Director/a", "Advisor"),
    ("director de tesis", "thesis advisor"),
    ("directora de tesis", "thesis advisor"),
    ("asesor principal", "main advisor"),
    ("co-asesor", "co-advisor"),
    ("co-director/a", "co-advisor"),
    ("si aplica", "if applicable"),
    ("Mes", "Month"),
    ("Año", "Year"),
    ("Ciudad de México", "Mexico City"),
    ("Requerido", "Required"),
    ("requerido", "required"),
    ("requerida", "required"),
    ("Obligatorio", "Required"),
    ("Obligatoria", "Required"),
    ("obligatorio", "required"),
    ("opcional", "optional"),
    ("Opcional", "Optional"),
    ("convencional", "customary"),
    ("La UBA exige", "UBA requires"),
    ("La UCM exige", "UCM requires"),
    ("exige", "requires"),
    ("requiere", "requires"),
    ("puede requerir", "may require"),
    ("puede exigir", "may require"),
    ("Algunas facultades requieren", "Some faculties require"),
    ("Algunas universidades exigen", "Some universities require"),
    ("formulario específico firmado", "specific signed form"),
    ("formato específico firmado", "specific signed form"),
    ("Texto estándar", "Standard text"),
    ("declara bajo juramento", "declares under oath"),
    ("declaro", "I declare"),
    ("presente tesis", "this thesis"),
    ("presente trabajo", "this work"),
    ("es de su autoría", "is their own work"),
    ("es de mi autoría", "is my own work"),
    ("autoría", "authorship"),
    ("Autoría", "Authorship"),
    ("originalidad", "originality"),
    ("Originalidad", "Originality"),
    ("correctamente citadas", "correctly cited"),
    ("debidamente citadas", "properly cited"),
    ("correctamente citados", "correctly cited"),
    ("normas", "standards"),
    ("séptima edición", "seventh edition"),
    ("séptima", "seventh"),
    ("edición", "edition"),
    ("Debe incluir", "It must include"),
    ("debe incluir", "must include"),
    ("Debe ser", "It must be"),
    ("Debe", "It must"),
    ("Misma estructura", "Same structure"),
    ("misma estructura", "same structure"),
    ("al final", "at the end"),
    ("Al final", "At the end"),
    ("autocontenido", "self-contained"),
    ("Autocontenido", "Self-contained"),
    ("sin citas", "no citations"),
    ("sin figuras", "no figures"),
    ("sin acrónimos no definidos", "no undefined acronyms"),
    ("sin siglas no definidas", "no undefined acronyms"),
    ("sin ecuaciones", "no equations"),
    ("no definidos", "undefined"),
    ("siglas", "acronyms"),
    ("acrónimos", "acronyms"),
    ("términos", "terms"),
    ("words clave", "keywords"),
    ("términos en inglés", "English terms"),
    ("pregunta de investigación", "research question"),
    ("Pregunta de investigación", "Research question"),
    ("aportación", "contribution"),
    ("aportaciones", "contributions"),
    ("hallazgos principales", "main findings"),
    ("hallazgos", "findings"),
    ("Hallazgos", "Findings"),
    ("conclusión principal", "main conclusion"),
    ("conclusiones", "conclusions"),
    ("Conclusiones", "Conclusions"),
    ("metodología", "methodology"),
    ("Metodología", "Methodology"),
    ("método", "method"),
    ("métodos", "methods"),
    ("antecedentes", "background"),
    ("Antecedentes", "Background"),
    ("objetivo principal", "main objective"),
    ("objetivo", "objective"),
    ("Objetivo", "Objective"),
    ("objetivos específicos", "specific objectives"),
    ("objetivos", "objectives"),
    ("Objetivos", "Objectives"),
    ("hipótesis", "hypotheses"),
    ("Hipótesis", "Hypotheses"),
    ("preguntas", "questions"),
    ("investigación", "research"),
    ("Investigación", "Research"),
    ("resultados", "results"),
    ("Resultados", "Results"),
    ("principal", "main"),
    ("principales", "main"),
    ("aportación al campo", "contribution to the field"),
    ("coordinación", "coordination office"),
    ("Comité Académico", "Academic Committee"),
    ("comité tutorial", "tutorial committee"),
    ("Comité Tutorial", "Tutorial Committee"),
    ("sinodales", "committee examiners"),
    ("becas", "scholarships"),
    ("beca", "scholarship"),
    ("financiamiento", "funding"),
    ("proyectos", "projects"),
    ("proyecto", "project"),
    ("número de beca", "scholarship number"),
    ("número de proyecto", "project number"),
    ("convenio", "agreement"),
    ("menciona", "mention"),
    ("mencionalo", "mention it"),
    ("también", "also"),
    ("También", "Also"),
    ("fondos", "funds"),
    ("apoyo", "support"),
    ("personalmente", "personally"),
    ("durante el proceso", "during the process"),
    ("longitud típica", "typical length"),
    ("Longitud típica", "Typical length"),
    ("media a una página", "half a page to one page"),
    ("páginas", "pages"),
    ("página", "page"),
    ("capítulos", "chapters"),
    ("capítulo", "chapter"),
    ("Capítulo", "Chapter"),
    ("apartados", "sections"),
    ("apartado", "section"),
    ("preliminares", "front matter"),
    ("excepto", "except"),
    ("referencias", "references"),
    ("Referencias", "References"),
    ("apéndices", "appendices"),
    ("Apéndices", "Appendices"),
    ("anexos", "appendices"),
    ("Anexos", "Appendices"),
    ("números de página", "page numbers"),
    ("número de página", "page number"),
    ("paginación", "pagination"),
    ("imprimir", "printing"),
    ("contiene", "contains"),
    ("contienen", "contain"),
    ("contiene figuras", "contains figures"),
    ("contiene tablas", "contains tables"),
    ("gráficas", "graphs"),
    ("imágenes", "images"),
    ("figuras", "figures"),
    ("Figuras", "Figures"),
    ("tablas", "tables"),
    ("Tablas", "Tables"),
    ("cuadros", "tables"),
    ("Cuadros", "Tables"),
    ("numera", "number"),
    ("referéncialas", "refer to them"),
    ("referenciadas", "referenced"),
    ("referenciada", "referenced"),
    ("en el texto", "in the text"),
    ("antes de que aparezcan", "before they appear"),
    ("primera vez que aparece", "first time it appears"),
    ("cuerpo del texto", "body text"),
    ("cuerpo principal", "main body"),
    ("La introducción", "The introduction"),
    ("introducción", "introduction"),
    ("Introducción", "Introduction"),
    ("enmarca", "frames"),
    ("establece", "establishes"),
    ("convierte", "turns"),
    ("convence al lector", "convinces the reader"),
    ("importancia", "importance"),
    ("relevancia", "relevance"),
    ("teórica", "theoretical"),
    ("práctica", "practical"),
    ("social", "social"),
    ("económica", "economic"),
    ("clínica", "clinical"),
    ("tecnológica", "technological"),
    ("alcance", "scope"),
    ("delimitaciones", "boundaries"),
    ("delimitación", "boundary"),
    ("párrafo breve", "short paragraph"),
    ("un párrafo", "one paragraph"),
    ("por capítulo", "per chapter"),
    ("Extensión típica", "Typical length"),
    ("extension típica", "typical length"),
    ("El marco teórico", "The theoretical framework"),
    ("marco teórico", "theoretical framework"),
    ("base conceptual", "conceptual foundation"),
    ("conceptos clave", "key concepts"),
    ("literatura", "literature"),
    ("Literatura", "Literature"),
    ("estado del arte", "state of the art"),
    ("Estado del arte", "State of the art"),
    ("enfoques", "approaches"),
    ("debates", "debates"),
    ("vacío", "gap"),
    ("contradicción", "contradiction"),
    ("justifica", "justifies"),
    ("justificar", "justify"),
    ("posicionamiento", "positioning"),
    ("perspectiva", "perspective"),
    ("citas", "citations"),
    ("Citas", "Citations"),
    ("cita", "citation"),
    ("Autor", "Author"),
    ("año", "year"),
    ("forma narrativa", "narrative form"),
    ("citas textuales", "direct quotations"),
    ("número de página", "page number"),
    ("temas", "themes"),
    ("corrientes", "schools"),
    ("lista de autores", "list of authors"),
    ("La metodología", "The methodology"),
    ("debe permitir", "must allow"),
    ("replicabilidad", "replicability"),
    ("enfoque", "approach"),
    ("paradigma", "paradigm"),
    ("cuantitativo", "quantitative"),
    ("cualitativo", "qualitative"),
    ("mixto", "mixed"),
    ("diseño", "design"),
    ("Diseño", "Design"),
    ("experimental", "experimental"),
    ("correlacional", "correlational"),
    ("descriptivo", "descriptive"),
    ("fenomenológico", "phenomenological"),
    ("hermenéutico", "hermeneutic"),
    ("unidades de análisis", "units of analysis"),
    ("población", "population"),
    ("muestra", "sample"),
    ("corpus", "corpus"),
    ("criterios de selección", "selection criteria"),
    ("tamaño", "size"),
    ("procedimiento de muestreo", "sampling procedure"),
    ("instrumentos", "instruments"),
    ("Instrumentos", "Instruments"),
    ("técnicas de recolección", "collection techniques"),
    ("encuestas", "surveys"),
    ("entrevistas", "interviews"),
    ("observación", "observation"),
    ("análisis documental", "document analysis"),
    ("análisis de contenido", "content analysis"),
    ("validación de instrumentos", "instrument validation"),
    ("análisis de datos", "data analysis"),
    ("análisis estadístico", "statistical analysis"),
    ("consideraciones éticas", "ethical considerations"),
    ("Consideraciones éticas", "Ethical considerations"),
    ("seres humanos", "human participants"),
    ("consentimiento informado", "informed consent"),
    ("limitaciones metodológicas", "methodological limitations"),
    ("evaluación", "evaluation"),
    ("Evaluación", "Evaluation"),
    ("criterios de evaluación", "evaluation criteria"),
    ("hallazgos de manera objetiva", "findings objectively"),
    ("manera objetiva", "objective manner"),
    ("sin interpretación", "without interpretation"),
    ("sin conclusiones", "without conclusions"),
    ("Organiza", "Organize"),
    ("organiza", "organize"),
    ("conforme a", "according to"),
    ("datos cuantitativos", "quantitative data"),
    ("datos cualitativos", "qualitative data"),
    ("estadísticas descriptivas", "descriptive statistics"),
    ("medias", "means"),
    ("desviaciones estándar", "standard deviations"),
    ("porcentajes", "percentages"),
    ("pruebas inferenciales", "inferential tests"),
    ("tamaños del efecto", "effect sizes"),
    ("intervalos de confianza", "confidence intervals"),
    ("notas al pie", "footnotes"),
    ("categorías", "categories"),
    ("temas emergentes", "emerging themes"),
    ("representativas", "representative"),
    ("confidencialidad", "confidentiality"),
    ("participantes", "participants"),
    ("mencionada", "mentioned"),
    ("mencionado", "mentioned"),
    ("La discusión", "The discussion"),
    ("discusión", "discussion"),
    ("Discusión", "Discussion"),
    ("interpreta", "interprets"),
    ("interpreta los resultados", "interprets the results"),
    ("conecta", "connects"),
    ("revisada", "reviewed"),
    ("oración", "sentence"),
    ("retoma", "returns to"),
    ("respóndela", "answer it"),
    ("directamente", "directly"),
    ("base en", "based on"),
    ("Compara", "Compare"),
    ("compara", "compare"),
    ("estudios previos", "previous studies"),
    ("coinciden", "agree"),
    ("contradicen", "contradict"),
    ("matizan", "qualify"),
    ("hallazgos", "findings"),
    ("resultados inesperados", "unexpected results"),
    ("inesperados", "unexpected"),
    ("implicaciones", "implications"),
    ("limitaciones del estudio", "study limitations"),
    ("investigación futura", "future research"),
    ("fusiona", "merged"),
    ("capítulo independiente", "standalone chapter"),
    ("lo requieres", "you need it"),
    ("Las conclusiones", "The conclusions"),
    ("responden", "answer"),
    ("responde", "answer"),
    ("Responde", "Answer"),
    ("verifica", "verify"),
    ("cada", "each"),
    ("Resume", "Summarize"),
    ("resume", "summarize"),
    ("originales", "original"),
    ("campo de conocimiento", "field of knowledge"),
    ("aplicaciones posibles", "possible applications"),
    ("sé honesto", "be honest"),
    ("líneas de investigación futura", "future research lines"),
    ("No repitas", "Do not repeat"),
    ("Puntos clave", "Key points"),
    ("Cursiva", "Italics"),
    ("títulos de libros", "book titles"),
    ("revistas", "journals"),
    ("artículos", "articles"),
    ("capítulos", "chapters"),
    ("fecha de acceso", "access date"),
    ("Apellido", "Last name"),
    ("Título", "Title"),
    ("Repositorio", "Repository"),
    ("base de datos", "database"),
    ("solo las", "only the"),
    ("que citas", "you cite"),
    ("Materiales complementarios", "Supplementary materials"),
    ("Material complementario", "Supplementary material"),
    ("demasiado extensos", "too extensive"),
    ("interrumpirían", "would interrupt"),
    ("flujo narrativo", "narrative flow"),
    ("cuestionarios", "questionnaires"),
    ("escalas", "scales"),
    ("guías de entrevista", "interview guides"),
    ("datos brutos", "raw data"),
    ("tablas estadísticas adicionales", "additional statistical tables"),
    ("transcripciones", "transcripts"),
    ("grupos de enfoque", "focus groups"),
    ("cartas de aprobación ética", "ethics approval letters"),
    ("formatos de consentimiento informado", "informed consent forms"),
    ("protocolos", "protocols"),
    ("intervención", "intervention"),
    ("Etiqueta", "Label"),
    ("Referencia desde el texto", "Reference from the text"),
    ("véase", "see"),
    ("propuesta", "proposal"),
    ("Propuesta", "Proposal"),
    ("desarrollo", "development"),
    ("Desarrollo", "Development"),
    ("trabajo", "work"),
    ("Trabajo", "Work"),
    ("tesina", "short thesis"),
    ("Tesina", "Short thesis"),
    ("tesis", "thesis"),
    ("Tesis", "Thesis"),
    ("disertación", "dissertation"),
    ("Disertación", "Dissertation"),
    ("documento", "document"),
    ("Documento", "Document"),
    ("académico", "academic"),
    ("académica", "academic"),
    ("académicos", "academic"),
    ("académicas", "academic"),
    ("profesional", "professional"),
    ("clínico", "clinical"),
    ("estrategia", "strategy"),
    ("utilidad", "usefulness"),
    ("Longitud sugerida", "Suggested length"),
    ("procedimiento", "procedure"),
    ("Procedimiento", "Procedure"),
    ("herramientas", "tools"),
    ("empleados", "used"),
    ("empleadas", "used"),
    ("empleado", "used"),
    ("empleada", "used"),
    ("productos", "outputs"),
    ("métricas", "metrics"),
    ("observados", "observed"),
    ("práctica", "practical"),
    ("protocolos", "protocols"),
    ("formatos", "forms"),
    ("extensas", "extended"),
    ("documentación técnica", "technical documentation"),
    ("evidencia", "evidence"),
    ("complementaria", "supplementary"),
    ("agenda", "agenda"),
    ("posdoctoral", "postdoctoral"),
    ("contribuciones", "contributions"),
    ("proyección futura", "future projection"),
    ("campo de investigación", "research field"),
    ("estancia", "stay"),
    ("datasets", "datasets"),
    ("avances verificables", "verifiable progress"),
    ("novedad", "novelty"),
    ("relación", "relationship"),
    ("la primera impresión", "the first impression"),
    ("universidad", "university"),
    ("abreviaturas", "abbreviations"),
    ("tipo de document", "document type"),
    ("grado al que aspira", "degree sought"),
    ("ciudad", "city"),
    ("presentación", "submission"),
    ("coordinación", "coordination office"),
    ("protesta de decir verdad", "under oath"),
    ("ha sido elaborado", "has been prepared"),
    ("suscrito", "undersigned"),
    ("notariada", "notarized"),
    ("primer elemento", "first element"),
    ("leerán otros", "other"),
    ("investigadores", "researchers"),
    ("oraciones", "sentences"),
    ("datos empleados", "data used"),
    ("enfoque utilizado", "approach used"),
    ("implicaciones", "implications"),
    ("agrega", "add"),
    ("Agrega", "Add"),
    ("separadas por punto y coma", "separated by semicolons"),
    ("visibilidad internacional", "international visibility"),
    ("bases de datos internacionales", "international databases"),
    ("Sección", "Section"),
    ("sección", "section"),
    ("quienes contribuyeron", "those who contributed"),
    ("colegas", "colleagues"),
    ("bibliotecarios", "librarians"),
    ("externo", "external"),
    ("recurso", "funding"),
    ("principal", "main"),
    ("sustenta", "supports"),
    ("Cuáles", "Which"),
    ("Dónde", "Where"),
    ("teórico", "theoretical"),
    ("No repetir", "Do not repeat"),
    ("No incluir", "Do not include"),
    ("incluir", "include"),
    ("Incluir", "Include"),
    ("Usar", "Use"),
    ("usar", "use"),
    ("Reportar", "Report"),
    ("reportar", "report"),
    ("Discutir", "Discuss"),
    ("discutir", "discuss"),
    ("Presentación objetiva", "Objective presentation"),
    ("breves", "brief"),
    ("directamente derivadas", "directly derived"),
    ("obtenidos", "obtained"),
    ("obtenidas", "obtained"),
    ("propuestas", "proposals"),
    ("trabajo futuro", "future work"),
    ("líneas de desarrollo futuro", "future development lines"),
    ("cuando aplique", "where applicable"),
    ("si aplica", "if applicable"),
    ("si la investigación", "if the research"),
    ("si tu institución", "if your institution"),
    ("si tu programa", "if your program"),
    ("si tu diseño", "if your design"),
    ("cuando disponible", "when available"),
    ("cuando esté disponible", "when available"),
    ("Obligatorio cuando", "Required when"),
    ("Número máximo recomendado", "Maximum recommended number"),
    ("sin límite estricto", "no strict limit"),
    ("típicamente", "typically"),
    ("Materiales", "Materials"),
    ("dictamen", "approval"),
    ("autorización", "authorization"),
    ("institución", "institution"),
    ("realizó", "was conducted"),
    ("estudio", "study"),
    ("versión final aprobada", "final approved version"),
    ("Incluye institución", "Include institution"),
    ("programa de especialidad", "specialty program"),
    ("título del trabajo", "work title"),
    ("formato oficial", "official format"),
    ("úsalo como fuente de verdad", "use it as the source of truth"),
    ("Presenta el problema", "Present the problem"),
    ("contexto institucional", "institutional context"),
    ("relevancia del trabajo", "relevance of the work"),
    ("Describe el diseño del trabajo", "Describe the work design"),
    ("consideraciones éticas", "ethical considerations"),
    ("Expón los hallazgos", "Present the findings"),
    ("Interpreta los resultados", "Interpret the results"),
    ("reconoce limitaciones", "acknowledge limitations"),
    ("señala implicaciones prácticas", "state practical implications"),
    ("Revisa la paginación final antes de entregar", "Review final pagination before submission"),
]

PHRASE_ES = [
    ("Thesis/Dissertation", "Tesis/Disertación"),
    ("Doctoral Thesis", "Tesis doctoral"),
    ("Thesis", "Tesis"),
    ("Short Thesis", "Tesina"),
    ("Dissertation", "Disertación"),
    ("Generic Thesis", "Tesis genérica"),
    ("Generic Short Thesis", "Tesina genérica"),
    ("Generic Specialty Project", "Trabajo de especialidad genérico"),
    ("University of Buenos Aires", "Universidad de Buenos Aires"),
    ("University of Chile", "Universidad de Chile"),
    ("University of Guadalajara", "Universidad de Guadalajara"),
    ("National Autonomous University of Mexico", "Universidad Nacional Autónoma de México"),
    ("National Polytechnic Institute", "Instituto Politécnico Nacional"),
    ("State University of Campinas", "Universidad Estatal de Campinas"),
    ("University of Sao Paulo", "Universidad de São Paulo"),
    ("complete guidance in English", "guía completa en español"),
    ("guidance in English", "guía en español"),
    ("APA 7th edition", "APA 7ª edición"),
    ("IMRaD structure", "estructura IMRyD"),
]

SPANISH_RE = (
    r"\b(portada|resumen|introducción|conclusiones|metodología|agradecimientos|índice|"
    r"declaración|autoría|originalidad|incluye|presenta|reconoce|revisa|activa|"
    r"interpreta|expón|tesis|palabras|fuentes|objetivos|resultados|capítulo|"
    r"figuras|tablas|pregunta|hallazgos|si|con|para|del|las|los)\b"
)

ENGLISH_RE = (
    r"\b(abstract|acknowledgements|appendices|background|bibliography|chapter|conclusion|"
    r"discussion|introduction|methodology|results|references|table of contents|title page|"
    r"generated automatically|required|include|present|thesis|figures|tables|words)\b"
)


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def add_if_string(target: dict[str, str], key: str, value: Any) -> None:
    if isinstance(value, str) and value.strip():
        target[key] = value


def translate_string_en(value: str, field: str) -> str:
    if field in {"title"} and value in TITLE_EN:
        return TITLE_EN[value]

    translated = value
    for source, target in PHRASE_EN:
        translated = translated.replace(source, target)

    # Small grammar cleanup after phrase replacement.
    translated = translated.replace("English académico", "academic English")
    translated = translated.replace("English, guidance", "English, guidance")
    translated = translated.replace("English, 200–350 words", "English abstract, 200–350 words")
    translated = translated.replace("English English", "English")
    translated = translated.replace("  ", " ")
    return translated


def translate_string_es(value: str, field: str) -> str:
    if field == "title" and value in TITLE_ES:
        return TITLE_ES[value]

    translated = value
    for source, target in PHRASE_ES:
        translated = translated.replace(source, target)
    return translated


def translate_tree_es(value: Any, key: str = "") -> Any:
    if isinstance(value, dict):
        translated: dict[str, Any] = {}
        for child_key, child_value in value.items():
            translated[child_key] = translate_tree_es(child_value, child_key)
        if key == "":
            translated["locale"] = "es"
        return translated
    if isinstance(value, list):
        return [translate_tree_es(item, key) for item in value]
    if isinstance(value, str):
        if key == "locale":
            return "es"
        if key in {"name", "description", "institution", "department", "faculty", "program_name", "title", "guidance"}:
            return translate_string_es(value, key)
    return value


def translate_tree_en(value: Any, key: str = "") -> Any:
    if isinstance(value, dict):
        translated: dict[str, Any] = {}
        for child_key, child_value in value.items():
            translated[child_key] = translate_tree_en(child_value, child_key)
        if key == "":
            translated["locale"] = "en"
        return translated
    if isinstance(value, list):
        return [translate_tree_en(item, key) for item in value]
    if isinstance(value, str):
        if key == "locale":
            return "en"
        if key in {"name", "description", "institution", "department", "faculty", "program_name", "title", "guidance"}:
            return translate_string_en(value, key)
    return value


def generic_guidance(section_id: str, title: str, locale: str) -> str:
    key = f"{section_id} {title}".lower()
    if locale == "en":
        if any(token in key for token in ["portada", "title", "cover", "capa", "folha"]):
            return "Prepare the title page according to your institution's official template. Include the full title, author, program, advisors, institution, place, and year."
        if any(token in key for token in ["abstract", "resumen", "resumo", "summary"]):
            return "Write a self-contained abstract with the problem, objective, method, main results, and contribution. Keep the length required by your program and add keywords if requested."
        if any(token in key for token in ["acknow", "agrade"]):
            return "Acknowledge advisors, committee members, collaborators, institutions, and funding sources. Include grant or scholarship numbers when applicable."
        if any(token in key for token in ["contents", "indice", "índice", "sumario"]):
            return "Generate this section automatically and verify final page numbers before submission."
        if any(token in key for token in ["figures", "figuras"]):
            return "Enable this section when the document contains several numbered figures. Verify that every listed figure has a caption and page number."
        if any(token in key for token in ["tables", "tablas", "cuadros"]):
            return "Enable this section when the document contains several numbered tables. Verify that every listed table has a caption and page number."
        if any(token in key for token in ["introduction", "introduc"]):
            return "Present the research context, problem statement, rationale, research questions, objectives, scope, and chapter structure."
        if any(token in key for token in ["framework", "literature", "marco", "background"]):
            return "Review the relevant literature and theoretical foundations. Organize the discussion by themes or debates and identify the gap your work addresses."
        if any(token in key for token in ["method", "metod", "material"]):
            return "Describe the research design, data or sample, instruments, procedure, analysis strategy, tools, and ethical considerations with enough detail for replication."
        if any(token in key for token in ["result", "resultado"]):
            return "Present findings objectively and organize them by research question, objective, or theme. Use tables and figures where they improve clarity."
        if any(token in key for token in ["discussion", "discusi"]):
            return "Interpret the results in relation to the literature, explain their implications, and discuss limitations."
        if any(token in key for token in ["conclusion", "conclus"]):
            return "Answer the research questions, summarize the contribution, state limitations, and suggest future work."
        if any(token in key for token in ["reference", "bibliograf", "referencia", "fuentes"]):
            return "List only cited sources and follow the bibliography style required by the profile."
        if any(token in key for token in ["append", "apend", "anexo"]):
            return "Include supplementary material such as instruments, extended tables, protocols, approvals, or supporting technical documentation."
        return "Complete this section according to the profile requirements and your institution's current submission guidelines."

    if any(token in key for token in ["title", "cover", "portada", "capa", "folha"]):
        return "Prepara la portada conforme a la plantilla oficial de tu institución. Incluye título completo, autor, programa, asesores, institución, lugar y año."
    if any(token in key for token in ["abstract", "resumen", "resumo", "summary"]):
        return "Redacta un resumen autocontenido con problema, objetivo, método, resultados principales y aportación. Respeta la extensión requerida y agrega palabras clave si se solicitan."
    if any(token in key for token in ["acknow", "agrade"]):
        return "Reconoce a asesores, comité, colaboradores, instituciones y fuentes de financiamiento. Incluye números de beca o proyecto cuando aplique."
    if any(token in key for token in ["contents", "indice", "índice", "sumario"]):
        return "Genera esta sección automáticamente y verifica la paginación final antes de entregar."
    if any(token in key for token in ["figures", "figuras"]):
        return "Activa esta sección cuando el documento contenga varias figuras numeradas. Verifica que cada figura tenga pie y número de página."
    if any(token in key for token in ["tables", "tablas", "cuadros"]):
        return "Activa esta sección cuando el documento contenga varias tablas numeradas. Verifica que cada tabla tenga título y número de página."
    if any(token in key for token in ["introduction", "introduc"]):
        return "Presenta el contexto, planteamiento del problema, justificación, preguntas de investigación, objetivos, alcance y estructura del documento."
    if any(token in key for token in ["framework", "literature", "marco", "background"]):
        return "Revisa la literatura relevante y los fundamentos teóricos. Organiza por temas o debates e identifica el vacío que aborda tu trabajo."
    if any(token in key for token in ["method", "metod", "material"]):
        return "Detalla el diseño de investigación, datos o muestra, instrumentos, procedimiento, estrategia de análisis, herramientas y consideraciones éticas con detalle suficiente para replicar el estudio."
    if any(token in key for token in ["result", "resultado"]):
        return "Presenta los hallazgos de forma objetiva y organízalos por pregunta, objetivo o tema. Usa tablas y figuras cuando mejoren la claridad."
    if any(token in key for token in ["discussion", "discusi"]):
        return "Interpreta los resultados en relación con la literatura, explica sus implicaciones y discute las limitaciones."
    if any(token in key for token in ["conclusion", "conclus"]):
        return "Responde las preguntas de investigación, resume la aportación, señala limitaciones y propone trabajo futuro."
    if any(token in key for token in ["reference", "bibliograf", "referencia", "fuentes"]):
        return "Incluye solo las fuentes citadas y sigue el estilo bibliográfico requerido por el perfil."
    if any(token in key for token in ["append", "apend", "anexo"]):
        return "Incluye material suplementario como instrumentos, tablas extensas, protocolos, dictámenes o documentación técnica de apoyo."
    return "Completa esta sección conforme a los requisitos del perfil y los lineamientos vigentes de tu institución."


def sanitize_locale(messages: dict[str, Any], locale: str) -> dict[str, Any]:
    bad_re = re.compile(SPANISH_RE if locale == "en" else ENGLISH_RE, re.IGNORECASE)
    for style_id, style in messages.get("citation_styles", {}).items():
        description = style.get("description")
        if isinstance(description, str) and bad_re.search(description):
            style_name = style.get("name", style_id)
            if locale == "en":
                style["description"] = f"Bibliography style profile for {style_name}."
            else:
                style["description"] = f"Perfil de estilo bibliográfico para {style_name}."
    for profile in messages.get("profiles", {}).values():
        description = profile.get("description")
        if isinstance(description, str) and bad_re.search(description):
            name = profile.get("name", "profile")
            if locale == "en":
                profile["description"] = f"Academic profile for {name}. Follow the profile metadata, required sections, and bibliography style."
            else:
                profile["description"] = f"Perfil académico para {name}. Sigue los metadatos, secciones requeridas y estilo bibliográfico del perfil."
        for section_id, section in (profile.get("sections") or {}).items():
            title = section.get("title", section_id)
            guidance = section.get("guidance")
            if isinstance(guidance, str) and bad_re.search(guidance):
                section["guidance"] = generic_guidance(section_id, title, locale)
    return messages


def profile_dirs() -> list[Path]:
    dirs: list[Path] = []
    for root, dirnames, filenames in os.walk(ROOT):
        dirnames.sort()
        norm = Path(root).as_posix().lstrip("./")
        if norm.startswith((".git", "dist", "profile_samples", "i18n")):
            dirnames.clear()
            continue
        if "manifest.yaml" in filenames and "profile.yaml" in filenames:
            parts = [p for p in norm.split("/") if p]
            if len(parts) == 4:
                dirs.append(Path(root))
    return sorted(dirs)


def build_messages() -> dict[str, Any]:
    messages: dict[str, Any] = {
        "schema_version": "1.0.0",
        "locale": "es",
        "profiles": {},
        "institutions": {},
        "citation_styles": {},
    }

    for inst_path in sorted(ROOT.glob("*/*/*/_institution.yaml")):
        rel = inst_path.parent.as_posix()
        data = read_yaml(inst_path)
        entry: dict[str, str] = {}
        for field in ["name", "short_name", "description"]:
            add_if_string(entry, field, data.get(field))
        if entry:
            messages["institutions"][rel] = entry

    for style_path in sorted((ROOT / "citation_styles").glob("*.yaml")):
        data = read_yaml(style_path)
        style_id = data.get("id") or style_path.stem
        entry: dict[str, str] = {}
        for field in ["name", "short_name", "description"]:
            add_if_string(entry, field, data.get(field))
        if entry:
            messages["citation_styles"][style_id] = entry

    for directory in profile_dirs():
        manifest = read_yaml(directory / "manifest.yaml")
        profile = read_yaml(directory / "profile.yaml")
        profile_id = manifest.get("id") or profile.get("id") or directory.name
        entry: dict[str, Any] = {"sections": {}}

        for field in ["name", "description", "institution", "department", "faculty", "program_name"]:
            add_if_string(entry, field, manifest.get(field) or profile.get(field))

        for section in profile.get("sections") or []:
            if not isinstance(section, dict):
                continue
            section_id = section.get("id") or section.get("element_id")
            if not isinstance(section_id, str) or not section_id:
                continue
            section_entry: dict[str, str] = {}
            for field in ["title", "label", "guidance"]:
                add_if_string(section_entry, field, section.get(field))
            if section_entry:
                entry["sections"][section_id] = section_entry

        if not entry["sections"]:
            entry.pop("sections")
        if len(entry) > 0:
            messages["profiles"][profile_id] = entry

    return messages


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    source_messages = build_messages()
    es_messages = sanitize_locale(translate_tree_es(source_messages), "es")
    en_messages = sanitize_locale(translate_tree_en(source_messages), "en")

    with ES_OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(es_messages, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with EN_OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(en_messages, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(
        "i18n: "
        f"{len(es_messages['profiles'])} perfiles/profiles, "
        f"{len(es_messages['institutions'])} instituciones/institutions, "
        f"{len(es_messages['citation_styles'])} estilos/styles"
    )


if __name__ == "__main__":
    main()
