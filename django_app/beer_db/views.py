from django.shortcuts import render
from .models import Beer

content={'Keys': [i for i in Beer.keys], 'Beers': []}
for i in range(1,Beer.objects.count()+1):
	content['Beers'].append(Beer.objects.get(id=i))

def database_view(request):
	"""
	Creates a list of all beers stored int he database.

	**Context:**

	``Beer``
        An instance of :model:`beer_db.beer`

	**Template:**

	:template:`database.html`

	"""
	return render(request,'database.html',content)

def dynamic_info_view(request,beer_id):
	"""
	Creates a page descripting a single beer. Takes the informations from the Beer object of a 
	given ID.

	**Context:**

	``Beer``
        An instance of :model:`beer_db.beer`

	**Template:**

	:template:`beer_info.html`

	"""
	beer_dict=Beer.objects.get(id=beer_id).__dict__
	beer_keys=Beer.objects.get(id=beer_id).__dict__.keys()
	beer_keys=[i.replace('_',' ') for i in beer_keys]
	beer_dict=[(i,j) for i,j in zip(beer_keys,beer_dict.values())]
	Table = beer_dict[4:]
	Table=[i for i in Table if i[0]!='Style Key']
	content_dynamic={'Beer': Beer.objects.get(id=beer_id), 'Table':Table}
	return render(request,'beer_info.html',content_dynamic)
