import string
import re
from nltk.corpus import stopwords
import nltk
#from commonfunctions import get_positive_negative_file_data
import os
import json

stop_word_list = []
stop_word_string = ''




def get_directory_textfile_names(path_link):
    """This function is used to get all the text file names which is available in directory
     in a list format and it does not go to subdirectory"""
    # Get list of entries in the current directory
    directory_file_names = os.listdir(path_link)
    return directory_file_names


def get_positive_negative_file_data():
    """This functions will used to fetch the positive and negative sentiment."""
    # making an empty set for Positive and negative master dictionary word because we don't need double words.
    POSITIVE_WORD_SET = set()
    NEGATIVE_WORD_SET = set()

    MasterDirectoryfilePath = "MasterDictionary/"
    master_dictionary_files_list = get_directory_textfile_names(MasterDirectoryfilePath)
    for file_name in master_dictionary_files_list:
        if file_name == "negative-words.txt":
            with open(f"MasterDictionary/{file_name}", 'r') as file:
                for word in file:
                    NEGATIVE_WORD_SET.add(word.lower().replace('\n', ''))
        else:
            with open(f"MasterDictionary/{file_name}", 'r') as file:
                for word in file:
                    POSITIVE_WORD_SET.add(word.lower().replace('\n', ''))

    return POSITIVE_WORD_SET, NEGATIVE_WORD_SET


def stop_words_extractions():
    """This functions will used for extracting the stop words from different files."""

    stop_word_folder_link = "StopWords/"
    stop_word_file_list = get_directory_textfile_names(stop_word_folder_link)
    # get_positive_negative_file_data()  # # This function located in commonfunctions file for get the content of
    # the master dictionary.
    for file_link in stop_word_file_list:
        with open(f"StopWords/{file_link}", 'r') as file:
            for word in file:
                stop_word_list.append(word.replace("\n", "").lower())  # this lines gives all the stop words from the
                # text
                # files which is located in StopWord.




def get_positive_negative_score(tokenized_title: list, tokenized_content: list):
    """This functions will used to fetch the positive and negative sentiment."""
    positive = 0
    negative = 0
    POSITIVE_WORD_SET, NEGATIVE_WORD_SET = get_positive_negative_file_data()
    # title and Content are the list
    list_positive = list(POSITIVE_WORD_SET)
    list_negative = list(NEGATIVE_WORD_SET)
    positive = sum([1 for title_word in tokenized_title if title_word in list_positive])
    negative = sum([1 for title_word in tokenized_title if title_word in list_negative])
    # for title_word in title:
    #     if title_word in list_positive:
    #         positive += 1
    #     elif title_word in list_negative:
    #         negative -= 1
    #     else:
    #         pass
    positive += sum([1 for context_word in tokenized_content if context_word in list_positive])
    negative += sum([1 for content_word in tokenized_content if content_word in list_negative])
    # for content_word in content:
    #     if content_word in list_positive:
    #         positive += 1
    #     elif content_word in list_negative:
    #         negative -= 1
    # negative *= -1  # for change the sign to positive
    return positive, negative


def get_polarity_score(positive_score, negative_score, title=None, content=None):
    """This will Calculate Polarity Score
    Formula:- Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)
    It ranges from -1 to +1"""
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    return polarity_score


def get_subjective_score(positive_score, negative_score, clean_word_count):
    """This will give Subjective score
    Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
    Range is from 0 to +1
    """
    subjective_score = (positive_score + negative_score) / (clean_word_count + 0.000001)
    return subjective_score


def get_average_words(total_words: int, total_sentence: int):
    """The formula for calculating is:
        Average Number of Words Per Sentence = the total number of words / the total number of sentences
"""
    avg_words = total_words / total_sentence
    return avg_words


def get_syllable_count_per_word(tokenized_title, tokenized_content=""):
    """We count the number of Syllables in each word of the text by counting the vowels present in each word. We also
    handle some exceptions like words ending with "es","ed" by not counting them as a syllable."""
    word_list = tokenized_title + tokenized_content
    vowels = 'aeiouy'
    count = 0
    last_char_was_vowel = False
    for word in word_list:
        for char in word.lower():
            if char in vowels:
                if not last_char_was_vowel:
                    count += 1
                last_char_was_vowel = True
            else:
                last_char_was_vowel = False
        # Adjust for words ending with a silent 'e'
        if word.endswith('e'):
            count -= 1
        # Ensure at least one syllable is counted
    return max(count, 1)


def complex_word_count(tokenize_title, tokenize_content):
    """Complex words are words in the text that contain more than two syllables."""
    tokens = tokenize_title + tokenize_content
    # Initialize complex word count
    complex_words = 0

    # Count the number of complex words
    for word in tokens:
        syllable_count = get_syllable_count_per_word(word)
        if syllable_count > 2:
            complex_words += 1

    return complex_words


def remove_punctuations_word(tokens):
    # Tokenize the text into words

    # Filter out punctuations using NLTK's built-in punctuation list
    tokens_without_punctuations = [word for word in tokens if word not in string.punctuation]
    return tokens_without_punctuations


def remove_stop_word(tokenized_title: list, tokenized_content: list):
    tokens = tokenized_title + tokenized_content
    # Get the English stopwords from NLTK
    stop_words = set(stopwords.words('english'))

    # Filter out stopwords
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    return remove_punctuations_word(filtered_tokens)


def get_word_count(tokenized_title: list, tokenized_content: list):
    """We count the total cleaned words present in the text by
1.	removing the stop words (using stopwords class of nltk package).
2.	removing any punctuations like ? ! , . from the word before counting.
"""
    return len(remove_stop_word(tokenized_title=tokenized_title, tokenized_content=tokenized_content))


def get_personal_pronoun(tokenized_title, tokenized_content):
    """To calculate Personal Pronouns mentioned in the text, we use regex to find the counts of the words - “I,” “we,
    ” “my,” “ours,” and “us”. Special care is taken so that the country name US is not included in the list."""
    words_list = tokenized_title + tokenized_content
    text = " ".join(words_list)
    # Define the regular expression pattern to match personal pronouns
    pronoun_pattern = r'\b(?:I|we|my|ours|us)\b'

    # Compile the pattern
    regex = re.compile(pronoun_pattern, flags=re.IGNORECASE)

    # Find all matches of personal pronouns in the text
    matches = regex.findall(text)

    # Count the number of matches
    pronoun_count = len(matches)

    return pronoun_count


def get_avg_word_length(tokenized_title, tokenized_content):
    """Average Word Length is calculated by the formula:
    Sum of the total number of characters in each word/Total number of words"""
    words = tokenized_title + tokenized_content

    # Calculate the total number of characters in all words
    total_characters = sum(len(word) for word in words)

    # Calculate the total number of words
    total_words = len(words)

    # Calculate the average word length
    average_length = total_characters / total_words if total_words > 0 else 0

    return average_length


def get_average_sentence_length(tokenized_title, tokenized_content):
    """This will give average sentence length
    Average Sentence Length = the number of words / the number of sentences"""
    words = tokenized_title + tokenized_content

    ##############################################
    sentences = []
    start_idx = 0

    for i, word in enumerate(words):
        if word == '.':
            sentence = ' '.join(words[start_idx:i + 1])
            sentences.append(sentence)
            start_idx = i + 1

    # If there are remaining words after the last period
    if start_idx < len(words):
        sentence = ' '.join(words[start_idx:])
        sentences.append(sentence)

    return len(words) / len(sentences)


def get_percentage_of_complex_words(tokenize_title, tokenize_content):
    """This will give the percentage of complex word
    Percentage of Complex words = the number of complex words / the number of words """
    complex_word_percentage = complex_word_count(tokenize_title=tokenize_title,
                                                 tokenize_content=tokenize_content) / len(tokenize_content) + len(
        tokenize_title)
    return complex_word_percentage


def get_fog_index(tokenized_title, tokenized_content):
    """This link will give fog index= 0.4 * (Average Sentence Length + Percentage of Complex words)"""
    fog_index = 0.4 * (
            get_average_sentence_length(tokenized_title, tokenized_content) + get_percentage_of_complex_words(
        tokenize_title=tokenized_title, tokenize_content=tokenized_content))
    return fog_index
