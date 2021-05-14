import sys

from ppprint import console

if __name__ == '__main__':
    print("Attempting to read the csv file with one word per line")
    try:
        with open(sys.argv[1], 'r') as f:
            contents = f.readlines()
    except IndexError:
        console.error("IndexError during reading of csv file ")
        exit(1)
    language_code = input("What is the wikimedia language code?: ")
    language_item_id = input("What language item QID?: ")
    lexical_category_item_id = input("What lexical category QID?: ")
    print("Writing output to output.tsv")
    with open("output.tsv", "a") as f:
        for line in contents:
            line = line.strip()
            f.write(f"CREATE\n")
            f.write(f"LAST\tLEM\t{line}\n")
            f.write(f"LAST\tLC\t{lexical_category_item_id}\n")
            f.write(f"LAST\tLANG\t{language_item_id}\n")
            f.write(f"LAST\tLANG_CODE\t{language_code}\n")
            f.write(f"LAST\tCREATE_FORM\n")
            f.write(f"LAST\tRsv\t{line}\n")
            f.write(f"LAST\tEND_FORM\n")
            f.write(f"END\n")
    print("Done")