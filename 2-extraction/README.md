# The filtering and extraction module of GeoTweet

Requirements: python2.7*, langid if user-level language identification is run

## Filtering

For filtering before starting the analysis for now there is only the ```filter_by_user.py``` script available which runs the lang_id language identifier on a concatenation of all texts of a user. All users satisfying the set language criterion are added to the ```users.pickle``` file and only those users are considered when extracting variables.

## Extraction

For defining the extraction process you should edit the ```config.py``` file.

There are three variable extraction phases:
- extraction of any metadata from the Status (as obtained through tweepy) object, list of functions is defined in ```config.EXTRACTION_STATUS```
- linguistic variable extraction from original text, list of functions is defined in ```config.EXTRACTION_TEXT```
- linguistic variable extraction from normalised text, list of functions is defined in ```config.EXTRACTION_NORMALISED```

How the text is normalised is defined in the ```config.normalise``` function.

There are two main types of functions for extracting linguistic variables: ```lexicon_choice``` and ```regex_choice```.

The ```lexicon_choice``` function uses one of the lexical resources placed in the ```resources/``` folder. Each lexical resource consists of one entry per line, two tab-separated values, the first being the token of interest, the second being the value of the linguistic variable. If in a text tokens covering more than one value of the linguitic variable are found, the ```NA``` value is returned, same as if no token was found in the defined resource.

The ```regex_choice``` function works on the same principles as the ```lexicon_choice``` function, but not with lists of tokens, but with regular expressions mapped to the value of the linguistic variable.

The output file, with the path defined in ```config.TSV```, contains the tweet id, screen name, longitude, latitude and text attribute after which the user-defined attributes are added by the order as they are defined.

The output file is a simple tab-separated file with newlines and tabs removed from any attribute value.
