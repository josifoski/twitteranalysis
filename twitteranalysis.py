#!/usr/bin/env python3.5
# created by about.me/josifsk 2015-december

# Program for filtering "usable?!" twitter users with this criteria
# Last update don't ends with: months ago) or year ago) years ago)
# users average tweeting (from their account create till today) is less or equal to maxavgtw (see bellow for values)
# last 20 tweets fluctuates in fluctl20 or more days
# in last 20 tweets there are max maxRTinl20 RT and max maxIminl20 posted images and max maxMeinl20 mention tweets
# program is dependant on installed console twitter client https://github.com/sferik/t
# also on installed elinks which is used for scraping link for twitter profile photo
# for now it works on linux, in future we shall see
# inputfile should be text file with usernames separated by newlines
# for example in terminal with t followings @someusername > input or t followers @someusername > input you can create that file for analysis
# and catching usable?! personalities
# Program creates html file for ->further investigating, for following or adding in some of your list new personalities

import os
import sys
import re
import datetime
import time
import codecs

years = ('2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015' )
dmonths = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
lastupdatereject = ('months ago', 'year ago', 'years ago')

#INPUT##########################################################
inputfile = 'input03'
passingfile = 'passing03.html'
maxavgtw = 3
fluctl20 = 6
maxRTinl20 = 5
maxMeinl20 = 7
maxIminl20 = 5
# feel free to change criteria numbers acording your criteriaa
################################################################

os.system("comm -23 <(sort %s) <(sort processed) | sort -r > temp && mv temp %s" % (inputfile, inputfile))
enddate = time.strftime("%Y-%m-%d")
f = open(inputfile,'r')
g = codecs.open(passingfile, 'w', 'utf-8')
g.write('<!DOCTYPE html>\n')
g.write('<html>\n')
g.write('<head>\n')
g.write('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n')
g.write('</head>\n')
g.write('<body>\n')
#g.write('$$$ ' + passingfile + '\n')
time1=time.time()

def dayofyear(stringdate):
    return datetime.datetime.strptime(stringdate, "%Y-%m-%d").timetuple().tm_yday

def strip_nasty_characters(input):
    if input:
        try:
            # Wide UCS-4 build
            myre = re.compile(u'['
                u'\U0001F300-\U0001F64F'
                u'\U0001F680-\U0001F6FF'
                u'\u2600-\u26FF\u2700-\u27BF]+',
                re.UNICODE)
        except re.error:
            # Narrow UCS-2 build
            myre = re.compile(u'('
                u'\ud83c[\udf00-\udfff]|'
                u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                u'[\u2600-\u26FF\u2700-\u27BF])+',
                re.UNICODE)
        input = re.sub(myre, "", input)
    return input

counter = 0
filtered = 0

for user in f:
    counter += 1

    user = user.strip()
    i = 0

    while True:
        try:
            os.system('t whois %s > temp' % user)
            ft = open('temp', 'r')
            lft = ft.readlines()
            if len(lft) > 1:
                if (lft[2].split()[0] == 'Last') and not (' '.join(lft[2].split()[-2:]).strip(')') in lastupdatereject):
                    Allowed = True
                    if lft[4].split()[0] == 'Screen':
                        lft[2] = lft[2].strip() + ' ' + lft[3].strip()
                        del lft[3]                        
                else:
                    Allowed = False
                    #print('r ' + lft[3].split()[2].strip('@'), ' '.join(lft[2].split()[-2:]).strip(')'))
            else:
                Allowed = False
            break
        except:
            print('*** sleeping 2 minutes to avoid twitter rate overflow ***')
            Allowed = False
            time.sleep(120)
    
    if Allowed:
        for line in lft:
            line = line.strip()
            line = strip_nasty_characters(line)
            i += 1
            if i == 2:
                l = line.split()
                month = l[1]
                day = l[2]
                if l[3] in years:
                    year = l[3]
                else:
                    year = '2015' ###### check

            if i == 4:
                screenname = line.split()[2].strip('@')
                #print(str(counter) + '  processing.. ' + screenname)
            if i == 6:
                numoftweets = int(line.split()[1].replace(',',''))

                startdate = year + '-' + str(dmonths[month]) + '-' + day

                firstday = dayofyear(startdate)
                lastday = dayofyear(enddate)

                if lastday > firstday:
                    numofdays = (int(enddate[:4]) - int(startdate[:4]))*365 + lastday - firstday
                else:
                    numofdays = (int(enddate[:4]) - int(startdate[:4]) - 1)*365 + 365 - firstday + lastday

                averagetweets = float(numoftweets/numofdays)

                
        if averagetweets <= maxavgtw:
            os.system("t timeline -l -r -n 20 %s --decode-uris | sed -r 's/^.{20}//' > temp" % screenname)
            f2 = codecs.open('temp', 'r', 'utf-8')
            lf2 = f2.readlines()
            f2.close()
            try:
                imonth = dmonths[lf2[0].split()[0]]
                idate = lf2[0].split()[1]
            except:
                imonth = 12 ##### check
                idate = 1
            
            parse1date = enddate[:4] + '-' + str(imonth) + '-' + str(idate)
            if dayofyear(enddate) - dayofyear(parse1date) >= fluctl20:
                numofRT = 0
                numofImages = 0
                numofMent = 0
                for item in lf2:
                    try:
                        if item.split()[4] == 'RT':
                            numofRT += 1
                        else:
                            if item.split()[4].strip()[0] == '@':
                                numofMent += 1    
                        if '//t.co/' in item:
                            numofImages += 1
                    except:
                        pass
                        #print(item)
                
                if ( numofRT <= maxRTinl20 ) and ( numofImages <= maxIminl20 ) and (numofMent <= maxMeinl20 ):
                    print(str(counter))
                    #print(str(counter), lft[3].split()[2].strip('@'))

                    os.system("elinks -dump twitter.com/%s | grep ' 99\. ' | sed 's/^.\{6\}//' > temp" % screenname)
                    fimage = open('temp', 'r')
                    simage = fimage.read()
                    fimage.close()
                    g.write("<img src=%s width='200' height='200'></br>\n" % simage.strip())
                    g.write('@' + screenname + '</br>\n')
                    
                    for line in lft:
                        g.write(line.strip() + '</br>\n')
                    g.write('<pre>\n')
                    g.write('Average number of tweets (from start)         ' + '%.1f' % averagetweets  + '</br>\n')
                    g.write('Number of RT in last 20 tweets                ' + str(numofRT) + '</br>\n')
                    g.write('Number of images in last 20 tweets            ' + str(numofImages) + '</br>\n')
                    g.write('Number of mentions in last 20 tweets          ' + str(numofMent) + '</br>\n')
                    g.write('</pre>\n')
                    g.write('</br>\n')
                    
                    for line in lf2:
                        line = line.strip()
                        lline = line.split()
                        del lline[2:4]
                        g.write(' '.join(lline) + '</br></br>\n')

                    filtered += 1
                    g.write('</br>\n')
                

    ft.close()
    
time2=time.time()
difftimeinmin = (time2-time1)/60.
print('From: ' + str(counter) + ' filtered: ' + str(filtered))
g.write('From: ' + str(counter) + ' filtered: ' + str(filtered) + '</br>\n')
g.write('</body>\n')
g.write('</html>\n')
print("%.2f minutes" % difftimeinmin)
os.system('cat %s >> processed' % inputfile)
os.system('sort %s | uniq > temp && mv temp processed' % 'processed')
f.close()
g.close()
os.system('mpv /home/mlovely/phonering.wav')
print('Done.')
