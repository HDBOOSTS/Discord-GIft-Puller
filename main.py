import random
from urllib import request
import colorama, httpx, json, time, threading, ctypes
from colorama import Fore, Style, init
import os
import requests
from datetime import datetime

def clear_screen():
    try:
        os.system('cls')  
    except:
        os.system('clear')  
    return

init()

threads = input("Enter the number of threads to use: ")
display_errors = input("Do you want to show errors (y/n): ").lower()
display_errs = display_errors in ["y", "yes"]
clear_screen()
gray_color = "\033[90m" 
class Logger:
    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def Success(text):
        lock = threading.Lock()
        lock.acquire()
        timestamp = Logger.get_timestamp()
        print(f"{gray_color}{timestamp} {Fore.GREEN}[+]{Fore.WHITE} {text}")
        lock.release()

    @staticmethod
    def Error(text):
        lock = threading.Lock()
        lock.acquire()
        timestamp = Logger.get_timestamp()
        print(f"{gray_color}{timestamp} {Fore.RED}[-]{Fore.WHITE} {text}")
        lock.release()


def format_token(token_str):
    try:
        return token_str.split(":")[-1].strip()
    except IndexError:
        Logger.Error(f"Invalid token format: {token_str}")
        return None

def load_proxies():
    proxies = []
    try:
        with open("proxies.txt", "r") as file:
            proxies = [line.strip() for line in file.readlines() if line.strip()]
        if not proxies:
            Logger.Error("No proxies found in proxies.txt.")
    except FileNotFoundError:
        Logger.Error("proxies.txt file not found.")
    return proxies


def remove_line_from_tokens_file(token: str):
    with open('tokens.txt', "r") as f:
        lines = f.readlines()
    
    with open('tokens.txt', "w") as f:
        for line in lines:
            if line.strip("\n") != token:
                f.write(line)



class DiscordFetch:
    def __init__(self):
        self.tokens = []
        self.total_tokens = 0
        self.tokens_index = 0
        self.xbox_codes_claimed = 0
        self.display_err = display_errs
        self.cookies = None
        self.proxies = load_proxies()
        with open("tokens.txt", "r") as dataa:
            self.data = dataa.readlines()
            for token in self.data:
                self.tokens.append(token.strip())
                self.total_tokens += 1

    def get_cookies(self):
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.5",
            "connection": "keep-alive",
            "host": "canary.discord.com",
            "referer": "https://canary.discord.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
            "x-context-properties": "eyJsb2NhdGlvbiI6IkFjY2VwdCBJbnZpdGUgUGFnZSJ9",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MTc3Iiwib3NfdmVyc2lvbiI6IjEwLjAuMjAzNDgiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJoYXNfY2xpZW50X21vZHMiOmZhbHNlLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBkaXNjb3JkLzEuMC45MTc3IENocm9tZS8xMjguMC42NjEzLjE4NiBFbGVjdHJvbi8zMi4yLjcgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjMyLjIuNyIsIm9zX3Nka192ZXJzaW9uIjoiMjAzNDgiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjozNTg3ODksIm5hdGl2ZV9idWlsZF9udW1iZXIiOjU3MTI2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
        }

        try:
            response = httpx.get("https://discord.com/login", headers=headers)
            response.raise_for_status()
            if response.status_code in [200, 201, 202, 204]:
                cookies = response.cookies
                self.cookies = f"dcfduid={cookies.get('dcfduid')}; sdcfduid={cookies.get('sdcfduid')}; cfruid={cookies.get('cfruid')}; locale=en-US"
                return self.cookies
            else:
                raise Exception(f"Failed to retrieve cookies. Status code: {response.status_code}")
        except Exception as e:
            Logger.Error(f"Error fetching cookies: {e}")
            return None

    def start_discord(self):
        try:
            self.token = self.tokens[self.tokens_index]
            self.tokens_index += 1
        except IndexError:
            if self.total_tokens == self.tokens_index:
                Logger.Success("Successfully Claimed All Xbox Codes From All Tokens")
                time.sleep(1)
                exit(0)

        self.code = self.xbox_live_gamepass(self.token)
        if self.code == "error":
        
            return self.start_discord()

        with open("codes.txt", "a+") as file:
            file.write(f"{self.code}\n")


        
    
        return self.start_discord()


    def update_console_headers(self):
        while True:
            ctypes.windll.kernel32.SetConsoleTitleW(f"Xbox Code Fetcher | Tokens Loaded: {self.total_tokens} | Tokens Processed: {self.tokens_index} | Xbox Code Claimed: {self.xbox_codes_claimed}")

    def xbox_live_gamepass(self, token):
        formatted_token = format_token(token)
        if not self.cookies:
            self.get_cookies()

        pytk = formatted_token[:32] + "*" * 3
        if self.proxies:
                proxy = random.choice(self.proxies)
                if "://" not in proxy:
                    proxy = "http://" + proxy
                proxies = {"http://": proxy, "https://": proxy}
        else:
            proxies = {}
        url = 'https://discord.com/api/v10/outbound-promotions/1328402675645026435/claim'
        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"{formatted_token}",
            "Cookie": self.cookies,
            "Referer": "https://discord.com/channels/@me",
            "Sec-CH-UA": '"Google Chrome";v="103", "Chromium";v="103", "Not_A Brand";v="24"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9177 Chrome/128.0.6613.186 Electron/32.2.7 Safari/537.36",
            "X-Debug-Options": "bugReporterEnabled",
            "X-Discord-Locale": "en-US",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MTc3Iiwib3NfdmVyc2lvbiI6IjEwLjAuMjAzNDgiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJoYXNfY2xpZW50X21vZHMiOmZhbHNlLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBkaXNjb3JkLzEuMC45MTc3IENocm9tZS8xMjguMC42NjEzLjE4NiBFbGVjdHJvbi8zMi4yLjcgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjMyLjIuNyIsIm9zX3Nka192ZXJzaW9uIjoiMjAzNDgiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjozNTg3ODksIm5hdGl2ZV9idWlsZF9udW1iZXIiOjU3MTI2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
        }

        try:
            response = requests.post(url, headers=headers, proxies=proxies)

            if response.status_code == 401:
                Logger.Error(f"{Fore.RED}[ERROR] Token is invalid {Fore.RESET}- {Fore.CYAN}{pytk}{Fore.RESET}")
                return "error"

            if response.status_code == 403:
                response_json = response.json()
                errorcode = response_json.get('code')
                errormessage = response_json.get('message')
                
                if errorcode == 20015:
                    Logger.Error(f"{Fore.YELLOW}[WARN] {errormessage} {Fore.RESET}- {Fore.CYAN}{pytk}{Fore.RESET}")
                elif errorcode == 40071:
                    Logger.Error(f"{Fore.YELLOW}[WARN] {errormessage} {Fore.RESET}- {Fore.CYAN}{pytk}{Fore.RESET}")
                
                return "error"

            if response.status_code != 200:
                Logger.Error(f"{Fore.RED}[ERROR] Failed to claim Xbox code. Status Code: {response.text} {Fore.RESET}- {Fore.CYAN}{pytk}{Fore.RESET}")
                return "error"

        except Exception as err:
            if self.display_err:
                Logger.Error(f"{Fore.RED}[ERROR] Error making request: {err} {Fore.RESET}- {Fore.CYAN}{pytk}{Fore.RESET}")
            return "error"

        try:
            promotion_code = response.json().get('code')
            if promotion_code:
                Logger.Success(f"{Fore.GREEN}[SUCCESS] Claimed Xbox code: {promotion_code} {Fore.RESET}- {Fore.CYAN}{pytk}{Fore.RESET}")
                self.xbox_codes_claimed += 1
                return promotion_code
            else:
                raise Exception(f"No code returned in response. {Fore.CYAN}- {pytk}{Fore.RESET}")

        except Exception as err:
            if self.display_err:
                Logger.Error(f"{Fore.RED}[ERROR] Error extracting promotion code: {err} {Fore.RESET}- {Fore.CYAN}{pytk}{Fore.RESET}")
            return "error"
        
        
if __name__ == "__main__":
    discord_fetch = DiscordFetch()
    
    threading.Thread(target=discord_fetch.update_console_headers, daemon=True).start()
    
    for _ in range(int(threads)):
        threading.Thread(target=discord_fetch.start_discord, daemon=True).start()

    while True:
        time.sleep(1)
