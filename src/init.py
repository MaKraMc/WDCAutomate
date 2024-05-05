import re
from os import getenv

def init():
    print(r"""
 __          _______   _____               _                        _        
 \ \        / /  __ \ / ____|   /\        | |                      | |       
  \ \  /\  / /| |  | | |       /  \  _   _| |_ ___  _ __ ___   __ _| |_ ___  
   \ \/  \/ / | |  | | |      / /\ \| | | | __/ _ \| '_ ` _ \ / _` | __/ _ \ 
    \  /\  /  | |__| | |____ / ____ \ |_| | || (_) | | | | | | (_| | ||  __/ 
     \/  \/   |_____/ \_____/_/    \_\__,_|\__\___/|_| |_| |_|\__,_|\__\___| 
""")

    # Get the platform environment variable
    platform = getenv("PLATFORM") or "dslvip.com"
    platform = re.sub(r'^https?://', '', platform)
    platform = platform.split('/')[0]

    return platform