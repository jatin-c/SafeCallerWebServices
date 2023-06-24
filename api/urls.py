from django.urls import path
from .views import UserRegistrationView, LoginView, TokenRefreshView, MarkSpamView, AddContactView, SearchView


urlpatterns = [
    # Other URL patterns...
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('mark-spam/', MarkSpamView.as_view(), name='mark_spam'),
    path('addcontact/', AddContactView.as_view(), name='add_contact'),
    path('search/', SearchView.as_view(), name='search'),

]
