# from django.urls import path
# from backend.api.views import SendEmailView, VerifyTokenView

urlpatterns = [
	path('verification/send/', SendEmailView.as_view(), name='send_email'),
	path('verification/verify/', VerifyTokenView.as_view(), name='verify_token'),
]
