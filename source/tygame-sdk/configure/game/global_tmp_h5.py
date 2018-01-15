# -*- coding=utf-8 -*-
from pyscript._helper_config_ import add_global_item
from collections import OrderedDict

add_global_item('servers.bi.http', {
    "sids": [
        "*"
    ],
    "groupinfos": {
        "chip_update": {
            "count": 8,
            "log_type": "chip",
            "name": "user"
        },
        "game": {
            "count": 8,
            "log_type": "game",
            "name": "user"
        },
        "sdk_login": {
            "count": 8,
            "log_type": "login",
            "name": "user"
        },
        "sdk_buy": {
            "count": 8,
            "log_type": "pay",
            "name": "user"
        },
        "card": {
            "count": 8,
            "log_type": "card",
            "name": "user"
        }
    },
    "servers": [
        "http://127.0.0.1:10001",
        "http://127.0.0.1:10002",
        "http://127.0.0.1:10003",
        "http://127.0.0.1:10004",
        "http://127.0.0.1:10005",
        "http://127.0.0.1:10006",
        "http://127.0.0.1:10007",
        "http://127.0.0.1:10008",
        "http://127.0.0.1:10009",
        "http://127.0.0.1:10010",
        "http://127.0.0.1:10011",
        "http://127.0.0.1:10012",
        "http://127.0.0.1:10013",
        "http://127.0.0.1:10014",
        "http://127.0.0.1:10015",
        "http://127.0.0.1:10016",
        "http://127.0.0.1:10017",
        "http://127.0.0.1:10018",
        "http://127.0.0.1:10019",
        "http://127.0.0.1:10020",
        "http://127.0.0.1:10021",
        "http://127.0.0.1:10022",
        "http://127.0.0.1:10023",
        "http://127.0.0.1:10024"
    ]
})
