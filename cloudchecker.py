"""Cloud Checker by rxyal """

import itertools
import string
import queue
import threading
from time import sleep, time
import traceback
import random
import os
from signal import signal, SIGINT
import requests
import json
from pathlib import Path
from urllib3.exceptions import MaxRetryError
import sys

VERSION = "1.0.5"

class Config:
    """Config class"""
    def __init__(self):
        self.config = None
        self.load_config()

    def load_config(self):
        with open('data/config.json', 'a') as f:
            if os.path.getsize("data/config.json") == 0:
                f.write("{}")
                f.close()
        

    def get(self, key):
        with open('data/config.json', 'r') as f:
            self.config = json.load(f)
        try:
            return self.config[key]
        except KeyError:
            return None
    
    def set(self, key, value):
        with open('data/config.json', 'r') as f:
            self.config = json.load(f)
        self.config[key] = value
        with open('data/config.json', 'w') as f:
            json.dump(self.config, f, indent=4)
        
    def get_all(self):
        with open('data/config.json', 'r') as f:
            self.config = json.load(f)
        return self.config


###############################################################
#                      Close on ctrl+c                        #
###############################################################
@staticmethod
def handler(signal_received, frame):
    # Handle any cleanup here
    print('\nSIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

signal(SIGINT, handler)







confirmators =  ["y", "yes", "1", "true", "t"]
negators =      ["n", "no", "0", "false", "f"]

os.makedirs("logs", exist_ok=True)
os.makedirs("results", exist_ok=True)  
os.makedirs("data", exist_ok=True)


def create_empty_file(file_path):
    file_path = Path(file_path)
    
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding='utf-8'):
            pass

def clear_file(file_path):
    file_path = Path(file_path)
    
    if file_path.exists():
        with file_path.open("w", encoding='utf-8'):
            pass


create_empty_file("logs/log.txt")
clear_file("logs/log.txt")


create_empty_file("results/hits.txt")

create_empty_file("data/names_to_check.txt")

create_empty_file("logs/error.txt")
clear_file("logs/error.txt")

create_empty_file("data/proxies.txt")

with Path("data/proxies.txt").open("r", encoding='utf-8') as proxies_file:
    proxies = proxies_file.read().splitlines()





config = Config()
lock = threading.Lock()





if len(proxies) == 0:
    proxies = [None]
proxy_cycle = itertools.cycle(proxies)


#Globals
RPS =       0
REQUESTS =  0
WORKS =     0
TAKEN =     0
DEACTIVATE = False


class Logger:
    """Logger class"""
    def __init__(self, file_name: str):
        """Initiate the class"""
        self.file_name = file_name
        self.file = open(self.file_name, "a")

    def log(self, message: str):
        """Log a message to the file"""
        self.file.write(f"{message}\n")
        self.file.flush()

    def close(self):
        """Close the file"""
        self.file.close()

 


class _Colors:
    """Menu colors"""
    @staticmethod
    def _color_code(code):
        """Static method to format color codes"""
        return f'\033[{code}m'


    ENDC: str =         _color_code(0)
    BOLD: str =         _color_code(1)
    UNDERLINE: str =    _color_code(4)
    BLACK: str =        _color_code(30)
    RED: str =          _color_code(31)
    GREEN: str =        _color_code(32)
    YELLOW: str =       _color_code(33)
    BLUE: str =         _color_code(34)
    MAGENTA: str =      _color_code(35)
    CYAN: str =         _color_code(36)
    WHITE: str =        _color_code(37)
    REDBG: str =        _color_code(41)
    GREENBG: str =      _color_code(42)
    YELLOWBG: str =     _color_code(43)
    BLUEBG: str =       _color_code(44)
    MAGENTABG: str =    _color_code(45)
    CYANBG: str =       _color_code(46)
    WHITEBG: str =      _color_code(47)
    GREY: str =         _color_code(90)


Colors = _Colors()

logger = Logger("logs/log.txt")


logger.log(f"CloudChecker started at {time()}")



def clear():
    """Clear the screen"""
    os.system('cls' if os.name=='nt' else 'clear')

clear()

class Pomelo:
    """Cloud Checker"""
    def __init__(self):
        """Initiate the class"""
        self.endpoint = "https://discord.com/api/v9"
        self.headers_post = {"Content-Type": "application/json"}
        self.session = requests.Session()
        self.proxies_not_working = []
        self.remove_proxies = config.get("remove_proxies")
        self.timeout = config.get("timeout")
        if self.timeout is None:
            self.timeout = 30

        logger.log(f"Timeout set to {self.timeout}")
        logger.log(f"Remove proxies set to {self.remove_proxies}")
        logger.log(f"Headers set to {self.headers_post}")

    # def restart_session(self):
    #     """Restart the session"""
    #     requests.Session.close(self.session)
    #     self.session = requests.Session()

    def proxy_err(self, name, proxy, proxy_cycle):
        name = [name, next(proxy_cycle)]
        logger.log(f"ReadTimeout with proxy {proxy}")
        if self.remove_proxies and proxy != None:
            logger.log(f"Removing proxy {proxy}")
            self.proxies_not_working.append(proxy)
        
        
    def  check(self, name: list):
        """Check if the name is available"""

    
        # self.restart_session()
        global RPS, REQUESTS, WORKS, TAKEN, DEACTIVATE
        proxy = None
        while not DEACTIVATE:
            try:
                try:
                    name, proxy = name
                # only name is passed
                except ValueError:
                    proxy = None
                    if proxy_cycle is not None:
                        proxy = next(proxy_cycle)
                        if len(self.proxies_not_working) >= len(proxies):
                            logger.log(f"Exiting because all proxies are not working")
                            
                            DEACTIVATE = True
                            # clear queue
                            logger.log(f"Clearing queue")
                            while username_queue.qsize() > 0:
                                username_queue.get()
                                username_queue.task_done()
                            logger.log(f"Queue cleared")
                            sleep(self.timeout+1)
                            print(f"\n{Colors.RED}No proxies left{Colors.ENDC}"*3)
                            
                            
                        while proxy in self.proxies_not_working:
                            proxy = next(proxy_cycle)
                        
                if proxy is not None:
                    proxy = f"http://{str(proxy).strip()}"

                
                # Logger.log(f"Checking {name} with proxy {proxy}")

                proxy_dict = {"http": proxy, "https": proxy} if proxy else None
                r = self.session.post(
                    url=self.endpoint + "/unique-username/username-attempt-unauthed",
                    headers = self.headers_post,
                    json={"username": name},
                    proxies=proxy_dict,
                    timeout=self.timeout
                ) 
                REQUESTS += 1

                if r.status_code in [200, 201, 204]:
                    if str(r.json()) in ["", None, "{}"]:
                        logger.log(f"Unexpected response resp = {r.text}")
                        return self.check(name)
                    

                    elif r.json()["taken"]:
                        TAKEN += 1
                        return [False, r.json(), r.status_code]

                    elif not r.json()["taken"]:
                        WORKS += 1
                        return [True, r.json(), r.status_code]

                #rate limited
                elif r.status_code == 429:
                    if proxy is None or proxy == "None" or proxy == "":

                        print("PROXYLESS RATELIMITED SLEEPING")
                        sleep(r.json()["retry_after"])
                        name = [name, next(proxy_cycle)]
                        return self.check(name)
                else:
                    logger.log(f"Unknown error with request {r.status_code}    |   {r.json()}")

            except requests.exceptions.ProxyError:
                self.proxy_err(name, proxy, proxy_cycle)
                return self.check(name)

            except requests.exceptions.ConnectionError:
                self.proxy_err(name, proxy, proxy_cycle)
                return self.check(name)
            
            except requests.exceptions.ReadTimeout:
                self.proxy_err(name, proxy, proxy_cycle)
                return self.check(name)
            
            except MaxRetryError:
                self.proxy_err(name, proxy, proxy_cycle)
                return self.check(name)



            except Exception:
            # timeout
                with lock:
                    try:
                        exception = traceback.format_exc()
                        logger.log(f"Unknown error with proxy {proxy}")
                        with open("logs/error.txt", "w") as f:
                            f.write(f"{exception}\n")
                            f.close()
                        sleep(0.3) # rest for 1s
                    except Exception:
                        pass
                return self.check(name)

g = Colors.GREY
r = Colors.RED
x = Colors.ENDC
ASCII = f"""
{g}                      :::!~!!!!!:.
                .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
            :!!!!!!?H! :!$!$$$$$$$$$$8X:
            !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
            :!~::!H!<   ~.U$X!?R$$$$$$$$MM!
            ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!
            !:~~~ .:!M"T#$$$$WX??#MRRMMM!
            ~?WuxiW*`   `"#$$$$8!!!!??!!!
            :X- M$$$$       `"T#$T~!8$WUXU~
            :%`  ~#$$$m:        ~!~ ?$$$$$$
        :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:``
?MXT@Wx.~    :     ~"##*$$$$M~

                    {r}@{x}  Cloud 2023                  {r}@{x}
                    {r}@{x}  github.com/cloudzik1337     {r}@{x}
                    {r}@{x}  discord.cloudzik.me         {r}@{x}
                    {r}@{x}  Version: {VERSION}              {r}@{x}
        """
clear()
print(ASCII)



# username can contain letters, numbers, and underscores
CHARS = string.ascii_lowercase + string.digits + "_" + '.'

with open("data/names_to_check.txt", "r", encoding='utf-8') as f:
    combos = f.read().splitlines()
    f.close()

with open("data/config.json", "r") as f:
    config_str = f.read()
    f.close()

if len(config_str) == 2 or os.path.getsize("data/config.json") == 0 or config.get("remove_proxies") is None:
    if config.get("webhook") is None:
        # Check if webhook URL is available in environment variables
        webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
        if webhook_url:
            print(f"{Colors.GREEN}Using webhook from environment variables{Colors.ENDC}")
            config.set("webhook", webhook_url)
            # Set default message
            message = "🎯 Available username: <name> | RPS: <RPS> | Time: <elapsed>s"
            print(f"{Colors.GREEN}Using default webhook message: {message}{Colors.ENDC}")
            config.set("message", message)
        else:
            ask_webhook = input(f"Send hits to webhook [y/n] {Colors.YELLOW}>>>{Colors.ENDC} ")
            if ask_webhook.lower() in confirmators:
                webhook = input(f"Webhook url {Colors.YELLOW}>>>{Colors.ENDC} ")
                config.set("webhook", webhook)
                print(f"{Colors.MAGENTA}Use <name> to send the name of the hit \nuse <@userid> to mention the user (replace user id with actuall id)\n<time> to send timestamp of the hit\nUse <RPS> to send requests per second\nUse <elapsed> to send elapsed time{Colors.ENDC}")
                message = input(f"Message to send {Colors.YELLOW}>>>{Colors.ENDC} ")
                config.set("message", message)
