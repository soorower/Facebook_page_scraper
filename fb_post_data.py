from shutil import which
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# for waiting please import:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from random import randint
import pandas as pd   
facebook_mail = input("Provide fb email address: ")
facebook_pass = input("Fb password: ")

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-extensions")

# chrome_options.add_argument("--headless")
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}


# Pass the argument 1 to allow and 2 to block
chrome_options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2 
})

chrome_path = which("chromedriver")
driver = webdriver.Chrome(executable_path=chrome_path, options= chrome_options)
url = 'https://m.facebook.com/login/'
driver.get(url)


class login():
    driver.find_element_by_xpath("//*[@id='m_login_email']").send_keys(facebook_mail)
    driver.find_element_by_xpath("//*[@id='m_login_password']").send_keys(facebook_pass)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "login"))
    )
    # sleep(randint(1,3))
    element.click()
    sleep(randint(1,3))
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='_2pis']/button"))
    )
    element.click()

login()
sleep(2)
df = pd.read_excel('Post_links.xlsx')
df.columns = ['number','Links']
all_links_collected_to_excel = df['Links'].tolist()


df2 = pd.read_excel('Total_scraped_no.xlsx')
df2.columns = ['number','Last_scraped_number']
last_number = df2['Last_scraped_number'][0]

u = last_number
last_scraped1 = []
data_list = []
item = {}


try:
    for one_link in all_links_collected_to_excel[last_number:]:
        ids = one_link.split('/')
        post_id = ids[5]
        u= u+1
        last_scraped1.append(u)


        driver.get(one_link)
        sleep(0.5)

        poster_name_class = driver.find_element_by_xpath("*//h3").get_attribute("class")
        poster_name_xpath = f"//h3[@class='{poster_name_class}']/span/strong[1]/a"
        poster_name = driver.find_element_by_xpath(poster_name_xpath).text
        try:
            try:
                post_text = driver.find_element_by_xpath("//div[@id='m_story_permalink_view']/div/div/div/div").text
            except:
                post_text = driver.find_element_by_xpath("//div[@id='m_story_permalink_view']/div/div/div/div[2]").text
        except:
            pass

        post_date = driver.find_element_by_xpath("*//abbr").text
        try:
            shares = driver.find_element_by_xpath("//span[@data-sigil='feed-ufi-sharers']").text
        except:
            shares = '-'
            pass
        try:
            driver.find_element_by_xpath("//div[@class='_1w1k _5c4t']").click()
            sleep(1)
            likes = driver.find_elements_by_xpath("//span[@data-sigil='reaction_profile_tab_count']")[1].text
        except:
            likes = '-'
            pass


        print(f"\n Scraping link : {one_link}")

        item1 = {
                'Post Link': one_link,
                'Page Name': poster_name,
                'Post Text': post_text,
                'Posting Date/Time': post_date,
                'Share Count': shares,
                'Likes Count': likes
                }

        data_list.append(item1)

        print(poster_name)
        print(post_text)
        print(post_date)
        print(shares)
        print(likes)

        driver.execute_script("window.history.go(-1)")
        sleep(0.2)

        try:
            more_comments_id = f"//*[@id='see_prev_{post_id}']/a"
        except:
            more_comments_id = f"//*[@id='see_next_{post_id}']/a"
            pass
        try:
            for i in range(1,20):
                loading_comments = driver.find_element_by_xpath(more_comments_id).click()
                sleep(2)
        except:
            pass

        replies = driver.find_elements_by_partial_link_text("replied")
        try:
            for reply in replies:
                reply.click()
                # sleep(1)
        except:
            pass
        sleep(1)

        commenters_name = driver.find_elements_by_xpath("//*[@class='_2b06']/div[1]")
        commenters_comment = driver.find_elements_by_xpath("//*[@class='_2b06']/div[2]")

        try:
            for commenter_name,commenter_comment in zip(commenters_name,commenters_comment):
                name = commenter_name.text.replace('Top fan','')
                comment = commenter_comment.text
                print(name)
                # sleep(0.01)
                print(comment)
                # print('\n''\n')
                item = {
                'Commentator Name': name,
                'Commentators Comment': comment
                }

                data_list.append(item)
        except:
            pass 
except:
    print('Data Collection Failed. Relaunch the bot. ')
    pass


last_scraped2 = max(last_scraped1)
last_scraped = []
last_scraped.append(last_scraped2)
print(last_number)

df1 = pd.DataFrame(last_scraped)
df1.to_excel('Total_scraped_no.xlsx')

df_final = pd.DataFrame(data_list)
df_final.to_excel(f"post_details_{last_number}_to_{last_scraped2}.xlsx")