#!/usr/bin/env python3.5

# Python program for filtering twitter profiles with this criteria  
# Last update don't ends with: month ago) or months ago) or year ago) years ago)  
# User tweeted at least 15 tweets  
# users average tweeting (from their account create till today) is less or equal to maxavgtw (see bellow in program for values)  
# last 20 tweets fluctuates in fluctl20 or more days  
# in last 20 tweets there are max maxRTinl20 RT and max maxLinksl20 links and max maxMeinl20 mention tweets  
# program is dependant on installed console twitter client https://github.com/sferik/t  
# best as far as i know console twitter client publicly available  
# also on installed elinks which is used for scraping link for twitter profile photo  
# for now it works on linux  
# inputfile should be text file with usernames separated by newlines  
# for example in terminal with t followings @someusername > input or  
# t followers @someusername > input you can create that file for analysis  
# and catch personalities according your criteria  
# program creates html file for ->further investigating, for following or adding in some of your list new personalities  
  
# created by Josifoski Aleksandar 2015-december  

import os
import sys
import re
import datetime
import time
import codecs

years = ('2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015' )
dmonths = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
lastupdatereject = ('month ago', 'months ago', 'year ago', 'years ago')

#INPUT#################################################################################################################################
inputfile = 'input'
passingfile = 'output.html'
notpassingfile = 'notpassing'
maxavgtw = 7      # users average tweeting (from their account create till today) is less or equal to x
fluctl20 = 5      # fluctuation of last 20 tweets is x or more days
maxRTinl20 = 7    # in last 20 tweets there are max x RT
maxMeinl20 = 8    # in last 20 tweets there are max x mentions, mention tweet starts with @, if @ is on other place is regular one
maxLinksl20 = 15  # in last 20 tweets there are max x links
# feel free to change numbers according your criteria
#######################################################################################################################################
print('processing ' + inputfile + '...')
os.system('bash -c "comm -23 <(sort %s) <(sort processed) > temp && mv temp %s"' % (inputfile, 'newprofiles'))
with open('newprofiles') as f:
    newpl = len(f.readlines())
print(str(newpl) + ' new profiles')
enddate = time.strftime("%Y-%m-%d")
f = open('newprofiles','r')
g = codecs.open(passingfile, 'w', 'utf-8')
n = open(notpassingfile, 'w')
n.write('#######################################################################################################################################\n')
n.write('maxavgtw = ' + str(maxavgtw) + '     # users average tweeting (from their account create till today) is less or equal to x\n')
n.write('fluctl20 = ' + str(fluctl20) + '     # fluctuation of last 20 tweets is x or more days\n')
n.write('maxRTinl20 = ' + str(maxRTinl20) + '   # in last 20 tweets there are max x RT\n')
n.write('maxMeinl20 = ' + str(maxMeinl20) + '   # in last 20 tweets there are max x mentions, mention tweet starts with @, if @ is on other place is regular one\n')
n.write('maxLinksl20 = ' + str(maxLinksl20) + ' # in last 20 tweets there are max x links\n')
n.write('#######################################################################################################################################\n')

g.write('<!DOCTYPE html>\n')
g.write('<html>\n')
g.write('<head>\n')
g.write('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n')
g.write('</head>\n')
g.write('<body>\n')

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
            if ( len(lft) > 1 ) and (not '/usr/bin/t' in lft[0].split()[0]):
                if (lft[2].split()[0] == 'Last') and not (' '.join(lft[2].split()[-2:]).strip(')') in lastupdatereject):
                    Allowed = True
                    if lft[4].split()[0] == 'Screen':
                        lft[2] = lft[2].strip() + ' ' + lft[3].strip()
                        del lft[3]                        
                else:
                    Allowed = False
                    n.write(user + ' - tweets are protected or last tweet was long ago\n')
                break             
            else:
                print(lft)
                print('*** sleeping 2 minutes to avoid twitter rate overflow ***')
                Allowed = False
                time.sleep(120)
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
                    year = enddate[:4]

            if i == 4:
                try:
                    screenname = line.split()[2].strip('@')
                except:
                    pass
            if i == 6:
                try:
                    numoftweets = int(line.split()[1].replace(',',''))
                    startdate = year + '-' + str(dmonths[month]) + '-' + day
                    firstday = dayofyear(startdate)
                    lastday = dayofyear(enddate)

                    if lastday > firstday:
                        numofdays = (int(enddate[:4]) - int(startdate[:4]))*365 + lastday - firstday
                    else:
                        numofdays = (int(enddate[:4]) - int(startdate[:4]) - 1)*365 + 365 - firstday + lastday

                    averagetweets = float(numoftweets/numofdays)
                except:
                    averagetweets = 0
            
        if averagetweets <= maxavgtw:
            os.system("t timeline -l -r -n 20 %s --decode-uris | sed -r 's/^.{20}//' > temp" % screenname)
            f2 = codecs.open('temp', 'r', 'utf-8')
            lf2 = f2.readlines()
            f2.close()
            try:
                imonth = dmonths[lf2[0].split()[0]]
                idate = lf2[0].split()[1]
            except:
                imonth = enddate[5:7].strip('-')
                idate = 1
            
            parse1date = enddate[:4] + '-' + str(imonth) + '-' + str(idate)
            if (dayofyear(enddate) - dayofyear(parse1date) + 1 ) >= fluctl20:
                numofRT = 0
                numofLinks = 0
                numofMent = 0
                for item in lf2:
                    try:
                        if item.split()[4] == 'RT':
                            numofRT += 1
                        else:
                            if item.split()[4].strip()[0] == '@':
                                numofMent += 1    
                        if 'http' in item:
                            numofLinks += 1
                    except:
                        pass
                
                if ( numofRT <= maxRTinl20 ) and ( numofLinks <= maxLinksl20 ) and (numofMent <= maxMeinl20 ) and (len(lf2) >= 15):
                    print(str(counter))
                    os.system("elinks -dump twitter.com/%s | grep ' 99\. ' | sed 's/^.\{6\}//' > temp" % screenname)
                    fimage = open('temp', 'r')
                    simage = fimage.read()
                    fimage.close()
                    g.write("<img src=%s width='200' height='200'></br>\n" % simage.strip())
                    g.write('@' + screenname + '</br>\n')
                    
                    for line in lft:
                        g.write(strip_nasty_characters(line).strip() + '</br>\n')
                    g.write('<pre>\n')
                    g.write('Average number of tweets (from start)         ' + '%.1f' % averagetweets  + '</br>\n')
                    g.write('Number of RT in last 20 tweets                ' + str(numofRT) + '</br>\n')
                    g.write('Number of mentions in last 20 tweets          ' + str(numofMent) + '</br>\n')
                    g.write('Number of links in last 20 tweets             ' + str(numofLinks) + '</br>\n')
                    
                    g.write('</pre>\n')
                    g.write('</br>\n')
                    
                    for line in lf2:
                        line = line.strip()
                        line = strip_nasty_characters(line)
                        line = re.sub('< *iframe', '', line, flags=re.UNICODE)
                        lline = line.split()
                        del lline[2:4]
                        g.write(' '.join(lline) + '</br></br>\n')

                    filtered += 1
                    g.write('</br>\n')
                else:
                    why = user + ' - '
                    if numofRT > maxRTinl20:
                        why += 'number of RT: ' + str(numofRT) + '; '
                    if numofLinks > maxLinksl20:
                        why += 'number of links: ' + str(numofLinks) + '; '
                    if numofMent > maxMeinl20:
                        why += 'number of mentions: ' + str(numofMent) + '; '
                    if len(lf2) < 15:
                        why += ' only: ' + str(len(lf2)) + ' tweets from creating account.'
                    n.write(why + '\n')
            else:
                if ( dayofyear(enddate) - dayofyear(parse1date) + 1 ) == 1:
                    n.write(user + ' - fluctuation of last 20 tweets is condensed in ' + str(dayofyear(enddate) - dayofyear(parse1date) + 1) + ' day, possible + other criteria\n')
                else:
                    n.write(user + ' - fluctuation of last 20 tweets is condensed in ' + str(dayofyear(enddate) - dayofyear(parse1date) + 1) + ' days, possible + other criteria\n')
                
        else:
            n.write(user + ' - average tweets = ' + '%.1f' % averagetweets + ' + possible other criteria\n')
    ft.close()
    
time2=time.time()
difftimeinmin = (time2-time1)/60.
print('From: ' + str(counter) + ' filtered: ' + str(filtered))
g.write('From: ' + str(counter) + ' filtered: ' + str(filtered) + '</br>\n')
g.write('</body>\n')
g.write('</html>\n')
print("%.2f minutes" % difftimeinmin)
os.system('cat %s >> processed' % 'newprofiles')
f.close()
g.close()
n.close()
if os.path.isfile('temp'):
    os.remove('temp')
os.system('mpv /home/mlovely/phonering.wav') # here if you want sound alarm when program finish, chose some console player for your system
                                             # and apropriate melody with full path
print('Done.')
