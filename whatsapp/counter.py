rev_dates = open('rev_dates.csv', 'r')
rev_count = open('rev_count.csv','w')
y = rev_dates.readline()
y = rev_dates.read()
from collections import Counter
counter =  Counter(y.split('\n'))

for item, value in counter:
  rev_count.write(count + ' ' + value + '\n')

soha_dates = open('soha_dates.csv', 'r')
