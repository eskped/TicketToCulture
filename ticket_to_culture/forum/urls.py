from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

# from ticket_to_culture.ticket_to_culture import settings

from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.discovery_page, name='discoveryPage'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('profile/', views.profile_page, name='profile'),
    path('createPost/', views.create_post, name='createPost'),
    path('my-posts/', views.my_posts, name='myPosts'),
    path('my-posts/sell/<int:sold_id>/', views.sell_post, name='sellPost'),
    path('my-posts/undo-sold/<int:sold_id>/', views.undo_sold, name='undoSoldPost'),
    path('rate-buyer-search/<int:sold_id>/', views.rate_buyer_search, name='rateBuyerSearch'),
    path('rate-buyer/<int:sold_id>/<int:buyer_id>/', views.rate_buyer, name='rateBuyer'),
    path('rate-seller/<int:seller_rating_id>/', views.rate_seller, name='rateSeller'),
    path('post/<int:post_id>', views.post, name = 'post'),
    path('change-password/', views.change_password, name='changePassword'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
