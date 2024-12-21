# Fire
This model implements a time series feature engineering and classification workflow that issues eruption likelihood based on real-time seismic data.

## Installation

Ensure you have Anaconda Python 3.7 installed. Then

1. Clone the repo

```bash
git clone https://github.com/aardid/steamboat_jgr_ml
```

2. CD into the repo and create a conda environment

```bash
cd steamboat_jgr_ml

conda env create -f environment.yml

conda activate steamboat_jgr_ml
```

The installation has been tested on Windows, Mac and Unix operating systems. Total install with Anaconda Python should be less than 10 minutes.

## Running models
An examples have been included in ```main_test.py```. 

The ```forecast_test()``` trains on weather data between 2002 and 2017 but *excluding* a 20 daysperiod either side of a fire. It then constructs a model 'forecast' of this event. It could take several hours or a day to run depending on the cpus available for your computer.


To run the models, open ```main_test.py```, then in a terminal type
```bash
python main_test.py
```

## Disclaimers
1. This  forecast model is not guaranteed to predict every future eruption, it only increases the likelihood. In our paper, we discuss the conditions under which the forecast model is likely to perform poorly.

3. This software is not guaranteed to be free of bugs or errors. Most codes have a few errors and, provided these are minor, they will have only a marginal effect on accuracy and performance. That being said, if you discover a bug or error, please report to aardids@gmail.com.

4. This is not intended as an API for designing your own eruption forecast model. Nor is it designed to be especially user-friendly for Python/Machine Learning novices. Nevertheless, if you do want to adapt this model for another region, we encourage you to do that and are happy to answer queries about the best way forward. 