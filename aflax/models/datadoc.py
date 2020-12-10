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

from pydoc import (
    locate
    )
from time import (
    time,
    strftime
    )
from datetime import (
    datetime
    )
from aflax.models import (
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

db = client.datadoc

epath = os.path.dirname(
    os.path.realpath(__file__)
    ) + "/datadoc.py"


def indexinit(dat):
    # print("""Create Database Document Entry:""", dat['desc'])
    data = {}
    data['data'] = False
    try:
        hashkey = dat['name']
        hashkey += dat['func']
        hashkey += dat['file']

        hashkey = hashlib.sha256(
            hashkey.encode()
            ).hexdigest()

        x = db.core_documents.find({
            "hash": hashkey,
            })
        if x.count():
            data['id'] = str(x[0].get('_id'))
        else:
            print("""Create Database Document Entry:""", dat['name'],hashkey)
            x = db.core_documents.insert_one({
                "name": dat['name'],
                "desc": dat['desc'],
                "func": dat['func'],
                "file": dat['file'],
                "docs": dat['docs'],
                "size": 0,
                "hash": hashkey,
                "purge": [],
                "status": "active",
                "created": int(time()),
                })
            data['id'] = str(x.inserted_id)
        data['data'] = True
    except Exception as e:
        err = "Error {}".format(e)
        errordoc.indexcreate({
            "source": "indexcreate",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexdata(dat):
    """Database Document Data"""
    data = {"data": False}
    try:
        docs = []
        data['next'] = False
        data['prev'] = False

        if 'prev' in dat:
            x = db.core_documents.find({
                "_id": {"$lte": ObjectId(dat['prev'])}
                })
        elif 'next' in dat:
            x = db.core_documents.find({
                "_id": {"$gte": ObjectId(dat['prev'])}
                })
        else:
            x = db.core_documents.find()
        
        if x.count():
            while True:
                i = 0
                for y in x:
                    i += 1

                    if i == 1 and data['prev']:
                        data['prev'] = str(y.get('_id'))

                    if i > 10:
                        if not data['next']:
                            data['next'] = str(y.get('_id'))
                        break

                    z = indexinfo({
                        "id": str(y.get('_id'))
                        })
                    if z['data']:
                        del z['data']
                        docs.append(z)
                    else:
                        err = ""

                data['next'] = False
                data['prev'] = False
                break

        data['docs'] = docs
        data['count'] = len(docs)
        data['data'] = True

    except Exception as e:
        err = "Error Docs-Manager Data {}".format(e)
        errordoc.indexcreate({
            "source": "indexdata",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexinfo(dat):
    """Database Document Info"""
    data = {"data": False}
    try:
        x = db.core_documents.find({
            "_id": ObjectId(dat['id'])
            })
        if x.count():
            data['id'] = dat['id']
            data['name'] = x[0].get('name')
            data['file'] = x[0].get('file')
            data['func'] = x[0].get('func')
            data['docs'] = x[0].get('docs')
            data['size'] = x[0].get('size')
            data['hash'] = x[0].get('hash')
            data['purge'] = x[0].get('purge')
            data['status'] = x[0].get('status')
            data['created'] = x[0].get('created')
            data['date'] = datetime.fromtimestamp(
                int(x[0].get('created'))
                ).strftime('%d %B %Y')
            data['data'] = True
    except Exception as e:
        err = "Error Docs-Manager Info {}".format(e)
        errordoc.indexcreate({
            "source": "indexinfo",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexstats(dat):
    """Database Document Stats"""
    try:
        pass
    except Exception as e:
        err = "Error Docs-Manager Stats {}".format(e)
        errordoc.indexcreate({
            "source": "indexstats",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexreset():
    # print("""Database Document Delete""")
    data = {}
    data['data'] = False
    try:
        data['reset'] = []
        reset = []
        x = db.core_documents.find()
        data['docs'] = x.count()
        if x.count():
            for y in x:
                z = y.get('file')
                z = z.split("/")
                # print(z[-3:], len(z))
                a = z[-3] + "."
                a += z[-2] + "."
                a += z[-1].replace(".py", "")
                
                try:
                    # print('Locate Path', a)
                    b = locate(a)
                    r = b.indexreset()
                    if 'data' in r:
                        del r['data']
                    reset.append(r)
                except Exception as e:
                    print('No Reset Index', e, a)
            # db.core_documents.remove()
        data['reset'] = reset
        data['data'] = True
    except Exception as e:
        err = "Error Docs-Data Reset {}".format(e)
        errordoc.indexcreate({
            "source": "indexreset",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexdash(dat):
    """Collections-Data Dashboard"""
    data = {"data": False}
    try:
        data['data'] = True
    except Exception as e:
        err = "Error Docs-Data Dashboard {}".format(e)
        errordoc.indexcreate({
            "source": "indexdash",
            "error": err, 
            "path": epath
            })
        print(err)

    return data
