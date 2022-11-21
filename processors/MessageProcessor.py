import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import cloudinary
import cloudinary.uploader
from webdriver_manager.chrome import ChromeDriverManager

# heroku config
import environ
env = environ.Env()
environ.Env.read_env()
json_file = env('CONFIG')
config = json.loads(json_file)

# Local config
# with open('config.json') as json_file:
#     config = json.load(json_file)

cloudinary.config(
    cloud_name = config["cloudinary"]["cloud_name"],
    api_key = config["cloudinary"]["api_key"],
    api_secret = config["cloudinary"]["api_secret"],
    secure = True
)

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

# driver_path = "./chromedriver"
# brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
option = webdriver.ChromeOptions()
# option.binary_location = GOOGLE_CHROME_PATH
option.add_argument('--no-sandbox')
option.add_argument('--headless')
option.add_argument('--disable-gpu')
option.add_argument('window-size=1295x775')
# driver = webdriver.Chrome(executable_path=GOOGLE_CHROME_PATH, options=option)
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
url_login = 'https://ecampus.psgtech.ac.in/studzone2/'
url_attandance = 'https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx'
url_camarks = 'https://ecampus.psgtech.ac.in/studzone2/CAMarks_View.aspx'
url_result = 'https://ecampus.psgtech.ac.in/studzone2/FrmEpsStudResult.aspx'

class MessageProcessor():
    def __init__(self):
        pass

    def getPassword(self, user):
        return config["student_credentials"][user]

    def reply(self, user):
        student_rollno = user
        student_password = self.getPassword(user)
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
        driver.get(url_login)
        driver.find_element(by=By.NAME, value='txtusercheck').send_keys(student_rollno)
        driver.find_element(by=By.NAME, value='txtpwdcheck').send_keys(student_password)
        driver.find_element(by=By.NAME, value='abcd3').send_keys(Keys.ENTER)
        # Attandance screenshot
        driver.get(url_attandance)
        im = driver.get_screenshot_as_png()
        attandance_res = cloudinary.uploader.upload(im, public_id=user + '_attandance', overwrite=True)
        
        # CA marks screenshot
        driver.get(url_camarks)
        im = driver.get_screenshot_as_png()
        camarks_res = cloudinary.uploader.upload(im, public_id=user + '_camarks', overwrite=True)

         # Results screenshot
        driver.get(url_result)
        results_res = None
        try:
            im = driver.get_screenshot_as_png()
            results_res = cloudinary.uploader.upload(im, public_id=user + '_results', overwrite=True)
        except:
            pass

        # End Session
        driver.quit()
        if results_res:
            return [attandance_res['url'], camarks_res['url'], results_res['url']]
        else:
            return [attandance_res['url'], camarks_res['url']]
