from collections import Counter
import nltk
#from nltk.corpus import stopwords
#nltk.download('stopwords')
#stopwords = stopwords.words('dutch')
from collections import defaultdict
import pickle


feature_dict = defaultdict(list)
feature_dict_per_subcat = defaultdict(list)
def get_unique_ne(ne_list, othercat_lists):
	other = set([j for i in othercat_lists for j in i])
	unique_list = []
	for item in ne_list:
		if item in other:
			continue
		else:
			unique_list.append(item)
	return unique_list


def at_least_five(feat_list, featurename):
	string_list = ["punt","lijn","bc","water","none","regio","fictief","land","cont","heelal","ORG_none","ORG_misc","gov","com"]
	for subcat in string_list:
		if subcat in featurename:
			global_subcat = subcat
			
	counts = Counter(feat_list)
	#print(featurename)
	#print(type(counts))
	at_least_n = []
	for item, count in counts.items():
		if count >= 3:
			at_least_n.append(item)
	if global_subcat not in feature_dict:
		feature_dict[global_subcat] = at_least_n
	else:
		val = feature_dict.get(global_subcat)
		val.append(at_least_n)
		feature_dict[global_subcat] = val
	# make dictionary that has the feature_name as keys and features as values
	if featurename not in feature_dict_per_subcat:
		feature_dict_per_subcat[featurename] = at_least_n
	else:
		val = feature_dict_per_subcat.get(featurename)
		val.append(at_least_n)
		feature_dict_per_subcat[featurename] = val
	return at_least_n

	

def main():
	#test_list = ["a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","b","b","b","c","c","c","c","c","c","c","c","c","c","d","d","e"]
	#print(at_least_five(test_list, "test"))
	#exit()
	infile = open("../data/using_development/SoNaR1_devcut_training.txt", "r",encoding="utf8")
	next(infile)
	main_cats = ["PER", "LOC" , "ORG" , "PRO", "EVE", "MISC"]
	per = []
	loc = []
	org = []
	eve = []
	pro = []
	misc = []
	lines = []
	for line in infile:
		line = line.rstrip().split('\t')
		lines.append(line)
		try:
			if line[-2] == "PER":
				per.append(line)
			elif line[-2] == "LOC":
				loc.append(line)
			elif line[-2] == "ORG":
				org.append(line)
			elif line[-2] == "PRO":
				pro.append(line)
			elif line[-2] == "EVE":
				eve.append(line)
			elif line[-2] == "MISC":
				misc.append(line)
		except:
			continue
	org_subcats = ['NONE', 'MISC', 'GOV', 'COM']
	# LOCATION DATA
	location_subcats = ['PUNT', 'LIJN', 'BC', 'WATER', 'NONE', 'REGIO', 'FICTIEF', 'LAND', 'CONT', 'HEELAL']
	punt=lijn=bc=water=none=regio=fictief=land=cont=heelal = 0
	puntNE= []
	lijnNE= []
	bcNE= []
	waterNE= []
	noneNE= []
	regioNE= []
	fictiefNE= []
	landNE= []
	contNE= []
	heelalNE = []
	for item in loc:
		lsubcat = item[-1]
		ne = item[2]
		if lsubcat == location_subcats[0]:
			punt += 1
			puntNE.append(ne)
		elif lsubcat == location_subcats[1]:
			lijn += 1
			lijnNE.append(ne)
		elif lsubcat == location_subcats[2]:
			bc += 1
			bcNE.append(ne)
		elif lsubcat == location_subcats[3]:
			water += 1
			waterNE.append(ne)
		elif lsubcat == location_subcats[4]:
			none += 1
			noneNE.append(ne)
		elif lsubcat == location_subcats[5]:
			regio += 1
			regioNE.append(ne)
		elif lsubcat == location_subcats[6]:
			fictief += 1
			fictiefNE.append(ne)
		elif lsubcat == location_subcats[7]:
			land += 1
			landNE.append(ne)
		elif lsubcat == location_subcats[8]:
			cont += 1
			contNE.append(ne)	
		elif lsubcat == location_subcats[9]:
			heelal += 1
			heelalNE.append(ne)
			
	# GET UNIQUE LISTS OF WORDS PER SUBCAT
	uniquepunt = get_unique_ne(puntNE, [lijnNE, bcNE,waterNE,noneNE,regioNE,fictiefNE,landNE,contNE,heelalNE])
	uniquelijn = get_unique_ne(lijnNE, [puntNE, bcNE,waterNE,noneNE,regioNE,fictiefNE,landNE,contNE,heelalNE])
	uniquebc = get_unique_ne(bcNE, [lijnNE, puntNE,waterNE,noneNE,regioNE,fictiefNE,landNE,contNE,heelalNE])
	uniquewater = get_unique_ne(waterNE, [lijnNE, bcNE,puntNE,noneNE,regioNE,fictiefNE,landNE,contNE,heelalNE])
	uniquenone = get_unique_ne(noneNE, [lijnNE, bcNE,waterNE,puntNE,regioNE,fictiefNE,landNE,contNE,heelalNE])
	uniqueregio = get_unique_ne(regioNE, [lijnNE, bcNE,waterNE,noneNE,puntNE,fictiefNE,landNE,contNE,heelalNE])
	uniquefictief = get_unique_ne(fictiefNE, [lijnNE, bcNE,waterNE,noneNE,regioNE,puntNE,landNE,contNE,heelalNE])
	uniqueland = get_unique_ne(landNE, [lijnNE, bcNE,waterNE,noneNE,regioNE,fictiefNE,puntNE,contNE,heelalNE])
	uniquecont = get_unique_ne(contNE, [lijnNE, bcNE,waterNE,noneNE,regioNE,fictiefNE,landNE,puntNE,heelalNE])
	uniqueheelal = get_unique_ne(heelalNE, [lijnNE, bcNE,waterNE,noneNE,regioNE,fictiefNE,landNE,contNE,puntNE])

	# GET LIST OF UNIQUE BIGRAMS PER SUBCAT
	
	location_subcats = ['PUNT', 'LIJN', 'BC', 'WATER', 'NONE', 'REGIO', 'FICTIEF', 'LAND', 'CONT', 'HEELAL']
	
	punt_pre_bi = []
	lijn_pre_bi = []
	bc_pre_bi = []
	water_pre_bi = []
	none_pre_bi = []
	regio_pre_bi = []
	fictief_pre_bi = []
	land_pre_bi = []
	cont_pre_bi = []
	heelal_pre_bi = []
	
	punt_post_bi = []
	lijn_post_bi = []
	bc_post_bi = []
	water_post_bi = []
	none_post_bi = []
	regio_post_bi = []
	fictief_post_bi = []
	land_post_bi = []
	cont_post_bi = []
	heelal_post_bi = []
	
	org_subcats = ['NONE', 'MISC', 'GOV', 'COM']
	
	org_none_pre_bi = []
	org_misc_pre_bi = []
	gov_pre_bi = []
	com_pre_bi = []
	
	org_none_post_bi = []
	org_misc_post_bi = []
	gov_post_bi = []
	com_post_bi = []
	
	
	lines_for_bigrams = []
	for line in lines:
		if line[0] not in ["DOCUMENT", "SENTENCE"]:
			lines_for_bigrams.append(line)
		elif line[0] == "SENTENCE":
			lines_for_bigrams.append(["fakeID", "fakeMarkable","XXXXXXXX"])
		else:
			continue
	# get list of all word bigrams per subcat
	for i in range(len(lines_for_bigrams)):
		if i < (len(lines_for_bigrams) - 2):
			word1 = lines_for_bigrams[i][2]
			word2 = lines_for_bigrams[(i+1)][2]
			word3 = lines_for_bigrams[(i+2)][2]
			if len(lines_for_bigrams[(i+2)]) == 5:
				cat = lines_for_bigrams[(i+2)][-2]
				subcat = lines_for_bigrams[(i+2)][-1]
				# PRE NE WORDS
				if cat == "LOC":
					if subcat == location_subcats[0]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							punt_pre_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							punt_pre_bi.append(tuple((word1, word2)))
					elif subcat == location_subcats[1]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							lijn_pre_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							lijn_pre_bi.append(tuple((word1, word2)))
					elif subcat == location_subcats[2]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							bc_pre_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							bc_pre_bi.append(tuple((word1, word2)))
					elif subcat == location_subcats[3]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							water_pre_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							water_pre_bi.append(tuple((word1, word2)))
					elif subcat == location_subcats[4]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							none_pre_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							none_pre_bi.append(tuple((word1, word2)))
					elif subcat == location_subcats[5]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							regio_pre_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							regio_pre_bi.append(tuple((word1, word2)))
					elif subcat == location_subcats[6]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							fictief_pre_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							fictief_pre_bi.append(tuple((word1, word2)))
					elif subcat == location_subcats[7]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							land_pre_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							land_pre_bi.append(tuple((word1, word2)))
					elif subcat == location_subcats[8]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							cont_pre_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							cont_pre_bi.append(tuple((word1, word2)))
					elif subcat == location_subcats[9]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							heelal_pre_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							heelal_pre_bi.append(tuple((word1, word2)))
				if cat == "ORG":
					if subcat == org_subcats[0]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							org_none_pre_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							org_none_pre_bi.append(tuple((word1, word2)))
					elif subcat == org_subcats[1]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							org_misc_pre_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							org_misc_pre_bi.append(tuple((word1, word2)))
					elif subcat == org_subcats[2]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							gov_pre_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							gov_pre_bi.append(tuple((word1, word2)))
					elif subcat == org_subcats[3]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							com_pre_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							com_pre_bi.append(tuple((word1, word2)))
			# POST NE WORDS
			if len(lines_for_bigrams[(i)]) == 5:
				cat = lines_for_bigrams[(i)][-2]
				subcat = lines_for_bigrams[(i)][-1]
				if cat == "LOC":
					if subcat == location_subcats[0]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							punt_post_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							punt_post_bi.append(tuple((word2, word3)))
					elif subcat == location_subcats[1]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							lijn_post_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							lijn_post_bi.append(tuple((word2, word3)))
					elif subcat == location_subcats[2]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							bc_post_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							bc_post_bi.append(tuple((word2, word3)))
					elif subcat == location_subcats[3]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							water_post_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							water_post_bi.append(tuple((word2, word3)))
					elif subcat == location_subcats[4]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							none_post_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							none_post_bi.append(tuple((word2, word3)))
					elif subcat == location_subcats[5]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							regio_post_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							regio_post_bi.append(tuple((word2, word3)))
					elif subcat == location_subcats[6]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							fictief_post_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							fictief_post_bi.append(tuple((word2, word3)))
					elif subcat == location_subcats[7]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							land_post_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							land_post_bi.append(tuple((word2, word3)))
					elif subcat == location_subcats[8]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							cont_post_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							cont_post_bi.append(tuple((word2, word3)))
					elif subcat == location_subcats[9]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							heelal_post_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							heelal_post_bi.append(tuple((word2, word3)))
				if cat == "ORG":
					if subcat == org_subcats[0]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							org_none_post_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							org_none_post_bi.append(tuple((word2, word3)))
					elif subcat == org_subcats[1]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							org_misc_post_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							org_misc_post_bi.append(tuple((word2, word3)))
					elif subcat == org_subcats[2]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							gov_post_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							gov_post_bi.append(tuple((word2, word3)))
					elif subcat == org_subcats[3]:
						# first word in new sentence happens to be a NE
						if word2 == "XXXXXXXX":
							com_post_bi.append(tuple(("XXXXXXXX", "XXXXXXXX")))
						else:
							com_post_bi.append(tuple((word2, word3)))
	
	
	
	# set bigram lists to be unique
	punt_pre_bi_un = get_unique_ne(punt_pre_bi, [lijn_pre_bi,bc_pre_bi,water_pre_bi,none_pre_bi,regio_pre_bi,fictief_pre_bi,land_pre_bi,cont_pre_bi,heelal_pre_bi])
	lijn_pre_bi_un = get_unique_ne(lijn_pre_bi, [punt_pre_bi,bc_pre_bi,water_pre_bi,none_pre_bi,regio_pre_bi,fictief_pre_bi,land_pre_bi,cont_pre_bi,heelal_pre_bi])
	bc_pre_bi_un = get_unique_ne(bc_pre_bi, [lijn_pre_bi,punt_pre_bi,water_pre_bi,none_pre_bi,regio_pre_bi,fictief_pre_bi,land_pre_bi,cont_pre_bi,heelal_pre_bi])
	water_pre_bi_un = get_unique_ne(water_pre_bi, [lijn_pre_bi,bc_pre_bi,punt_pre_bi,none_pre_bi,regio_pre_bi,fictief_pre_bi,land_pre_bi,cont_pre_bi,heelal_pre_bi])
	none_pre_bi_un = get_unique_ne(none_pre_bi, [lijn_pre_bi,bc_pre_bi,water_pre_bi,punt_pre_bi,regio_pre_bi,fictief_pre_bi,land_pre_bi,cont_pre_bi,heelal_pre_bi])
	regio_pre_bi_un = get_unique_ne(regio_pre_bi, [lijn_pre_bi,bc_pre_bi,water_pre_bi,none_pre_bi,punt_pre_bi,fictief_pre_bi,land_pre_bi,cont_pre_bi,heelal_pre_bi])
	fictief_pre_bi_un = get_unique_ne(fictief_pre_bi, [lijn_pre_bi,bc_pre_bi,water_pre_bi,none_pre_bi,regio_pre_bi,punt_pre_bi,land_pre_bi,cont_pre_bi,heelal_pre_bi])
	land_pre_bi_un = get_unique_ne(land_pre_bi, [lijn_pre_bi,bc_pre_bi,water_pre_bi,none_pre_bi,regio_pre_bi,fictief_pre_bi,punt_pre_bi,cont_pre_bi,heelal_pre_bi])
	cont_pre_bi_un = get_unique_ne(cont_pre_bi, [lijn_pre_bi,bc_pre_bi,water_pre_bi,none_pre_bi,regio_pre_bi,fictief_pre_bi,land_pre_bi,punt_pre_bi,heelal_pre_bi])
	heelal_pre_bi_un = get_unique_ne(heelal_pre_bi, [lijn_pre_bi,bc_pre_bi,water_pre_bi,none_pre_bi,regio_pre_bi,fictief_pre_bi,land_pre_bi,cont_pre_bi,punt_pre_bi])
	
	punt_post_bi_un = get_unique_ne(punt_post_bi, [lijn_post_bi,bc_post_bi,water_post_bi,none_post_bi,regio_post_bi,fictief_post_bi,land_post_bi,cont_post_bi,heelal_post_bi])
	lijn_post_bi_un = get_unique_ne(lijn_post_bi, [punt_post_bi,bc_post_bi,water_post_bi,none_post_bi,regio_post_bi,fictief_post_bi,land_post_bi,cont_post_bi,heelal_post_bi])
	bc_post_bi_un = get_unique_ne(bc_post_bi, [lijn_post_bi,punt_post_bi,water_post_bi,none_post_bi,regio_post_bi,fictief_post_bi,land_post_bi,cont_post_bi,heelal_post_bi])
	water_post_bi_un = get_unique_ne(water_post_bi, [lijn_post_bi,bc_post_bi,punt_post_bi,none_post_bi,regio_post_bi,fictief_post_bi,land_post_bi,cont_post_bi,heelal_post_bi])
	none_post_bi_un = get_unique_ne(none_post_bi, [lijn_post_bi,bc_post_bi,water_post_bi,punt_post_bi,regio_post_bi,fictief_post_bi,land_post_bi,cont_post_bi,heelal_post_bi])
	regio_post_bi_un = get_unique_ne(regio_post_bi, [lijn_post_bi,bc_post_bi,water_post_bi,none_post_bi,punt_post_bi,fictief_post_bi,land_post_bi,cont_post_bi,heelal_post_bi])
	fictief_post_bi_un = get_unique_ne(fictief_post_bi, [lijn_post_bi,bc_post_bi,water_post_bi,none_post_bi,regio_post_bi,punt_post_bi,land_post_bi,cont_post_bi,heelal_post_bi])
	land_post_bi_un = get_unique_ne(land_post_bi, [lijn_post_bi,bc_post_bi,water_post_bi,none_post_bi,regio_post_bi,fictief_post_bi,punt_post_bi,cont_post_bi,heelal_post_bi])
	cont_post_bi_un = get_unique_ne(cont_post_bi, [lijn_post_bi,bc_post_bi,water_post_bi,none_post_bi,regio_post_bi,fictief_post_bi,land_post_bi,punt_post_bi,heelal_post_bi])
	heelal_post_bi_un = get_unique_ne(heelal_post_bi, [lijn_post_bi,bc_post_bi,water_post_bi,none_post_bi,regio_post_bi,fictief_post_bi,land_post_bi,cont_post_bi,punt_post_bi])
	
	org_none_pre_bi_un = get_unique_ne(org_none_pre_bi, [org_misc_pre_bi,gov_pre_bi,com_pre_bi])
	org_misc_pre_bi_un = get_unique_ne(org_misc_pre_bi, [org_none_pre_bi,gov_pre_bi,com_pre_bi])
	gov_pre_bi_un = get_unique_ne(gov_pre_bi, [org_misc_pre_bi,org_none_pre_bi,com_pre_bi])
	com_pre_bi_un = get_unique_ne(com_pre_bi, [org_misc_pre_bi,gov_pre_bi,org_none_pre_bi])
	
	org_none_post_bi_un = get_unique_ne(org_none_post_bi, [org_misc_post_bi,gov_post_bi,com_post_bi])
	org_misc_post_bi_un = get_unique_ne(org_misc_post_bi, [org_none_post_bi,gov_post_bi,com_post_bi])
	gov_post_bi_un = get_unique_ne(gov_post_bi, [org_misc_post_bi,org_none_post_bi,com_post_bi])
	com_post_bi_un = get_unique_ne(com_post_bi, [org_misc_post_bi,gov_post_bi,org_none_post_bi])
	
	
	# ORGANISATION DATA
	
	org_none= org_misc= gov= com = 0
	org_noneNE=[]
	org_miscNE =[]
	govNE = []
	comNE =[]
	for item in org:
		ne = item[2]
		if item[-1] == org_subcats[0]:
			org_none += 1
			org_noneNE.append(ne)
		elif item[-1] == org_subcats[1]:
			org_misc += 1
			org_miscNE.append(ne)
		elif item[-1] == org_subcats[2]:
			gov += 1
			govNE.append(ne)
		elif item[-1] == org_subcats[3]:
			com += 1
			comNE.append(ne)
	# GET UNIQUE LISTS OF WORDS PER SUBCAT
	uniqueorg_none = get_unique_ne(org_noneNE, [org_miscNE,govNE,comNE])
	uniqueorg_misc = get_unique_ne(org_miscNE, [org_noneNE,govNE,comNE])
	uniquegov = get_unique_ne(govNE, [org_miscNE,org_noneNE,comNE])
	uniquecom = get_unique_ne(comNE, [org_miscNE,govNE,org_noneNE])
	
	# GET unique unigrams for NE word before and word after without stopwords
	punt_pre_si = []
	lijn_pre_si = []
	bc_pre_si = []
	water_pre_si = []
	none_pre_si = []
	regio_pre_si = []
	fictief_pre_si = []
	land_pre_si = []
	cont_pre_si = []
	heelal_pre_si = []
	
	punt_post_si = []
	lijn_post_si = []
	bc_post_si = []
	water_post_si = []
	none_post_si = []
	regio_post_si = []
	fictief_post_si = []
	land_post_si = []
	cont_post_si = []
	heelal_post_si = []
	
	org_none_pre_si = []
	org_misc_pre_si = []
	gov_pre_si = []
	com_pre_si = []
	
	org_none_post_si = []
	org_misc_post_si = []
	gov_post_si = []
	com_post_si = []
	
	
	for i in range(len(lines_for_bigrams)):
		if i < (len(lines_for_bigrams) - 2):
			word1 = lines_for_bigrams[i][2]
			word2 = lines_for_bigrams[(i+1)][2]
			word3 = lines_for_bigrams[(i+2)][2]
			if len(lines_for_bigrams[(i+1)]) == 5:
				cat = lines_for_bigrams[(i+1)][-2]
				subcat = lines_for_bigrams[(i+1)][-1]
				# PRE NE WORDS
				if cat == "LOC":
					if subcat == location_subcats[0]:
						punt_pre_si.append(word1)
						punt_post_si.append(word3)
					elif subcat == location_subcats[1]:
						lijn_pre_si.append(word1)
						lijn_post_si.append(word3)
					elif subcat == location_subcats[2]:
						bc_pre_si.append(word1)
						bc_post_si.append(word3)
					elif subcat == location_subcats[3]:
						water_pre_si.append(word1)
						water_post_si.append(word3)
					elif subcat == location_subcats[4]:
						none_pre_si.append(word1)
						none_post_si.append(word3)
					elif subcat == location_subcats[5]:
						regio_pre_si.append(word1)
						regio_post_si.append(word3)
					elif subcat == location_subcats[6]:
						fictief_pre_si.append(word1)
						fictief_post_si.append(word3)
					elif subcat == location_subcats[7]:
						land_pre_si.append(word1)
						land_post_si.append(word3)
					elif subcat == location_subcats[8]:
						cont_pre_si.append(word1)
						cont_post_si.append(word3)
					elif subcat == location_subcats[9]:
						heelal_pre_si.append(word1)
						heelal_post_si.append(word3)
				if cat == "ORG":
					if subcat == org_subcats[0]:
						org_none_pre_si.append(word1)
						org_none_post_si.append(word3)
					elif subcat == org_subcats[1]:
						org_misc_pre_si.append(word1)
						org_misc_post_si.append(word3)
					elif subcat == org_subcats[2]:
						gov_pre_si.append(word1)
						gov_post_si.append(word3)
					elif subcat == org_subcats[3]:
						com_pre_si.append(word1)
						com_post_si.append(word3)
							
	# set unigram lists to be unique
	punt_pre_si_un = get_unique_ne(punt_pre_si, [lijn_pre_si,bc_pre_si,water_pre_si,none_pre_si,regio_pre_si,fictief_pre_si,land_pre_si,cont_pre_si,heelal_pre_si])
	lijn_pre_si_un = get_unique_ne(lijn_pre_si, [punt_pre_si,bc_pre_si,water_pre_si,none_pre_si,regio_pre_si,fictief_pre_si,land_pre_si,cont_pre_si,heelal_pre_si])
	bc_pre_si_un = get_unique_ne(bc_pre_si, [lijn_pre_si,punt_pre_si,water_pre_si,none_pre_si,regio_pre_si,fictief_pre_si,land_pre_si,cont_pre_si,heelal_pre_si])
	water_pre_si_un = get_unique_ne(water_pre_si, [lijn_pre_si,bc_pre_si,punt_pre_si,none_pre_si,regio_pre_si,fictief_pre_si,land_pre_si,cont_pre_si,heelal_pre_si])
	none_pre_si_un = get_unique_ne(none_pre_si, [lijn_pre_si,bc_pre_si,water_pre_si,punt_pre_si,regio_pre_si,fictief_pre_si,land_pre_si,cont_pre_si,heelal_pre_si])
	regio_pre_si_un = get_unique_ne(regio_pre_si, [lijn_pre_si,bc_pre_si,water_pre_si,none_pre_si,punt_pre_si,fictief_pre_si,land_pre_si,cont_pre_si,heelal_pre_si])
	fictief_pre_si_un = get_unique_ne(fictief_pre_si, [lijn_pre_si,bc_pre_si,water_pre_si,none_pre_si,regio_pre_si,punt_pre_si,land_pre_si,cont_pre_si,heelal_pre_si])
	land_pre_si_un = get_unique_ne(land_pre_si, [lijn_pre_si,bc_pre_si,water_pre_si,none_pre_si,regio_pre_si,fictief_pre_si,punt_pre_si,cont_pre_si,heelal_pre_si])
	cont_pre_si_un = get_unique_ne(cont_pre_si, [lijn_pre_si,bc_pre_si,water_pre_si,none_pre_si,regio_pre_si,fictief_pre_si,land_pre_si,punt_pre_si,heelal_pre_si])
	heelal_pre_si_un = get_unique_ne(heelal_pre_si, [lijn_pre_si,bc_pre_si,water_pre_si,none_pre_si,regio_pre_si,fictief_pre_si,land_pre_si,cont_pre_si,punt_pre_si])
	
	punt_post_si_un = get_unique_ne(punt_post_si, [lijn_post_si,bc_post_si,water_post_si,none_post_si,regio_post_si,fictief_post_si,land_post_si,cont_post_si,heelal_post_si])
	lijn_post_si_un = get_unique_ne(lijn_post_si, [punt_post_si,bc_post_si,water_post_si,none_post_si,regio_post_si,fictief_post_si,land_post_si,cont_post_si,heelal_post_si])
	bc_post_si_un = get_unique_ne(bc_post_si, [lijn_post_si,punt_post_si,water_post_si,none_post_si,regio_post_si,fictief_post_si,land_post_si,cont_post_si,heelal_post_si])
	water_post_si_un = get_unique_ne(water_post_si, [lijn_post_si,bc_post_si,punt_post_si,none_post_si,regio_post_si,fictief_post_si,land_post_si,cont_post_si,heelal_post_si])
	none_post_si_un = get_unique_ne(none_post_si, [lijn_post_si,bc_post_si,water_post_si,punt_post_si,regio_post_si,fictief_post_si,land_post_si,cont_post_si,heelal_post_si])
	regio_post_si_un = get_unique_ne(regio_post_si, [lijn_post_si,bc_post_si,water_post_si,none_post_si,punt_post_si,fictief_post_si,land_post_si,cont_post_si,heelal_post_si])
	fictief_post_si_un = get_unique_ne(fictief_post_si, [lijn_post_si,bc_post_si,water_post_si,none_post_si,regio_post_si,punt_post_si,land_post_si,cont_post_si,heelal_post_si])
	land_post_si_un = get_unique_ne(land_post_si, [lijn_post_si,bc_post_si,water_post_si,none_post_si,regio_post_si,fictief_post_si,punt_post_si,cont_post_si,heelal_post_si])
	cont_post_si_un = get_unique_ne(cont_post_si, [lijn_post_si,bc_post_si,water_post_si,none_post_si,regio_post_si,fictief_post_si,land_post_si,punt_post_si,heelal_post_si])
	heelal_post_si_un = get_unique_ne(heelal_post_si, [lijn_post_si,bc_post_si,water_post_si,none_post_si,regio_post_si,fictief_post_si,land_post_si,cont_post_si,punt_post_si])
	
	org_none_pre_si_un = get_unique_ne(org_none_pre_si, [org_misc_pre_si,gov_pre_si,com_pre_si])
	org_misc_pre_si_un = get_unique_ne(org_misc_pre_si, [org_none_pre_si,gov_pre_si,com_pre_si])
	gov_pre_si_un = get_unique_ne(gov_pre_si, [org_misc_pre_si,org_none_pre_si,com_pre_si])
	com_pre_si_un = get_unique_ne(com_pre_si, [org_misc_pre_si,gov_pre_si,org_none_pre_si])
	
	org_none_post_si_un = get_unique_ne(org_none_post_si, [org_misc_post_si,gov_post_si,com_post_si])
	org_misc_post_si_un = get_unique_ne(org_misc_post_si, [org_none_post_si,gov_post_si,com_post_si])
	gov_post_si_un = get_unique_ne(gov_post_si, [org_misc_post_si,org_none_post_si,com_post_si])
	com_post_si_un = get_unique_ne(com_post_si, [org_misc_post_si,gov_post_si,org_none_post_si])
	
	pro_subcats = ['AANDEEL', 'MISC', 'TAAL']
	for item in pro:
		pro_subcats.append(item[-1])
	
	
	eve_subcats = ['MENS', 'NAT']
	for item in eve:
		eve_subcats.append(item[-1])

	misc_subcats = []
	for item in misc:
		misc_subcats.append(item[-1])
	
	
	print("--------------------STATISTICS----------------------------")
	print("		   LOCATION (total: {})				".format(len(loc)))
	print("PUNT, LIJN, BC, WATER, NONE, REGIO, FICTIEF, LAND, CONT, HEELAL")
	print("{}   {}   {}   {}   {}   {}   {}      {}     {}     {}".format(punt,lijn,bc,water,none,regio,fictief,land,cont,heelal))
	print("\n")
	print("		   ORGANISATION (total: {})				".format(len(org)))
	print("NONE, MISC, GOV, COM")
	print("{}   {}   {}   {}".format(org_none, org_misc, gov, com))
	print("----------------------------------------------------------")
	#print("\n")
	#print("Top ten words in each subcat")
	#print("LOC PUNT: {}".format(at_least_five(puntNE,"puntNE")))
	#print("LOC LIJN: {}".format(at_least_five(lijnNE,"lijnNE")))
	#print("LOC BC: {}".format(at_least_five(bcNE,"bcNE")))
	#print("LOC WATER: {}".format(at_least_five(waterNE,"waterNE")))
	#print("LOC NONE: {}".format(at_least_five(noneNE,"noneNE")))
	#print("LOC REGIO: {}".format(at_least_five(regioNE,"regioNE")))
	#print("LOC FICTIEF: {}".format(at_least_five(fictiefNE,"fictiefNE")))
	#print("LOC LAND: {}".format(at_least_five(landNE,"landNE")))
	#print("LOC CONT: {}".format(at_least_five(contNE,"contNE")))
	#print("LOC HEELAL: {}".format(at_least_five(heelalNE,"heelalNE")))
	#print("\n")
	#print("ORG NONE: {}".format(at_least_five(org_noneNE,"org_noneNE")))
	#print("ORG MISC: {}".format(at_least_five(org_miscNE,"org_miscNE")))
	#print("ORG GOV: {}".format(at_least_five(govNE,"govNE")))
	#print("ORG COM: {}".format(at_least_five(comNE,"comNE")))
	#print("----------------------------------------------------------")
	print("\n")
	print("Top ten words in each subcat AND ONLY IN THAT SUBCAT")
	print("LOC PUNT: {}".format(at_least_five(uniquepunt,"LOC_punt_unique")))
	print("LOC LIJN: {}".format(at_least_five(uniquelijn,"LOC_lijn_unique")))
	print("LOC BC: {}".format(at_least_five(uniquebc,"LOC_bc_unique")))
	print("LOC WATER: {}".format(at_least_five(uniquewater,"LOC_water_unique")))
	print("LOC NONE: {}".format(at_least_five(uniquenone,"LOC_none_unique")))
	print("LOC REGIO: {}".format(at_least_five(uniqueregio,"LOC_regio_unique")))
	print("LOC FICTIEF: {}".format(at_least_five(uniquefictief,"LOC_fictief_unique")))
	print("LOC LAND: {}".format(at_least_five(uniqueland,"LOC_land_unique")))
	print("LOC CONT: {}".format(at_least_five(uniquecont,"LOC_cont_unique")))
	print("LOC HEELAL: {}".format(at_least_five(uniqueheelal,"LOC_heelal_unique")))
	print("\n")
	print("ORG NONE: {}".format(at_least_five(uniqueorg_none,"ORG_none_unique")))
	print("ORG MISC: {}".format(at_least_five(uniqueorg_misc,"ORG_misc_unique")))
	print("ORG GOV: {}".format(at_least_five(uniquegov,"ORG_gov_unique")))
	print("ORG COM: {}".format(at_least_five(uniquecom,"ORG_com_unique")))
	print("----------------------------------------------------------")
	print("\n")
	print("Top ten unique word bigrams in front of NE")
	print("LOC PUNT: {}".format(at_least_five(punt_pre_bi_un,"LOC_punt_pre_bi_un")))
	print("LOC LIJN: {}".format(at_least_five(lijn_pre_bi_un,"LOC_lijn_pre_bi_un")))
	print("LOC BC: {}".format(at_least_five(bc_pre_bi_un,"LOC_bc_pre_bi_un")))
	print("LOC WATER: {}".format(at_least_five(water_pre_bi_un,"LOC_water_pre_bi_un")))
	print("LOC NONE: {}".format(at_least_five(none_pre_bi_un,"LOC_none_pre_bi_un")))
	print("LOC REGIO: {}".format(at_least_five(regio_pre_bi_un,"LOC_regio_pre_bi_un")))
	print("LOC FICTIEF: {}".format(at_least_five(fictief_pre_bi_un,"LOC_fictief_pre_bi_un")))
	print("LOC LAND: {}".format(at_least_five(land_pre_bi_un,"LOC_land_pre_bi_un")))
	print("LOC CONT: {}".format(at_least_five(cont_pre_bi_un,"LOC_cont_pre_bi_un")))
	print("LOC HEELAL: {}".format(at_least_five(heelal_pre_bi_un,"LOC_heelal_pre_bi_un")))
	print("\n")
	print("ORG NONE: {}".format(at_least_five(org_none_pre_bi_un,"ORG_none_pre_bi_un")))
	print("ORG MISC: {}".format(at_least_five(org_misc_pre_bi_un,"ORG_misc_pre_bi_un")))
	print("ORG GOV: {}".format(at_least_five(gov_pre_bi_un,"ORG_gov_pre_bi_un")))
	print("ORG COM: {}".format(at_least_five(com_pre_bi_un,"ORG_com_pre_bi_un")))
	print("----------------------------------------------------------")
	print("\n")
	print("Top ten unique word bigrams after NE")
	print("LOC PUNT: {}".format(at_least_five(punt_post_bi_un,"LOC_punt_post_bi_un")))
	print("LOC LIJN: {}".format(at_least_five(lijn_post_bi_un,"LOC_lijn_post_bi_un")))
	print("LOC BC: {}".format(at_least_five(bc_post_bi_un,"LOC_bc_post_bi_un")))
	print("LOC WATER: {}".format(at_least_five(water_post_bi_un,"LOC_water_post_bi_un")))
	print("LOC NONE: {}".format(at_least_five(none_post_bi_un,"LOC_none_post_bi_un")))
	print("LOC REGIO: {}".format(at_least_five(regio_post_bi_un,"LOC_regio_post_bi_un")))
	print("LOC FICTIEF: {}".format(at_least_five(fictief_post_bi_un,"LOC_fictief_post_bi_un")))
	print("LOC LAND: {}".format(at_least_five(land_post_bi_un,"LOC_land_post_bi_un")))
	print("LOC CONT: {}".format(at_least_five(cont_post_bi_un,"LOC_cont_post_bi_un")))
	print("LOC HEELAL: {}".format(at_least_five(heelal_post_bi_un,"LOC_heelal_post_bi_un")))
	print("\n")
	print("ORG NONE: {}".format(at_least_five(org_none_post_bi_un,"ORG_none_post_bi_un")))
	print("ORG MISC: {}".format(at_least_five(org_misc_post_bi_un,"ORG_misc_post_bi_un")))
	print("ORG GOV: {}".format(at_least_five(gov_post_bi_un,"ORG_gov_post_bi_un")))
	print("ORG COM: {}".format(at_least_five(com_post_bi_un,"ORG_com_post_bi_un")))
	print("----------------------------------------------------------")
	print("\n")
	print("Top ten unique word bigrams before NE")
	print("LOC PUNT: {}".format(at_least_five(punt_pre_si_un,"LOC_punt_pre_si_un")))
	print("LOC LIJN: {}".format(at_least_five(lijn_pre_si_un,"LOC_lijn_pre_si_un")))
	print("LOC BC: {}".format(at_least_five(bc_pre_si_un,"LOC_bc_pre_si_un")))
	print("LOC WATER: {}".format(at_least_five(water_pre_si_un,"LOC_water_pre_si_un")))
	print("LOC NONE: {}".format(at_least_five(none_pre_si_un,"LOC_none_pre_si_un")))
	print("LOC REGIO: {}".format(at_least_five(regio_pre_si_un,"LOC_regio_pre_si_un")))
	print("LOC FICTIEF: {}".format(at_least_five(fictief_pre_si_un,"LOC_fictief_pre_si_un")))
	print("LOC LAND: {}".format(at_least_five(land_pre_si_un,"LOC_land_pre_si_un")))
	print("LOC CONT: {}".format(at_least_five(cont_pre_si_un,"LOC_cont_pre_si_un")))
	print("LOC HEELAL: {}".format(at_least_five(heelal_pre_si_un,"LOC_heelal_pre_si_un")))
	print("\n")
	print("ORG NONE: {}".format(at_least_five(org_none_pre_si_un,"ORG_none_pre_si_un")))
	print("ORG MISC: {}".format(at_least_five(org_misc_pre_si_un,"ORG_misc_pre_si_un")))
	print("ORG GOV: {}".format(at_least_five(gov_pre_si_un,"ORG_gov_pre_si_un")))
	print("ORG COM: {}".format(at_least_five(com_pre_si_un,"ORG_com_pre_si_un")))
	print("----------------------------------------------------------")
	print("\n")
	print("Top ten unique word unigrams after NE")
	print("LOC PUNT: {}".format(at_least_five(punt_post_si_un,"LOC_punt_post_si_un")))
	print("LOC LIJN: {}".format(at_least_five(lijn_post_si_un,"LOC_lijn_post_si_un")))
	print("LOC BC: {}".format(at_least_five(bc_post_si_un,"LOC_bc_post_si_un")))
	print("LOC WATER: {}".format(at_least_five(water_post_si_un,"LOC_water_post_si_un")))
	print("LOC NONE: {}".format(at_least_five(none_post_si_un,"LOC_none_post_si_un")))
	print("LOC REGIO: {}".format(at_least_five(regio_post_si_un,"LOC_regio_post_si_un")))
	print("LOC FICTIEF: {}".format(at_least_five(fictief_post_si_un,"LOC_fictief_post_si_un")))
	print("LOC LAND: {}".format(at_least_five(land_post_si_un,"LOC_land_post_si_un")))
	print("LOC CONT: {}".format(at_least_five(cont_post_si_un,"LOC_cont_post_si_un")))
	print("LOC HEELAL: {}".format(at_least_five(heelal_post_si_un,"LOC_heelal_post_si_un")))
	print("\n")
	print("ORG NONE: {}".format(at_least_five(org_none_post_si_un,"ORG_none_post_si_un")))
	print("ORG MISC: {}".format(at_least_five(org_misc_post_si_un,"ORG_misc_post_si_un")))
	print("ORG GOV: {}".format(at_least_five(gov_post_si_un,"ORG_gov_post_si_un")))
	print("ORG COM: {}".format(at_least_five(com_post_si_un,"ORG_com_post_si_un")))
	print("----------------------------------------------------------")
	
	'''

	counter_list = []
	for k,v in feature_dict.items():
		joined_v = []
		
		for item in v:
			if type(item) == list:
				for l_i in item:
					joined_v.append(l_i)
			else:
				joined_v.append(item)
		lenght = len(joined_v)	
		counter_list.append(tuple((k, lenght)))
		if k == "cont":
			print("\n")
			print(joined_v)
	print("\n")
	print(counter_list)	
	print("--------------------STATISTICS----------------------------")
	print("		   LOCATION (total: {})				".format(len(loc)))
	print("PUNT, LIJN, BC, WATER, NONE, REGIO, FICTIEF, LAND, CONT, HEELAL")
	print("{}   {}   {}   {}   {}   {}   {}      {}     {}     {}".format(punt,lijn,bc,water,none,regio,fictief,land,cont,heelal))
	print("\n")
	print("		   ORGANISATION (total: {})				".format(len(org)))
	print("NONE, MISC, GOV, COM")
	print("{}   {}   {}   {}".format(org_none, org_misc, gov, com))
	print("----------------------------------------------------------")
	'''

	#print("\n")
	#for key,v in feature_dict_per_subcat.items():
	#	print(key)
	
	
	f = open("initial_DL.pkl","wb")
	pickle.dump(feature_dict_per_subcat,f)
	f.close()


if __name__ == '__main__':
	main()


