# path to 'geckodriver' file
GECKODRIVER_PATH = "/usr/bin/geckodriver"
# email and password for testing
AUTH_EMAIL = "esiatest002@yandex.ru"
AUTH_PASS = "11111111"
# role name - needs to match exactly
AUTH_ROLE = "Фамилия002 Имя002  Отчество002"

# delay between each interaction with browser
# if you have problems with script missing some clicks, consider setting it to a higher value
DELAY_BETWEEN_ACTIONS = 0.1
# if set to True, will close browser automatically after completing all actions
CLOSE_AFTER_TEST = True
# if previous setting is set to True, this will determine how many seconds will browser wait before automatically closing
WAIT_AFTER_TEST = 1

# file for logs of all network interactions
LOG_FILE = "network.log"

