import re
import sys
import json
from typing import Dict, List, Tuple
from pprint import pprint

from ppprint import console
#from wikibaseintegrator import wbi_core, wbi_login
#import mwapi
import LexData
import LexData.language

import config

# ***********************
# Purpose: This script creates lexemes based on a list with the following syntax
# Syntax: similar to QS V1
# LC = lexical category
# LEM = lemma
# LANG = language QID
# LANG_CODE = wikimedia code for language
# Form syntax:
# Rxx = representation language code e.g. Rsv for Swedish
# GF = grammatical feature
# FP = form property
# see example.tsv for an example

# Pseudo code
# Parse the commands
# if not valid give parse error
# For each command execute against the API

wd_prefix = "http://www.wikidata.org/entity/"

def parse_input_file(contents) -> Dict:
    create_lexeme_found = False
    create_form_found = False
    data = {}
    commands =[]
    new_lexemes = []
    create_lexeme_data = {}
    claims = []
    forms = []
    create_form_data = {}
    grammatical_features = []
    form_representations = []
    for line in contents:
        # Handle new lexemes
        if line.strip() == "CREATE":
            create_lexeme_found = True
            console.info("Found create lexeme")
        elif line.find("LAST", 0) == 0 and create_lexeme_found:
            #print(f"Found command starting with last: {line}")
            # check command validity
            valid = re.search(r"[A-Z]+\t[A-Z0-9_]+\t*.*", line.strip())
            # print(tabs)
            if valid is None:
                console.error(f"Error. This line is not a valid command: {line}")
                exit(1)
            if line.find("LEM") == 5:
                lemma = line.strip()[9:]
                if len(lemma) > 0:
                    create_lexeme_data["lemma"] = lemma
                    console.debug(f"lemma:{lemma}")
                else:
                    console.error(f"No lemma found")
                    exit(1)
            elif line.find("LC") == 5:
                category = line.strip()[8:]
                create_lexeme_data["lexical_category"] = category
                console.debug(f"category:{category}")
            elif line.find("LANG\t") == 5:
                language = line.strip()[10:]
                create_lexeme_data["language_item_id"] = language
                console.debug(f"language:{language}")
            # TODO consider fetching this using sparql and https://www.wikidata.org/wiki/Property:P424
            elif line.find("LANG_CODE") == 5:
                language_code = line.strip()[15:]
                create_lexeme_data["language_code"] = language_code
                console.debug(f"language_code:{language_code}")
            elif line.find("\tP") == 4:
                tab_index = line.find('\t', 5)
                property = line[5:tab_index]
                console.debug(f"property:{property}")
                value = line.strip()[tab_index + 1:]
                claims.append((property,value))
                console.debug(f"value:{value}")
            # Handle forms
            elif line.find("LAST\tCREATE_FORM") == 0:
                create_form_found = True
                console.debug("Found create form")
            elif create_form_found and line.find("\tR") == 4:
                tab_index = line.find('\t', 5)
                form_representation_language_code = line[6:tab_index]
                console.debug(f"Found form representation with code {form_representation_language_code}")
                tab_index = line.find('\t', 5)
                form_representation = line.strip()[tab_index + 1:]
                console.debug(f"form_representation:{form_representation}")
                form_representations.append((
                    form_representation_language_code,
                    form_representation
                ))
            elif create_form_found and line.find("\tGF") == 4:
                tab_index = line.find('\t', 5)
                grammatical_feature = line.strip()[tab_index + 1:]
                console.debug(f"grammatical_feature:{grammatical_feature}")
                grammatical_features.append(grammatical_feature)
            elif create_form_found and line.find("\tFP") == 4:
                tab_index = line.find('\t', 5)
                property = line[6:tab_index]
                console.debug(f"form property:{property}")
                value = line.strip()[tab_index + 1:]
                create_form_data[property] = value
                console.debug(f"value:{value}")
            elif create_form_found and line.find("LAST\tEND_FORM") == 0:
                # add list of grammatical features to form data
                create_form_data["grammatical_features"] = grammatical_features
                # add list of form representations to form data
                create_form_data["form_representations"] = form_representations
                # add form to list of forms
                forms.append(create_form_data)
                create_form_found = False
                # Cleanup
                create_form_data = {}
                grammatical_features = []
                form_representations = []
            else:
                console.warn(f"Skipped {line}", line.find("\tP"))
        elif line.find("END") == 0:
            # add forms to lexeme data
            create_lexeme_data["forms"] = forms
            # add claims to lexeme data
            create_lexeme_data["claims"] = claims
            # add lexeme data to list of new lexemes
            new_lexemes.append(create_lexeme_data)
            create_lexeme_found = False
            create_lexeme_data = {}
        elif line.find("L") == 0:
            # Command on existing lexeme found
            if line.find("P") != -1:
                lexeme_id_index = line.find("L")
                property_index = line.find("P")
                first_tab_index = property_index - 1
                lexeme_id = line.strip()[0:first_tab_index]
                second_tab_index = line.find('\t', property_index)
                property = line[property_index:second_tab_index]
                console.debug(f"property:{property}")
                value = line.strip()[second_tab_index + 1:]
                command = dict(
                    lexeme=lexeme_id,
                    property=property,
                    value=value,
                )
                commands.append(command)
                console.debug(f"value:{value}")
            else:
                console.error(f"No property found on line {line}")
                exit(1)
        else:
            console.warn(f"Skipped {line}")
    data["new_lexemes"] = new_lexemes
    data["commands"] = commands
    return data

if __name__ == '__main__':
    try:
        with open(sys.argv[1], 'r') as f:
            contents = f.readlines()
    except IndexError:
        console.error("IndexError during reading of tsv file ")
        exit(1)
    if contents is not None:
        data = parse_input_file(contents)
    console.info("Commands parsed successfully")
    pprint(data)
    #exit(0)
    new_lexeme_count = len(data["new_lexemes"])
    command_count = len(data["commands"])
    if new_lexeme_count > 0 or command_count > 0:
        # see https://www.wikidata.org/w/api.php?action=help&modules=wbeditentity for documentation
        console.info("Logging in with LexData")
        repo = LexData.WikidataSession(config.user, config.botpassword)
        # first execute creation of lexemes
        if new_lexeme_count > 0:
            for lexeme in data["new_lexemes"]:
                lemma = lexeme["lemma"]
                forms = lexeme["forms"]
                claims = lexeme["claims"]
                wikimedia_language_code = lexeme["language_code"]
                language_item_id = lexeme["language_item_id"]
                lexical_category = lexeme["lexical_category"]
                console.info(f"Creating {lemma} with {len(forms)} forms and {len(claims)} claims")
                # Find or create a Lexeme by lemma, language and lexical category
                # Configure languages of LexData
                lang = LexData.language.Language(wikimedia_language_code, language_item_id)
                # Try finding it or create a new lexeme
                new_lexeme = LexData.get_or_create_lexeme(repo, lemma, lang, lexical_category)
                pprint(new_lexeme)
                for form in forms:
                    # FIXME only supports 1 representation
                    form_representation: Tuple = form["form_representations"][0] # list of tuples
                    word: str = form_representation[1]
                    grammatical_features = form["grammatical_features"] # list of strings
                    pprint(grammatical_features)
                    result = new_lexeme.createForm(form_representation[1], grammatical_features)
                    pprint(result)

                # lexeme_data = {
                #     'type': 'lexeme',
                #     #'forms': forms,
                #     'lemmas': {lang: {'language': lang, 'value': lemma}},
                #     'language': language_item_id,
                #     'lexicalCategory': lexical_category,
                #     #'claims': template.get('statements', {}),
                # }
                # #selector = {'id': lexeme_data['id']} if 'id' in lexeme_data else {'new': 'lexeme'}
                # selector = {'new': 'lexeme'}
                # # if 'base_revision_id' in lexeme_data:
                # #     selector['baserevid'] = lexeme_data['base_revision_id']
                # summary = "Adding lexeme using LexBatchCreator by So9q"
                # response = session.post(
                #     action='wbeditentity',
                #     data=json.dumps(lexeme_data),
                #     summary=summary,
                #     token=token,
                #     **selector
                # )
                # lexeme_id = response['entity']['id']
                # print(lexeme_id)
                # exit(0)
                # print("Logging in with WikibaseIntegrator")
                # wbi_login.Login(user=config.user, pwd=config.botpassword)
        if command_count > 0:
            # TODO implement adding claims to existing lexemes (using WikibaseIntegrator)
            #print("Updating lexeme now using LexData")
            # Open a Lexeme
            # L2 = LexData.Lexeme(repo, "L2")
            pass