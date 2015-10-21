module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    // Email Builder
    // ----------------------

    emailBuilder: {
      test :{
        files: [{
          expand: true,           // Enable dynamic expansion.
          cwd: 'build',        // Src matches are relative to this path.
          src: ['**/*.html'],        // Actual pattern(s) to match.
          dest: 'prod/',     // Destination path prefix.
          ext: '.html',           // Dest filepaths will have this extension.
        }],
        options: {
          encodeSpecialChars: true
        }
      }
    },

     // Litmus testing
    // ----------------------

    // Test in all Outlook clients
    litmus: {
      test: {
        src: ['prod/'+grunt.option('template')],
        options: {
          username: 'andy.hardy@purered.net',
          password: 'pur3r3d_qa',
          url: 'https://litmus.com',
          clients: ['ol2000','ol2002','ol2003','ol2007','ol2010','ol2011','ol2013','android4','androidgmailapp','ipad','iphone4','iphone5','iphone5s','iphone6','iphone6plus','chromegmailnew', 'ffgmailnew','gmailnew','chromeoutlookcom','outlookcom','ffoutlookcom']
        }
      }
    },

  });

  grunt.loadNpmTasks('grunt-email-builder');
  grunt.loadNpmTasks('grunt-litmus');
  grunt.loadNpmTasks('grunt-newer');

  // Default task(s).
  grunt.registerTask('default', ['emailBuilder']);
  grunt.registerTask('build',   ['newer:emailBuilder']);
  grunt.registerTask('send', ['litmus']); // grunt send --template=yourtemplate.html (relative to 'prod' folder)
};