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
db = client.authdata

epath = os.path.dirname(
    os.path.realpath(__file__)
    ) + "/authdoc.py"


def indexinit():
    """Initialize User Auth"""
    data = {}
    data['data'] = False
    try:
        x = datadoc.indexinit({
            "name": "authdata",
            "func": "authdoc",
            "desc": "Admin User Auth",
            "docs": ["user_auth"],
            "file": epath
            })
        if x['data']:
            z = indexload()
            if z['data']:
                data['data'] = True
        else:
            print('Issue Document Auth')
    except Exception as e:
        err = "Error Auth-Init {}".format(e)
        errordoc.indexcreate({
            "source": "indexinit",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexcreate(dat):
    """Register Auth"""
    data = {}
    data['data'] = False
    try:
        x = db.user_auth.find({
            "username": dat['username']
            })
        if not x.count():
            passd = hashlib.sha256(
                dat['password'].encode()
                ).hexdigest()
            x = db.user_auth.insert_one({
                "username": dat['username'],
                "password": passd,
                "status": "validate",
                "reset": False,
                "created": int(time())
                })
            data['id'] = str(x.inserted_id)
            data['data'] = True
    except Exception as e:
        err = "Error Auth-Register {}".format(e)
        errordoc.indexcreate({
            "source": "indexcreate",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexlogin(dat):
    """Login Auth"""
    data = {}
    data['data'] = False
    try:
        passd = hashlib.sha256(
            dat['password'].encode()
            ).hexdigest()
        x = db.user_auth.find({
            "username": dat['username'],
            "password": passd
            })
        if x.count():
            data['data'] = True
    except Exception as e:
        err = "Error Auth-Login {}".format(e)
        errordoc.indexcreate({
            "source": "indexlogin",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexforgot(dat):
    """Forgot Auth"""
    data = {}
    data['data'] = False
    try:
        pass
    except Exception as e:
        err = "Error Auth-Forgot {}".format(e)
        errordoc.indexcreate({
            "source": "indexforgot",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexdata(dat):
    """Data Auth"""
    data = {}
    data['data'] = False
    try:
        pass
    except Exception as e:
        err = "Error Auth-Data {}".format(e)
        errordoc.indexcreate({
            "source": "indexdata",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexinfo(dat):
    """Info Auth"""
    data = {}
    data['data'] = False
    try:
        pass
    except Exception as e:
        err = "Error Auth-Info {}".format(e)
        errordoc.indexcreate({
            "source": "indexinfo",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexreset(dat=False):
    """Reset Auth"""
    data = {"data": False}
    try:
        data['source'] = "authdata"
        if dat and 'id' in dat:
            x = db.user_auth.find({
                "id": ObjectId(dat['id'])
                })
            if x.count():
                data['data'] = True
                if credentials.RUNSTATUS == 'production':
                    edit = {}
                    edit['status'] = "deleted"
                    edit['deleted'] = int(time())
                    db.user_auth.update_one(
                        {"_id": ObjectId(dat['id'])},
                        {"$set": edit}
                        )
                else:
                    db.user_auth.remove({
                        "_id": ObjectId(dat['id'])
                        })
        else:
            if credentials.RUNSTATUS == 'production':
                x = db.user_auth.find({
                    "reset": False
                    })
                data['count'] = x.count()
                if data['count']:
                    edit = {}
                    edit['status'] = "deleted"
                    edit['reset'] = int(time())
                    db.user_auth.update_many(
                        {"reset": False},
                        {"$set": edit}
                        )
            else:
                x = db.user_auth.find()
                data['count'] = x.count()
                if data['count']:
                    db.user_auth.remove()
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


def indexload():
    """Load Default Auth"""
    data = {}
    data['data'] = False
    try:
        x = db.user_auth.find()
        if not x.count():
            userd = ["bngari@gmail.com", "wanyama@gmail.com"]
            for i in userd:
                z = indexcreate({
                    "username": i,
                    "password": "changeme123"
                    })
                if z['data']:
                    print('Create Default User', i, 'ID', z['id'])
                else:
                    err = "Error Creating Default User " + i
                    errordoc.indexcreate({
                        "source": "indexload",
                        "error": err, 
                        "path": epath
                        })
                    print(err)

        data['data'] = True
    except Exception as e:
        err = "Error Auth-Default {}".format(e)
        errordoc.indexcreate({
            "source": "indexload",
            "error": err, 
            "path": epath
            })
        print(err)

    return data
