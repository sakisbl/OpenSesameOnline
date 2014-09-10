# -*- coding: ascii -*-
"""
#==============================================================================
#title           :os_generator.py
#description     :This class creates test strings for open sesame, and stores
                  them in text files for easy reference later
#author          :OpenSesame group of GipHouse 2014, Radboud University
#programmers     :Ben Bruecker, Laurens van Bercken
#date            :20140419
#version         :0.1
#usage           :python ../translator.py
#notes           :
#python_version  :2.7
#==============================================================================
"""
import random
import sys
import string
import os.path
import re

class TestStringGenerator(object):
    """ Testset creates a set of test variables that can be used to test
    open sesame online modules
    """

    # pylint: disable=too-few-public-methods
    LETTERS = string.letters
    DIGITS = string.digits
    NEWLINE = '\n'
    WHITESPACE = re.sub(NEWLINE, '', string.whitespace)
    PUNCTUATION = re.sub(r'"', '', string.punctuation)
    NAME_NOT_ALLOW = re.sub(r'[|]|\'|"', '', PUNCTUATION)
    TEXT_NOT_ALLOW = '[|]'

    # pylint: disable=too-few-public-methods
    def __init__(self, amount, max_l, file_mapping, force=False):
        """ Generates all types of possible os input strings.
        amount      -- The number of strings to generate
        max_l       -- Maximal string length
        mapping     -- Mapping of string types to filenames
                       MUST include: number, name, text AND their _inc variants
        force       -- If this is true, force generation of a new file
                       Default False. If there already is a dict, create no new
        """
        self.file_mapping = file_mapping
        self.max_l = max_l
        for key in self.file_mapping:
            self._generate_output_file(amount, force, key)

    def _check_file(self, s_type):
        """ This function checks whether a file as defined in the mapping of
        type s_type exists
        """
        return os.path.isfile(self.file_mapping[s_type])

    def _generate_output_file(self, amount, force, s_type):
        """ Write test string corresponding to s_type to a file defined in the
        file_mapping for s_type
        If force = true, force generation of a new file
        """
        # If it already exists, do not generate again, unless forced
        if self._check_file(s_type) and not force:
            return
        outfile = open(self.file_mapping[s_type], 'w')
        for _ in xrange(0, amount):
            outstring = self._get_string(s_type)
            re.sub(r'\n', r'\\n', outstring)
            outstring += '\n'
            outfile.write(outstring)
        outfile.close()

    def _get_string(self, s_type):
        """ Get a test string corresponding to the s_type """
        # pylint: disable=too-many-return-statements
        # Too many returns is disabled because this is basically a switch
        if s_type == 'number':
            return self._get_number(correct=True)
        elif s_type == 'number_inc':
            return self._get_number(correct=False)
        elif s_type == 'name':
            return self._get_name(correct=True)
        elif s_type == 'name_inc':
            return self._get_name(correct=False)
        elif s_type == 'text':
            return self._get_text(correct=True)
        elif s_type == 'text_inc':
            return self._get_text(correct=False)
        elif s_type == 'keyword':
            return self._get_keyword(correct=True)
        elif s_type == 'keyword_inc':
            return self._get_keyword(correct=False)
        elif s_type == 'condition':
            return self._get_condition(correct=True)
        elif s_type == 'condition_inc':
            return self._get_condition(correct=False)
        return ""

    def _get_number(self, correct):
        """ Gets a number test string.
        correct determines if a correct or incorrect string should be returned
        """
        random_value = random.sample([\
                random.randrange(-sys.maxint -1, sys.maxint),
                random.uniform(-sys.maxint-1, sys.maxint)], 1)
        random_value = str(random_value[0])
        if correct:
            return random_value
        else:
            possible_values = []
            possible_values.extend(
                    self._correct_quotes(random_value))
            possible_values.extend(
                    self._incorrect_quotes(random_value))
            possible_values.append(self._get_text(correct=True))
            possible_values.append(self._get_name(correct=True))
            return str(random.sample(possible_values, 1)[0])

    def _get_name(self, correct):
        """ Gets a name test string.
        correct determines if a correct or incorrect string should be returned
        """
        alphabet = self.LETTERS+self.DIGITS
        length = random.randint(1, self.max_l)
        if length == 0:
            return ''
        word = self._get_word(length, alphabet)
        if correct:
            return word
        else:
            nr_bad_chars = random.randint(1, length)
            return self._insert_bad_chars(word, nr_bad_chars,\
                    self.NAME_NOT_ALLOW)

    def _get_condition(self, correct):
        """ Gets a condition test string.
        correct determines if a correct or incorrect string should be returned
        """
        possibilities = []
        key_pat = '"[{}] = {}"'
        possibilities.append('always')
        if correct:
            name = self._get_name(correct=True)
            value = self._get_number(correct=True)
            possibilities.append(key_pat.format(name, value))
        else:
            name = self._get_name(correct=False)
            value = self._get_number(correct=True)
            possibilities.append(key_pat.format(name, value))
            value = self._get_number(correct=False)
            possibilities.append(key_pat.format(name, value))
            name = self._get_name(correct=True)
            possibilities.append(key_pat.format(name, value))
        result = random.choice(possibilities)
        return result

    def _get_text(self, correct):
        """ Gets a text test string.
        correct determines if a correct or incorrect string should be returned
        """
        without_quotes = self.LETTERS+self.DIGITS
        with_quotes = without_quotes + self.PUNCTUATION + self.WHITESPACE
        length = random.randint(1, self.max_l)
        if length == 0:
            return ''
        word = self._get_word(length, without_quotes)
        text = self._get_word(length, with_quotes)
        possibilities = []
        if correct:
            possibilities.append(word)
            possibilities.extend(self._correct_quotes(word))
            possibilities.extend(self._correct_quotes(text))
        else:
            possibilities.extend(self._incorrect_quotes(word))
            possibilities.extend(self._incorrect_quotes(text))
            nr_bad_chars = random.randint(1, length)
            possibilities.append(self._insert_bad_chars(word, nr_bad_chars,\
                    self.TEXT_NOT_ALLOW))
            possibilities.append(self._insert_bad_chars(text, nr_bad_chars,\
                    self.TEXT_NOT_ALLOW))
        result = random.sample(possibilities, 1)
        return ''.join(result)

    def _get_keyword(self, correct):
        """ Gets a keyword test string.
        correct determines if a correct or incorrect string should be returned
        """
        possibilities = []
        key_pat = '{}={}'
        if correct:
            name = self._get_name(correct=True)
            value = self._get_name(correct=True)
            possibilities.append(key_pat.format(name, value))
            value = self._get_text(correct=True)
            possibilities.append(key_pat.format(name, value))
            value = self._get_number(correct=True)
            possibilities.append(key_pat.format(name, value))
        else:
            name = self._get_name(correct=False)
            value = self._get_name(correct=True)
            possibilities.append(key_pat.format(name, value))
            value = self._get_text(correct=True)
            possibilities.append(key_pat.format(name, value))
            value = self._get_number(correct=True)
            possibilities.append(key_pat.format(name, value))
            name = self._get_name(correct=True)
            value = self._get_name(correct=False)
            possibilities.append(key_pat.format(name, value))
            value = self._get_text(correct=False)
            possibilities.append(key_pat.format(name, value))
            value = self._get_number(correct=False)
            possibilities.append(key_pat.format(name, value))
            possibilities.append(self._get_name(correct=True))
            possibilities.append(self._get_number(correct=True))
        result = random.choice(possibilities)
        return result

    @staticmethod
    def _get_word(length, alphabet):
        """ Gets a random word from the given alphabet with length length """
        word = ''.join([random.choice(alphabet) for _ in xrange(length)])
        return word

    @staticmethod
    def _insert_bad_chars(word, nr_bad_chars, bad_alphabet):
        """ Insert a bad character into a number of random positions in a word
        """
        bad_chars = [random.choice(bad_alphabet) for _ in xrange(nr_bad_chars)]
        w_list = list(word)
        for bad_char in bad_chars:
            bad_loc = random.randint(0, len(word) -1)
            w_list[bad_loc] = bad_char
        return ''.join(w_list)

    @staticmethod
    def _correct_quotes(quote_string):
        """ Adds 'correct' quotes, so to the start and end of the string """
        return ['"'+quote_string+'"', "'"+quote_string+"'"]

    @staticmethod
    def _incorrect_quotes(q_string):
        """ Adds 'incorrect' quotes, to the start or end of the string"""
        return [q_string+'"', q_string+"'", '"'+q_string, "'"+q_string]
