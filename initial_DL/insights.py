def main():
	infile = open("../data/SoNaR1_training.txt", "r")
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
	for item in org:
		if item[-1] == org_subcats[0]:
			org_none += 1
		elif item[-1] == org_subcats[1]:
			org_misc += 1
		elif item[-1] == org_subcats[2]:
			gov += 1
		elif item[-1] == org_subcats[3]:
			com += 1

	
	pro_subcats = ['AANDEEL', 'MISC', 'TAAL']
	for item in pro:
		pro_subcats.append(item[-1])
	print(set(pro_subcats))
	
	eve_subcats = ['MENS', 'NAT']
	for item in eve:
		eve_subcats.append(item[-1])
	print(set(eve_subcats))

	misc_subcats = []
	for item in misc:
		misc_subcats.append(item[-1])
	print(set(misc_subcats))
	
	print("--------------------STATISTICS----------------------------")
	print("		   LOCATION (total: {})				".format(len(loc)))
	print("PUNT, LIJN, BC, WATER, NONE, REGIO, FICTIEF, LAND, CONT, HEELAL")
	print("{}   {}   {}   {}   {}   {}   {}      {}     {}     {}".format(punt,lijn,bc,water,none,regio,fictief,land,cont,heelal))
	print("\n")
	print("		   ORGANISATION (total: {})				".format(len(org)))
	print("NONE, MISC, GOV, COM")
	print("{}   {}   {}   {}".format(org_none, org_misc, gov, com))
	print("----------------------------------------------------------")
	
	

	
if __name__ == '__main__':
	main()


