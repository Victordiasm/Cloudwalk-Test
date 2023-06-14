import os, traceback, logging, time, re, json
from pathlib import Path

# Class of the Quake Log file
# Input: String with path to file.
# Attributes: raw_log, log_list, match_list
# Methods: find_matches()
class quake_log_file():
    def __init__(self, file):
        logging.info("Initializing read of file {}".format(file))
        with open(file, "r", encoding="utf-8") as log_file: # Open log file.
            game_log = log_file.read()
            log_list = game_log.split("\n")
        self.raw_log = game_log     # Raw Log for occasional future use
        self.log_list = log_list    # raw log split by lines in a list for occasional future use
        self.match_list = []        # Empty list to be filled with matches


# Class of the quake match
# Input: match_log_list.
# attributes: 
# Methods:
class quake_match():
    def __init__(self, match_log, match_n, **kwargs):
        self.match_n = match_n
        self.match_log = match_log

def main():
    path_cwd = Path(os.getcwd())    # Get current directory
    path_log = path_cwd/"logs"      # Path for logging
    path_db = path_cwd/"db"         # Path for databases
    current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) #Get current local time
    try:
        logging.basicConfig(filename=path_log/"{}.log".format(current_time), encoding="utf-8", level=logging.INFO, filemode="w", format="%(asctime)s %(message)s") # Basic configuration for logging
        logging.info("Initing log-parser")
    except OSError: # In case there's no folder on working directory
        os.mkdir(path_log)
        logging.basicConfig(filename=path_log/"{}.log".format(current_time), encoding="utf-8", level=logging.INFO, filemode="w", format="%(asctime)s %(message)s")
        logging.info("Initing log-parser")
        logging.info("Log folder not present, creating one".format(path_log/"{}.log".format(current_time)))
        logging.error(traceback.format_exc())   # Writes python except on log file.
    except:
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    main()
