from src.baseline import Baseline
import argparse


def main(time, n_days = 21, n_ahead = 24, conf = False):
    baseline = Baseline()

    if n_days is None:
        n_days = 21
    if n_ahead is None:
        n_ahead = 24
    forecast = baseline.get_forecast(time, n_days, n_ahead)

    if conf:
        return forecast
    else:
        return forecast[['mean']]


argparser = argparse.ArgumentParser()
argparser.add_argument('--time', type=str, help='Time to forecast for')
argparser.add_argument('--n_days', type=int, help='Number of days to fetch data for')
argparser.add_argument('--n_ahead', type=int, help='Number of steps to forecast')
argparser.add_argument('--conf', type=bool, help='Return confidence intervals')
args = argparser.parse_args()



if __name__ == '__main__':
    print(main(args.time, args.n_days, args.n_ahead, args.conf))