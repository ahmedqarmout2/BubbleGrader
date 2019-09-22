# BubbleGrader

## Contents

0. [Introduction](#introduction)
1. [Screenshots](#screenshots)
2. [Setup](#setup)
3. [Instructions](#instructions)

## Introduction
Program used to generate bubble sheets for grading, as well as scanning those bubble sheets and exporting the marks into digestable formats.

## Screenshots

## Setup
0. Start by cloning the repository.
```
git clone https://github.com/ahmedqarmout2/BubbleGrader.git
```
1. Navigate to the web application directory.
```
cd BubbleAnalyser
```
2. Install the required dependencies.
```
pip install -r requirements.txt
```

## Instructions
0. Start the web application.
```
python server.py
```
1. Go to the web application from a browser by visiting the following link:
```
http://localhost:5000
```
2. Create a new project
![New Project Image](/Screenshots/newproject.png?raw=true "New Project Image")
3. Enter the maximum length of the student number (up to 10 digits), and the number of questions you want to be marked (up to 10 questions). Then click the update button to generate a marking sheet.

![Marking Sheet Image](/Screenshots/markingsheet.png?raw=true "Marking Sheet Image")