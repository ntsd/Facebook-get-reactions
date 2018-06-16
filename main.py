import datetime
from urllib.parse import urlparse

import pandas as pd

import config
from get_facebook_reaction import FacebookPostReactionsGetter

def main():
    # driver is browser to use
    # headless is faster but not show in window
    fb_reaction_getter = FacebookPostReactionsGetter(driver='chrome', headless=True)
    fb_reaction_getter.showlog = True # use to show log default is false
    fb_reaction_getter.login_facebook(config.FACEBOOK_EMAIL, config.FACEBOOK_PASSWORD)

    post_path = 'https://www.facebook.com/gmmgrammyofficial/photos/a.427260850672454.100071.416543598410846/1786434408088418/?type=3&theater'
    fb_reaction_getter.post_reactions_to_csv(post_path)

    fb_reaction_getter.close()

if __name__ == '__main__':
    main()