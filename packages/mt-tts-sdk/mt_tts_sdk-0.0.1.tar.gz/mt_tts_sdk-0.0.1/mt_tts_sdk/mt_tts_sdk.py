#coding:utf8
import time

import requests
import json
import hmac
import base64
import uuid
import datetime
import threading

from hashlib import sha1
from abc import ABC, abstractmethod

class CallbackAction(ABC):
    @abstractmethod
    def onSuc(self, sessionId, data):
        pass

    @abstractmethod
    def onFail(self, sessionId, errorCode):
        pass



class TtsClient:
    AUTHORIZATION_FORMAT = "AIAUTH-V1 {}:{}"

    def __init__(self, env, appId, appKey, secretKey):
        self.env = env
        self.appId = appId
        self.appKey = appKey
        self.secretKey = secretKey

    def hmac_sha1(self, key, data):
        try:
            key_bytes = key.encode('utf-8')
            data_bytes = data.encode('utf-8')
            hmac_obj = hmac.new(key_bytes, data_bytes, sha1)
            raw_hmac = hmac_obj.digest()
            return base64.b64encode(raw_hmac).decode('utf-8')
        except Exception as ex:
            raise RuntimeError(str(ex))

    def generate_signature(self, verb, uri, date, secret_key):
        string_to_sign = f"{verb} {uri}\n{date}"
        return self.hmac_sha1(secret_key, string_to_sign)

    def generate_authorization(self, verb, uri, date, appkey, secret_key):
        signature = self.generate_signature(verb, uri, date, secret_key)
        return self.AUTHORIZATION_FORMAT.format(appkey, signature)
    #整句合成
    def synthesize(self, text, voiceName, speed, volume, sampleRate, audioFormat, enableExtraVolume, subtitleMode, extendParams):
        url = self.getHost() + "/tts/v1/synthesis"
        sessionId = str(uuid.uuid4())
        date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        headers = {
            'Content-Type': 'application/json',
            'Date': date,
            'Authorization': self.generate_authorization("POST", "/tts/v1/synthesis", date, self.appKey, self.secretKey),
            'SessionID': sessionId
        }
        payload = {
            key: value for key, value in {
                "text": text,
                "voice_name": voiceName,
                "speed": speed,
                "volume": volume,
                "sample_rate": sampleRate,
                "audio_format": audioFormat,
                "enable_extra_volume": enableExtraVolume,
                "subtitle_mode": subtitleMode,
                "extend_params": extendParams,
                "src": "python-sdk"
            }.items() if value is not None
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if(response.status_code == 200):
            content_type = response.headers.get('content-type').strip().split(';')[0]
            if content_type == 'application/json':
                return SynthesizeResponse(response.json().get('errcode'), None, None, sessionId, None)
            else:
                return SynthesizeResponse(0, response.content, base64.b64decode(response.headers.get('Subtitles')).decode('utf-8'), sessionId, None)
        else:
            return SynthesizeResponse(400403, None, None, sessionId, None)

    def streamSynthesize(self, text, voiceName, speed, volume, sampleRate, audioFormat, enableExtraVolume, extendParams, callback):
        url = self.getHost() + "/tts/v1/stream"
        sessionId = str(uuid.uuid4())
        date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        headers = {
            'Content-Type': 'application/json',
            'Date': date,
            'Authorization': self.generate_authorization("POST", "/tts/v1/stream", date, self.appKey, self.secretKey),
            'SessionID': sessionId
        }
        payload = {
            key: value for key, value in {
                "text": text,
                "voice_name": voiceName,
                "speed": speed,
                "volume": volume,
                "sample_rate": sampleRate,
                "audio_format": audioFormat,
                "enable_extra_volume": enableExtraVolume,
                "extend_params": extendParams,
                "src": "python-sdk"
            }.items() if value is not None
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload), stream=True)
        # 处理响应结果
        if response.status_code == 200:
            content_type = response.headers.get('content-type').strip().split(';')[0]
            if content_type != 'application/json':
                for chunk in response.iter_content(chunk_size=3200):
                    if chunk:  # 过滤掉keep-alive的新块
                        callback.onSuc(sessionId, chunk)
            else:
                callback.onFail(sessionId, response.json().get('errcode'))
        else:
            callback.onFail(sessionId, 400403)

    def proxyStreamSynthesize(self, text, voiceName, speed, volume, sampleRate, audioFormat, enableExtraVolume, extendParams, proxyService, callback):
        url = self.getHost() + "/tts/v1/proxy/stream"
        sessionId = str(uuid.uuid4())
        date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        headers = {
            'Content-Type': 'application/json',
            'Date': date,
            'Authorization': self.generate_authorization("POST", "/tts/v1/proxy/stream", date, self.appKey, self.secretKey),
            'SessionID': sessionId
        }
        payload = {
            key: value for key, value in {
                "text": text,
                "voice_name": voiceName,
                "speed": speed,
                "volume": volume,
                "sample_rate": sampleRate,
                "audio_format": audioFormat,
                "enable_extra_volume": enableExtraVolume,
                "extend_params": extendParams,
                "proxy_service": proxyService,
                "src": "python-sdk"
            }.items() if value is not None
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload), stream=True)
        # 处理响应结果
        if response.status_code == 200:
            content_type = response.headers.get('content-type').strip().split(';')[0]
            if content_type != 'application/json':
                for chunk in response.iter_content(chunk_size=3200):
                    if chunk:  # 过滤掉keep-alive的新块
                        callback.onSuc(sessionId, chunk)
            else:
                callback.onFail(sessionId, response.json().get('errcode'))
        else:
            callback.onFail(sessionId, 400403)

    def streamTextSynthesize(self, sessionId, index, text, voiceName, speed, volume, sampleRate, enableExtraVolume, extendParams, tolerance, callback):
        url = self.getHost() + "/tts/v1/stream_text/submit"
        date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        headers = {
            'Content-Type': 'application/json',
            'Date': date,
            'Authorization': self.generate_authorization("POST", "/tts/v1/stream_text/submit", date, self.appKey, self.secretKey),
            'SessionID': sessionId
        }
        payload = {
            key: value for key, value in {
                "index": index,
                "text": text,
                "voice_name": voiceName,
                "speed": speed,
                "volume": volume,
                "sample_rate": sampleRate,
                "enable_extra_volume": enableExtraVolume,
                "extend_params": extendParams,
                "tolerance": tolerance,
                "src": "python-sdk"
            }.items() if value is not None
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if (response.status_code == 200):
            errcode = response.json().get('errcode')
            if errcode == 0 and index == 1:
                threading.Thread(target=self.pull_audio_stream, args=(sessionId, payload, callback)).start()
            elif errcode != 0:
                callback.onFail(sessionId, errcode)
        else:
            callback.onFail(400403, None, None, sessionId)

    def pull_audio_stream(self, sessionId, payload, callback):
        url = self.getHost() + "/tts/v1/audio/stream"
        date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        headers = {
            'Content-Type': 'application/json',
            'Date': date,
            'Authorization': self.generate_authorization("POST", "/tts/v1/audio/stream", date, self.appKey, self.secretKey),
            'SessionID': sessionId
        }

        with requests.post(url, headers=headers, data=json.dumps(payload), stream=True) as response:
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type').split(';')[0].strip()
                if content_type != 'application/json':
                    for chunk in response.iter_content(chunk_size=3200):
                        if chunk:
                            callback.onSuc(sessionId, chunk)
                else:
                    errcode = response.json().get('errcode')
                    callback.onFail(sessionId, errcode)
            else:
                callback.onFail(sessionId, 400403)


    def asyncLongTextSynthesize(self, text, voiceName, speed, volume, sampleRate, audioFormat, enableExtraVolume,
                                subtitleMode, extendParams, callbackAddr, expireSeconds):
        url = self.getHost() + "/async/v1/task_submit"
        sessionId = str(uuid.uuid4())
        date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        headers = {
            'Content-Type': 'application/json',
            'Date': date,
            'Authorization': self.generate_authorization("POST", "/async/v1/task_submit", date, self.appKey, self.secretKey),
            'SessionID': sessionId
        }
        requestParams = {
            key: value for key, value in {
                "text": text,
                "voice_name": voiceName,
                "speed": speed,
                "volume": volume,
                "sample_rate": sampleRate,
                "audio_format": audioFormat,
                "enable_extra_volume": enableExtraVolume,
                "subtitle_mode": subtitleMode,
                "extend_params": extendParams,
                "src": "python-sdk"
            }.items() if value is not None
        }
        requestParams = json.dumps(requestParams)
        payload = {
            key: value for key, value in {
                "data": text,
                "data_type": "text",
                "expire_seconds": expireSeconds,
                "api": "tts/v1/long_text/synthesis",
                "callback_addr": callbackAddr,
                "request_params": requestParams,
                "src": "python-sdk"
            }.items() if value is not None
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if(response.status_code == 200):
            return response.json().get('errcode')
        else:
            return 400403


    def proxySynthesize(self, text, voiceName, speed, volume, sampleRate, audioFormat, enableExtraVolume, subtitleMode, extendParams, proxyService):
        url = self.getHost() + "/tts/v1/proxy/synthesis"
        sessionId = str(uuid.uuid4())
        date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        headers = {
            'Content-Type': 'application/json',
            'Date': date,
            'Authorization': self.generate_authorization("POST", "/tts/v1/proxy/synthesis", date, self.appKey, self.secretKey),
            'SessionID': sessionId
        }
        payload = {
            key: value for key, value in {
                "text": text,
                "voice_name": voiceName,
                "speed": speed,
                "volume": volume,
                "sample_rate": sampleRate,
                "audio_format": audioFormat,
                "enable_extra_volume": enableExtraVolume,
                "subtitle_mode": subtitleMode,
                "extend_params": extendParams,
                "proxy_service": proxyService,
                "src": "python-sdk"
            }.items() if value is not None
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if(response.status_code == 200):
            content_type = response.headers.get('content-type').strip().split(';')[0]
            if content_type == 'application/json':
                return SynthesizeResponse(response.json().get('errcode'), None, None, sessionId, None)
            else:
                return SynthesizeResponse(0, response.content, base64.b64decode(response.headers.get('Subtitles')).decode('utf-8'),
                                          sessionId, base64.b64decode(response.headers.get('Extend-info-base64')).decode('utf-8'))
        else:
            return SynthesizeResponse(400403, None, None, sessionId, None)

    def getHost(self):
        if self.env == "prod":
            return "https://aispeech.sankuai.com"
        else:
            return "http://speechplatform.ai.test.sankuai.com"

class SynthesizeResponse:
    def __init__(self, errorCode, data, subtitle, sessionId, extendInfo):
        self.errorCode = errorCode
        self.data = data
        self.subtitle = subtitle
        self.sessionId = sessionId
        self.extendInfo = extendInfo


