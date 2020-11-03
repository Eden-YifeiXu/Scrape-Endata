import urllib.request
from bs4 import BeautifulSoup
import re
import pymysql

URLdict=dict()#set up a dictionary, arrange space

# 1.Connection Open
conn = pymysql.connect(user='root', password='123456', database='film',charset='utf8')
# 2.Cursor Creating:
cursor = conn.cursor()

#3
for i in range(3):
        response = urllib.request.urlopen('http://www.entgroup.cn/newslist/52-' + str(i) + '.html')
        HTMLText = response.read()

        BSobj = BeautifulSoup(HTMLText, "html.parser")  # analyze the page with beautiful soup
        for a in BSobj.findAll("a", href=True):  # sift all URL(s)
            if re.findall('/news/Exclusive/', a['href']):  # Get all URL(s) needed based on page features
                # print(a['href']) #Hyperlink
                # print(a.get_text()) #news title
                URLdict[a['href']] = a.get_text()  # Load into dictionary, keyed with Hyperlink and remove duplicates
for link,title in URLdict.items():
        print(title, ":", link) #get title, hyperlink and store them
        #substract hyperlink

        sqlstr = "select * from film_news where ORIGINAL_URL='http://www.entgroup.cn" + link + "'"
        cursor.execute(sqlstr)
        numrows= len(cursor.fetchall())
        if numrows > 0:
            continue;  # judge whether the URL exists, if exists, next run
        else:# judge whether the URL exists, if not, scrape and store into database
            ContentResponse = urllib.request.urlopen('http://www.entgroup.cn' + link)
            ContentHTMLText = ContentResponse.read()
            ContentBSobj = BeautifulSoup(ContentHTMLText, "html.parser")
            Content = ContentBSobj.find("div", {"class": "detailsbox"})  # get concrete contents and store them
            PublishDate = ContentBSobj.find("div", {"class": "detailsbox"}).find("div", {"class": "biaoqian"}).find({"i"})
            #print(Content.get_text())
            #print(PublishDate.get_text())
            sqlstr = "INSERT INTO FILM_NEWS(NEWS_TITLE,NEWS_CONTENT,ORIGINAL_URL,PUBLISH_DATE) VALUES('" +title.replace("'","’")+ "','" + Content.get_text().replace("'","’") +"',"+  "'http://www.entgroup.cn" + link + "','" + PublishDate.get_text() + "')"
            print(sqlstr)
            cursor.execute(sqlstr)
            conn.commit()
        with open('C:\xxx'+str(i)+'.txt', 'wb') as f:
            f.write(HTMLText)


