/*! 

Constant Contact: Get Image URLs


How to use:

* upload images to Constant Contact
# select "Thumb Strip View" (the middle view option)
* open browser console while the image preview modal is still open
* update the variable 'tracker' to be enough of the image filename pattern to uniquely identify images for a single email
* copy and paste updated JS into browser console and press enter (or return)
* copy the image file names from the console

*/

// update tracker to be specific to your email!
var tracker = '0330_KF_WeeklyEmail_HOBO';
var $thumbs = jQuery('.image*-title[title^=' + tracker + ']');
var out = '';

$thumbs.each(function( i, item ){ 
	var $this = $thumbs.eq( i );
	var $img = $this.siblings( '.image-thumb-wrap' ).find( 'img' );
	var title = $this.attr('title');
	var url = $img.attr('src').replace( '-thumbnail.', '.' );

	// build the string backwards so the images output in numeric order
	out = title + '\n' + url + '\n\n' + out;
	// console.log( '%s: %s', title, url );
});

console.log( 'out:' );
console.log( out );

