import os
import hashlib
import uuid
# from mixin_ws_api import MIXIN_WS_API
import prs_utility
from flask import Flask, render_template, g, request, redirect, session, url_for, flash, Blueprint
from flask_restful import Api, Resource
import requests
import json
import time
from io import BytesIO
import base64
import gzip
import prs_lib
import pressone_config
from assets import CNB
from Crypto.PublicKey import RSA
import requests
import time
import prs_utility
import mixin_config
from mixin_api import MIXIN_API
import random, string

mixin_api = MIXIN_API(mixin_config)

client = prs_lib.PRS({
  'env': 'dev',
  'private_key': '01e05107e3141083f66aa2ec5fa78d095115a912ca17148813b87d4313115837',
  'address': 'acd8960a52de7017059cfd6c7113f073fad2a2a2e',
  'debug': True,
})

'''
生成一个uuid格式的trace
'''
def genTrace():
    return str(uuid.uuid1())

'''
生成一个收款链接，需出入trace
'''
def genAPaylink(userid, trace=genTrace(), asset=CNB, amount='1', memo='1'):
    return "https://mixin.one/pay?recipient="+userid+"&asset="+asset+"&amount="+amount+"&trace="+trace+"&memo="+memo

def pubkeyContent(inputContent):
    contentWithoutHeader = inputContent[len("-----BEGIN PUBLIC KEY-----") + 1:]
    contentWithoutTail = contentWithoutHeader[:-1 * (len("-----END PUBLIC KEY-----") + 1)]
    contentWithoutReturn = contentWithoutTail[:64] + contentWithoutTail[65:129] + contentWithoutTail[
                                                                                  130:194] + contentWithoutTail[195:]
    return contentWithoutReturn


def generateMixinAPI(private_key,pin_token,session_id,user_id,pin,client_secret):
    mixin_config.private_key       = private_key
    mixin_config.pin_token         = pin_token
    mixin_config.pay_session_id    = session_id
    mixin_config.client_id         = user_id
    mixin_config.client_secret     = client_secret
    mixin_config.pay_pin           = pin
    return MIXIN_API(mixin_config)

def genMixinUser():
    key = RSA.generate(1024)  # 生成随机数，作为私钥
    pubkey = key.publickey()  # 生成公钥
    private_key = key.exportKey()
    session_key = pubkeyContent(pubkey.exportKey())  # 用以加密
    input_session = session_key.decode()
    account_name = ''
    body = {
        "session_secret": input_session,
        "full_name": account_name
    }

    '''
    获取token，生成 mixin network 账户
    '''
    token_from_freeweb = mixin_api.fetchTokenForCreateUser(body, "http://freemixinapptoken.myrual.me/token")
    userInfo = mixin_api.createUser(input_session, account_name, token_from_freeweb)
    # print(userInfo.get("data").get("user_id"))
    # print(userInfo)
    mixinApiNewUserInstance = generateMixinAPI(private_key.decode(),
                                               userInfo.get("data").get("pin_token"),
                                               userInfo.get("data").get("session_id"),
                                               userInfo.get("data").get("user_id"),
                                               "", "")
    '''
    为用户设置PIN
    '''
    pinInfo = mixinApiNewUserInstance.updatePin('000000', "")
    time.sleep(1)
    # pinInfo2 = mixinApiNewUserInstance.verifyPin('000000', "")
    # print(pinInfo2)
    return [userInfo, private_key.decode()]


'''
对一个文本签名
'''

def pub_text(userid, data, trace=genTrace()):
    texthash = prs_utility.keccak256(text=userid+r'\n'+data+r'\n'+trace)

    data = {
        'file_hash': texthash,
    }

    sig = prs_utility.sign_block_data(data, private_key=pressone_config.private_key)
    post_url = 'https://press.one/api/v2/datasign'

    payload = {
        'user_address': pressone_config.address,
        'type': 'PUBLISH:2',
        'meta': {
            'uris': '',
            'mime': 'text/markdown;UTF-8'
        },
        'data': data,
        'hash': prs_utility.hash_block_data(data),
        'signature': sig.get('signature')
    }

    req = requests.post(post_url, json=payload)

    return req.json()