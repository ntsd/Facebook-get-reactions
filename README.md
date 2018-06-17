# Facebook get reactions
get reactions of Facebook post



### Install

1.install Python 3.5+

2.install dependency via ```pip install -r requirements.txt```

3.download Selenium browser driver to this path (I already add Firefox win64 driver and Chrome win64 driver) 

​	you can download other version [Here](http://selenium-python.readthedocs.io/installation.html)

4.rename `example.config.py` to `config.py` 



### How to use

1.setup Facebook e-mail and password in `config.py` 

2.change post path in `main.py`

3.run ```python main.py``` to test run `python test.py`



### Example Code

**Simple** - save post reaction to csv

```python
import config
from get_facebook_reaction import FacebookPostReactionsGetter

fb_reaction_getter = FacebookPostReactionsGetter()

# to set show log default is False
fb_reaction_getter.showlog = True

# to login Facebook should do before get post reactions
fb_reaction_getter.login_facebook(config.FACEBOOK_EMAIL, config.FACEBOOK_PASSWORD)

post_path = 'url of Facebook post'

# get post reacton to csv
fb_reaction_getter.post_reactions_to_csv(post_path)

# to close driver
fb_reaction_getter.close()
```

**Advance** - to save csv yourself

```python
import pandas as pd
import config
from urllib.parse import urlparse
from get_facebook_reaction import FacebookPostReactionsGetter

# to init FacebookPostReactionsGetter class
# use firefox driver
# use headless mode will not show ui for more performance
# disable log to make faster
fb_reaction_getter = FacebookPostReactionsGetter(driver='firefox', headless=True, showlog=False)

# to login Facebook should do before get post reactions
fb_reaction_getter.login_facebook(config.FACEBOOK_EMAIL, config.FACEBOOK_PASSWORD)

post_path = 'url of Facebook post'

# to get Reactions class
reactions = fb_reaction_getter.get_post_reactons(post_path)

# to set name of csv file
short_path = '_'.join(list(filter(lambda x: not x.startswith('a.'),filter(None,urlparse(post_path).path.split('/')))))
date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = '{}_{}_{}.csv'.format(short_path, len(reactions), date_time)

# to save csv file
df = pd.DataFrame(reactions, columns=['name', 'profile_url', 'reaction'])
df.to_csv(file_name, sep=',', encoding='utf-8')

# to close driver
fb_reaction_getter.close()
```

**Multiprocessing** - make it more performance via multiprocessing

```python
import multiprocessing
import config
from get_facebook_reaction import FacebookPostReactionsGetter

def get_reactings_from_post(post_path):
    fb_reaction_getter = FacebookPostReactionsGetter(driver='firefox', headless=True, showlog=False)
    fb_reaction_getter.login_facebook(config.FACEBOOK_EMAIL, config.FACEBOOK_PASSWORD)
    fb_reaction_getter.post_reactions_to_csv(post_path)
    fb_reaction_getter.close()

# to set list of posts url
post_paths = ['https://www.facebook.com/gmmgrammyofficial/posts/1799049140160278',
             'https://www.facebook.com/gmmgrammyofficial/videos/1798910450174147/',
             'https://www.facebook.com/gmmgrammyofficial/photos/1797558486976010/']

processes = list()
for post_path in post_paths:
    process = multiprocessing.Process(target=get_reactings_from_post, args=(post_path, ))
    process.start()
    processes.append(process)
for process in processes:
    process.join()
```



