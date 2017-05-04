# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import xgboost as xgb
import datetime
import operator
from sklearn.cross_validataion import train_test_split
import matplotlib.pyplot as plt
#random_state
RS = 12357
#xgb_rounds
np.random.seed(RS)

xgb_params = {
    'eta': 0.05,
    'max_depth': 6,
    'subsample': 0.7,
    'colsample_bytree': 0.7,
    'objective': 'reg:linear',
    'eval_metric': 'rmse',
    'silent': 1
}

def xgb_train(X, y, params, ROUNDS):
	x, x_val, y_train, y_val = train_test_split(X,y,test_size=0.2,random_state = RS)

	xgb_train = xgb.DMatrix(x, label = y_train)
	xgb_val = xgb.DMatrix(x_val, label = y_val)

	watchlist = [(xgb_train,'train'),(xgb_val,'eval')]
	return xgb.train(params, xgb_train, ROUNDS, watchlist)

def predict_xgb(clr, X_test):
	return clr.predict(xgb.DMatrix(X_test))

def create_feature_map(features):
	outfile = open('xgb.fmap', 'w')
	i = 0
	for feat in features:
		outfile.write('{0}\t{1}\tq\n').format(i, feat)
		i += 1
	outfile.close


from sklearn import preprocessing, model_selection
#transform the object features
def LABELENCODER(X):
	lbl = preprocessing.LabelEncoder()
	for c in X.columns:
		if X[c].dtype == 'object':
			X[c] = lbl.fit_transform(X[c].values)

#xgboost_cv
cv_output = xgb.cv(xgb_params, x_train, num_boost_round = 1000,early_stopping_rounds = 20,
					verbose_eval = 50, show_stdv = False)
cv_output = [['train-rmse-maan', 'test-rmse-mean']].plot()

num_boost_round = len(cv_output)
model = xgb_train(x_train, y_train, xgb_params, num_boost_round)

#show the feature importance
fig, ax = plt.subplots(1, 1, figsize = (8,13))
xgb.plot_importance(model, max_num_features = 50, height = 0.5, ax = ax)

#predict xgb
xgb_predict = predict_xgb(model, x_test)
