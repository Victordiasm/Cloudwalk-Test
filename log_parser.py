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
    # This funcion scans through the lines of the log in search of the message InitGame and ShutdownGame to separete matches.
    def find_matches(self):
        init_game_regex = re.compile(r".*InitGame:.*")           # Regex to match the initiation of a game
        shutdown_game_regex = re.compile(r".*ShutdownGame:.*")   # Regex to match the shutdown of a game
        init_recording = False
        i = 1
        logging.info("Initializing find_matches from quake_log_file class")
        for line in self.log_list:                  # Scans the log for the InitGame and ShutdownGame lines for recording the matches
            if re.search(init_game_regex, line):
                if not init_recording:
                    init_recording = True
                    match_record = []               # Resets the match record for first/another recording
                elif init_recording:                # In case the game starts without shutdown the last game
                    self.match_list.append(quake_match(match_record, i))    # appends the recorded match to the match list with the match number
                    i += 1
                    match_record = []
            elif re.search(shutdown_game_regex, line):
                init_recording = False
                self.match_list.append(quake_match(match_record, i))
                i += 1
            elif init_recording:
                match_record.append(line)

# Class of the quake match
# Input: match_log_list, match_number.
# attributes: match_n, match_log, total_kills, players, kills, match_dict, match_json
# Methods:
class quake_match():
    def __init__(self, match_log, match_n, **kwargs):
        self.match_n = match_n      # Match number for tracking
        self.match_log = match_log  # Match_log
        self.total_kills = 0        # Total kills in the match
        self.players = []           # Match players list
        self.kills = {}             # Kill dict for players
        self.kills_by_means = {}    # Kill means for tracking
        self.analyze_match()        
        self.match_dict = {"total_kills":self.total_kills, "players":self.players, "kills":self.kills, "kills_by_mean":self.kills_by_means} # Dict with all data required
        self.match_json = json.dumps(self.match_dict, indent=1) # Json of the match dict
    # This function analyses the data looking for kills
    def analyze_match(self):
        logging.info("Initializing analyze_match from quake_match class")
        player_regex = re.compile(r'.*ClientUserinfoChanged: [0-9]+ n\\(.*?)\\t.*')           # Regex for identifying players names
        kill_regex = re.compile(r".+Kill: [0-9]+ [0-9]+ [0-9]+: (.*) killed (.*) by .+")    # Regex for identifying kills
        for line in self.match_log:                             # Search the log for the player name and kill message
            if re.search(player_regex, line) != None:           # True if initing game
                regex_match = re.search(player_regex, line)
                player_name = regex_match.group(1)              
                if player_name not in self.players: # Introduct the player name in the class
                    self.players.append(player_name)
                    if player_name not in self.kills: self.kills[player_name] = 0 
            elif re.search(kill_regex, line) != None:
                self.total_kills += 1
                regex_match = re.search(kill_regex, line)
                player_kill = regex_match.group(1)      # Player who killed
                player_killed = regex_match.group(2)    # Player who got killed
                if player_kill == "<world>": self.kills[player_killed] += -1 # In case the player got killed by the world
                else: 
                    self.kills[player_kill] += 1

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
