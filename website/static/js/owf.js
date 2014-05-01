(function(i, s, o, g, r, a, m) {
  i['GoogleAnalyticsObject'] = r;
  i[r] = i[r] || function() {
    (i[r].q = i[r].q || []).push(arguments)
  }, i[r].l = 1 * new Date();
  a = s.createElement(o),
      m = s.getElementsByTagName(o)[0];
  a.async = 1;
  a.src = g;
  m.parentNode.insertBefore(a, m)
})(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

ga('create', 'UA-9730554-4', 'openworldforum.org');
ga('send', 'pageview');

$('#myCarousel').bind("slide", function() {
  var img1 = $('#carousel-button-img1');
  var img2 = $('#carousel-button-img2');
  if (img1.attr('src') == '/static/pictures/ellipse-red.png') {
    img1.attr('src', '/static/pictures/ellipse-grey.png');
    img2.attr('src', '/static/pictures/ellipse-red.png');
  }
  else {
    img1.attr('src', '/static/pictures/ellipse-red.png');
    img2.attr('src', '/static/pictures/ellipse-grey.png');
  }
});
