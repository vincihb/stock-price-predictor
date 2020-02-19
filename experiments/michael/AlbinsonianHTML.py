from api.alpha_vantage.AlphaVantageAPI import AlphaVantageAPI
from client.util.HTMLUtil import HTMLUtil
from client.util.html.LinkBuider import LinkBuilder
from client.util.html.ScrollableDiv import ScrollableDiv
from client.util.html.TableBuilder import TableBuilder
from reports.Sorting import Sorting


class AlbinsonianHTML:
    @staticmethod
    def get_ticker_table(tickers_found, lookup_thresh=3, force_reload=False):
        table_header = ['Ticker', 'Mentions', 'Name', 'Description', 'Movement', 'Links']

        norm_factor = 0
        for tf in tickers_found:
            norm_factor += tickers_found[tf]['count']

        table_values = []
        for tf in tickers_found:
            addendum = ''
            counter = 0
            for submission in tickers_found[tf]['submissions']:
                addendum += LinkBuilder('[%d] - %d' % (counter, submission['score']),
                                        'https://www.reddit.com' + submission['link']).compile() + '<br />'
                counter += 1

            addendum = ScrollableDiv(addendum, '5rem').compile()

            desc = '...'
            if 'description' in tickers_found[tf] and tickers_found[tf]['description'] is not None:
                desc = tickers_found[tf]['description']

            if tickers_found[tf]['count'] >= lookup_thresh - 1:
                print('crawling AV for %s' % tf)
                pct_change = AlphaVantageAPI().get_parsed_quote(tf, force_reload)['10. change percent']
                pct_in_tag = HTMLUtil.wrap_in_tag(pct_change, 'div',
                                                  attributes={'class': 'negative' if '-' in pct_change else 'positive'})
            else:
                pct_in_tag = 'N/A'

            table_values.append([tf, tickers_found[tf]['count'], tickers_found[tf]['name'],
                                 desc[:200] + '...', pct_in_tag, addendum])

        table_values.sort(key=Sorting.sort_by_mentions, reverse=True)
        return TableBuilder(headers=table_header, rows=table_values)