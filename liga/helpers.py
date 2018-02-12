import requests

from liga.models import User, Faculty
from liga_esportowa import settings

d = Faculty.objects.all()[0]


# TODO: faculty choose


def get_user(**kwargs):
    try:
        user = User.objects.get(**kwargs)
    except User.DoesNotExist:
        user = None
    return user


def create_user(social_data):
    new_user = User(facebook_id=social_data['id'],
                    name=social_data['name'].split()[0],
                    surname=social_data['name'].split()[1],
                    mail=social_data['email'],
                    faculty=d)
    new_user.save()
    return get_user(id=new_user.id)


def fill_user_info(social_user):
    # TODO: Move path to settings
    url = "https://graph.facebook.com/me?fields=id,name,email&access_token={1}".format(social_user.uid,
                                                                                       social_user.extra_data[
                                                                                           'access_token'])
    r = requests.get(url)
    return create_user(r.json())


def get_social_data(request):
    try:
        social_data = request.user.social_auth.filter(provider='facebook')[0]
    except IndexError:
        social_data = None
    return social_data


def get_user_facebook_id(social_data):
    try:
        fid = social_data.uid
    except AttributeError:
        fid = -1  # not using None here - model queries could possibly return an incorrect user with facebook_id=None
    return fid


def authenticate_user(request):
    social_data = get_social_data(request)
    fid = get_user_facebook_id(social_data)

    if settings.DEBUG:
        # request user allows django admin access in debug config
        user = get_user(facebook_id=fid) or get_user(id=request.user.id) or fill_user_info(social_data)
    else:
        user = get_user(facebook_id=fid) or fill_user_info(social_data)
    return user
