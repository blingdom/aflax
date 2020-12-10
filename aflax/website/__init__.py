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
    webnalysis
    )

webview = Blueprint(
    'webview',
    __name__
    )

epath = os.path.dirname(
    os.path.realpath(__file__)
    ) + "/website.py"


@webview.before_app_request
def analytics():
    """App Before Request"""
    try:
        if request.endpoint != 'static':
            ipadd = request.environ.get(
                'HTTP_X_REAL_IP',
                request.remote_addr
                )
            if ipadd in ['127.0.0.1', 'localhost']:
                pass
            else:
                x = webnalysis.indexcreate({
                    "access": request.endpoint,
                    "method": request.method,
                    "ipadd": ipadd
                    })
    except Exception as e:
        err = "Analytics Error {}".format(e)
        errordoc.indexcreate({
            "source": "indexanalytics",
            "error": err,
            "path": epath
            })
        print(err)


@webview.route("/accessweb", methods=['GET', 'POST'])
def accessweb():
    """Web Access Database"""
    try:
        if request.method == 'POST':
            x = request.get_json()
            data = webnalysis.indexdata(x)
            if data['data']:
                return render_template(
                    "webaccessdata.html",
                    data=data
                    )
            else:
                return jsonify({}), 404

        else:
            data = webnalysis.indexdash()
            print(data)
            return render_template(
                "webaccess.html",
                data=data
                )

    except Exception as e:
        err = "Error Web-Access {}".format(e)
        errordoc.indexcreate({
            "source": "accessweb",
            "error": err,
            "path": epath
            })
        print(err)

    return render_template("error/404.html", data={})


@webview.route("/accessdata", methods=['GET'])
def accessdata():
    """Access Data"""
    try:
        x = request.args.to_dict()
        if 'next' not in x:
            x['next'] = False

        data = webnalysis.indexdata(x)
        if data['data']:
            return jsonify(data)

    except Exception as e:
        err = "Error Data-Access {}".format(e)
        errordoc.indexcreate({
            "source": "accessdata",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404


@webview.route("/accessreset", methods=['GET'])
def accessreset():
    """Reset Access Database"""
    try:
        x = request.args.to_dict()
        data = webnalysis.indexreset(x)
        if data['data']:
            return jsonify(data)

    except Exception as e:
        err = "Error Reset-Access {}".format(e)
        errordoc.indexcreate({
            "source": "accessreset",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404

