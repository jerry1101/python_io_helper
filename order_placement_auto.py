import yaml
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from colorama import Fore, Back, Style


def perform_action(driver, findby, findby_value, action, sleep_before, sleep_after,action_value=''):
    time.sleep(sleep_before)  # Let the user actually see something!
    if findby == 'id':

        print("id--->" + findby_value)

        elm = driver.find_element_by_id(findby_value)
        pass
    elif findby == 'class':
        print("class--->" + findby_value)
        elm = driver.find_element_by_class_name(findby_value)
        print(elm.text)
        pass
    elif findby == 'xpath':
        print("xpath--->"+findby_value)
        elm = driver.find_element_by_xpath(findby_value)
        print(elm.text)
        pass
    elif findby == 'css':

        elm = driver.find_element(By.CSS_SELECTOR,str(findby_value))
        #elm = driver.find_element_by_css_selector(str(findby_value))
        pass

    if elm is not None:
        if action == 'click':
            elm.click()
            pass
        elif action == 'select':
            s1 = Select(elm)
            s1.select_by_visible_text(action_value)
            pass
        elif action == 'sendkeys':
            elm.send_keys(action_value)
            pass
    time.sleep(sleep_after)


def load_script(filpath='order_script.yaml'):
    with open(filpath) as f:
        dataMap = yaml.safe_load(f)
        #print(yaml.dump(dataMap))
        #print(len(dataMap['root']))
        return dataMap


def main():
    #driver = webdriver.Chrome('./chromedriver.exe')  # Optional argument, if not specified will search path.
    driver = webdriver.Firefox()  # Optional argument, if not specified will search path.

    driver.delete_all_cookies()
    driver.get('http://www.totalwine.com');
    driver.implicitly_wait(5)
    #driver.maximize_window()
    script= load_script()
    action_list = []
    for action in script['root']:
        action_list.append(action)

    sorted_action_list = sorted(action_list)
    for action in sorted_action_list:
        print("==XX"+action)

        findby = script['root'][action]['findby']
        findby_val = script['root'][action]['findby_value']
        action_name = script['root'][action]['action']

        action_val = None
        sleepbefore = script['root'][action]['sleep_before']
        sleepafter = script['root'][action]['sleep_after']

        try:
            action_val =  script['root'][action]['action_value']
        except Exception as e:
            print('no action value found')

        if script['root'][action]['enter_iframe'] == True:
            print("in iframe")
            driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))

        if str(script['root'][action]['needed']) == 'ture':
            perform_action(driver,findby,findby_val,action_name,sleepbefore,sleepafter,action_value=action_val)
            print(Fore.WHITE +str(datetime.now())+"  "+Style.BRIGHT+script['root'][action]['success_msg']+"\n")
        else:
            try:
                perform_action(driver, findby, findby_val,action_name, sleepbefore, sleepafter,action_value=action_val)
                print(Fore.WHITE +str(datetime.now())+"  "+Fore.GREEN +script['root'][action]['success_msg'])
            except Exception as e:
                print(Fore.WHITE +str(datetime.now())+"  "+Fore.RED +script['root'][action]['failure_msg']+": \n")
                print(e)


if __name__ == "__main__":
    main()