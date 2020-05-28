#! python 3
# synonyms.py - Automated search dictionary
# and find out synonyms and pronunciation.

from selenium import webdriver
from nltk.corpus import wordnet as wn
import pyperclip, time
import logging
import requests
import bs4

logging.disable(logging.DEBUG)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_data():
    print("Ready - Use cltr + C or copy to get key word")
    words = {}
    pyperclip.copy('')
    try:
        while True:
            word = pyperclip.paste()
            if word and word not in words:
                morphy_word = wn.morphy(word.strip())
                word = morphy_word if morphy_word else word
                words[word] = None
                logging.debug(f'Insert {word} to dictionary')
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    return words

def main():
    words = get_data()
    print('Start searching............')
    browser = webdriver.Firefox()
    browser.get('https://translate.google.com')
    search = browser.find_element_by_id('source')
    time.sleep(1)

    # Search word.
    for word in words:
        # Search synonyms with Google Translate
        search.send_keys(word)
        time.sleep(1.5)
        synonyms = browser.find_elements_by_class_name('gt-cd-cl')
        synonyms = {syn.text for syn in synonyms if syn.text != ''}
        synonyms = ', '.join(synonyms) if synonyms else 'NOT FOUND'
        search.clear()

        # Get pronunciation from LDOMAN
        ldoman = requests.get(f'https://www.ldoceonline.com/dictionary/{word}')
        try:
            ldoman = bs4.BeautifulSoup(ldoman.text)
            pronun = ldoman.select_one('.PRON').text
        except (TypeError, AttributeError):
            pronun = 'NOT FOUND'
        # Save data
        words[word] = (pronun, synonyms)

    
    # Close browser
    browser.quit()
    
    print("Synonyms:")
    for word, value in words.items():
        print(word.capitalize() + ' - /{0}/ : {1}'.format(*value))
        print('****************************************************')


if __name__ == "__main__":
    main()
