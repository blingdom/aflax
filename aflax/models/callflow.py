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
    userdata,
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
    ) + "/callflow.py"


def indexinit():
    # print("""Init Call Flow Datasets""")
    data = {}
    data['data'] = False
    try:
        x = datadoc.indexinit({
            "name": "calldata",
            "func": "callflow",
            "desc": "Asterisk Call Flow",
            "docs": ["calls_flow"],
            "file": epath
            })
        if x['data']:
            data['data'] = True
        else:
            print('Issue Document Calls Flow')
    except Exception as e:
        err = "Error Asterisk-Call-Flow {}".format(e)
        errordoc.indexcreate({
            "source": "indexinit",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexcreate(dat):
    """Create Asterisk Datasets"""
    data = {}
    data['data'] = False
    try:
        x = db.calls_flow.insert_one({
            "cdr": dat['cdr'],
            "media": dat['media'],
            "type": dat['type'],
            "created": int(time()),
            "status": "available"
            })
        data['id'] = str(x.inserted_id)
        data['data'] = True
    except Exception as e:
        err = "Error Asterisk-Create {}".format(e)
        errordoc.indexcreate({
            "source": "indexcreate",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexinfo(dat):
    """Info Asterisk Datasets"""
    data = {}
    data['data'] = False
    try:
        x = db.calls_flow.find({
            "_id": ObjectId(dat['id'])
            })
        if x.count():
            data['id'] = dat['id']
            data['cdr'] = x[0].get('cdr')
            data['media'] = x[0].get('media')
            data['type'] = x[0].get('type')
            data['created'] = x[0].get('created')
            data['status'] = x[0].get('status')
            data['data'] = True
    except Exception as e:
        err = "Error Asterisk-Info {}".format(e)
        errordoc.indexcreate({
            "source": "indexinfo",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexdata(dat):
    """Asterisk Datasets"""
    data = {}
    data['data'] = False
    try:
        cdr = []
        x = db.calls_flow.find({
            "reset": False
            })
        if x.count():
            while True:
                for y in x:
                    z = indexinfo({
                        "id": str(y.get('_id'))
                        })
                    if z['data']:
                        del z['data']
                        cdr.append(z)
                break

        data['cdr'] = cdr
        data['data'] = True
    except Exception as e:
        err = "Error Asterisk-Data {}".format(e)
        errordoc.indexcreate({
            "source": "indexdata",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexdash(dat):
    """Index Dashboard Asterisk"""
    data = {"data": False}
    try:
        data['source'] = "corporates"
        x = db.calls_flow.find()
        data['corps'] = x.count()
        data['data'] = True
    except Exception as e:
        err = "Error Dashboard-Asterisks {}".format(e)
        errorlog.indexcreate({
            "source": "indexdash",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexreset(dat=False):
    """Index Reset Asterisk"""
    data = {"data": False}
    try:
        data['source'] = "callflow"
        if dat:
            x = db.calls_flow.find({
                "id": ObjectId(dat['id'])
                })
            if x.count():
                data['data'] = True
                if credentials.RUNSTATUS == 'production':
                    edit = {}
                    edit['status'] = "deleted"
                    edit['deleted'] = int(time())
                    db.calls_flow.update_one(
                        {"_id": ObjectId(dat['id'])},
                        {"$set": edit}
                        )
                else:
                    db.calls_flow.remove({
                        "_id": ObjectId(dat['id'])
                        })
        else:
            if credentials.RUNSTATUS == 'production':
                x = db.calls_flow.find({
                    "reset": False
                    })
                edit = {}
                edit['status'] = "deleted"
                edit['reset'] = int(time())
                db.calls_flow.update_many(
                    {"reset": False},
                    {"$set": edit}
                    )
            else:
                x = db.calls_flow.find()
                data['callflow'] = x.count()
                db.calls_flow.remove()
            data['data'] = True
    except Exception as e:
        err = "Error Reset-Asterisks {}".format(e)
        errorlog.indexcreate({
            "source": "indexreset",
            "error": err, 
            "path": epath
            })
        print(err)

    return data
