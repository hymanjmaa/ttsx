/**
 * Created by python on 17-8-2.
 */
$(function () {
    var error_name = false;
    var error_pwd = false;

    $('.name_input').blur(function() {
		check_user_name();
	});

	$('.pass_input').blur(function() {
		$('.pass_input').next().hide();
	});

	function check_user_name() {
        var len = $('.name_input').val().length;

        if (len<5||len>20){
            $('.name_input').next().html('请输入5-20个字符的用户名');
            $('.name_input').next().show();
            error_name = true
        }
        else {
            $('.name_input').next().hide();
            error_name = false;
        }

    }

    function check_pwd() {
        var len = $('.pass_input').val().length;

        if (len < 8 || len > 20) {
            $('.pass_input').next().html('密码最少8位，最长20位');
            $('.pass_input').next().show();
            error_pwd = true
        }
        else {
            $('.pass_input').next().hide();
            error_pwd = false;
        }

    }

    $('#login_form').submit(function() {
		check_user_name();
		check_pwd();

		if(error_name == false && error_pwd == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});

})