from collections import Counter
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stopwords = stopwords.words('dutch')

def get_unique_ne(ne_list, othercat_lists):
	other = set([j for i in othercat_lists for j in i])
	unique_list = []
	for item in ne_list:
		if item in other:
			continue
		else:
			unique_list.append(item)
	return unique_list
	
	
	

def main():
	infile = open("../data/SoNaR1_training.txt", "r",encoding="utf8")
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
	print("\n")
	print("Top ten words in each subcat")
	print("LOC PUNT: {}".format(Counter(puntNE).most_common(10)))
	print("LOC LIJN: {}".format(Counter(lijnNE).most_common(10)))
	print("LOC BC: {}".format(Counter(bcNE).most_common(10)))
	print("LOC WATER: {}".format(Counter(waterNE).most_common(10)))
	print("LOC NONE: {}".format(Counter(noneNE).most_common(10)))
	print("LOC REGIO: {}".format(Counter(regioNE).most_common(10)))
	print("LOC FICTIEF: {}".format(Counter(fictiefNE).most_common(10)))
	print("LOC LAND: {}".format(Counter(landNE).most_common(10)))
	print("LOC CONT: {}".format(Counter(contNE).most_common(10)))
	print("LOC HEELAL: {}".format(Counter(heelalNE).most_common(10)))
	print("\n")
	print("ORG NONE: {}".format(Counter(org_noneNE).most_common(10)))
	print("ORG MISC: {}".format(Counter(org_miscNE).most_common(10)))
	print("ORG GOV: {}".format(Counter(govNE).most_common(10)))
	print("ORG COM: {}".format(Counter(comNE).most_common(10)))
	print("----------------------------------------------------------")
	print("\n")
	print("Top ten words in each subcat AND ONLY IN THAT SUBCAT")
	print("LOC PUNT: {}".format(Counter(uniquepunt).most_common(10)))
	print("LOC LIJN: {}".format(Counter(uniquelijn).most_common(10)))
	print("LOC BC: {}".format(Counter(uniquebc).most_common(10)))
	print("LOC WATER: {}".format(Counter(uniquewater).most_common(10)))
	print("LOC NONE: {}".format(Counter(uniquenone).most_common(10)))
	print("LOC REGIO: {}".format(Counter(uniqueregio).most_common(10)))
	print("LOC FICTIEF: {}".format(Counter(uniquefictief).most_common(10)))
	print("LOC LAND: {}".format(Counter(uniqueland).most_common(10)))
	print("LOC CONT: {}".format(Counter(uniquecont).most_common(10)))
	print("LOC HEELAL: {}".format(Counter(uniqueheelal).most_common(10)))
	print("\n")
	print("ORG NONE: {}".format(Counter(uniqueorg_none).most_common(10)))
	print("ORG MISC: {}".format(Counter(uniqueorg_misc).most_common(10)))
	print("ORG GOV: {}".format(Counter(uniquegov).most_common(10)))
	print("ORG COM: {}".format(Counter(uniquecom).most_common(10)))
	print("----------------------------------------------------------")
	print("\n")
	print("Top ten unique word bigrams in front of NE")
	print("LOC PUNT: {}".format(Counter(punt_pre_bi_un).most_common(10)))
	print("LOC LIJN: {}".format(Counter(lijn_pre_bi_un).most_common(10)))
	print("LOC BC: {}".format(Counter(bc_pre_bi_un).most_common(10)))
	print("LOC WATER: {}".format(Counter(water_pre_bi_un).most_common(10)))
	print("LOC NONE: {}".format(Counter(none_pre_bi_un).most_common(10)))
	print("LOC REGIO: {}".format(Counter(regio_pre_bi_un).most_common(10)))
	print("LOC FICTIEF: {}".format(Counter(fictief_pre_bi_un).most_common(10)))
	print("LOC LAND: {}".format(Counter(land_pre_bi_un).most_common(10)))
	print("LOC CONT: {}".format(Counter(cont_pre_bi_un).most_common(10)))
	print("LOC HEELAL: {}".format(Counter(heelal_pre_bi_un).most_common(10)))
	print("\n")
	print("ORG NONE: {}".format(Counter(org_none_pre_bi_un).most_common(10)))
	print("ORG MISC: {}".format(Counter(org_misc_pre_bi_un).most_common(10)))
	print("ORG GOV: {}".format(Counter(gov_pre_bi_un).most_common(10)))
	print("ORG COM: {}".format(Counter(com_pre_bi_un).most_common(10)))
	print("----------------------------------------------------------")
	print("\n")
	print("Top ten unique word bigrams after NE")
	print("LOC PUNT: {}".format(Counter(punt_post_bi_un).most_common(10)))
	print("LOC LIJN: {}".format(Counter(lijn_post_bi_un).most_common(10)))
	print("LOC BC: {}".format(Counter(bc_post_bi_un).most_common(10)))
	print("LOC WATER: {}".format(Counter(water_post_bi_un).most_common(10)))
	print("LOC NONE: {}".format(Counter(none_post_bi_un).most_common(10)))
	print("LOC REGIO: {}".format(Counter(regio_post_bi_un).most_common(10)))
	print("LOC FICTIEF: {}".format(Counter(fictief_post_bi_un).most_common(10)))
	print("LOC LAND: {}".format(Counter(land_post_bi_un).most_common(10)))
	print("LOC CONT: {}".format(Counter(cont_post_bi_un).most_common(10)))
	print("LOC HEELAL: {}".format(Counter(heelal_post_bi_un).most_common(10)))
	print("\n")
	print("ORG NONE: {}".format(Counter(org_none_post_bi_un).most_common(10)))
	print("ORG MISC: {}".format(Counter(org_misc_post_bi_un).most_common(10)))
	print("ORG GOV: {}".format(Counter(gov_post_bi_un).most_common(10)))
	print("ORG COM: {}".format(Counter(com_post_bi_un).most_common(10)))
	print("----------------------------------------------------------")
	print("\n")
	print("Top ten unique word bigrams before NE")
	print("LOC PUNT: {}".format(Counter(punt_pre_si_un).most_common(10)))
	print("LOC LIJN: {}".format(Counter(lijn_pre_si_un).most_common(10)))
	print("LOC BC: {}".format(Counter(bc_pre_si_un).most_common(10)))
	print("LOC WATER: {}".format(Counter(water_pre_si_un).most_common(10)))
	print("LOC NONE: {}".format(Counter(none_pre_si_un).most_common(10)))
	print("LOC REGIO: {}".format(Counter(regio_pre_si_un).most_common(10)))
	print("LOC FICTIEF: {}".format(Counter(fictief_pre_si_un).most_common(10)))
	print("LOC LAND: {}".format(Counter(land_pre_si_un).most_common(10)))
	print("LOC CONT: {}".format(Counter(cont_pre_si_un).most_common(10)))
	print("LOC HEELAL: {}".format(Counter(heelal_pre_si_un).most_common(10)))
	print("\n")
	print("ORG NONE: {}".format(Counter(org_none_pre_si_un).most_common(10)))
	print("ORG MISC: {}".format(Counter(org_misc_pre_si_un).most_common(10)))
	print("ORG GOV: {}".format(Counter(gov_pre_si_un).most_common(10)))
	print("ORG COM: {}".format(Counter(com_pre_si_un).most_common(10)))
	print("----------------------------------------------------------")
	print("\n")
	print("Top ten unique word unigrams after NE")
	print("LOC PUNT: {}".format(Counter(punt_post_si_un).most_common(10)))
	print("LOC LIJN: {}".format(Counter(lijn_post_si_un).most_common(10)))
	print("LOC BC: {}".format(Counter(bc_post_si_un).most_common(10)))
	print("LOC WATER: {}".format(Counter(water_post_si_un).most_common(10)))
	print("LOC NONE: {}".format(Counter(none_post_si_un).most_common(10)))
	print("LOC REGIO: {}".format(Counter(regio_post_si_un).most_common(10)))
	print("LOC FICTIEF: {}".format(Counter(fictief_post_si_un).most_common(10)))
	print("LOC LAND: {}".format(Counter(land_post_si_un).most_common(10)))
	print("LOC CONT: {}".format(Counter(cont_post_si_un).most_common(10)))
	print("LOC HEELAL: {}".format(Counter(heelal_post_si_un).most_common(10)))
	print("\n")
	print("ORG NONE: {}".format(Counter(org_none_post_si_un).most_common(10)))
	print("ORG MISC: {}".format(Counter(org_misc_post_si_un).most_common(10)))
	print("ORG GOV: {}".format(Counter(gov_post_si_un).most_common(10)))
	print("ORG COM: {}".format(Counter(com_post_si_un).most_common(10)))
	print("----------------------------------------------------------")
	
	
	
	
if __name__ == '__main__':
	main()


