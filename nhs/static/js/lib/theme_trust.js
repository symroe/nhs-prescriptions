///////////////////////////////
// Set Variables
///////////////////////////////

var gridContainer = jQuery('.thumbs.masonry');
var colW;
var gridGutter = 0;
var thumbWidth = 300;
var widgetsHidden = false;


///////////////////////////////
// Mobile Detection
///////////////////////////////

function isMobile(){
    return (
        (navigator.userAgent.match(/Android/i)) ||
		(navigator.userAgent.match(/webOS/i)) ||
		(navigator.userAgent.match(/iPhone/i)) ||
		(navigator.userAgent.match(/iPod/i)) ||
		(navigator.userAgent.match(/iPad/i)) ||
		(navigator.userAgent.match(/BlackBerry/))
    );
}

///////////////////////////////
// Project Filtering
///////////////////////////////

function projectFilterInit() {
	jQuery('#filterNav a').click(function(){
		var selector = jQuery(this).attr('data-filter');
		jQuery('#projects .thumbs').isotope({
			filter: selector,
			hiddenStyle : {
		    	opacity: 0,
		    	scale : 1
			}
		});

		if ( !jQuery(this).hasClass('selected') ) {
			jQuery(this).parents('#filterNav').find('.selected').removeClass('selected');
			jQuery(this).addClass('selected');
		}

		return false;
	});
}


///////////////////////////////
// Project thumbs
///////////////////////////////

function projectThumbInit() {

	if(!isMobile()) {
		jQuery(".project.small a").hover(
			function() {
				jQuery(this).find('.overlay').stop().fadeTo("fast", .9);
				jQuery(this).find('.description').stop().fadeTo("fast", 1);
				jQuery(this).find('img:last').attr('title','');
			},
			function() {
				jQuery(this).find('.overlay').stop().fadeTo("fast", 0);
				jQuery(this).find('.description').stop().fadeTo("fast", 0);
			});
	}

	setColumns();
	gridContainer.isotope({
		resizable: false,
		layoutMode: 'fitRows',
		masonry: {
			columnWidth: colW
		}
	});

	jQuery(".project.small").css("visibility", "visible");
	jQuery("#floatingCirclesG").fadeOut("slow");
}

///////////////////////////////////
// Theme fixed position adjustment
///////////////////////////////////
function sidebarAbsolute(firstRun) {
	var viewH = jQuery(window).height(), screenH = jQuery(document).height(), header = jQuery("#header");
	if ( header.height() > viewH && header.height() < screenH ) {
		if (firstRun) { screenH = screenH + 200; }
		header.css( { "position" : "absolute", "height" : screenH + "px" } );
	} else {
		header.attr("style", "");
	}
}

///////////////////////////////////
// Relocate Elements
///////////////////////////////////

function relocateElements()
{
	if(jQuery('#container').width() <= 768) {
		jQuery('#sidebar').insertAfter(jQuery('#content'));
		widgetsHidden = true;
	}
	else if(widgetsHidden) {
		jQuery('#sidebar').insertAfter(jQuery('#mainNav'));
	}
}

///////////////////////////////
// Isotope Grid Resize
///////////////////////////////

function setColumns()
{
	var columns;
	columns = Math.ceil(gridContainer.width()/thumbWidth);
	colW = Math.floor(gridContainer.width() / columns);
	jQuery('.thumbs.masonry .project.small').each(function(id){
		jQuery(this).css('width',colW-gridGutter+'px');
	});
}

function gridResize() {
	setColumns();
	gridContainer.isotope({
		resizable: false,
		masonry: {
			columnWidth: colW
		}
	});
}


///////////////////////////////
// Mobile Nav
///////////////////////////////

function setMobileNav(){
	jQuery('#mainNav .sf-menu').tinyNav({
	  active: 'current-menu-item'
	});
}

///////////////////////////////
// Initialize Page
///////////////////////////////

jQuery.noConflict();
jQuery(window).ready(function(){
	jQuery(".videoContainer").fitVids();
});

jQuery(window).load(function(){
	projectThumbInit();
	projectFilterInit();
	jQuery(".videoContainer").fitVids();
	//sidebarAbsolute(1);
	relocateElements();
	setMobileNav();
	jQuery("#filterNav").find("a").eq(0).click(); // TODO find a fix without this code
	jQuery(window).smartresize(function(){
		gridResize();
		sidebarAbsolute();
		relocateElements();
	});
});