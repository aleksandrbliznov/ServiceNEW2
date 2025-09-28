#!/usr/bin/env python3
"""
Translation compilation script for Service PRO
Compiles .po files to .mo files for Flask-Babel
"""

import os
import subprocess
import sys
from app import app

def compile_translations():
    """Compile translation files using Babel"""
    translations_dir = 'translations'

    if not os.path.exists(translations_dir):
        print("No translations directory found")
        return

    try:
        # Use Babel's compile_catalog command
        from babel.messages.frontend import compile_catalog
        compile_catalog()
        print("Successfully compiled translations using Babel")
    except ImportError:
        print("Babel not available, using fallback method")
        fallback_compile()
    except Exception as e:
        print(f"Error compiling with Babel: {e}")
        fallback_compile()

    print("Translation compilation completed!")

if __name__ == '__main__':
    compile_translations()