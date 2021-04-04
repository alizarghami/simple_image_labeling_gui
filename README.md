# Simple Image Labeling GUI

### Introduction

This is a simple python program that assists the user with labeling groups of images.
Each group of images should be placed in a separate folder. The program creates an excel file for each group and cycles through them and helps the user with the frustrating job of labeling.

### Getting Started

In order to use this code you just need to have the following requirements installed:
* **Python 3.6** or above
* **Numpy**
* **Pandas**
* **pandastable**
* **TKInter**

pandastable can be installed by the following command:

`
pip install pandastable
`

### Instructions

In order to use the program, run `app.py`.

* Click on `Browse` button to specify the location of the images.

* Use `Previous` and `Next` buttons to cycle between groups of images.

* Write the desired label in the provided text box and click `Submit & Next` to submit the label and show the next image. Use `Back` button to go back to the previous image.

* You can see your progress in the provided pandas table. You can also cycle between images by clicking on the image names in the pandas table.

* The program has Auto-save feature in different stages but you can save your progress manually whenever you want by clicking on `save` button.