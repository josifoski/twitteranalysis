# twitteranalysis  
  
Python program for filtering twitter profiles with this criteria  
Last update don't ends with: months ago) or year ago) years ago)  
User tweeted at least 15 tweets  
users average tweeting (from their account create till today) is less or equal to maxavgtw (see bellow in program for values)  
last 20 tweets fluctuates in fluctl20 or more days  
in last 20 tweets there are max maxRTinl20 RT and max maxLinksl20 links and max maxMeinl20 mention tweets  
program is dependant on installed console twitter client https://github.com/sferik/t  
best as far as i know console twitter client publicly available  
also on installed elinks which is used for scraping link for twitter profile photo  
for now it works on linux  
inputfile should be text file with usernames separated by newlines  
for example in terminal with t followings @someusername > input or  
t followers @someusername > input you can create that file for analysis  
and catch personalities according your criteria  
program creates html file for ->further investigating, for following or adding in some of your list new personalities  
  
created by Josifoski Aleksandar 2015-december  

