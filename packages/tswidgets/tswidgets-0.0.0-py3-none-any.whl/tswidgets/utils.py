import os
import pandas as pd
import numpy as np

import requests
from io import StringIO

import itertools

import seaborn as sns
import matplotlib.pyplot as plt

import statsmodels.api as sm
import statsmodels.tsa.api as smt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

# General settings class
class CFG:
    data_folder = '/data/'
    img_dim1 = 25
    img_dim2 = 8
    style = 'https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle'

# Set figure style
plt.rcParams.update({'figure.figsize': (CFG.img_dim1, CFG.img_dim2)})
plt.style.use(CFG.style)

# Function to fetch data from the "apis.datos.gob.ar" API
def sdt_get(serie, **kwargs):
    """
    Fetch data from the "apis.datos.gob.ar" API.

    Parameters:
        serie: str or list of series IDs to query.
        kwargs: Additional parameters like start_date, collapse, etc.

    Returns:
        pd.DataFrame: A DataFrame with 'indice_tiempo' as the index.
    """
    if isinstance(serie, list):
        serie = ','.join(serie)

    settings = '&'.join([f"{k}={v}" for k, v in kwargs.items()])
    url = f"https://apis.datos.gob.ar/series/api/series/?format=csv&last=5000&ids={serie}&{settings}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        csv_data = StringIO(response.text)
        output = pd.read_csv(csv_data).set_index('indice_tiempo')
        output.index = pd.to_datetime(output.index)
        return output

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Function to compare moments of distribution by splitting the series in two
def sdt_compare(serie):
    """
    Compare the moments of the distribution by splitting the series in two.
    """
    split = int(len(serie) / 2)
    X1, X2 = serie[:split], serie[split:]
    mean1, mean2 = np.round(X1.mean(), 0), np.round(X2.mean(), 0)
    std1, std2 = np.round(X1.std(), 0), np.round(X2.std(), 0)
    
    print(f'Mean A: {mean1} - Mean B: {mean2} - Ratio A/B = {np.round(100 * mean1 / mean2, 2)}%')
    print(f'Std A: {std1} - Std B: {std2} - Ratio A/B = {np.round(100 * std1 / std2, 2)}%')
    
    return [mean1, mean2, std1, std2]

# Function to generate scatter plots for lagged values
def sdt_auto_scatter(series, lags=9, ncols=3):
    """
    Scatter plot of lagged values.
    """
    series = pd.Series(series)
    nrows = int(np.ceil(lags / ncols))
    
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows, figsize=(4 * ncols, 4 * nrows))
    for ax, lag in zip(axes.flat, np.arange(1, lags + 1, 1)):
        lag_str = f't-{lag}'
        X = pd.concat([series, series.shift(-lag)], axis=1, keys=['y', lag_str]).dropna()
        
        X.plot(ax=ax, kind='scatter', y='y', x=lag_str)
        corr = X.corr().iloc[0, 1]
        ax.set_ylabel('Original')
        ax.set_title(f'Lag: {lag_str} (corr={corr:.2f})')
        sns.despine()

    fig.tight_layout()

# Augmented Dickey-Fuller test for stationarity
def sdt_adf(serie):
    """
    Perform the Augmented Dickey-Fuller test for stationarity.
    """
    result = adfuller(serie)
    print(f'ADF Statistic: {result[0]:.6f}')
    print(f'p-value: {result[1]:.6f}')
    print('Critical Values:')
    for key, value in result[4].items():
        print(f'\t{key}: {value:.3f}')
    return result

# ARIMA process simulator
def sdt_sim(AR=[], I=0, MA=[], obs=1000, seed=113, title=''):
    """
    Simulate ARIMA process.
    """
    np.random.seed(seed)
    arparams = np.array(AR)
    maparams = np.array(MA)
    ar = np.r_[1, -arparams]
    ma = np.r_[1, maparams]
    
    arma_process = sm.tsa.ArmaProcess(ar, ma)
    y = arma_process.generate_sample(obs)
    for _ in range(I):
        y = y.cumsum()

    tsplot(pd.Series(y), title=title)
    return y

# ARIMA model exploration
def sdt_explore(series, p=[0, 4], d=[0, 2], q=[0, 4]):
    """
    Explore ARIMA models and compute AIC/BIC values.
    """
    results_bic = pd.DataFrame(index=[f'AR{i}' for i in range(p[0], p[1] + 1)],
                               columns=[f'MA{i}' for i in range(q[0], q[1] + 1)])
    results_aic = results_bic.copy()

    for i, j, k in itertools.product(range(p[0], p[1] + 1),
                                     range(d[0], d[1] + 1),
                                     range(q[0], q[1] + 1)):
        if i == j == k == 0:
            results_bic.loc[f'AR{i}', f'MA{k}'] = np.nan
            results_aic.loc[f'AR{i}', f'MA{k}'] = np.nan
            continue

        try:
            model = sm.tsa.SARIMAX(series, order=(i, j, k))
            results = model.fit()
            results_bic.loc[f'AR{i}', f'MA{k}'] = results.bic
            results_aic.loc[f'AR{i}', f'MA{k}'] = results.aic
        except:
            continue

    return results_bic.astype(float), results_aic.astype(float)

# Helper function to get minimum values from DataFrame
def get_min(df):
    """
    Return the index and column where the minimum value occurs in a DataFrame.
    """
    return df.idxmin().loc[df.min().idxmin()], df.min().idxmin()



def tsplot(y, lags=None, title='', figsize=(14, 7)):
    '''Examine the patterns of ACF and PACF, along with the time series plot and histogram.

    Original source: https://tomaugspurger.github.io/modern-7-timeseries.html
    '''
    fig = plt.figure(figsize=figsize)
    layout = (2, 2)
    ts_ax   = plt.subplot2grid(layout, (0, 0))
    hist_ax = plt.subplot2grid(layout, (0, 1))
    acf_ax  = plt.subplot2grid(layout, (1, 0))
    pacf_ax = plt.subplot2grid(layout, (1, 1))

    y.plot(ax=ts_ax)
    ts_ax.set_title(title)
    y.plot(ax=hist_ax, kind='hist', bins=25)
    hist_ax.set_title('Histogram')
    smt.graphics.plot_acf(y, lags=lags, ax=acf_ax)
    smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax)
    [ax.set_xlim(0) for ax in [acf_ax, pacf_ax]]
    sns.despine()
    plt.tight_layout()
    return ts_ax, acf_ax, pacf_ax
