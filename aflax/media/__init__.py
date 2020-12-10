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
    jsonify,
    send_from_directory
    )

from aflax.models import (
    errordoc,
    mediadoc,
    recording,
    )

media = Blueprint(
    'media',
    __name__
    )

epath = os.path.dirname(
    os.path.realpath(__file__)
    ) + "/__init__.py"


@media.before_app_first_request
def indexinit():
    """Initialize Media"""
    try:
        x = mediadoc.indexinit()
        x = recording.indexinit()
    except Exception as e:
        err = "Error Index-Init Media {}".format(e)
        errordoc.indexcreate({
            "source": "indexinit",
            "error": err,
            "path": epath
            })
        print(err)


@media.route("/recordings", methods=['POST', 'GET'])
def recordings():
    # print("""Media Data""")
    try:
        if request.method == 'POST':
            """Return Recordings Data"""
            x = request.get_json()
            data = recording.indexdata(x)
            if data['data']:
                return render_template(
                    "mediarecording.html",
                    data=data
                    )
        else:
            # print("""Return Recordings Index""")
            return render_template("recordings.html", data={})
    except Exception as e:
        err = "Error Recordings-Data {}".format(e)
        errordoc.indexcreate({
            "source": "recordings",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404


@media.route("/prompts", methods=['POST', 'GET'])
def prompts():
    # print("""Media Data""")
    try:
        if request.method == 'POST':
            """Return Prompts Data"""
            x = request.get_json()
            data = mediadoc.indexdata(x)
            if data['data']:
                return render_template(
                    "mediaprompts.html",
                    data=data
                    )
        else:
            # print("""Return Media Index""")
            return render_template("prompts.html", data={})
    except Exception as e:
        err = "Error Prompts-Data {}".format(e)
        errordoc.indexcreate({
            "source": "prompts",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404


@media.route("/createmedia", methods=['POST'])
def createmedia():
    """Create Media Database"""

    try:
        """From Web Upload"""
        x = request.get_json()
        data = mediadoc.indexcreate(x)
        if data['data']:
            return jsonify(data)
    except Exception as e:
        err = "Error Media-Create {}".format(e)
        errordoc.indexcreate({
            "source": "createmedia",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404


@media.route("/infomedia", methods=['GET', 'POST'])
def infomedia():
    """Info Media Database - Modal"""

    try:
        if request.method == 'POST':
            x = request.get_json()
        else:
            x = request.args.to_dict()
    except Exception as e:
        err = "Error Media-Info {}".format(e)
        errordoc.indexcreate({
            "source": "infomedia",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404


@media.route("/viewprompt", methods=['POST'])
def viewprompt():
    """Info Media Database - Modal"""
    try:
        x = request.get_json()
        data = mediadoc.indexinfo(x)
        if data['data']:
            return render_template(
                "modals/editprompt.html",
                data=data
                )
    except Exception as e:
        err = "Error View-Prompt {}".format(e)
        errordoc.indexcreate({
            "source": "viewprompt",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404


@media.route("/editmedia", methods=['POST'])
def editmedia():
    """Edit Media Database"""

    try:
        if request.method == 'POST':
            x = request.get_json()
        else:
            x = request.args.to_dict()
    except Exception as e:
        err = "Error Media-Editor {}".format(e)
        errordoc.indexcreate({
            "source": "editmedia",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404


@media.route("/playprompt", methods=['GET'])
def playprompt():
    """Play Media"""

    try:
        x = request.args.to_dict()
        data = mediadoc.indexinfo(x)
        if data['data']:
            return send_from_directory(
                data['path'],
                data['media']
                )
    except Exception as e:
        err = "Error Media-Player {}".format(e)
        errordoc.indexcreate({
            "source": "playprompt",
            "error": err,
            "path": epath
            })
        print(err)

    return "", 404


@media.route("/mediareset", methods=['GET'])
def mediareset():
    """Reset Media Database item=recording"""
    try:
        if request.method == 'POST':
            x = request.get_json()

        else:
            x = request.args.to_dict()

        if x['item'] == 'prompts':
            data = mediadoc.indexreset(x)

        else:
            data = recording.indexreset(x)

        if data['data']:
            return jsonify(data)

    except Exception as e:
        err = "Error Reset-Core {}".format(e)
        errordoc.indexcreate({
            "source": "mediareset",
            "error": err,
            "path": epath
            })
        print(err)

    return jsonify({}), 404
    