import os, traceback, logging, time, log_parser, sys
from pathlib import Path

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
    quake_game = log_parser.quake_log_file(sys.argv[1])
    quake_game.find_matches()
    quake_game.rank_players()
    for match in quake_game.match_list:
        print("game_{}:".format(match.match_n), match.match_json)
    print("-----------------")
    print(quake_game.log_ranking_json)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()
    else:
        print("report.py uses an argument of the log path. Please include one. Example: py report.py .\db\qgames.log")
    
