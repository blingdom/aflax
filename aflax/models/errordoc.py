#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function
    )

import os
import re
import hashlib
import credentials

from time import (
    time,
    strftime
    )

from datetime import (
    datetime
    )
from aflax.models import (
    datadoc
    )
from bson.objectid import (
    ObjectId
    )
from pymongo import (
    MongoClient,
    DESCENDING
    )

client = MongoClient(
    credentials.MONGOHOST
    )
db = client.datadoc

epath = os.path.dirname(
    os.path.realpath(__file__)
    ) + "/errordoc.py"


def indexinit():
    # print("""Init Errors Datasets""")
    data = {}
    data['data'] = False
    try:
        x = datadoc.indexinit({
            "name": "datadoc",
            "func": "errordoc",
            "desc": "App Errors Management",
            "docs": ["errors_aflax"],
            "file": epath
            })
        if x['data']:
            data['data'] = True
        else:
            print('Issue Document Errors')
    except Exception as e:
        err = "Error Errors-Init {}".format(e)
        errordoc.indexcreate({
            "source": "indexinit",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexcreate(dat):
    print("""Create Error""", dat)
    try:
        data = {"data": True}
    except Exception as e:
        err = "Error Create {}".format(e)
        print(err)

    return data
    