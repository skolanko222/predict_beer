from django.db import models
import pandas as pd
import numpy as np


# Create your models here.

class Beer(models.Model):
	"""

	This model holds informations about every beer from datasets/beer_data_set.csv.
	It's application's main data source, used in ML and predict_beer aplications.

	"""

	beer_set=pd.read_csv('../datasets/beer_data_set.csv')
	keys=beer_set.keys()
	keys=keys.drop(['Name','key','Style Key'])
	new_columns=[i.replace(' ','_') for i in beer_set.keys()]
	beer_set.columns=new_columns
	for i,j in zip(beer_set.keys(),beer_set.dtypes):
		if j=='int64':
			exec(f'{i} = models.IntegerField()')
		elif j=='float64':
			exec(f'{i} = models.DecimalField(decimal_places=2, max_digits=10)')
		else:
			exec(f'{i} = models.TextField()')

