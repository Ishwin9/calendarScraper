import pandas
import time
import webdriver_manager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https:www.scotiabankarena.com/events-1/calendar')

scrapingData = []
for x in range(6):
    #Go back to january by clicking previous button
    driver.find_element_by_class_name('cal-prev').click()
for x in range(6):   
    #To keep going to the next month click next button 
    driver.find_element_by_class_name('cal-next').click()
    # Giving time for the dynamic calendar to load
    time.sleep(5)
    #Find all divs with hasEvent class
    divsHasEvent = driver.find_elements_by_class_name('hasEvent')
    #extracting dates and names of the events
    dates = [temp.get_attribute('aria-label') for temp in divsHasEvent]
    desc = [temp.find_element_by_tag_name('a').text for temp in divsHasEvent]
    for i in range(len(dates)):
        #classifying event type
        eventType = 'Concert'
        if 'toronto maple leafs' in desc[i].lower():
            eventType = 'Hockey' 
        elif 'toronto raptors' in desc[i].lower():
            eventType = 'Basketball'
        #appending to list in required format for the pandas dataframe
        scrapingData.append([datetime.strptime(dates[i], '%B %d %Y'),desc[i],eventType])

print(scrapingData)
#creating pandas dataframe
scotiabankevents = pandas.DataFrame(scrapingData, columns=['Date','Event Name', 'Event Type'])  
print(scotiabankevents)  

driver.quit()