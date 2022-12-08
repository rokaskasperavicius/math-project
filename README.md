# Mathematical Modelling of Misinformation Spreading via Twitter

### Directory layout
    Directories                                       Explanations
    ------------------------------------------------------------------------------------------------------------
    .
    ├── images                                        # Graph images
    │   └── [...].png
    ├── code                                          # Python files
    │   └── fitting.ipynb                                  # ODE-based parameter fitting + networks
    │   ├── random_graphs.ipynb                            # Random graphs outside ODEs and Networks
    ├── data                                          # Twitter data
    │   ├── trump_chanting_verified.csv
    │   ├── judicial_watch_alleges_[...].csv
    │   ├── machines_westmoreland_m[...].csv
    │   └── ballot_harvesting_ilhan[...].csv
    ├── server                                       # Everything for dedicated server compiling
    │   ├── script.py                                      # Script for running computationally extensive network simulations
    │   └── data                                           # csv outputs
    │       ├── trump_simulation.csv
    │       ├── judicial_simulation.csv
    │       ├── machines_simulation.csv
    │       └── ballot_simulation.csv
    ├── CITATION
    ├── LICENSE
    ├── README.md
    └── .gitignore
