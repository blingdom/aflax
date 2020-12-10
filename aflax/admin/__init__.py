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
    render_template,
    redirect,
    url_for,
    session,
    jsonify
    )

from aflax.models import (
    errordoc,
    userdata,
    callflow,
    securidoc,
    authdoc
    )

admin = Blueprint(
    'admin',
    __name__
    )

epath = os.path.dirname(
    os.path.realpath(__file__)
    ) + "/admin.py"


@admin.before_app_first_request
def indexinit():
    # print("""Initialize Website Data""")
    try:
        x = errordoc.indexinit()
        x = authdoc.indexinit()
        x = userdata.indexinit()
        x = callflow.indexinit()
        x = securidoc.indexinit()
    except Exception as e:
        err = "Error Index-Init Admin {}".format(e)
        errordoc.indexcreate({
            "source": "indexinit",
            "error": err,
            "path": epath
            })
        print(err)


@admin.route("/", methods=['GET'])
def indexhome():
    # print("""Initialize Website Data""")
    try:
        return render_template("index.html")
    except Exception as e:
        err = "Error Index-Init {}".format(e)
        errordoc.indexcreate({
            "source": "indexhome",
            "error": err,
            "path": epath
            })
        print(err)

    return "", 404


@admin.route("/indexform", methods=['POST'])
def indexform():

    try:
        x = request.get_json()
        if 'item' in x:
            return render_template(x['item'] + ".html")
    except Exception as e:
        err = "Error Index-Forms {}".format(e)
        errordoc.indexcreate({
            "source": "indexform",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404


@admin.route("/dashboard", methods=['GET', 'POST'])
def dashboard():

    try:
        if request.method == 'POST':
            data = {}
            data['calls'] = 0
            data['prompts'] = 0
            data['recording'] = 0
            data['webaccess'] = 0

            x = astrxdoc.indexdash()
            if x['data']:
                """Calls data"""
                data['calls'] = x['calls']

            x = mediadoc.indexdash()
            if x['data']:
                """Calls data"""
                data['prompts'] = x['prompts']

            x = recordings.indexdash()
            if x['data']:
                """Calls data"""
                data['recording'] = x['recording']

            x = securidoc.indexdash()
            if x['data']:
                """Calls data"""
                data['webaccess'] = x['webaccess']
            
        else:
            return render_template(
                "dashboard.html",
                data={}
                )
    except Exception as e:
        err = "Error Index-Dashboard {}".format(e)
        errordoc.indexcreate({
            "source": "dashboard",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404


@admin.route("/indexlogin", methods=['POST'])
def indexlogin():
    try:
        x = request.get_json()
        data = authdoc.indexlogin(x)
        if data['data']:
            return jsonify(data)
    except Exception as e:
        err = "Error Index-Login {}".format(e)
        errordoc.indexcreate({
            "source": "indexlogin",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404


@admin.route("/indexlogout", methods=['GET'])
def indexlogout():
    try:
        return render_template("index.html")
    except Exception as e:
        err = "Error Index-Logout {}".format(e)
        errordoc.indexcreate({
            "source": "indexlogout",
            "error": err,
            "path": epath
            })
        print(err)

    return render_template("error/404.html")


@admin.route("/indexregister", methods=['POST'])
def indexregister():
    try:
        x = request.get_json()
        data = authdoc.indexregister(x)
        if data['data']:
            return jsonify(data)
    except Exception as e:
        err = "Error Index-Register{}".format(e)
        errordoc.indexcreate({
            "source": "indexregister",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404


@admin.route("/indexforgot", methods=['POST'])
def indexforgot():
    try:
        x = request.get_json()
        data = authdoc.indexforgot(x)
        if data['data']:
            return jsonify(data)
    except Exception as e:
        err = "Error Index-Forgot {}".format(e)
        errordoc.indexcreate({
            "source": "indexforgot",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404


@admin.route("/security", methods=['GET'])
def security():
    """Admin Security"""
    try:
        return render_template(
            "hacker.html",
            data={}
            )
    except Exception as e:
        err = "Error Security-Index {}".format(e)
        errordoc.indexcreate({
            "source": "security",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404


@admin.route("/indexhacker", methods=['GET', 'POST'])
def indexhacker():
    """Call Hack Data"""
    try:
        if request.method == 'POST':
            x = request.get_json()
            data = securidoc.indexdata(x)
            if data['data']:
                return render_template(
                    "hackerdata.html",
                    data=data
                    )

        else:
            x = request.args.to_dict()
            if x['item'] == 'create':
                data = securidoc.indexcreate(x)
                if data['data']:
                    return "success"
                else:
                    return "fail"

            else:
                x['next'] = False
                data = securidoc.indexdata(x)
                return jsonify(data)

    except Exception as e:
        err = "Error Hacker Data {}".format(e)
        errordoc.indexcreate({
            "source": "indexhacker",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404


@admin.route("/indexreset", methods=['GET'])
def indexreset():
    """Reset Database"""
    try:
        data = datadoc.indexreset()
        if data['data']:
            return jsonify(data)
    except Exception as e:
        err = "Error Reset-Core {}".format(e)
        errordoc.indexcreate({
            "source": "resetcore",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404
    