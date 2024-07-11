# Electricity Maps - Data Science Challenge

### Objective:
- Build an algorithm that can be called regularly from a backend and return a forecast for the carbon intensity of Eastern Denmark (DK-DK2) for the next 24 hours. 

---

#### Data 
The provided data consists of hourly averages of the average carbon intensity of electricity consumed in Denmark during an hour 2014-12-11 to 2019-09-26 along with other variables, suchs as the power consumption of different energy sources.

Forecasted values are also provided. This includes forecasts of solar production, wind speed, price power net import.

These forecasts are "latest-forecasted", with no information on the time of the forecast (only that is was before their recorded timestamp).

I believe, that these forecasts will serve as good predictors. However, as I don't know whether they are made 1 hour or 1 day in advance, I cannot use them for a 24 hour forecast algorithm.

#### Signal
In the jupyter notebook `signal.ipynb` I have outlined my initial data exploration.

#### Model
With limited time I decided to make a baseline forecasting model.
It is always good to start simple, and we need a baseline to compare more complicated models with.
As baseline I chose an ARIMA model. I ended up with an ARIMA $(2,1,1)\times(1,1,1)_{24}$. See the notebook `modeling.ipynb`for details.

#### Algorithm
The baseline model is found in the `src/baseline.py`.
It is build as python class and needs to be initiated. 
A 24 hour forecast is given by calling the function get_forecast with a time given as a string:
```python
from src.baseline import Baseline

model = Baseline()
mean, lower, upper = model.get_forecast('2019-01-01')
```

Here, mean is the predicted value and lower and upper are confidence bands.

The algorithm work as follows:
-  Fetches three weeks (default) of data prior to the time point.
- Fit an  ARIMA $(2,1,1)\times(1,1,1)_{24}$ to the data.
- Run the filter on the three weeks
- Return 24 hour forecasts (24 steps) including confidence intervals

#### Results
I tested the model on 200 days in 2019:
- MSE (24h) = 7172
- MAE (24h) = 61
- MAPE (24h) = 36 %

See the notebook `results.ipynb` for details

#### Get started
```
git clone https://github.com/petergroenning/em_challenge.git
cd em_challenge

pip install -r requirements.txt
pip install .
```

The data needs to be stored in the `data/` folder.
You can get the outputs directly by calling the main function:

```
python src/main.py --time='2019-01-01' --n_days=21 --n_ahead=24 --conf=False
```
where time is the time you want the forecast from, n_days is how many days to fetch data from to fit the model, n_head is the forecast horizon and conf is whether or not to include condifence intervals.
The last three arguments are optional.



#### How to improve?
The ARIMA model is linear and only considers carbon_intensity_avg. It could be improved by included external regressors such as wind speed or solar production if 24-hour forecasts are available.

The model should be considered as a baseline as more complicated non-linear models are expected to do better.
If it is possible to obtain features for future values, then boosting algorithms such as xgboost could be interesting to consider.

I could also have created other models to predict other variables to include in the carbon_intensity forecasting model, but that’s a task for later :)