from django.db import models
from django import forms
from beer_db.models import Beer
import pandas as pd
import numpy as np
from multiprocessing import Process,Manager
from ML.dec_tree import DecisionForestReg

data=Beer.objects.all()
data=pd.DataFrame(data=data.values())
data.drop([i for i in data.keys() if (data.dtypes[i]=='object' or i=='key' or i=='id') and i!='ABV'],axis=1,inplace=True)

data2 = list(data)
max_values = [126,60,65, 100, 83, 197, 139, 150, 263, 323, 66, 222, 193, 184, 304]
max_dic = {data2[i]: max_values[i] for i in range(len(max_values))}

class RatingModel(models.Model):
    """

	Model holding informations submited in RatingForm.

    """
    for i in data.keys():
        if i=='ABV':
            exec(f'{i} = models.DecimalField(decimal_places=2, max_digits=10)')	
        exec(f'{i} = models.IntegerField()')

    rating = models.DecimalField(decimal_places=2, max_digits=5)

class RatingForm(forms.ModelForm):
	class Meta:
		model=RatingModel
		# fields=('Style_Key',)
		tmp=[i for i in data.keys()]
		fields=tmp
	def __init__(self, *args, **kwargs):
		super(RatingForm, self).__init__(*args, **kwargs)
		for i,j in max_dic.items():
			exec(f'self.fields[\'{str(i)}\'].widget.attrs[\'max\'] = {j}')
			exec(f'self.fields[\'{str(i)}\'].widget.attrs[\'min\'] = 0')

class Parallel_ML():
    def __init__(self,forest_fit=Manager().list()):
        self.forest_fit=forest_fit
        self.paralelling_ML=Process(target=DecisionForestReg, args=[self.forest_fit])
        self.built=False
    def start_creating_model(self):
        self.paralelling_ML.start()
        self.built=True