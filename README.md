## email farm

this is a middleman application that generates html for emails. Only one email is setup this way at present, and that is the alabama monthly newsletter, though I planned to move all the others here.

TO DEVELOP:

clone this repository, cd to it, bundle, and run middleman. at localhost:4567 will be the root file, which is a link to the newsletter (currently).

In general, all you wil be doing is modifying the .yml file that the email is generated from, and changing the images.

TO SEND:

run `middleman build`, and collect the finished html file from the build directory. Right now, you have to zip up the images folder, I want to make a hook on build that does that automagically and plunks it on your desktop with the finished html file, but I haven't gotten to that yet.

UPDATES:

The functionality to inline CSS and send to Litmus from your dev environment has been added.

CSS
------------
When you have finished editing your email and have built the project (using `middleman build`), you can inline your CSS by running `grunt build`. This will inline the CSS in your templates and place them in the directory named 'prod'. The prod directory will have the same structure as the data and source directories.

When inlining CSS, all `style` blocks will be stripped from the header.  If you are using media queries, wrap them in a separate `style` tag and  add `data-ignore="true"` to the  tag: `<style type="text/css" data-ignore="true"`. This will keep the inliner from stripping this style block and it will not inline the styles contained in block.

Litmus
------------
To send your template to Litmus, run `grunt send --template=yourTemplatePath.html`.  The template path should be relaitve to the prod folder and should not start with a forward slash. Once you have sent the file, sign in to Litmus to view the test.