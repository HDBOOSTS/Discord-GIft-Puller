# Discord-Gift-Puller
This script allows you to pull Xbox gift codes from Discord tokens using a multi-threaded approach. It retrieves Xbox Live GamePass codes from Discord promotions.




Discord Server - https://discord.hdboosts.cc
Website - https://hdboosts.mysellix.io  - https://hdboosts.cc






Requirements
- Python 3.x
- colorama for colorful terminal output
- httpx for handling HTTP requests
- requests for handling HTTP requests (for Discord API)
- Proxies (optional, for rotating IPs to avoid rate-limiting)
- A list of Discord tokens in a file (tokens.txt)
- A list of proxies in a file (proxies.txt, optional)


Installation
Clone the repository:

git clone https://github.com/HDBOOSTS/Discord-GIft-Puller.git

Install the required dependencies:

pip install -r requirements.txt

Make sure you have the necessary files:
tokens.txt – This file should contain one Discord token per line.
proxies.txt (Optional) – This file should contain one proxy URL per line (e.g., USER:PASS@HOST:PORT).


How to Use
Run the script using the following command:

python main.py

The script will prompt you for input:

Number of Threads: Enter the number of threads you want to use for fetching the codes (e.g., 5).
Display Errors: Choose whether you want errors to be displayed by entering y or n.

The script will begin processing tokens and attempting to claim Xbox gift codes. You will see color-coded success and error messages in the console.

The claimed Xbox codes will be saved in the codes.txt file.

Script Explanation
Token Format: Tokens must be in the format user:pass:token or just token

Proxies: The script will attempt to use proxies from proxies.txt to rotate the IP for each request. This helps avoid rate-limiting.
Concurrency: The script uses multiple threads to speed up the process of claiming codes. You can specify how many threads to use at the beginning.
Logging: Logs are displayed with timestamps, including success and error messages.

Configuration
tokens.txt: This file should contain one Discord token per line. The script will iterate through each token to claim Xbox codes.
proxies.txt (Optional): If you want to use proxies, create this file and add your proxy addresses in the format http://proxy.com.

Example:

tokens.txt:

user1:token1
user2:token2
user3:token3


proxies.txt (optional):

http://proxy1.com
http://proxy2.com
http://proxy3.com


Error Handling
If a token is invalid, it will be skipped, and an error message will be shown in the log.
If the script encounters issues with claiming Xbox codes (e.g., rate limiting, network errors), it will retry with the next token.


DO NOT SKID THIS TOOL 
