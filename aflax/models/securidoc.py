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
    ) + "/securidoc.py"


def indexinit():
    """Initialize User Auth"""
    data = {}
    data['data'] = False
    try:
        x = datadoc.indexinit({
            "name": "authdata",
            "func": "securidoc",
            "desc": "Admin Security Data",
            "docs": ["hacker_data"],
            "file": epath
            })
        if x['data']:
            data['data'] = True
        else:
            print('Issue Document Security')
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
    """Security Data Create"""
    data = {}
    data['data'] = False
    try:
        x = db.hacker_data.insert_one({
            "ipadd": dat['ipadd'],
            "number": dat['number'],
            "ban": False,
            "status": "active",
            "created": int(time())
            })
        data['id'] = str(x.inserted_id)
        data['data'] = True
    except Exception as e:
        err = "Error Security-Create {}".format(e)
        errordoc.indexcreate({
            "source": "indexcreate",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexdata(dat):
    """Security Data"""
    data = {}
    data['data'] = False
    try:
        sec = []
        x = db.hacker_data.distinct('ipadd')
        if len(x) > 0:
            for y in x:
                z = {}
                z['ipadd'] = y
                c = db.hacker_data.find({
                    "ipadd": y
                    })
                z['first'] = datetime.fromtimestamp(
                    int(c[0].get('created'))
                    ).strftime('%d-%m-%Y')
                z['total'] = c.count()
                c = db.hacker_data.find({
                    "ipadd": y
                    }).sort('DESCENDING')
                z['last'] = datetime.fromtimestamp(
                    int(c[0].get('created'))
                    ).strftime('%d-%m-%Y')
                z['ban'] = c[0].get('ban')
                z['xtry'] = "Unknown"

                sec.append(z)

        data['security'] = sec
        data['data'] = True
    except Exception as e:
        err = "Error Security-Data {}".format(e)
        errordoc.indexcreate({
            "source": "indexdata",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexsecurity(dat):
    """Data Security"""
    data = {}
    data['data'] = False
    try:
        i = 0
        sec = []
        if dat['next']:
            x = db.hacker_data.find({
                "_id": {"$gte": ObjectId(dat['next'])}
                })
        else:
            x = db.hacker_data.find()

        if x.count():
            while True:
                for y in x:
                    i += 1
                    # if i >= 10:
                    #    break
                    z = indexinfo({
                        "id": str(y.get('_id'))
                        })
                    if z['data']:
                        del z['data']
                        sec.append(z)
                break
        data['data'] = True
        data['security'] = sec
    except Exception as e:
        err = "Error Security-Data {}".format(e)
        errordoc.indexcreate({
            "source": "indexsecurity",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexinfo(dat):
    """Info Security"""
    data = {}
    data['data'] = False
    try:
        x = db.hacker_data.find({
            "_id": ObjectId(dat['id'])
            })
        if x.count():
            data['id'] = dat['id']
            data['ipadd'] = x[0].get('ipadd')
            data['number'] = x[0].get('number')
            data['status'] = x[0].get('status').title()
            data['ban'] = x[0].get('ban')
            data['createdate'] = datetime.fromtimestamp(
                int(x[0].get('created'))
                ).strftime('%d-%m-%Y')
            data['createtime'] = datetime.fromtimestamp(
                int(x[0].get('created'))
                ).strftime('%H:%M:%S')
            data['data'] = True
    except Exception as e:
        err = "Error Security-Info {}".format(e)
        errordoc.indexcreate({
            "source": "indexinfo",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexreset(dat=False):
    """Index Reset Security"""
    data = {"data": False}
    try:
        data['source'] = "security"
        if dat:
            x = db.hacker_data.find({
                "id": ObjectId(dat['id'])
                })
            if x.count():
                data['data'] = True
                if credentials.RUNSTATUS == 'production':
                    edit = {}
                    edit['status'] = "deleted"
                    edit['deleted'] = int(time())
                    db.hacker_data.update_one(
                        {"_id": ObjectId(dat['id'])},
                        {"$set": edit}
                        )
                else:
                    db.hacker_data.remove({
                        "_id": ObjectId(dat['id'])
                        })
        else:
            if credentials.RUNSTATUS == 'production':
                x = db.hacker_data.find({
                    "reset": False
                    })
                data['cdr'] = x.count()
                edit = {}
                edit['status'] = "deleted"
                edit['reset'] = int(time())
                db.hacker_data.update_many(
                    {"reset": False},
                    {"$set": edit}
                    )
            else:
                x = db.hacker_data.find()
                data['cdr'] = x.count()
                db.hacker_data.remove()
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
