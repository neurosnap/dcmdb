$(function() {
	
	$("#login").on("click", function() {

		login.loginState("disabled");

		login.auth($("#user").val(), $("#pass").val());

	});

});

var login = {};

login.auth = function(user, pass) {

	$.ajax({
		"url": "/users/checkLogin",
		"dataType": "json",
		"type": "POST",
		"data": {
			"user": $("#user").val(),
			"pass": $("#pass").val()
		},
		"success": function(res) {
			
			if (res.success) {
				
				$("#login_response")
					.removeClass("alert-info")
					.removeClass("alert-danger")
					.addClass("alert-success")
					.html(res.msg + '  <a href="/users/" class="alert-link">View your profile</a>');

				window.location = '/users';

			} else {
				
				$("#login_response")
					.removeClass("alert-info")
					.removeClass("alert-success")
					.addClass("alert-danger")
					.html(res.msg);

				login.loginState("enabled");
			}

		}
	});

};

login.loginState = function(state) {

	if (state == "enabled") {

		$("#login").removeAttr("disabled");
		$("#user").removeAttr("disabled");
		$("#pass").removeAttr("disabled");

	} else if (state == "disabled") {

		$("#login").attr("disabled", "disabled");
		$("#user").attr("disabled", "disabled");
		$("#pass").attr("disabled", "disabled");

	}

}