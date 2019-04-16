from django import forms


crops_code= (
("02002","Bajra"),
("03022","Urad"),
("04005","Castor seed"),
("01001","Cotton(lint)"),
("03006","Gram"),
("03016","Moong(Green Gram)"),
("04003","Groundnut"),
("04007","Linseed"),
("02015","Maize"),
("08046","Maize"),
("10015","Rapeseed &Mustard"),
("03020","Arhar/Tur"),
("02023","Rice"),
("04008","Safflower"),
("04019","Sesamum"),
("02011","Jowar"),
("04017","Soyabean"),
("04018","Sunflower"),
("02009","Wheat"),
("02012","Wheat")
)

seasons=(('current','current'),('Kharif','Kharif'),('Rabi','Rabi'),('Summer','Summer'),('Whole Year','Whole Year'))

class LoginForm(forms.Form):
   lag = forms.FloatField()
   lat = forms.FloatField()

   season = forms.ChoiceField(widget=forms.Select,choices=seasons)
   last1 = forms.ChoiceField(widget=forms.Select,choices = crops_code)
   last2 = forms.ChoiceField(widget=forms.Select,choices = crops_code)
   last3 = forms.ChoiceField(widget=forms.Select,choices = crops_code)
