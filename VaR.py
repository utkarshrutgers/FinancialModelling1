def value_at_risk(returns, confidence_level=.05):
	"""
	It calculates the Value at Risk (VaR) of some time series. It represents 
	the maximum loss with the given confidence level.
	
	Parameters
	----------
	returns : pandas.DataFrame
		Returns of each time series. It could be daily, weekly, monthly, ...
		
	confidence_level : int
		Confidence level. 5% by default.
			
	Returns
	-------
	var : pandas.Series
		Value at Risk for each time series.
	
	"""
	
	# Calculating VaR
	return returns.quantile(confidence_level, axis=0, interpolation='higher')


def expected_shortfall(returns, confidence_level=.05):
	"""
	It calculates the Expected Shortfall (ES) of some time series. It represents 
	the average loss according to the Value at Risk.
	
	Parameters
	----------
	returns : pandas.DataFrame
		Returns of each time serie. It could be daily, weekly, monthly, ...
		
	confidence_level : int
		Confidence level. 5% by default.
			
	Returns
	-------
	es : pandas.Series
		Expected Shortfall for each time series.
	
	"""
	
	# Calculating VaR
	var = value_at_risk(returns, confidence_level)
	
	# ES is the average of the worst losses (under var)
	return returns[returns.lt(var, axis=1)].mean()


# Importing libraries
from pandas_datareader import data as pdr

# Defining general variables
ticker = 'SPY'
first_date = '2010-01-01'
last_date = '2018-08-31'
conficence_level = 0.05 
k = 0.02

# Getting data from yahoo
ticker_close = pdr.get_data_yahoo(ticker, first_date, last_date)[['Close']]

# Getting daily percentage returns from ticker close prices
ticker_returns = ticker_close.copy().pct_change().dropna(axis=0).rename(columns={'Close': 'dr1'})

# Modifying returns with a constant value
ticker_returns['dr2'] = ticker_returns['dr1'].copy()
ticker_returns.loc[ticker_returns['dr1'] < ticker_returns['dr1'].quantile(conficence_level), 'dr2'] -= k

# Getting VaR using value_at_risk function
var = value_at_risk(ticker_returns)

# Getting ES using expected_shortfall function
es = expected_shortfall(ticker_returns)
