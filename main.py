import re
import sys

from typing import Dict
from pprint import pprint
from wikibaseintegrator import wbi_core, wbi_login
import mwapi

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

def parse_input_file() -> Dict:
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
            print("Found create lexeme")
        elif line.find("LAST", 0) == 0 and create_lexeme_found:
            #print(f"Found command starting with last: {line}")
            # check command validity
            valid = re.search(r"[A-Z]+\t[A-Z0-9_]+\t*.*", line.strip())
            # print(tabs)
            if valid is None:
                print(f"Error. This line is not a valid command: {line}")
                exit(1)
            if line.find("LEM") == 5:
                lemma = line.strip()[9:]
                if len(lemma) > 0:
                    create_lexeme_data["lemma"] = lemma
                    print(f"lemma:{lemma}")
                else:
                    print(f"No lemma found")
                    exit(1)
            elif line.find("LC") == 5:
                category = line.strip()[8:]
                create_lexeme_data["category"] = category
                print(f"category:{category}")
            elif line.find("LANG\t") == 5:
                language = line.strip()[10:]
                create_lexeme_data["language"] = language
                print(f"language:{language}")
            # TODO consider fetching this using sparql and https://www.wikidata.org/wiki/Property:P424
            elif line.find("LANG_CODE") == 5:
                language_code = line.strip()[15:]
                create_lexeme_data["language_code"] = language_code
                print(f"language_code:{language_code}")
            elif line.find("\tP") == 4:
                tab_index = line.find('\t', 5)
                property = line[5:tab_index]
                print(f"property:{property}")
                value = line.strip()[tab_index + 1:]
                claims.append((property,value))
                print(f"value:{value}")
            # Handle forms
            elif line.find("LAST\tCREATE_FORM") == 0:
                create_form_found = True
                print("Found create form")
            elif create_form_found and line.find("\tR") == 4:
                tab_index = line.find('\t', 5)
                form_representation_language_code = line[6:tab_index]
                print(f"Found form representation with code {form_representation_language_code}")
                tab_index = line.find('\t', 5)
                form_representation = line.strip()[tab_index + 1:]
                print(f"form_representation:{form_representation}")
                form_representations.append((
                    form_representation_language_code,
                    form_representation
                ))
            elif create_form_found and line.find("\tGF") == 4:
                tab_index = line.find('\t', 5)
                grammatical_feature = line.strip()[tab_index + 1:]
                print(f"grammatical_feature:{grammatical_feature}")
                grammatical_features.append(grammatical_feature)
            elif create_form_found and line.find("\tFP") == 4:
                tab_index = line.find('\t', 5)
                property = line[6:tab_index]
                print(f"form property:{property}")
                value = line.strip()[tab_index + 1:]
                create_form_data[property] = value
                print(f"value:{value}")
            elif create_form_found and line.find("LAST\tEND_FORM") == 0:
                # add list of grammatical features to form data
                create_form_data["grammatical_features"] = grammatical_features
                # add list of form representations to form data
                create_form_data["form_representations"] = form_representations
                # add form to list of forms
                forms.append(create_form_data)
                create_form_found = False
                create_form_data = {}
            else:
                print(f"Skipped {line}", line.find("\tP"))
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
                print(f"property:{property}")
                value = line.strip()[second_tab_index + 1:]
                command = dict(
                    lexeme=lexeme_id,
                    property=property,
                    value=value,
                )
                commands.append(command)
                print(f"value:{value}")
        else:
            print(f"Skipped {line}")
    data["new_lexemes"] = new_lexemes
    data["commands"] = commands
    return data

if __name__ == '__main__':
    commands = None
    try:
        with open(sys.argv[1], 'r') as f:
            contents = f.readlines()
    except IndexError:
        print("IndexError during reading of tsv file ")
        exit(1)
    data = parse_input_file()
    print("Commands parsed succesfully")
    pprint(data)
    exit(0)
    if len(data["new_lexemes"]) > 0 and len(data["commands"]) > 0:
        # login
        # see https://www.wikidata.org/w/api.php?action=help&modules=wbeditentity for documentation
        print("Logging in with mwapi")
        host = 'https://test.wikidata.org'
        session = mwapi.Session(host)
        print(session.login(config.user, config.botpassword))
        # first execute creation of lexemes
        if len(data["new_lexemes"]) > 0:
            for lexeme in data["new_lexemes"]:
                lemma = lexeme["lemma"]
                forms = lexeme["forms"]
                claims = lexeme["claims"]
                print(f"Creating {lemma} with {len(forms)} forms and {len(claims)} claims")
                # TODO translate the data into Wikibase JSON format
                # lexeme_data = {
                #     'type': 'lexeme',
                #     'forms': forms,
                # }
                # lexeme_data.update({
                #     'lemmas': {lang: {'language': lang, 'value': lemma}},
                #     'language': template['language_item_id'],
                #     'lexicalCategory': template['lexical_category_item_id'],
                #     'claims': template.get('statements', {}),
                # })
                # token = session.get(action='query', meta='tokens')['query']['tokens']['csrftoken']
                # #selector = {'id': lexeme_data['id']} if 'id' in lexeme_data else {'new': 'lexeme'}
                # selector = {'new': 'lexeme'}
                # if 'base_revision_id' in lexeme_data:
                #     selector['baserevid'] = lexeme_data['base_revision_id']
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
                # print("Creating lexeme now")
                #
                # # first create the lexeme using mwapi