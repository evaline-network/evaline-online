#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import shutil

sys.path.append('/home/evabot')
sys.path.append('/home/evabot/manifesto_builder')

import helpers
import css_styles
import nav_and_hero
import sections_01_03
import sections_04_07
import section_08
import section_09
import models_renderer
import footer_and_scripts

print("Starting Master Compilation of EvaLine Manifesto...")

# =========================================================================
# 1. COMPILE INTERACTIVE TRILINGUAL MANIFESTO (Full Cyber UI + Style Toggle)
# =========================================================================
helpers.set_render_lang(None)
prerendered_models_html = models_renderer.get_prerendered_models()

head_html = """<!DOCTYPE html>
<html lang="ru" data-lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Манифест EvaLine // Фабрика автономных ИИ-агентов, система «Консилиум», Тетраксис ролей и производство полимеров EVA</title>
  <meta name="description" content="Технологический манифест EvaLine: фабрика автономных ИИ-агентов, система Консилиум, матрица из 94 LLM моделей, 10 ролей Тетраксиса и реальное производство полимеров EVA.">
  
  <!-- Complete Roboto Font Family: Roboto, Roboto Mono, Roboto Condensed, Roboto Slab (All weights & styles) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&family=Roboto+Condensed:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&family=Roboto+Mono:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&family=Roboto+Slab:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  
  <style id="main-manifesto-styles">
""" + css_styles.CSS_CONTENT + """
  </style>
</head>
<body>
"""

nav_hero = nav_and_hero.get_nav_and_hero()
sec1 = sections_01_03.get_section_01()
sec2 = sections_01_03.get_section_02()
sec3 = sections_01_03.get_section_03()
sec4 = sections_04_07.get_section_04(prerendered_models_html)
sec5 = sections_04_07.get_section_05()
sec6 = sections_04_07.get_section_06()
sec7 = sections_04_07.get_section_07()
sec8 = section_08.get_section_08()
sec9 = section_09.get_section_09()
footer = footer_and_scripts.get_footer()
scripts = footer_and_scripts.get_scripts()

full_interactive_html = head_html + nav_hero + sec1 + sec2 + sec3 + sec4 + sec5 + sec6 + sec7 + sec8 + sec9 + footer + scripts

# =========================================================================
# 2. COMPILE CLEAN STANDALONE SINGLE-LANGUAGE SEMANTIC HTML (For w3m/lynx & Raw)
# =========================================================================
def compile_clean_html(lang):
    helpers.set_render_lang(lang)
    helpers.set_include_mermaid(False)
    lang_models = models_renderer.get_prerendered_models()
    
    titles = {
        'ru': "Манифест EvaLine // Фабрика ИИ-агентов, Консилиум и Завод полимеров EVA (Текстовая версия)",
        'uk': "Маніфест EvaLine // Фабрика ШІ-агентів, Консиліум та Завод полімерів EVA (Текстова версія)",
        'en': "EvaLine Manifesto // Autonomous AI Factory, Consilium Consensus & EVA Polymer Plant (Text Edition)"
    }
    
    clean_head = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{titles[lang]}</title>
</head>
<body>
"""
    c_nav = nav_and_hero.get_nav_and_hero()
    c_s1 = sections_01_03.get_section_01()
    c_s2 = sections_01_03.get_section_02()
    c_s3 = sections_01_03.get_section_03()
    c_s4 = sections_04_07.get_section_04(lang_models)
    c_s5 = sections_04_07.get_section_05()
    c_s6 = sections_04_07.get_section_06()
    c_s7 = sections_04_07.get_section_07()
    c_s8 = section_08.get_section_08()
    c_s9 = section_09.get_section_09()
    c_foot = footer_and_scripts.get_footer()
    
    clean_html = clean_head + c_nav + c_s1 + c_s2 + c_s3 + c_s4 + c_s5 + c_s6 + c_s7 + c_s8 + c_s9 + c_foot + "\n</body>\n</html>"
    return clean_html

print("Generating single-language clean semantic editions...")
html_ru = compile_clean_html('ru')
html_uk = compile_clean_html('uk')
html_en = compile_clean_html('en')

# Reset helpers back to trilingual and enable mermaid for safety
helpers.set_render_lang(None)
helpers.set_include_mermaid(True)

# =========================================================================
# 3. WRITE TARGET ARTIFACTS TO BACKEND AND REPO
# =========================================================================
file_matrix = [
    # Full Interactive Cyber Web UI
    ('/var/www/evabot-backend/public/manifesto.html', full_interactive_html),
    ('/home/evabot/evaline-online/index.html', full_interactive_html),
    ('/home/evabot/evaline-online/public/manifesto.html', full_interactive_html),

    # Single Language Semantic Russian
    ('/var/www/evabot-backend/public/manifesto-ru.html', html_ru),
    ('/home/evabot/evaline-online/public/manifesto-ru.html', html_ru),

    # Single Language Semantic Ukrainian
    ('/var/www/evabot-backend/public/manifesto-uk.html', html_uk),
    ('/home/evabot/evaline-online/public/manifesto-uk.html', html_uk),

    # Single Language Semantic English
    ('/var/www/evabot-backend/public/manifesto-en.html', html_en),
    ('/home/evabot/evaline-online/public/manifesto-en.html', html_en),

    # Raw Semantic Default (Russian)
    ('/var/www/evabot-backend/public/manifesto-raw.html', html_ru),
    ('/home/evabot/evaline-online/public/manifesto-raw.html', html_ru),
]

for file_path, content in file_matrix:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[+] Wrote {file_path} ({len(content)} bytes)")

# Ensure models_catalog.json is present
with open('/home/evabot/evaline-online/models_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(models_renderer.raw_models, f, ensure_ascii=False, indent=2)
print("[+] Synced models_catalog.json")

# Ensure manifesto.txt is synced across all required spots
txt_source = '/var/www/evabot-backend/public/manifesto.txt'
if os.path.exists(txt_source):
    shutil.copy(txt_source, '/home/evabot/evaline-online/public/manifesto.txt')
    shutil.copy(txt_source, '/home/evabot/evaline-online/manifesto.txt')
    shutil.copy(txt_source, '/var/www/evabot-backend/pages/evaline.online.unui.txt')
    print("[+] Synced manifesto.txt across public, repo root, and pages/")

# Ensure MANIFESTO.md (Markdown export) is available on the web server root
for md_out in ['/var/www/evabot-backend/public/MANIFESTO.md',
               '/home/evabot/evaline-online/public/MANIFESTO.md']:
    try:
        shutil.copy('/home/evabot/evaline-online/MANIFESTO.md', md_out)
    except (OSError, shutil.SameFileError):
        pass
print("[+] Synced MANIFESTO.md to public/")

print("Master Compilation Finished Successfully!")
