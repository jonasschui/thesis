from collections import Counter

def main():
	infile = open("../data/SoNaR1_training.txt", "r",encoding="utf8")
	main_cats = ["PER", "LOC" , "ORG" , "PRO", "EVE", "MISC"]
	per = []
	loc = []
	org = []
	eve = []
	pro = []
	misc = []
	for line in infile:
		line = line.rstrip().split()
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
		ne = ' '.join(item[2:-2]).lower().rstrip()
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
		
	org_subcats = ['NONE', 'MISC', 'GOV', 'COM']
	org_none= org_misc= gov= com = 0
	org_noneNE=[]
	org_miscNE =[]
	govNE = []
	comNE =[]
	for item in org:
		ne = ' '.join(item[2:-2]).lower().rstrip()
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
	
	

	
if __name__ == '__main__':
	main()


