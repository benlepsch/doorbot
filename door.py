from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from credentials import username, password, token
import time, discord, asyncio




chrome_options = Options()
chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')

class DoorClient(discord.Client):
    async def on_ready(self):
        print('logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------------')


        self.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=chrome_options)
        self.driver.get('https://csg-web1.eservices.virginia.edu/student/openmydoor.php')

        # if we already lgged in dont fucking log in!
        try:
            link = self.driver.find_element_by_link_text('Click to login...')
            link.click()
            # netbadge login
            try:
                inputUser = self.driver.find_element_by_name('j_username')
                inputUser.send_keys(username)

                inputPass = self.driver.find_element_by_name('j_password')
                inputPass.send_keys(password)


                # click login
                link = self.driver.find_element_by_name('_eventId_proceed')
                link.click()

                # duo shit
                try:
                    time.sleep(3)
                    
                    iframe = self.driver.find_element_by_xpath('//*[@id="duo_iframe"]')
                    # iframe = self.driver.find_element_by_xpath('/html/body/main/iframe')
                    # self.driver.switchTo().frame('duo_iframe')
                    self.driver.switch_to.frame(iframe)

                    remember_me = self.driver.find_element_by_xpath('//*[@id="login-form"]/div[2]/div/label/input')
                    # remember_me = self.driver.find_element_by_xpath('/html/body/div/div/div[1]/div/form/div[2]/div/label/input')
                    remember_me.click()
                    
                    push = self.driver.find_element_by_xpath('//*[@id="auth_methods"]/fieldset/div[1]/button')
                    push.click()
                except:
                    pass
            except:
                pass
        except:
            pass

        # door shit here

        while True:
            if self.driver.current_url == 'https://csg-web1.eservices.virginia.edu/student/welcome.php':
                break


        time.sleep(1)
        # go to main menu
        link = self.driver.find_element_by_xpath('//*[@id="leftnav"]/a')
        link.click()

        time.sleep(1)
        link = self.driver.find_element_by_xpath('//*[@id="mmenu"]/div[2]/table/tbody/tr[1]/td[2]/a')
        link.click()

        time.sleep(1)
        self.refresh_page()
    
    async def refresh_page(self):
        time.sleep(30*60)
        self.driver.refresh()
        self.refresh_page()

    def open_door(self):
        try:
            link = self.driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[2]/div/form[1]/ul/li/input[3]')
            link.click()
        except:
            time.sleep(3)
            link = self.driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[2]/div/form[1]/ul/li/input[3]')
            link.click()

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('open door'):
            self.open_door()
            await message.author.send('pin is 5150')
client = DoorClient()
client.run(token)
