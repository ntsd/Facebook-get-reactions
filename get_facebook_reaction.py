# -*- coding: utf-8 -*-
import datetime
from urllib.parse import urlparse

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from reaction import Reaction

class FacebookPostReactionsGetter:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.showlog = False

    def login_facebook(self, facebook_email, facebook_password):
        """
            Argument:
                - facebook_email String 
                - facebook_password String
            Output:
                - driver sign in to Facbook
        """
        self.log('sign in facebook...')
        self.driver.get("https://www.facebook.com/")
        emailFieldID = "email"
        passFieldID = "pass"
        loginButtonXpath = "//label[@id='loginbutton']/input"
        facebookLogo = "//a[@class='_19eb']"

        emailFieldElement = WebDriverWait(self.driver, 5).until(lambda driver: self.driver.find_element_by_id(emailFieldID))
        passFieldElement = WebDriverWait(self.driver, 5).until(lambda driver: self.driver.find_element_by_id(passFieldID))
        loginButtonElement = WebDriverWait(self.driver, 5).until(lambda driver: self.driver.find_element_by_xpath(loginButtonXpath))

        emailFieldElement.clear()
        emailFieldElement.send_keys(facebook_email)
        passFieldElement.clear()
        passFieldElement.send_keys(facebook_password)
        loginButtonElement.click()
        WebDriverWait(self.driver, 5).until(lambda driver: self.driver.find_element_by_xpath(facebookLogo)) # wait login success
        self.log('sign in success')

    def get_post_reactons(self, post_url):
        """
            Argument:
                - post_url String 
            Output:
                - Reactions List [Reaction]
        """
        self.log('load post page: ', post_url)
        self.driver.get(post_url)
        self.log('load post page success')
        reactionModalXpath = "//a[@class='_2x4v']"
        seeMoreXpath = "//a[text() = 'See More']"

        reactionPath = WebDriverWait(self.driver, 5).until(lambda driver: self.driver.find_element_by_xpath(reactionModalXpath)).get_attribute("href")
        self.driver.get(reactionPath)

        class_reaction_xpath = "//div[@class='_3p56']"
        class_reaction_elements = self.driver.find_elements_by_xpath(class_reaction_xpath)
        class_reaction_names = []
        for class_reaction in class_reaction_elements:
            class_reaction_names.append(class_reaction.text)

        list_class_xpath = ".//div[@class='_5i_p']"
        list_class_elements = self.driver.find_elements_by_xpath(list_class_xpath)

        profile_xpath = ".//li[@class='_5i_q']"
        profile_name_xpath = ".//div[@class='_5j0e fsl fwb fcb']/a"
        # profile_url_xpath = "//a[@clas='_5i_s _8o _8r lfloat _ohe']"
        reactions = []
        for reaction_index, reaction_profile_list in enumerate(list_class_elements):
            list_profile_elements = reaction_profile_list.find_elements_by_xpath(profile_xpath)
            # self.log(len(list_profile_elements))
            old_len = len(list_profile_elements) #old len to check show more button work
            sum_len = 0
            tried = 0
            while True: # show 50 more
                try:
                    showMoreButton = WebDriverWait(self.driver, 10).until(lambda driver: reaction_profile_list.find_element_by_xpath(seeMoreXpath)) # wait util show more button
                    self.driver.execute_script("arguments[0].click();", showMoreButton) # use for click show more button
                    # showMoreButton.send_keys("\n") #doesn't work
                    WebDriverWait(self.driver, 10).until(lambda driver: len(reaction_profile_list.find_elements_by_xpath(profile_xpath)) > old_len) # check show more load complete

                    list_profile_elements = reaction_profile_list.find_elements_by_xpath(profile_xpath) # replace new list

                    new_len = len(list_profile_elements)
                    sum_len += new_len

                    self.log('click show more for {} reactions for {} rows now {} rows...'.format(\
                        class_reaction_names[reaction_index], new_len-old_len, sum_len))

                    for li_profile in list_profile_elements: # for in profile element
                        profile_name = li_profile.find_element_by_xpath(profile_name_xpath).text # get name of profile
                        profile_url = li_profile.find_element_by_xpath(profile_name_xpath).get_attribute("href") # get url of profile
                        # self.log(profile_name, profile_url, class_reaction_names[reaction_index])
                        reactions.append(Reaction(name=profile_name, profile_url=profile_url, reaction=class_reaction_names[reaction_index]))
                        self.driver.execute_script("""
                            var element = arguments[0];
                            element.parentNode.removeChild(element);
                            """, li_profile) # delete element after append to list
                    
                    old_len = 0

                except Exception as e:
                    self.log(e)
                    if tried>2:
                        self.log("click show more success")
                        break
                    tried+=1
                    self.log('tried {}'.format(tried))
            
        self.log('get {} reactions success'.format(len(reactions)))
        return reactions

    def post_reactions_to_csv(self, full_path):
        reactions = self.get_post_reactons(full_path)
        short_path = '_'.join(list(filter(None,urlparse(full_path).path.split('/'))))

        date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = '{}_{}_{}.csv'.format(short_path, len(reactions), date_time)
        self.log('saving csv to {}'.format(file_name))
            
        df = pd.DataFrame(reactions,
                        columns=['name', 'profile_url', 'reaction'])
        df.to_csv(file_name, sep=',', encoding='utf-8')
        self.log('saved success'.format(file_name))

    def close(self):
        """
            Output:
                - close this driver
        """
        self.driver.quit()
        self.log('closed driver')

    def log(self, *args, **kwargs):
        if self.showlog:
            print(*args, **kwargs)

if __name__ == '__main__':
    import config
    fb_reaction_getter = FacebookPostReactionsGetter()
    fb_reaction_getter.login_facebook(config.FACEBOOK_EMAIL, config.FACEBOOK_PASSWORD)
    # https://www.facebook.com/bnk48official/photos/a.849974175129842.1073741828.842370685890191/1569874263139826/?type=3&theater
    reactions = fb_reaction_getter.get_post_reactons('https://www.facebook.com/gmmgrammyofficial/photos/a.427260850672454.100071.416543598410846/1786434408088418/?type=3&theater')
    print(reactions)
