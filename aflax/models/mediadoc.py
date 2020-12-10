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
    ) + "/mediadoc.py"


def indexinit():
    """Initialize Media Data"""
    data = {}
    data['data'] = False
    try:
        x = datadoc.indexinit({
            "name": "datamedia",
            "func": "mediadoc",
            "desc": "Asterisk Media Data",
            "docs": ["prompt_media"],
            "file": epath
            })
        if x['data']:
            data['data'] = True
            z = indexload()
            print('Sorted Prompts', z)
        else:
            print('Issue Document Media')
    except Exception as e:
        err = "Error Media-Init {}".format(e)
        errordoc.indexcreate({
            "source": "indexinit",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexcreate(dat):
    """Create Media"""
    data = {}
    data['data'] = False
    try:
        x = db.prompt_media.find({
            "media": dat['media'],
            "language": dat['language']
            })
        if not x.count():
            x = db.prompt_media.insert_one({
                "media": dat['media'],
                "length": dat['length'],
                "text": dat['text'],
                "language": dat['language'],
                "path": dat['path'],
                "status": "active",
                "reset": False,
                "created": int(time())
                })
            data['id'] = str(x.inserted_id)
            data['data'] = True

    except Exception as e:
        err = "Error Media-Create {}".format(e)
        errordoc.indexcreate({
            "source": "indexcreate",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexdata(dat):
    """Data Media"""
    data = {}
    data['data'] = False
    try:
        media = []

        if dat['next']:
            """Next Item """
            x = db.prompt_media.find({
                "status": "active",
                "_id": {"$gte": ObjectId(dat['next'])}
                })
        else:
            """Initial Data"""
            x = db.prompt_media.find({
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
                        media.append(z)
                break
        data['media'] = media
        data['data'] = True
    except Exception as e:
        err = "Error Media-Data {}".format(e)
        errordoc.indexcreate({
            "source": "indexdata",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexinfo(dat):
    """Info Media"""
    data = {}
    data['data'] = False
    try:
        x = db.prompt_media.find({
            "_id": ObjectId(dat['id'])
            })
        if x.count():
            data['id'] = dat['id']
            data['media'] = x[0].get('media')
            data['length'] = x[0].get('length')
            data['text'] = x[0].get('text')
            data['language'] = x[0].get('language').title()
            data['path'] = x[0].get('path')
            data['status'] = x[0].get('status').title()
            data['created'] = x[0].get('created')
            data['createdate'] = datetime.fromtimestamp(
                int(x[0].get('created'))
                ).strftime('%d-%m-%Y')
            data['data'] = True
    except Exception as e:
        err = "Error Media-Info {}".format(e)
        errordoc.indexcreate({
            "source": "indexinfo",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexload():
    """Load Media"""
    data = {}
    data['data'] = False
    try:
        x = db.prompt_media.find()
        if not x.count():
            dirp = "/opt/aflax/media"
            tmpf = dirp + "/media.txt"
            d = os.listdir(dirp)
            for l in d:
                f = dirp + "/" + l
                for k in os.listdir(f):
                    os.system("sox --info -d " + f + "/" + k + " > " + tmpf)
                    with open(tmpf, 'r') as t:
                        lenf = t.readline()

                    xl = lenf.rstrip()
                    mn, ss = xl.split(".")

                    z = indexcreate({
                        "media": k,
                        "length": mn,
                        "text": False,
                        "language": l,
                        "path": f
                        })
                    if not z['data']:
                        err = "Error Creating Prompt " + k
                        errordoc.indexcreate({
                            "source": "indexload",
                            "error": err, 
                            "path": epath
                            })
                        print(err)
                    os.system("rm " + tmpf)
        data['data'] = True
    except Exception as e:
        err = "Error Media-Load {}".format(e)
        errordoc.indexcreate({
            "source": "indexload",
            "error": err, 
            "path": epath
            })
        print(err)

    return data


def indexreset(dat=False):
    """Index Reset Prompts"""
    data = {"data": False}
    try:
        data['source'] = "prompts"
        if dat and 'id' in dat:
            x = db.prompt_media.find({
                "id": ObjectId(dat['id'])
                })
            if x.count():
                data['data'] = True
                if credentials.RUNSTATUS == 'production':
                    edit = {}
                    edit['status'] = "deleted"
                    edit['deleted'] = int(time())
                    db.prompt_media.update_one(
                        {"_id": ObjectId(dat['id'])},
                        {"$set": edit}
                        )
                else:
                    db.prompt_media.remove({
                        "_id": ObjectId(dat['id'])
                        })
        else:
            if credentials.RUNSTATUS == 'production':
                x = db.prompt_media.find({
                    "reset": False
                    })
                data['count'] = x.count()
                if data['count']:
                    edit = {}
                    edit['status'] = "deleted"
                    edit['reset'] = int(time())
                    db.prompt_media.update_many(
                        {"reset": False},
                        {"$set": edit}
                        )
            else:
                x = db.prompt_media.find()
                data['count'] = x.count()
                if data['count']:
                    db.prompt_media.remove()
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
