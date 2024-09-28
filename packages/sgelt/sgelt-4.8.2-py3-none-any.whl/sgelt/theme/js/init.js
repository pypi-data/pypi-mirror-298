(function ($) {
  $(function () {

    $('.sidenav').sidenav();
    $('.dropdown-trigger').dropdown();
    $('.modal').modal();
    $('.materialboxed').materialbox();
    $('.collapsible').collapsible();
    $('.tabs').tabs();
    $('.carousel').carousel();
    $('.carousel.carousel-slider').carousel({
      fullWidth: true,
      indicators: true,
      duration: 200
    });
    autoplay();
    function autoplay() {
      $('.carousel').carousel('next');
      setTimeout(autoplay, 8000);
    }
  }); // end of document ready
})(jQuery); // end of jQuery name space

function CopyToClipBoard(toast_text) {

  const text = document.getElementById('content_to_copy').innerText;
  navigator.clipboard.writeText(text);
  M.toast({html: toast_text})

}