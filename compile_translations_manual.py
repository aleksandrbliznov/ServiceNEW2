#!/usr/bin/env python3
"""
Manual translation compilation script for Service PRO
Compiles .po files to .mo files for Flask-Babel
"""

import os
import sys
import struct

def compile_po_to_mo(po_file, mo_file):
    """Manually compile a .po file to .mo file"""
    try:
        with open(po_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse the .po file content
        messages = {}
        current_msgid = None
        current_msgstr = []

        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line.startswith('msgid "') and line != 'msgid ""':
                # Start of a new message
                if current_msgid:
                    messages[current_msgid] = ''.join(current_msgstr).replace('msgstr "', '').replace('"', '')

                current_msgid = line.replace('msgid "', '').replace('"', '')
                current_msgstr = []
                i += 1
                # Collect msgstr lines
                while i < len(lines) and (lines[i].strip().startswith('"') or lines[i].strip() == ''):
                    if lines[i].strip().startswith('msgstr "'):
                        current_msgstr.append(lines[i].strip())
                    i += 1
                continue
            i += 1

        # Add the last message
        if current_msgid:
            messages[current_msgid] = ''.join(current_msgstr).replace('msgstr "', '').replace('"', '')

        # Write the .mo file
        write_mo_file(mo_file, messages)
        print(f"Successfully compiled {po_file} to {mo_file}")
        return True

    except Exception as e:
        print(f"Error compiling {po_file}: {e}")
        return False

def write_mo_file(mo_file, messages):
    """Write a .mo file from parsed messages"""
    # .mo file format constants
    MO_MAGIC = 0x950412de
    MO_FORMAT_VERSION = 0

    # Prepare the data
    msgids = []
    msgstrs = []
    offsets = []

    for msgid, msgstr in messages.items():
        if msgid and msgstr:  # Skip empty messages
            msgids.append(msgid.encode('utf-8'))
            msgstrs.append(msgstr.encode('utf-8'))

    # Calculate offsets
    offset = 28  # Header size
    for i in range(len(msgids)):
        offsets.append((len(msgids[i]), len(msgstrs[i]), offset, offset + len(msgids[i])))
        offset += len(msgids[i]) + len(msgstrs[i])

    # Write the .mo file
    with open(mo_file, 'wb') as f:
        # Write header
        f.write(struct.pack('<I', MO_MAGIC))  # magic
        f.write(struct.pack('<I', MO_FORMAT_VERSION))  # version
        f.write(struct.pack('<I', len(msgids)))  # num_strings
        f.write(struct.pack('<I', 28))  # msgid_offset
        f.write(struct.pack('<I', 28))  # msgstr_offset
        f.write(struct.pack('<I', 0))  # hash_size
        f.write(struct.pack('<I', 0))  # hash_offset

        # Write offsets table
        for msgid_len, msgstr_len, msgid_offset, msgstr_offset in offsets:
            f.write(struct.pack('<I', msgid_len))
            f.write(struct.pack('<I', msgstr_offset))
            f.write(struct.pack('<I', msgstr_len))
            f.write(struct.pack('<I', msgid_offset))

        # Write strings
        for msgid, msgstr in zip(msgids, msgstrs):
            f.write(msgid + b'\x00')
            f.write(msgstr + b'\x00')

if __name__ == '__main__':
    po_file = 'translations/et/LC_MESSAGES/messages.po'
    mo_file = 'translations/et/LC_MESSAGES/messages.mo'

    if os.path.exists(po_file):
        success = compile_po_to_mo(po_file, mo_file)
        if success:
            print("Translation compilation completed successfully!")
        else:
            print("Translation compilation failed!")
            sys.exit(1)
    else:
        print(f"PO file not found: {po_file}")
        sys.exit(1)