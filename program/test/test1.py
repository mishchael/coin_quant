#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-19 21:50:10
# @Author  : Michael (mishchael@gmail.com)

import requests  # pip install requests
import json
import hashlib
import hmac
import time #for nonce

class BitfinexClient(object):
    BASE_URL = "https://api.bitfinex.com/"
    KEY=""
    SECRET=""
    proxies = {
        'http': 'socks5://127.0.0.1:1080',
        'https': 'socks5://127.0.0.1:1080'
    }

    def _nonce(self):
        """
        Returns a nonce
        Used in authentication
        """
        return str(int(round(time.time() * 1000)))

    def _headers(self, path, nonce, body):

        signature = "/api/" + path + nonce + body
        print("Signing: " + signature)
        h = hmac.new(self.SECRET.encode('utf8'), signature.encode('utf8'), hashlib.sha384)
        signature = h.hexdigest()

        return {
            "bfx-nonce": nonce,
            "bfx-apikey": self.KEY,
            "bfx-signature": signature,
            "content-type": "application/json"
        }

    def active_orders(self):
        """
        Fetch active orders
        """
        nonce = self._nonce()
        body = {}
        rawBody = json.dumps(body)
        path = "v2/auth/r/orders"


        print(self.BASE_URL + path)
        print(nonce)


        headers = self._headers(path, nonce, rawBody)

        print(headers)
        print(rawBody)


        print("requests.post("+self.BASE_URL + path + ", headers=" + str(headers) + ", data=" + rawBody + ", verify=True)")
        r = requests.post(self.BASE_URL + path, headers=headers, proxies = self.proxies ,data=rawBody, verify=True)

        if r.status_code == 200:
          print(r.status_code)
          return r.json()
        else:
          print(r.status_code)
          print(r)
          return 'error'

print(BitfinexClient().active_orders())
