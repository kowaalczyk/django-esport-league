import requests
from liga.models import User, Faculty

d=Faculty.objects.all()[0]
#TODO: faculty choose

def create_user(data):
    new_user=User(facebook_id=data['id'],
         name=data['name'].split()[0],
         surname=data['name'].split()[1],
         mail=data['email'],
        faculty=d)
    new_user.save()



def fill_user_info(social_user):
    url = "https://graph.facebook.com/me?fields=id,name,email&access_token={1}".format(social_user.uid,
                                                                                       social_user.extra_data[
                                                                                           'access_token'])
    r = requests.get(url)
    create_user(r.json())
