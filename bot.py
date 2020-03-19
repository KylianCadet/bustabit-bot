import time
import signal
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys

class Bustabit:
    _browser = None
    _error = False

    def __init__(self, firefox_folder):
        # Launch Firefox GUI
        self._browser = webdriver.Firefox(firefox_folder)

        # Catch SIGINT to close browser before exiting
        def signal_handler(signal, frame):
            self._browser.quit()
            exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        return

    def _login(self):
        """Login into bustabit by getting the login pages"""
        self._browser.get('https://www.bustabit.com/login')

        # Get username and password textboxes
        user_textbox = self._browser.find_element_by_name("uname")
        password_textbox = self._browser.find_element_by_name("password")

        # Fill userame and password textboxes
        user_textbox.send_keys(self._username)
        password_textbox.send_keys(self._password)

        # Click on submit button
        sumbit_button = self._browser.find_element_by_class_name("btn-lg")
        sumbit_button.click()
        return

    def _connect(self):
        """Init browser"""
        self._browser.get('https://www.bustabit.com/play')

        # Wait until we find the presence of tha 'auto' button
        try:
            wait = ui.WebDriverWait(self._browser, 5)
            wait.until(EC.presence_of_element_located((By.XPATH, "//li[@class='' and @role='presentation']/a[@role='button' and @href='#']")))
        except:
            self._error = True
        return

    def _auto_bet(self):
        """Starting auto bet with flat bet strategie in simulated mode"""

        # Get and click on 'Auto' button
        auto_button = self._browser.find_element_by_xpath("//li[@class='' and @role='presentation']/a[@role='button' and @href='#']")
        auto_button.click()

        # Get and click on 'Flat bet' arrow button
        flat_bet_button = self._browser.find_element_by_xpath("//button[@class='btn btn-xs btn-default']")
        flat_bet_button.click()

        # Get and click on 'Simulation' checkbox
        simulation_button = self._browser.find_element_by_xpath("//div[@class='checkbox simCheckbox']/label/input[@type='checkbox']")
        simulation_button.click()

        # Get and fill the 'simulated balance'
        SIMULATED_BALANCE = 100000
        simulated_balance_textbox = self._browser.find_element_by_name("simulatedBalance")
        simulated_balance_textbox.clear()
        simulated_balance_textbox.send_keys(str(SIMULATED_BALANCE))

        # Get and click on the 'Run script' button
        run_script_button = self._browser.find_element_by_xpath("//button[@class='btn btn-success' and @type='submit']")
        run_script_button.click()
        return

    def _run(self):
        """Infinite loop"""
        while True:
            time.sleep(1)

    def start(self):
        """Start the Bustabit bot"""
        self._connect()
        if (self._error):
            print('Are you sure you are logged with your profile ?')
            self._browser.quit()
            return
        self._auto_bet()
        self._run()
        return


def print_usage():
    print("python3 bot.py [firefox_folder]")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_usage()
        exit(0)
    bot = Bustabit(sys.argv[1])
    bot.start()
    exit(0)
