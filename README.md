# email farm

This is a middleman application that generates html for emails. You can view example emails and there setup under the data/examples and source/examples folder.

All responsive emails use the Antwort Responsive Layouts for Email (http://internations.github.io/antwort/).  The framework supports the all email clients and is one of the few that can handle older versions of Android as well as Outlook and Lotus Notes.

## TO DEVELOP:

clone this repository, cd to it, bundle, and run middleman. at localhost:4567 will be the root file, which is a link to the newsletter (currently).


## NOTE: Prerequisites:
* Node - https://docs.npmjs.com/getting-started/installing-node
* Ruby
* Bundler
* Grunt - `npm install -g grunt-cli`
* Middleman - `bundle install middleman`

---------------------------------------

To build the email files, run `middleman build` (or `bundle exec middleman build`) from the root of this repository.
__NOTE:__ This will build ALL emails from all projects because Middleman is a static site compiler.
__ALSO NOTE:__ middleman commands might need to be preceeded by `bundle exec` on some systems.

To view the emails in your browser, run `middleman server`. Then browse to http://localhost:4567/client_name/project_name/project_name.html

In general, all you wil be doing is modifying the .yml file that the email is generated from, and changing the images.

When creating files use the following structure: 

In the source directory: 

* HTML email: `client_name/project_name/project_name.html.erb`

* Text email: `client_name/project_name/project_name.txt.erb`

* Image directory: `client_name/project_name/images`

* In the data directory: `client_name/project_name/project_name.yml`

Do not use dashes (-) when naming folders or directories, use an underscore instead (_)

Images
------------
To minify/optimize images in a project folder, use the following command: 

`grunt images --imgpath=client_name/project_name/images`

_OR_

`grunt bob --path=source/client_name/project_name`

__NOTE:__ requiring `source` as part of the `path` argument allows tab-completion of file and directory names!



CSS
------------
When you have finished editing your email and have built the project (using `middleman build`), you can inline your CSS by running `grunt build`. This will inline the CSS in your templates and encode any HTML entites and place the file in the directory named 'prod'. The prod directory will have the same structure as the data and source directories.

To inline CSS for a single email (instead of all), use:
`grunt single --path=build/client_name/project_name`
__REMEMBER:__ requiring `build` in the `path` argument allows tab completion of those long and finicky file and directory names!

When inlining CSS, all `style` blocks with the attribute `data-embed` will be stripped from the header.  If you are using media queries, wrap them in a separate `style` tag and  add `data-embed-ignore` to the  tag: `<style type="text/css" data-embed-ignore`. This will keep the inliner from stripping this style block and it will not inline the styles contained in block.

Litmus
------------
To send your template to Litmus, run `grunt send --template=yourTemplatePath.html`.  The template path should be relaitve to the prod folder and should not start with a forward slash. Once you have sent the file, sign in to Litmus to view the test.

Litmus Credentials:

User: {- andy.hardy@purered.net -} {+ thomas.kosko@purered.net +}

Pass: pur3r3d_qa
