# Credit Cycle Monitor

An interactive dashboard that shows where U.S. credit stands today compared with its own history since 2000. It pulls Federal Reserve data on bank loan delinquencies, charge-offs, banks' lending standards, corporate bond spreads and the 10-year Treasury yield, and puts it all on one page.

I built it because every other project in my portfolio is a model of one piece of the credit market (an auto ABS deal, consumer loan defaults, a warehouse line, an insurer's bond portfolio). I wanted one place that shows the whole cycle those pieces sit in.

**Live dashboard:** https://deepangiarora.github.io/credit-cycle-monitor/

## I. What's on it

| Section | What it shows |
|---|---|
| The read | A short summary of where credit stands, written from the latest numbers |
| Tiles | Six key series with today's value, the change over a year, a sparkline, and where today ranks against every reading since 2000 |
| Chart | Four tabs (delinquencies, charge-offs, lending standards, spreads and rates) from 2000 to today, with recessions shaded. Hover for exact values, click a name to hide it |
| Notes | What I take from the data, and how it connects to my other projects |
| Table | Every series with its latest value, 1-year change, median and percentile |

Each tile gets a label from its percentile rank since 2000. For delinquencies and lending standards: below the 40th percentile is "Low", 40th to 70th is "Near median", 70th to 90th is "Elevated" and above the 90th is "High". For the corporate spread it's flipped, because a very low spread means investors are relaxed about risk, so the bottom 10% is "Unusually tight".

## II. What I found (data through Q2 2026 for banks, September 2026 for rates)

- **Bank loan losses look normal, not stressed.** Most delinquency rates are close to their medians since 2000. Credit cards rose from 1.53% in Q3 2021 to 3.22% in Q2 2024 and have eased to 2.85% since.
- **Commercial real estate is the slow one.** CRE delinquencies went from 0.63% in Q3 2022 to 1.58% in Q4 2025, more than double, and have barely come down (1.53%).
- **The bond market is the unusual part.** The spread between Baa corporate bonds and the 10-year Treasury was 1.48 points in September 2026, lower than 98% of months since 2000. It was also this low in early 2007.
- **Rates are the pressure point.** The 10-year averaged 4.99% in September 2026, up 0.87 points in a year.

## III. How it works

- `index.html` is the whole dashboard: plain HTML, CSS and JavaScript with the data built in, so it opens offline and needs no libraries.
- `update_data.py` downloads the latest data for all 11 series straight from FRED (no API key needed) and rewrites the data inside `index.html`. Run `python update_data.py` to refresh it. Every number on the page, including the written summary, recalculates from the data.
- `data.json` is the same data on its own, if you want to use it somewhere else.

## IV. Data

All series come from FRED (Federal Reserve Bank of St. Louis), from January 2000 onward:

| Series | FRED ID | Frequency |
|---|---|---|
| Delinquency rate: credit cards | DRCCLACBS | Quarterly |
| Delinquency rate: consumer loans | DRCLACBS | Quarterly |
| Delinquency rate: single-family mortgages | DRSFRMACBS | Quarterly |
| Delinquency rate: commercial real estate (excl. farmland) | DRCRELEXFACBS | Quarterly |
| Delinquency rate: business loans | DRBLACBS | Quarterly |
| Charge-off rate: credit cards | CORCCACBS | Quarterly |
| Charge-off rate: all loans | CORALACBS | Quarterly |
| Net % of banks tightening: business loans to large and middle-market firms | DRTSCILM | Quarterly |
| Net % of banks tightening: credit cards | DRTSCLCC | Quarterly |
| Moody's Baa yield minus 10-year Treasury | BAA10YM | Monthly |
| 10-year Treasury yield | GS10 | Monthly |

The bank data comes from the Federal Reserve Board's Charge-Off and Delinquency Rates release (all U.S. commercial banks), and the lending standards from the Fed's Senior Loan Officer Opinion Survey. Recession dates are from the NBER.

## V. Limitations

- Bank data only covers commercial banks, not private credit, credit unions or fintech lenders, which is where a lot of riskier lending happens now.
- Quarterly bank data arrives about two months after the quarter ends, so the dashboard always lags a bit.
- Percentiles compare against 2000 onward only, which includes one big crisis (2008) and one short one (2020).
- I use the Moody's Baa spread instead of the ICE BofA spreads because FRED now only keeps three years of ICE history.

## Files

- `index.html`: the dashboard
- `update_data.py`: refreshes the data from FRED
- `data.json`: the raw data
