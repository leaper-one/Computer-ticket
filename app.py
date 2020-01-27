from flask import Flask, jsonify, make_response, request, abort
import os
import hashlib
import mixin_config
import uuid
from mixin_api import MIXIN_API
import prs_utility
from flask import Flask, render_template, g, request, redirect, session, url_for, flash, Blueprint
from flask_restful import Api, Resource
from Crypto.PublicKey import RSA

import requests
import json
import time
from io import BytesIO
import base64
import gzip
import prs_lib

import fundmethood as fm
from assets import CNB

def generateMixinAPI(private_key,pin_token,session_id,user_id,pin,client_secret):
    mixin_config.private_key       = private_key
    mixin_config.pin_token         = pin_token
    mixin_config.pay_session_id    = session_id
    mixin_config.client_id         = user_id
    mixin_config.client_secret     = client_secret
    mixin_config.pay_pin           = pin
    return MIXIN_API(mixin_config)

app = Flask(__name__)
mixin_api = MIXIN_API(mixin_config)



@app.route('/')
def index():
    return "Hello, World!"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/v1/creat_id/', methods=['GET'])
def create_userid():
    r = fm.genMixinUser()
    userInfo = r[0]
    private_key = r[1]
    userid = userInfo.get('data').get('user_id')
    sessionid = userInfo.get('data').get('session_id')
    pintoken = userInfo.get('data').get('pin_token')
    print(type(userInfo))
    print(type(private_key))
    print(type(userid))
    print(type(sessionid))
    print(type(pintoken))
    return jsonify({'userid': userid, 'private_key': private_key, 'sessionid': sessionid, 'pintoken': pintoken}), 201


@app.route('/api/v1/charge/', methods=['POST'])
def charge():
    now = time.time()
    trace = fm.genTrace()
    print(trace)
    if not request.json:
        abort(400)
    j = request.json
    userid = j.get('userid')
    print(userid)
    amount = j.get('amount')
    print(amount)
    url = fm.genAPaylink(userid, trace=trace, asset=CNB, amount=amount, memo='CHARGE')
    return jsonify({'time': now, 'userid': userid, 'charge_url': url}), 201


@app.route('/api/v1/pub/', methods=['POST'])
def create_pub():
    if not request.json:
        abort(400)
    j = request.json
    now = time.time()
    trace = fm.genTrace()

    userid = j.get('userid')
    private_key = j.get('private_key')
    sessionid = j.get('sessionid')
    pintoken = j.get('pintoken')
    pin = j.get('pin')
    data = j.get('data')

    NewUserInstance = generateMixinAPI(private_key, pintoken, sessionid, userid, pin, "")

    # pay = NewUserInstance.transferTo(mixin_config.client_id, CNB, 1, 'pay', trace, '000000','')
    # print(pay)
    # for i in (0, 20):
    #     # print(mixin_api.verifyPayment(CNB, mixin_config.client_id, "1", trace))
    #     # payment_trace = mixin_api.verifyPayment(CNB, mixin_config.client_id, "1", trace).get("data").get("status")
    #     if True or payment_trace == 'paid':
    #         pub = fm.pub_text(userid, data)
    #         pub_result = {
    #             'createdAt': pub.get('createdAt'),
    #             'data_id': pub.get('id'),
    #             'userid': userid,
    #             'trace': trace,
    #             'data': data
    #         }
    #         break

    pub = fm.pub_text(userid, data)
    pub_result = {
        'createdAt': pub.get('createdAt'),
        'data_id': pub.get('id'),
        'userid': userid,
        'trace': trace,
        'data': data
    }
    return jsonify(pub_result), 201


if __name__ == '__main__':
    app.run(debug=True)