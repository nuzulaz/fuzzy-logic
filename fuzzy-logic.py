import numpy as np
import pandas as pd
import matplotlib.pyplot as plt # chart library

def readData():
	dataSet = pd.read_csv("influencers.csv",delimiter =',')
	return dataSet

def rumus_segitiga(x,a,b,c):
	if x<0 or x >= c:
		return 0
	elif a<x<=b:
		return (x-a)/(b-a)
	elif b < x < c:
		return -(x-c)/(c-b)
	else:
		return 0

def derajatKeanggotaanFollower(data_set):
	variabel_linguistik = {
		"sangat_sedikit" : [0,10000,20000],
		"sedikit" : [10000,20000,40000],
		"sedang" : [20000,40000,60000],
		"banyak" : [40000,60000,80000],
		"sangat_banyak" : [60000,80000,100000]
	}

	crisp_set = {
		"sangat_sedikit" : 0.0,
		"sedikit" : 0.0,
		"sedang" : 0.0,
		"banyak" : 0.0,
		"sangat_banyak" : 0.0
	}

	for fuzzy_set in variabel_linguistik.keys():
		crisp_set[fuzzy_set] = rumus_segitiga(data_set, *variabel_linguistik[fuzzy_set])

	return crisp_set

def derajatKeanggotaanEngagement(data_set):
	lines  = []
	variabel_linguistik = {
		"rendah" : [0.0,1.0,3.0],
		"normal" : [1.0,4.0,6.0],
		"tinggi" : [4.0,7.0,10.0],
	}

	crisp_set = {
		"rendah" : 0.0,
		"normal" : 0.0,
		"tinggi" : 0.0,
	}

	for fuzzy_set in variabel_linguistik.keys():
		crisp_set[fuzzy_set] = rumus_segitiga(data_set, *variabel_linguistik[fuzzy_set])

	return crisp_set

def fuzzyfication(data_set):
	linguistik_follower = []
	linguistik_engagement = []

	for index,row in data_set.iterrows():
		linguistik_follower.append(derajatKeanggotaanFollower(row['followerCount']))
		linguistik_engagement.append(derajatKeanggotaanEngagement(row['engagementRate']))

	data_set['Crips_follower'] = linguistik_follower
	data_set['Crips_engagement'] = linguistik_engagement

def setRule(var_linguistik_follower,var_linguistik_enganggement):

	if var_linguistik_follower == "sangat_sedikit" and var_linguistik_enganggement == "rendah" : return "tolak"
	if var_linguistik_follower == "sangat_sedikit" and var_linguistik_enganggement == "normal" : return "tolak"
	if var_linguistik_follower == "sangat_sedikit" and var_linguistik_enganggement == "tinggi" : return "pertimbangkan"
	
	if var_linguistik_follower == "sedikit" and var_linguistik_enganggement == "rendah" : return "tolak"
	if var_linguistik_follower == "sedikit" and var_linguistik_enganggement == "normal" : return "pertimbangkan"
	if var_linguistik_follower == "sedikit" and var_linguistik_enganggement == "tinggi" : return "pertimbangkan"

	if var_linguistik_follower == "sedang" and var_linguistik_enganggement == "rendah" : return "pertimbangkan"
	if var_linguistik_follower == "sedang" and var_linguistik_enganggement == "normal" : return "pertimbangkan"
	if var_linguistik_follower == "sedang" and var_linguistik_enganggement == "tinggi" : return "terima"
	
	if var_linguistik_follower == "banyak" and var_linguistik_enganggement == "rendah" : return "pertimbangkan"
	if var_linguistik_follower == "banyak" and var_linguistik_enganggement == "normal" : return "terima"
	if var_linguistik_follower == "banyak" and var_linguistik_enganggement == "tinggi" : return "terima"
	
	if var_linguistik_follower == "sangat_banyak" and var_linguistik_enganggement == "rendah" : return "terima"
	if var_linguistik_follower == "sangat_banyak" and var_linguistik_enganggement == "normal" : return "terima"
	if var_linguistik_follower == "sangat_banyak" and var_linguistik_enganggement == "tinggi" : return "terima"

def defuzzyficationSugeno(rule):
	top,bottom = 0,0
	
	for i in rule:
		if i[0] == "tolak":
			top += i[1]*20

		elif i[0] == "pertimbangkan":
			top += i[1]*40

		elif i[0] == "terima":
			top += i[1]*80

		bottom += i[1]
	
	return top/bottom
		
def inferenceSugeno(rule,index):
	hasil,arrTolak,arrPertimbangan,arrTerima = [],[],[],[]
	for data in rule:
		data.append(min(data_set['Crips_follower'][index][data[0]],data_set['Crips_engagement'][index][data[1]]))
	
	for i in range(len(rule)):
		if rule[i][2] == "tolak":
			arrTolak.append(["tolak",rule[i][3]])
	
		if rule[i][2] == "pertimbangkan":
			arrPertimbangan.append(["pertimbangkan",rule[i][3]])	

		if rule[i][2] == "terima":
			arrTerima.append(["terima",rule[i][3]])

	if arrTolak != []:
		hasil.append(max(arrTolak))
	if arrPertimbangan != []:
		hasil.append(max(arrPertimbangan))
	if arrTerima != []:
		hasil.append(max(arrTerima))		
	
	return hasil

def ruleInference(data_set):	
	defuzz = []
	rule = []
	for i in range(len(data_set)):
		# print(data_set['Crips_follower'][i],data_set['Crips_engagement'][i])
		for keys_follow in data_set['Crips_follower'][i]:
			for keys_engag in data_set['Crips_engagement'][i]:
			# print(data_set['Crips_engagement'][i][keys_engag])
				if data_set['Crips_follower'][i][keys_follow] != 0 and data_set['Crips_engagement'][i][keys_engag] != 0:
					# print(keys_engag,data_set['Crips_engagement'][i][keys_engag])
					# print(keys_follow,data_set['Crips_follower'][i][keys_follow])	
					rule.append([keys_follow,keys_engag,setRule(keys_follow,keys_engag)])
		defuzz.append(defuzzyficationSugeno(inferenceSugeno(rule,i)))			
	
	data_set["deffuz"] = defuzz		
		

if __name__ == '__main__':

	# print(derajatKeanggotaanFollower(38237))
	# print(derajatKeanggotaanEngagement(5.8))
	data_set = readData();
	fuzzyfication(data_set )
	ruleInference(data_set)
	x = data_set.sort_values(by=['deffuz'],ascending = False).head()
	pd.set_option('display.max_colwidth', -1)
	print(x)
	print(data_set.sort_values(by=['deffuz'],ascending = False).head())