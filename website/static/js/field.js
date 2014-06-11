
$(document).ready(function(){
	
	// Je compte le nombre de champs pour créer une base d'incrémentation
	
	var nombreChamps = $('.form-control.fieldIntervenants').length;

	// J'ajoute un champs
	
	$('#plus').on('click', function(e){

		e.preventDefault();
	
		var incrementation = nombreChamps++;
	
		$('#intervenantsWrapper').append("<input class='form-control fieldIntervenants' name='intervenants"+incrementation+"' type='text' placeholder='ex : Nom - Prénom - E-mail'>");
	
	})
	
	// Je supprime le dernier champs au click sur le bouton Moins
	
	$('#moins').on('click', function(e){

		e.preventDefault();
	
		$( ".form-control.fieldIntervenants" ).remove();
	
	})

});