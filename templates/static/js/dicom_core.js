
/* Google Analytics */
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-18083814-3', 'dcmdb.org');
ga('send', 'pageview');
/* End GA */

$.expr[':'].external = function(obj) {
	return !obj.href.match(/^mailto\:/)
				 && (obj.hostname != location.hostname)
				 && !obj.href.match(/^javascript\:/)
				 && !obj.href.match(/^$/);
};

$(function() {

	var default_width = $("#dcm_query").parent().css("width");

	$("#dcm_query").on("focus", function() {
		$(this).parent().animate({
			"width": 500
		});
	});

	$("#dcm_query").on("blur", function() {
		$(this).parent().animate({
			"width": default_width
		});
	});

	$("a:external").each(function() {
		var link_text = $(this).html() + ' <span class="glyphicon glyphicon-new-window"></span>';
		$(this).html(link_text);
	});

	$('a:external').attr('target', '_blank');

	var csrftoken = getCookie('csrftoken');
		
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
				// Send the token to same-origin, relative URLs only.
				// Send the token only if the method warrants CSRF protection
				// Using the CSRFToken value acquired earlier
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});

	/* NAVBAR FUNCTIONALITY */
	var url = document.URL.replace("http://", "").replace("https://", "");

	var first = url.indexOf("/");
	var uri = url.substring(first, url.length);
	$(".dcm_nav").find("li").each(function() {

		if ($(this).hasClass("active"))
			$(this).removeClass("active");

		if ($(this).find("a").attr("href") == uri 
			|| $(this).find("a").attr("href") == uri.slice(0, -1))
				$(this).addClass("active");

	});
	/* END NAVBAR FUNCTIONALITY */

});

// using jQuery
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}

	return cookieValue;
}

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
	// test that a given url is a same-origin URL
	// url could be relative or scheme relative or absolute
	var host = document.location.host; // host + port
	var protocol = document.location.protocol;
	var sr_origin = '//' + host;
	var origin = protocol + sr_origin;
	// Allow absolute or scheme relative URLs to same origin
	return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
			(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
			// or any other URL that isn't scheme relative or absolute i.e relative.
			!(/^(\/\/|http:|https:).*/.test(url));
}
