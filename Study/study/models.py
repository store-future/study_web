from django.db import models
from django.contrib.auth.models import User



'''IMPORTANT for room
null  = TRUE(work upon filling data into table not mandatory) 
blank = True(work upon submiting model with blank cloumn ) 
      both together works so that table column can remain empty
a user can have multiple messages = so in vthe messages class we have to make a user column and set relationship (foreigney)
a Topic can have multiple rooms   = so here in the Room class we define topic column for setting one to many relatioship
'''

# model for room topic 
class Topic(models.Model):
    topic=models.CharField(max_length=200)
    
    def __str__(self):
        return self.topic



class Room(models.Model):
    host        = models.ForeignKey(User  , on_delete=models.SET_NULL , null=True)
    topic       = models.ForeignKey(Topic , on_delete=models.SET_NULL , null=True)  # SET_NULL is saying if topic is deleted than we don't want to delete Room model adn null=True is saying that databse column can be remain empty
    name        = models.CharField(max_length=200)
    description = models.TextField(null=True , blank=True)
    # participants = 
    update      = models.DateTimeField(auto_now=True)       # auto_now updates add timestamp  every time we update the model
    created     = models.DateTimeField(auto_now_add=True)   # while auto_now_add only add timestamp once it changes  never
    
    def __str__(self):
        return self.name
    
    #ordering our all rooms into  new comes first old in last
    class Meta:
        ordering = ['-update' , '-created']



# Message model lets user to comment inside the Room 
class Message(models.Model):
    user    = models.ForeignKey(User , on_delete=models.CASCADE)   # this attribute setting relationship with user so if user will delete then message associated to usr  will also be deleted  
    room    = models.ForeignKey(Room , on_delete=models.CASCADE)   # setting up one to many realtionship (one user can comment many mesesege) with Room models so that if room is deleted than room's comment shold also be deleted
    body    = models.TextField()
    update  = models.DateTimeField(auto_now=True)                  # auto_now updates add timestamp  every time we update the model
    created = models.DateTimeField(auto_now_add=True)              # while auto_now_add only add timestamp once it changes  never
    
    def __str__(self):
        return self.body[:50]