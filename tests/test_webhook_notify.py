import os
import shelve
import time
import json                             # req python 2.6
import urllib

import testutil
from twill.commands import *

###

rpc_url = None
DB_TEST_FILE='tests/tests.db'

github_data = dict(payload='{"commits":[{"modified":["IDEAS"],"url":"http://github.com/ctb/pony-build/commit/e95f152f6d4e50da340d361a41789e0f0b904d56","message":"test","author":{"email":"t@titus-browns-macbook-2.local","name":"Titus Brown"},"timestamp":"2009-12-04T17:03:04-08:00","removed":[],"id":"e95f152f6d4e50da340d361a41789e0f0b904d56","added":[]}],"repository":{"forks":4,"description": "CI for Python","url":"http://github.com/ctb/pony-build","fork":false,"watchers":31,"private":false,"homepage":"","owner":{"email":"titus@idyll.org","name":"ctb"},"name":"pony-build","open_issues":1},"ref":"refs/heads/test","before":"cd759759417253f630123e89684e9fd29a4d9225","after":"e95f152f6d4e50da340d361a41789e0f0b904d56"}')


###

def setup():
    testutil.run_server(DB_TEST_FILE)
    assert testutil._server_url
    
def teardown():
    testutil.kill_server()

def test_basic():
    go(testutil._server_url)
    go('./notify')
    code(200)
    find('received')

def test_github_notify():
    fp = urllib.urlopen(testutil._server_url + 'notify?format=github',
                        urllib.urlencode(github_data))

    received = fp.read()
    assert received == 'received', (received,)