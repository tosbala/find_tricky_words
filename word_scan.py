import re
import sys, getopt

from PyDictionary import PyDictionary
import pytesseract
import requests

   
def extract_words(image_file):
    text = pytesseract.image_to_string(image_file)
    word_list = re.sub("[^\w]", " ",  text).lower().split()
    return word_list


def find_uncommon_words(word_list):
    if not word_list:
        return

    common_words_resource = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt'
    response = requests.get(common_words_resource)
    if response.status_code != 200:
        print('unable to fetch common english words')
        return 

    common_words = response.text
    return set(word_list).difference(common_words.split('\n'))


def scan_and_list_meanings(input_image):
    uncommon_words = find_uncommon_words(extract_words(input_image))
    dictionary = PyDictionary()
    for word in uncommon_words:
        meaning = dictionary.meaning(word, disable_errors=True)
        if meaning:
            print('{word}: {meaning}\n'.format(word=word, meaning=meaning))


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi:",["image="])
    except getopt.GetoptError:
        print ('word_scan.py -i <input_image>')
        sys.exit(2)

    input_image = ''
    for opt, arg in opts:
        if opt == '-h':
            print ('word_scan.py -i <input_image>')
            sys.exit()
        elif opt in ("-i", "--image"):
            input_image = arg

    if input_image:
        scan_and_list_meanings(input_image)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print ('word_scan.py -i <input_image>')
