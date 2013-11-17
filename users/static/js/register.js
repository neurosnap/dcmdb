$(function() {
	
	//register button
	$("#register").on("click", function(e) {

		var errors = 0;

		//prevents default behavior for an event
		e.preventDefault();

		//element that have an "error" class when input is invalid
		$(".form-group").each(function() {

			if ($(this).hasClass("error"))
				errors++;

		});

		//checks to make sure both passwords match
		if ($("#pass").val() == "" || $("#pass").val() == " ") {

			errors++;

			register.validate({ 
				"success": false, 
				"msg": "Password cannot be blank" 
			}, document.getElementById("pass"));

			register.validate({ 
				"success": false, 
				"msg": "Password cannot be blank" 
			}, document.getElementById("pass_check"));

		} else if ($("#pass").val() != $("#pass_check").val()) {

			errors++;

			register.validate({ 
				"success": false, 
				"msg": "Passwords do not match" 
			}, document.getElementById("pass"));

			register.validate({ 
				"success": false 
			}, document.getElementById("pass_check"));

		} else {

			register.validate({ 
				"success": true, 
				"msg": "Passwords match" 
			}, document.getElementById("pass"));
			
			register.validate({ 
				"success": true 
			}, document.getElementById("pass_check"));

		}

		//create the user
		if (errors == 0) {

			$.ajax({
				"url": "/users/createUser",
				"type": "POST",
				"dataType": "json",
				"data": {
					"user": $("#user").val(),
					"email": $("#email").val(),
					"pass": $("#pass").val()
				},
				"success": function(res) {
					
					if (res.success) {
				
						$("#register_response")
							.removeClass("alert-danger")
							.addClass("alert-success")
							.html(res.msg + '.  <a href="/users/login">Login!</a>');

					}

				}
			});

		}

	});
	
	//username input validation
	$("#user").on("blur", function(e) {

		var user = $("#user").val();

		var that = this;

		if (register.last_user != user) {

			$.ajax({
				"url": "/users/checkUniqueUser",
				"type": "POST",
				"dataType": "json",
				"data": {
					"user": user
				},
				"success": function(res) {

					register.last_user = user;

					register.validate(res, that);

				}
			});

		}

	});

	//email input validation
	$("#email").on("blur", function(e) {
		
		var email = $("#email").val();

		var that = this;

		if (register.last_email != email) {

			$.ajax({
				"url": "/users/checkUniqueEmail",
				"type": "POST",
				"dataType": "json",
				"data": {
					"email": email
				},
				"success": function(res) {

					register.last_email = email;

					register.validate(res, that);

				}
			});

		}

	});

});

//object literal singleton
var register = {
	"last_email": "",
	"last_user": ""
};

//CSS validation visuals, error = red, success = green and displays a message from the server
register.validate = function(data, el) {

	if (data.hasOwnProperty("success")) {

		if (data.success) {

			if (data.hasOwnProperty("msg"))
				$(el).parent().find(".help-block").html(data.msg);

			$(el)
				.parent()
				.parent()
				.removeClass("error")
				.addClass("success");

		} else {

			if (data.hasOwnProperty("msg"))
				$(el).parent().find(".help-block").html(data.msg);

			$(el)
				.parent()
				.parent()
				.removeClass("success")
				.addClass("error");

		}

	} else {

		alert("success property not found");

	}

}