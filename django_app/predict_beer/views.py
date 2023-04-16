from django.shortcuts import render
from .forms import SnippetForm
from .models import PreferenceSnippet
from beer_db.models import Beer
import pandas as pd
import numpy as np
import copy
from math import sqrt
from user_handling.models import CustomUser

def predict(request):
	"""
	Calculates the most proper beer for given data from the form. Received form is stored in the database and the
	fitting beer is appended to the user's history (if one is logged in)

	**Context:**

	``CustomUser``
		An instance of :model:`user_handling.customuser`. 

	``PreferenceSnippet``
		An instance of :model:`predict_beer.preferencesnippet`.

	**Template:**

	:template:`results.html`

	:template:`predict.html`

	"""
	if request.method == 'POST':
		form = SnippetForm(request.POST)
		if form.is_valid():
			Values = []
			for item in form.cleaned_data:
				if item != 'predicted_beer':
					Values.append(form.cleaned_data[item])

			fitted_beer_name, index = fit_test(request,Values)
			data = {'predicted_beer' : Beer(index)}
			if request.user.is_authenticated:
				id=request.user.id
				CustomUser.objects.append_to_history(id, index)
			data.update(form.cleaned_data) 

			model = PreferenceSnippet(**data)
			model.save()

			return render(request, 'results.html', {'data' : form.cleaned_data, 'beer' : fitted_beer_name, 'index' : index})
	else:
		form = SnippetForm()
		return render(request,'predict.html', {'form' : form, 'username':request.user.username})


# not a view
def fit_test(request,Values):
	beer_set=Beer.objects.all()
	beer_set=pd.DataFrame(beer_set.values())
	col_to_drop=['id','Name','Brewery','Description','Style','key','Ave_Rating']
	beer_pred_set=beer_set.drop(col_to_drop,axis=1)
	
	if request.user.is_authenticated:
		history=request.user.history
		history=history.split(',')
		beer_list=[int(i)-1 for i in pd.unique(history) if i!='']
		beer_pred_set.drop(beer_list,axis=0,inplace=True)

	column=beer_pred_set.keys()
	Arr=[]
	row = pd.Series()
	for index, row in beer_pred_set.iterrows():
		len=0
		for i,j in zip(column,range(column.size)):
			len+=(Values[j]-row[i])**2
		res=sqrt(len)
		Arr.append(res)
	Arr1=pd.DataFrame(Arr)
	Arr2=copy.deepcopy(Arr1)
	index=Arr2[0].idxmin()
	return beer_set.iloc[index]['Name'], index+1