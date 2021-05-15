# LexBatchCreator
This script creates lexemes based on a special syntax that can be easily generated manually using LibreOffice or similar spreadsheet software or by other tools.

## Syntax
similar to QuickStatements V1
- LC = lexical category item ID
- LEM = lemma
- LANG = language QID
- LANG_CODE = wikimedia code for language e.g. "sv"
- Form syntax:
- Rxx = representation language code e.g. "Rsv" for Swedish
- GF = grammatical feature
- FP = form property
- TODO: Sense syntax

see the examples-folder for more

## Development
Below is list of features that is planned to be implemented, pull requests are welcome :)

On existing lexemes:
- Check for duplicates when adding a form
- Adding forms with 1 form representation
- Adding multiple form representations to a form
- Adding senses with one gloss
- Adding senses with multiple glosses
- Adding lexeme statements (QS supports this, WikibaseIntegrator as well)
- Adding form statements
- Adding sense statements
- Adding form representation on existing form
- Adding gloss on existing sense
- Deleting lexeme statements (QS supports this)
- Deleting form statements
- Deleting sense statements
- Removing forms
- Removing senses
- Removing grammatical features on forms
- Removing glosses on senses

On new lexemes: 
- Adding forms with 1 form representation (implemented may 2021)
- Adding forms with multiple grammatical features (implemented may 2021)
- Adding multiple form representations to a form
- Adding senses with one gloss
- Adding senses with multiple glosses
- Adding lexeme statements
- Adding form statements
- Adding sense statements

## Setup
Copy config.example.py to config.py yourself and adjust the following
content:
```
username = "username"
password = "password"
```
