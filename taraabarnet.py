from telethon import TelegramClient, sync
from telethon import utils
import re
import csv

# Special attributes for Taraabarnet channel
target_exp ="مبداء" # "اعلام بار ترابرنت"
keyword = [["نوع بار", "محموله", "نام کالا", "نام :"],
           ["مبداء", "null", "null", "null"],
           ["مقصد", "null", "null", "null"],
           ["نوع ماشین", "وسیله", "نوع وسیله", "null"],
           ["وزن", "تناژ", "null", "null"],
           ["زمان بارگیری", "تاریخ بارگیری", "null", "null"]]

# Parser function
def parser(value):
    content = value.splitlines()
    result = [""]*6
    for i in range(0, 6):
        for k in range(0, 4):
            for j in range(0, len(content)):
                if bool(re.search(keyword[i][k], content[j])) is True:
                    result[i] = content[j].replace(keyword[i][k], "")
                    # print(content[j].replace(keyword[i][k], ""))
                    break

    if result[0] == "":
        for j in range(0, len(value.splitlines())):
            if bool(re.search(r'#', value.splitlines()[j])) is True:
                result[0] = value.splitlines()[j].replace("#","")
                break
    return result;

# Identity for authorization by Telegram server
api_id = 
api_hash = 
phone_number = 

# Connecting to Telegram server and authorization in case of need
client = TelegramClient('/home/amirdaghestani/PycharmProjects/client', api_id = api_id, api_hash = api_hash)
client.connect()
print("Successfully connected to Telegram server")

if not client.is_user_authorized():
    client.send_code_request(phone_number)
    me = client.sign_in(phone_number, input ('Enter code: '))
else:
    print("Client is authorized")

# Hooray! Crawling starts
# Just parse those messages with target keyword
#  Check which tuple has a value; in this case number 1!
tarabar_hist = []
for message in client.iter_messages('@taraabarnet', limit = 20000000):
    content = utils.get_display_name(message.sender), message.message

    if bool(re.search(target_exp, ''.join(str(content)))) is True:
        tarabar_hist.append(parser(content[1]))
    else:
        continue

with open('taraabarnet.csv', 'w', encoding = 'utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerows(tarabar_hist)

