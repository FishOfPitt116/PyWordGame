import csv
from path import get_root_path

file = open(get_root_path() + '/words/words.csv')

reader = csv.reader(file)

words = []

for word in reader:
    words.append(word[0])