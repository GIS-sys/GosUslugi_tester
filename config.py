# path to 'geckodriver' file
GECKODRIVER_PATH = "/usr/bin/geckodriver"
# file for logs of all network interactions
LOG_FILE = "network.log"
# path for downloading vm/pdf
DOWNLOAD_PATH = "/download"
# path where all .scn files are
SCENES_FOLDER = "data"

# if line in .scn file starts with one of these, it will count as a comment
ACTIONS_COMMENTS = ("#", "//")
# if line in .scn starts with one of these, it will count as a config rule
CONFIG_LINESTART = ("!")

# delay between each interaction with browser
# if you have problems with script missing some clicks, consider setting it to a higher value
DELAY_BETWEEN_ACTIONS = 0.25
# total delay during LOOKUP action
DELAY_ACTION_LOOKUP = 2
# total delay during ADDRESS action
DELAY_ACTION_ADDRESS = 1

# if set to True, will close browser automatically after completing all actions
CLOSE_AFTER_TEST = True
# if previous setting is set to True, this will determine how many seconds will browser wait before automatically closing
WAIT_AFTER_TEST = 1

