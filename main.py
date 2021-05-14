import re
import sys

from pprint import pprint
import wikibaseintegrator

# ***********************
# Purpose: This script creates lexemes based on a list with the following syntax
# Syntax: similar to QS V1
# LC = lexical category
# LEM = lemma
# Example:
# CREATE
# LAST  LEM  "test lemma"
# LAST  LC  Q1084
# LAST  LANG    Q9058
# LAST  P31 Q489168

# Pseudo code
# Parse the commands
# if not valid give parse error
# For each command execute against the API

def parse_input_file():
    create_found = False
    commands = {}
    for line in contents:
        if line.strip() == "CREATE":
            create_found = True
            print("Found create")
        elif line.find("LAST", 0) == 0 and create_found:
            print(f"Found command starting with last: {line}")
            # check command validity
            valid = re.search(r"[A-Z]+\t[A-Z0-9]+\t.*", line.strip())
            # print(tabs)
            if valid is None:
                print(f"Error. This line is not a valid command: {line}")
                exit(1)
            if line.find("LEM") == 5:
                lemma = line.strip()[9:]
                if len(lemma) > 0:
                    commands["lemma"] = lemma
                    print(f"lemma:{lemma}")
                else:
                    print(f"No lemma found")
                    exit(1)
            elif line.find("LC") == 5:
                category = line.strip()[8:]
                commands["category"] = category
                print(f"category:{category}")
            elif line.find("LANG") == 5:
                language = line.strip()[10:]
                commands["language"] = language
                print(f"language:{language}")
            elif line.find("P") == 5:
                tabindex = line.find('\t', 5)
                property = line[5:tabindex]
                print(f"property:{property}")
                value = line.strip()[tabindex + 1:]
                commands[property] = value
                print(f"value:{value}")
        else:
            print(f"Skipped {line}")
    return commands

if __name__ == '__main__':
    try:
        with open(sys.argv[1], 'r') as f:
            contents = f.readlines()
        #print(contents)
        commands = parse_input_file()
        if len(commands) > 1:
            print("Creating lexeme now")
            pprint(commands)
            
    except IndexError:
        print("Error: no input file provided. ")
        exit(1)