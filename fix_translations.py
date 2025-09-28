#!/usr/bin/env python3
"""
Translation fix script for Service PRO
Properly compiles .po files to .mo files
"""

import os
import sys
from babel.messages.pofile import read_po
from babel.messages.mofile import write_mo

def compile_translation_files():
    """Compile .po files to .mo files properly"""
    translations_dir = 'translations'

    if not os.path.exists(translations_dir):
        print("No translations directory found")
        return

    languages = ['et', 'ru']

    for lang in languages:
        po_path = os.path.join(translations_dir, lang, 'LC_MESSAGES', 'messages.po')
        mo_path = os.path.join(translations_dir, lang, 'LC_MESSAGES', 'messages.mo')

        if os.path.exists(po_path):
            try:
                # Read the .po file
                with open(po_path, 'rb') as f:
                    catalog = read_po(f)

                # Write the .mo file
                os.makedirs(os.path.dirname(mo_path), exist_ok=True)
                with open(mo_path, 'wb') as f:
                    write_mo(f, catalog)

                print(f"Compiled translations for {lang}")
            except Exception as e:
                print(f"Error compiling {lang}: {e}")
        else:
            print(f"✗ No translation file found for {lang}")

    print("Translation compilation completed!")

if __name__ == '__main__':
    compile_translation_files()