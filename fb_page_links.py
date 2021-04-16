from shutil import which
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep
from random import randint
import pandas as pd   

link = input("Provide fb page link: ")
facebook_mail = input("Provide fb email address: ")
facebook_pass = input("Fb password: ")
scroll = int(input("how many times do you want to scroll the page: "))
# group_id = link.split("/")[4]

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--headless")
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
chrome_options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2 
})
# scroll_number = int(input('How many times do you want to scroll: '))
chrome_path = which("chromedriver")
driver = webdriver.Chrome(executable_path=chrome_path, options= chrome_options)

url = 'https://www.facebook.com/login/'
driver.get(url)


class login():
    driver.find_element_by_xpath("//*[@id='email']").send_keys(facebook_mail)
    driver.find_element_by_xpath("//*[@id='pass']").send_keys(facebook_pass)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "login"))
    )
    element.click()

login()
sleep(2)



#--------------------Setting Excel to save scraping progess--------------------------------------
last_scraped = [1]
df2 = pd.DataFrame(last_scraped)
df2.to_excel('Total_scraped_no.xlsx')
df2.columns = ['Last_scraped_number']
# sleep(2)



#---------------------Opening the group----------------------------------------------------------
driver.get(f'{link}')
all_stories_link = []
only_group_list = []
ultimate_post_list = []
sleep(2)



#-------------------Scrolling up and down to load the page perfectly--------------------------------------
driver.execute_script(f"window.scrollBy(0,500)","")
sleep(1)
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)



#-------------------Scrolling Starting(this will stop when no more post is found)------------------------------------
try:
    for i in range(scroll):
        any = randint(1000,1500)
        driver.execute_script(f"window.scrollBy(0,{any})","")
        sleep(randint(1,3))
        print(i)        
except:
    print("Scrolling not working...")
sleep(2)

print('uncomment the below code if scrolling not working. Also comment out the upper 9 lines.')

# def scroll_to_bottom(driver):
#     old_position = 0
#     new_position = None

#     while new_position != old_position:
#         # Get old scroll position
#         old_position = driver.execute_script(
#                 ("return (window.pageYOffset !== undefined) ?"
#                  " window.pageYOffset : (document.documentElement ||"
#                  " document.body.parentNode || document.body);"))
#         # Sleep and Scroll
#         sleep(randint(1,3))
#         any = randint(11000,1500)
#         driver.execute_script(f"window.scrollBy(0,{any})","")
#         # Get new position
#         new_position = driver.execute_script(
#                 ("return (window.pageYOffset !== undefined) ?"
#                  " window.pageYOffset : (document.documentElement ||"
#                  " document.body.parentNode || document.body);"))


# scroll_to_bottom(driver)


#-------------------Going back to top of the page------------------------------------------------
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
sleep(2.5)


#---------------Finding 'Post links', from Comments------------------------------------------------
try:
    post_links_comment = driver.find_elements_by_xpath("*//div[@role='article']/div[2]/ul/li[3]/a")
    for post_link in post_links_comment:
        link1 = post_link.get_attribute("href")
        link2 = link1.split('?')[0]
        link = link2.replace('www','m')
        all_stories_link.append(link)  
        print(link)
except:
    print("Collecting links from comments, stopped!")

print('Total Links from comments(has duplicates):')
print(len(all_stories_link))



#-------------------Going back to top of the page-----------------------------------------------------
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
sleep(1)


#-------------------Hovering Started------------------------------------------------------------------
hover_overing = driver.find_elements_by_xpath("*//span[@dir='auto']/span/span/span/a")

try:
    for hover in hover_overing:
        webdriver.ActionChains(driver).move_to_element(hover).perform()
        sleep(0.2) #you can change it upto 1 sec, if internet is slow
except:
    print('Problem while hovering...')



#----------------Collecting Links after hovering---------------------------------------------
try:
    for hover in hover_overing:
        link1 = hover.get_attribute("href")
        link2 = link1.split('?')[0]
        link = link2.replace('www','m')
        all_stories_link.append(link)
        print(link)

except:
    print('Problem while collecting links after hovering...')



#-------------Saving the final output in an Excel---------------------------------------------------
df1 = pd.DataFrame(all_stories_link)
done = df1.drop_duplicates(keep='first')
dn = done.reset_index(drop = True)
dn.to_excel('Post_links.xlsx')