# twitteranalysis  

Python program for filtering "usable?!" twitter users with this criteria  
Last update don't ends with: months ago) or year ago) years ago)  
users average tweeting (from their account create till today) is less or equal to maxavgtw (see bellow for values)  
last 20 tweets fluctuates in fluctl20 or more days  
in last 20 tweets there are max maxRTinl20 RT and max maxIminl20 posted images and max maxMeinl20 mention tweets  
program is dependant on installed console twitter client https://github.com/sferik/t  
best as far as i know console twitter client publicly available  
also on installed elinks which is used for scraping link for twitter profile photo  
for now it works on linux  
inputfile should be text file with usernames separated by newlines  
for example in terminal with t followings @someusername > input or  
t followers @someusername > input you can create that file for analysis  
and catching usable?! personalities  
Program creates html file for ->further investigating, for following or adding in some of your list new personalities  