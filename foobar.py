from bs4 import BeautifulSoup
import tweepy 
import urllib3
import requests 
from flask import Flask, request, render_template
import os
from sklearn.neighbors import KNeighborsClassifier as KNN
import pandas as pd
import sklearn as sk
import matplotlib.pyplot as plt
import pickle as pkl
import sys 



with open('dogInit.pkl', 'rb') as f:
	dogInit = pkl.load(f)
with open('y.pkl', 'rb') as f:
	y = pkl.load(f)
with open('X.pkl', 'rb') as f:
	X = pkl.load(f)

PEOPLE_FOLDER = os.path.join('static', 'graphs')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER


@app.route("/", methods=['GET', 'POST'])
def mainPage():
	global flag
	medicine_columns = [
   'Baytril mL (Strength:100mg/mL) SQ ONLY',
   'Polyflex mL (Strength: 200mg/mL) SQ ONLY',
   'Metoclopromide mL (Strength: 5mg/mL)',
   'Cerenia mL ',
   'Cefazolin mL (1 gram/vial) IV ONLY',
   'Hetastarch Rate mL/hr (6% Concentrate) IV ONLY',
   'Oral Dextrose mL (50% concentrate)',
   'Panacur mL (100mg/mL) ORAL ONLY',
   'Strongid mL ORAL ONLY',
   'Marquis Paste ORAL ONLY',
   'Amount of SQ Fluids Administered mL',
   'Anzemet mL (20mg/mL) IV ONLY',
   'Famotidine mL (10mg/mL) ',
   'Amount of IV Fluids Administered mL/hr',
   'Oral Nutrical mL',
   'Hetastarch Dosage mL (6% Concentrate) IV ONLY'
	]
	catnames = ['IV', 'SQ Fluid', 'Anzemet', 'Baytril', 'Cefazolin', 'Cerenia', 'Famotidine','Hetastarch Dose', 'Hetastarch Rate',
          'Marquis', 'Metoclopromide','Dextrose','Nutrical','Panacur','Polyflex','Strongid','Probability of Death']

	# paw = 0 
	# gum = 1 
	# attitude = 2
	# distemper = 0 
	# vomit = 2 
	# appetite = 2
	# feces = 0
	# sex = 0 
	# weight = 40 
	# age = 20 


	# if request.method == 'POST':
	attitude = request.form['attitude']
	paw = request.form['paw']
	vomit = request.form['vomit']
	gum = request.form['gum']
	distemper = request.form['distemper']
	appetite = request.form['appetite']
	feces = request.form['Feces']
	water = request.form['water']
	weight = request.form['weight']
	sex = request.form['sex']
	age = request.form['age']

	
	sys.stdout.flush()
   
	knn = KNN(n_neighbors = 10)
	knn.fit(X, y)
	# if flag == 1:
	# 	exDog = pd.DataFrame([[0, 1, 2, 0, 2, 2, 0, 142, 6, 103, 0, 40, 20]], columns = X.columns.values)
	# 	flag = 0
	# else: 
	exDog = pd.DataFrame([[paw, gum, attitude, distemper, vomit, appetite, feces, 142, 6, 103, sex, weight, age]], columns = X.columns.values)

	dists, elem = knn.kneighbors(exDog, 10)
	closestdog = dogInit.iloc[elem[0],:]
	res = closestdog[medicine_columns + ['outcome']].mean()
	reso = ([res[ind] for ind in res.index])
	result = [[catnames[i], reso[i]] for i in range(17)]
	plt.bar(catnames[:-1], reso[:-1])
	plt.xticks(rotation=90)
	plt.savefig('graph.png')
	surv = reso[-1]
	#plt.bar(catnames[-1], reso[-1])
	#plt.ylim(0,1)
	full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'graphs.png')
	plt.clf()
	return render_template("index.html", user_image = full_filename, user_input= str(surv))


@app.route("/adopt.html")
def adopt():
	
	return render_template("adopt.html")

# @app.rout("/index.html#two")
# def index2():
# 	return render_templace("index.html")

if __name__ == "__main__":
    app.run()
	