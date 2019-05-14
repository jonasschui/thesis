import pickle
from collections import defaultdict
from collections import Counter
from heapq import nlargest

def label_ne(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, main_cat, decision_list):
	# check which main cat it belongs to
	candidate_tags = []
	if main_cat == "LOC":
		# keys are every subcat and their values
		for key, value in decision_list.items():
			if main_cat == key[:3]:
				# bi, si or unique(shown as subcat name)
				bi_or_si = key.split("_")[-2]
				# the specific name of the feature without category mentioned
				feat = "_".join(key.split("_")[2:])
				# the subcategory the feature is in
				subcat = key.split("_")[1]

				# working with list of tuples ((bigram), weight)
				
				if bi_or_si == "bi":
					for item in value:
						bigram = item[0]
						weight = item[1]
						# see if there is a match in bigram features
						if feat == "post_bi_un":
							# see if the feature given matches a feature in the dictionary
							if post_bi_un == bigram:
								candidate_tags.append(tuple((subcat, weight)))
						elif feat == "pre_bi_un": 
							if pre_bi_un == bigram:
								candidate_tags.append(tuple((subcat, weight)))

				# working with list of tuples (string, weight)
				else:
					for item in value:
						string = item[0]
						weight = item[1]
						# see if there is a match in unigram of ne features
						#print(key, string, weight)
						if feat == "post_si_un":
							if post_si_un == string:
								candidate_tags.append(tuple((subcat, weight)))
						elif feat == "pre_si_un": 
							if pre_si_un == string: 
								candidate_tags.append(tuple((subcat, weight)))
						elif feat == "unique":
							if ne == string:
								candidate_tags.append(tuple((subcat, weight)))
		w = 0
		if len(candidate_tags) > 0:
			for tag, weighted in candidate_tags:
				if weighted >= w:
					label = tag
					w = weighted
		else:
			label = "none_found"
		# add feature to certain subcategory
		return label
	
	if main_cat == "ORG":
		# keys are every subcat and their values
		for key, value in decision_list.items():
			if main_cat == key[:3]:
				# bi, si or unique(shown as subcat name)
				bi_or_si = key.split("_")[-2]
				# the specific name of the feature without category mentioned
				feat = "_".join(key.split("_")[2:])
				# the subcategory the feature is in
				subcat = key.split("_")[1]

				# working with list of tuples ((bigram), weight)
				
				if bi_or_si == "bi":
					for item in value:
						bigram = item[0]
						weight = item[1]
						# see if there is a match in bigram features
						if feat == "post_bi_un":
							# see if the feature given matches a feature in the dictionary
							if post_bi_un == bigram:
								candidate_tags.append(tuple((subcat, weight)))
						elif feat == "pre_bi_un": 
							if pre_bi_un == bigram:
								candidate_tags.append(tuple((subcat, weight)))

				# working with list of tuples (string, weight)
				else:
					for item in value:
						string = item[0]
						weight = item[1]
						# see if there is a match in unigram of ne features
						#print(key, string, weight)
						if feat == "post_si_un":
							if post_si_un == string:
								candidate_tags.append(tuple((subcat, weight)))
						elif feat == "pre_si_un": 
							if pre_si_un == string: 
								candidate_tags.append(tuple((subcat, weight)))
						elif feat == "unique":
							if ne == string:
								candidate_tags.append(tuple((subcat, weight)))
		w = 0
		if len(candidate_tags) > 0:
			for tag, weighted in candidate_tags:
				if weighted >= w:
					label = tag
					w = weighted
		else:
			label = "none_found"
		return label
	


def load_final_DL():
	pickle_in = open("../data/final_DL.pkl","rb")
	final_DL = pickle.load(pickle_in)
	return final_DL

def precision(match, no_match):
	if no_match == 0:
		return 1
	precision = (match/(match+no_match))
	return precision
	
def recall(match, present):
	if present == 0:
		return 1
	recall = (match/present)
	return recall

def main():
	final_DL = load_final_DL()
	lines = []
	infile = open("../data/using_development/SoNaR1_dev.txt", "r",encoding="utf8")
	next(infile)
	for line in infile:
		line = line.rstrip().split("\t")
		if line[0] != "DOCUMENT":
			lines.append(line)
		
	no_match_org = 0
	no_match_loc = 0
	match_org = 0
	match_loc = 0
	
	punt_match = 0				
	lijn_match = 0
	bc_match = 0
	water_match = 0
	none_match = 0
	regio_match = 0
	fictief_match = 0
	land_match = 0
	cont_match = 0
	heelal_match = 0
	
	punt_no_match = 0				
	lijn_no_match = 0
	bc_no_match = 0
	water_no_match = 0
	none_no_match = 0
	regio_no_match = 0
	fictief_no_match = 0
	land_no_match = 0
	cont_no_match = 0
	heelal_no_match = 0
	
	punt_present = 0
	lijn_present = 0
	bc_present = 0
	water_present = 0
	none_present = 0
	regio_present = 0
	fictief_present = 0
	land_present = 0
	cont_present = 0
	heelal_present = 0
	loc_present = 0
	
	org_misc_match = 0				
	com_match = 0
	gov_match = 0
	org_none_match = 0
	
	org_misc_no_match = 0				
	com_no_match = 0
	gov_no_match = 0
	org_none_no_match = 0
	
	none_found = 0
	
	com_present = 0
	org_misc_present = 0
	gov_present = 0
	org_none_present = 0
	org_present = 0

	
	for i in range((len(lines)-4)):
		line_one = lines[i]
		line_two = lines[(i+1)]
		line_three = lines[(i+2)]
		line_four = lines[(i+3)]
		line_five = lines[(i+4)]
		
		# step2: when NE found try to label it using decision list
		# when able to label ne save feature information in temporary decision list
		if i == 0:
			# do for the two three lines in the file, then switch to the 3rdline for information
			if len(line_one) == 5 and line_one[0] != "SENTENCE":
				main_cat = line_one[3]
				if line_two[0] == 'SENTENCE':
					line_two = ["XXXXXXXX","XXXXXXXX","XXXXXXXX"]
					line_three = ["XXXXXXXX","XXXXXXXX","XXXXXXXX"]
				if line_three[0] == 'SENTENCE':
					line_three = ["XXXXXXXX","XXXXXXXX","XXXXXXXX"]
				ne = line_one[2]
				post_bi_un =  tuple((line_two[2], line_three[2]))
				pre_bi_un = tuple(("XXXXXXXX", "XXXXXXXX"))
				post_si_un = line_two[2]
				pre_si_un = "XXXXXXXX"				
				
				# label the NE
				label = label_ne(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, main_cat, final_DL)
				#print(line_one, label)
					
					
		elif i == 1:
			if len(line_two) == 5 and line_two[0] != "SENTENCE":
				main_cat = line_two[3]
				if line_three[0] == "SENTENCE":
					line_three = ["XXXXXXXX","XXXXXXXX","XXXXXXXX"]
					line_four = ["XXXXXXXX","XXXXXXXX","XXXXXXXX"]
				if line_four[0] == "SENTENCE":
					line_four = ["XXXXXXXX","XXXXXXXX","XXXXXXXX"]

				ne = line_two[2]
				post_bi_un =  tuple((line_three[2], line_four[2]))
				pre_bi_un = tuple(("XXXXXXXX", line_one[2]))
				post_si_un = line_four[2]
				pre_si_un = line_one[2]

				# label the NE
				label = label_ne(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, main_cat, final_DL)
				#print(line_two, label)
					
			
					
		# for the rest of the document
		else:
			if len(line_three) == 5 and line_three[0] != "SENTENCE":
				main_cat = line_three[3]
				if line_one[0] == "SENTENCE":
					line_one = ["XXXXXXXX","XXXXXXXX","XXXXXXXX"]
				if line_two[0] == "SENTENCE":
					line_one = ["XXXXXXXX","XXXXXXXX","XXXXXXXX"]
					line_two = ["XXXXXXXX","XXXXXXXX","XXXXXXXX"]
				if line_four[0] == "SENTENCE":
					line_four = ["XXXXXXXX","XXXXXXXX","XXXXXXXX"]
					line_five = ["XXXXXXXX","XXXXXXXX","XXXXXXXX"]
				if line_five[0] == "SENTENCE":
					line_five = ["XXXXXXXX","XXXXXXXX","XXXXXXXX"]

				ne = line_three[2]
				post_bi_un =  tuple((line_four[2], line_five[2]))
				pre_bi_un = tuple((line_one[2], line_two[2]))
				post_si_un = line_four[2]
				pre_si_un = line_two[2]
				
				# label the NE
				string_list = []
				for item in ["punt","lijn","bc","water","none","regio","fictief","land","cont","heelal","ORG_none","ORG_misc","gov","com"]:
					string_list.append(item.upper())
				label = label_ne(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, main_cat, final_DL)
				if label == "none_found":
					none_found += 1
				if main_cat == "LOC":
					label = label.upper()
					subcat = line_three[-1].upper()
					if subcat == label:
						if label == "PUNT":
							punt_match += 1
						elif label == "LIJN":
							lijn_match += 1
						elif label == "BC":
							bc_match += 1
						elif label == "WATER":
							water_match += 1
						elif label == "NONE":
							none_match += 1
						elif label == "REGIO":
							regio_match += 1
						elif label == "FICTIEF":
							fictief_match += 1
						elif label == 'LAND':
							land_match += 1
						elif label == 'CONT':
							cont_match += 1
						elif label == 'HEELAL':
							heelal_match += 1
						else:
							print(label)
						match_loc += 1
					else:
						if label == "PUNT":
							punt_no_match += 1
						elif label == "LIJN":
							lijn_no_match += 1
						elif label == "BC":
							bc_no_match += 1
						elif label == "WATER":
							water_no_match += 1
						elif label == "NONE":
							none_no_match += 1
						elif label == "REGIO":
							regio_no_match += 1
						elif label == "FICTIEF":
							ficitef_no_match += 1
						elif label == 'LAND':
							land_no_match += 1
						elif label == 'CONT':
							cont_no_match += 1
						elif label == 'HEELAL':
							heelal_no_match += 1
						no_match_loc += 1
					if subcat == "PUNT":
						punt_present += 1
					elif subcat == "LIJN":
						lijn_present += 1
					elif subcat == "BC":
						bc_present += 1
					elif subcat == "WATER":
						water_present += 1
					elif subcat == "NONE":
						none_present += 1
					elif subcat == "REGIO":
						regio_present += 1
					elif subcat == "FICTIEF":
						fictief_present += 1
					elif subcat == 'LAND':
						land_present += 1
					elif subcat == 'CONT':
						cont_present += 1
					elif subcat == 'HEELAL':
						heelal_present += 1
					loc_present += 1
						
				if main_cat == "ORG":
					label = label.upper()
					subcat = line_three[-1].upper()
					if subcat == label:
						if label == "MISC":
							org_misc_match += 1
						elif label == "COM":
							com_match += 1
						elif label == "GOV":
							gov_match += 1
						elif label == "NONE":
							org_none_match += 1
						match_org += 1
					else:
						if subcat == "MISC":
							org_misc_no_match += 1
						elif subcat == "COM":
							com_no_match += 1
						elif subcat == "GOV":
							gov_no_match += 1
						elif subcat == "NONE":
							org_none_no_match += 1
						no_match_org += 1
					if subcat == "MISC":
						org_misc_present += 1
					elif subcat == "COM":
						com_present += 1
					elif subcat == "GOV":
						gov_present += 1
					elif subcat == "NONE":
						org_none_present += 1
					org_present += 1
	print("LOC \n")
	print("LOC matches = {}, no_matches = {} ,present = {}, precision = {}, recall = {}  \n".format(match_loc, no_match_loc,loc_present, precision(match_loc, no_match_loc), recall(match_loc,loc_present)))
	print("PUNT matches = {}, no_matches = {},present = {}, precision = {}, recall = {} \n".format(punt_match, punt_no_match,punt_present, precision(punt_match, punt_no_match), recall(punt_match,punt_present)))
	print("LIJN matches = {}, no_matches = {},present = {}, precision = {}, recall = {} \n".format(lijn_match, lijn_no_match,lijn_present, precision(lijn_match, lijn_no_match), recall(lijn_match,lijn_present)))
	print("BC matches = {}, no_matches = {},present = {}, precision = {}, recall = {} \n".format(bc_match, bc_no_match,bc_present, precision(bc_match, bc_no_match), recall(bc_match,bc_present)))
	print("WATER matches = {}, no_matches = {},present = {}, precision = {}, recall = {} \n".format(water_match, water_no_match,water_present, precision(water_match, water_no_match), recall(water_match,water_present)))
	print("NONE matches = {}, no_matches = {},present = {}, precision = {}, recall = {} \n".format(none_match, none_no_match,none_present, precision(none_match, none_no_match), recall(none_match,none_present)))
	print("REGIO matches = {}, no_matches = {},present = {}, precision = {}, recall = {} \n".format(regio_match, regio_no_match,regio_present, precision(regio_match, regio_no_match), recall(regio_match,regio_present)))
	print("FICTIEF matches = {}, no_matches = {},present = {}, precision = {}, recall = {} \n".format(fictief_match, fictief_no_match,fictief_present, precision(fictief_match, fictief_no_match), recall(fictief_match,fictief_present)))
	print("LAND matches = {}, no_matches = {},present = {}, precision = {}, recall = {} \n".format(land_match, land_no_match,land_present, precision(land_match, land_no_match), recall(land_match,land_present)))
	print("CONT matches = {}, no_matches = {},present = {}, precision = {}, recall = {} \n".format(cont_match, cont_no_match,cont_present, precision(cont_match, cont_no_match), recall(cont_match,cont_present)))
	print("HEELAL matches = {}, no_matches = {},present = {}, precision = {}, recall = {} \n".format(heelal_match, heelal_no_match, heelal_present, precision(heelal_match, heelal_no_match), recall(heelal_match, heelal_present)))

	print("\n ORG \n") 
	print("ORG matches = {}, no_matches = {},present = {}, precision = {}, recall = {} \n".format(match_org, no_match_org,org_present, precision(match_org, no_match_org), recall(match_org,org_present)))
	print("MISC matches = {}, no_matches = {},present = {}, precision = {}, recall = {} \n".format(org_misc_match, org_misc_no_match,org_misc_present, precision(org_misc_match, org_misc_no_match), recall(org_misc_match,org_misc_present)))
	print("COM matches = {}, no_matches = {},present = {}, precision = {}, recall = {} \n".format(com_match, com_no_match,com_present, precision(com_match, com_no_match), recall(com_match,com_present)))
	print("GOV matches = {}, no_matches = {},present = {}, precision = {}, recall = {} \n".format(gov_match, gov_no_match,gov_present, precision(gov_match, gov_no_match), recall(gov_match,gov_present)))
	print("NONE matches = {}, no_matches = {},present = {}, precision = {}, recall = {} \n".format(org_none_match, org_none_no_match,org_none_present, precision(org_none_match, org_none_no_match), recall(org_none_match,org_none_present)))
	#print("ORG matches = {}, no_matches = {} \n".format(match_org, no_match_org))
	
	for key, value in final_DL.items():
		subcat = key.split("_")[1]
		if subcat == "misc":
			print(key, value)
	
	print(none_found)

if __name__ == '__main__':
	main()
