from service.bookturks.adapters.UserAdapter import UserAdapter
from service.bookturks.user.UserProfileTools import UserProfileTools


def get_avatar(backend, strategy, details, response,
               user=None, *args, **kwargs):
    url = None
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
    if backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal', '')
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
        ext = url.split('.')[-1]
    if url:
        user_adapter = UserAdapter()
        user_profile_tools = UserProfileTools()

        user_model = user_adapter.get_user_instance_from_django_user(user)
        print user_model
        print "User = ", user
        if user_model:
            user_profile_model = user_profile_tools.get_profile(user_model=user_model)
            user_profile_model.display_picture = url
            user_profile_tools.upload_profile(filename=user_profile_tools.create_filename(user_model),
                                              content=user_profile_tools.create_content(user_profile_model))
            print user_profile_model
        else:
            print "NOOOOOOOOOOO"
