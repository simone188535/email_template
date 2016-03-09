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
          cwd: 'build',           // Src matches are relative to this path.
          src: ['**/*.html'],     // Actual pattern(s) to match.
          dest: 'prod/',          // Destination path prefix.
          ext: '.html',           // Dest filepaths will have this extension.
        }],
        options: {
          encodeSpecialChars: true
        }
      }
    },

    // Image Compression
    // ----------------------

    imagemin: {
      dynamic: {
        files: [{
          expand: true,
          cwd: 'build/'+grunt.option('imgpath')+'/',  // image files are relative to this path
          src: ['**/*.{png,jpg,gif}'],
          dest: 'prod/'+grunt.option('imgpath')+'/'
        }]
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
          url: 'https://gaprc.litmus.com',
          clients: ['ol2000','ol2002','ol2003','ol2007','ol2010','ol2011','ol2013','android4','androidgmailapp','ipad','iphone4','iphone5','iphone5s','iphone6','iphone6plus','chromegmailnew', 'ffgmailnew','gmailnew','chromeoutlookcom','outlookcom','ffoutlookcom']
        }
      }
    },

  });

  grunt.loadNpmTasks('grunt-email-builder');
  grunt.loadNpmTasks('grunt-litmus');
  grunt.loadNpmTasks('grunt-contrib-imagemin');
  grunt.loadNpmTasks('grunt-newer');

  // Default task(s).
  grunt.registerTask('default', ['emailBuilder']);
  grunt.registerTask('images', ['newer:imagemin']); // grunt images --imgpath=client_name/project_name/images (replative to 'prod' folder, do not include '/' after the images directory path)
  grunt.registerTask('build',   ['newer:emailBuilder']);
  grunt.registerTask('send', ['litmus']); // grunt send --template=yourtemplate.html (relative to 'prod' folder)
};