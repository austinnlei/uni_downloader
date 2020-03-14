from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import datetime

# 1. SET UP

## Get date
now = datetime.datetime.now()
year = str(now.year)

## Get uni term based on date
current_term = ""
if now.month <= 5:
    current_term = "T1"
elif now.month <= 8:
    current_term = "T2"
else:
    current_term = "T3"

## Set up info from user input, downloading from echo360
baseurl = "https://echo360.org.au/"
firstname = input("Type your first name in lower case: ")
lastname = input("Type your last name in lower case: ")
zID = input("Type your zID: ")
password = input("Type your password: ")
courses = input("Type the courses you would like to download and the number of lectures per week in the format 'COURSE1:#OFLECTURES,COURSE2:#OFLECTURES': ")
uni_directory = input("Type the directory where you would like to download the lectures to: ")


echo360email = firstname+"."+lastname+"@student.unsw.edu.au"
microsoftemail = zID+"@ad.unsw.edu.au"
course_list = courses.split(",")
course_dict = {}
for course in course_list:
    course_dict[course.split(":")[0]] = int(course.split(":")[1])

# assuming UNSW trimesters
num_weeks = 10

for course_code in course_dict.keys():
    course_directory = uni_directory + "/" + course_code
    if not os.path.exists(course_directory):
        os.mkdir(course_directory)
    export_directory = course_directory + "/lecture videos/"
    if not os.path.exists(export_directory):
        os.mkdir(export_directory)
    # START UP BROWSER AND LOGON TO ECHO360
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : export_directory}
    chromeOptions.add_experimental_option("prefs",prefs)

    browser = webdriver.Chrome(executable_path='/Users/austinlei/Downloads/chromedriver', options=chromeOptions)
    try:
        browser.set_page_load_timeout(15)
        browser.get(baseurl)
        browser.implicitly_wait(30)
        # set up download directory
    except:
        pass
    

    #logon to echo360
    email_input = browser.find_element_by_id("email")
    email_input.send_keys(echo360email)
    browser.find_element_by_id("submitBtn").click()

    #logon to microsoft
    browser.find_element_by_id("userNameInput").send_keys(microsoftemail)
    browser.find_element_by_id("passwordInput").send_keys(password)
    browser.find_element_by_id("submitButton").click()

    # Navigate to necessary course to start scraping
    all_lecture_vids = browser.find_elements_by_tag_name('a')
   
    for course in all_lecture_vids:
        if course_code in course.text:
            print(course_code)
            course.click()
            break
    weeknames = []
    if course_dict[course_code] == 1:
        weeknames = range(num_weeks)
    else:
        for i in range(num_weeks):
            for j in range(course_dict[course_code]):
                weeknames.append(str(i+1)+chr(j+97))

    menu_openers = browser.find_elements_by_class_name("menu-opener")

    # Find all available lectures and download them
    lecture_num = 0
    for menu_opener in menu_openers:
        lecture_filename = "Week " + weeknames[lecture_num] + ".mp4"
        if lecture_filename in os.listdir(export_directory):
            lecture_num = lecture_num + 1
            continue

        menu_opener.click()
        menu = browser.find_element_by_class_name("menu-items")
        menu.find_elements_by_tag_name("li")[1].click()
        select_wrapper = browser.find_element_by_class_name("select-wrapper")
        options = select_wrapper.find_elements_by_tag_name("option")
        HD_text = options[1].text
        select_element = select_wrapper.find_element_by_tag_name("select")
        quality_options_select = Select(select_element)
        quality_options_select.select_by_visible_text(HD_text)
        modal_footer = browser.find_element_by_class_name("modal-footer")
        download_button = modal_footer.find_elements_by_tag_name("a")[1]
        download_button.click()

        #check export directory continuously till finishes downloading
        dl_wait = True
        while dl_wait:
            time.sleep(2)
            dl_wait = False
            for fname in os.listdir(export_directory):
                if fname.endswith('.crdownload'):
                    dl_wait = True
                    basename = fname.split(".")[0]
            time.sleep(5)
        for fname in os.listdir(export_directory):
            if fname.split(".")[0] == basename:
                os.rename(export_directory+fname, export_directory+lecture_filename)
        lecture_num = lecture_num + 1

    browser.quit()


        





#logon to moodle
# logon_iframe = mydriver.find_element_by_xpath("//*[@id='region-main']/div/div[1]/iframe")
# mydriver.switch_to.frame(logon_iframe)
# username_box = mydriver.find_element_by_id("username")
# password_box = mydriver.find_element_by_id("password")
# username_box.send_keys(username)
# password_box.send_keys(password)
# submit_button = mydriver.find_element_by_xpath("/html/body/div/div/div/form/div[3]/input[1]")
# submit_button.click()


### probably should just download to pre defined chrome directory -> then rename them when they finish downloading