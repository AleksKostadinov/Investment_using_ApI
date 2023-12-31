import pandas as pd
import psycopg2
from decouple import config

# connect to database
conn = psycopg2.connect(
    host=config('POSTGRES_HOST'),
    port="5432",
    database="db13f2023",
    user=config('POSTGRES_USER'),
    password=config('POSTGRES_PASSWORD')
)

cur = conn.cursor()

cur.execute("""
SELECT tmp_table.total_shares,
        holding_infos.cusip,
        holding_infos.ticker,
        holding_infos.security_name,
        filings.period_of_report,
        filings.filing_id
FROM
(
  SELECT SUM(shares) as total_shares, cusip, filing_id
  FROM holdings
  GROUP BY cusip, filing_id
) tmp_table
INNER JOIN filings
ON filings.filing_id = tmp_table.filing_id
INNER JOIN holding_infos
ON tmp_table.cusip = holding_infos.cusip
WHERE (filings.period_of_report = '2023-06-30' or filings.period_of_report = '2023-03-31') and filings.cik = '1067983'
""")

rows = cur.fetchall()

cur.close()

buffet_holdings = pd.DataFrame(rows, columns =['Shares',
                                               'CUSIP',
                                               'Ticker',
                                               'SecurityName',
                                               'PeriodOfReport',
                                               'FilingId'])
