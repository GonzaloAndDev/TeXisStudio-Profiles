#!/usr/bin/env python3
"""
Script to update all 21 profiles:
1. Rewrite YAML files with English text in title/guidance fields
2. Update en.json with detailed English translations

Run from repo root:
  python3 scripts/i18n_translate.py
"""

import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────────────────────────
# TRANSLATIONS DATA
# Each profile maps section_id -> {"title": ..., "guidance": ...}
# We only set keys present in the YAML; if guidance is None we skip it.
# ─────────────────────────────────────────────────────────────────────────────

TRANSLATIONS = {

# ══════════════════════════════════════════════════════════════════════════════
# ar_uba_apa7
# ══════════════════════════════════════════════════════════════════════════════
"ar_uba_apa7": {
    "verified_by": "TeXisStudio Community — reviewed against UBA Rectorate guidelines and Doctoral Commission regulations",
    "sections": {
        "portada": {
            "title": "Title Page",
            "guidance": (
                "The official UBA title page must include:\n"
                "• Logo and name of the Universidad de Buenos Aires.\n"
                "• Name of the Faculty (FCE, FFyL, FMED, etc.).\n"
                "• Name of the doctoral program.\n"
                "• Full title of the thesis.\n"
                "• \"Thesis submitted to obtain the degree of Doctor/a in [field].\"\n"
                "• Full name of the author.\n"
                "• Thesis supervisor and co-supervisor (if applicable).\n"
                "• Buenos Aires, [Month] [Year].\n"
                "Each faculty has its own specific title page format —\n"
                "download it from the Secretaría de Posgrado of your academic unit.\n"
            ),
        },
        "declaracion": {
            "title": "Sworn Authorship Statement",
            "guidance": (
                "UBA requires a Sworn Statement of Authorship and Originality.\n"
                "The Rectorate or Faculty may require a specific signed form.\n"
                "Standard text: \"The undersigned declares under oath that this thesis\n"
                "is their own work, that it has not previously been submitted to obtain\n"
                "any degree at any institution, and that all sources consulted have been\n"
                "correctly cited.\"\n"
            ),
        },
        "resumen": {
            "title": "Abstract",
            "guidance": (
                "Abstract in Spanish, 200–350 words.\n"
                "Problem, objectives, methodology, results and conclusions.\n"
                "Keywords (4–6).\n"
            ),
        },
        "abstract_ingles": {
            "title": "Abstract",
            "guidance": (
                "Abstract in English. Recommended for international visibility.\n"
                "Maximum 350 words. Keywords (4–6).\n"
            ),
        },
        "agradecimientos": {
            "title": "Acknowledgements",
            "guidance": (
                "Acknowledge the supervisor, evaluation committee, CONICET and ANPCyT\n"
                "(PICT) grants, UBACyT (UBA Institutional Recognition Programs),\n"
                "MINCYT and other funding sources. Include the project or scholarship number.\n"
            ),
        },
        "indice": {
            "title": "Table of Contents",
            "guidance": "Generated automatically. Exact page numbers.",
        },
        "indice_figuras": {
            "title": "List of Figures",
            "guidance": "Enable if you have 5 or more figures.",
        },
        "indice_tablas": {
            "title": "List of Tables",
            "guidance": "Enable if you have 5 or more tables.",
        },
        "introduccion": {
            "title": "Introduction",
            "guidance": (
                "Contextualization, problem statement, rationale,\n"
                "research questions, objectives and hypotheses. Structure.\n"
                "APA 7: (Author, year) in the text.\n"
            ),
        },
        "marco_teorico": {
            "title": "Theoretical Framework",
            "guidance": (
                "Critical review and conceptual foundations.\n"
                "Organize by theoretical approaches. Identify the gap the thesis addresses.\n"
            ),
        },
        "metodologia": {
            "title": "Methodology",
            "guidance": (
                "Research design, sample, instruments, procedure, analysis.\n"
                "Institutional Ethics Committee approval if human subjects are involved.\n"
            ),
        },
        "resultados": {
            "title": "Results",
            "guidance": "Objective findings. APA 7 tables and figures. No interpretation.",
        },
        "discusion": {
            "title": "Discussion",
            "guidance": "Interpretation, comparison with literature, implications and limitations.",
        },
        "conclusiones": {
            "title": "Conclusions",
            "guidance": "Address objectives, summarize contributions, limitations and future work.",
        },
        "referencias": {
            "title": "References",
            "guidance": "APA 7th edition, alphabetical list, hanging indent.",
        },
        "apendices": {
            "title": "Appendices",
            "guidance": "Instruments, additional data, ethics approval. Appendix A, B…",
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# br_unicamp_abnt  (Brazilian Portuguese — titles stay in Portuguese per ABNT convention,
#                   but en.json provides English display names)
# ══════════════════════════════════════════════════════════════════════════════
"br_unicamp_abnt": {
    "sections": {
        "capa": {
            "title": "Cover Page",
            "guidance": (
                "The UNICAMP cover page (Capa) must include: institution name and logo,\n"
                "faculty or institute, full thesis title, author name, city and year.\n"
                "Follow the ABNT NBR 14724:2011 standard and UNICAMP’s official template.\n"
            ),
        },
        "folha_rosto": {
            "title": "Title Page",
            "guidance": (
                "The Title Page (Folha de Rosto) includes: author name, full thesis title,\n"
                "a note indicating the nature and objective of the work and the name of the\n"
                "supervising professor, and the city and year of submission. ABNT NBR 14724.\n"
            ),
        },
        "resumo": {
            "title": "Abstract (Portuguese)",
            "guidance": (
                "Abstract in Portuguese (Resumo), up to 500 words (ABNT NBR 6028).\n"
                "Self-contained: no citations, no undefined abbreviations.\n"
                "Include 3–5 keywords (Palavras-chave) at the end.\n"
            ),
        },
        "abstract": {
            "title": "Abstract (English)",
            "guidance": (
                "English translation of the Resumo. Required by UNICAMP for dissertations\n"
                "and doctoral theses. Same structure and length as the Resumo.\n"
                "Include 3–5 keywords at the end.\n"
            ),
        },
        "sumario": {
            "title": "Table of Contents",
            "guidance": (
                "Generated automatically. Must follow ABNT NBR 6027 format.\n"
                "Lists all pre-textual elements (except cover), chapters, references and annexes\n"
                "with exact page numbers.\n"
            ),
        },
        "introducao": {
            "title": "Introduction",
            "guidance": (
                "Presents the research problem, justification, research questions,\n"
                "objectives and structure of the dissertation. ABNT citations: (AUTHOR, year).\n"
            ),
        },
        "capitulos": {
            "title": "Development Chapters",
            "guidance": (
                "Core content of the dissertation. Divide into thematic chapters:\n"
                "theoretical framework, methodology, results and discussion.\n"
                "Each chapter begins on a new page. ABNT citation style throughout.\n"
            ),
        },
        "conclusao": {
            "title": "Conclusion",
            "guidance": (
                "Answers the research questions, summarizes contributions, states limitations\n"
                "and proposes future work. No new information that was not discussed earlier.\n"
            ),
        },
        "referencias": {
            "title": "References",
            "guidance": (
                "ABNT NBR 6023:2018 format, alphabetical order.\n"
                "All sources cited in the text must appear here.\n"
            ),
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# br_usp_abnt
# ══════════════════════════════════════════════════════════════════════════════
"br_usp_abnt": {
    "sections": {
        "capa": {
            "title": "Cover Page",
            "guidance": (
                "The USP cover page (Capa) must include: institution name and logo,\n"
                "faculty or institute, full thesis title, author name, city and year.\n"
                "Follow ABNT NBR 14724:2011 and the USP/FFLCH official template.\n"
            ),
        },
        "folha_rosto": {
            "title": "Title Page",
            "guidance": (
                "The Title Page (Folha de Rosto) includes: author name, full thesis title,\n"
                "a note stating the nature and objective of the work and the name of the\n"
                "supervising professor, and the city and year. ABNT NBR 14724.\n"
            ),
        },
        "resumo": {
            "title": "Abstract (Portuguese)",
            "guidance": (
                "Abstract in Portuguese (Resumo), up to 500 words (ABNT NBR 6028).\n"
                "Self-contained: no citations, no undefined abbreviations.\n"
                "Include 3–5 keywords (Palavras-chave) at the end.\n"
            ),
        },
        "abstract": {
            "title": "Abstract (English)",
            "guidance": (
                "English translation of the Resumo. Required by USP for dissertations\n"
                "and doctoral theses. Same structure and length as the Resumo.\n"
                "Include 3–5 keywords at the end.\n"
            ),
        },
        "sumario": {
            "title": "Table of Contents",
            "guidance": (
                "Generated automatically. Must follow ABNT NBR 6027 format.\n"
                "Lists all pre-textual elements (except cover), chapters, references and\n"
                "annexes with exact page numbers.\n"
            ),
        },
        "introducao": {
            "title": "Introduction",
            "guidance": (
                "Presents the research problem, justification, research questions,\n"
                "objectives and structure of the dissertation. ABNT citations: (AUTHOR, year).\n"
            ),
        },
        "capitulos": {
            "title": "Development Chapters",
            "guidance": (
                "Core content of the dissertation. Divide into thematic chapters:\n"
                "theoretical framework, methodology, results and discussion.\n"
                "Each chapter begins on a new page. ABNT citation style throughout.\n"
            ),
        },
        "conclusao": {
            "title": "Conclusion",
            "guidance": (
                "Answers the research questions, summarizes contributions, states limitations\n"
                "and proposes future work. No new information that was not discussed earlier.\n"
            ),
        },
        "referencias": {
            "title": "References",
            "guidance": (
                "ABNT NBR 6023:2018 format, alphabetical order.\n"
                "All sources cited in the text must appear here.\n"
            ),
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# cl_uchile_apa7
# ══════════════════════════════════════════════════════════════════════════════
"cl_uchile_apa7": {
    "verified_by": "TeXisStudio Community — reviewed against Universidad de Chile Graduate Regulations and VID guidelines",
    "sections": {
        "portada": {
            "title": "Title Page",
            "guidance": (
                "The official U. de Chile title page must include:\n"
                "• Logo and name of the Universidad de Chile.\n"
                "• Faculty and Institute or Department.\n"
                "• Full thesis title.\n"
                "• \"THESIS to obtain the degree of Doctor in [field].\"\n"
                "• Author’s name.\n"
                "• Thesis supervisor (guía) and co-supervisor (if applicable).\n"
                "• Santiago, Chile, [Month] [Year].\n"
                "Verify the format with the Doctoral Coordination of your Faculty.\n"
            ),
        },
        "declaracion": {
            "title": "Authorship Declaration",
            "guidance": (
                "Originality declaration required by U. de Chile.\n"
                "The Graduate Unit may require a signed record by the Academic Committee.\n"
            ),
        },
        "resumen": {
            "title": "Abstract",
            "guidance": (
                "Abstract in Spanish, 200–350 words.\n"
                "Problem, objectives, methodology, results and conclusions.\n"
                "Keywords (4–6).\n"
            ),
        },
        "abstract_ingles": {
            "title": "Abstract",
            "guidance": "Abstract in English. Recommended. Maximum 350 words. Keywords (4–6).",
        },
        "agradecimientos": {
            "title": "Acknowledgements",
            "guidance": (
                "Acknowledge the thesis supervisor, Academic Committee, ANID grants\n"
                "(ex-CONICYT: FONDECYT, FONDEF, Becas Chile) — include project or scholarship number.\n"
                "Also include UCH funds such as VID-FONDAP or Vicerrectoría projects.\n"
            ),
        },
        "dedicatoria": {
            "title": "Dedication",
            "guidance": "Optional. One to three lines. No printed heading.",
        },
        "indice": {
            "title": "Table of Contents",
            "guidance": "Generated automatically. Exact page numbers.",
        },
        "indice_figuras": {
            "title": "List of Figures",
            "guidance": "Enable if you have 5 or more figures.",
        },
        "indice_tablas": {
            "title": "List of Tables",
            "guidance": "Enable if you have 5 or more tables.",
        },
        "introduccion": {
            "title": "Introduction",
            "guidance": (
                "Contextualization, problem statement, rationale,\n"
                "research questions, objectives, hypotheses and structure.\n"
                "APA 7: (Author, year) in the text.\n"
            ),
        },
        "marco_teorico": {
            "title": "Theoretical Framework",
            "guidance": "Critical review organized by topics. Identify the gap the thesis addresses.",
        },
        "metodologia": {
            "title": "Methodology",
            "guidance": (
                "Research design, sample, instruments, procedure, analysis.\n"
                "Approval from the Research Ethics Committee on Human Beings (CEISH)\n"
                "if applicable.\n"
            ),
        },
        "resultados": {
            "title": "Results",
            "guidance": "Objective findings. APA 7 tables and figures.",
        },
        "discusion": {
            "title": "Discussion",
            "guidance": "Interpretation, comparison with literature, implications and limitations.",
        },
        "conclusiones": {
            "title": "Conclusions",
            "guidance": "Address objectives, contributions, limitations and future work.",
        },
        "referencias": {
            "title": "References",
            "guidance": "APA 7th edition, alphabetical list, hanging indent.",
        },
        "apendices": {
            "title": "Appendices",
            "guidance": "Instruments, additional data, ethics approval. Appendix A, B…",
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# mx_ipn_apa7
# ══════════════════════════════════════════════════════════════════════════════
"mx_ipn_apa7": {
    "verified_by": "TeXisStudio Community — reviewed against IPN-SIP and COFAA guidelines",
    "sections": {
        "portada": {
            "title": "Title Page",
            "guidance": (
                "The official IPN title page must include:\n"
                "• Logo of the IPN and of the Center or School (CINVESTAV, ESIME, UPIITA, etc.).\n"
                "• Full name of the Center or School.\n"
                "• Full thesis title.\n"
                "• \"THESIS submitted to obtain the degree of [Master/Doctor] in Sciences\n"
                "  with specialty in [area], PRESENTED BY:\"\n"
                "• Author’s name.\n"
                "• Thesis advisor’s name and affiliation.\n"
                "• Mexico City / [City], [Month] [Year].\n"
                "Each IPN academic unit may have a specific title page format —\n"
                "verify with the Academic Secretariat of your Center.\n"
            ),
        },
        "declaracion": {
            "title": "Authenticity Declaration",
            "guidance": (
                "The IPN requires an originality declaration. The SIP may additionally require\n"
                "a No-Debt Certificate and certification by the Tutorial Committee.\n"
                "Verify the specific documents required by your center or school.\n"
            ),
        },
        "resumen": {
            "title": "Abstract",
            "guidance": (
                "Abstract in Spanish, 200–350 words.\n"
                "Problem, methodology, results and contribution. Keywords (4–6).\n"
            ),
        },
        "abstract_ingles": {
            "title": "Abstract",
            "guidance": (
                "Abstract in English. Recommended for theses with international publication.\n"
                "Maximum 350 words. Keywords (4–6).\n"
            ),
        },
        "agradecimientos": {
            "title": "Acknowledgements",
            "guidance": (
                "Acknowledge the thesis advisor, tutorial committee, SIP/IPN grants,\n"
                "CONACYT/CONAHCYT (with scholarship number), COFAA, and research projects\n"
                "of the Center (SIP project key).\n"
            ),
        },
        "indice": {
            "title": "Table of Contents",
            "guidance": "Generated automatically. Includes all chapters, appendices and references.",
        },
        "indice_figuras": {
            "title": "List of Figures",
            "guidance": "Enable if you have 5 or more figures.",
        },
        "indice_tablas": {
            "title": "List of Tables",
            "guidance": "Enable if you have 5 or more tables.",
        },
        "introduccion": {
            "title": "Introduction",
            "guidance": (
                "Contextualization of the problem, problem statement, rationale,\n"
                "research questions, objectives, hypotheses and structure.\n"
                "The IPN has a polytechnic profile — if your research has a technological\n"
                "application, describe its engineering or industrial relevance.\n"
            ),
        },
        "marco_teorico": {
            "title": "Theoretical Framework and State of the Art",
            "guidance": (
                "Theoretical foundations and critical review of the state of the art.\n"
                "Organize by topics or technical approaches.\n"
                "Identify the gap that justifies your research.\n"
                "APA 7: (Author, year) in the text.\n"
            ),
        },
        "metodologia": {
            "title": "Methodology",
            "guidance": (
                "Research design, tools and equipment used,\n"
                "experimental or analytical procedure, validation, and\n"
                "ethical considerations if applicable.\n"
            ),
        },
        "resultados": {
            "title": "Results",
            "guidance": (
                "Objective findings organized by specific objective.\n"
                "APA 7 tables and figures. No interpretation in this chapter.\n"
            ),
        },
        "discusion": {
            "title": "Discussion",
            "guidance": "Interpretation of results, comparison with literature and limitations.",
        },
        "conclusiones": {
            "title": "Conclusions",
            "guidance": (
                "Address objectives, summarize original contributions,\n"
                "note limitations and propose future work.\n"
            ),
        },
        "referencias": {
            "title": "References",
            "guidance": "APA 7th edition, alphabetical list, hanging indent, DOI when available.",
        },
        "apendices": {
            "title": "Appendices",
            "guidance": "Additional data, source code, technical drawings or diagrams.",
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# mx_tec_apa7
# ══════════════════════════════════════════════════════════════════════════════
"mx_tec_apa7": {
    "verified_by": "TeXisStudio Community — reviewed against Tec de Monterrey Graduation Standards",
    "sections": {
        "portada": {
            "title": "Title Page",
            "guidance": (
                "The Tec title page must include:\n"
                "• Logo of Tecnológico de Monterrey.\n"
                "• Corresponding School or Department.\n"
                "• Full thesis title.\n"
                "• \"THESIS submitted as a partial requirement to obtain the degree of\n"
                "  [Master in / Doctor in] [Program name].\"\n"
                "• Author’s full name.\n"
                "• Name of principal advisor and co-advisor (if applicable).\n"
                "• \"Monterrey, Nuevo León / [Campus], [Month] [Year].\"\n"
                "Download the official title page template for your program from the\n"
                "Tec graduation portal — format varies by school.\n"
            ),
        },
        "declaracion": {
            "title": "Academic Integrity Statement",
            "guidance": (
                "The Tec de Monterrey requires an Academic Integrity Statement. Standard text:\n"
                "\"The author of this work declares that, to the best of their knowledge,\n"
                "this is original work and that no plagiarism exists, as defined by\n"
                "the Tec de Monterrey standards.\"\n"
                "The Tec uses plagiarism detection tools (Turnitin) — the acceptable\n"
                "similarity percentage is defined by your program (typically < 15%).\n"
            ),
        },
        "resumen": {
            "title": "Abstract",
            "guidance": (
                "Abstract in Spanish, 150–350 words.\n"
                "Includes: research question, methodology, main findings\n"
                "and contribution to the field. End with Keywords (4–6).\n"
                "Self-contained: no citations, no figures, no undefined acronyms.\n"
            ),
        },
        "abstract_ingles": {
            "title": "Abstract",
            "guidance": (
                "Abstract in English. Required in international Tec programs.\n"
                "Maximum 350 words. Same structure as the Spanish Abstract.\n"
                "The Tec has English-language programs (EGADE, CITEM, etc.) that may require\n"
                "the entire thesis to be in English — verify with your coordinator.\n"
            ),
        },
        "agradecimientos": {
            "title": "Acknowledgements",
            "guidance": (
                "Optional. Acknowledge the advisor, committee members and funding sources.\n"
                "If you received a CONAHCYT, Tec or corporate sponsor scholarship,\n"
                "include the scholarship or agreement number.\n"
            ),
        },
        "indice": {
            "title": "Table of Contents",
            "guidance": "Generated automatically with exact page numbers.",
        },
        "indice_figuras": {
            "title": "List of Figures",
            "guidance": "Enable if you have 5 or more figures. APA 7.",
        },
        "indice_tablas": {
            "title": "List of Tables",
            "guidance": "Enable if you have 5 or more tables. APA 7.",
        },
        "introduccion": {
            "title": "Introduction",
            "guidance": (
                "Contextualization, problem statement, rationale, research questions,\n"
                "objectives, hypotheses (if applicable) and thesis structure.\n"
                "The Tec values applied relevance: explain the practical or business impact\n"
                "of the problem you address.\n"
                "Typical length: 10–20 pages.\n"
            ),
        },
        "marco_teorico": {
            "title": "Theoretical Framework",
            "guidance": (
                "Conceptual foundations and critical review of the literature.\n"
                "Organize by topics or approaches — not as a sequential summary of authors.\n"
                "Identify the gap that justifies your research.\n"
                "APA 7: (Author, year) in the text.\n"
            ),
        },
        "metodologia": {
            "title": "Methodology",
            "guidance": (
                "Research design, sample, instruments, procedure,\n"
                "statistical analysis and ethical considerations.\n"
                "The Tec values mixed methods and corporate case studies.\n"
            ),
        },
        "resultados": {
            "title": "Results",
            "guidance": (
                "Objective findings organized by research question.\n"
                "APA 7 tables and figures. No interpretation in this chapter.\n"
            ),
        },
        "discusion": {
            "title": "Discussion",
            "guidance": (
                "Interpretation of results, comparison with literature, practical implications\n"
                "(highly valued at the Tec) and limitations.\n"
            ),
        },
        "conclusiones": {
            "title": "Conclusions",
            "guidance": (
                "Answer research questions, summarize contributions, note\n"
                "limitations and suggest future research.\n"
            ),
        },
        "referencias": {
            "title": "References",
            "guidance": "APA 7th edition, alphabetical list, hanging indent, DOI mandatory when available.",
        },
        "apendices": {
            "title": "Appendices",
            "guidance": "Supplementary materials. Turnitin report if required by your program.",
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# mx_uam_azc_cbi
# ══════════════════════════════════════════════════════════════════════════════
"mx_uam_azc_cbi": {
    "sections": {
        "title_page": {
            "title": "Title Page",
            "guidance": (
                "The title page must include: UAM logo, university name, campus,\n"
                "division and department, work title, student name and ID,\n"
                "term and year, and advisor’s name.\n"
            ),
        },
        "dedication": {
            "title": "Dedication",
        },
        "acknowledgements": {
            "title": "Acknowledgements",
        },
        "abstract_es": {
            "title": "Abstract (Spanish)",
            "guidance": "Maximum 350 words. Includes: background, problem, methodology, contributions and conclusions.",
        },
        "abstract_en": {
            "title": "Abstract (English)",
            "guidance": "English abstract. Mandatory for graduate theses; recommended for undergraduate.",
        },
        "table_of_contents": {
            "title": "Table of Contents",
        },
        "list_of_figures": {
            "title": "List of Figures",
        },
        "list_of_tables": {
            "title": "List of Tables",
        },
        "introduction": {
            "title": "Introduction",
            "guidance": "Presents the context, problem statement, objectives and hypotheses.",
        },
        "theoretical_framework": {
            "title": "Theoretical Framework",
            "guidance": "Review of the state of the art and theoretical foundations of the work.",
        },
        "methodology": {
            "title": "Methodology",
            "guidance": "Describes the method, tools and procedures used.",
        },
        "results": {
            "title": "Results",
            "guidance": "Presents and analyzes the obtained results.",
        },
        "discussion": {
            "title": "Discussion",
        },
        "conclusions": {
            "title": "Conclusions",
            "guidance": "Conclusions, limitations and future work.",
        },
        "references": {
            "title": "References",
        },
        "appendix": {
            "title": "Appendices",
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# mx_uam_azc_dcsh
# ══════════════════════════════════════════════════════════════════════════════
"mx_uam_azc_dcsh": {
    "sections": {
        "title_page": {
            "title": "Title Page",
            "guidance": (
                "Official UAM-DCSH title page: UAM logo, university name, campus,\n"
                "division, department, title of the research work or thesis,\n"
                "student name and ID, term and year, advisor’s or director’s name\n"
                "and co-advisor (if applicable).\n"
            ),
        },
        "dedication": {
            "title": "Dedication",
        },
        "acknowledgements": {
            "title": "Acknowledgements",
        },
        "abstract_es": {
            "title": "Abstract (Spanish)",
            "guidance": (
                "Maximum 300 words. Must include: problem statement,\n"
                "general objective, methodology, main findings and conclusions.\n"
                "Avoid bibliographic citations in the abstract.\n"
            ),
        },
        "abstract_en": {
            "title": "Abstract (English)",
            "guidance": "English abstract. Recommended for graduate programs.",
        },
        "table_of_contents": {
            "title": "Table of Contents",
        },
        "list_of_figures": {
            "title": "List of Figures",
        },
        "list_of_tables": {
            "title": "List of Tables",
        },
        "introduction": {
            "title": "Introduction",
            "guidance": (
                "General context, rationale, problem statement,\n"
                "research question, hypothesis or objectives, and structure\n"
                "of the work.\n"
            ),
        },
        "theoretical_framework": {
            "title": "Theoretical-Conceptual Framework",
            "guidance": (
                "Critical review of the literature. In social sciences, an explicit\n"
                "positioning of the author with respect to theoretical approaches is expected.\n"
                "Use Chicago Author-Date style for citations.\n"
            ),
        },
        "methodology": {
            "title": "Methodology",
            "guidance": (
                "Methodological strategy: qualitative, quantitative or mixed.\n"
                "Units of analysis, data collection techniques, selection criteria,\n"
                "and ethical considerations if applicable.\n"
            ),
        },
        "results": {
            "title": "Results and Analysis",
            "guidance": "Presentation and critical analysis of findings.",
        },
        "discussion": {
            "title": "Discussion",
        },
        "conclusions": {
            "title": "Conclusions",
            "guidance": (
                "Synthesis of findings, answer to the research question,\n"
                "limitations, contributions to the field and future research directions.\n"
            ),
        },
        "references": {
            "title": "Bibliography",
            "guidance": "Chicago Author-Date format. Include all sources cited in the text.",
        },
        "appendix": {
            "title": "Appendices",
            "guidance": "Data collection instruments, transcriptions, supplementary tables, etc.",
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# mx_uam_cua_dci
# ══════════════════════════════════════════════════════════════════════════════
"mx_uam_cua_dci": {
    "sections": {
        "title_page": {
            "title": "Title Page",
            "guidance": (
                "Official UAM-DCI title page: UAM logo, university name, campus,\n"
                "division, research area, work title, student name and ID,\n"
                "term and year, and thesis director’s name.\n"
            ),
        },
        "dedication": {
            "title": "Dedication",
        },
        "acknowledgements": {
            "title": "Acknowledgements",
        },
        "abstract_es": {
            "title": "Abstract (Spanish)",
            "guidance": (
                "Maximum 350 words. Must include: problem context, main objective,\n"
                "technical methodology used, key results or contributions\n"
                "and conclusions.\n"
            ),
        },
        "abstract_en": {
            "title": "Abstract (English)",
            "guidance": "English translation of the abstract. Mandatory for graduate programs.",
        },
        "table_of_contents": {
            "title": "Table of Contents",
        },
        "list_of_figures": {
            "title": "List of Figures",
        },
        "list_of_tables": {
            "title": "List of Tables",
        },
        "introduction": {
            "title": "Introduction",
            "guidance": (
                "Technological or information-system context, problem statement,\n"
                "general objective, specific objectives, scope and\n"
                "organization of the document.\n"
            ),
        },
        "theoretical_framework": {
            "title": "Theoretical Framework and State of the Art",
            "guidance": (
                "Review of fundamental concepts and related work. In DCI, a review\n"
                "of recent technical literature (ACM, IEEE conferences, Scopus or WoS articles)\n"
                "and identification of the knowledge gap is valued.\n"
            ),
        },
        "methodology": {
            "title": "Methodology",
            "guidance": (
                "Development or research methodology: SCRUM, RUP, Design Science,\n"
                "controlled experimentation, etc. Include system architecture diagram\n"
                "if applicable, use cases, and evaluation criteria.\n"
            ),
        },
        "results": {
            "title": "Results",
            "guidance": (
                "Description of the developed system, conducted experiments,\n"
                "evaluation metrics and comparison with related work.\n"
            ),
        },
        "discussion": {
            "title": "Discussion",
        },
        "conclusions": {
            "title": "Conclusions and Future Work",
            "guidance": "Technical conclusions, work limitations and future development directions.",
        },
        "references": {
            "title": "References",
            "guidance": "APA 7 format. Include DOI when available.",
        },
        "appendix": {
            "title": "Appendices",
            "guidance": "Relevant source code, additional diagrams, experimental data, etc.",
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# mx_uam_izt_cbi
# ══════════════════════════════════════════════════════════════════════════════
"mx_uam_izt_cbi": {
    "sections": {
        "title_page": {
            "title": "Title Page",
            "guidance": (
                "The title page must include: UAM logo, university and campus name,\n"
                "division, department and research area, work title,\n"
                "student’s name, degree sought, advisor(s)’ name(s),\n"
                "term-year of presentation.\n"
            ),
        },
        "dedication": {
            "title": "Dedication",
        },
        "acknowledgements": {
            "title": "Acknowledgements",
        },
        "abstract_es": {
            "title": "Abstract (Spanish)",
            "guidance": "Maximum 300 words. Describes the problem, methods used and main results.",
        },
        "abstract_en": {
            "title": "Abstract (English)",
            "guidance": "English abstract mandatory for graduate programs (ICR, Master’s, Doctoral).",
        },
        "table_of_contents": {
            "title": "Table of Contents",
        },
        "list_of_figures": {
            "title": "List of Figures",
        },
        "list_of_tables": {
            "title": "List of Tables",
        },
        "introduction": {
            "title": "Introduction",
            "guidance": "Background, problem statement, hypothesis and objectives.",
        },
        "theoretical_framework": {
            "title": "Theoretical Framework and State of the Art",
            "guidance": "Bibliographic review and theoretical foundations.",
        },
        "methodology": {
            "title": "Methodology and Experimental Development",
            "guidance": "Materials, methods and experimental or computational procedures.",
        },
        "results": {
            "title": "Results and Discussion",
            "guidance": "Presents results with figures, tables and statistical analysis when applicable.",
        },
        "discussion": {
            "title": "Discussion",
            "guidance": "Interprets results in relation to the hypothesis and literature. Compares with previous work.",
        },
        "conclusions": {
            "title": "Conclusions and Perspectives",
            "guidance": "Conclusions regarding the stated hypothesis and proposals for future work.",
        },
        "glossary": {
            "title": "Glossary",
            "guidance": "Definitions of technical terms and acronyms used in the document.",
        },
        "references": {
            "title": "References",
            "guidance": "APA 7 format for social sciences; IEEE or Vancouver for exact sciences.",
        },
        "appendix": {
            "title": "Appendices",
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# mx_uam_izt_dcsh
# ══════════════════════════════════════════════════════════════════════════════
"mx_uam_izt_dcsh": {
    "sections": {
        "title_page": {
            "title": "Title Page",
            "guidance": (
                "Official UAM-CSH title page: UAM logo, university name, campus,\n"
                "division and department, thesis or terminal work title,\n"
                "student name and ID, term and year, advisor’s name.\n"
            ),
        },
        "dedication": {
            "title": "Dedication",
        },
        "acknowledgements": {
            "title": "Acknowledgements",
        },
        "abstract_es": {
            "title": "Abstract (Spanish)",
            "guidance": "Maximum 300 words. Includes objective, methodology and main findings.",
        },
        "abstract_en": {
            "title": "Abstract (English)",
        },
        "table_of_contents": {
            "title": "Table of Contents",
        },
        "list_of_figures": {
            "title": "List of Figures",
        },
        "list_of_tables": {
            "title": "List of Tables",
            "guidance": "In CSH, ‘cuadros’ (tables) is preferred over ‘tablas’.",
        },
        "introduction": {
            "title": "Introduction",
            "guidance": (
                "Presentation of the research problem, relevance, research question,\n"
                "hypothesis (if applicable) and organization of the work.\n"
                "In humanities it may be more extensive (10–15 pages).\n"
            ),
        },
        "theoretical_framework": {
            "title": "Theoretical Framework",
            "guidance": (
                "Theoretical debate and author’s positioning. In CSH-Iztapalapa,\n"
                "depth in the discussion of theoretical approaches and explicit\n"
                "articulation with the research problem is valued.\n"
            ),
        },
        "methodology": {
            "title": "Methodology",
            "guidance": (
                "Research paradigm, design, techniques (interviews, surveys,\n"
                "discourse analysis, ethnography, etc.) and justification of their choice.\n"
            ),
        },
        "results": {
            "title": "Analysis and Results",
        },
        "discussion": {
            "title": "Discussion",
        },
        "conclusions": {
            "title": "Conclusions",
        },
        "references": {
            "title": "Reference Sources",
            "guidance": "Chicago Author-Date format. Include primary and secondary sources.",
        },
        "appendix": {
            "title": "Appendices",
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# mx_uam_xoc_dcbs
# ══════════════════════════════════════════════════════════════════════════════
"mx_uam_xoc_dcbs": {
    "sections": {
        "title_page": {
            "title": "Title Page",
            "guidance": (
                "Official UAM-DCBS title page: UAM logo, university name, campus,\n"
                "division and department, research work title, student name and ID,\n"
                "term and year, and thesis director’s name.\n"
            ),
        },
        "dedication": {
            "title": "Dedication",
        },
        "acknowledgements": {
            "title": "Acknowledgements",
        },
        "abstract_es": {
            "title": "Abstract (Spanish)",
            "guidance": (
                "Maximum 250 words. Abbreviated IMRaD structure: background,\n"
                "objective, methods, results and main conclusion.\n"
                "Do not include bibliographic citations or undefined abbreviations.\n"
            ),
        },
        "abstract_en": {
            "title": "Abstract (English)",
            "guidance": "Exact English translation of the abstract. Mandatory for graduate programs.",
        },
        "table_of_contents": {
            "title": "Table of Contents",
        },
        "list_of_figures": {
            "title": "List of Figures",
        },
        "list_of_tables": {
            "title": "List of Tables",
        },
        "introduction": {
            "title": "Introduction",
            "guidance": (
                "Background to the problem, clinical or biological relevance,\n"
                "rationale, research question and hypothesis (if applicable).\n"
            ),
        },
        "theoretical_framework": {
            "title": "Theoretical Framework",
            "guidance": (
                "Review of the state of the art. In health sciences, a review of recent\n"
                "literature (preferably last 5 years) with emphasis on controlled studies\n"
                "and systematic reviews is expected.\n"
            ),
        },
        "methodology": {
            "title": "Methodology",
            "guidance": (
                "Study type (observational, experimental, clinical, etc.),\n"
                "population and sample, inclusion/exclusion criteria, variables,\n"
                "procedures, instruments and statistical analysis.\n"
                "Include ethics committee approval if applicable.\n"
            ),
        },
        "results": {
            "title": "Results",
            "guidance": (
                "Objective presentation of findings without interpretation.\n"
                "Use tables and figures when clearer than text.\n"
                "Report frequency, central tendency and dispersion measures.\n"
            ),
        },
        "discussion": {
            "title": "Discussion",
            "guidance": (
                "Interpretation of results in the context of the literature.\n"
                "Discuss study limitations. Do not repeat the results.\n"
            ),
        },
        "conclusions": {
            "title": "Conclusions",
            "guidance": "Brief conclusions, directly derived from the results.",
        },
        "references": {
            "title": "References",
            "guidance": "Vancouver format (numbered, in order of appearance). Maximum 60 references for undergraduate, no limit for graduate.",
        },
        "appendix": {
            "title": "Appendices",
            "guidance": "Measurement instruments, informed consent forms, committee approvals, etc.",
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# mx_uanl_apa7
# ══════════════════════════════════════════════════════════════════════════════
"mx_uanl_apa7": {
    "verified_by": "TeXisStudio Community — reviewed against UANL Graduate Studies Office guidelines",
    "sections": {
        "portada": {
            "title": "Title Page",
            "guidance": (
                "Official UANL title page. Includes:\n"
                "• UANL shield and name.\n"
                "• Name of the Faculty or Graduate Division.\n"
                "• Thesis title.\n"
                "• \"THESIS for the degree of [Master/Doctor] in [Program].\"\n"
                "• Author’s name.\n"
                "• Thesis director.\n"
                "• San Nicolás de los Garza, N.L., [Month] [Year].\n"
                "Verify the specific title page format with the Graduate Office of your Faculty.\n"
            ),
        },
        "declaracion": {
            "title": "Authenticity Declaration",
            "guidance": (
                "Originality declaration required by UANL.\n"
                "Some faculties require an additional letter signed by the director.\n"
            ),
        },
        "resumen": {
            "title": "Abstract",
            "guidance": (
                "Abstract in Spanish, 200–350 words.\n"
                "Problem, objective, method, results and main conclusion.\n"
                "Keywords (4–6).\n"
            ),
        },
        "abstract_ingles": {
            "title": "Abstract",
            "guidance": "Abstract in English. Recommended. Maximum 350 words. Keywords (4–6).",
        },
        "agradecimientos": {
            "title": "Acknowledgements",
            "guidance": (
                "Acknowledge the thesis director, committee members, CONAHCYT grants and\n"
                "PAICYT projects (UANL Scientific and Technological Research Support Program).\n"
            ),
        },
        "indice": {
            "title": "Table of Contents",
            "guidance": "Generated automatically. Exact page numbers.",
        },
        "indice_figuras": {
            "title": "List of Figures",
            "guidance": "Enable if you have 5 or more figures.",
        },
        "indice_tablas": {
            "title": "List of Tables",
            "guidance": "Enable if you have 5 or more tables.",
        },
        "introduccion": {
            "title": "Introduction",
            "guidance": (
                "Contextualization, problem statement, rationale,\n"
                "research questions, objectives and hypotheses. Thesis structure.\n"
            ),
        },
        "marco_teorico": {
            "title": "Theoretical Framework",
            "guidance": (
                "Critical review of the literature and conceptual foundations.\n"
                "Organize by topics. Identify the gap. APA 7: (Author, year).\n"
            ),
        },
        "metodologia": {
            "title": "Methodology",
            "guidance": "Design, sample, instruments, procedure, analysis and ethics.",
        },
        "resultados": {
            "title": "Results",
            "guidance": "Objective findings. APA 7 tables and figures. No interpretation.",
        },
        "discusion": {
            "title": "Discussion",
            "guidance": "Interpretation, comparison with literature, implications and limitations.",
        },
        "conclusiones": {
            "title": "Conclusions",
            "guidance": "Answer questions, summarize contributions, limitations and future work.",
        },
        "referencias": {
            "title": "References",
            "guidance": "APA 7th edition, alphabetical list, hanging indent.",
        },
        "apendices": {
            "title": "Appendices",
            "guidance": "Supplementary materials. Label Appendix A, B…",
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# mx_udg_apa7
# ══════════════════════════════════════════════════════════════════════════════
"mx_udg_apa7": {
    "verified_by": "TeXisStudio Community — reviewed against UdeG Academic Coordination guidelines",
    "sections": {
        "portada": {
            "title": "Title Page",
            "guidance": (
                "Official Universidad de Guadalajara title page. Includes:\n"
                "• Shield and name of the Universidad de Guadalajara.\n"
                "• University Center or corresponding Studies Division\n"
                "  (CU Valles, CUCEA, CUCSH, CUCS, etc.).\n"
                "• Thesis title.\n"
                "• \"THESIS to obtain the degree of [Master/Doctor] in [Program].\"\n"
                "• Author’s name.\n"
                "• Thesis director and institution.\n"
                "• Guadalajara, Jalisco, [Month] [Year].\n"
                "Verify the title page format with the Graduate Coordination\n"
                "of your University Center.\n"
            ),
        },
        "declaracion": {
            "title": "Authenticity Declaration",
            "guidance": (
                "Originality declaration required by UdeG.\n"
                "The University Center may also request a Tutorial Committee record.\n"
            ),
        },
        "resumen": {
            "title": "Abstract",
            "guidance": (
                "Abstract in Spanish, 200–350 words.\n"
                "Research question, methodology, results and contribution.\n"
                "Keywords (4–6).\n"
            ),
        },
        "abstract_ingles": {
            "title": "Abstract",
            "guidance": "Abstract in English. Recommended. Maximum 350 words.",
        },
        "agradecimientos": {
            "title": "Acknowledgements",
            "guidance": (
                "Acknowledge the thesis director, tutorial committee, CONAHCYT grants\n"
                "and the UdeG Quality Education Strengthening Program (PFCE)\n"
                "or UDG-PRO projects.\n"
            ),
        },
        "dedicatoria": {
            "title": "Dedication",
            "guidance": "Optional. One to three lines. No printed heading.",
        },
        "indice": {
            "title": "Table of Contents",
            "guidance": "Generated automatically with exact page numbers.",
        },
        "indice_figuras": {
            "title": "List of Figures",
            "guidance": "Enable if you have 5 or more figures.",
        },
        "indice_tablas": {
            "title": "List of Tables",
            "guidance": "Enable if you have 5 or more tables.",
        },
        "introduccion": {
            "title": "Introduction",
            "guidance": (
                "Contextualization, problem statement, rationale, research questions,\n"
                "objectives, hypotheses and thesis structure.\n"
            ),
        },
        "marco_teorico": {
            "title": "Theoretical Framework",
            "guidance": (
                "Conceptual foundations and critical review of the literature.\n"
                "Organize by topics. APA 7: (Author, year).\n"
            ),
        },
        "metodologia": {
            "title": "Methodology",
            "guidance": "Design, sample, instruments, procedure, analysis and ethics.",
        },
        "resultados": {
            "title": "Results",
            "guidance": "Objective findings. APA 7 tables and figures. No interpretation.",
        },
        "discusion": {
            "title": "Discussion",
            "guidance": "Interpretation, comparison with literature, implications and limitations.",
        },
        "conclusiones": {
            "title": "Conclusions",
            "guidance": "Answer questions, summarize contributions, note limitations and future work.",
        },
        "referencias": {
            "title": "References",
            "guidance": "APA 7th edition, alphabetical list, hanging indent. DOI when available.",
        },
        "apendices": {
            "title": "Appendices",
            "guidance": "Instruments, additional data. Label Appendix A, B…",
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# mx_unam_apa7
# ══════════════════════════════════════════════════════════════════════════════
"mx_unam_apa7": {
    "sections": {
        "portada": {
            "title": "Title Page",
            "guidance": (
                "Generated automatically from project metadata.\n"
                "The official UNAM title page must include:\n"
                "• UNAM logo and name (university shield).\n"
                "• Name of the Faculty, Institute or National School.\n"
                "• Full name of the graduate or undergraduate program.\n"
                "• Thesis title (in title case, centered).\n"
                "• \"THESIS\" or \"DISSERTATION\" as appropriate, followed by the degree\n"
                "  (e.g., \"submitted to obtain the degree of Doctor in [field] by:\").\n"
                "• Author’s full name (no abbreviations).\n"
                "• Name of the thesis supervisor.\n"
                "• Mexico City, month and year (e.g., \"Mexico City, June 2026\").\n"
                "Consult the title page template for your program — the format varies\n"
                "between faculties and graduate programs.\n"
            ),
        },
        "declaracion": {
            "title": "Authenticity Declaration",
            "guidance": (
                "The Authenticity Declaration certifies that the work is original\n"
                "and sources are correctly cited. Standard content:\n"
                "\"I declare that this thesis is original and my own work.\n"
                "All sources consulted have been duly cited and referenced\n"
                "in accordance with APA 7th edition standards.\"\n"
                "Some faculties and programs additionally require:\n"
                "• A Letter of Responsibility signed by the thesis supervisor.\n"
                "• A specific form issued by the Graduate Studies Division.\n"
                "Verify the requirements with your program — the form may be required\n"
                "at the Coordination office before the final print.\n"
            ),
        },
        "resumen": {
            "title": "Abstract",
            "guidance": (
                "Abstract in Spanish. Recommended: 200–350 words.\n"
                "Must be self-contained: no citations, no undefined abbreviations, no equations.\n"
                "Recommended structure per APA 7th edition:\n"
                "  1. Research problem statement.\n"
                "  2. General objective(s) of the study.\n"
                "  3. Methodological approach and research design.\n"
                "  4. Main findings or results.\n"
                "  5. Conclusions and contributions to the field.\n"
                "End with 4 to 6 Keywords separated by semicolons.\n"
                "The abstract will appear in the UNAM Library System catalog\n"
                "(UNAM Biblioweb) — write it as a standalone piece.\n"
            ),
        },
        "abstract_ingles": {
            "title": "Abstract",
            "guidance": (
                "Abstract in English. Recommended for graduate theses for international\n"
                "visibility and required for ProQuest Dissertations & Theses.\n"
                "Maximum 350 words (ProQuest limit for doctoral dissertations).\n"
                "Self-contained: no citations, no undefined abbreviations.\n"
                "Same structure as the Spanish Abstract, in English.\n"
                "End with: Keywords (4–6 English keywords).\n"
            ),
        },
        "agradecimientos": {
            "title": "Acknowledgements",
            "guidance": (
                "Optional but conventional in Mexican university theses.\n"
                "Acknowledge: thesis supervisor and committee, fellow lab or research\n"
                "group members, institutions that provided access to data or archives,\n"
                "and personal support.\n"
                "If the research received external funding (CONACYT/CONAHCYT,\n"
                "DGAPA-PAPIIT, PAPIME, international scholarships), it is mandatory to\n"
                "mention it with the project or scholarship number.\n"
                "Example: \"This research was funded by CONAHCYT through the\n"
                "national doctoral scholarship No. [xxxxx].\"\n"
                "Typical length: half to one page.\n"
            ),
        },
        "dedicatoria": {
            "title": "Dedication",
            "guidance": (
                "Optional. Brief — typically 1 to 3 lines.\n"
                "No printed heading; the profile manages the formatting.\n"
            ),
        },
        "indice_general": {
            "title": "Table of Contents",
            "guidance": (
                "Generated automatically from document headings.\n"
                "UNAM requires a complete table of contents with exact page numbers.\n"
                "Includes: all front matter (except the title page), body chapters,\n"
                "appendices and references.\n"
                "Recommended depth: up to level 2 (chapters and main sections).\n"
            ),
        },
        "indice_figuras": {
            "title": "List of Figures",
            "guidance": (
                "Required if the thesis contains figures, graphs, maps or illustrations.\n"
                "Generated automatically from figure captions.\n"
                "Enable this section if you have 5 or more figures.\n"
                "In APA 7, figures are designated “Figure X” in the text.\n"
            ),
        },
        "indice_tablas": {
            "title": "List of Tables",
            "guidance": (
                "Required if the thesis contains tables. Generated automatically.\n"
                "Enable this section if you have 5 or more tables.\n"
                "In APA 7, tables are designated “Table X” in the text.\n"
            ),
        },
        "lista_abreviaturas": {
            "title": "List of Abbreviations and Acronyms",
            "guidance": (
                "Optional, but recommended if the thesis uses more than 10 abbreviations or acronyms.\n"
                "List in alphabetical order: abbreviation on the left, full term on the right.\n"
                "In the body text, define each abbreviation the first time it appears\n"
                "by writing the full term followed by the abbreviation in parentheses.\n"
            ),
        },
        "introduccion": {
            "title": "Introduction",
            "guidance": (
                "The introduction establishes the context, the problem and the contribution.\n"
                "Structure recommended by UNAM-CEP for graduate theses:\n"
                "1. Contextualization: overview of the field of study.\n"
                "2. Problem statement: what gap or contradiction exists in current knowledge?\n"
                "3. Rationale: why is it relevant to address it? (theoretical, practical\n"
                "   or social importance).\n"
                "4. Research question(s): stated precisely.\n"
                "5. General objective and specific objectives: concrete and measurable.\n"
                "6. Hypothesis or working assumption (if applicable to the research design).\n"
                "7. Scope: spatial, temporal and thematic boundaries of the study.\n"
                "8. Thesis structure: a brief paragraph per chapter.\n"
                "APA 7 citations: (Author, year) in the text or Author (year) in narrative form.\n"
                "Typical length: 15–25 pages.\n"
            ),
        },
        "marco_teorico": {
            "title": "Theoretical Framework and Literature Review",
            "guidance": (
                "The theoretical framework presents the conceptual foundations and state of the art.\n"
                "CEP-UNAM guidelines:\n"
                "• Organize by theoretical currents, approaches or debates — not as a\n"
                "  sequential summary of authors.\n"
                "• Define the key concepts you will use throughout the thesis.\n"
                "• Review the most relevant literature (last 10 years, plus foundational works).\n"
                "• Identify contradictions, gaps and unresolved debates that\n"
                "  justify your research.\n"
                "• Conclude by explicitly positioning your work within the field.\n"
                "APA 7 citations: every claim about existing literature requires a citation.\n"
                "For secondary citations, use: \"as cited in Author (year)\".\n"
                "Typical length: 30–60 pages.\n"
            ),
        },
        "marco_conceptual": {
            "title": "Conceptual Framework",
            "guidance": (
                "Optional. Activate as an independent chapter if your thesis requires\n"
                "developing a novel analytical framework or if the theoretical contribution\n"
                "is central to the research.\n"
                "Includes: operational definition of variables or analytical categories,\n"
                "conceptual relationships, and the author’s own model or analytical scheme.\n"
                "In many social science and humanities theses, the conceptual framework\n"
                "is integrated within the Theoretical Framework chapter.\n"
            ),
        },
        "metodologia": {
            "title": "Methodology",
            "guidance": (
                "The methodology must allow the study to be replicated. Includes:\n"
                "• Approach and paradigm: quantitative, qualitative or mixed. Justify\n"
                "  the choice based on the problem and research questions.\n"
                "• Research design: experimental, quasi-experimental, correlational,\n"
                "  descriptive, phenomenological, hermeneutic, etc.\n"
                "• Units of analysis, population and sample (or corpus): selection\n"
                "  criteria, size, sampling procedure.\n"
                "• Data collection instruments and techniques: surveys, interviews,\n"
                "  observation, documentary analysis, content analysis, etc.\n"
                "  Include information about instrument validation.\n"
                "• Data analysis procedure: software used (SPSS, R, Atlas.TI, NVivo),\n"
                "  statistical or analytical techniques.\n"
                "• Ethical considerations: Ethics Committee approval if human subjects\n"
                "  were involved; informed consent.\n"
                "• Methodological limitations.\n"
                "APA 7: standardized assessment instruments require a full citation.\n"
            ),
        },
        "resultados": {
            "title": "Results",
            "guidance": (
                "Present findings objectively, without interpretation.\n"
                "• Organize by research question or specific objective.\n"
                "• For quantitative studies: report descriptive statistics,\n"
                "  hypothesis test results (statistic, p-value, effect size),\n"
                "  confidence intervals. Tables and figures with footnotes per APA 7.\n"
                "• For qualitative studies: present emerging categories or themes\n"
                "  with representative verbatim quotes; ensure participant anonymization\n"
                "  as committed to in the informed consent.\n"
                "• Every table and figure must be referenced in the text before it appears.\n"
                "• APA 7: “Table X shows…”, “Figure X illustrates…”\n"
                "Length: varies; in quantitative theses often 30–60 pages.\n"
            ),
        },
        "discusion": {
            "title": "Discussion",
            "guidance": (
                "Interpret results in relation to the theoretical framework and literature.\n"
                "APA 7 recommends opening with a statement of support or non-support for the hypothesis.\n"
                "A solid discussion:\n"
                "• Takes each result and connects it to theory and prior evidence\n"
                "  (confirming, contradicting or nuancing it).\n"
                "• Explains unexpected or contradictory results.\n"
                "• Discusses theoretical and practical implications.\n"
                "• Honestly acknowledges the study’s limitations.\n"
                "• Suggests specific future research directions, derived from\n"
                "  limitations and unresolved findings.\n"
                "In many UNAM theses this chapter is merged with Results or Conclusions.\n"
                "Activate as an independent chapter if the analysis warrants it.\n"
            ),
        },
        "conclusiones": {
            "title": "Conclusions",
            "guidance": (
                "Conclusions synthesize the central argument and contributions:\n"
                "• Directly answer each research question or objective.\n"
                "• Summarize original contributions: what does the field now know that\n"
                "  it did not know before this research?\n"
                "• Practical, public policy or management implications (if applicable).\n"
                "• Specific and honest limitations of the work.\n"
                "• Concrete and bounded future research directions.\n"
                "Avoid repeating results — the committee has read the previous chapter.\n"
                "In UNAM doctoral theses the committee will evaluate an oral defense;\n"
                "conclusions are the text that best prepares that conversation.\n"
                "Typical length: 10–20 pages.\n"
            ),
        },
        "referencias": {
            "title": "References",
            "guidance": (
                "APA 7th edition: alphabetical list by first author’s last name,\n"
                "hanging indent, generated automatically from your .bib file.\n"
                "APA 7 verification points:\n"
                "• Book and journal titles in italics.\n"
                "• Article and chapter titles without quotation marks (unlike APA 6).\n"
                "• DOI in URL format: https://doi.org/xxxxx (no trailing period).\n"
                "• For online sources: include URL and access date if content may change.\n"
                "• For unpublished theses: Last, N. (Year). Thesis title\n"
                "  [Doctoral dissertation, Universidad Nacional Autónoma de México].\n"
                "Expected volume for doctoral theses: 100–300 references.\n"
            ),
        },
        "apendices": {
            "title": "Appendices",
            "guidance": (
                "Supplementary materials that would interrupt the main narrative:\n"
                "• Research instruments (questionnaires, interview guides,\n"
                "  observation rubrics).\n"
                "• Raw data, extended statistical tables or additional results.\n"
                "• Ethics Committee approval letter and consent forms.\n"
                "• Interview transcripts (representative excerpts).\n"
                "• Authorization letters from collaborating institutions.\n"
                "Label: Appendix A, B… with descriptive title.\n"
                "Reference from the text: \"(see Appendix A)\".\n"
            ),
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# mx_unam_vancouver
# ══════════════════════════════════════════════════════════════════════════════
"mx_unam_vancouver": {
    "sections": {
        "portada": {
            "title": "Title Page",
            "guidance": (
                "Official UNAM title page. Must include:\n"
                "• UNAM and Faculty or Institute logo and name.\n"
                "• Full name of the specialization or graduate program.\n"
                "• Thesis title (centered, in title case).\n"
                "• \"THESIS submitted to obtain the title/degree of [Specialist in / Doctor in]\n"
                "  [specialty/area], PRESENTED BY:\"\n"
                "• Author’s full name.\n"
                "• Thesis supervisor’s name and institutional affiliation.\n"
                "• Mexico City, month and year.\n"
                "Medical specializations (UNAM-IMSS, UNAM-ISSSTE, Hospital General, etc.)\n"
                "have specific title page formats — consult your program coordinator.\n"
            ),
        },
        "declaracion": {
            "title": "Originality Statement",
            "guidance": (
                "Some specializations and doctoral health sciences programs at UNAM\n"
                "require an Originality Letter or a sworn statement that the thesis is original work.\n"
                "Verify the requirement with the Graduate Studies Division of your Faculty.\n"
            ),
        },
        "resumen": {
            "title": "Abstract",
            "guidance": (
                "Structured abstract in Spanish. ICMJE recommends 250 words maximum\n"
                "for research articles; for degree theses: 200–350 words.\n"
                "Recommended structured format:\n"
                "  • Background/Introduction: one or two sentences contextualizing the problem.\n"
                "  • Objective: general objective of the study (one sentence).\n"
                "  • Methods: study design, population, intervention/exposure,\n"
                "    outcome variables, statistical analysis.\n"
                "  • Results: main findings with key numerical data\n"
                "    (n, percentages, key p-values or 95% CI).\n"
                "  • Conclusions: main clinical or scientific implication.\n"
                "End with: 3–6 Keywords (preferably from the MeSH/DeCS in Spanish).\n"
            ),
        },
        "abstract_ingles": {
            "title": "Abstract",
            "guidance": (
                "Structured abstract in English. Recommended for international visibility\n"
                "and required for PubMed/Medline if the thesis is adapted for publication.\n"
                "Maximum 350 words. Same structure as the Spanish Abstract:\n"
                "Background, Objective, Methods, Results, Conclusions.\n"
                "Keywords: 3–6 terms from the Medical Subject Headings (MeSH).\n"
            ),
        },
        "agradecimientos": {
            "title": "Acknowledgements",
            "guidance": (
                "Optional. Acknowledge: thesis supervisor and advisor(s), head of the\n"
                "service or department where the research was conducted,\n"
                "study patients or participants (anonymously),\n"
                "funding sources (CONAHCYT, DGAPA-PAPIIT, hospital funds).\n"
                "Include the protocol number if the study was registered with a CLIS\n"
                "(Local Health Research Committee) of IMSS, ISSSTE, etc.\n"
            ),
        },
        "indice": {
            "title": "Table of Contents",
            "guidance": (
                "General table of contents with page numbers. Generated automatically.\n"
                "Health sciences theses in Mexico typically also list\n"
                "the list of tables and list of figures.\n"
            ),
        },
        "indice_tablas": {
            "title": "List of Tables",
            "guidance": (
                "Required if there are 5 or more tables. Generated automatically.\n"
                "Vancouver designates tables as “Table X” — be consistent throughout.\n"
            ),
        },
        "indice_figuras": {
            "title": "List of Figures",
            "guidance": (
                "Required if there are 5 or more figures, images or graphs.\n"
                "Generated automatically. Vancouver: “Figure X” in the text.\n"
            ),
        },
        "introduccion": {
            "title": "Introduction and Background",
            "guidance": (
                "In health sciences, the Introduction and Background are typically\n"
                "a single chapter or adjacent sections. Includes:\n"
                "1. Epidemiological context: prevalence, incidence, disease burden,\n"
                "   relevance in the Mexican and global context.\n"
                "2. Pathophysiology or conceptual framework of the disease/clinical problem.\n"
                "3. State of the art: critical review of the most relevant literature\n"
                "   (last 5–10 years + foundational works).\n"
                "   Vancouver: numerical citations in order of appearance [1], [2].\n"
                "4. Problem statement: what knowledge gap or unresolved clinical problem\n"
                "   justifies this thesis?\n"
                "5. Rationale: clinical, epidemiological or scientific relevance.\n"
                "6. Hypothesis (if applicable to the design).\n"
                "7. General objective and specific objectives.\n"
                "Vancouver: the first citation of a source takes its number; if cited again,\n"
                "use the same original number.\n"
                "Typical length: 15–30 pages.\n"
            ),
        },
        "planteamiento": {
            "title": "Theoretical Framework",
            "guidance": (
                "Optional. For basic science or biomedical theses with a relevant theoretical\n"
                "component (biochemistry, pharmacology, genetics, biostatistics).\n"
                "Develops the theoretical foundations of the biological model, molecular\n"
                "mechanism, or analytical methodology underpinning the thesis.\n"
                "In many clinical theses this content is integrated into the Introduction.\n"
            ),
        },
        "materiales_metodos": {
            "title": "Materials and Methods",
            "guidance": (
                "Critical section for reproducibility. ICMJE structure:\n"
                "• Study design: observational (cohort, case-control, cross-sectional),\n"
                "  experimental (RCT, pre-post, time series), or qualitative.\n"
                "  Justify the choice.\n"
                "• Setting and period: hospital, clinic, laboratory; start and\n"
                "  end dates of data collection.\n"
                "• Population: inclusion and exclusion criteria, operational definition\n"
                "  of cases.\n"
                "• Sample: sample size calculated with an explicit formula, confidence\n"
                "  level, power and parameters used. Sampling type.\n"
                "• Variables: operational definition, type (continuous/discrete\n"
                "  quantitative, nominal/ordinal qualitative) and units of measurement.\n"
                "• Intervention or exposure (if applicable): precise and reproducible description.\n"
                "• Instruments and techniques: validated or standardized with their references.\n"
                "• Statistical analysis: software (SPSS, Stata, R, MedCalc, GraphPad),\n"
                "  statistical tests with justification (parametric/non-parametric),\n"
                "  significance level (generally α = 0.05).\n"
                "• Ethical considerations: Ethics and Research Committee (CEI) registration\n"
                "  number, COFEPRIS registration if applicable,\n"
                "  ClinicalTrials.gov registration (if RCT), informed consent.\n"
                "Typical length: 10–20 pages.\n"
            ),
        },
        "resultados": {
            "title": "Results",
            "guidance": (
                "Present findings objectively and in order, without interpretation.\n"
                "• Begin with sociodemographic characteristics of the population\n"
                "  (Table 1 with baseline characteristics).\n"
                "• Report results in the order of the specific objectives.\n"
                "• Quantitative: report mean ± SD or median (IQR) according to distribution;\n"
                "  comparisons with statistic, p-value and effect size; 95% CI.\n"
                "  Use tables for extensive numerical data and figures for trends.\n"
                "• Qualitative: present thematic categories with representative verbatims.\n"
                "• All tables and figures must be numbered sequentially and\n"
                "  referenced in the text before they appear.\n"
                "• Vancouver: each table has a brief title above; each figure has\n"
                "  a detailed legend below.\n"
                "Typical length: 15–40 pages.\n"
            ),
        },
        "discusion": {
            "title": "Discussion",
            "guidance": (
                "The discussion interprets results in the context of the literature.\n"
                "ICMJE recommended structure for biomedical discussions:\n"
                "1. Summary of the main finding (first sentence of the discussion).\n"
                "2. Comparison with similar studies: do they confirm, contradict or nuance\n"
                "   your results? What explains discrepancies?\n"
                "3. Proposed mechanisms: how do you biologically or clinically explain\n"
                "   the observed findings?\n"
                "4. Clinical implications: what changes in medical practice?\n"
                "   (Be conservative — avoid claims not supported by evidence.)\n"
                "5. Study limitations: selection bias, information bias, residual confounding,\n"
                "   sample size, generalizability.\n"
                "   Be specific and honest — reviewers and committees always look for them.\n"
                "6. Strengths of the study.\n"
                "7. Future research: questions that remain unanswered.\n"
                "Typical length: 15–30 pages.\n"
            ),
        },
        "conclusiones": {
            "title": "Conclusions",
            "guidance": (
                "Conclusions directly answer the specific objectives.\n"
                "Each conclusion must:\n"
                "• Derive directly from the results (no unsupported inferences).\n"
                "• Be written in declarative affirmative or negative language.\n"
                "• Include the level of certainty if applicable (e.g., results suggest,\n"
                "  it was demonstrated, no significant difference was found).\n"
                "Avoid concluding beyond what the data allow.\n"
                "Briefly add practical or public health recommendations\n"
                "if the evidence justifies it.\n"
                "Typical length: 1–5 pages (health science conclusions tend to be\n"
                "more concise than in social sciences).\n"
            ),
        },
        "referencias": {
            "title": "References",
            "guidance": (
                "Vancouver style (ICMJE): numbered in order of first appearance in the text.\n"
                "Generated automatically from your .bib file by biber/biblatex-vancouver.\n"
                "Standard entry format:\n"
                "• Article: Last N, Last N. Article title.\n"
                "  Abbreviated J Name. year;vol(num):pp–pp. DOI or PMID.\n"
                "• Book: Last N. Title. City: Publisher; year. p. pp.\n"
                "• Chapter: Last N. Chapter title. In: Editor A, editor.\n"
                "  Book title. City: Publisher; year. p. pp–pp.\n"
                "Journal abbreviations: use the Index Medicus / PubMed list.\n"
                "DOI mandatory when available; if not, URL + access date.\n"
                "ICMJE recommended maximum for articles: 30–40 refs.\n"
                "Theses: no strict limit; typically 60–150 references.\n"
            ),
        },
        "apendices": {
            "title": "Appendices",
            "guidance": (
                "Supplementary materials:\n"
                "• Ethics and Research Committee opinion.\n"
                "• Informed consent form (final approved version).\n"
                "• Data collection instruments: questionnaires, scales, capture forms.\n"
                "• ClinicalTrials.gov registration or equivalent (if applicable).\n"
                "• Extended data tables or sensitivity analysis results.\n"
                "• Authorization from the institution where the study was conducted.\n"
                "Label: Appendix A, B… with descriptive title.\n"
            ),
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# es_ucm_apa7
# ══════════════════════════════════════════════════════════════════════════════
"es_ucm_apa7": {
    "verified_by": "TeXisStudio Community — reviewed against UCM Doctoral Regulation and EDCM guidelines",
    "sections": {
        "portada": {
            "title": "Title Page",
            "guidance": (
                "The official UCM title page must include:\n"
                "• Logo of the Universidad Complutense de Madrid.\n"
                "• Name of the Faculty or Department.\n"
                "• Full title of the doctoral thesis.\n"
                "• \"DOCTORAL THESIS\" (in uppercase).\n"
                "• \"submitted by [Author’s name].\"\n"
                "• \"supervised by [Dr./Dra. Director’s name].\"\n"
                "• \"to obtain the degree of Doctor by the Universidad Complutense de Madrid.\"\n"
                "• Madrid, [Year].\n"
                "The Doctoral School (EDCM) may have a standardized format —\n"
                "download the template from the EDCM portal.\n"
            ),
        },
        "declaracion": {
            "title": "Authorship and Originality Statement",
            "guidance": (
                "UCM requires an Authorship and Originality Statement in accordance\n"
                "with Article 9 of the UCM Doctoral Regulation.\n"
                "Standard text: \"Mr./Ms. [name], with ID/NIE [number], declare that\n"
                "this doctoral thesis is my own work, original and unpublished,\n"
                "that it has not been submitted to any other institution, and that\n"
                "the results are truthful.\"\n"
                "The thesis supervisor’s signature may also be required.\n"
            ),
        },
        "resumen": {
            "title": "Abstract",
            "guidance": (
                "Abstract in Spanish, 200–350 words.\n"
                "Problem, objectives, methodology, results and conclusions.\n"
                "Keywords (4–6).\n"
            ),
        },
        "abstract_ingles": {
            "title": "Abstract",
            "guidance": (
                "UCM requires an English abstract for doctoral theses.\n"
                "Maximum 350 words. Same structure as the Spanish Abstract.\n"
                "Keywords (4–6). Required for deposit in TESEO and the\n"
                "UCM Library database.\n"
            ),
        },
        "agradecimientos": {
            "title": "Acknowledgements",
            "guidance": (
                "Acknowledge the thesis supervisor, committee, grants (FPI, FPU,\n"
                "UCM predoctoral contract) and Ministry (PID, PIE) or\n"
                "Community of Madrid (PRICIT) research projects with the project reference.\n"
            ),
        },
        "indice": {
            "title": "Table of Contents",
            "guidance": "Generated automatically. Required by the EDCM.",
        },
        "indice_figuras": {
            "title": "List of Figures",
            "guidance": "Enable if you have 5 or more figures.",
        },
        "indice_tablas": {
            "title": "List of Tables",
            "guidance": "Enable if you have 5 or more tables.",
        },
        "introduccion": {
            "title": "Introduction",
            "guidance": (
                "Contextualization, problem statement, rationale,\n"
                "research questions, objectives, hypotheses and structure.\n"
                "APA 7: (Author, year) in the text.\n"
                "UCM requires the introduction to demonstrate mastery of the field.\n"
            ),
        },
        "marco_teorico": {
            "title": "Theoretical Framework and Literature Review",
            "guidance": (
                "Critical review of the literature and theoretical foundations.\n"
                "Organize by theoretical currents or debates — not chronologically.\n"
                "Identify the gap that justifies the thesis.\n"
            ),
        },
        "metodologia": {
            "title": "Methodology",
            "guidance": (
                "Research design, sample, instruments, procedure, analysis and ethics.\n"
                "If the research involves human subjects: approval from the\n"
                "Research Ethics Committee (CEISH-UCM or equivalent).\n"
            ),
        },
        "resultados": {
            "title": "Results",
            "guidance": "Objective findings. APA 7 tables and figures. No interpretation.",
        },
        "discusion": {
            "title": "Discussion",
            "guidance": "Interpretation, comparison with literature, implications and limitations.",
        },
        "conclusiones": {
            "title": "Conclusions",
            "guidance": (
                "Answer research questions, summarize contributions, note\n"
                "limitations and propose future research.\n"
                "UCM may require separate “Conclusions” and “Discussion” chapters —\n"
                "verify with your supervisor and your program’s regulations.\n"
            ),
        },
        "referencias": {
            "title": "References",
            "guidance": (
                "APA 7th edition, alphabetical list, hanging indent.\n"
                "Generated automatically. Include DOI when available.\n"
                "The EDCM may require references in a final chapter with continuous\n"
                "numbering — verify your program’s requirements.\n"
            ),
        },
        "apendices": {
            "title": "Appendices",
            "guidance": (
                "Instruments, additional data, ethics statements,\n"
                "publications derived from the thesis (if submitted as a compendium).\n"
                "Compendium-format theses (frequent modality at UCM)\n"
                "require including published articles in appendices or chapters.\n"
            ),
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# generic_especialidad
# ══════════════════════════════════════════════════════════════════════════════
"generic_especialidad": {
    "sections": {
        "portada": {
            "title": "Title Page",
            "guidance": (
                "Include institution, specialty program name, work title,\n"
                "author, advisor, city and date. If your hospital, professional college\n"
                "or program has an official format, use it as the source of truth.\n"
            ),
        },
        "resumen": {
            "title": "Abstract",
            "guidance": (
                "Summarizes the professional problem addressed, the context, the intervention\n"
                "or analysis strategy, the main results and the practical utility of the work.\n"
                "Suggested length: 150–300 words.\n"
            ),
        },
        "indice": {
            "title": "Table of Contents",
            "guidance": (
                "Generated automatically. Review the final pagination before submission.\n"
            ),
        },
        "introduccion": {
            "title": "Introduction",
            "guidance": (
                "Presents the professional or clinical problem, the institutional context,\n"
                "the relevance of the work and the document’s objectives.\n"
            ),
        },
        "marco_referencial": {
            "title": "Reference Framework",
            "guidance": (
                "Synthesizes the regulations, prior evidence, protocols, clinical guidelines\n"
                "or literature that underpin the adopted approach.\n"
            ),
        },
        "metodologia": {
            "title": "Methodology / Intervention",
            "guidance": (
                "Describes the work design, procedure, selection criteria,\n"
                "instruments, applied intervention or strategy, and ethical considerations.\n"
            ),
        },
        "resultados": {
            "title": "Results",
            "guidance": (
                "Presents the findings, products, metrics, evaluations or observed results\n"
                "of the specialty work.\n"
            ),
        },
        "discusion": {
            "title": "Discussion",
            "guidance": (
                "Interprets the results, compares them with literature or standards,\n"
                "acknowledges limitations and highlights practical implications.\n"
            ),
        },
        "conclusiones": {
            "title": "Conclusions and Recommendations",
            "guidance": (
                "Summarizes the professional contribution of the work, its applied utility\n"
                "and recommendations for continuity or improvement.\n"
            ),
        },
        "referencias": {
            "title": "References",
            "guidance": (
                "Final reference list in APA 7. Include only cited sources.\n"
            ),
        },
        "anexos": {
            "title": "Annexes",
            "guidance": (
                "Supplementary material: instruments, protocols, forms, extended tables\n"
                "or supporting technical documentation.\n"
            ),
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# generic_posdoctorado
# ══════════════════════════════════════════════════════════════════════════════
"generic_posdoctorado": {
    "sections": {
        "portada": {
            "title": "Title Page",
            "guidance": (
                "Include the host institution, postdoctoral project or fellowship,\n"
                "report or monograph title, principal investigator, mentor\n"
                "or supervisor, venue and date.\n"
            ),
        },
        "resumen": {
            "title": "Abstract",
            "guidance": (
                "Synthesizes the postdoctoral agenda, objectives, methodological approach,\n"
                "contributions, results and future projections.\n"
                "Suggested length: 200–350 words.\n"
            ),
        },
        "abstract_ingles": {
            "title": "Abstract (English)",
            "guidance": (
                "Recommended when the postdoctoral report will circulate internationally\n"
                "or will be reported to an external funding call.\n"
            ),
        },
        "indice": {
            "title": "Table of Contents",
            "guidance": (
                "Generated automatically. Review final pagination consistency.\n"
            ),
        },
        "introduccion": {
            "title": "Introduction",
            "guidance": (
                "Presents the research field, the project agenda and the\n"
                "positioning of the work within the postdoctoral line of research.\n"
            ),
        },
        "estado_arte": {
            "title": "State of the Art",
            "guidance": (
                "Develops a critical review of the current state of the field,\n"
                "identifies gaps and justifies the contribution of the postdoctoral work.\n"
            ),
        },
        "metodologia": {
            "title": "Methodology",
            "guidance": (
                "Explains design, corpus or data, procedures, protocols, tools,\n"
                "reproducibility and ethical considerations as applicable.\n"
            ),
        },
        "resultados": {
            "title": "Results",
            "guidance": (
                "Presents results, academic outputs, prototypes, articles,\n"
                "datasets or verifiable advances obtained during the fellowship.\n"
            ),
        },
        "discusion": {
            "title": "Discussion",
            "guidance": (
                "Interprets the scope of the results, their novelty, limitations,\n"
                "and relationship to the state of the art.\n"
            ),
        },
        "conclusiones": {
            "title": "Conclusions",
            "guidance": (
                "Summarizes the contributions of the postdoctoral work and its scientific,\n"
                "methodological or applied impact.\n"
            ),
        },
        "referencias": {
            "title": "References",
            "guidance": (
                "Final list of cited references, in APA 7 format.\n"
            ),
        },
        "anexos": {
            "title": "Annexes",
            "guidance": (
                "Supporting evidence: instruments, extended tables, protocols,\n"
                "outputs, technical documentation or supplementary material.\n"
            ),
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# generic_tesina
# ══════════════════════════════════════════════════════════════════════════════
"generic_tesina": {
    "sections": {
        "portada": {
            "title": "Title Page",
            "guidance": (
                "The title page must include:\n"
                "• Logo and name of the institution, faculty or school.\n"
                "• Full title of the tesina (clear and specific).\n"
                "• \"TESINA\" and the degree or certificate sought\n"
                "  (e.g., \"to obtain the title of Bachelor in [field]\").\n"
                "• Author’s full name.\n"
                "• Advisor’s or director’s name.\n"
                "• City, month and year.\n"
                "Consult the official title page format of your program.\n"
            ),
        },
        "resumen": {
            "title": "Abstract",
            "guidance": (
                "Brief abstract of the tesina. 150–300 words.\n"
                "Includes: the topic, the objective, the method used, the main\n"
                "findings and the central conclusion or contribution.\n"
                "End with 4–6 Keywords.\n"
                "No citations, no figures, no undefined acronyms.\n"
            ),
        },
        "agradecimientos": {
            "title": "Acknowledgements",
            "guidance": (
                "Optional. Thank your advisor, those who provided access to data\n"
                "or information, and personal support received.\n"
                "Typical length: one paragraph or half a page.\n"
            ),
        },
        "indice": {
            "title": "Table of Contents",
            "guidance": (
                "Generated automatically. Includes all chapters and sections\n"
                "with their page numbers.\n"
            ),
        },
        "introduccion": {
            "title": "Introduction",
            "guidance": (
                "The introduction situates the topic and justifies the work.\n"
                "Includes:\n"
                "1. Topic presentation: what is the tesina about?\n"
                "2. Relevance: why is this topic important?\n"
                "3. Central question or purpose of the work.\n"
                "4. Objective(s) of the study.\n"
                "5. Brief description of the tesina’s structure.\n"
                "Typical length: 3–8 pages.\n"
            ),
        },
        "desarrollo": {
            "title": "Development",
            "guidance": (
                "The development is the main body of the tesina. You can structure it\n"
                "in the following ways depending on the type of work:\n"
                "Theoretical tesina / academic essay:\n"
                "  • Review and critical analysis of the relevant literature.\n"
                "  • Development of the central argument or position with bibliographic support.\n"
                "  • Discussion of different perspectives or approaches.\n"
                "Empirical research tesina (small scale):\n"
                "  • Brief theoretical framework.\n"
                "  • Methodology: design, sample, instruments, procedure.\n"
                "  • Results and analysis.\n"
                "  • Discussion of findings.\n"
                "Design or project tesina:\n"
                "  • Diagnosis or problem justification.\n"
                "  • Intervention or design proposal.\n"
                "  • Evaluation or validation.\n"
                "Divide this chapter into sections with clear subheadings.\n"
                "APA 7: cite with (Author, year) or Author (year).\n"
                "Typical length: 25–60 pages.\n"
            ),
        },
        "conclusiones": {
            "title": "Conclusions",
            "guidance": (
                "Conclusions synthesize what you learned or demonstrated.\n"
                "• Answer the central question or purpose of the tesina.\n"
                "• Summarize the main points of the development.\n"
                "• Note implications or applications.\n"
                "• Acknowledge the work’s limitations.\n"
                "• Suggest possible future lines of work or further study.\n"
                "Typical length: 3–8 pages.\n"
                "Avoid introducing new information not discussed previously.\n"
            ),
        },
        "referencias": {
            "title": "References",
            "guidance": (
                "APA 7th edition: alphabetical list, hanging indent.\n"
                "Include only sources cited in the text.\n"
                "Generated automatically from your .bib file.\n"
                "Include DOI when available.\n"
            ),
        },
        "apendices": {
            "title": "Appendices",
            "guidance": (
                "Optional. Additional supporting materials:\n"
                "• Data collection instruments (if used).\n"
                "• Extended data tables.\n"
                "• Additional analysis materials.\n"
                "Label: Appendix A, B… Reference from the text.\n"
            ),
        },
    },
},

# ══════════════════════════════════════════════════════════════════════════════
# generic_thesis
# ══════════════════════════════════════════════════════════════════════════════
"generic_thesis": {
    "sections": {
        "portada": {
            "title": "Title Page",
            "guidance": (
                "The title page is the first impression of your thesis. Includes:\n"
                "• Logo and name of your institution (university / faculty / department).\n"
                "• Full thesis title (informative and specific, no abbreviations).\n"
                "• Document type: \"THESIS\" or \"DISSERTATION\" and the degree sought\n"
                "  (e.g., \"to obtain the degree of Bachelor’s in / Master’s in /\n"
                "  Doctor’s in [field name]\").\n"
                "• Author’s full name.\n"
                "• Name of the thesis supervisor or director.\n"
                "• City, month and year of submission.\n"
                "Check with your coordinator or program — many institutions have\n"
                "an official title page format you must follow exactly.\n"
            ),
        },
        "declaracion": {
            "title": "Authenticity Declaration",
            "guidance": (
                "The Authenticity Declaration certifies that the work is yours and that\n"
                "sources are correctly cited. Standard text (adapt if your institution\n"
                "has a specific format):\n"
                "\"I declare under oath that this work is original and has been prepared\n"
                "by the undersigned. All sources consulted have been duly cited and\n"
                "referenced according to applicable standards.\"\n"
                "Some universities require this declaration to be signed, notarized,\n"
                "or in a specific format — verify with your program.\n"
            ),
        },
        "resumen": {
            "title": "Abstract",
            "guidance": (
                "The Spanish abstract is the first academic element other researchers will read.\n"
                "Recommended: 150–350 words.\n"
                "APA 7 (for theses and student papers) recommends including:\n"
                "  1. The research problem (1–2 sentences).\n"
                "  2. Participants or data used (if applicable).\n"
                "  3. The methodology or approach used.\n"
                "  4. The main findings or conclusions.\n"
                "  5. Implications or contributions of the study.\n"
                "End with 4–6 Keywords separated by semicolons.\n"
                "Must be self-contained: no citations, no figures, no undefined acronyms.\n"
            ),
        },
        "abstract_ingles": {
            "title": "Abstract",
            "guidance": (
                "Abstract in English. Optional but recommended for international visibility.\n"
                "Maximum 350 words. Same structure as the Spanish Abstract.\n"
                "End with: Keywords: (4–6 terms in English).\n"
                "Mandatory if your program requires publication in international databases\n"
                "(Scopus, Web of Science, ProQuest Dissertations & Theses).\n"
            ),
        },
        "agradecimientos": {
            "title": "Acknowledgements",
            "guidance": (
                "Optional but conventional section. Acknowledge those who contributed\n"
                "to your research: thesis supervisor, committee or jury, colleagues,\n"
                "librarians, study participants, and those who supported you\n"
                "personally throughout the process.\n"
                "If your research was funded with a scholarship or external resource\n"
                "(CONAHCYT, CONACYT, DGAPA, etc.), it is mandatory to mention it with\n"
                "the project or scholarship number.\n"
                "Typical length: half to one page.\n"
            ),
        },
        "dedicatoria": {
            "title": "Dedication",
            "guidance": (
                "Optional. One to three lines. No printed heading.\n"
            ),
        },
        "indice": {
            "title": "Table of Contents",
            "guidance": (
                "Generated automatically. Includes all front matter (except the title page),\n"
                "body chapters, appendices and references.\n"
                "Verify that page numbers are exact before printing.\n"
            ),
        },
        "indice_figuras": {
            "title": "List of Figures",
            "guidance": (
                "Enable this section if your thesis has 5 or more figures, graphs or images.\n"
                "APA 7: number figures continuously (Figure 1, Figure 2…)\n"
                "and reference them in the text before they appear.\n"
            ),
        },
        "indice_tablas": {
            "title": "List of Tables",
            "guidance": (
                "Enable if you have 5 or more tables. APA 7: number tables continuously\n"
                "(Table 1, Table 2…) and reference them in the text.\n"
            ),
        },
        "introduccion": {
            "title": "Introduction",
            "guidance": (
                "The introduction frames your research and convinces the reader of its importance.\n"
                "Recommended structure:\n"
                "1. General contextualization of the research topic.\n"
                "2. Problem statement: what knowledge gap, contradiction\n"
                "   or practical need does your thesis address?\n"
                "3. Rationale: why does it matter to resolve it? (theoretical, social,\n"
                "   economic, clinical, technological relevance, etc.)\n"
                "4. Research question(s): stated precisely and narrowly.\n"
                "5. General objective and specific objectives (concrete and measurable).\n"
                "6. Hypothesis or working assumption (if your design requires it).\n"
                "7. Scope and delimitations of the study.\n"
                "8. Thesis structure: a brief paragraph per chapter.\n"
                "Typical length for undergraduate: 10–20 pages.\n"
                "For graduate: 15–30 pages.\n"
            ),
        },
        "marco_teorico": {
            "title": "Theoretical Framework and Literature Review",
            "guidance": (
                "The theoretical framework is the conceptual foundation of your research. Includes:\n"
                "• Definition and discussion of the fundamental concepts and theories\n"
                "  that underpin your work.\n"
                "• Critical review of the literature: what is known about the topic?\n"
                "  What are the main approaches? Where are the debates?\n"
                "• Identification of the gap or contradiction that justifies your study.\n"
                "• Theoretical positioning: what perspective do you adopt and why?\n"
                "APA 7: cite with (Author, year) or Author (year) for narrative citations.\n"
                "For direct quotations include page number: (Author, year, p. xx).\n"
                "Organize by topics or currents, not as a list of authors.\n"
                "Typical length: 20–50 pages.\n"
            ),
        },
        "metodologia": {
            "title": "Methodology",
            "guidance": (
                "The methodology describes in sufficient detail how you conducted your research.\n"
                "Includes:\n"
                "• Approach: quantitative, qualitative or mixed. Justify the choice.\n"
                "• Research design: experimental, quasi-experimental, correlational,\n"
                "  descriptive, phenomenological, case study, etc.\n"
                "• Population and sample (or analysis corpus): selection criteria and size.\n"
                "• Data collection instruments or techniques: describe each one,\n"
                "  cite the instrument if published, and indicate if it was adapted or created.\n"
                "• Data collection procedure: when, where and how data were obtained.\n"
                "• Data analysis: software used and analysis techniques.\n"
                "• Ethical considerations: informed consent, confidentiality,\n"
                "  Ethics Committee approval if human subjects were involved.\n"
                "• Methodological limitations.\n"
                "Typical length: 10–25 pages.\n"
            ),
        },
        "resultados": {
            "title": "Results",
            "guidance": (
                "Present findings objectively, without interpretation or conclusions.\n"
                "Organize results according to your research questions or objectives.\n"
                "For quantitative data:\n"
                "• Report descriptive statistics first (means, standard deviations, percentages).\n"
                "• Then inferential tests (t, F, χ², correlations, regressions) with\n"
                "  their statistics, p-values and effect sizes.\n"
                "• Include APA 7 tables and figures with footnotes.\n"
                "For qualitative data:\n"
                "• Present emerging categories or themes with representative verbatim quotes.\n"
                "• Ensure participant confidentiality.\n"
                "APA 7: “Table 1 shows…”, “Figure 2 illustrates…”.\n"
                "Every table and figure must be mentioned in the text before it appears.\n"
            ),
        },
        "discusion": {
            "title": "Discussion",
            "guidance": (
                "The discussion interprets results and connects them to the theoretical\n"
                "framework and reviewed literature.\n"
                "Recommended structure:\n"
                "• First sentence: restate the research question and answer it directly\n"
                "  based on your results.\n"
                "• Compare with prior studies: do your findings agree with, contradict or\n"
                "  nuance existing literature? Why?\n"
                "• Explain unexpected results.\n"
                "• Theoretical and practical implications of the findings.\n"
                "• Study limitations.\n"
                "• Specific future research suggestions.\n"
                "In many undergraduate theses this chapter is merged with Results\n"
                "or Conclusions. Activate as an independent chapter if needed.\n"
            ),
        },
        "conclusiones": {
            "title": "Conclusions",
            "guidance": (
                "Conclusions directly answer your research question(s) and objectives.\n"
                "• Answer each research question or verify each hypothesis.\n"
                "• Summarize the original contributions of your work to the field.\n"
                "• Practical implications or possible applications.\n"
                "• Study limitations (be honest — the committee will find them regardless).\n"
                "• Future research directions: concrete and bounded.\n"
                "Do not repeat results — the committee has already read that chapter.\n"
                "Typical length: 5–15 pages.\n"
            ),
        },
        "referencias": {
            "title": "References",
            "guidance": (
                "APA 7th edition: alphabetical list by first author’s last name,\n"
                "hanging indent. Generated automatically from your .bib file.\n"
                "Key APA 7 points:\n"
                "• Italics for book, journal and thesis titles.\n"
                "• No italics for articles and chapters.\n"
                "• DOI in URL format: https://doi.org/xxxxx (no trailing period).\n"
                "• For online sources: URL and access date.\n"
                "• Thesis: Last, N. (Year). Title [Bachelor’s/Master’s/doctoral thesis,\n"
                "  University Name]. Repository or database.\n"
                "Include only sources cited in the body text.\n"
            ),
        },
        "apendices": {
            "title": "Appendices",
            "guidance": (
                "Supplementary materials too extensive for the main body\n"
                "or that would disrupt the narrative flow:\n"
                "• Complete instruments (questionnaires, scales, interview guides).\n"
                "• Raw data or additional statistical tables.\n"
                "• Interview or focus group transcripts.\n"
                "• Ethics approval letters and informed consent forms.\n"
                "• Stimulus materials or intervention protocols.\n"
                "Label: Appendix A, B… with descriptive title.\n"
                "Reference from the text: \"(see Appendix A)\".\n"
            ),
        },
    },
},

}  # end TRANSLATIONS


# ─────────────────────────────────────────────────────────────────────────────
# Helper: update en.json
# ─────────────────────────────────────────────────────────────────────────────

def update_en_json():
    en_path = BASE / "i18n" / "en.json"
    with open(en_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    profiles = data["profiles"]

    for profile_id, trans in TRANSLATIONS.items():
        if profile_id not in profiles:
            print(f"  [WARN] {profile_id} not found in en.json — skipping")
            continue

        prof = profiles[profile_id]
        if "sections" not in prof:
            prof["sections"] = {}

        sec_trans = trans.get("sections", {})
        for sec_id, sec_data in sec_trans.items():
            if sec_id not in prof["sections"]:
                prof["sections"][sec_id] = {}
            sec = prof["sections"][sec_id]
            sec["title"] = sec_data["title"]
            if "guidance" in sec_data:
                sec["guidance"] = sec_data["guidance"].rstrip("\n")
            if "label" in sec_data:
                sec["label"] = sec_data["label"]

        print(f"  [OK] Updated en.json sections for {profile_id}")

    with open(en_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\nen.json written: {en_path}")


# ─────────────────────────────────────────────────────────────────────────────
# Helper: update YAML files
# We do a targeted regex replacement of title/guidance within each section.
# Approach: read raw text, replace field-by-field using pattern matching.
# ─────────────────────────────────────────────────────────────────────────────

def yaml_scalar(value):
    """Return a YAML representation of a string value."""
    if "\n" in value:
        # Use literal block scalar
        lines = value.rstrip("\n").split("\n")
        indented = "\n".join("      " + line for line in lines)
        return "|\n" + indented + "\n"
    else:
        # Simple quoted string
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'


def update_yaml_file(yaml_path, profile_id):
    """
    Update title and guidance fields in a YAML file.
    Uses line-by-line processing to preserve comments and structure.
    """
    trans = TRANSLATIONS.get(profile_id, {})
    sec_trans = trans.get("sections", {})
    verified_by = trans.get("verified_by")

    with open(yaml_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update verified_by if specified
    if verified_by:
        content = re.sub(
            r'(  verified_by:\s*)"[^"]*"',
            f'  verified_by: "{verified_by}"',
            content,
        )

    # 2. For each section, replace title and guidance
    # We find each section block by its `- id: <sec_id>` marker and replace
    # the title and guidance within it.

    for sec_id, sec_data in sec_trans.items():
        new_title = sec_data.get("title")
        new_guidance = sec_data.get("guidance")

        # Find the section block starting with `  - id: <sec_id>`
        # The block ends at the next `  - id:` or end of sections
        # We use a regex that captures the section block
        sec_pattern = re.compile(
            r'(  - id: ' + re.escape(sec_id) + r'\b.*?)(?=  - id: |\Z)',
            re.DOTALL
        )

        def replace_section(m):
            block = m.group(1)
            original_block = block

            # Replace title
            if new_title is not None:
                block = re.sub(
                    r'(    title:\s*).*',
                    lambda tm: '    title: "' + new_title.replace('"', '\\"') + '"',
                    block,
                    count=1
                )

            # Replace guidance (block scalar or inline)
            if new_guidance is not None:
                # Check if guidance exists at all
                if re.search(r'    guidance:', block):
                    def _replace_guidance(gm, _new_guidance=new_guidance):
                        matched = gm.group(0)
                        # Preserve trailing whitespace/newlines from the original match
                        trail_m = re.search(r'\s+$', matched)
                        trailing_ws = trail_m.group(0) if trail_m else ""
                        if "\n" in _new_guidance:
                            lines = _new_guidance.rstrip("\n").split("\n")
                            indented_lines = "\n".join("      " + line for line in lines)
                            replacement = "    guidance: |\n" + indented_lines
                        else:
                            replacement = '    guidance: "' + _new_guidance.replace('"', '\\"') + '"'
                        return replacement + trailing_ws

                    block = re.sub(
                        r'    guidance:.*?(?=\n    [a-z_]|\n  - |\Z)',
                        _replace_guidance,
                        block,
                        count=1,
                        flags=re.DOTALL
                    )

            return block

        content = sec_pattern.sub(replace_section, content)

    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(content)


# ─────────────────────────────────────────────────────────────────────────────
# Profile paths mapping
# ─────────────────────────────────────────────────────────────────────────────

PROFILES = {
    "ar_uba_apa7":          "america/argentina/uba/apa7/profile.yaml",
    "br_unicamp_abnt":      "america/brazil/unicamp/abnt/profile.yaml",
    "br_usp_abnt":          "america/brazil/usp/abnt/profile.yaml",
    "cl_uchile_apa7":       "america/chile/uchile/apa7/profile.yaml",
    "mx_ipn_apa7":          "america/mexico/ipn/apa7/profile.yaml",
    "mx_tec_apa7":          "america/mexico/tec/apa7/profile.yaml",
    "mx_uam_azc_cbi":       "america/mexico/uam/azc-cbi/profile.yaml",
    "mx_uam_azc_dcsh":      "america/mexico/uam/azc-dcsh/profile.yaml",
    "mx_uam_cua_dci":       "america/mexico/uam/cua-dci/profile.yaml",
    "mx_uam_izt_cbi":       "america/mexico/uam/izt-cbi/profile.yaml",
    "mx_uam_izt_dcsh":      "america/mexico/uam/izt-dcsh/profile.yaml",
    "mx_uam_xoc_dcbs":      "america/mexico/uam/xoc-dcbs/profile.yaml",
    "mx_uanl_apa7":         "america/mexico/uanl/apa7/profile.yaml",
    "mx_udg_apa7":          "america/mexico/udg/apa7/profile.yaml",
    "mx_unam_apa7":         "america/mexico/unam/apa7/profile.yaml",
    "mx_unam_vancouver":    "america/mexico/unam/vancouver/profile.yaml",
    "es_ucm_apa7":          "europe/spain/ucm/apa7/profile.yaml",
    "generic_especialidad": "generic/generic/generic/especialidad/profile.yaml",
    "generic_posdoctorado": "generic/generic/generic/posdoctorado/profile.yaml",
    "generic_tesina":       "generic/generic/generic/tesina/profile.yaml",
    "generic_thesis":       "generic/generic/generic/thesis/profile.yaml",
}


def update_all_yamls():
    for profile_id, rel_path in PROFILES.items():
        yaml_path = BASE / rel_path
        if not yaml_path.exists():
            print(f"  [WARN] File not found: {yaml_path}")
            continue
        update_yaml_file(yaml_path, profile_id)
        print(f"  [OK] Updated YAML: {rel_path}")


# ─────────────────────────────────────────────────────────────────────────────
# Verification
# ─────────────────────────────────────────────────────────────────────────────

SPANISH_INDICATORS = [
    'Portada', 'Índice', 'Introducción', 'Metodología', 'Conclusiones',
    'Agradecimientos', 'Resumen', 'Referencias', 'Apéndices', 'Discusión',
    'Marco Teórico', 'Resultados', 'Dedicatoria', 'Declaración',
    'revisado contra', 'Generado automáticamente', 'Activa si tienes',
]

def verify():
    print("\n=== Verification ===")
    issues = []

    for profile_id, rel_path in PROFILES.items():
        yaml_path = BASE / rel_path
        if not yaml_path.exists():
            continue
        with open(yaml_path, "r", encoding="utf-8") as f:
            content = f.read()

        for indicator in SPANISH_INDICATORS:
            if indicator in content:
                # Only flag if it's in a title or guidance field
                # Look for the indicator in value context
                for line in content.split("\n"):
                    if indicator in line and ("title:" in line or "guidance:" in line or "verified_by:" in line):
                        issues.append(f"  [WARN] {profile_id}: '{indicator}' found in: {line.strip()[:80]}")
                        break

    if issues:
        print("Potential Spanish text remaining:")
        for i in issues:
            print(i)
    else:
        print("No Spanish indicators found in title/guidance/verified_by fields.")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Step 1: Updating YAML files...")
    update_all_yamls()

    print("\nStep 2: Updating en.json...")
    update_en_json()

    verify()
    print("\nDone.")
