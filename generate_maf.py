#!/usr/bin/env python
# coding: utf-8
#
# Copyright (c) 2013, Preferred Infrastructure, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import tarfile
import base64

TEMPLATE_FILE_NAME = 'maf_template.py'
TARGET_FILE_NAME = 'maf.py'
ARCHIVE_FILE_NAME = 'maflib.tar.bz2'
MAFLIB_PATH = 'maflib'

NEW_LINE = b'#XXX'
CARRIAGE_RETURN = b'#YYY'

ARCHIVE_BEGIN = b'#==>\n#'
ARCHIVE_END = b'#<==\n#'

if __name__ == '__main__':
    try:
        archive = tarfile.open(ARCHIVE_FILE_NAME, 'w:bz2')
        archive.add(MAFLIB_PATH, exclude=lambda fn: fn.endswith('.pyc'))
    except tarfile.TarError:
        raise Exception('can not use tar.bz2 file')
    finally:
        archive.close()
   
    with open(TEMPLATE_FILE_NAME, 'rb') as f:
        code = f.read()

    with open(ARCHIVE_FILE_NAME, 'rb') as f:
        archive = base64.b64encode(f.read())

    code += b'#==>\n#'
    code += archive.replace(b'\n', NEW_LINE).replace(b'\r', CARRIAGE_RETURN)
    code += b'\n#<==\n'

    with open(TARGET_FILE_NAME, 'wb') as f:
        f.write(code)

    os.unlink(ARCHIVE_FILE_NAME)
