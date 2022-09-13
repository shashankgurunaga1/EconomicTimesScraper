from bs4 import BeautifulSoup # bs4 library 
import lxml # lxml is the file parsor which allows web scraping
import requests # requests  module contains   functions such as get,content  that allow the user to access  the url and get the content in binary format
import pandas as pd

html_text = requests.get('https://economictimes.indiatimes.com/').text # we are fetching 
soup = BeautifulSoup(html_text,'lxml') # soup object is created which parses through the url
newslist=soup.find_all('ul',class_="newsList")


d=dict()
titles=[]
links=[]
texts=[]


for news in newslist: 
    #traverse through each list item
    listitems=news.find_all('li')

    for listitem in listitems:
        if listitem.find('a'):
            title=''
            link=''
            text=''

            #get news title
            if (listitem.a.text!=None):
                title= listitem.a.text            
        
        
            #get    news link 
            if(listitem.a['href']!=None):
        
                link="https://economictimes.indiatimes.com/"+listitem.a['href'] # We are creating this to go to the news article  webpage                 

                html_text1 = requests.get(link).text #Using the above link generated we are now creating another object which allows us to access the url
                soup1 = BeautifulSoup(html_text1,'lxml')
                body1=soup1.find_all('div',{"class": ["artText","medium"]}, limit=1)
                for k in body1:
                    text=k.text
        
        # add data in each list representing each column in xls
                   
        titles.append(title)
        texts.append(text)
        links.append(link)

    # add the list in the dictionary
        
    d['Title']=titles
    d['Text']=texts
    d['Link']=links
#print(d)
# # saving the data in demo.xls
df = pd.DataFrame(d)
writer = pd.ExcelWriter('news_data.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()
