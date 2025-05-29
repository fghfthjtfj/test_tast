from django.urls import path
from .views import *

app_name = 'ads'

urlpatterns = [
    path('', AdsListView.as_view(), name='ads_list'),
    path('manage/', AdManageView.as_view(), name='ad_create'),
    path('manage/<int:pk>/', AdManageView.as_view(), name='ad_edit'),
    path('proposal/manage/', ProposalManageView.as_view(), name='proposal_create'),
    path('proposal/manage/<int:pk>/', ProposalManageView.as_view(), name='proposal_edit'),
    path('proposal/manage/<int:pk>/cancel/', ProposalManageView.as_view(), name='proposal_cancel'),
    path('proposal/manage/<int:pk>/accept/', ProposalManageView.as_view(), name='proposal_accept'),

]