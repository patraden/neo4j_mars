import csv
import sys
sys.path.append('/app/text_to_speech/')
with open('/app/text_to_speech/google_translate_words.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        print(', '.join(row))
