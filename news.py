from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import json
from datetime import datetime

web = 'https://timesofindia.indiatimes.com/mostcommentedsec/msid-8236896.cms'
path = '~/Music/chromedriver_linux64'  # introduce path here ,enter your own  chrome driver path here 

now = datetime.now()
month_day_year = now.strftime("%m-%d-%Y")

# add headless mode
options = Options()
options.add_argument('--headless')
driver_service = Service(executable_path=path)
driver = webdriver.Chrome(service=driver_service, options=options)
driver.get(web)

headlines = driver.find_elements(by='xpath',value="//ul[@class='content']/li/a")
titles = []
links = []
details = []
for news in headlines:
    titles.append(news.text)
    links.append(news.get_attribute('href'))
a = 0
print(links[12])
for link in links :
    driver.get(link)
    try :
       article = driver.find_element(by='xpath',value="//div[@class='_s30J clearfix  ']") 
       details.append(article.text)
    except NoSuchElementException: 
        details.append("needed TOI subscription") 
        pass  

my_dict = {'title': titles, 'link': links , 'Details' : details}
df = pd.DataFrame(my_dict)
json_str = df.to_json(orient='records')
parsed = json.loads(json_str)
with open(f'Headlines_{month_day_year}.json', 'w') as json_file:
    json_file.write(json.dumps({"data": parsed}, indent=4 ))

driver.quit()
