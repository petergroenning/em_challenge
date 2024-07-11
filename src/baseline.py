from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np

class Baseline():
    '''
    Baseline ARIMA model
    '''
    def __init__(self, order=(2,1,1), seasonal_order=(1,1,0,24)):
        self.order = order
        self.seasonal_order = seasonal_order
        self.params = None

    def fit(self, x_train):
        ''' Fit the ARIMA model to the training data 
            Args:
                x_train: np.array, training data
            Returns:
                model_fit: ARIMA model fit to the training data
        '''
        self.model = ARIMA(x_train, order=self.order, seasonal_order=self.seasonal_order)
        fit = self.model.fit()
        self.params = fit.params
        return fit
    
    def _forecast(self, x_train, n_steps = 24):
        ''' Forecast future values of the time series
        Fits the ARIMA model to the latest data and gives forecasts for 
        the next n_steps (including confidence intervals)
            Args:
                x_train: np.array, training data
                n_steps: int, number of steps to forecast
            Returns:
                mean: np.array, forecasted mean values
                upper: np.array, upper bound of the forecasted values
                lower: np.array, lower bound of the forecasted values
        '''
        model_fit = self.fit(x_train)
        forecast = model_fit.get_forecast(steps =n_steps)
        mean = forecast.predicted_mean
        upper, lower = forecast.conf_int().T
        return  mean, upper, lower
    
    def fetch_data(self, time, n_days = 21):
        ''' Fetch data from the database
            Args:
                time: datetime, time to fetch data for
                n_days: int, number of days to fetch data for
            Returns:
                data: np.array, fetched data

        '''

        df = pd.read_csv('data/DK-DK2.csv', index_col=0)
        data = df.carbon_intensity_avg[:time].iloc[-n_days*24:].values
        return data
    
    
    
    def get_forecast(self, time, n_days = 21, n_ahead = 24):

        data = self.fetch_data(time, n_days)
        mean, upper, lower = self._forecast(data, n_ahead)
        return mean, upper, lower
    





if __name__ == '__main__':
    import pandas as pd
    df = pd.read_csv('data/DK-DK2.csv', index_col=0)

    x_train =df.carbon_intensity_avg.values
    model = Baseline()


    mean, upper, lower = model.get_forecast('2016-01-04', 21, 24)
    print(mean)

