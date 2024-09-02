from accounts.handlers import FetchCoinData, Forex_Currencies, StockData
from django.shortcuts import render
from accounts.models import TrackingPayment
from django.contrib import messages
from django.http import JsonResponse


def HomePage(request):
    # return render(request,'pages/home.html')
    return render(request, "pages/homepage.html", {"crypto": FetchCoinData})


def RecoverAssets(request):
    if request.method == "POST":
        data = request.POST
        files = request.FILES
        TrackingPayment.objects.create(
            email_address=data["email"],
            amount=data["amount"],
            user_address=data["wallet"],
            fraud_address=data["swallet"],
            user_platform=data["exchange"],
            fraud_platform=data["sexchange"],
            fraud_proof=files["scam"],
            payment_proof=files["payment"],
        )
        messages.success(
            request,
            "Tracking request successfully created, admins will contact you soon",
        )
        return JsonResponse({"staus": "done"}, safe=False)

    return render(request, "pages/recover-crypto.html")
