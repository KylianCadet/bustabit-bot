from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import time
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys

HOST = ''
PORT = 8080
SIMULATION = True
HEADLESS = True
FIREFOX_DIR = "firefox_profile"
SCRIPT_NAME = "bustabit_script.js"

class MyHTTPHandler(BaseHTTPRequestHandler):
    """The request handler class for our server.
    It is instantiated once per connection to the server.
    """

    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/plain')
        self.end_headers()


        # get log textarea text
        self.server.webdriver.execute_script("document.getElementsByClassName('_1jjBnDK05lCAzmYgV4q7d7')[0].style.height = '800px'") # modify the height to have more log
        log = self.server.webdriver.find_element_by_xpath("//div[@class='ReactVirtualized__Grid ReactVirtualized__List _3xAcZv1JrYCV_Ajd1Cp11h']").text

        # Open profile screen
        self.server.webdriver.find_element_by_xpath("//a[@href='/account/overview']").click()

        # Wait for the information table to show
        wait = ui.WebDriverWait(self.server.webdriver, 1)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//table[@class='_1zLoOT7tI9HTWvoFSMtMUA _2pVOOBSgMNp3OXBpclwWYS table table-sm table-hover']")))
        except:
            self.wfile.write(b'error')
            return

        # Get usefull player informations
        game_profit = self.server.webdriver.find_element_by_xpath("//table[@class='_1zLoOT7tI9HTWvoFSMtMUA _2pVOOBSgMNp3OXBpclwWYS table table-sm table-hover']/tbody/tr[7]/td[2]").text
        username = self.server.webdriver.find_element_by_xpath("//div[@class='_1QUsIcc0SPjOxwvm2IHPh-']/h3").text
        balance = self.server.webdriver.find_element_by_xpath("//table[@class='_1zLoOT7tI9HTWvoFSMtMUA _2pVOOBSgMNp3OXBpclwWYS table table-sm table-hover']/tbody/tr[8]/td[2]").text

        # Close profile screen
        self.server.webdriver.find_element_by_xpath("//button[@class='close']").click()
        msg = 'Username : ' + username + '\nProfit : ' + game_profit + '\nBalance : ' + balance + '\n\n' + log
        self.wfile.write(bytes(msg, 'utf-8'))


class Server:
    """This class deserve the PORT variable
    It must be instantiated only once
    """

    _httpd = None

    def __init__(self, webdriver):
        self._httpd = HTTPServer((HOST, int(PORT)), MyHTTPHandler)
        self._httpd.webdriver = webdriver

    def run(self):
        self._httpd.serve_forever()


class Bustabit:
    """The Bustabit class is the core of this project
    It instantiate and run the selenium's webdriver used to communicate with the bustabit site
    """

    _error = False
    _webdriver = None
    _script = None

    def __init__(self, profile_folder, script_name):
        fd = open(script_name, "r")
        self._script = fd.read()
        fd.close()

        # Launch Firefox GUI in headless mode
        opt = webdriver.FirefoxOptions()
        opt.headless = HEADLESS
        self._webdriver = webdriver.Firefox(firefox_profile=profile_folder, options=opt)
        return

    def _connect(self):
        """Init webdriver"""

        self._webdriver.get('https://www.bustabit.com/play')

        # Wait until we find the presence of the 'auto' button
        try:
            wait = ui.WebDriverWait(self._webdriver, 5)
            wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='/account/overview']")))
        except:
            print('Are you sure you are logged with your profile ?')
            self._error = True
        return

    def _auto_bet(self):
        """Starting auto bet with the user script (butabit_script.js)"""

        # Get and click on 'Auto' button
        self._webdriver.find_element_by_xpath("//div[@class='bet-controls']/div/a[2]").click()

        # Get and click on the 'New' button
        self._webdriver.find_element_by_xpath("//button[@class='btn btn-success btn-xs btn btn-primary']").click()
        time.sleep(1) # Wait for the popup to dislay

        # Fill the text area with the user script
        text_area = self._webdriver.find_element_by_xpath("//textarea[@rows=8]")
        text_area.click()
        text_area.send_keys(Keys.CONTROL, 'a')
        text_area.send_keys(Keys.RETURN)
        text_area.send_keys(self._script)

        # Get and click on the 'Save Script' button
        self._webdriver.find_element_by_xpath("//button[@class='btn btn-success' and @type='submit']").click()
        time.sleep(1)

        # Get and click on the 'Arrow' button
        self._webdriver.find_element_by_xpath("//ul[@class='PynYN1mGJjFu9UXQGsHTQ']/li[6]/span/button[1]").click()

        if (SIMULATION):
            # Get and click on 'Simulation' checkbox
            self._webdriver.find_element_by_xpath("//input[@id='simulationModeCheck']").click()

            # Get and fill the 'simulated balance'
            SIMULATED_BALANCE = 100000
            simulated_balance_textbox = self._webdriver.find_element_by_name("simulatedBalance")
            simulated_balance_textbox.clear()
            simulated_balance_textbox.send_keys(str(SIMULATED_BALANCE))

        # Get and click on the 'Run script' button
        time.sleep(1)
        self._webdriver.find_element_by_xpath("//button[@class='_14fFtlT1cpnw5CHIWeqBgY btn btn-success']").click()
        return

    def _run(self):
        """Infinite loop"""
        s = Server(self._webdriver)
        s.run()

    def start(self):
        """Start the Bustabit bot"""
        self._connect()
        if (self._error):
            self._webdriver.quit()
            return
        self._auto_bet()
        self._run()
        return

if __name__ == "__main__":
    if not os.path.isdir(FIREFOX_DIR):
        print(FIREFOX_DIR + ' must be a directory')
        exit(1)
    if not os.path.isfile(SCRIPT_NAME):
        print(SCRIPT_NAME + ' must be a file')
        exit(1)
    bot = Bustabit(FIREFOX_DIR, SCRIPT_NAME)
    bot.start()
    exit(0)
