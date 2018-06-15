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
        self.fb_reaction_getter.log = True
        @timetest
        def test_facebook_Login():
            self.fb_reaction_getter.login_facebook(config.FACEBOOK_EMAIL, config.FACEBOOK_PASSWORD)
        test_facebook_Login()

    @timetest
    def test_get_post_reaction(self):
        full_path = 'https://www.facebook.com/bnk48official/photos/a.849974175129842.1073741828.842370685890191/1569874263139826/?type=3&theater'
        reactions = self.fb_reaction_getter.get_post_reactons(full_path)
        short_path = '_'.join(urlparse(full_path).path.split('/'))

        date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = '{}_{}_{}.csv'.format(short_path, len(reactions), date_time)
        print('saving csv to {}'.format(file_name))
        
        
        df = pd.DataFrame(reactions,
                        columns=['name', 'profile_url', 'reaction'])
        df.to_csv(file_name, sep=',', encoding='utf-8')
        print('saved success'.format(file_name))

    def tearDown(self):
        self.fb_reaction_getter.close()

if __name__ == '__main__':
    unittest.main()
    #set up and login used 27 sec
    #get 1600 reactions used 534.9189 sec 
    #0.375 sec per reaction
