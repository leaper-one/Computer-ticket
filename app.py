from flask import Flask, jsonify, make_response, request, abort
import os
import hashlib
import mixin_config
import uuid
from mixin_api import MIXIN_API
import prs_utility
import pressone_config
import requests
import time
import fundmethood as fm
from assets import CNB



'''
用余生成一个可操作的 mixin network 用户实例
'''
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

'''
生成一套 mixin network 用户信息
'''
@app.route('/api/v1/creat_id/', methods=['GET'])
def create_userid():
    r = fm.genMixinUser()
    userInfo = r[0]
    private_key = r[1]
    userid = userInfo.get('data').get('user_id')
    sessionid = userInfo.get('data').get('session_id')
    pintoken = userInfo.get('data').get('pin_token')
    return jsonify({'userid': userid, 'private_key': private_key, 'sessionid': sessionid, 'pintoken': pintoken}), 201

'''
充值
'''
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

'''
签名并发布
'''
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


    pub = fm.pub_text(userid, data)
    pub_result = {
        'createdAt': pub.get('createdAt'),
        'data_id': pub.get('id'),
        'userid': userid,
        'trace': trace,
        'data': data
    }
    return jsonify(pub_result), 201

'''
根据 userid， blockid， data， trace 校验四者是否匹配
'''
@app.route('/api/v1/blocks/', methods=['POST'])
def blocks():
    if not request.json:
        abort(400)
    j = request.json
    data = j.get('data')
    userid = j.get('userid')
    blockid = j.get('blockid')
    trace = j.get('trace')

    texthash = prs_utility.keccak256(text=userid + r'\n' + data + r'\n' + trace)

    asked_data = {'file_hash': texthash, }

    datahash = prs_utility.hash_block_data(asked_data)

    r = requests.get('https://press.one/api/v2/blocks/'+blockid)
    result = r.json()
    print(result)
    print(datahash)
    print(result[0].get('hash'))
    if datahash == result[0].get('hash'):
        response = {
            'userid': userid,
            'blockid': blockid,
            'data': data,
            'datahash': datahash,
            'status': 'matched'
        }
    else:
        response = {
            'userid': userid,
            'blockid': blockid,
            'data': data,
            'datahash': datahash,
            'status': 'unmatched'
        }

    return jsonify(response), 201


if __name__ == '__main__':
    app.run(debug=True)