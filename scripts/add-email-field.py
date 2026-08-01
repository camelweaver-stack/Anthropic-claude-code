#!/usr/bin/env python3
"""Ensure every lead-capture form has a required email input.
Inserts an email field (with a matching <label>) right after the name input
in any <form> that lacks a type=email input. Idempotent."""
import re, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

FORM_RE = re.compile(r'<form\b.*?</form>', re.S)
HAS_EMAIL = re.compile(r'type=["\']email["\']')
NAME_INPUT = re.compile(r'([ \t]*)(<label[^>]*>\s*Name\s*</label>\s*)?(<input[^>]*\bname=["\']name["\'][^>]*>)')
BUTTON = re.compile(r'([ \t]*)<button')

ES = None  # set per file

def email_block(indent, eid, es):
    if es:
        return (f"\n{indent}<label for=\"{eid}\">Correo electrónico</label>"
                f"\n{indent}<input id=\"{eid}\" name=\"email\" type=\"email\" required autocomplete=\"email\">")
    return (f"\n{indent}<label for=\"{eid}\">Email</label>"
            f"\n{indent}<input id=\"{eid}\" name=\"email\" type=\"email\" required autocomplete=\"email\">")

def process(path):
    es = path == 'es' or path.startswith('es/')
    html = open(path, encoding='utf-8').read()
    changed = [0]
    counter = [0]

    def fix_form(m):
        form = m.group(0)
        if HAS_EMAIL.search(form):
            return form
        eid = f"leadmail{counter[0]}"
        counter[0] += 1
        nm = NAME_INPUT.search(form)
        if nm:
            indent = nm.group(1) or '  '
            insert_at = nm.end()
            new = form[:insert_at] + email_block(indent, eid, es) + form[insert_at:]
        else:
            bm = BUTTON.search(form)
            if not bm:
                return form
            indent = bm.group(1) or '  '
            insert_at = bm.start()
            new = form[:insert_at] + email_block(indent, eid, es).lstrip('\n') + '\n' + form[insert_at:]
        changed[0] += 1
        return new

    new_html = FORM_RE.sub(fix_form, html)
    if changed[0]:
        open(path, 'w', encoding='utf-8').write(new_html)
    return changed[0]

total_forms_fixed = 0
files_touched = 0
for f in glob.glob('**/*.html', recursive=True):
    if f.startswith(('node_modules/', 'assets/')):
        continue
    n = process(f)
    if n:
        files_touched += 1
        total_forms_fixed += n
print(f"added required email field to {total_forms_fixed} forms across {files_touched} files")
