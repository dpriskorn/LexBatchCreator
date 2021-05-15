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
WLF = Wikidata Lexeme Forms
WS = QuickStatements

On existing lexemes:
- Check for duplicates when bulk-adding forms (WLF supports this)
- Bulk-adding forms with 1 form representation (WLF supports this)
- Bulk-adding multiple form representations to a form (WLF supports this. In bulk mode only?)
- Bulk-adding senses with one gloss
- Bulk-adding senses with multiple glosses
- Bulk-adding lexeme statements (QS supports this, WikibaseIntegrator as well)
- Bulk-adding form statements
- Bulk-adding sense statements
- Bulk-adding form representation on existing form (WLF supports this, but the drag-n-drop possibility might not be clear to users leading to duplication of forms)
- Bulk-adding gloss on existing sense
- Bulk-removing lexeme statements (QS supports this)
- Bulk-removing form statements
- Bulk-removing sense statements
- Bulk-removing forms
- Bulk-removing senses
- Bulk-removing grammatical features on forms (WLF supports this, but the drag-n-drop possibility might not be clear to users leading to duplication of forms)
- Bulk-removing glosses on senses

On new lexemes: 
- Bulk-adding forms with 1 form representation (implemented may 2021) (WLF supports this)
- Bulk-adding forms with multiple grammatical features (implemented may 2021) (WLF supports this)
- Bulk-adding multiple form representations to a form (WLF supports this)
- Bulk-adding senses with one gloss
- Bulk-adding senses with multiple glosses
- Bulk-adding lexeme statements
- Bulk-adding form statements
- Bulk-adding sense statements

## Setup
Copy config.example.py to config.py yourself and adjust the following
content:
```
username = "username"
password = "password"
```
