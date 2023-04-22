from discord import SyncWebhook
import keyboard
import time
import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup


chromedriver_autoinstaller.install()

finished = False
webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/1099195527695974421/d9Wmt_y4ao70dXb5Sk1nRkqF5FhkVEKX_DLCuD6RyG1A2lvQl-qZxkD25nrtf2pcQPGU") 
print("Starting up program...")

attributes = {
    "ph-tevent": "job_click"
}

while not finished:
    job_list = []
    print("Getting webpage...")
    driver = webdriver.Chrome()
    driver.get("https://careers.microsoft.com/us/en/search-results?ak=t4csf8iad2ra")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    jobs = soup.find_all("li", "jobs-list-item")

    for each in jobs:
        job = each.find("a", attrs=attributes)
        job_list.append(job)

    
    time.sleep(5)
    webhook.send("Hello, World!")
    
    if keyboard.is_pressed("F12"):
        print("F12 pressed, exiting program...")
        finished = True