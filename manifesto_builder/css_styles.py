# -*- coding: utf-8 -*-
import os

_css_path = os.path.join(os.path.dirname(__file__), 'style.css')
with open(_css_path, 'r', encoding='utf-8') as f:
    CSS_CONTENT = f.read()
