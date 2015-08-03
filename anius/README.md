# README #

Financial time series evaluation platform in Python/Pandas that statistically analyzes the expected value of trading strategies.

Anius is a statistical back-testing system. It is like other back-testing systems insofar as a set of conditions, e.g., the values of some number of indicators, trigger an entry, but it is unique in other ways.  Most back-testing systems are designed to tune the values of indicators. Anius, by contrast, plots market conditions after an entry is triggered. In other words it is designed to answer this question: Once an entry is triggered by a trading system, what does the market do afterwords, statistically speaking?

This project's namesake is the mythic Greek king and priest of Apollo who prophesied that the Trojan War would not be won until its tenth year, and therefore insisted that Agamemnon and his troops stay with him for nine years before going on to Troy.

The source data is in MySQL and the system makes assumptions about the schema.
