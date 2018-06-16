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

Simple

```python
fb_reaction_getter = FacebookPostReactionsGetter(driver='chrome', headless=True)
# use chrome driver
# use headless mode for more performance
fb_reaction_getter.showlog = True
# to set show log default is false
fb_reaction_getter.login_facebook(config.FACEBOOK_EMAIL, config.FACEBOOK_PASSWORD)
# to login Facebook should do before get post reactions
post_path = 'url of Facebook post'
fb_reaction_getter.post_reactions_to_csv(post_path)
# get post reacton to csv
fb_reaction_getter.close()
```

Advance

```python
reactions = fb_reaction_getter.get_post_reactons(post_path)
# to get Reactions from post_path
short_path = '_'.join(list(filter(None,urlparse(post_path).path.split('/'))))
date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = '{}_{}_{}.csv'.format(short_path, len(reactions), date_time)
# to set name of csv file
df = pd.DataFrame(reactions, columns=['name', 'profile_url', 'reaction'])
df.to_csv(file_name, sep=',', encoding='utf-8')
# to save csv file
```

