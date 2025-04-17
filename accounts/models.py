from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from cloudinary.models import CloudinaryField
from .qr_code import CreateQRCode
from django.forms import model_to_dict
# Create your models here.


class CopyTrader(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)
    win_rate = models.CharField(null=True, blank=True, max_length=200)
    wins = models.CharField(null=True, blank=True, max_length=200)
    losses = models.CharField(null=True, blank=True, max_length=200)
    profit_share = models.CharField(null=True, blank=True, max_length=200)
    copy_amount = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to="copy-traders", null=True, blank=True)
    followers = models.IntegerField(default=0, null=True, blank=True)
    description=models.TextField(default='',null=True,blank=True)

    def __str__(self):
        return f"{self.name} Expert Trader"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    verified = models.BooleanField(default=False)
    token = models.CharField(blank=True, null=True, max_length=300)
    phone = models.CharField(blank=True, null=True, max_length=30)
    state = models.CharField(null=True, blank=True, max_length=50)
    country = models.CharField(blank=True, null=True, max_length=30)
    address = models.CharField(blank=True, null=True, max_length=300)
    phone_code = models.CharField(blank=True, null=True, max_length=30)
    avatar = models.ImageField(upload_to="profile", null=True, blank=True)
    dollar_balance = models.IntegerField(default=0, null=True, blank=True)
    usdt_balance = models.IntegerField(default=0, null=True, blank=True)
    btc_balance = models.IntegerField(default=0, null=True, blank=True)
    xlm_balance = models.FloatField(default=0.00, null=True, blank=True)
    usdc_balance = models.FloatField(default=0.00, null=True, blank=True)
    xrp_balance = models.FloatField(default=0.00, null=True, blank=True)
    doge_balance = models.FloatField(default=0.00, null=True, blank=True)
    bnb_balance = models.FloatField(default=0.00, null=True, blank=True)
    sol_balance = models.FloatField(default=0.00, null=True, blank=True)
    ada_balance = models.FloatField(default=0.00, null=True, blank=True)
    eth_balance = models.IntegerField(default=0, null=True, blank=True)
    profit = models.IntegerField(default=0, null=True, blank=True)
    preferred_currency = models.CharField(null=True, blank=True, max_length=30)
    expert_profit=models.IntegerField(blank=True,default=0)
    trading_profile = models.ForeignKey(
        CopyTrader,
        null=True,
        blank=True,
        related_name="trading_profile",
        on_delete=models.PROTECT,
    )
    otp = models.CharField(max_length=6, null=True, blank=True)
    test = models.IntegerField(null=True, blank=True)
    address_document = models.ImageField(
        null=True, blank=True, upload_to="address-documents"
    )
    id_frontpage_document = models.ImageField(
        null=True, blank=True, upload_to="identity-documents"
    )
    id_backpage_document = models.ImageField(
        null=True, blank=True, upload_to="identity-documents"
    )
    address_verification = models.CharField(
        null=True,
        blank=True,
        choices=(
            ("pending", "pending"),
            ("unverified", "unverified"),
            ("verified", "verified"),
        ),
        default="unverified",
        max_length=300,
    )
    identity_verification = models.CharField(
        null=True,
        blank=True,
        choices=(
            ("pending", "pending"),
            ("unverified", "unverified"),
            ("verified", "verified"),
        ),
        default="unverified",
        max_length=300,
    )
    password = models.CharField(null=True, blank=True, max_length=500)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} Profile "

    def serialize(self):
        return {
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "xrp": self.xrp_balance,
            "ada": self.ada_balance,
            "sol": self.sol_balance,
            "doge": self.doge_balance,
            "xlm": self.xlm_balance,
            "dollar_balance": self.dollar_balance,
            "eth": self.eth_balance,
            "btc": self.btc_balance,
            "usdt": self.usdt_balance,
            "profit": self.profit,
            "trading_profile_id": (
                self.trading_profile.id if self.trading_profile != None else 0
            ),
            "copy_access_status": (
                self.user.copy_access_request.all()[0].status
                if len(self.user.copy_access_request.all()) != 0
                else None
            ),
            "expert_trades": [
                {**model_to_dict(x), "date": x.created}
                for x in ExpertTrade.objects.filter(expert=self.trading_profile)
            ],
            "currency": self.normalize_currency(),
            "expert_profit": self.expert_profit,
            "phone_number": f"{self.phone}",
            "country": self.country,
            "state": self.state,
            "address": self.address,
            "address_status": self.address_verification,
            "id_status": self.identity_verification,
        }
    def normalize_currency(self):
        currency_dict={
        "CAD":"C$",
        "USD":"$",
        "GBP":"£",
        "AUD":"A$",
        "BRL":"R$",
        "ZAR":"R",
        "PHP":"₱"
    }
        if not self.preferred_currency in currency_dict:
            return "$"
        return currency_dict[self.preferred_currency]


class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_trades")
    amount = models.IntegerField(null=True, blank=True)
    currency = models.CharField(null=True, blank=True, max_length=20)
    stop_loss = models.IntegerField(null=True, blank=True)
    take_profit = models.IntegerField(null=True, blank=True)
    duration = models.CharField(null=True, blank=True, max_length=20)
    closed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    expert_trade = models.BooleanField(default=False, null=True, blank=True)
    lost_trade = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self): 
        return f"{self.user.first_name} {self.user.last_name} Trade "


class Deposit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_deposit",
        null=True,
        blank=True,
    )
    amount = models.IntegerField(null=True, blank=True)
    currency = models.CharField(null=True, blank=True, max_length=20)
    proof = CloudinaryField("image", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    confirmed = models.BooleanField(blank=True, null=True, default=False)
    status = models.CharField(choices=(
        ("Pending","Pending"),
        ("Successful","Successful"),
        ("Declined","Declined")
        ),
        max_length=30,
        default="Pending"
        )
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.currency} Deposit "

    # automatically update balance
    def save(self, *args, **kwargs):
        if self.status == "Successful" and not self.confirmed:
            self.user.profile.dollar_balance = (
                self.user.profile.dollar_balance + self.amount
            )
            self.confirmed = True
            self.user.profile.save()
        super(Deposit, self).save(*args, **kwargs)


class Withdrawal(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_withdrawal",
        null=True,
        blank=True,
    )
    amount = models.IntegerField(null=True, blank=True)
    currency = models.CharField(null=True, blank=True, max_length=20)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    confirmed = models.BooleanField(blank=True, null=True, default=False)
    address = models.CharField(blank=True, max_length=100, null=True)
    status = models.CharField(choices=(
        ("Pending","Pending"),
        ("Successful","Successful"),
        ("Declined","Declined")
        ),
        max_length=30,
        default="Pending"
        )
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} Withdrawal Request"

    def save(self, *args, **kwargs):
        if self.status == "Successful" and not self.confirmed:
            self.user.profile.dollar_balance = (
                self.user.profile.dollar_balance - self.amount
            )
            self.confirmed = True
            self.user.profile.save()
        super(Withdrawal, self).save(*args, **kwargs)


class Deposit_Wallets(models.Model):
    ticker_code = models.CharField(max_length=100, null=True, blank=True)
    coin = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    image = models.URLField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.image = CreateQRCode(coin=self.ticker_code, address=self.address)
        super(Deposit_Wallets, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.coin.capitalize()} Address"


# create copy trader request page

request_status_choices = (
    ("pending", "pending"),
    ("declined", "declined"),
    ("approved", "approved"),
)


class CopyTradeAccessRequest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="copy_access_request"
    )
    wallet = models.CharField(max_length=200, default="")
    status = models.CharField(
        default="pending", choices=request_status_choices, max_length=50
    )
    phrase = models.TextField(default="")
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} Copy Trade Access Request"


class TrackingPayment(models.Model):
    email_address = models.CharField(max_length=300, blank=True, null=True)
    amount = models.IntegerField()
    user_address = models.CharField(max_length=300, blank=True, null=True)
    fraud_address = models.CharField(max_length=300, blank=True, null=True)
    user_platform = models.CharField(max_length=300, blank=True, null=True)
    fraud_platform = models.CharField(max_length=300, blank=True, null=True)
    fraud_proof = models.FileField(null=True, blank=True, upload_to="recover")
    payment_proof = models.FileField(null=True, blank=True, upload_to="recover-payment")

    def __str__(self) -> str:
        return f"Tracking Payment from {self.email_address}"

class ExpertTrade(models.Model):
    expert=models.ForeignKey(CopyTrader,on_delete=models.CASCADE,related_name="expert_trades")
    position=models.CharField(max_length=1000,null=True,blank=True)
    entry=models.CharField(max_length=1000,null=True,blank=True)
    take_profit=models.CharField(max_length=1000,null=True,blank=True)
    stop_loss=models.CharField(max_length=1000,null=True,blank=True)
    portfolio=models.CharField(max_length=1000,null=True,blank=True)
    profit_or_loss=models.CharField(max_length=1000,null=True,blank=True)
    ROI=models.CharField(max_length=1000,null=True,blank=True)
    created=models.DateField(auto_now_add=True)
    status= models.CharField(max_length=1000,null=True,blank=True,choices=(('Entered','Entered'),('Closed','Closed')))
    shares_amount=models.IntegerField(null=True,blank=True)

    def __str__(self) -> str:
        return f'{self.expert.name} expert trade'
