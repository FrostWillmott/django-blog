console.log('sign-up')
$(function () {
  $('#signUpForm').submit(signUp);
});

function signUp(e) {
  let form = $(this);
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      alert('Sign-up successful!');
      location.reload();
    },
    error: function (data) {
      // $("#emailGroup").addClass("has-error");
      // $("#passwordGroup").addClass("has-error");
      // $(".help-block").remove();
      // $("#passwordGroup").append(
      //   '<div class="help-block">' + data.responseJSON.email + "</div>"
      // );

    }
  });
}
