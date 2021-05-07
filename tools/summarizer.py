"""
    This module provides a summarize_book function.
    It takes a url as input, and attempts to generates a 
    summary for the text.
"""

# imports
from transformers import pipeline
import re
import requests

def summarize_book(url):
    # get the text with requests
    
    txt_url = url
    # for now, work with a single book
    # txt_url = "https://www.gutenberg.org/files/103/103.txt"  # verne (1st)
    # txt_url = "https://www.gutenberg.org/files/11/11-0.txt"  # alice (short)
    #txt_url = "https://www.gutenberg.org/files/65238/65238-0.txt"  # (recent)

    r = requests.get(txt_url)
    print(f"Request for {txt_url} returned status code: {r.status_code}")
    ebook = r.content.decode()

    # clean it up

    # cut off the boilerplate text at the start and at the end
    sp = re.compile("[*]{3}\sSTART\sOF.+PROJECT\sGUTENBERG\sEBOOK.+\s[*]{3}")
    ep = re.compile("[*]{3}\sEND\sOF.+PROJECT\sGUTENBERG\sEBOOK.+\s[*]{3}")

    # remove the text before the start pattern
    cut_start = sp.split(ebook)[1]

    # remove the text after the end pattern
    cut_end = ep.split(cut_start)[0]

    # trim leading and trailing spaces and line breaks
    ebook = cut_end.strip()

    # define a list of chars to substitute by space
    chars_to_sub = re.compile("[\r\n—*]+")

    # substitute them
    ebook = chars_to_sub.sub(" ", ebook)

    # define a list of chars to drop
    chars_to_drop = re.compile("[_]+")

    # drop them
    ebook = chars_to_drop.sub("", ebook)

    # remove consecutive spaces
    ebook = " ".join(ebook.split())

    # replace ebook with textfile for now because of errors
    with open('chapter.txt', 'r') as file:
        ebook = file.read()

    # preprocess the ebook for summarization
    doc = ebook

    max_chunk = 500

    end_of_sentence = [".", "?", "!"]
    suffix = "<eos>"
    for eos in end_of_sentence:
        doc = doc.replace(eos, f"{eos}{suffix}")

    sentences = doc.split(suffix)
    current_chunk = 0
    chunks = []

    for sentence in sentences:
        if len(chunks) == current_chunk + 1:
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            print(current_chunk)
            chunks.append(sentence.split(' '))
    
    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])
    
    print(f"Number of chunks: {len(chunks)}")

    # summarize it
    # summarizer = pipeline("summarization", model="sshleifer/distilbart-xsum-12-6")
    summarizer = pipeline("summarization")

    res = summarizer(chunks, max_length=120, min_length=30, do_sample=False)

    summary = ' '.join([summ['summary_text'] for summ in res])

    return summary