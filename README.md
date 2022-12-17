# Mathematical Modelling of Misinformation Spreading via Twitter

### Authors

* Rokas Kasperavicius
* Alona Konstantinova
* Dinu Cojocaru

### Directory layout
    Directories                                       Explanations
    ------------------------------------------------------------------------------------------------------------
    .
    ├── code                                          # Python files
    │   └── main.ipynb                                      # ODE-based parameter fitting + networks
    ├── data                                          # Twitter data
    │   ├── trump_chanting_verified.csv
    │   ├── judicial_watch_alleges_[...].csv
    │   ├── machines_westmoreland_m[...].csv
    │   └── ballot_harvesting_resed[...].csv
    ├── images                                        # Graph images
    │   ├── [...].png
    │   ├── trump
    │   ├── judicial
    │   ├── machines
    │   └── ballot
    ├── server                                        # Everything for the dedicated server compiling
    │   ├── script.py                                       # Example of a script for the server
    │   └── data                                            # Processed csv outputs from the server
    │       ├── trump
    │       ├── judicial
    │       ├── machines
    │       └── ballot
    ├── .gitignore
    ├── CITATION.cff
    ├── LICENSE
    └── README.md
