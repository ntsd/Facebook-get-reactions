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
        self.log = False

    def login_facebook(self, facebook_email, facebook_password):
        """
            Argument:
                - facebook_email String 
                - facebook_password String
            Output:
                - driver sign in to Facbook
        """
        if self.log:print('sign in facebook...')
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
        if self.log:print('sign in success')

    def get_post_reactons(self, post_url):
        """
            Argument:
                - post_url String 
            Output:
                - Reactions List [Reaction]
        """
        if self.log:print('load post page: ', post_url)
        self.driver.get(post_url)
        if self.log:print('load post page success')
        reactionModalXpath = "//a[@class='_2x4v']"
        seeMoreXpath = "//a[text() = 'See More']"

        reactionPath = WebDriverWait(self.driver, 5).until(lambda driver: self.driver.find_element_by_xpath(reactionModalXpath)).get_attribute("href")
        self.driver.get(reactionPath)

        xpath_profile = ".//li[@class='_5i_q']"

        old_len = len(self.driver.find_elements_by_xpath(xpath_profile))

        tried = 0
        while True: # show 50 more
            try:
                showMoreButton = WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_xpath(seeMoreXpath)) # wait util see see more
                self.driver.execute_script("arguments[0].click();", showMoreButton) # use for click show more button
                # showMoreButton.send_keys("\n") #doesn't work
                
                WebDriverWait(self.driver, 10).until(lambda driver: len(self.driver.find_elements_by_xpath(xpath_profile)) > old_len) # check element load complete

                if self.log:print('click show more now {} rows...'.format(len(self.driver.find_elements_by_xpath(xpath_profile))))

                old_len = len(self.driver.find_elements_by_xpath(xpath_profile))

            except Exception as e:
                if self.log:print(e)
                if old_len==len(self.driver.find_elements_by_xpath(xpath_profile)) or tried>2:
                    if self.log:print("click show more success")
                    break
                else:
                    tried+=1
                    if self.log:print('tried {}'.format(tried))

        class_reaction_xpath = "//div[@class='_3p56']"
        class_reaction_elements = self.driver.find_elements_by_xpath(class_reaction_xpath)
        class_reaction_names = []
        for class_reaction in class_reaction_elements:
            class_reaction_names.append(class_reaction.text)

        list_profile_xpath = "//div[@class='_5i_p']"
        list_profile_elements = self.driver.find_elements_by_xpath(list_profile_xpath)

        profile_name_xpath = ".//div[@class='_5j0e fsl fwb fcb']/a"
        # profile_url_xpath = "//a[@clas='_5i_s _8o _8r lfloat _ohe']"
        reactions = []
        for index, list_profile in enumerate(list_profile_elements):
            li_profile_elements = list_profile.find_elements_by_xpath(xpath_profile)
            # print(len(li_profile_elements))
            for li_profile in li_profile_elements:
                profile_name = li_profile.find_element_by_xpath(profile_name_xpath).text
                profile_url = li_profile.find_element_by_xpath(profile_name_xpath).get_attribute("href")
                # print(profile_name, profile_url, class_reaction_names[index])
                reactions.append(Reaction(name=profile_name, profile_url=profile_url, reaction=class_reaction_names[index]))
        if self.log:print('get {} reactions success'.format(len(reactions)))
        return reactions

    def post_reactions_to_csv(self, full_path):
        reactions = self.get_post_reactons(full_path)
        short_path = '_'.join(list(filter(None,urlparse(full_path).path.split('/'))))

        date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = '{}_{}_{}.csv'.format(short_path, len(reactions), date_time)
        print('saving csv to {}'.format(file_name))
            
        df = pd.DataFrame(reactions,
                        columns=['name', 'profile_url', 'reaction'])
        df.to_csv(file_name, sep=',', encoding='utf-8')
        print('saved success'.format(file_name))

    def close(self):
        """
            Output:
                - close this driver
        """
        self.driver.quit()
        if self.log:print('closed driver')

if __name__ == '__main__':
    import config
    fb_reaction_getter = FacebookPostReactionsGetter()
    fb_reaction_getter.login_facebook(config.FACEBOOK_EMAIL, config.FACEBOOK_PASSWORD)
    # https://www.facebook.com/bnk48official/photos/a.849974175129842.1073741828.842370685890191/1569874263139826/?type=3&theater
    reactions = fb_reaction_getter.get_post_reactons('https://www.facebook.com/gmmgrammyofficial/photos/a.427260850672454.100071.416543598410846/1786434408088418/?type=3&theater')
    print(reactions)
