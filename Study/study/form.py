'''IMPORTANT - why we are using inbuilt form 
ans - to display our model columns directly into our website ,till here we are filing these columns by django admin panel
'''

from django.forms import ModelForm
from .models import Room

# it will create a form of Room model with specified fields 
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'