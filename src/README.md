# README
Input "python3 expression_tree.py" into the CODIO terminal.
The program offers a menu interface with basic input checking.
If your input has invalid expressions, it'll prompt you with a INVALID message and tell you what to input.

From the Tree class to the "Expression validity checking" below represents chapter 8 of the Goodrich Python Algorithm Book,
the code is taken from the publisher's textbook repository - https://bcs.wiley.com/he-bcs/Books?action=chapter&bcsId=8028&itemId=1118290275&chapterId=88988 .
This app is submitted as a single module to remove the dead code that isnt used.
Original code ultilized the method of using multiple inherited modules which results in muliple python modules which isn't needed for the assessment.

## ---Testing the app---
  Unit testing can be done via the main menu option 'test', once tests are finished the app will close
  and you will need to restart the app again if you wish to use the other features.

##  - Notes -
  -> Saved/Loaded files must be in the same directory when executing app.
  -> Expressions should not have whitespace inside them.
  -> The operator '*' can also be substituted for 'x' and does the exact same operation.  Example 3 * 2 = 6, 3 x 2 = 6.
  -> Take care that your minus operator are the ones exactly like in the OPERATORS variable.

##  - Pickle Notes -
  -> Two .pickle files are added to the directory for loading use.  However you can also create new .pickles by saving them.