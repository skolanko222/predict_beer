from django.shortcuts import render
from django.http import HttpResponse
from .models import RatingForm
from .models import RatingModel
from user_handling.views import machine_learning
from ML.dec_tree import definite_fit
# Create your views here.

def predict_val(request):
	"""
	Predicts the average raiting of a beer described in the given form.

	**Context:**

	``RatingForm``
		An instance of :model:`ML.RatingForm`. 

	``PreferenceSnippet``
		An instance of :model:`predict_beer.preferencesnippet`.

	**Template:**

	:template:`form.html`

	"""
	if machine_learning.paralelling_ML.is_alive():
		return render(request,'waiting.html')
	else:		
		if request.method=='POST':
			form=RatingForm(request.POST)
			if form.is_valid():
				predicted_rating=definite_fit([list(form.cleaned_data.values())],machine_learning.forest_fit)
				data = {'rating' : float(predicted_rating)}
				data.update(form.cleaned_data)
				model = RatingModel(**data)
				model.save()
				predicted_rating = str(predicted_rating).replace('[','').replace(']','')
				return render(request,'res.html',{'data' : form.cleaned_data, 'Ave_Rating': predicted_rating[0:4]})
		else:
			form=RatingForm()
			return render(request,'form.html',{'form' : form})