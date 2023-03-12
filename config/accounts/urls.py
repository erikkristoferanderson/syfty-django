from django.urls import path
from .views import login_view
from .views import validate_magic_link
from .views import profile
from .views import signup
from .views import delete_account
from .views import logout_view
from .views import login_requested_view
from .views import error_view


urlpatterns = [
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    # path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('delete-account/', delete_account, name='delete_account'),
    path('login_requested/', login_requested_view, name='login_requested'),
    path('validate-magic-link', validate_magic_link, name="validate_magic_link"),
    path('error', error_view, name='error'),
    # ...other URL patterns...
]
