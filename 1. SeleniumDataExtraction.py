import csv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
from AverageNumberOFWords import *

# Initialize a browser instance
driver = webdriver.Chrome()  # For Chrome
isheaderwritten = False


def save_the_data(result_dict):
    filepath = "Output_data.csv"
    global isheaderwritten
    with open(filepath, 'a', newline="") as file:
        csv_writer = csv.DictWriter(file, fieldnames=result_dict.keys())
        if not isheaderwritten:
            csv_writer.writeheader()
            csv_writer.writerow(result_dict)
            isheaderwritten = True
        else:
            csv_writer.writerow(result_dict)

    print("Data Has Been Saved")
    print("*" * 50)


def get_all_the_data(tokenized_title, tokenized_content, url_id, url):
    print("get all the data")
    """This function will call all the functions and return all the values"""
    positive_score, negative_score = get_positive_negative_score(tokenized_title=tokenized_title,
                                                                 tokenized_content=tokenized_content)
    polarity_score = get_polarity_score(positive_score=positive_score, negative_score=negative_score)
    word_count_after_cleaning = get_word_count(tokenized_title=tokenized_title, tokenized_content=tokenized_content)
    subjective_score = get_subjective_score(positive_score=positive_score, negative_score=negative_score,
                                            clean_word_count=word_count_after_cleaning)
    avg_sent_length = get_average_sentence_length(tokenized_title, tokenized_content)
    percentage_of_complex_word = get_percentage_of_complex_words(tokenize_title=tokenized_title,
                                                                 tokenize_content=tokenized_content)
    fog_index = get_fog_index(tokenized_title, tokenized_content)
    avg_number_of_words = avg_sent_length
    complex_count = complex_word_count(tokenize_title=tokenized_title, tokenize_content=tokenized_content)
    word_count = get_word_count(tokenized_title=tokenized_title, tokenized_content=tokenized_content)
    syllable_count = get_syllable_count_per_word(tokenized_title=tokenized_title, tokenized_content=tokenized_content)
    personal_pronoun = get_personal_pronoun(tokenized_title=tokenized_title, tokenized_content=tokenized_content)
    avg_word_length = get_avg_word_length(tokenized_title=tokenized_title, tokenized_content=tokenized_content)
    result_dict = {
        "url_id": url_id,
        "url": url,
        "positive_score": positive_score,
        "negative_score": negative_score,
        "polarity_score": f"{polarity_score:.2f}",
        "subjective_score": f"{subjective_score:.2f}",
        "Avg_Sentence_length": f"{avg_sent_length:.2f}",
        "percentage_of_complex_word": f"{percentage_of_complex_word:.2f}%",
        "fog_index": f"{fog_index:.2f}",
        "avg_number_of_words":f"{avg_number_of_words:.2f}" ,
        "complex_word_count": complex_count,
        "word_count": word_count,
        "Syllable_per_word": syllable_count,
        "personal_pronoun": personal_pronoun,
        "avg_word_length": f"{avg_word_length:.2f}"
    }
    print(f"Data Calculated")
    save_the_data(result_dict)


def tokenized_title_and_content(title, content, url_id=" ", url=""):
    """This will take input from Scraping data"""
    # nltk.download('stopwords') # for installing package first time
    # nltk.download('punkt')  # for installing package first time.
    # This functions stop_word_extractions will extract the stop word from the text file and  return the stop word list
    stop_word_set = set(stop_word_list)  # converting to set because I don't to add repeat word daily.

    # Using NLTK
    tokenize_title = nltk.word_tokenize(title)
    tokenize_content = nltk.word_tokenize(content)

    filter_tokenized_title = [title for title in tokenize_title if title.lower() not in stop_word_set]  # This is a list
    filter_tokenized_content = [content for content in tokenize_content if
                                content.lower() not in stop_word_set]  # This is a list
    print("Title and Contents has Tokenized Succefully")
    get_all_the_data(filter_tokenized_title, filter_tokenized_content, url_id, url)


def get_url_from_excel():
    df = pd.read_excel('Input.xlsx')
    # Iterate over the rows of the DataFrame and convert each row into a tuple
    dict_list = df.to_dict(orient='records')
    # returns the list of dictionary
    return dict_list


# This function is used to extract the data and sent to tokenized_title_and_content
def data_extraction_and_sending(url_id, url):
    try:
        title_text = driver.find_element(By.TAG_NAME, 'h1')
        div_tag_text = driver.find_element(By.CLASS_NAME, 'td-post-content.tagdiv-type')
        title = title_text.text
        content = div_tag_text.text
        print("Data Extraxtacted Successfully")
    except NoSuchElementException:
        print("There is no data on link")
        return
    # This function is written in SentimentAnalysis file for sending the title and content to perform sentiment
    # analysis.
    tokenized_title_and_content(title, content, url_id, url)


def link_setting(url_id, url):
    """This is used for setting the link"""
    driver.get(url)
    data_extraction_and_sending(url_id=url_id, url=url)


# {'URL_ID': 'blackassign0001', 'URL': 'https://insights.blackcoffer.com/rising-it-cities-and-its-impact-on-the
# -economy-environment-infrastructure-and-city-life-by-the-year-2040-2/'}

# entry point of this file
def get_urlName_url():
    """This function is taking url and url_id from ExtractionOfLink name get_urlId_url"""
    dict_list = get_url_from_excel()
    # update the list for the stop words
    stop_words_extractions()
    for value in dict_list:
        url_id = value['URL_ID']
        url = value['URL']
        print("*" * 50)
        print(url_id)
        link_setting(url_id, url)
        #time.sleep(2)


get_urlName_url()

# Close the browser
driver.quit()
