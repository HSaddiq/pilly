import requests
import xmljson
from xml.etree.ElementTree import fromstring, tostring
import json


# returns ID of drug from a list
def drug_name_to_ID(drug_name):
    requests_url = "https://rxnav.nlm.nih.gov/REST/approximateTerm?term=" + drug_name.replace(" ", "%20")
    response = requests.get(requests_url)
    xml = fromstring(response.text)
    drug_json = json.loads(json.dumps(xmljson.parker.data(xml)))
    return drug_json["approximateGroup"]["candidate"][0]["rxcui"]


# checks compatibility with existing prescription for compatibility issues with suggested drug
def get_drug_compatibility(list_of_drug_names, additional_drug):
    list_of_ids = [drug_name_to_ID(drug_name) for drug_name in list_of_drug_names]
    list_of_ids.append(drug_name_to_ID(additional_drug))

    addtional_drug_ID = drug_name_to_ID(additional_drug)

    interaction_url = "https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis=" + "+".join(
        str(id) for id in list_of_ids)

    interactions_json = json.loads(requests.get(interaction_url).text)
    interaction_pairs = interactions_json["fullInteractionTypeGroup"][0]["fullInteractionType"]
    comments = []

    for interaction in interaction_pairs:

        if addtional_drug_ID == int(interaction["minConcept"][0]["rxcui"]) or addtional_drug_ID == int(
                interaction["minConcept"][1]["rxcui"]):
            interaction_comment = interaction["interactionPair"][0]["description"]
            comments.append(interaction_comment)
    return comments


print(get_drug_compatibility(["levothyroxine", "omeprazole"], "ibuprofen"))
