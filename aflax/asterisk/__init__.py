#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function
    )

import os
import json
import credentials

from flask import (
    Blueprint,
    request,
    jsonify,
    render_template
    )

from aflax.models import (
    astrxdoc,
    recording,
    callflow,
    errordoc
    )

asterisk = Blueprint(
    'asterisk',
    __name__
    )

epath = os.path.dirname(
    os.path.realpath(__file__)
    ) + "/asterisk.py"


@asterisk.route("/incoming", methods=['GET'])
def incoming():
    # print("""Initialize Website Data""")
    try:
        x = request.args.to_dict()
        data = astrxdoc.indexcreate(x)
        if data['data']:
            call = data['lang'] + ","
            call += data['id']

            return call
    except Exception as e:
        err = "Error Index-Incoming {}".format(e)
        errordoc.indexcreate({
            "source": "incoming",
            "error": err,
            "path": epath
            })
        print(err)

    return "fail"


@asterisk.route("/langchoice", methods=['GET'])
def langchoice():
    """Language Choice"""
    try:
        x = request.args.to_dict()
        data = astrxdoc.indexlogin(x)
        if data['data']:
            return data['id'] + ",enter-password-daktari"
    except Exception as e:
        err = "Error Index-Login {}".format(e)
        errordoc.indexcreate({
            "source": "langchoice",
            "error": err,
            "path": epath
            })
        print(err)

    return "fail"


@asterisk.route("/hangup", methods=['GET'])
def hangup():
    """Call Hangup"""
    try:
        x = request.args.to_dict()
        data = astrxdoc.indexlogout(x)
        if data['data']:
            return "success"
    except Exception as e:
        err = "Error Index-Hangup {}".format(e)
        errordoc.indexcreate({
            "source": "hangup",
            "error": err,
            "path": epath
            })
        print(err)

    return "fail"


@asterisk.route("/astrecord", methods=['GET'])
def astrecord():
    """Asterisk Record"""
    try:
        x = request.args.to_dict()
        data = recording.indexcreate(x)
        if data['data']:
            return "success," + data['id']
    except Exception as e:
        err = "Error Asterisk-Record {}".format(e)
        errordoc.indexcreate({
            "source": "astrecord",
            "error": err,
            "path": epath
            })
        print(err)

    return "fail"


@asterisk.route("/astflow", methods=['GET'])
def astflow():
    """Asterisk Call-Flow"""
    try:
        x = request.args.to_dict()
        data = callflow.indexcreate(x)
        if data['data']:
            return "success"
    except Exception as e:
        err = "Error Asterisk-Call-Flow {}".format(e)
        errordoc.indexcreate({
            "source": "astflow",
            "error": err,
            "path": epath
            })
        print(err)

    return "fail"


@asterisk.route("/cdrdata", methods=['GET', 'POST'])
def cdrdata():
    """Call Detail Records"""

    try:
        if request.method == 'POST':
            x = request.get_json()
            data = astrxdoc.indexdata(x)
            if data['data']:
                return render_template(
                    "cdrdata.html",
                    data=data
                    )
        else:
            return render_template(
                "cdr.html",
                data={}
                )
    except Exception as e:
        err = "Error Call Details Data {}".format(e)
        errordoc.indexcreate({
            "source": "cdrdata",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404



@asterisk.route("/resetcdr", methods=['GET'])
def resetcdr():
    """Call Detail Records Reset"""

    try:
        x = astrxdoc.indexreset()
        return jsonify(x)
    except Exception as e:
        err = "Error Call Details Reset{}".format(e)
        errordoc.indexcreate({
            "source": "resetcdr",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404


@asterisk.route("/resetflow", methods=['GET'])
def resetflow():
    """Call Flow Reset"""

    try:
        x = callflow.indexreset()
        return jsonify(x)
    except Exception as e:
        err = "Error Call Flow Reset{}".format(e)
        errordoc.indexcreate({
            "source": "resetflow",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404
    