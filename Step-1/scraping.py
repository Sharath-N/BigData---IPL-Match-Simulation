from bs4 import BeautifulSoup as soup
#from urllib.request import urlopen as uReq
import csv
import pandas as pd


bat_arr = [['Player', 'Span', 'Mat', 'Inns', 'NO', 'Runs', 'HS', 'Ave', 'BF', 'SR', '100', '50', '0', '4s', '6s']]
bowl_arr = [['Player', 'Span', 'Mat', 'Inns', 'Overs', 'Mdns', 'Runs', 'Wkts', 'BBI', 'Ave', 'Econ', 'SR', '4', '5', 'Ct', 'St']]

def duplicate(fn, res, row_arr):
    df = pd.DataFrame(row_arr)
    
    for dup in res:
        if((fn == 'batting.csv' and len(dup) != 15) or (fn == 'bowling.csv' and len(dup) != 16)) :
            dup.insert(1, '-')
        #print("g" not in df[0].values.tolist(), df[0].values.tolist()) #print dup[0] not in df[0].values.tolist()
        if(dup[0] not in df[0].values.tolist()):
    	    row_arr.append(dup)
    	    df = pd.DataFrame(row_arr) #print("dts0", str(dup[0]) not in df[0].values.tolist(), dup[0], df[0].values.tolist())
        else:
            print dup[0]
            for i in row_arr:
                if(dup[0] == i[0]):
                    if(fn == 'batting.csv'):
                        for c in [2, 3, 4, 5, 8, 10, 11, 12, 13, 14]:
                            i[c] = str(int(i[c]) + int(dup[c]))
                        i[7] = str((float(i[7]) + float(dup[7])) / 2)
                        i[9] = str((float(i[9]) + float(dup[9])) / 2)
                    if(fn == 'bowling.csv'):
                        for c in [2, 3, 5, 6, 7, 12, 13, 14, 15]:
                            i[c] = str(int(i[c]) + int(dup[c]))
                        i[4] = str(float(i[4]) + float(dup[4]))
                        i[9] = str((float(i[9]) + float(dup[9])) / 2)
                        i[10] = str((float(i[10]) + float(dup[10])) / 2)
                        i[11] = str((float(i[11]) + float(dup[11])) / 2)
                    df = pd.DataFrame(row_arr)

def scraper(lp, fn, row_arr):
    '''#Online
    uClient = uReq(lp)
    page = soup(uClient.read(), "html.parser")
    uClient.close()'''
    page = soup(open(lp, 'rb').read(), "html.parser") # Offline
    
    #print(page.prettify())
    rows=page.find_all('tr') #print(rows)
   
    res=[]
    l=[]
    for row in rows:
        cols=row.find_all('td')
        cols=[x.text.strip().replace('-', '0').encode('utf8') for x in cols]
        res.append(cols)

    for i in res:
        if len(i)<14:
            l.append(i)

    for i in l:
        res.remove(i)
    
    duplicate(fn, res, row_arr)

def writer(fn, row_arr):
    with open(fn, 'w') as myFile:
        writer = csv.writer(myFile)
        for r in row_arr:
            writer.writerow(r)
        myFile.close()


filename = 'batting.csv'
'''#Online
for u_link in ['4343', '4344', '4347', '4342', '5845', '4788', '4341', '4346', '4787', '4345', '5843', '4340', '5143']:
    my_on_url = 'http://stats.espncricinfo.com/indian-premier-league-2016/engine/records/averages/batting.html?id=117;team=' + u_link + ';type=trophy'
    scraper(my_on_url, filename)'''
for u_link in range(1, 14):
    my_off_url = '/home/sharath_n/Desktop/BigData/Project/WebPages/Batsmen/' + str(u_link) + '.html'
    scraper(my_off_url, filename, bat_arr)
writer(filename, bat_arr)

filename = 'bowling.csv'
'''for u_link in ['4343', '4344', '4347', '4342', '5845', '4788', '4341', '4346', '4787', '4345', '5843', '4340', '5143']:
    my_on_url = 'http://stats.espncricinfo.com/indian-premier-league-2016/engine/records/averages/bowling.html?id=117;team=' + u_link + ';type=trophy'
    scraper(my_on_url, filename)'''
for u_link in range(1, 14):
    my_off_url = '/home/sharath_n/Desktop/BigData/Project/WebPages/Bowler/' + str(u_link) + '.html'
    scraper(my_off_url, filename, bowl_arr)
writer(filename, bowl_arr)
