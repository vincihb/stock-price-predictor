
from api.alpha_vantage.AlphaVantageAPI import AlphaVantageAPI

quote = AlphaVantageAPI().get_quote('HEXO')
print(quote['Global Quote']['10. change percent'])
