from summa.summarizer import summarize
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize


def get_drug_summary(drug_name, info_required):
    top_hit = ""
    drug_search_url = "https://www.webmd.com/drugs/2/search?type=drugs&query=" + drug_name.replace(" ", "%20")
    response = requests.get(drug_search_url)

    if drug_search_url != response.url:
        top_hit = response.url

    else:
        try:
            search_soup = BeautifulSoup(response.text, 'html.parser')

            results = search_soup.find(class_="exact-match")
            first_result = results.find("li").find("a")

            top_hit = "https://www.webmd.com" + first_result.get("href")

        #if no drug found:
        except:
            return False

    # grab information about drug:

    drug_info_resposne = requests.get(top_hit)
    drug_soup = BeautifulSoup(drug_info_resposne.text, 'html.parser')

    if info_required == "uses":
        tab_number = "tab-1"

    if info_required == "side effects":
        tab_number = "tab-2"

    if info_required == "precautions":
        tab_number = "tab-3"

    if info_required == "interactions":
        tab_number = "tab-4"

    uses = drug_soup.find("div", attrs={"id": tab_number})
    main_text = uses.find("div", attrs={"class": "inner-content"})

    paragraphs = main_text.find_all("p")

    text = ""

    for paragraph in paragraphs:
        text += paragraph.text

    text = text.replace(".", ". ")
    text = text.replace(")", ") ")
    text_sentences = sent_tokenize(text)

    text_sentences = [sentence for sentence in text_sentences if
                      "doctor" not in sentence.lower() and "www" not in sentence.lower() and "likelihood" not in sentence.lower()]

    text = ""

    for sentence in text_sentences:
        text += sentence + " "

    summarized = summarize(text, words=30)
    return summarized


print(get_drug_summary("migraine tablets", "uses"))
