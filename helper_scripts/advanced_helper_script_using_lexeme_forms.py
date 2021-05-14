import sys

import requests as r
from pprint import pprint
from ppprint import console
# from prompt_toolkit import prompt
# from prompt_toolkit.history import FileHistory
# from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
# from prompt_toolkit.completion import Completer, Completion
# import click
# from fuzzyfinder import fuzzyfinder

def fetch_lexeme_forms_templates():
    # This is a bit of a hack since the information is not available in e.g. JSON
    # we have to write it to a file to use the data
    response = r.get(url="https://lexeme-forms.toolforge.org/api/v1/template/")
    if response.status_code == 200:
        return response.json()

def read_file():
    print("Attempting to read the csv file with one word per line")
    try:
        with open(sys.argv[1], 'r') as f:
            return f.readlines()
    except IndexError:
        console.error("IndexError during reading of csv file ")
        exit(1)

if __name__ == '__main__':
    lines = read_file()
    console.info("Fetching lexeme forms templates")
    templates = fetch_lexeme_forms_templates()
    #pprint(templates["swedish-noun-common"])
    # Ask relevant questions
    language_code = input("What is the wikimedia language code?: ")
    language_item_id = input("What language item QID?: ")
    lexical_category_item_id = input("What lexical category QID?: ")
    # find the right form among the templates
    # TODO enable choosing in repl
    forms = templates["swedish-noun-neuter"]["forms"]
    # let the user type in a generic ending for each form
    generic_endings = []
    for form in forms:
        ending = input(f'Type in the generic ending for: {form["label"]} \nwith the example: {form["example"]}: ')
        generic_endings.append(ending)
    print("Writing output to output.tsv")
    with open("output.tsv", "a") as f:
        for line in lines:
            line = line.strip()
            f.write(f"CREATE\n")
            f.write(f"LAST\tLEM\t{line}\n")
            f.write(f"LAST\tLC\t{lexical_category_item_id}\n")
            f.write(f"LAST\tLANG\t{language_item_id}\n")
            f.write(f"LAST\tLANG_CODE\t{language_code}\n")
            # get the grammatical features for each of the forms and generate them
            for index, form in enumerate(forms):
                f.write(f"LAST\tCREATE_FORM\n")
                f.write(f"LAST\tRsv\t{line+generic_endings[index]}\n")
                grammatical_features = form['grammatical_features_item_ids']
                if len(grammatical_features) > 1:
                    for gf in grammatical_features:
                        f.write(f"LAST\tGF\t{gf}\n")
                elif len(grammatical_features) == 0:
                    console.warn("No grammatical features specified")
                else:
                    # only 1 gf
                    console.debug(f"Only 1 grammatical feature found for {line}")
                    f.write(f"LAST\tGF\t{form['grammatical_features_item_ids']}\n")
                f.write(f"LAST\tEND_FORM\n")
            f.write(f"END\n")
    print("Done")