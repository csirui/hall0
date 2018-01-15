'''
Created on 2013-3-22
@author: Administrator
'''
import base64
import os
import traceback

from Crypto.Hash import SHA, MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from OpenSSL.crypto import load_privatekey, FILETYPE_PEM, load_certificate, sign, verify
from cffi import FFI

from tyframework.context import TyContext

# jinli public key
JINLI_PUB_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCeJl4Tb7mYtQb9u7/q9n4EjfM9
qZZdD7Uy4ME5gQ6P4oUZOXqWNCY/If5JNt9zppPfkmcTMCBOkkRPAnTinyh/nLft
dDClMaK2xbVgX5RBS178YQzlq7iGcGs7uLSu9Fg/BDeFgJopnt0jbaBfAYeTWCBa
mDYkFQxpv2CN0O6DeQIDAQAB
-----END PUBLIC KEY-----'''

# aliprivate.pem
ALIPAY_PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBAOIc0bKk2wj6nA2F
zd59LDfhXJGlurRs+GzYPKtKKjyMLVxq/PDLOahkiYNzaOBeWFa4smtdFZdd39sg
HCyqoMkVTSR1KGZHiiPrlUEoIdwYI+iS7vRvwPk4RkN7C/gL1OKZ1P6/EhCb/R5w
J1zfymiRd1iv3ztDL+0dLOlOcbklAgMBAAECgYEAtSPNQkYbSugpmBO3RyQUBng+
Blg0aFJb+iaJA9gYWgUaWc1D8Ut9V0+jcnFEdWpfbqnsFWKu52JG8W6Z45aV0sAD
voMHe0DzB+OD4nqgObG/lFZif3vSWEyN+UIxmW+Eu+nOyR/PHUD6W0Etg5B47W2r
qzpXEzU2zfknwM7uWsECQQDytNtBxeMg2Y5w82WU+GuMtaFNIAe6g+YreEKEn6Tm
bU266x8HCktXsSP1jKSt4GpvkLDUB5zOa+HZobnuVkmZAkEA7n9J+iP7JcMPU+X8
O1nxzsMe103gfzQaGyiIVtPLoHHkZU/2kJ8O3WBAcS4glJ8ZBoqQJs3yel+GNSar
2MNbbQJBAKondVgFXhjXrW8ulNb92pjJdY5WmFSAyEtNgoTsT3VkyAv1bslGxE90
Vxt9QK7OGJCixfXAaISnSa2EHpAjWnECQGzeNgq1OgO20txdc5I0MKlNcFqf9gaa
5f/XtMTN0XngA34rzkWeFc8ADOqdP8oYBfhyb/MGt9UcncrNaEx+gNECQQDXYEhX
ZEptZMm3nb2tj0u//kOEgfnVqu18/pfFbJOyXjRqoIya46hMvzEcEvq0dND5bdhP
8mIud7No5ZelmAPn
-----END RSA PRIVATE KEY-----'''

# get public key from private key,for testing...
# openssl rsa -in aliprivate.pem -pubout -out alipublic.pem
# alipublic.pem
ALIPAY_PUB_KEY_TUYOO = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDiHNGypNsI+pwNhc3efSw34VyR
pbq0bPhs2DyrSio8jC1cavzwyzmoZImDc2jgXlhWuLJrXRWXXd/bIBwsqqDJFU0k
dShmR4oj65VBKCHcGCPoku70b8D5OEZDewv4C9TimdT+vxIQm/0ecCdc38pokXdY
r987Qy/tHSzpTnG5JQIDAQAB
-----END PUBLIC KEY-----'''

# public key from ali,KEY SWAP!!!
ALIPAY_PUB_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCStnZ2gtxZW8GdetfCxwiz7jkd
XF9RFaEV7GyU uXEvC9ss5di6SWHkieKccJhBCOULujkADKDXO2uEurjIRIQMufA
jaBbNNSIoMa+u72R252BQrocv hILmd2hUur9P+s4dPg3lFqAEPiJtrEJQo/Anxn
hFqm7scnl+BuMfYA0nwwIDAQAB
-----END PUBLIC KEY-----'''

JOLO_PUB_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDbRLzWfCD4pQb1mjeGLy6gw+Af
OKZ1dpNbMUyZml+p3stTSdTyHHpkuPPsaOqsT9gFDSmXz5KRBt4w6KCeLj/R61KA
5rmMJipDnSJV19kld0z6NW47kiEQHslaalDBCST94TUIcCzjhaiG3yTChDCTFo3v
47qyt6j3YvVpih8UNQIDAQAB
-----END PUBLIC KEY-----'''

CHANGBA_PUB_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDEfjMO0XZsHrnAQKECxYFc0FX3
wbz6cEDf5GUEbktaPOlcJJhuDrb1Tp8LtmZ/28i5ENkSFDE4d2bJV8Koj5E0y9XT
39NcV3XqzbNHNcGr73wpURkkPDzYIGaHYHSQha13FD8DdByDT34narPVlcxtTrWn
bj4Z+09EEgaCMUKWvwIDAQAB
-----END PUBLIC KEY-----'''

WANDOUJIA_PUB_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCd95FnJFhPinpNiE/h4VA6bU1r
zRa5+a25BxsnFX8TzquWxqDCoe4xG6QKXMXuKvV57tTRpzRo2jeto40eHKClzEgj
x9lTYVb2RFHHFWio/YGTfnqIPTVpi7d7uHY+0FZ0lYL5LlW4E2+CQMxFOPRwfqGz
Mjs1SDlH7lVrLEVy6QIDAQAB
-----END PUBLIC KEY-----'''

JUSDK_PUB_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDYoLXLI6SZJD9p9o5c+lrvVcBw
Wq7t16qLE1701pZNXsHc6yxU6sQnIbU7yd1UpnmJxvgcN7sNImnyiTeIRRz4fvtD
taSMGBoFHPi4Z16kL33eC0Shn8Vajz9KUjhQfKIjVsg54+p5yicWm8wPLIEQT2R3
EjihbHJ6PUG9paupWQIDAQAB
-----END PUBLIC KEY-----'''

# get cert for verify from private key,for testing...
# openssl req -new -x509 -key aliprivate.pem -out cacert.pem -days 1095
# alicert.pem
ALIPAY_CERT = '''-----BEGIN CERTIFICATE-----
MIICfDCCAeWgAwIBAgIJAIyGyXVCWgG0MA0GCSqGSIb3DQEBBQUAMFcxCzAJBgNV
BAYTAmNuMQswCQYDVQQIDAJiajELMAkGA1UEBwwCYmoxDjAMBgNVBAoMBXR1eW9v
MQ4wDAYDVQQLDAV0dXlvbzEOMAwGA1UEAwwFdHV5b28wHhcNMTQwNTIwMTQyMTMx
WhcNMTcwNTE5MTQyMTMxWjBXMQswCQYDVQQGEwJjbjELMAkGA1UECAwCYmoxCzAJ
BgNVBAcMAmJqMQ4wDAYDVQQKDAV0dXlvbzEOMAwGA1UECwwFdHV5b28xDjAMBgNV
BAMMBXR1eW9vMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDiHNGypNsI+pwN
hc3efSw34VyRpbq0bPhs2DyrSio8jC1cavzwyzmoZImDc2jgXlhWuLJrXRWXXd/b
IBwsqqDJFU0kdShmR4oj65VBKCHcGCPoku70b8D5OEZDewv4C9TimdT+vxIQm/0e
cCdc38pokXdYr987Qy/tHSzpTnG5JQIDAQABo1AwTjAdBgNVHQ4EFgQUoBmgDNGh
xa2sePJsPR2ju2JPHaAwHwYDVR0jBBgwFoAUoBmgDNGhxa2sePJsPR2ju2JPHaAw
DAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQUFAAOBgQB9EFh/mB99YAADQrkiXB5g
BYZBdrAD0yjqg0DSPpmHooE20RPhajl1yc+2tI4QMSHoORnboXR2CYTbiUtS+5q+
LmKwO/MkhnlrN/7oJqahEj4U3nGdfIQJSIntHEvzTXLxCEt0cNDfcGyW8GwHYTwz
LTiaz87yjytQsYTJSYiTTg==
-----END CERTIFICATE-----'''

SHEDIAO_ALIPAY_PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDcGCg29NnHMXIaFGLdyWPwY6yA2h9dPny3C1n7cRqHzNCKr9iK
T4qNv0PG1KEr9aVkVZBIXjy8/3r4SrkKVPDWxU3hMUpEit/XAmkBqJ660OY9oySE
8qhjhZQzKWJiRopOobQEX4icQOFytLpRiSZ6R91yCVMlgYGwbIh9G8jnMwIDAQAB
AoGBAJQHM1TzDV3ppaJgv7YHc04E28q16Y5fLqY13kk84ukfGcuNRYiQwtFfKIic
DeJxDtISsj3aE+PRuLUyHI4UXv302kzsrPZarJ6ESTS6PEKeT6b4qDPbOub9XsXf
/8bLu+5DJkM7IUfggA5pocU3/ShX/JHL1ZU3p/b7Nf99OHahAkEA73ppMX59cBNj
qT6NSAfIB2wYUoqyHmLD9E2ufta7gAFnVSDVK+F9xLH3Y+IsW314MMk0RRvXpyCK
HBcRedXbSwJBAOtHZTvrfpPyCz4UWAm+kJh391Z7tmWmi0Xs4joMfS6qfBdEYXp1
pz0lpkLYo8ex24HtYEw9hii7jTA0HrS1irkCQERzvA/etSJNGIavD5lQSBf/CPDH
HmTbHGH/tmohHRVY0V2e9fAGE3oe2LUfWEiKk8l2Kc+7RqhJ/9BJs8AcpgMCQQDo
W0skIQ+R5qGpvoevn+7HVPsFAwqAWzkCZs6Iy5q5go8on1Sxjw4J+mu3aqJc7k69
gwPuZ3heM9Nc/qwwhXWpAkAp/f2wfpK1tTA1v8u9lBqIFt2wWjUYrefXy3udX1MH
KR0ZAWU12YuyCeBdiYgWCNRWVszUAQjVJA+mpSb4ZYUy
-----END RSA PRIVATE KEY-----'''

SHEDIAO_ALIPAY_PUB_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCnxj/9qwVfgoUh/y2W89L6BkRA
FljhNhgPdyPuBV64bfQNN1PjbCzkIM6qRdKBoLPXmKKMiFYnkd6rAoprih3/PrQE
B/VsW8OoM8fxn67UDYuyBTqA23MML9q1+ilIZwBC2AQ2UBVOrFXfFl75p6/B5Ksi
NG9zpgmLCUYuLkxpLQIDAQAB
-----END PUBLIC KEY-----'''

SHEDIAO_ALIPAY_CERT = '''-----BEGIN CERTIFICATE-----
MIIChjCCAe+gAwIBAgIJAO97O0Oal26ZMA0GCSqGSIb3DQEBBQUAMFwxCzAJBgNV
BAYTAkNOMRAwDgYDVQQIDAdCZWlKaW5nMQswCQYDVQQHDAJiajEOMAwGA1UECgwF
dHV5b28xDjAMBgNVBAsMBXR1eW9vMQ4wDAYDVQQDDAV0dXlvbzAeFw0xNDA1MjEw
MTM2NThaFw0xNzA1MjAwMTM2NThaMFwxCzAJBgNVBAYTAkNOMRAwDgYDVQQIDAdC
ZWlKaW5nMQswCQYDVQQHDAJiajEOMAwGA1UECgwFdHV5b28xDjAMBgNVBAsMBXR1
eW9vMQ4wDAYDVQQDDAV0dXlvbzCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEA
3BgoNvTZxzFyGhRi3clj8GOsgNofXT58twtZ+3Eah8zQiq/Yik+Kjb9DxtShK/Wl
ZFWQSF48vP96+Eq5ClTw1sVN4TFKRIrf1wJpAaieutDmPaMkhPKoY4WUMyliYkaK
TqG0BF+InEDhcrS6UYkmekfdcglTJYGBsGyIfRvI5zMCAwEAAaNQME4wHQYDVR0O
BBYEFFuNW3L4cyBiEl4vl437Ux2SAsRdMB8GA1UdIwQYMBaAFFuNW3L4cyBiEl4v
l437Ux2SAsRdMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADgYEAKqFhMLvd
jAD9WG9lNEjVYiaI8zfuz44fNUQNvMQZslSLd8IXu960KBXnyjvDKlitDTYxhWSA
bJL4kst3r7QLkhFKsGkA66YVISLp5FKALVfJQ4TkBkCnoHqfrz3x44Hxs4kPvd0d
wMYESyYLOB2JogeVDqgME6IKSF8D88CF1p8=
-----END CERTIFICATE-----'''

OPPO_PUB_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCmreYIkPwVovKR8rLHWlFVw7YD
fm9uQOJKL89Smt6ypXGVdrAKKl0wNYc3/jecAoPi2ylChfa2iRu5gunJyNmpWZzl
CNRIau55fxGW0XEu553IiprOZcaw5OuYGlf60ga8QT6qToP0/dpiL/ZbmNUO9kUh
osIjEu22uFgR+5cYyQIDAQAB
-----END PUBLIC KEY-----'''

HUAFUBAO_PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQDNNwIEQ/vk53CTKtfi2HSaE5lU6IvL+/MTAc6Gn8gvilLfP5jU
VPBzPdNeFZPH4e/0S6FrIzMTP/iv3hLQpa1Va3HsKe2CrO00zA4cLp2SIxvSQNXB
rSfrTohIVif2T3+Yhz/oX6wfI2bfIb6uc7p1vsSWsssmA2CmlCo4FQ+e2wIDAQAB
AoGAZ6U8s4LSmk36IZol50CDw73aV3QMBz59CkCDWqMgrEIkkPTB75vmxY2YT5B+
Txnh43S/Vik1BqfspoZ24kKLRA0UdV5HF2CSbM3nCf7y9fSvpDMIEOySB5ZMKw3t
eBowe7gax4HFg5J3yigiCfe8tBSZyscT+M5ILQRqKyYQJ4ECQQD2uGL9ipyzu56u
j8PG2Ix92fjeZVHIfNuwXll3OlOTUuwpQMAvvDygkz891953m69M65ZwJTUyYiBK
M7U4AigRAkEA1O75qyE8+DiBaobaikGoj2dWYOPscFrXX2U6XuijooYIxSaapfO9
0gd4KxXJ8EA4EImnT57LlRACVwZC4oikKwJBANvOosLof3vRqCo1g2LhAyoMzKC2
/An203NqW6LRoCwdMLIAMjlVJ16YUTuz20wMtD1/luQLAj4FFmeFceqYYUECQQCX
l16Vr38ZdBjmfwUcwqu/FCGRrxJH1tRXrNiGcvb0IJojyVz14nX0Da9GdSej7AQ9
+dHsRC/JenFABUwevIqrAkEAtFggYorv14BjhrDj037MnbuvEUbnkwAmo/qXR7kx
/SCj+XNrH5ELAjgvXmMDoJaayiLnaOKY7bcRb9ZddB/AqA==
-----END RSA PRIVATE KEY-----'''

HUAFUBAO_CERT_KEY = '''-----BEGIN CERTIFICATE-----
MIIDNDCCAp2gAwIBAgICLVkwDQYJKoZIhvcNAQEFBQAwPTEOMAwGA1UEBhMFQ0hJ
TkExKzApBgNVBAMTIkNISU5BVEVMRUNPTSBDRVJUSUZJQ0FURSBBVVRIT1JJVFkw
HhcNMDEwMzIxMTA0NzEzWhcNMDMwMzIxMTA0NzEzWjBcMQswCQYDVQQGEwJDTjER
MA8GA1UEChMItPPBrLXn0MUxETAPBgNVBAgTCFNoZW55YW5nMRQwEgYDVQQDEwsx
OTIuMTY4LjIuMjERMA8GA1UEBxMIU2hlbnlhbmcwgZ8wDQYJKoZIhvcNAQEBBQAD
gY0AMIGJAoGBAMZYC7inporVKJCo0pPWdOBjADxzPRF1719G2YskDHVDEuqt6sBR
WX+65dXs1AVKROKmi6jdzAQSlp7z3brsB4skHMo9sqdQgPolgZvCersKJFHgTbjj
NyCoTyOjwOeRsfcqSJaiehQwPW4fLpNQW/lbvOuFrP8Tn0xWZvOunVPDAgMBAAGj
ggEiMIIBHjAJBgNVHRMEAjAAMEYGA1UdHwQ/MD0wO6A5oDeGNWxkYXA6Ly8yMDIu
MTAzLjY1LjE4L291PWNhLG91PXN5c3RlbSxvdT1jYTEsbz1jdCxjPUNOMC8GCCsG
AQUFBwEBBCMwITAfBggrBgEFBQcwAYYTLDIwMi4xMDMuNjUuMTg6OTAwMzAPBghg
hkgBhvhDDAQDAgEBMBIGCGCGSAGG+EMOBAYWBDI3RjkwGQYIYIZIAYb4QxAEDRYL
MTkyLjE2OC4yLjIwEAYIYIZIAYb4QxEEBBYCTlQwGgYIYIZIAYb4QxkEDhYMOTe9
ybfRt/7O8cb3MBkGCGCGSAGG+EMbBA0WCzE5Mi4xNjguMi4yMA8GCGCGSAGG+EMa
BAMCAQMwDQYJKoZIhvcNAQEFBQADgYEAckkH/Vem5+kXPSGgkowjPwv47XXNbD0h
GRMTVXm5PC2kY/wNApQh3lv7Tf5k3UQEoFBACxf6XJtuxf6S0uKBS4ySMKdpbMbO
Uvtwu6ycQUQTRAs1EBgoh1zyuafU2D3iyHQM8etHxaSePXZOZXFkkvBJemyPz23H
AyIn5SKQ2Es=
-----END CERTIFICATE-----'''

iTools_pubkey_str = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC2kcrRvxURhFijDoPpqZ/IgPlA
gppkKrek6wSrua1zBiGTwHI2f+YCa5vC1JEiIi9uw4srS0OSCB6kY3bP2DGJagBo
Egj/rYAGjtYJxJrEiTxVs5/GfPuQBYmU0XAtPXFzciZy446VPJLHMPnmTALmIOR5
Dddd1Zklod9IQBMjjwIDAQAB
-----END PUBLIC KEY-----'''

KUAIYONGPINGGUO_PUB_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCf95qPwV3SWSuBHXiYnm1coHWe
d3uVmAal81XZ+ELj1nfRkTl9EX7NIBH4bPxzLi6mhAp6QT3CoscorT2NyWVLW/wo
424qRW7ytH/MXstMCiurZdTyygsZtiKuD9DhIhQwNZ9G0pyQ7YtYPCEM5ffRrY6s
kgVylIiX1OFxV0XB+QIDAQAB
-----END PUBLIC KEY-----'''

aisi_pubkey_str = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCaOPvswjMFqCSsEG8aNhojc2UORldE2IMLqj0O
qHQSgktt9dFsLAlhr20BFUyzDQ1ZDzXwI9op/xHqaJwCGCrForJ+plACnhwzziI3l1YobsZFvdGE
Pr7B+inFS41TD5LXgDt8pOXiPo8F6vNqnitJHcOFunyukJ0NaYKvFLlr2wIDAQAB
-----END PUBLIC KEY-----'''

### union pay key
UNIONPAY_PRIVATE_KEY = '''-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCbqN3354qu9RWX
naHoU7xIKc9zPXh5hv22GmwsgZdsPD9rbboqX//itB7a/qBpXZ7ZT82RXN0yj6DW
B81Bf2tgzMG2wg8C8KDF/aX0nLD49M9IMPU+a/sCvPpBUApgQt/62J1c9282Vn/N
gWyZGOZbSLdH43f3g9T7KVGYkNgnRQdbOWMt4U26XYMqjwaX+yvJFquzJ3zYc9D/
j8GloPy8WMbjnigN4hFhuJtOWO/PIW2gJwS4bPcQKBXg+f/zzFmBQ6k96ojdJKTh
OaO0nO6SFHdwVt3BXwBpFd0QUITsSWhZ6gPcTkmWa0c1KIGi+IWuH3n99uuLjD1C
0yzZM+BDAgMBAAECggEAUmfQsvgiREM9Xhm2aC9EQxPXXlPRnsynLivIzrsAde1j
SbU6VEqkRdlDaH5aX82PVc5Yrrbx512AMS7KK/2P1BwyBVWw6saG5qpEnD4Dtpir
z7UTcCtsJGP1PHRqOdHNj5fznw7jEmoymJIG8vnqobLaTLWQgjmJnDmgl9s+g3LE
w9yLrU4qLdHX5ekjftBj9wREXfdZud5BsgByAg30D6dcEGFxHpygZPgbaJA9a096
DR3tEublQnMgwnz6FIamyVhMFSiK5euRfQYz4MftVpG0n2za4yfCcjuatyoIEyZn
3XlzRqotHzHuqERcYN3sgnpUFGcfjj4Cd6UVi4wusQKBgQDYoKozK1n89fGvk706
QIOVTbzwQrxGJ57dwnmNTdHAlJcZT5eNXeMhUWpGK9RDhVejfoH8uHRFkPe5+7DW
mphPU41z1Y0iZD5JaNohwmxFxvvOfCYm1AMS2WROE6nSbBXnFHFc/++s9TEbnSBY
GMoXOqtnrq7v5XnlVFGC+whOSQKBgQC383XvHcdjNr6s4+kkHDuScVfr7fID6OMX
Or1DT3q4RfvHcw/acghJT4eFbDfY6OxGP+WjAMprye5dBSBWyDVstG/MjBg/bcMZ
cxtna4/Vt8dkDTrMfMHSYO9kNwhKw5BqfpvVsRzr/50ae0FZUmHdYpKImQdVB7r9
lVybXUDqKwKBgHrs6MfykLT3xzbPyjA1DbX6j/1ykS3qK79BLQKfJyh16SwmuyQw
I8PzVDAPjPrnvqx7DD4hWXFkav6xsU6GGWniSsFxbA4Y/jNf+W/wyMnruVYZovij
lD7s93tKszJBvUgMlKumXBY0aLJ3vjPflUYLN9q1CHX/LOWSrFJ8KuFpAoGAEoRC
WdiQio8nMHYcsNLauEoKhKhGFVirC1qRVKY6fzQkPRZ7AQ07gk2sIaUcFgyURBoI
fpkEx0bjZJ+weqvanN+o5Vkw06mz2ur4VjfAmc3PF2YxhgYE6K1zS44ymnwHHIE0
JJWYiLUJVnITyO7/BO74OyHUWB3YF9CiKs1/TFMCgYBD071Fqmnvtl4gfQWa9TSG
TvCGeJt5s99JxL2h87X1NjJfg0d/QHOIQzcBybuffFHpRJLs6uW2ZwHSquJvwQZj
WTqQgyZfqi/xcQCSy3/jihPJxgF9FKTbgRdrGgxbWqbOrO/Gxwzrp9dRDmn+mKux
R4laPJuBO5SGI4b0M1008g==
-----END PRIVATE KEY-----'''

UNIONPAY_CERT_KEY = '''-----BEGIN CERTIFICATE-----
MIIEIDCCAwigAwIBAgIFEDRVM3AwDQYJKoZIhvcNAQEFBQAwITELMAkGA1UEBhMC
Q04xEjAQBgNVBAoTCUNGQ0EgT0NBMTAeFw0xNTEwMjcwOTA2MjlaFw0yMDEwMjIw
OTU4MjJaMIGWMQswCQYDVQQGEwJjbjESMBAGA1UEChMJQ0ZDQSBPQ0ExMRYwFAYD
VQQLEw1Mb2NhbCBSQSBPQ0ExMRQwEgYDVQQLEwtFbnRlcnByaXNlczFFMEMGA1UE
Aww8MDQxQDgzMTAwMDAwMDAwODMwNDBA5Lit5Zu96ZO26IGU6IKh5Lu95pyJ6ZmQ
5YWs5Y+4QDAwMDE2NDkzMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA
tXclo3H4pB+Wi4wSd0DGwnyZWni7+22Tkk6lbXQErMNHPk84c8DnjT8CW8jIfv3z
d5NBpvG3O3jQ/YHFlad39DdgUvqDd0WY8/C4Lf2xyo0+gQRZckMKEAId8Fl6/rPN
HsbPRGNIZgE6AByvCRbriiFNFtuXzP4ogG7vilqBckGWfAYaJ5zJpaGlMBOW1Ti3
MVjKg5x8t1/oFBkpFVsBnAeSGPJYrBn0irfnXDhOz7hcIWPbNDoq2bJ9VwbkKhJq
Vz7j7116pziUcLSFJasnWMnp8CrISj52cXzS/Y1kuaIMPP/1B0pcjVqMNJjowooD
OxID3TZGfk5V7S++4FowVwIDAQABo4HoMIHlMB8GA1UdIwQYMBaAFNHb6YiC5d0a
j0yqAIy+fPKrG/bZMEgGA1UdIARBMD8wPQYIYIEchu8qAQEwMTAvBggrBgEFBQcC
ARYjaHR0cDovL3d3dy5jZmNhLmNvbS5jbi91cy91cy0xNC5odG0wNwYDVR0fBDAw
LjAsoCqgKIYmaHR0cDovL2NybC5jZmNhLmNvbS5jbi9SU0EvY3JsMjI3Mi5jcmww
CwYDVR0PBAQDAgPoMB0GA1UdDgQWBBTEIzenf3VR6CZRS61ARrWMto0GODATBgNV
HSUEDDAKBggrBgEFBQcDAjANBgkqhkiG9w0BAQUFAAOCAQEAHMgTi+4Y9g0yvsUA
p7MkdnPtWLS6XwL3IQuXoPInmBSbg2NP8jNhlq8tGL/WJXjycme/8BKu+Hht6lgN
Zhv9STnA59UFo9vxwSQy88bbyui5fKXVliZEiTUhjKM6SOod2Pnp5oWMVjLxujkk
WKjSakPvV6N6H66xhJSCk+Ref59HuFZY4/LqyZysiMua4qyYfEfdKk5h27+z1MWy
nadnxA5QexHHck9Y4ZyisbUubW7wTaaWFd+cZ3P/zmIUskE/dAG0/HEvmOR6CGlM
55BFCVmJEufHtike3shu7lZGVm2adKNFFTqLoEFkfBO6Y/N6ViraBilcXjmWBJNE
MFF/yA==
-----END CERTIFICATE-----'''

# for pycrypto...
_ali_privkey_py = RSA.importKey(ALIPAY_PRIVATE_KEY)
_shediao_privkey_py = RSA.importKey(SHEDIAO_ALIPAY_PRIVATE_KEY)
_huafubao_privkey_py = RSA.importKey(HUAFUBAO_PRIVATE_KEY)
_ali_pubkey_py = RSA.importKey(ALIPAY_PUB_KEY)
_ali_pubkey_tuyoo_py = RSA.importKey(ALIPAY_PUB_KEY_TUYOO)
_shediao_pubkey_py = RSA.importKey(SHEDIAO_ALIPAY_PUB_KEY)
_oppo_pubkey_py = RSA.importKey(OPPO_PUB_KEY)
_jinli_pubkey_py = RSA.importKey(JINLI_PUB_KEY)
_iTools_pubkey_py = RSA.importKey(iTools_pubkey_str)
_kuaiyongpingguo_pubkey_py = RSA.importKey(KUAIYONGPINGGUO_PUB_KEY)
_unionpay_private_key = RSA.importKey(UNIONPAY_PRIVATE_KEY)
_jolo_pubkey_py = RSA.importKey(JOLO_PUB_KEY)
_changba_pubkey_py = RSA.importKey(CHANGBA_PUB_KEY)
_wandoujia_pubkey_py = RSA.importKey(WANDOUJIA_PUB_KEY)
_jusdk_public_py = RSA.importKey(JUSDK_PUB_KEY)

# for openssl...
try:
    _ali_privkey = load_privatekey(FILETYPE_PEM, ALIPAY_PRIVATE_KEY)
    _shediao_privkey = load_privatekey(FILETYPE_PEM, SHEDIAO_ALIPAY_PRIVATE_KEY)
    _huafubao_privkey = load_privatekey(FILETYPE_PEM, HUAFUBAO_PRIVATE_KEY)
    _ali_certkey = load_certificate(FILETYPE_PEM, ALIPAY_CERT)
    _shediao_certkey = load_certificate(FILETYPE_PEM, SHEDIAO_ALIPAY_CERT)
    _huafubao_certkey = load_certificate(FILETYPE_PEM, HUAFUBAO_CERT_KEY)
    _unionpay_certkey = load_certificate(FILETYPE_PEM, UNIONPAY_CERT_KEY)
except:
    traceback.print_exc()
    _ali_privkey = None
    _shediao_privkey = None
    _huafubao_privkey = None
    _ali_certkey = None
    _shediao_certkey = None
    _huafubao_certkey = None
    _unionpay_certkey = None


def _import_rsa_key_(keystr):
    return RSA.importKey(keystr)


def _sign_with_privatekey_openssl(data, private_key):
    try:
        d = sign(private_key, data, 'sha1')
        b = base64.b64encode(d)
        return b
    except:
        TyContext.ftlog.exception()
        return None


def _sign_with_privatekey_openssl_md5(data, private_key):
    try:
        d = sign(private_key, data, 'md5')
        b = base64.b64encode(d)
        return b
    except:
        TyContext.ftlog.exception()
        return None


def _verify_with_publickey_pycrypto_md5(data, sign, public_key):
    try:
        TyContext.ftlog.info("data*****", data)
        TyContext.ftlog.info("sign*****", sign)
        h = MD5.new(data)
        verifier = PKCS1_v1_5.new(public_key)
        ds = base64.b64decode(sign)
        return verifier.verify(h, ds)
    except:
        return False


def _verify_with_cert_openssl(data, sign, cert):
    try:
        s = base64.b64decode(sign)
        verify(cert, s, data, 'sha1')
        return True
    except:
        TyContext.ftlog.exception()
        return False


def _sign_with_privatekey_pycrypto(data, private_key):
    try:
        hash_obj = SHA.new(data)
        signer = PKCS1_v1_5.new(private_key)
        d = signer.sign(hash_obj)
        b = base64.b64encode(d)
        return b
    except:
        TyContext.ftlog.exception()
        return None


def _verify_with_publickey_pycrypto(data, sign, public_key):
    try:
        h = SHA.new(data)
        verifier = PKCS1_v1_5.new(public_key)
        ds = base64.b64decode(sign)
        return verifier.verify(h, ds)
    except:
        TyContext.ftlog.exception()
        return False


def rsaSign(data, channel=''):
    if channel == 'huafubao':
        priv_key = _huafubao_privkey
    else:
        priv_key = _ali_privkey
    return _sign_with_privatekey_openssl(data, priv_key)


def rsaAliSign(data):
    priv_key = _ali_privkey_py
    return _sign_with_privatekey_pycrypto(data, priv_key)


def rsaUnionPaySign(data):
    priv_key = _unionpay_private_key
    return _sign_with_privatekey_pycrypto(data, priv_key)


def verifyUnionPayCert(data, sign):
    return _verify_with_cert_openssl(data, sign, _unionpay_certkey)


def rsaVerify(data, sign, channel='', mock='false'):
    if channel == 'huafubao':
        return _verify_with_cert_openssl(data, sign, _huafubao_certkey)
    if channel == 'changba':
        public_key = _changba_pubkey_py
        return _verify_with_publickey_pycrypto_md5(data, sign, public_key)
    if channel == 'wandoujia':
        public_key = _wandoujia_pubkey_py
        return _verify_with_publickey_pycrypto(data, sign, public_key)

    if channel == 'shediao':
        public_key = _shediao_pubkey_py
    elif channel == 'oppo':
        public_key = _oppo_pubkey_py
    elif channel == 'jolo':
        public_key = _jolo_pubkey_py
    elif channel == 'jusdk':
        public_key = _jusdk_public_py
    else:
        public_key = _ali_pubkey_py
        if mock == 'true':
            public_key = _ali_pubkey_tuyoo_py
    return _verify_with_publickey_pycrypto(data, sign, public_key)


#######################
# some kinds of padding
# pkcs1_padding = 1
# sslv23_padding = 2
# no_padding = 3
# pkcs1_oaep_padding = 4
########################
def rsa_decrypto_with_publickey(pri_str, pkey_str, padding):
    lib, ffi = rsaLib.getLib()
    pub_str = ffi.new("char[]", 10240)
    lib.decrypt(pri_str, pkey_str, padding, pub_str)
    pubstring = ffi.string(pub_str)
    return pubstring


class RsaLibLoader(object):
    def __init__(self):
        self.__ffi = None
        self.__lib = None

    def getLib(self):
        if self.__lib:
            return self.__lib, self.__ffi

        path = os.path.split(os.path.realpath(__file__))[0]
        self.__ffi = FFI()
        self.__lib = self.__ffi.dlopen(path + "/libdec.so")
        TyContext.ftlog.info('Loaded lib {0}'.format(self.__lib))
        self.__ffi.cdef(
            '''
            void decrypt(char* pristr, char* pubkey, int padding, char* pubstr);
            '''
        )
        return self.__lib, self.__ffi


rsaLib = RsaLibLoader()

if __name__ == '__main__':
    data = '123456789'
    for x in xrange(1000000):
        if x % 10000 == 0:
            print x
        si = _sign_with_privatekey_openssl(data, _ali_privkey)
        _verify_with_cert_openssl(data, si, _ali_certkey)
        si = _sign_with_privatekey_pycrypto(data, _ali_privkey_py)
        _verify_with_publickey_pycrypto(data, si, _ali_pubkey_tuyoo_py)
