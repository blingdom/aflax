#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function
    )

import os

RUNSTATUS = "development"  # production

# Flask Secret
FLASKSECRET = "\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16"

# Datasets
DATASETS = os.getcwd() + "/datasets"

# Roles File
ROLEITEMS = DATASETS + "/roles.json"

# MongoDB Host
MONGOHOST = "localhost"

