#!/usr/bin/env python3
"""Compile Russian translations to .mo file"""

import os
import sys
import subprocess

def compile_russian():
    """Compile Russian .po file to .mo file"""
    po_file = 'translations/ru/LC_MESSAGES/messages.po'
    mo_file = 'translations/ru/LC_MESSAGES/messages.mo'

    if not os.path.exists(po_file):
        print(f"Error: {po_file} not found")
        return False

    try:
        # Try using Babel if available
        result = subprocess.run([
            sys.executable, '-m', 'babel', 'compile',
            '-i', po_file, '-o', mo_file, '-l', 'ru'
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("Successfully compiled Russian translations using Babel")
            return True
        else:
            print(f"Babel compilation failed: {result.stderr}")

            # Try alternative method using Python's polib if available
            try:
                import polib
                po = polib.pofile(po_file)
                po.save_as_mofile(mo_file)
                print("Successfully compiled Russian translations using polib")
                return True
            except ImportError:
                print("polib not available")

                # Manual compilation as last resort
                print("Attempting manual compilation...")
                try:
                    import msgfmt
                    msgfmt.make(po_file, mo_file)
                    print("Successfully compiled Russian translations using msgfmt")
                    return True
                except ImportError:
                    print("msgfmt not available")

    except FileNotFoundError:
        print("Babel not found in PATH")

    print("Failed to compile Russian translations")
    print("The .po file exists but compilation tools are not available")
    print("Russian translations will not work until the .mo file is created")
    return False

if __name__ == '__main__':
    success = compile_russian()
    sys.exit(0 if success else 1)