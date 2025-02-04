console.log('confirm_email');
$(function () {
  $('#confirm_email').submit(confirm_email);
});

function confirm_email(e) {
  let email = $(this);
  e.preventDefault();
  $.ajax({
    url: email.attr("action"),
    type: "POST",
    dataType: 'json',
    data: email.serialize(),
    success: function () {
      alert('Email confirmed!');
      location.reload();
    },
    error: function (data) {
    }
  });
}
