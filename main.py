import datetime
import time
from urllib.parse import urlparse
import multiprocessing
# multiprocessing.set_start_method('spawn')

import pandas as pd

import config
from get_facebook_reaction import FacebookPostReactionsGetter


def simple():
    """A Simple Tutorial"""
    # use firefox driver
    # use headless mode will not show ui for more performance
    # disable log to make faster
    fb_reaction_getter = FacebookPostReactionsGetter(driver='firefox', headless=False, showlog=True)
    
    # to login Facebook should do before get post reactions
    fb_reaction_getter.login_facebook(config.FACEBOOK_EMAIL, config.FACEBOOK_PASSWORD)

    post_path = 'https://www.facebook.com/gmmgrammyofficial/photos/a.427260850672454.100071.416543598410846/1786434408088418/?type=3&theater'
    
    # to write csv of reaction post
    fb_reaction_getter.post_reactions_to_csv(post_path)
    
    # to close driver
    fb_reaction_getter.close()

def get_reaction_by_post_list():
    """to use with post url list"""  
    post_paths = [
    'https://www.facebook.com/gmmgrammyofficial/videos/1798910450174147/',
    'https://www.facebook.com/gmmgrammyofficial/photos/1797558486976010/?type=3',
    'https://www.facebook.com/gmmgrammyofficial/photos/1786435471421645/?type=3',
    'https://www.facebook.com/gmmgrammyofficial/posts/1799049140160278'
    ]

    t=time.time()
    fb_reaction_getter = FacebookPostReactionsGetter(driver='firefox', headless=True, showlog=False)
    fb_reaction_getter.login_facebook(config.FACEBOOK_EMAIL, config.FACEBOOK_PASSWORD)
    for post_path in post_paths:
        fb_reaction_getter.post_reactions_to_csv(post_path)
    fb_reaction_getter.close()
    print(time.time()-t)

def get_reactings_from_post(post_path):
    fb_reaction_getter = FacebookPostReactionsGetter(driver='firefox', headless=True, showlog=False)
    fb_reaction_getter.login_facebook(config.FACEBOOK_EMAIL, config.FACEBOOK_PASSWORD)
    fb_reaction_getter.post_reactions_to_csv(post_path)
    fb_reaction_getter.close()

def use_multiprocessing():
    """make it more performance via multiprocessing"""
    post_paths = [
    'https://www.facebook.com/gmmgrammyofficial/videos/1798910450174147/',
    'https://www.facebook.com/gmmgrammyofficial/photos/1797558486976010/?type=3',
    'https://www.facebook.com/gmmgrammyofficial/photos/1786435471421645/?type=3',
    'https://www.facebook.com/gmmgrammyofficial/posts/1799049140160278'
    ]

    t=time.time()
    processes = list()
    for post_path in post_paths:
       process = multiprocessing.Process(target=get_reactings_from_post, args=(post_path, ))
       process.start()
       processes.append(process)
    for process in processes:
       process.join()
    print(time.time()-t)

def main():
    # simple()
    # get_reaction_by_post_list()
    use_multiprocessing()


if __name__ == '__main__':
    main()