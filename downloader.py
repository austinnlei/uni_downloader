from selenium import webdriver
import os
#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

import requests
import urllib
import json

import datetime

def download_file(url, filename):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

now = datetime.datetime.now()
year = str(now.year)

current_term = ""
if now.month <= 5:
    current_term = "T1"
elif now.month <= 8:
    current_term = "T2"
else:
    current_term = "T3"


#baseurl = "https://moodle.telt.unsw.edu.au/login/index.php?"
baseurl = "https://echo360.org.au/"
firstname = "austin"#input("Type your first name in lower case: ")
lastname = "lei"#input("Type your last name in lower case: ")
echo360email = firstname+"."+lastname+"@student.unsw.edu.au"
zID = "z5117242"#input("Type your zID: ")
microsoftemail = zID+"@ad.unsw.edu.au"
courses = "COMP3311:2"#input("Type the courses you would like to download and the number of lectures per week in the format 'COURSE1:#OFLECTURES,COURSE2:#OFLECTURES': ")
course_list = courses.split(",")
course_dict = {}
for course in course_list:
    course_dict[course.split(":")[0]] = int(course.split(":")[1])

#username = "austin.lei@student.unsw.edu.au"#input("Type your Echo360 account email 'firstname.lastname@student.unsw.edu.au': ")
password = "Working@Macq09"#input("Type your password: ")

num_weeks = 10

uni_directory = "/Users/austinlei/Documents/UNI"
uni_year_directory = uni_directory + "/" + year
uni_year_term_directory = uni_year_directory + "/"+ current_term

if not os.path.exists(uni_year_directory):
    os.mkdir(uni_year_directory)
if not os.path.exists(uni_year_term_directory):
    os.mkdir(uni_year_term_directory)


browser = webdriver.Chrome('/Users/austinlei/Downloads/chromedriver')
try:
    browser.set_page_load_timeout(15)
    browser.get(baseurl)
    browser.implicitly_wait(30)
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

#start scraping echo360

for course_code in course_dict.keys():
    all_lecture_vids = browser.find_elements_by_tag_name('a')
    course_directory = uni_year_term_directory + "/" + course_code
    if not os.path.exists(course_directory):
        os.mkdir(course_directory)
    export_directory = course_directory + "/lectures"
    if not os.path.exists(export_directory):
        os.mkdir(export_directory)
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
    lecture_num = 0
    for menu_opener in menu_openers:
        menu_opener.click()
        menu = browser.find_element_by_class_name("menu-items")
        menu.find_elements_by_tag_name("li")[1].click()

        select_wrapper = browser.find_element_by_class_name("select-wrapper")
        options = select_wrapper.find_elements_by_tag_name("option")
        HD_text = options[1].text
        video_link = options[1].get_attribute("value")
        print(video_link)
        export_name = export_directory+"/Week "+weeknames[lecture_num]+".mp4"

        # select_element = select_wrapper.find_element_by_tag_name("select")
        # quality_options_select = Select(select_element)
        # quality_options_select.select_by_visible_text(HD_text)

        # modal_footer = browser.find_element_by_class_name("modal-footer")
        # video_link = modal_footer.find_elements_by_tag_name("a")[1].get_attribute('href')
        # print(video_link)


        # r = urllib2.urlopen(video_link)
        # content = r.read()
        # # extract download link
        # download_url = json.loads(content)['link']
        # download_content = urllib2.urlopen(download_url).read()
        # # save downloaded content to file
        # f = open(export_directory+"/Week "+weeknames[lecture_num]+".mp4", 'wb')
        # f.write(download_content)
        # f.close()
        #download_file(video_link, export_name)

        urllib.request.urlretrieve(video_link, export_name)
        lecture_num = lecture_num + 1


        

    print("outta loop")



#logon to moodle
# logon_iframe = mydriver.find_element_by_xpath("//*[@id='region-main']/div/div[1]/iframe")
# mydriver.switch_to.frame(logon_iframe)
# username_box = mydriver.find_element_by_id("username")
# password_box = mydriver.find_element_by_id("password")
# username_box.send_keys(username)
# password_box.send_keys(password)
# submit_button = mydriver.find_element_by_xpath("/html/body/div/div/div/form/div[3]/input[1]")
# submit_button.click()


