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
db = client.datamedia

epath = os.path.dirname(
    os.path.realpath(__file__)
    ) + "/recording.py"


def indexinit():
    """Initialize Recordings Data"""
    data = {}
    data['data'] = False
    try:
        x = datadoc.indexinit({
            "name": "datamedia",
            "func": "recording",
            "desc": "Asterisk Recordings Data",
            "docs": ["record_media"],
            "file": epath
            })
        if x['data']:
            data['data'] = True
        else:
            print('Issue Document Recordings')
    except Exception as e:
        err = "Error Recordings-Init {}".format(e)
        errordoc.indexcreate({
            "source": "indexinit",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexcreate(dat):
    """Create Recordings"""
    data = {}
    data['data'] = False
    try:
        x = db.record_media.insert_one({
            "cdr": dat['cdr'],
            "length": False,
            "status": "verify",
            "reset": False,
            "created": int(time())
            })
        data['id'] = str(x.inserted_id)
        data['data'] = True
    except Exception as e:
        err = "Error Recordings-Create {}".format(e)
        errordoc.indexcreate({
            "source": "indexcreate",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexdata(dat):
    """Data Recordings"""
    data = {}
    data['data'] = False
    try:
        media = []

        if dat['next']:
            """Next Item """
            x = db.record_media.find({
                "status": "active",
                "_id": {"$gte": ObjectId(dat['next'])}
                })
        else:
            """Initial Data"""
            x = db.record_media.find({
                "status": "active"
                })

        if x.count():
            while True:
                for y in x:
                    if len(media) >= 10:
                        data['next'] = str(y.get('_id'))
                        break

                    z = indexinfo({
                        "id": str(y.get('_id')) 
                        })
                    if z['data']:
                        del z['data']
                        media.append(z)
                break
        data['media'] = media
        data['data'] = True
    except Exception as e:
        err = "Error Recordings-Data {}".format(e)
        errordoc.indexcreate({
            "source": "indexdata",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexinfo(dat):
    """Info Recordings"""
    data = {}
    data['data'] = False
    try:
        x = db.record_media.find({
            "_id": ObjectId(dat['id'])
            })
        if x.count():
            data['id'] = dat['id']
            data['data'] = True
    except Exception as e:
        err = "Error Recordings-Info {}".format(e)
        errordoc.indexcreate({
            "source": "indexinfo",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexreset(dat=False):
    """Index Reset Recordings"""
    data = {"data": False}
    try:
        data['source'] = "recordings"
        if dat and 'id' in dat:
            x = db.record_media.find({
                "id": ObjectId(dat['id'])
                })
            if x.count():
                data['data'] = True
                if credentials.RUNSTATUS == 'production':
                    edit = {}
                    edit['status'] = "deleted"
                    edit['deleted'] = int(time())
                    db.record_media.update_one(
                        {"_id": ObjectId(dat['id'])},
                        {"$set": edit}
                        )
                else:
                    db.record_media.remove({
                        "_id": ObjectId(dat['id'])
                        })
        else:
            if credentials.RUNSTATUS == 'production':
                x = db.record_media.find({
                    "reset": False
                    })
                data['count'] = x.count()
                if data['count']:
                    edit = {}
                    edit['status'] = "deleted"
                    edit['reset'] = int(time())
                    db.record_media.update_many(
                        {"reset": False},
                        {"$set": edit}
                        )
            else:
                x = db.record_media.find()
                data['count'] = x.count()
                if data['count']:
                    db.record_media.remove()
            data['data'] = True
    except Exception as e:
        err = "Error Reset-Recordings {}".format(e)
        errordoc.indexcreate({
            "source": "indexreset",
            "error": err, 
            "path": epath
            })
        print(err)

    return data
