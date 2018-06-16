import datetime
import time
import unittest
from urllib.parse import urlparse

import pandas as pd

import config
from get_facebook_reaction import FacebookPostReactionsGetter

def timetest(f):
    def timed(*args, **kw):

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        print('func:%r took: %2.4f sec' % \
          (f.__name__, te-ts))
        return result

    return timed

class UnitTest(unittest.TestCase):
    @timetest
    def setUp(self):
        self.fb_reaction_getter = FacebookPostReactionsGetter()
        self.fb_reaction_getter.showlog = True
        @timetest
        def test_facebook_Login():
            self.fb_reaction_getter.login_facebook(config.FACEBOOK_EMAIL, config.FACEBOOK_PASSWORD)
        test_facebook_Login()

    @timetest
    def test_get_post_reaction(self):
        post_path = 'https://www.facebook.com/bnk48official/photos/a.849974175129842.1073741828.842370685890191/1569874263139826/?type=3&theater'
        self.fb_reaction_getter.post_reactions_to_csv(post_path)

    def tearDown(self):
        self.fb_reaction_getter.close()

if __name__ == '__main__':
    unittest.main()
    #set up and login used 27 sec
    #get 1600 reactions used 534.9189 sec 
    #0.375 sec per reaction
