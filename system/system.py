import pickle
from collections import defaultdict

# open the initial decision list made in insights.py
def load_initial_DL():
	pickle_in = open("../initial_DL/initial_DL.pkl","rb")
	initial_DL = pickle.load(pickle_in)
	return initial_DL
'''
def label_ne(unique,post_bi_un,pre_bi_un,post_si_un,pre_si_un, decision_list):
	# label and grab features to temporary list
	# step 1: check to see if feature occurs in the decision list
	# when occurences are found take the label with the highest weight
	# add all the features to the temporary decision list to the corresponding subcategory as feature
	# weigh the features in the temprorary decision list
	# filter the temporary decision list taking the top n weighted features
	# add the top n features per subcategory to the initial decision list including weight
	# label the data using the new decision list
	# return the newly labeled data
	return True
'''

def weigh_features(temporary_DL):
	return True

def label_ne(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, decision_list, main_cat):
	# check which main cat it belongs to
	if main_cat == "LOC":
		# CAT_subcat_featurename, list
		# keys are every subcat and their values
		for key, value in decision_list.items():
			if main_cat == key[:3]:
				feat = key[-5:-3]
				# working with list of tuples ((bigram), weight)
				if feat == "bi":
					for bigram, weigth in value:
						#print(key, bigram, weigth)
						continue
				# working with list of tuples (string, weight)
				else:
					for string, weight in value:
						#print(key, string, weight)
						continue
				#for item in value:
					#print(item)
					#if type(item) == "list":
					#	print(key[3:8])
					#else:
						#print("nolist", key[3:8])
					#	continue
	if main_cat == "ORG":
		for key, value in decision_list.items():
			if main_cat == key[:3]:
				print(main_cat)
	# add feature to certain subcategory
	return True

def send_to_subcat(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, main_cat, decision_list):
	label = label_ne(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, decision_list, main_cat)
	return dic_item

def retrieve_new_features(decision_list, lines):
	temporary_DL = defaultdict(list)
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
				temp_dic_item = send_to_subcat(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, main_cat, decision_list)
				
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
				temp_dic_item = send_to_subcat(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, main_cat, decision_list)
				
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
				temp_dic_item = send_to_subcat(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, main_cat, decision_list)

	new_features = weigh_features(temporary_DL)
	return new_features

def main():
	# read in intitial decision list as dictionary
	# key = CAT_subcat_featurename, value = list of features
	initial_DL = load_initial_DL()
	for key, value in initial_DL.items():
		if key == "LOC_land_unique":
			print(key, value)
	list_of_feature_keys = initial_DL.keys()
	# add weight of 1 for initial decision list items
	for key, value in initial_DL.items():
		weight = float(1)
		weighted_feats = []
		for feature in value:
			feature = tuple((feature, weight))
			weighted_feats.append(feature)
		initial_DL[key] = weighted_feats

	# list of feature names
	feat_names = ['post_bi_un', 'post_si_un', 'pre_si_un', 'pre_bi_un', 'unique']

	# read in dataset
	lines = []
	infile = open("../data/using_development/SoNaR1_dev.txt", "r",encoding="utf8")
	next(infile)
	for line in infile:
		line = line.rstrip().split("\t")
		if line[0] != "DOCUMENT":
			lines.append(line)

	# step1: iterate through data in search of NE
	counter = 0
	retrieve_new_features(initial_DL, lines)

	
	
	# step 3: choose top features from temporary decision list
	# add top features to the main decision list

	# step 4: iterate through data and label NE's that have not yet been labeled using main decision list
	# when able to label ne save feature information in temporary decision list

	# step 5: go back to step 3 until ceratin threshold is achieved

	# step 6: label every NE that does not have a label yet 
	
if __name__ == '__main__':
	main()
