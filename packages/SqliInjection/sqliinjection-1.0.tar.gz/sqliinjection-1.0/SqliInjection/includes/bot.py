"""import requests
from SqliInjection.units import url
def sendmessage(vuln):
    bot_token='7678284125:AAEaUtUr1KaotVy2sDdkIwef4wCTS-9Ejj8'
    vuln = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": 5306997876,"text":f"Bug Name: SQLInjection\n{vuln}"}
    header = {
        "Content-Type":"application/json"
    }
    try:
        response = requests.post(url.data.telegram,json=data,headers=header)
        if response.status_code == 200:
            print("Message send Successfully")
        else:
            print(f"Failed to send message:{response.status_code}-{response.text}")
    except Exception as e:
        print(f"Bot Error:{e}")"""