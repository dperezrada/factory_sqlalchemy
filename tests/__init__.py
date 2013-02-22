# -*- coding: utf-8 -*-
import os
import sys
import site

from .configs.virtualenv import virtualenv_dir


os.environ['PYTHON_EGG_CACHE'] = '/tmp'

ALLDIRS = ['%s/%s' % (virtualenv_dir, 'lib/python2.7/site-packages/')]

# Remember original sys.path.
prev_sys_path = list(sys.path)

# Add each new site-packages directory.
for directory in ALLDIRS:
    site.addsitedir(directory)

# Reorder sys.path so new directories at the front.
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path
