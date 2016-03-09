## email farm

this is a middleman application that generates html for emails. Only one email is setup this way at present, and that is a sample responsive email.

TO DEVELOP:

clone this repository, cd to it, bundle, and run middleman. at localhost:4567 will be the root file, which is a link to the newsletter (currently).

```
NOTE: Prerequisites:
* Node - https://docs.npmjs.com/getting-started/installing-node
* Ruby - ruby 2.0.0p481 (2014-05-08 revision 45883) [universal.x86_64-darwin14]
* Bundler - version 1.10.6
* Grunt - "npm install -g grunt-cli"
* Middleman - bundle install middleman

SETUP:
1. 
```

In general, all you wil be doing is modifying the .yml file that the email is generated from, and changing the images.

When creating files use the following structure: 

In the source directory: 

HTML email: client_name/project_name/project_name.html.erb

Text email: client_name/project_name/project_name.txt.erb

Image directory: client_name/project_name/images

In the data directory: client_name/project_name/project_name.yml

Do not use dashes (-) when naming folders or directories, use an underscore instead (_)


CSS
------------
When you have finished editing your email and have built the project (using `middleman build`), you can inline your CSS by running `grunt build`. This will inline the CSS in your templates and encode any HTML entites and place the file in the directory named 'prod'. The prod directory will have the same structure as the data and source directories.

When inlining CSS, all `style` blocks with the attribute `data-embed` will be stripped from the header.  If you are using media queries, wrap them in a separate `style` tag and  add `data-embed-ignore"` to the  tag: `<style type="text/css" data-ignore="true"`. This will keep the inliner from stripping this style block and it will not inline the styles contained in block.

Litmus
------------
To send your template to Litmus, run `grunt send --template=yourTemplatePath.html`.  The template path should be relaitve to the prod folder and should not start with a forward slash. Once you have sent the file, sign in to Litmus to view the test.

Litmus Credentials:

User: andy.hardy@purered.net

Pass: pur3r3d_qa
