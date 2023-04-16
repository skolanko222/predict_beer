from django import forms
from .models import PreferenceSnippet
from beer_db.models import Beer
import pandas as pd

data=Beer.objects.all()
data=pd.DataFrame(data=data.values())
data.drop(['id','Name','key','Style','Brewery','Description'],axis=1,inplace=True)
data = list(data)
max_values = [126,60,5,65, 100, 83, 197, 139, 150, 263, 323, 66, 222, 193, 184, 304]
max_dic = {data[i]: max_values[i] for i in range(len(max_values))}

class SnippetForm(forms.ModelForm):
	class Meta: 
		model = PreferenceSnippet
		fields = ('ABV','Style_Key','Ave_Rating','Min_IBU','Max_IBU','Astringency','Body','Alcohol','Bitter','Sweet','Sour','Salty','Fruits','Hoppy','Spices','Malty')

	def __init__(self, *args, **kwargs):
		super(SnippetForm, self).__init__(*args, **kwargs)
		for i,j in max_dic.items():
			exec(f'self.fields[\'{str(i)}\'].widget.attrs[\'max\'] = {j}')
			exec(f'self.fields[\'{str(i)}\'].widget.attrs[\'min\'] = 0')	
