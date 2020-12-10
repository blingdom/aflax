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
    ) + "/astrxdoc.py"


def indexinit():
    # print("""Init Calls Datasets""")
    data = {}
    data['data'] = False
    try:
        x = datadoc.indexinit({
            "name": "calldata",
            "func": "astrxdoc",
            "desc": "Asterisk Calls Management",
            "docs": ["calls_cdr"],
            "file": epath
            })
        if x['data']:
            data['data'] = True
        else:
            print('Issue Document Calls')
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
    """Create Asterisk Datasets"""
    data = {}
    data['data'] = False
    try:
        phone = dat['phone'].replace("+","")

        x = db.calls_cdr.insert_one({
            "phone": phone,
            "created": int(time()),
            "status": "online",
            "hangup": False,
            "recording": False,
            "reset": False
            })
        data['id'] = str(x.inserted_id)
        data['lang'] = "english"
        data['data'] = True
        lan = userdata.indexcreate({
            "phone": phone
            })
        if lan['data'] and lan['lang'] != "english":
            data['lang'] = lan['lang']
        
    except Exception as e:
        err = "Error Asterisk-Create {}".format(e)
        errordoc.indexcreate({
            "source": "indexcreate",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexlogout(dat):
    """Index Logout"""
    data = {"data": False}
    try:
        x = db.calls_cdr.find({
            "_id": ObjectId(dat['cdr'])
            })
        if x.count():
            edit = {}
            edit['status'] = "offline"
            edit['hangup'] = int(time())
            db.calls_cdr.update_one(
                {"_id": ObjectId(dat['cdr'])},
                {"$set": edit}
                )
        data['data'] = True
    except Exception as e:
        err = "Error Logout Call {}".format(e)
        errordoc.indexcreate({
            "source": "indexlogout",
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
        x = db.calls_cdr.find({
            "_id": ObjectId(dat['id'])
            })
        if x.count():
            data['id'] = dat['id']
            data['phone'] = x[0].get('phone')
            data['createdate'] = datetime.fromtimestamp(
                int(x[0].get('created'))
                ).strftime('%d-%m-%Y')
            data['createtime'] = datetime.fromtimestamp(
                int(x[0].get('created'))
                ).strftime('%H:%M:%S')
            data['status'] = x[0].get('status').title()
            data['hangup'] = "00:00:00"
            if x[0].get('hangup'):
                data['hangup'] = datetime.fromtimestamp(
                    int(x[0].get('hangup'))
                    ).strftime('%H:%M:%S')
            data['recording'] = x[0].get('recording')
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
        x = db.calls_cdr.find({
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


def indexcontext(dat):
    """Index Call-Flow Context"""
    data = {"data": False}
    try:
        data['data'] = True
    except Exception as e:
        err = "Error Context-Info {}".format(e)
        errordoc.indexcreate({
            "source": "indexcontext",
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
        x = db.calls_cdr.find()
        data['corps'] = x.count()
        data['data'] = True
    except Exception as e:
        err = "Error Dashboard-Asterisks {}".format(e)
        errordoc.indexcreate({
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
        data['source'] = "pbx"
        if dat:
            x = db.calls_cdr.find({
                "id": ObjectId(dat['id'])
                })
            if x.count():
                data['data'] = True
                if credentials.RUNSTATUS == 'production':
                    edit = {}
                    edit['status'] = "deleted"
                    edit['deleted'] = int(time())
                    db.calls_cdr.update_one(
                        {"_id": ObjectId(dat['id'])},
                        {"$set": edit}
                        )
                else:
                    db.calls_cdr.remove({
                        "_id": ObjectId(dat['id'])
                        })
        else:
            if credentials.RUNSTATUS == 'production':
                x = db.calls_cdr.find({
                    "reset": False
                    })
                data['cdr'] = x.count()
                edit = {}
                edit['status'] = "deleted"
                edit['reset'] = int(time())
                db.calls_cdr.update_many(
                    {"reset": False},
                    {"$set": edit}
                    )
            else:
                x = db.calls_cdr.find()
                data['cdr'] = x.count()
                db.calls_cdr.remove()
            data['data'] = True
    except Exception as e:
        err = "Error Reset-Asterisks {}".format(e)
        errordoc.indexcreate({
            "source": "indexreset",
            "error": err, 
            "path": epath
            })
        print(err)

    return data
