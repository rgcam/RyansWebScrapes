from discord import SyncWebhook
import requests
import keyboard
import time

finished = False
webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/1099195527695974421/d9Wmt_y4ao70dXb5Sk1nRkqF5FhkVEKX_DLCuD6RyG1A2lvQl-qZxkD25nrtf2pcQPGU") 
print("Starting up program...")

while not finished:
    print("Getting webpage...")
    webpage_response = requests.get("https://careers.microsoft.com/us/en/search-results?ak=t4csf8iad2ra")
    webpage = webpage_response.text

    #try:
    listStart = webpage.index("<!--Facet results-->")
    listEnd = webpage.index("<!--End Facet results-->")
    jobsListStr = ""
    print("Trimming results to list...")
    for i in range (listStart + len("<!--Facet results-->") + 1, listEnd):
        jobsListStr += webpage[i]
    #except:
    #    print("Failed to trim results! Please make sure URL is correct.")
    
    with open('htmldump.txt', encoding="utf-8") as f:
        f.write(webpage.text)
    time.sleep(5)

    webhook.send("Hello, World!")
    
    if keyboard.is_pressed("F12"):
        print("F12 pressed, exiting program...")
        finished = True