import pickle
from collections import defaultdict
from collections import Counter
from heapq import nlargest

#from nltk.corpus import stopwords
#import nltk
#nltk.download('stopwords')
#stopwords = stopwords.words('dutch')

# open the initial decision list made in insights.py
def load_initial_DL():
	pickle_in = open("../initial_DL/initial_DL.pkl","rb")
	initial_DL = pickle.load(pickle_in)
	return initial_DL

def label_ne(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, decision_list, main_cat, mode):
	# check which main cat it belongs to
	candidate_tags = []
	retrieved_features = defaultdict(list)
	counter = 0
	match_found = False
	if main_cat == "LOC":
		remove_feats = []
		# CAT_subcat_featurename, list
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
								match_found = True
								remove_feats.append("post_bi_un")
						elif feat == "pre_bi_un": 
							if pre_bi_un == bigram:
								candidate_tags.append(tuple((subcat, weight)))
								match_found = True
								remove_feats.append("pre_bi_un")

				# working with list of tuples (string, weight)
				else:
					for item in value:
						string = item[0]
						weight = item[1]
						# see if there is a match in unigram or ne features
						if feat == "post_si_un":
							#if string not in stopwords:
							if post_si_un == string:
								candidate_tags.append(tuple((subcat, weight)))
								match_found = True
								remove_feats.append("post_si_un")
						elif feat == "pre_si_un": 
							#if string not in stopwords:
							if pre_si_un == string: 
								candidate_tags.append(tuple((subcat, weight)))
								match_found = True
								remove_feats.append("pre_si_un")
						elif feat == "unique":
							if ne == string:
								candidate_tags.append(tuple((subcat, weight)))
								match_found = True
								remove_feats.append("unique")
		w = 0
		if len(candidate_tags) > 0:
			for tag, weighted in candidate_tags:
				if weighted >= w:
					label = tag
					w = weighted
			feat_already_in_dict = []
			for item in set(remove_feats):
				featname = "LOC_{}_{}".format(label, item)
				feat_already_in_dict.append(featname)
			'''
			if "LOC_{}_post_bi_un".format(label) not in feat_already_in_dict:
				retrieved_features["LOC_{}_post_bi_un".format(label)] = post_bi_un
			elif "LOC_{}_pre_bi_un".format(label) not in feat_already_in_dict:
				retrieved_features["LOC_{}_pre_bi_un".format(label)] = pre_bi_un
			elif "LOC_{}_post_si_un".format(label) not in feat_already_in_dict:
				retrieved_features["LOC_{}_post_si_un".format(label)] = post_si_un
			elif "LOC_{}_pre_si_un".format(label) not in feat_already_in_dict:
				retrieved_features["LOC_{}_pre_si_un".format(label)] = pre_si_un
			'''
			if "LOC_{}_unique".format(label) not in feat_already_in_dict:
				retrieved_features["LOC_{}_unique".format(label)] = ne
			# remove from suggested features the ones that are already in the decision list
			#for item in set(remove_feats):
			#	key = "LOC_{}_{}".format(label, item)
			#	retrieved_features.pop(key)
			#print("HERE: ", label, retrieved_features)
		else:
			label = "none_found"
			retrieved_features = defaultdict(list)
		# add feature to certain subcategory
		return label, retrieved_features
	
	if main_cat == "ORG":
		remove_feats = []
		# CAT_subcat_featurename, list
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
								match_found = True
								remove_feats.append("post_bi_un")
						elif feat == "pre_bi_un": 
							if pre_bi_un == bigram:
								candidate_tags.append(tuple((subcat, weight)))
								match_found = True
								remove_feats.append("pre_bi_un")
							
						

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
								match_found = True
								remove_feats.append("post_si_un")
						elif feat == "pre_si_un": 
							if pre_si_un == string: 
								candidate_tags.append(tuple((subcat, weight)))
								match_found = True
								remove_feats.append("pre_si_un")
						elif feat == "unique":
							if ne == string:
								candidate_tags.append(tuple((subcat, weight)))
								match_found = True
								remove_feats.append("unique")
		w = 0
		if len(candidate_tags) > 0:
			for tag, weighted in candidate_tags:
				if weighted >= w:
					label = tag
					w = weighted
			# if the feature was the one it hit on dont add it to the list of decisions
			feat_already_in_dict = []
			for item in set(remove_feats):
				featname = "ORG_{}_{}".format(label, item)
				feat_already_in_dict.append(featname)
			if "ORG_{}_post_bi_un".format(label) not in feat_already_in_dict:
				retrieved_features["ORG_{}_post_bi_un".format(label)] = post_bi_un
			elif "ORg_{}_pre_bi_un".format(label) not in feat_already_in_dict:
				retrieved_features["ORG_{}_pre_bi_un".format(label)] = pre_bi_un
			elif "ORG_{}_post_si_un".format(label) not in feat_already_in_dict:
				retrieved_features["ORG_{}_post_si_un".format(label)] = post_si_un
			elif "ORG_{}_pre_si_un".format(label) not in feat_already_in_dict:
				retrieved_features["ORG_{}_pre_si_un".format(label)] = pre_si_un
			elif "ORG_{}_unique".format(label) not in feat_already_in_dict:
				retrieved_features["ORG_{}_unique".format(label)] = ne
				
			# remove from suggested features the ones that are already in the decision list
			#for item in set(remove_feats):
			#	key = "ORG_{}_{}".format(label, item)
			#	retrieved_features.pop(key)
			#print("HERE: ", label, retrieved_features)
		else:
			label = "none_found"
			retrieved_features = defaultdict(list)
		# add feature to certain subcategory
		return label, retrieved_features
	if match_found == False:
		return "none_found", defaultdict(list)
	
		

def send_to_subcat(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, main_cat, decision_list, mode):
	label, retrieved_feats = label_ne(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, decision_list, main_cat, mode)
	return label, retrieved_feats

def weigh_features(temporary_DL, mode):

	# strenght = count(x,y) + alpha / count(x) +kalpha
	# x = feature, y = feature class 
	# count(x,y) is occurences of feature within that feature class
	# count(x) is total occurences of feature in all classes
	# alpha is smoothing parameter
	# k is number of possible labels = 14
	weighted_temp_DL = defaultdict(list)
	k = 14
	alpha = 0.1
	for key_main, value in temporary_DL.items():
		for featx in set(value):
			# occurences within the key subcategory and feature
			x = value.count(featx)
			nominator = x + alpha
			#print(featx, x)
			# total occurences in the entire temporary DL
			counter = 0
			for key2, value2 in temporary_DL.items():
				for item in value2:
					if item == featx:
						counter += 1
			if mode == "NORMAL":
			#	if counter == 1:
			#		weight_featx = 0.1
			#	else:
				denominator = counter + (k*alpha)
				weight_featx = (nominator/denominator)
			if mode == "FINAL":
				denominator = counter + (k*alpha)
				weight_featx = (nominator/denominator)
			
			if key_main not in weighted_temp_DL:
				weighted_temp_DL[key_main] = [tuple((featx, weight_featx))]
			else:
				val = weighted_temp_DL.get(key_main)
				val.append(tuple((featx, weight_featx)))
				weighted_temp_DL[key_main] = val
			
	# get the top n weighted features per subcat/featurecat
	if mode == "NORMAL":
		for key, item in weighted_temp_DL.items():
			weights = []
			top_n_feats = []
			for feature, w in item:
				weights.append(w)
			#print(weights)
			top_weights = nlargest(2, weights)
			#print(top_weights)
			for feature, w in item:
				if w in top_weights:
					top_n_feats.append(tuple((feature, w)))
			weighted_temp_DL[key] = top_n_feats
	# add all features and weights on final iteration
	elif mode == "FINAL":
		weighted_temp_DL = weighted_temp_DL
			
	return weighted_temp_DL

def retrieve_new_features(decision_list, lines, mode):
	temporary_DL = defaultdict(list)
	strings = []
	
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
				label, temp_dic_item = send_to_subcat(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, main_cat, decision_list, mode)
				if label != "none_found":
					# add the temporary features (without weight) to the temrorary_DL
					for key, value in temp_dic_item.items():
						if key not in temporary_DL:
							strings = []
							for unit in decision_list.get(key):
								strings.append(unit[0])							
							if value not in strings:
								temporary_DL[key] = [value]
						else:
							val = temporary_DL.get(key)
							strings = []
							for unit in decision_list.get(key):
								strings.append(unit[0])							
							if value not in strings:
								val.append(value)
							temporary_DL[key] = val
					

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
				label, temp_dic_item = send_to_subcat(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, main_cat, decision_list, mode)
				if label != "none_found":
					# add the temporary features (without weight) to the temrorary_DL
					for key, value in temp_dic_item.items():
						if key not in temporary_DL:
							strings = []
							for unit in decision_list.get(key):
								strings.append(unit[0])							
							if value not in strings:
								temporary_DL[key] = [value]
						else:
							val = temporary_DL.get(key)
							strings = []
							for unit in decision_list.get(key):
								strings.append(unit[0])							
							if value not in strings:
								val.append(value)
							temporary_DL[key] = val
					
					
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
				label, temp_dic_item = send_to_subcat(ne,post_bi_un,pre_bi_un,post_si_un,pre_si_un, main_cat, decision_list, mode)
				if label != "none_found":
					# add the temporary features (without weight) to the temrorary_DL
					for key, value in temp_dic_item.items():
						if key not in temporary_DL:
							strings = []
							for unit in decision_list.get(key):
								strings.append(unit[0])							
							if value not in strings:
								temporary_DL[key] = [value]
						else:
							val = temporary_DL.get(key)
							strings = []
							for unit in decision_list.get(key):
								strings.append(unit[0])							
							if value not in strings:
								val.append(value)
							temporary_DL[key] = val
					
					

	# weight the features to get the top n new features per subcat to be added to the decision list
	new_features = weigh_features(temporary_DL, mode)
	# also return the newly labeled lines of which a feature matched
	if mode == "NORMAL" or mode == "FINAL":
		return new_features

def manually_add_to_initital_DL(decision_list):
	# manually add some features that should be true
	for key, value in decision_list.items():
		feat = "_".join(key.split("_")[2:])

		# add a list of continent names
		if key == "LOC_cont_unique":
			val = decision_list.get(key)
			conts = ["Afrika", "Europa", "Oceanië","Azië","Noord-Amerika", "Zuid-Amerika","Antartica"]
			for item in conts:
				val.append(tuple((item, 0.8)))
			decision_list[key] = val

		#if key == "
			
	
	return decision_list
def main():
	# read in intitial decision list as dictionary
	# key = CAT_subcat_featurename, value = list of features
	initial_DL = load_initial_DL()
	#for key, value in initial_DL.items():
	#	if key == "LOC_land_unique":
	#		print(key, value)
	list_of_feature_keys = initial_DL.keys()
	# add weight of 1 for initial decision list items
	for key, value in initial_DL.items():
		weight = float(1)
		weighted_feats = []
		for feature in value:
			feature = tuple((feature, weight))
			weighted_feats.append(feature)
		initial_DL[key] = weighted_feats

	initial_DL = manually_add_to_initital_DL(initial_DL)
	# read in dataset
	lines = []
	infile = open("../data/using_development/SoNaR1_dev.txt", "r",encoding="utf8")
	next(infile)
	for line in infile:
		line = line.rstrip().split("\t")
		if line[0] != "DOCUMENT":
			lines.append(line)

	# step1: iterate through data in search of NE
	track = 0
	for i in range(90):
		counter = 0
		print(i)
		new_decision_list = retrieve_new_features(initial_DL, lines, "NORMAL")
		for key, value in new_decision_list.items():
			if key not in initial_DL:
				initial_DL[key] = value
			else:
				val = initial_DL.get(key)
				for item in value:
					val.append(item)
				initial_DL[key] = val
			print(value)
		for key, value in initial_DL.items():
			counter += len(value)
		print(counter, "\n")
		if track == counter:
			break
		track = counter
	# final iteration
	print("HERE1")
	new_decision_list = retrieve_new_features(initial_DL, lines, "FINAL")
	for key, value in new_decision_list.items():
			if key not in initial_DL:
				initial_DL[key] = value
			else:
				val = initial_DL.get(key)
				for item in value:
					val.append(item)
				initial_DL[key] = val
	# label using the created decision list
	count2 = 0
	for key, value in initial_DL.items():
		print(key, "\t :",len(value))
		count2 += len(value)
	print(count2)
	# export the final decsion list
	f = open("../data/final_DL.pkl","wb")
	pickle.dump(initial_DL,f)
	f.close()
	
	

	
	
	# step 3: choose top features from temporary decision list
	# add top features to the main decision list

	# step 4: iterate through data and label NE's that have not yet been labeled using main decision list
	# when able to label ne save feature information in temporary decision list

	# step 5: go back to step 3 until ceratin threshold is achieved

	# step 6: label every NE that does not have a label yet 
	
if __name__ == '__main__':
	main()
