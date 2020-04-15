#!/usr/bin/env python
# coding: utf-8





import requests, re
from bs4 import BeautifulSoup
from collections import Counter
import statistics as stats
import string

class TextAnalyzer:
   
    def __init__(self, src, src_type = 'discover'):
        
        if src_type is 'discover':

            url = re.compile('^http.*$')
            path = re.compile('^.*\.txt$')
            '''The url and path variables represent the regex patterns used
            to search the src and determine src_type'''



            url_test = url.search(src)
            path_test = path.search(src)
            "use previously mentioned patterns to actually search the source"

            if url_test:
                src_type = 'url'
                is_url = True
            elif path_test:
                src_type = 'path'
                is_path = True  
            else:
                src_type = 'text'
                is_text = True
                """after the two tests are run, which ever test returns true will set the src_type 
                 and then creates a boolean based off the src_type to be used in later code if necessary"""   

        elif src_type.lower() == 'url':
            src_type = 'url'
            #is_url = True

        elif src_type.lower() == 'path':
            src_type = 'path'
            is_path = True

        elif src_type.lower() == 'text':
            src_type = 'text'
            is_text = True

        else:
            print('''Please enter a valid source type(url, path, or text) as the second parameter. 
                        If that does not work, the source may not be the correct type.''')
            sys.exit()
            
        #print('The source is:', src)
        #print('Source Type:', src_type)
        
        
        
        
        if src_type is 'url':
            r = requests.get(src)
            content = str(r.text)
        if src_type is 'path':
            with open(src) as p:
                content = p.read()
        if src_type is 'text':
            content = src
            

        self._src_type = src_type
        self._content = content
        self._orig_content = content
        '''Orig Content and Content point to the same thing, but orig content will not be changed, so if the
        content is changed for whatever reason, it can still be reset to the original content'''

        

   
    def set_content_to_tag(self, tag, tag_id=None):
        try:
            soup_spoon = BeautifulSoup(self._orig_content)
            div = soup_spoon.find(tag, id = tag_id)
            self._content = ''.join(map(str, div.contents))
        except:
            print('That tag and tag id do not exist as a pair')
        ''' Uses html tag and tag id to find a body of text and set to the _content variable'''
   
    def reset_content(self):
        self._content = self._orig_content
        #return self._content
        ''' uses orig content to restore content to its original value'''
   
    def _words(self, casesensitive=False):
        if casesensitive is False:
            test = str(_content).replace('</p><p>', ' ').replace('—', ' ').upper()
        else:
            test = str(_content).replace('</p><p>', ' ').replace('—', ' ')
        words = [word.strip(string.punctuation) for word in words]
        
        _words = words
   '''splits and strips punctuation from all of the words in content, creating a list of each individual word'''
    
    def common_words(self, minlen=1, maxlen=100, count=10, casesensitive=False):
        word_ls = self._content.strip(string.punctuation).split()
        
        if casesensitive is False:
            sized = [word.upper() for word in word_ls if len(word) >= minlen and len(word)<= maxlen ]
            
        else:
            sized = [word for word in word_ls if len(word) >= minlen and len(word)<= maxlen ]
            
        most_comm = Counter(sized).most_common(count)    
        return most_comm
   '''creates a list of the most common words. the minlen and maxlen parameters determine the length of each 
   word to be considered for the list, and the count parameter determines how many words to include in the new list'''

    def char_distribution(self, casesensitive=False, letters_only=False):
        leto = re.compile('[A-Za-z]')
        word_x = self._content.replace(' ','')
        
        if letters_only is False:
            word_pool = word_x
        if letters_only is True:
            word_pool = leto.findall(word_x)
        
        if casesensitive is False:
            char_pool =  [char.upper() for char in word_pool]
        else:
            char_pool =  [char for char in word_pool]
        
        
        c = Counter(char_pool)
        ord_dist = c.most_common(len(char_pool))
        
        return(ord_dist)
   '''counts the number of occurences of each character, if casesensitive is false it then "A" and "a" would be 
   considered the same, if letters only is false then numbers and punctuation are also counted as characters'''
   
    def plot_common_words(self, minlen=1, maxlen=100, count=10, casesensitive=False):
        word_ls = self._content.strip(string.punctuation).split()
        
        if casesensitive is False:
            sized = [word.upper() for word in word_ls if len(word) >= minlen and len(word)<= maxlen ]
        else:
            sized = [word for word in word_ls if len(word) >= minlen and len(word)<= maxlen ]
        most_comm = Counter(sized).most_common(count)    
        #return most_comm
    
        wf = pd.DataFrame(most_comm, columns =['Word', 'Frequency']) 
        wf.set_index('Word', inplace=True)
        #print(wf)

        word_plot = wf.plot(kind='bar',
                       title='Word Frequency',
                       figsize = (12,6),
                        width= .8,
                        fontsize=10)

        word_plot.set_ylabel('# of Uses', fontsize=20)
        word_plot.set_xlabel('Word', fontsize=20)
   '''This plots the common words, taking the same parameters as the common_words function above. It also uses a bit
   of the same code'''
   
   
    def plot_char_distribution(self, casesensitive=False, letters_only=False):
        leto = re.compile('[A-Za-z]')
        word_x = self._content.replace(' ','')
        
        if letters_only is False:
            word_pool = word_x
        if letters_only is True:
            word_pool = leto.findall(word_x)
        
        if casesensitive is False:
            char_pool =  [char.upper() for char in word_pool]
        else:
            char_pool =  [char for char in word_pool]
        
        
        c = Counter(char_pool)
        ord_dist = c.most_common(len(char_pool))
            
        cf = pd.DataFrame(ord_dist, columns =['Character', 'Frequency']) 
        cf.set_index('Character', inplace=True)
        #print(cf) 
        
        char_plot = cf.plot(kind='bar',
                   title='Character Frequency',
                   figsize = (12,6),
                    width= .8,
                    fontsize=12)

        char_plot.set_ylabel('Frequency', fontsize=20)
        char_plot.set_xlabel('Character', fontsize=20)
    '''This plots the distribution of each character, taking the same parameters as the char_distribution function above. 
    It also uses a bit of the same code'''
    
    @property
    def avg_word_length(self):
        word_list = self._content.split()
        new_list = [word.strip(string.punctuation).upper() for word in word_list]
        len_words = [len(word) for word in new_list]
        avg = sum(len_words)/len(len_words)
        avg_word_length = float("{:.2f}".format(avg))
        return avg_word_length
   '''returns the average word length of the content as a float, to the hundreths place'''
       
    
    @property
    def word_count(self):
        word_count = len(str(self._content).split())
        return word_count
   '''counts the words in _content'''
    
    @property
    def distinct_word_count(self):
        distinct_words = []
        
        
        word_s = str(self._content).upper().split()
        strp_word = [word.strip(string.punctuation) for word in word_s]
        count_words = Counter(strp_word)
        counts = count_words.items()
        '''^^turns counter into list of tuples'''
        
        
        for word in counts:
            if word[1] == 1:
                distinct_words.append(word)
        #return len(distinct_words)
        return len(counts)
      '''returns the number of words that only appear once in the content'''
              
    #original
    @property
    def words(self):
        word_con = str(self._content).replace('</p><p>', ' ').replace('—', ' ')
        
        if casesensitive is False:
            word_case = word_con.upper()
        else:
            word_case = word_con
        
        word_list = word_case.split()
        words = [word.strip(string.punctuation) for word in word_list]
        
        self._words = words
    
    #original
    @property
    def positivity(self):
        tally = 0
        with open ('positive.txt') as p:
              pos = p.read().split()
        with open ('negative.txt') as n:
              neg = n.read().split()
         
        word_list = self._content.upper().strip(string.punctuation).split()

        
        for word in word_list:
            if word in pos:
                tally += 1
            if word in neg:
                tally -= 1
        #print(tally)
        score = round( tally / self.word_count * 1000)
        return score
'''compares words in content to a list of words in a separate file, when a word from content matches a word in positive.txt
the positivity tally in incremented by one, when a word matches another in negative.txt the tally is decremented. score
is computed at the end'''

# ## Tests
'''Tests to make sure that all of the above code worked properly'''


import unittest

url = 'https://www.webucator.com/how-to/address-by-bill-clinton-1997.cfm'
path = 'pride-and-prejudice.txt'
text = '''The outlook wasn't brilliant for the Mudville Nine that day;
the score stood four to two, with but one inning more to play.
And then when Cooney died at first, and Barrows did the same,
a sickly silence fell upon the patrons of the game.'''

class TestTextAnalyzer(unittest.TestCase):
    def test_discover_url(self):
        ta = TextAnalyzer(url)
        self.assertEqual(ta._src_type, 'url')
    def test_discover_path(self):
        ta = TextAnalyzer(path)
        self.assertEqual(ta._src_type, 'path')
    def test_discover_text(self):
        ta = TextAnalyzer(text)
        self.assertEqual(ta._src_type, 'text')
    def test_set_content_to_tag(self):
        ta = TextAnalyzer(url)
        ta.set_content_to_tag('div','content-main')
        self.assertEqual(ta._content[0:25], '\n\nAddress by Bill Clinton')
    def test_reset_content(self):
        ta = TextAnalyzer(url)
        ta.set_content_to_tag('div','content-main')
        ta.reset_content()
        self.assertEqual(ta._content[0], '<')
    def test_common_words(self):
        ta = TextAnalyzer(path, src_type='path')
        common_words = ta.common_words(minlen=5, maxlen=10)
        liz = common_words[0]
        self.assertEqual(liz[0],'ELIZABETH')
    def test_avg_word_length(self):
        ta = TextAnalyzer(text, src_type='text')
        self.assertEqual(ta.avg_word_length, 4.16)
    def test_word_count(self):
        ta = TextAnalyzer(text, src_type='text')
        self.assertEqual(ta.word_count, 45)
    def test_distinct_word_count(self):
        ta = TextAnalyzer(text, src_type='text')
        self.assertEqual(ta.distinct_word_count, 38)
    def test_char_distribution(self):
        ta = TextAnalyzer(text, src_type='text')
        char_dist = ta.char_distribution(letters_only=True)
        self.assertEqual(char_dist[1][1], 20)
    def test_positivity(self):
        ta = TextAnalyzer(text, src_type='text')
        positivity = ta.positivity
        self.assertEqual(positivity, -44)
    

    
suite = unittest.TestLoader().loadTestsFromTestCase(TestTextAnalyzer)
unittest.TextTestRunner().run(suite)


# ## Plots



get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)

ta = TextAnalyzer('pride-and-prejudice.txt', src_type='path')
ta.plot_common_words(minlen=5)
ta.plot_char_distribution(letters_only=True)


