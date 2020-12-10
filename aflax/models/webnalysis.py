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
db = client.dataaccess

epath = os.path.dirname(
    os.path.realpath(__file__)
    ) + "/webnalysis.py"


def indexinit():
    """Initialize Analytics Data"""
    data = {}
    data['data'] = False
    try:
        x = datadoc.indexinit({
            "name": "dataaccess",
            "func": "webnalysis",
            "desc": "Web Analytics Data",
            "docs": ["web_access"],
            "file": epath
            })
        if not x['data']:
            print('Issue Document Analytics')
    except Exception as e:
        err = "Error Analytics-Init {}".format(e)
        errordoc.indexcreate({
            "source": "indexinit",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexcreate(dat):
    """Create Analytics"""
    data = {}
    data['data'] = False
    try:
        tdate = strftime('%d-%m-%Y')
        x = db.web_access.find({
            "ipadd": dat['ipadd'],
            "access": dat['access'],
            "method": dat['method'],
            "date": tdate,
            })
        if x.count():
            db.web_access.update_one(
                {"_id": x[0].get('_id')},
                {"$set": {"count": x[0].get('count') + 1}}
                )
            data['id'] = str(x[0].get('_id'))
        else:
            x = db.web_access.insert_one({
                "ipadd": dat['ipadd'],
                "method": dat['method'],
                "access": dat['access'],
                "count": 0,
                "status": "active",
                "reset": False,
                "date": tdate,
                "created": int(time())
                })
            data['id'] = str(x.inserted_id)
        data['data'] = True

    except Exception as e:
        err = "Error Analytics-Create {}".format(e)
        errordoc.indexcreate({
            "source": "indexcreate",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexdata(dat):
    """Data Analytics"""
    data = {}
    data['data'] = False
    try:
        web = []

        if dat['next']:
            """Next Item """
            x = db.web_access.find({
                "status": "active",
                "_id": {"$gte": ObjectId(dat['next'])}
                })
        else:
            """Initial Data"""
            x = db.web_access.find({
                "status": "active"
                })

        if x.count():
            while True:
                for y in x:
                    # if len(media) >= 10:
                    #    data['next'] = str(y.get('_id'))
                    #    break

                    z = indexinfo({
                        "id": str(y.get('_id')) 
                        })
                    if z['data']:
                        del z['data']
                        web.append(z)
                break
        data['web'] = web
        data['data'] = True
    except Exception as e:
        err = "Error Analytics-Data {}".format(e)
        errordoc.indexcreate({
            "source": "indexdata",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexinfo(dat):
    """Info Analytics"""
    data = {}
    data['data'] = False
    try:
        x = db.web_access.find({
            "_id": ObjectId(dat['id'])
            })
        if x.count():
            data['id'] = dat['id']
            data['ipadd'] = x[0].get('ipadd')
            data['method'] = x[0].get('method')
            data['access'] = x[0].get('access')
            data['date'] = x[0].get('date')
            data['status'] = x[0].get('status').title()
            data['date'] = x[0].get('date')
            data['created'] = x[0].get('created')
            data['createtime'] = datetime.fromtimestamp(
                int(x[0].get('created'))
                ).strftime('%H:%M:%S')
            data['data'] = True
    except Exception as e:
        err = "Error Analytics-Info {}".format(e)
        errordoc.indexcreate({
            "source": "indexinfo",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexdash():
    """Dash Analytics"""
    data = {}
    data['data'] = False
    try:
        x = db.web_access.distinct('ipadd')
        data['distinct'] = len(x)

        x = db.web_access.find({
            "date": strftime('%d-%m-%Y')
            })
        data['today'] = x.count()

        x = db.web_access.find({
            "status": "banned"
            })
        data['banned'] = x.count()

        data['data'] = True

    except Exception as e:
        err = "Error Web Analytics-Dashboard {}".format(e)
        errordoc.indexcreate({
            "source": "indexdash",
            "error": err, 
            "path": epath
            })
        print(err)
        
    return data


def indexreset(dat=False):
    """Index Reset Prompts"""
    data = {"data": False}
    try:
        data['source'] = "webaccess"
        if dat and 'id' in dat:
            x = db.web_access.find({
                "id": ObjectId(dat['id'])
                })
            if x.count():
                data['data'] = True
                if credentials.RUNSTATUS == 'production':
                    edit = {}
                    edit['status'] = "deleted"
                    edit['deleted'] = int(time())
                    db.web_access.update_one(
                        {"_id": ObjectId(dat['id'])},
                        {"$set": edit}
                        )
                else:
                    db.web_access.remove({
                        "_id": ObjectId(dat['id'])
                        })
        else:
            if credentials.RUNSTATUS == 'production':
                x = db.web_access.find({
                    "reset": False
                    })
                data['count'] = x.count()
                if data['count']:
                    edit = {}
                    edit['status'] = "deleted"
                    edit['reset'] = int(time())
                    db.web_access.update_many(
                        {"reset": False},
                        {"$set": edit}
                        )
            else:
                x = db.web_access.find()
                data['count'] = x.count()
                if data['count']:
                    db.web_access.remove()
            data['data'] = True
    except Exception as e:
        err = "Error Reset-Prompts {}".format(e)
        errordoc.indexcreate({
            "source": "indexreset",
            "error": err, 
            "path": epath
            })
        print(err)

    return data
