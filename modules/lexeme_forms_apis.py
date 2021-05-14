#import typing

import requests as r
from pprint import pprint
#from ppprint import console

# see documentation https://www.wikidata.org/wiki/Wikidata:Wikidata_Lexeme_Forms#Duplicates_API

# https://lexeme-forms.toolforge.org/api/v1/duplicates/www/language-code/lemma

# *********
# Duplicates API
def get_duplicates(lemma: str = None,
                   language_code: str = None):
    # The response is either a JSON array with objects for the search results, where each object has id,
    # label, description and uri members, or HTTP 204 No Content if there are no results.
    header = dict(
        Accept="application/json"
    )
    if lemma is not None and language_code is not None:
        response = r.get(url=f"https://lexeme-forms.toolforge.org/api/v1/duplicates/www/{language_code}/{lemma}",
                         headers=header)
        if response.status_code == 204:
            return None
        else:
            json = response.json()
            pprint(json)
            return json