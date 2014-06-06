title : Student Demo Cup
date: 2014/10/30

#Open World Forum

Appel à la candidature.


<form role="form" action="remerciement.md">

	<h3>Porteur du projet </h3>
  	<div class="form-group col-md-6">
	    <label for="nom">Nom</label>
	    <input type="text" class="form-control" id="nom" placeholder="Votre nom">
  	</div>
  	<div class="form-group col-md-6">
	    <label for="prenom">Prénom</label>
	    <input type="text" class="form-control" id="prenom" placeholder="Votre prénom">
  	</div>
  	<div class="form-group col-md-6">
	    <label for="mail">E-mail </label>
	    <input type="email" class="form-control" id="mail" placeholder="Votre e-mail">
  	</div>
  	<div class="form-group col-md-6">
	    <label for="telephone">Téléphone</label>
	    <input type="text" class="form-control" id="telephone" placeholder="Votre téléphone">
  	</div>

	<h3>Catégories</h3>
	<div class="form-group col-md-12">
	  	<div class="checkbox-inline">
		  <label>
		    <input type="checkbox" id="think" value="think" checked>
		    Think
		  </label>
		</div>
		<div class="checkbox-inline">
		  <label>
		    <input type="checkbox" id="code" value="code">
		    Code
		  </label>
		</div>
		<div class="checkbox-inline">
		  <label>
		    <input type="checkbox"id="experiment" value="experiment">
		    Experiment
		  </label>
		</div>
	</div>

	<h3>Informations</h3>
	<div class="form-group col-md-12">
	    <label for="etablissement">Etablissement / entreprise </label>
	    <input type="text" class="form-control" id="etablissement" placeholder="Votre établissement/entreprise">
	</div>
	<div class="form-group col-md-12" id="intervenantsWrapper">

	    <label for="intervenants">Intervenants : (autant que possible) </label>
	    <input class="form-control fieldIntervenants" name="intervenants" type="text" placeholder="ex : Nom - Prénom - E-mail">
	    <div>
			<button id="plus">
				Ajouter un intervenant
			</button>
			<button id="moins">
				Supprimer le dernier intervenant
			</button>
		</div>
  	</div>
  	<div class="form-group col-md-12">
  		<label for="resume">Résumé</label>
  		<textarea class="form-control" id="resume" placeholder="Résume de votre projet"></textarea>
  	</div>

  <button type="submit" class="btn btn-default">Valider</button>
</form>
