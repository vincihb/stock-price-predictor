from db.SqlExecutor import SqlExecutor


INSERT_SQL = "INSERT INTO `COMPANY` (TICKER) VALUES ('$$REP$$');"
executor = SqlExecutor(debug=True)
with open('../../data/tickers/compiled/all_tickers.txt') as all_tickers:
    for ticker_text in all_tickers:
        ticker = ticker_text.strip()
        sql = INSERT_SQL.replace('$$REP$$', ticker)
        executor.exec_insert(sql)

rows = executor.exec_select('SELECT COUNT(*) AS rowcount FROM COMPANY;')
for row in rows:
    print(row[0])

