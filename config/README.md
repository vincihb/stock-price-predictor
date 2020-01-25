# Add to this directory
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

At the end your project should look like:
```
glowing-pancake-praw/
    ...
    config/
        reddit_api.json
        stock_api.json
    ...
```