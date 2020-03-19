import time
import signal
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys

class Bustabit:
    _browser = None
    _script_name = None
    _wager = None
    _error = False

    def __init__(self, firefox_profile, script_name = None):
        # Launch Firefox GUI
        self._browser = webdriver.Firefox(firefox_profile=firefox_profile, firefox_binary="./firefox/firefox", executable_path="./firefox/geckodriver")
        self._script_name = script_name

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

    def _load_script(self):

        # Get and click on 'New' button
        edit_flatbet_script = self._browser.find_element_by_xpath("//button[@class='btn btn-xs btn-info']")
        edit_flatbet_script.click()

        # Paste your script in the textarea
        script_textarea = self._browser.find_element_by_xpath("//textarea[@class='form-control']")
        script_textarea.click()
        script_textarea.send_keys(Keys.CONTROL, 'a')
        print('Reading "' + self._script_name + '", this may take several seconds')
        try:
            file = open(self._script_name, "r")
        except:
            sys.stderr.write("No such file : " + self._script_name + "\n")
            exit(84)
        script_textarea.send_keys(file.read())
        print('Script saved')
        file.close()

        # Get and click on 'Create' button
        create_script_button = self._browser.find_element_by_xpath("//button[@class='btn btn-success']")
        create_script_button.click()

    def _fill_config(self):

        # Ask user and fill wager field
        wager_input = self._browser.find_element_by_css_selector(".form-group:nth-child(1) > .input-group > .form-control")
        # wager_input = self._browser.find_elements_by_xpath("//span[@class='input-group']/span[contains(text(), 'wager')]/following-sibling::input")
        wager_input.click()
        wager_input.send_keys(Keys.CONTROL, 'a')
        wager_input.send_keys(Keys.BACKSPACE)
        print("How much do you want to wager?")
        self._wager = input()
        while self._wager is None or isNumber(self._wager) is False or float(self._wager) < 1 or float(self._wager) > 1000:
            print("Please try again:")
            self._wager = input()
        self._wager = round(float(self._wager))
        wager_input.send_keys(str(self._wager))

        # Ask user and fill payout field
        payout_input = self._browser.find_element_by_css_selector(".form-group:nth-child(2) > .input-group > .form-control")
        # wager_input = self._browser.find_elements_by_xpath("//span[@class='input-group']/span[contains(text(), 'wager')]/following-sibling::input")
        payout_input.click()
        payout_input.send_keys(Keys.CONTROL, 'a')
        payout_input.send_keys(Keys.BACKSPACE)
        print("How much do you want to set the payout?")
        self._wager = input()
        while self._wager is None or isNumber(self._wager) is False or float(self._wager) < 1 or float(self._wager) > 1000:
            print("Please try again:")
            self._wager = input()
        payout_input.send_keys(str(self._wager))

    def _auto_bet(self):
        """Starting auto bet with flat bet strategie in simulated mode"""

        # Get and click on 'Auto' button
        auto_button = self._browser.find_element_by_xpath("//li[@class='' and @role='presentation']/a[@role='button' and @href='#']")
        auto_button.click()

        if self._script_name is not None:
            self._load_script()

        # Get and click on the first script arrow button
        my_script_button = self._browser.find_element_by_xpath("//button[@class='btn btn-xs btn-default']")
        my_script_button.click()

        self._fill_config()

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
        print("Bustabit bot starting...")
        self._connect()
        if (self._error):
            print('Are you sure you are logged with your profile ?')
            self._browser.quit()
            return
        print("Browser ready")
        self._auto_bet()
        print('Script starting...')
        self._run()
        return

def isNumber(nb):
    try:
        float(nb)
    except:
        sys.stderr.write("Error: '" + str(nb) + "' is not a number\n")
        return False
    return True

def print_usage():
    print("python3 bot.py firefox_folder [script]")

if __name__ == "__main__":
    if "-h" in sys.argv or len(sys.argv) < 2 or len(sys.argv) > 3:
        print_usage()
        exit(0)
    if len(sys.argv) == 2:
        bot = Bustabit(sys.argv[1])
    if len(sys.argv) == 3:
        bot = Bustabit(sys.argv[1], sys.argv[2])
    bot.start()
    exit(0)
