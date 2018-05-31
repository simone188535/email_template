To run Python script, cd to templates folder
Make sure there are no spaces in any of the file names.

Run this:
python createEmail.py {{client name}} {{emailname}} {{xls doc}} {{images folder}}



There's a setup.sh file with sudo pip for all the libraries we installed manually.


The script creates the logo header automatically; delete that slice from the images folder.
For SPR, enter the slice numbers in the column next to the Concatenate column.
Add a sheet to the excel doc named CUSTOM; make a single column with the number of each custom slice each in their own cell
Email name should be in the format SPR_XXXXXX_EmailName
After the script runs, double-check font colors in the Custom email; by default the script only uses black and white, and may need adjusted to match the creative.
Also, if there are more than 13 linetext items, you will need to increment them manually.
Add Auto and Custom folders to the prod folder
Copy the images folder into both; move the html files and rename both to layout1
Select the images folder and html; compress both
In SproutLoud, select New email template
Upload zip file
Add preview jpg
Select country (US is default; if you forget this for a Canada email you have to redo the entire email.)
Check the box for the footer
Copy in list of sllabels from setup.html
Save, then comment it out
Plain text—delete
Full SKU, Description, and Concatenate—copy and paste in plain text
In Component Layout, move Profile 1 to top, then sort its contents according to setup.html
Preview and testAdd address and logo (1st image in 1st folder)
For CUSTOM, same but add prices (Price1, Price2, etc.) and date
SPRID goes to:
qa@purered.net,
110215SPR@litmustest.com,
devpurered.runme@previews.emailonacid.com
GOPD, SKU, and HEADERLINK go to:
qa@purered.net