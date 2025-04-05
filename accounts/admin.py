from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    pass


@admin.register(Trade)
class TradeAdmin(ModelAdmin):
    pass


@admin.register(Deposit)
class DepositAdmin(ModelAdmin):
    pass


@admin.register(Withdrawal)
class WithdrawalAdmin(ModelAdmin):
    pass


@admin.register(Deposit_Wallets)
class DepositWalletsAdmin(ModelAdmin):
    pass


@admin.register(CopyTrader)
class CopyTraderAdmin(ModelAdmin):
    pass


@admin.register(CopyTradeAccessRequest)
class Admin(ModelAdmin):
    pass


@admin.register(TrackingPayment)
class TraderAccessAdmin(ModelAdmin):
    pass


@admin.register(ExpertTrade)
class ExpertTradeAdmin(ModelAdmin):
    pass
