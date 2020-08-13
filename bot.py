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
SIMULATION = False
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

        # click on "Copy" (log) button
        self.server.webdriver.find_element_by_xpath("/html/body/div/div/div/div[5]/div/div[2]/div[2]/button").click()

        # Open profile screen
        self.server.webdriver.find_element_by_xpath("//a[@href='/account/overview']").click()

        # Wait for the information table to show
        wait = ui.WebDriverWait(self.server.webdriver, 1)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/table")))
        except:
            self.wfile.write(b'error')
            return

        # Create a textarea into the profile screen
        self.server.webdriver.execute_script("""
            var input = document.createElement('textarea');
            input.id = 'my-textarea';
            var body = document.getElementsByClassName('modal-content')[0]
            body.appendChild(input);
        """)

        # get the textarea, paste the log and retreive its content
        textarea = self.server.webdriver.find_element_by_xpath("//*[@id='my-textarea']")
        textarea.send_keys(Keys.CONTROL + "v")
        log = textarea.get_attribute("value")

        # Get usefull player informations
        game_profit = self.server.webdriver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div/div/div/div/table/tbody/tr[7]/td[2]").text
        username = self.server.webdriver.find_element_by_xpath("//header/div/h3").text
        balance = self.server.webdriver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div/div/div/div/table/tbody/tr[8]/td[2]").text

        # Close profile screen
        self.server.webdriver.find_element_by_xpath("/html/body/div[3]/div/div/div[1]/button").click()

        # Create and send response
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
        if (opt.headless is False):
            print("Running in non headless mode !")
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
        self._webdriver.find_element_by_xpath("/html/body/div/div/div/div[5]/div/div[1]/a[2]").click()

        # Get and click on the 'New' button
        self._webdriver.find_element_by_xpath("/html/body/div/div/div/div[5]/div/div[2]/div/div/button").click()
        time.sleep(1) # Wait for the popup to dislay

        # Fill the text area with the user script
        text_area = self._webdriver.find_element_by_xpath("//form/textarea")
        text_area.click()
        text_area.send_keys(Keys.CONTROL, 'a')
        text_area.send_keys(Keys.RETURN)
        text_area.send_keys(self._script)

        # Get and click on the 'Create Script' button
        self._webdriver.find_element_by_xpath("//form/div/button").click()
        time.sleep(1)

        # Get and click on the 'Arrow' button
        self._webdriver.find_element_by_xpath("//ul/li[6]/span/button[1]").click()

        if (SIMULATION):
            # Get and click on 'Simulation' checkbox
            self._webdriver.find_element_by_xpath("//*[@id='simulationModeCheck']").click()

            # Get and fill the 'simulated balance'
            SIMULATED_BALANCE = 100000
            simulated_balance_textbox = self._webdriver.find_element_by_name("simulatedBalance")
            simulated_balance_textbox.clear()
            simulated_balance_textbox.send_keys(str(SIMULATED_BALANCE))

        # Get and click on the 'Run script' button
        time.sleep(1)
        self._webdriver.find_element_by_xpath("//form/button").click()
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
