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

ga('create', 'UA-9730554-4', 'openworldforum.paris');
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

/*** ajouter ou supprimer un champ pour le formulaire ***/

$(document).ready(function() {
  // Je compte le nombre de champs pour créer une base d'incrémentation
  var nombreChamps = $('.form-control.fieldIntervenants').length;

  // J'ajoute un champs
  $('#plus').on('click', function(e) {
    e.preventDefault();
    var incrementation = nombreChamps++;
    $('#intervenantsWrapper').append("<input class='form-control fieldIntervenants' title='intervenants" + incrementation + "' name='intervenants" + incrementation + "' type='text' placeholder='ex : Nom - Prénom - E-mail'>");
  })

  // Je supprime le dernier champs au click sur le bouton Moins

  $('#moins').on('click', function(e) {
    e.preventDefault();
    $(".form-control.fieldIntervenants:last-child").remove();
  })

});

/* Mozilla persona */
$(document).ready(function() {
  var signinLink = document.getElementById('persona-signin');
  if (signinLink) {
    signinLink.onclick = function() {
      navigator.id.request();
    };
  }

  var signoutLink = document.getElementById('persona-signout');
  if (signoutLink) {
    signoutLink.onclick = function() {
      navigator.id.logout();
    };
  }

  navigator.id.watch({
    loggedInEmail: $CURRENT_USER,
    onlogin:       function(assertion) {
      // Un utilisateur est connecté ! Voici ce qu'il faut faire :
      // 1. Envoyer l'assertion à votre backend pour vérification et pour créer la session.
      // 2. Mettre à jour l'interface utilisateur.
      $.ajax({
        type:    'POST',
        url:     $PERSONA_ROOT + '/login', // L'URL sur votre site web.
        data:    {assertion: assertion},
        success: function(res, status, xhr) {
          window.location.reload();
        },
        error:   function(res, status, xhr) {
          alert("login failure" + res);
        }
      });
    },
    onlogout:      function() {
      // Un utilisateur s'est déconnecté ! Voici ce qu'il faut faire :
      // Détruire la session de l'utilisateur en redirigeant l'utilisateur ou en appelant votre backend.
      $.ajax({
        type:    'POST',
        url:     $PERSONA_ROOT + '/logout', // L'URL sur votre site web.
        success: function(res, status, xhr) {
          window.location.reload();
        },
        error:   function(res, status, xhr) {
          alert("logout failure" + res);
        }
      });
    }
  });
});


/*
 * Image flipboard for 2013
 */
function setupFlipboard() {
  if (!$('.flipboard').length) {
    return;
  }
  active_board = new Flipboard();
  active_board.setup();

  $('.flipboard').bind('inview', function(event, visible) {
    if (visible == true) {
      active_board.start();
    }
    else {
      active_board.stop();
    }
  });
}

function main() {
  setupFlipboard();
}

$(main);
