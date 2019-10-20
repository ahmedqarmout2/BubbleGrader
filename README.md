# BubbleGrader

## Contents

0. [Introduction](#introduction)
1. [Setup](#setup)
2. [Instructions](#instructions)

## Introduction
Program used to generate bubble sheets for grading, as well as scanning those bubble sheets and exporting the marks into digestable formats.

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
![Project Image](/Screenshots/project.png?raw=true "Project Image")

2. Create a new project.
![New Project Image](/Screenshots/newproject.png?raw=true "New Project Image")

3. Enter the maximum length of the student number (up to 10 digits), and the number of questions you want to be marked (up to 10 questions). Then click the "UPDATE" button to  save your change and generate a marking sheet.
![Marking Sheet Image](/Screenshots/markingsheet.png?raw=true "Marking Sheet Image")

4. Add the marking sheet to the front page of your exam sheet.
![PDF Sample Sheet Image](/Screenshots/pdfSample.png?raw=true "PDF Sample Sheet Image")

5. Export your front page of your exam sheet as a pdf file, then upload it to the web application by clicking the "UPLOAD SAMPLE" button.
![Upload Sheet Image](/Screenshots/uploadsheet.png?raw=true "Upload Sheet Image")

6. Upload your class list as a csv.
![Upload Class List Image](/Screenshots/uploadclasslist.png?raw=true "Upload Class List Image")
Your class list file must contain the following columns:
"student number", "username", "first name", "last name"
![Class List File Image](/Screenshots/classlistfile.png?raw=true "Class List File Image")
![Class List File Image](/Screenshots/classlist.png?raw=true "Class List Image")

7. Enter the web application information into the phone application.
![Phone App Image](/Screenshots/phoneApp.png?raw=true "Phone App Image")

8. Take a photo of the paper. Be careful, shadows and blurriness can cause issues. Make sure the paper is on a flat surface with a dark color.
![Paper Image](/Screenshots/paperPhoto.png?raw=true "Paper Image")

Note: Refresh the page to see any updates in the marking list. If the web application had issues detecting the marks in the photoes you uploaded, iteams will appear on the "Error List" section. You can manually enter the marks for the problematic photoes.
![Error List Image](/Screenshots/errorList1.png?raw=true "Error List Image")
![Error List 2 Image](/Screenshots/errorList2.png?raw=true "Error List 2 Image")