import sqlite3
import asyncio
import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent


BASE_URL = "https://www.afisha.ru/msk/schedule_theatre/"
HEADERS = {"User-Agent": UserAgent().random}

items2 = []

conn = sqlite3.connect("events.db")
# # print(len(items2))
cursor = conn.cursor()

async def main():
    global items2
    k = 0
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=HEADERS) as response:
            r = await aiohttp.StreamReader.read(response.content)
            soup = BS(r, "html.parser")
            items1 = soup.find_all("a", {"class": "CjnHd y8A5E nbCNS yknrM"})
            items2 = soup.find_all("div", {"class": "S_wwn"})
            items3 = soup.find_all("div", {"class": "_JP4u"})
            items = []
            count = 0
            # for i in items1:
            #     count += 1
            for i in items1:
                for j in items2:
                    if j == items2[count]:
                        for k in items3:
                            if k == items3[count]:
                                if not (i.text, j.text, k.text) in items:
                                    args = (i.text, j.text, k.text)
                                    cursor.execute("INSERT INTO events VALUES (?, ?, ?)", args)
                                    conn.commit()
                                    items.append((i.text, j.text, k.text))
                count += 1


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
