twh_parser

(c) Michael Perkins, 2023, 2024

## Introduction/usage

Parses exported files from TroopWebHost, into YAML/TOML/JSON format or for use in Python projects. Also hooks into the objexplore browser for data checking/viewing. 

## Installation

pip install twh-parser

## Instructions:

In troopwebhost

YAML can be read in python with: 

    import yaml

    with open('output.yaml') as f:

        scouts = yaml.safe_load(f)


## Using twh_parser in code:

    from twh_parser import Parser

    #initializing the parser automatically parses the file and stores
    #the information in TmParser().scouts
    parser = TmParser(infile='filename.pdf')


    # Iterating on the parser yields scouts
    for scout in parser:
        print('----------------------------------------------')
        print(f"{scout['Data']['Name']:26}Date       Eagle Req")
        print('----------------------------------------------')
        ## do something with scout
        if "Merit Badges" in scout:

            #sort merit badges by date ascending
            for badge, data in sorted(scout['Merit Badges'].items(), 
                                        key=lambda x: x[1]['date']):
                print(f"{badge:26}{data['date']} {data['eagle_required']}")


Yields:

    ----------------------------------------------
    Smith, John               Date       Eagle Req
    ----------------------------------------------
    Climbing                  2017-03-11 False
    Mammal Study              2017-06-29 False
    Leatherwork               2017-06-30 False
    Swimming                  2017-06-30 True
    Kayaking                  2018-06-29 False
    Wilderness Survival       2018-06-29 False
    Rifle Shooting            2018-06-29 False
    First Aid                 2018-09-29 True

By default the information is a dictionary, with the scout names as keys, and each scout is a dictionary with the following keys:
- Data - contains biographical data
- Merit Badges
- Partial Merit Badges
- Rank Advancement

All dates have been parsed into datetime.date objects, in YYYY-MM-DD format, and are null if not assigned in the incoming data. 
