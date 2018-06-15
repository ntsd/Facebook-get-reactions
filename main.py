import datetime
from urllib.parse import urlparse

import pandas as pd

import config
from get_facebook_reaction import FacebookPostReactionsGetter

def main():
    fb_reaction_getter = FacebookPostReactionsGetter()
    fb_reaction_getter.log = True # use to show log default is false
    fb_reaction_getter.login_facebook(config.FACEBOOK_EMAIL, config.FACEBOOK_PASSWORD)

    full_path = 'https://www.facebook.com/gmmgrammyofficial/photos/a.427260850672454.100071.416543598410846/1786434408088418/?type=3&theater'
    reactions = fb_reaction_getter.get_post_reactons(full_path)
    short_path = '_'.join(urlparse(full_path).path.split('/'))

    date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = '{}_{}_{}.csv'.format(short_path, len(reactions), date_time)
    print('saving csv to {}'.format(file_name))
        
    df = pd.DataFrame(reactions,
                    columns=['name', 'profile_url', 'reaction'])
    df.to_csv(file_name, sep=',', encoding='utf-8')
    print('saved success'.format(file_name))

    fb_reaction_getter.close()

if __name__ == '__main__':
    main()