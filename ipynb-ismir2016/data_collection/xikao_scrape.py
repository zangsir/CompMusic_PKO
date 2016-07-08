#this script will scrape all listed jingju play libretto from webpages on xikao.com and extract to text files with html tags removed.

import urllib, htmllib, formatter, re, sys
from bs4 import BeautifulSoup

url = "http://scripts.xikao.com/list/comprehensive"
url_top = "http://scripts.xikao.com"
website = urllib.urlopen(url)
data = website.read()
website.close()
format = formatter.AbstractFormatter(formatter.NullWriter())
ptext = htmllib.HTMLParser(format)
ptext.feed(data)
links = ptext.anchorlist
#remove duplicate urls
uniq_links=list(set(links))

#compile the regex used in finding the titles of the html page
regex='<title>(.+?)</title>'
pattern=re.compile(regex,re.DOTALL)

errorlinks=[]

#we want text section between <div id="article"> ( ) <div id="footer">
print 'links on this page:',links
for link in uniq_links:
    #each 'link' contains one play
    link_comp = urlparse.urljoin(url_top,link)
    #only process those links from the parent page that has 'play' in the url, these correspond to the individual scripts
    if re.search('play',link_comp)!=None:
        print(link_comp)
        website = urllib.urlopen(link_comp)
        data = website.read() 
        website.close()
        #the individual play page html file should be stored in the data
        
        #find the title of the page, and using it to name the file of this play
        titles=re.findall(pattern,data)[0]
        titles_clean=re.sub('\r\n','',titles)
        titles_clean=titles_clean.replace(" ","")
        print titles_clean
        newfile=titles_clean + '.txt'
        
        #get into the relevant section with only lyrics
        try:
            soup = BeautifulSoup(data)
            target=soup.find("div", id="article")
            #print target.text will give you clean text without html tags
            f = open(newfile, 'w')
            f.write(target.text.encode('utf_8'))
        except:
            print "error while processing this link"
            errorlinks.append(link_comp)
            
print "links not processed:"
print errorlinks
            