import numpy as np
import pandas as pd
import matplotlib.pyplot as plt # chart library

def readData():
	dataSet = pd.read_csv("influencers.csv",delimiter =',')
	return dataSet

def rumus_segitiga(x,a,b,c,d):
	if x<a or x >=d:
		return 0
	elif a<x<=b:
		return (x-a)/(b-a)
	elif b <= x <= c:
		return 1
	elif c < x <= d:
		return -(x-d)/(d-c)
	else:
		return 0

def derajatKeanggotaanFollower(data_set):
	variabel_linguistik = {
		"sangat_sedikit" : [0,0,10000,15000],
		"sedikit" : [10000,15000,30000,35000],
		"sedang" : [30000,35000,50000,55000],
		"banyak" : [50000,55000,65000,70000],
		"sangat_banyak" : [65000,70000,100000,100000]
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
		"rendah" : [0.0,0.0,3.0,4.0],
		"normal" : [3.0,4.0,6.0,7.0],
		"tinggi" : [6.0,7.0,10.0,10.0],
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
		minim = min(data_set['Crips_follower'][index][data[0]],data_set['Crips_engagement'][index][data[1]])
		data.append(minim)
	
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
	# print(hasil)
	return hasil

def ruleInference(data_set):	
	defuzz = []
	for i in range(len(data_set)):
		rule = []
		for keys_follow in data_set['Crips_follower'][i]:
			for keys_engag in data_set['Crips_engagement'][i]:
				if data_set['Crips_follower'][i][keys_follow] != 0 and data_set['Crips_engagement'][i][keys_engag] != 0:
					rule.append([keys_follow,keys_engag,setRule(keys_follow,keys_engag)])
		defuzzy = defuzzyficationSugeno(inferenceSugeno(rule,i)) 
		defuzz.append(defuzzy)			
	data_set["deffuz"] = defuzz		
		

if __name__ == '__main__':


	data_set = readData();
	fuzzyfication(data_set)
	ruleInference(data_set)
	pd.set_option('display.max_colwidth', -1)
	x = data_set.sort_values(by=['deffuz'],ascending = False)
	dat = x.iloc[0:20,[0]]
	dataq = x.iloc[0:20,[0,1,2,5]]
	print(dataq)
	dat.to_csv('20_id_terbaik.csv',header=False,index=False)
	# print(x)