# glowing-pancake-praw
A project to construct heatmaps of stock tickers mentioned on key reddit threads and perform sentiment analysis.

##Required setup:
### Add a config directory
Add a reddit_api.json file with the details from your reddit scraper account
```json
{
  "username": "...",
  "password": "...",
  "id": "...",
  "secret": "..."
}
```

Add a stock_api.json file with your api key for AlphaVantage
```json
{
  "API_KEY": "..."
}
```

## AlphaVantage
https://www.alphavantage.co/

## PRAW (active reddit scraping)
https://praw.readthedocs.io/

## PSAW (historical reddit scraping)
https://github.com/pushshift/api

## Interesting proxy rotation site
https://gimmeproxy.com/