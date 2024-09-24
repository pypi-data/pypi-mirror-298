# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: uauth_common.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12uauth_common.proto\x12\x08uauth_pb\"B\n\x12UauthLoginPassword\x12\x10\n\x08password\x18\x01 \x01(\t\x12\x0c\n\x04time\x18\x02 \x01(\x03\x12\x0c\n\x04rand\x18\x03 \x01(\x05\"\xc4\x01\n\rDeviceMessage\x12\x0c\n\x04oaid\x18\x01 \x01(\t\x12\x12\n\nandroid_id\x18\x02 \x01(\t\x12\x0c\n\x04idfa\x18\x03 \x01(\t\x12\x0c\n\x04idfv\x18\x04 \x01(\t\x12\x13\n\x0b\x61ppflyer_id\x18\x05 \x01(\t\x12\x0c\n\x04gaid\x18\x06 \x01(\t\x12\x18\n\x10referrer_user_id\x18\x07 \x01(\t\x12\x1f\n\x17\x61\x66_referrer_customer_id\x18\x08 \x01(\t\x12\x17\n\x0f\x61\x66_referrer_uid\x18\t \x01(\t*9\n\x0fUauthWeightType\x12\n\n\x06UWT_H5\x10\x00\x12\r\n\tUWT_INNER\x10\x01\x12\x0b\n\x07UWT_ALL\x10\x02*4\n\x0cUauthPayType\x12\n\n\x06UPT_WX\x10\x00\x12\x0b\n\x07UPT_ALI\x10\x01\x12\x0b\n\x07UPT_ALL\x10\x02*\x97\x03\n\x0fUPayChannelType\x12\r\n\tUPCT_NULL\x10\x00\x12\x11\n\rUPCT_ZFBZF_H5\x10\x02\x12\x12\n\x0eUPCT_ZFBZF_APP\x10\x03\x12\x11\n\rUPCT_WXZF_APP\x10\x04\x12\x10\n\x0cUPCT_WXZF_H5\x10\x05\x12\x0c\n\x08UPCT_IAP\x10\x06\x12\r\n\tUPCT_PLAY\x10\x08\x12\x0e\n\nUPCT_PALZF\x10\n\x12\x0e\n\nUPCT_BOING\x10\x0b\x12\x10\n\x0cUPCT_UNIONZF\x10\x0c\x12\x0f\n\x0bUPCT_CMBPAY\x10\r\x12\x0f\n\x0bUPCT_MYCARD\x10\x0e\x12\x13\n\x0fUPCT_ZFBZF_MINI\x10\x0f\x12\x11\n\rUPCT_PAYSSION\x10\x16\x12\x12\n\x0eUPCT_MYCARD_TW\x10\x17\x12\x12\n\x0eUPCT_MYCARD_HK\x10\x18\x12\x11\n\rUPCT_NEWEBPAY\x10\x19\x12\x0f\n\x0bUPCT_PAYMAX\x10\x1a\x12\x0e\n\nUPCT_E_COM\x10(\x12\x0f\n\nUPCT_AGENT\x10\xfd\x01\x12\x10\n\x0bUPCT_MANUAL\x10\xfe\x01\x12\x11\n\x0cUPCT_DEVTEST\x10\xff\x01*\xb3\x03\n\x10UauthAccountType\x12\n\n\x06\x41T_DEV\x10\x00\x12\r\n\tAT_NATIVE\x10\x01\x12\t\n\x05\x41T_QQ\x10\x02\x12\r\n\tAT_WEIXIN\x10\x03\x12\x13\n\x0f\x41T_CHINA_MOBILE\x10\n\x12\x14\n\x10\x41T_CHINA_TELECOM\x10\x0b\x12\x0c\n\x08\x41T_UMENG\x10\x0c\x12\r\n\tAT_GOOGLE\x10\x64\x12\x0f\n\x0b\x41T_FACEBOOK\x10\x65\x12\x0c\n\x08\x41T_CAIJI\x10\x66\x12\x0c\n\x08\x41T_APPLE\x10g\x12\x1a\n\x16\x41T_WECHAT_SUBSCRIPTION\x10h\x12\x16\n\x12\x41T_QQ_MINI_PROGRAM\x10i\x12\x16\n\x12\x41T_WX_MINI_PROGRAM\x10j\x12\r\n\tAT_QQ_WEB\x10k\x12\x11\n\rAT_WEIXIN_WEB\x10l\x12\r\n\x08\x41T_ROBOT\x10\xc8\x01\x12\x18\n\x13\x41T_PHONE_SUBSIDIARY\x10\xcb\x01\x12\r\n\x08\x41T_GUEST\x10\xcc\x01\x12\x0f\n\nAT_TWITTER\x10\xcd\x01\x12\r\n\x08\x41T_EMAIL\x10\xce\x01\x12\x0c\n\x07\x41T_LINE\x10\xcf\x01\x12\x11\n\x0c\x41T_OPERATION\x10\xd2\x01\x12\x0e\n\tAT_TIKTOK\x10\xd3\x01*\xde\x03\n\x0eUauthLoginType\x12\n\n\x06LT_DEV\x10\x00\x12\r\n\tLT_NATIVE\x10\x01\x12\t\n\x05LT_QQ\x10\x02\x12\r\n\tLT_WEIXIN\x10\x03\x12\n\n\x06LT_SMS\x10\x04\x12\x0c\n\x08LT_QUICK\x10\x05\x12\x0c\n\x08LT_APPLE\x10\x06\x12\x0f\n\x0bLT_FACEBOOK\x10\x07\x12\x15\n\x11LT_PHONE_PASSWORD\x10\x08\x12\x1a\n\x16LT_WECHAT_SUBSCRIPTION\x10\t\x12\r\n\tLT_GOOGLE\x10\n\x12\x17\n\x13LT_QQ_SMALL_PROGRAM\x10\x0b\x12\x16\n\x12LT_WX_MINI_PROGRAM\x10\x0c\x12\r\n\tLT_QQ_WEB\x10\r\x12\x11\n\rLT_WEIXIN_WEB\x10\x0e\x12\x0c\n\x08LT_GUEST\x10\x0f\x12\x0e\n\nLT_TWITTER\x10\x10\x12\n\n\x06LT_SES\x10\x11\x12\x15\n\x11LT_EMAIL_PASSWORD\x10\x12\x12\x15\n\x11LT_REMOTE_MESSAGE\x10\x13\x12\x16\n\x12LT_PROTECT_MESSAGE\x10\x14\x12\x17\n\x13LT_WECHAR_MINI_SCAN\x10\x15\x12\x0b\n\x07LT_LINE\x10\x16\x12\x10\n\x0cLT_BING_NEON\x10\x18\x12\r\n\tLT_TIKTOK\x10\x19\x12\x12\n\x0eLT_QRCODE_SCAN\x10\x17*\xff\x01\n\x0fUauthDeviceType\x12\x0e\n\nDT_UNKNOWN\x10\x00\x12\x12\n\x0e\x44T_FLASHPLAYER\x10\x01\x12\x14\n\x10\x44T_ANDROID_PHONE\x10\x14\x12\x10\n\x0c\x44T_IOS_PHONE\x10(\x12\x18\n\x14\x44T_WINDOWS_ASSISTANT\x10P\x12\x11\n\rDT_WINDOWS_PC\x10Z\x12\x0c\n\x08\x44T_ROBOT\x10\x64\x12\x1a\n\x16\x44T_WECHAT_SUBSCRIPTION\x10n\x12\x16\n\x12\x44T_QQ_MINI_PROGRAM\x10x\x12\x17\n\x12\x44T_WX_MINI_PROGRAM\x10\x82\x01\x12\x0b\n\x06\x44T_WEB\x10\x8c\x01\x12\x0b\n\x06\x44T_MAC\x10\x96\x01*1\n\x0cUauthSexType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x08\n\x04MAIL\x10\x01\x12\n\n\x06\x46\x45MAIL\x10\x02*K\n\x11UauthAccountFlags\x12\x0b\n\x07\x41\x46_ZERO\x10\x00\x12\x15\n\x11\x41\x46_PHONE_VERIFIED\x10\x01\x12\x12\n\x0e\x41\x46_BIND_DEVICE\x10\x02*9\n\rCommonRpcType\x12\x0e\n\nCRPCT_NONE\x10\x00\x12\x18\n\x14\x43RPCT_PayPalRefunded\x10\x01\x42\x08\xa2\x02\x05PROTOb\x06proto3')

_UAUTHWEIGHTTYPE = DESCRIPTOR.enum_types_by_name['UauthWeightType']
UauthWeightType = enum_type_wrapper.EnumTypeWrapper(_UAUTHWEIGHTTYPE)
_UAUTHPAYTYPE = DESCRIPTOR.enum_types_by_name['UauthPayType']
UauthPayType = enum_type_wrapper.EnumTypeWrapper(_UAUTHPAYTYPE)
_UPAYCHANNELTYPE = DESCRIPTOR.enum_types_by_name['UPayChannelType']
UPayChannelType = enum_type_wrapper.EnumTypeWrapper(_UPAYCHANNELTYPE)
_UAUTHACCOUNTTYPE = DESCRIPTOR.enum_types_by_name['UauthAccountType']
UauthAccountType = enum_type_wrapper.EnumTypeWrapper(_UAUTHACCOUNTTYPE)
_UAUTHLOGINTYPE = DESCRIPTOR.enum_types_by_name['UauthLoginType']
UauthLoginType = enum_type_wrapper.EnumTypeWrapper(_UAUTHLOGINTYPE)
_UAUTHDEVICETYPE = DESCRIPTOR.enum_types_by_name['UauthDeviceType']
UauthDeviceType = enum_type_wrapper.EnumTypeWrapper(_UAUTHDEVICETYPE)
_UAUTHSEXTYPE = DESCRIPTOR.enum_types_by_name['UauthSexType']
UauthSexType = enum_type_wrapper.EnumTypeWrapper(_UAUTHSEXTYPE)
_UAUTHACCOUNTFLAGS = DESCRIPTOR.enum_types_by_name['UauthAccountFlags']
UauthAccountFlags = enum_type_wrapper.EnumTypeWrapper(_UAUTHACCOUNTFLAGS)
_COMMONRPCTYPE = DESCRIPTOR.enum_types_by_name['CommonRpcType']
CommonRpcType = enum_type_wrapper.EnumTypeWrapper(_COMMONRPCTYPE)
UWT_H5 = 0
UWT_INNER = 1
UWT_ALL = 2
UPT_WX = 0
UPT_ALI = 1
UPT_ALL = 2
UPCT_NULL = 0
UPCT_ZFBZF_H5 = 2
UPCT_ZFBZF_APP = 3
UPCT_WXZF_APP = 4
UPCT_WXZF_H5 = 5
UPCT_IAP = 6
UPCT_PLAY = 8
UPCT_PALZF = 10
UPCT_BOING = 11
UPCT_UNIONZF = 12
UPCT_CMBPAY = 13
UPCT_MYCARD = 14
UPCT_ZFBZF_MINI = 15
UPCT_PAYSSION = 22
UPCT_MYCARD_TW = 23
UPCT_MYCARD_HK = 24
UPCT_NEWEBPAY = 25
UPCT_PAYMAX = 26
UPCT_E_COM = 40
UPCT_AGENT = 253
UPCT_MANUAL = 254
UPCT_DEVTEST = 255
AT_DEV = 0
AT_NATIVE = 1
AT_QQ = 2
AT_WEIXIN = 3
AT_CHINA_MOBILE = 10
AT_CHINA_TELECOM = 11
AT_UMENG = 12
AT_GOOGLE = 100
AT_FACEBOOK = 101
AT_CAIJI = 102
AT_APPLE = 103
AT_WECHAT_SUBSCRIPTION = 104
AT_QQ_MINI_PROGRAM = 105
AT_WX_MINI_PROGRAM = 106
AT_QQ_WEB = 107
AT_WEIXIN_WEB = 108
AT_ROBOT = 200
AT_PHONE_SUBSIDIARY = 203
AT_GUEST = 204
AT_TWITTER = 205
AT_EMAIL = 206
AT_LINE = 207
AT_OPERATION = 210
AT_TIKTOK = 211
LT_DEV = 0
LT_NATIVE = 1
LT_QQ = 2
LT_WEIXIN = 3
LT_SMS = 4
LT_QUICK = 5
LT_APPLE = 6
LT_FACEBOOK = 7
LT_PHONE_PASSWORD = 8
LT_WECHAT_SUBSCRIPTION = 9
LT_GOOGLE = 10
LT_QQ_SMALL_PROGRAM = 11
LT_WX_MINI_PROGRAM = 12
LT_QQ_WEB = 13
LT_WEIXIN_WEB = 14
LT_GUEST = 15
LT_TWITTER = 16
LT_SES = 17
LT_EMAIL_PASSWORD = 18
LT_REMOTE_MESSAGE = 19
LT_PROTECT_MESSAGE = 20
LT_WECHAR_MINI_SCAN = 21
LT_LINE = 22
LT_BING_NEON = 24
LT_TIKTOK = 25
LT_QRCODE_SCAN = 23
DT_UNKNOWN = 0
DT_FLASHPLAYER = 1
DT_ANDROID_PHONE = 20
DT_IOS_PHONE = 40
DT_WINDOWS_ASSISTANT = 80
DT_WINDOWS_PC = 90
DT_ROBOT = 100
DT_WECHAT_SUBSCRIPTION = 110
DT_QQ_MINI_PROGRAM = 120
DT_WX_MINI_PROGRAM = 130
DT_WEB = 140
DT_MAC = 150
UNKNOWN = 0
MAIL = 1
FEMAIL = 2
AF_ZERO = 0
AF_PHONE_VERIFIED = 1
AF_BIND_DEVICE = 2
CRPCT_NONE = 0
CRPCT_PayPalRefunded = 1


_UAUTHLOGINPASSWORD = DESCRIPTOR.message_types_by_name['UauthLoginPassword']
_DEVICEMESSAGE = DESCRIPTOR.message_types_by_name['DeviceMessage']
UauthLoginPassword = _reflection.GeneratedProtocolMessageType('UauthLoginPassword', (_message.Message,), {
  'DESCRIPTOR' : _UAUTHLOGINPASSWORD,
  '__module__' : 'uauth_common_pb2'
  # @@protoc_insertion_point(class_scope:uauth_pb.UauthLoginPassword)
  })
_sym_db.RegisterMessage(UauthLoginPassword)

DeviceMessage = _reflection.GeneratedProtocolMessageType('DeviceMessage', (_message.Message,), {
  'DESCRIPTOR' : _DEVICEMESSAGE,
  '__module__' : 'uauth_common_pb2'
  # @@protoc_insertion_point(class_scope:uauth_pb.DeviceMessage)
  })
_sym_db.RegisterMessage(DeviceMessage)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\242\002\005PROTO'
  _UAUTHWEIGHTTYPE._serialized_start=299
  _UAUTHWEIGHTTYPE._serialized_end=356
  _UAUTHPAYTYPE._serialized_start=358
  _UAUTHPAYTYPE._serialized_end=410
  _UPAYCHANNELTYPE._serialized_start=413
  _UPAYCHANNELTYPE._serialized_end=820
  _UAUTHACCOUNTTYPE._serialized_start=823
  _UAUTHACCOUNTTYPE._serialized_end=1258
  _UAUTHLOGINTYPE._serialized_start=1261
  _UAUTHLOGINTYPE._serialized_end=1739
  _UAUTHDEVICETYPE._serialized_start=1742
  _UAUTHDEVICETYPE._serialized_end=1997
  _UAUTHSEXTYPE._serialized_start=1999
  _UAUTHSEXTYPE._serialized_end=2048
  _UAUTHACCOUNTFLAGS._serialized_start=2050
  _UAUTHACCOUNTFLAGS._serialized_end=2125
  _COMMONRPCTYPE._serialized_start=2127
  _COMMONRPCTYPE._serialized_end=2184
  _UAUTHLOGINPASSWORD._serialized_start=32
  _UAUTHLOGINPASSWORD._serialized_end=98
  _DEVICEMESSAGE._serialized_start=101
  _DEVICEMESSAGE._serialized_end=297
# @@protoc_insertion_point(module_scope)
