/*
add livereload to repo branch
auto generae text version
table of contents
dependent args
****** Requires npm 3.3.12+ ******
*/

/* Load plugins */
var gulp 			= require('gulp'),
	imagemin 		= require('gulp-imagemin'),
	livereload 		= require('gulp-livereload'),
	notify 			= require('gulp-notify'),
	plumber 		= require('gulp-plumber'),
	rename 			= require('gulp-rename'),
	builder 		= require('gulp-email-builder'),
	newer			= require('gulp-newer'),
	yargs			= require('yargs').argv,
	litmus 			= require('gulp-litmus'),
	path_replace 	= require('gulp-replace'),
	cache        	= require('gulp-cache'),
	copy 			= require('gulp-copy'),
	zip				= require('gulp-zip'),
	run_sequence	= require('run-sequence'),
	html2txt 		= require('gulp-html2txt'),


/* Title for Gulp notification */
notify_info = {
  title: 'Gulp'
},

/* Error notification settings for plumber */
plumberErrorHandler = { errorHandler: notify.onError({
    title: notify_info.title,
    message: "Error: <%= error.message %>"
  })
},

/* Directory path defaults */
base_path = {
	prod: 		'prod/',
	build: 		'build/',
	litmus: 	'litmus/',
	src_files: 	'source/',
	data_files: 'data/'
},

/* ---- CLI Params ----- */

/*
* Path to image directory referenced by specified template's image src paths
* Relative to 'build' directory 
*/
imgdir 			= yargs.imgdir ? yargs.imgdir : '',

/*
* Path to HTML template file to send to litmus
* File xtension required
* Relative to 'litmus' directory
*/
sendfile 		= yargs.sendfile ? base_path.litmus + yargs.sendfile : '',

/*
* Path to template file in which the image src paths should be switch out
* File extension required
* Relative to 'prod' directory
*/
swappaths 	= yargs.swappaths ? base_path.prod + yargs.swappaths : '', 
/* Helper - path to directory that the resulting file will be saved, relative to 'litmus' directory */
litmusdest 		= yargs.swappaths ? base_path.litmus + yargs.swappaths.substring(0, yargs.swappaths.lastIndexOf('/')) : '',

/*
* Path to HTML template file to convert to a plain text version
* File extension required
* Relative to 'prod' directory
*/
txtconvert = yargs.txtconvert ? base_path.prod + yargs.txtconvert : '',
/* Helper - slices provided directory path string */
txtdir = yargs.txtconvert ? base_path.prod + yargs.txtconvert.substring(0, yargs.txtconvert.lastIndexOf('/')) : '',

/*
* Path to the image directory referenced by the specified template's image src paths
* Relative to the 'prod' directory
*/
zipimages 		= yargs.zipimages ? base_path.prod + yargs.zipimages : '',

/*
* Path to directory of specifed template to be zipped for production
* Relative to 'prod' directory
*/
zipdir 			= yargs.zipdir ? base_path.prod + yargs.zipdir : '',
/* Helper - slices provided directory path string */
zipslice 		= yargs.zipdir ? yargs.zipdir.split('/') : '';
/* Helper - name of the generated zip file */
zipname 		= zipslice[zipslice.length - 1] + '.zip',


/* Build task configuration */
build_config = {
	encodeSpecialChars: true,
},

/* Litmus task configuration */
litmus_config = {
	username: 'andy.hardy@purered.net',
	password: 'pur3r3d_qa',
	url: 'https://gaprc.litmus.com',
	applications: ['ol2000','ol2002','ol2003','ol2007','ol2010','ol2011','ol2013','android4','androidgmailapp','ipad','iphone4','iphone5','iphone5sios8','iphone6','iphone6plus','chromegmailnew', 'ffgmailnew','gmailnew','chromeoutlookcom','outlookcom','ffoutlookcom', 'notes85', ] // Clients to test in litmus
};

/**
 * Build Emails for Production
 * ---------------------------------------------
 * Generates all email templates for production
 * 
 * Inline CSS (preserving media queries)
 * 
 * Encode symbols to HTML entites
 * 
 * Save updated files in 'prod' directory
 *
 * Example: $ gulp build
 * 
 */

gulp.task('build', function(){
	gulp.src(['build/**/*.html'])
		.pipe(plumber(plumberErrorHandler))
		.pipe(builder(build_config))
		.pipe(gulp.dest(base_path.prod))
		.pipe(notify({ message: 'Build task complete' }));
});

/**
 * Send Email to Litmus
 * --------------------------------------------------------------------------
 * Sends specified file (relative to 'litmus' directory) to litmus
 *
 * ***************************************************************************
 *
 * @sendfile: Path to template file to be send to litmus. Relative to 
 * 			  'litmus' directory
 *
 * Example: $ gulp litmus --sendfile=client/templDir/templFile.html
 *
 */

gulp.task('litmus', function(){
	return gulp.src(sendfile)
		.pipe(plumber(plumberErrorHandler))
		.pipe(litmus(litmus_config));
});

/**
 * Replace Image Paths for Litmus Testing
 * -----------------------------------------------------------------
 * Replaces relative image src path with QA server image src path
 * 
 * 
 * src path is relative to the 'build' directory on the QA server 
 * (http://proof.gaprc.org/build/)
 * 
 * Required directory structure: image directory should be located 
 * in directory above the specified template's directory 
 * Ex: clientDir/imgDir/templateDir
 * 
 * Expects relative img src path to be '../images'
 *
 * Saves resulting files in the 'litmus' directory
 *
 * ******************************************************************
 * 
 * @swappaths:  Path to template in which image src paths will be changed. 
 *                 Relative to 'litmus' directory
 *                 
 * @imgdir: Path to the image directory referenced by the specified template's 
 * 			image src paths. Relative to 'build' directory
 *
 * Ex: $ gulp replacepath --swappaths=client/templDir/templFile.html --imgdir=client/images
 * 
 */

gulp.task('replacepath', function(){
	return gulp.src([swappaths])
		.pipe(plumber(plumberErrorHandler))
		.pipe(path_replace('src="../images', 'src="http://proof.gaprc.org/build/' + imgdir))
		.pipe(gulp.dest(litmusdest))
		.pipe(notify({ message: 'Image path replacement task complete' }));
});

/*
 * Optimize/Compress Images 
 * ------------------------------------------------------------------------------
 * Optimizes all images in the 'build' directory and copys the resulting files 
 * to the 'prod' directory
 *
 * Example: 
 * $ gulp compress
 *
 * TODO - only optimize images that have changed since the last time the task ran
 * 
 */

gulp.task('compress', function(){
		return gulp.src(['build/**/*.jpg', 'build/**/*.gif'], {base: 'build'})
		.pipe(plumber(plumberErrorHandler))
		.pipe(imagemin())
		.pipe(gulp.dest('prod'));
});

/*
 * Copy All Images to 'prod' Directory
 * ------------------------------------------------------------------------------
 * Copies all images in the 'build' directory to the 'prod' directory
 *
 * Example: $ gulp copy
 * 
 */

gulp.task('copy', function(){
	return gulp.src([base_path.build + '**/*.jpg', base_path.build + '**/*.gif'], {base: 'build'})
		.pipe(gulp.dest('prod'));
});

/*
 * Zip Template Files for Production
 * ------------------------------------------------------------------------------
 * Zips the HTML, text and images image files of the specified template
 *
 * Required directory structure: image directory should be located 
 * in directory above the specified template's directroy 
 * Ex: clientDir/imgDir/templateDir
 *
 * The zip file is saved in the specified template's directory under the 
 * 'prod' directory
 *
 * ******************************************************************************
 *
 * @zipdir: Path to the template to zip. Relatve to 'prod' directory
 * @zipimages: Path to the image directory referenced by the specifed in 
 * 			   template's image src paths
 *
 * Ex: $ gulp zip --zipdir=client/templDir/templFile.html --zipimages=client/images
 *
 */

gulp.task('zip', function(){
	return gulp.src([zipimages + '/*', zipdir + '/*.html', zipdir + '/*.txt'], {base: 'prod'})
		.pipe(zip(zipname))
		.pipe(gulp.dest(zipdir))
		.pipe(notify({ message: 'Zip task complete' }));
});

/*
* Generate Plain Text Version of Email
* ---------------------------------------------------------------
* Generates a plain text version of the specified template
*
* The generated .txt file is safed to the specified template's 
* directory under the 'prod' directory
*
* NOTE: It's a little sloppy. A good tool to use for the initial 
* .txt file, but it will require a decent amount of editing if
* specific requirements are needed.
*
* *****************************************************************
*
* @txtconvert = Path to template to convert to text. Relative to 
*             	the 'prod' directory. Requires file extension.
* 
*/

gulp.task('htmltotxt', function(){
	gulp.src(txtconvert)
		.pipe(html2txt())
		.pipe(gulp.dest(txtdir));
});


gulp.task('watch', function(){
	gulp.watch([base_path.src_files + '**/*.erb', base_path.src_files + '**/*.yml'], ['build']);
});

/* ---- Gulp Tasks ---- */
gulp.task('default', ['build']);
gulp.task('build', ['build']);



/* ---- Combined Tasks ---- */
gulp.task('litmusbuild', function(callback){
	run_sequence('build', 'replacepath', 'litmus', callback);
});
/* Ex: $ gulp litmusbuild --sendfile=clientDir/templDir/templFile.html --swappaths=clientDir/templDir/templFile.html --imgdir=clientDir/images */

gulp.task('compressbuild', function(callback){
	run_sequence('build', 'copy', 'compress', callback);
});
/* Ex: $ gulp compressbuild */