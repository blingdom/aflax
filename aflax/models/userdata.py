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

from flask import (
    session
    )
from time import (
    time,
    strftime
    )
from datetime import (
    datetime
    )
from aflax.models import (
    datadoc,
    errordoc
    )

from bson.objectid import ObjectId
from pymongo import (
    MongoClient,
    DESCENDING
    )

client = MongoClient(
    credentials.MONGOHOST
    )
db = client.calldata

epath = os.path.dirname(
    os.path.realpath(__file__)
    ) + "/userdata.py"


def indexinit():
    # print("""Init User Contact Data""")
    data = {}
    data['data'] = False
    try:
        x = datadoc.indexinit({
            "name": "calldata",
            "func": "userdata",
            "desc": "User Contact Management",
            "docs": ["user_data"],
            "file": epath
            })
        if x['data']:
            data['data'] = True
        else:
            print('Issue Document Contacts')
    except Exception as e:
        err = "Error Asterisk-Init {}".format(e)
        errordoc.indexcreate({
            "source": "indexinit",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexcreate(dat):
    """Create Contacy Datasets"""
    data = {}
    data['data'] = False
    try:
        x = db.user_data.find({
            "phone": dat['phone']
            })
        if x.count():
            data['id'] = str(x[0].get('_id'))
            data['lang'] = x[0].get('language')
        else:
            x = db.user_data.insert_one({
                "phone": dat['phone'],
                "location": False,
                "language": "english",
                "status": "available",
                "created": int(time()),
                })
            data['id'] = str(x.inserted_id)
            data['lang'] = "english"
        data['data'] = True
    except Exception as e:
        err = "Error Contact-Create {}".format(e)
        errordoc.indexcreate({
            "source": "indexcreate",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexreset(dat=False):
    """Index Reset Asterisk"""
    data = {"data": False}
    try:
        data['source'] = "contacts"
        if dat:
            x = db.user_data.find({
                "id": ObjectId(dat['id'])
                })
            if x.count():
                data['data'] = True
                if credentials.RUNSTATUS == 'production':
                    edit = {}
                    edit['status'] = "deleted"
                    edit['deleted'] = int(time())
                    db.user_data.update_one(
                        {"_id": ObjectId(dat['id'])},
                        {"$set": edit}
                        )
                else:
                    db.user_data.remove({
                        "_id": ObjectId(dat['id'])
                        })
        else:
            if credentials.RUNSTATUS == 'production':
                x = db.user_data.find({
                    "reset": False
                    })
                edit = {}
                edit['status'] = "deleted"
                edit['reset'] = int(time())
                db.user_data.update_many(
                    {"reset": False},
                    {"$set": edit}
                    )
            else:
                db.user_data.remove()
            data['data'] = True
    except Exception as e:
        err = "Error Reset-Contacts {}".format(e)
        errorlog.indexcreate({
            "source": "indexreset",
            "error": err, 
            "path": epath
            })
        print(err)

    return data
