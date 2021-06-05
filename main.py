import requests
from bs4 import BeautifulSoup
import time
import sqlite3

base_url = "https://top.ge/page/"
count = 1
connection = sqlite3.connect("topsites.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS websites(
                    id INTEGER,
                    title TEXT,
                    category TEXT,
                    stats INTEGER,
                    description TEXT)
                    """)

for i in range(1,6):
     r = requests.get("https://top.ge/page/" + str(i))
     c = r.text

     soup = BeautifulSoup(c, "html.parser")
     tbody = soup.find("tbody")

     rows = tbody.find_all("tr")


     for item in rows:
          columns = item.find_all("td")

          links = columns[2].find_all("a")

          title = links[0].text
          category = links[1].text.strip()
          description = columns[4].text
          average_stats = columns[-4].find("span").text

          cursor.execute("insert into websites values(?, ?, ?, ?, ?)", (count,title,category,average_stats,description))
          count+= 1
     
     time.sleep(15)
    
connection.commit()
connection.close()