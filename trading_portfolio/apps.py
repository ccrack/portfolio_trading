from django.apps import AppConfig


class TradingPortfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trading_portfolio'

#bind my signal from profile model
class TradingConfig(AppConfig):
    name = 'trading'

    def ready(self):
        import trading.signals