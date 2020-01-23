from AlphaVantageAPI import AlphaVantageAPI


api = AlphaVantageAPI()
print(api.get_quote('PLUG'))
print(api.get_intraday_data('BLDP'))
