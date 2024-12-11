# Project Description
This repository contains a implementation of a Lexical Analyzer for OWL (Web Ontology Language) using Python. The project is part of the course of Compilers at the Universidade Federal Rural do Semi-Árido (UFERSA).


# System Usage
The setup and running instructions are pretty straightforward. You can follow the steps below to get the project up and running.

## Setup
All the requirements are in the `requirements.txt` file. To install them, run the following command:
```
pip install -r requirements.txt
```
After intalling the requirements, you can put the **OWL code** you want to analyze in the `owl_files/` folder. The file must be named with an `.owl` or `.txt` extension.

## Running the Project
The "Run" button of your IDE might not work properly as the relative paths could be different.
To run the project, you can execute the `main.py` file using the terminal: 
1. First, navigate to `/src` folder:
```
cd src
```
2. Then, run the python file:
```
python src/main.py
```

## Usage
The program is a TUI (Text User Interface) that will guide you through the process of analyzing an OWL file.

The first menu gives you 3 options:
1. **Analyse File** - This option will list the valid files inside `/owl_files` and ask you to choose one to analyze.
2. **Export Report** - After analyzing a file, you can export the report to a `.txt` file.
3. **Exit**

Note that the export option will only work after analyzing a file.


# Project Structure
The project is structured as follows:
```
.
├── docs
│   ├── class_diagram.png
├── owl_files
│   ├── example.owl
│   └── example2.txt
├── reports
│   └── example_report.txt
├── src
│   ├── LexicalAnalyser.py
│   ├── main.py
│   ├── SymbolTable.py
│   └── Token.py
├── requirements.txt
├── .gitignore
└── README.md
```