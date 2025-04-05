from django.urls import path,include
from .views import *

urlpatterns = [
    path('register-success',SignUpSuccessView,name='success'),
    path('resend-otp',ResendOTP,name='resend'),
    path('activate/',ActivateAccount,name='activate'),
    path('login/',LoginView,name='login'),
    path('sign-up/',SignUpView,name='sign-up'),
    path('dashboard/',Dashboard,name='dashboard'),
    path('assets/',Assets,name='assets'),
    path('trades/',Trades,name='trades'),
    path('markets/',Market,name='markets'),
    path('deposit/',DepositFunds,name='deposits'),
    path('withdraw/',Withdraw,name='withdraws'),
    path('copy/',CopyTrades,name='copy'),
    path('logout/',Logout,name='logout'),
    path('deposit-method/',SelectMethod,name='select'),
    path('bank-deposit',PayWithBank,name="bank"),
    path('card-deposit',PayWithCard,name="card"),
    path('history',History,name='history'),
    path('recover',RecoverUserData),
    path('copy-access',CopyTraderPageRequest,name='access'),
    path('copy/<int:pk>',ExpertTraderDetails,name='copy-details'),
    path('user-expert-profits',UserExpertTraderDetails,name='user-expert-profits'),
     path('settings',SettingsPage,name='settings'),
    path('upload-address',UploadAdressDocs,name='upload-address'),
    path('upload-id',UploadIdentityDocs,name='upload-id'),
    path('update-password',UpdatePassword,name='password'),
    path('forgot-password',ForgotPasswordSendOtp,name='forgot-password'),
    path('verify-identity',VerifyIdentity,name='verify-identity'),
    path('change-password/',ChangePassword,name='change-password')

]
