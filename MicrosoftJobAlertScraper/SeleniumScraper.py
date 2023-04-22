from discord import SyncWebhook
from selenium import webdriver
from bs4 import BeautifulSoup
import params_file
import keyboard
import datetime
import time
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

finished = False
webhook = SyncWebhook.from_url(params_file.discord_webhook) 

print("Getting webpage results...")
driver = webdriver.Chrome()
driver.get(params_file.microsoft_job_alert)

latest_job_posting = datetime.datetime.now().replace(microsecond=0).isoformat()
time_attr = "data-ph-at-job-post-date-text"

message = """
    **Job Title:** [{data-ph-at-job-title-text}]({href})
    **Job Location:** {data-ph-at-job-location-text}
    **Job ID:** {data-ph-at-job-id-text}
    **Employment Type:** {data-ph-at-job-employment-type-text}
    **Time Posted**: {data-ph-at-job-post-date-text}\n
    **----------------------------------------------------------------------**
"""

while not finished:

    #Reset vars
    job_notif = "**NEW JOB(S) POSTED** @here"
    job_list = []
    
    #Get HTML and jobs
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    jobs = soup.find_all("li", "jobs-list-item")
    for each in jobs:
        job_list.append(each.find("a", attrs={"ph-tevent": "job_click"}))

    # Trim list to new postings only
    job_list = [
        x for x in job_list if
        datetime.datetime.strptime(x.attrs[time_attr], "%Y-%m-%dT%H:%M:%S" ) > 
        datetime.datetime.strptime(latest_job_posting, "%Y-%m-%dT%H:%M:%S" )
        ]

    #If new jobs, create and send message
    if len(job_list) > 0:
        for each in job_list:
            job_notif += message.format(**each.attrs)
        webhook.send(job_notif)

    #Wait 15 minutes
    time.sleep(960)

    print("Refreshing webpage...")
    driver.refresh()
    time.sleep(5)
    
    if keyboard.is_pressed("F12"):
        print("F12 pressed, exiting program...")
        driver.close()
        finished = True

    #Set latest posting time
    if len(job_list) != 0:
        latest_job_posting = job_list[0].attrs[time_attr] 