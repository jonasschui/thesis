# program data_format.py
# author: Jonas Schuitemaker
# studentnumber: s2698617
# program to crudely retrieve the data from SoNaR1 xml files to be processed in SoNaR_neatly.py
# date 16-04-2019

import os
from xml.dom import minidom


def main():
	# get the words in documents from the basedata
	directory = os.fsencode('../../../../net/corpora/SoNaRCorpus_NC_1.2/SONAR1/NE/SONAR_1_NE/MMAX/Basedata/')
	filenames = []
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if filename.endswith(".xml"): 
			# print(os.path.join(directory, filename))
			#print(filename)
			filenames.append(filename)
		else:
			continue
	combination = 0
	for filename in filenames:
		doc_path = '../../../../net/corpora/SoNaRCorpus_NC_1.2/SONAR1/NE/SONAR_1_NE/MMAX/Basedata/{}'.format(filename)
		xmldoc = minidom.parse(doc_path)
		# print(xmldoc)
		itemlist = xmldoc.getElementsByTagName('word')
		# print(len(itemlist))
		#print(itemlist[0].attributes['id'].value)
		

		''' parse markables for this doc'''
		#WS-U-E-A-0000000202_words.xml
		#WS-U-E-A-0000000202_sentence_level.xml
		filename_handle = filename[:-9]
		#print(filename_handle)
		# sentence level
		sen_paste = 'sentence_level.xml'
		sen_path = '../../../../net/corpora/SoNaRCorpus_NC_1.2/SONAR1/NE/SONAR_1_NE/MMAX/Markables/{}{}'.format(filename_handle,sen_paste)
		xmldoc = minidom.parse(sen_path)
		sen_items = xmldoc.getElementsByTagName('markable')
		sentences = []
		for line in sen_items:
			sen_span = line.attributes['span'].value
			sen_first = sen_span[5:]
			sen_list = sen_first.split('.')
			sen_index = sen_list[0]
			start_index = float(sen_index)
			sentences.append(start_index)
		sentences = sorted(sentences, key=int)
		sentences.append(str('token'))
		#print(sentences)
		
		''' make dictionary of taggs'''
		tag_dic = {}
		# per
		per_paste = 'per_level.xml'
		per_path = '../../../../net/corpora/SoNaRCorpus_NC_1.2/SONAR1/NE/SONAR_1_NE/MMAX/Markables/{}{}'.format(filename_handle,per_paste)
		xmldoc = minidom.parse(per_path)
		per_items = xmldoc.getElementsByTagName('markable')
		for line in per_items:
			try:
				per_span = line.attributes['span'].value
				per_first = per_span[5:]
				if len(per_first) >= 8:
					per_list = per_first.split('.')
					per_index_first = per_list[0]
					per_index_second = per_list[-1:][0]
					per_index_second = per_index_second[5:]
				
					range_list = list(range(int(per_index_first), (int(per_index_second)+1)))
					for num in range_list:
						tag_dic[float(num)] = "PER comb{}".format(combination)
				
				else:
					tag_dic[float(per_first)] = "PER"
			except:
				continue
			combination += 1
		
		# loc	
		loc_paste = 'loc_level.xml'
		loc_path = '../../../../net/corpora/SoNaRCorpus_NC_1.2/SONAR1/NE/SONAR_1_NE/MMAX/Markables/{}{}'.format(filename_handle,loc_paste)
		xmldoc = minidom.parse(loc_path)
		loc_items = xmldoc.getElementsByTagName('markable')
		for line in loc_items:
			try: 
				loc_span = line.attributes['span'].value
				main_loc_cat = line.attributes['mmax_level'].value.upper()
				sub_loc_cat = line.attributes['subtype'].value.upper()
				loc_first = loc_span[5:]
				if len(loc_first) >= 8:
					loc_list = loc_first.split('.')
					loc_index_first = loc_list[0]
					loc_index_second = loc_list[-1:][0]
					loc_index_second = loc_index_second[5:]
					range_list = list(range(int(loc_index_first), (int(loc_index_second)+1)))
					for num in range_list:
						tag_dic[float(num)] = "{} {} comb{}".format(main_loc_cat,sub_loc_cat, combination)
				else:
					tag_dic[float(loc_first)] = "{} {}".format(main_loc_cat,sub_loc_cat)
			except:
				continue
			combination += 1
		
		# org
		paste = 'org_level.xml'
		path = '../../../../net/corpora/SoNaRCorpus_NC_1.2/SONAR1/NE/SONAR_1_NE/MMAX/Markables/{}{}'.format(filename_handle,paste)
		xmldoc = minidom.parse(path)
		items = xmldoc.getElementsByTagName('markable')
		for line in items:
			try:
				span = line.attributes['span'].value
				main_cat = line.attributes['mmax_level'].value.upper()
				sub_cat = line.attributes['subtype'].value.upper()
				first = span[5:]
				if len(first) >= 8:
					alist = first.split('.')
					index_first = alist[0]
					index_second = alist[-1:][0]
					index_second = index_second[5:]
					range_list = list(range(int(index_first), (int(index_second)+1)))
					for num in range_list:
						tag_dic[float(num)] = "{} {} comb{}".format(main_cat,sub_cat, combination)
				else:
					tag_dic[float(first)] = "{} {}".format(main_cat,sub_cat)
			except:
				continue
			combination += 1
		# pro
		paste = 'pro_level.xml'
		path = '../../../../net/corpora/SoNaRCorpus_NC_1.2/SONAR1/NE/SONAR_1_NE/MMAX/Markables/{}{}'.format(filename_handle,paste)
		xmldoc = minidom.parse(path)
		items = xmldoc.getElementsByTagName('markable')
		for line in items:
			try:
				span = line.attributes['span'].value
				main_cat = line.attributes['mmax_level'].value.upper()
				sub_cat = line.attributes['subtype'].value.upper()
				first = span[5:]
				if len(first) >= 8:
					alist = first.split('.')
					index_first = alist[0]
					index_second = alist[-1:][0]
					index_second = index_second[5:]
					range_list = list(range(int(index_first), (int(index_second)+1)))
					for num in range_list:
						tag_dic[float(num)] = "{} {} comb{}".format(main_cat,sub_cat, combination)
				else:
					tag_dic[float(first)] = "{} {}".format(main_cat,sub_cat)
			except:
				continue
			combination += 1
			
		# eve
		paste = 'eve_level.xml'
		path = '../../../../net/corpora/SoNaRCorpus_NC_1.2/SONAR1/NE/SONAR_1_NE/MMAX/Markables/{}{}'.format(filename_handle,paste)
		xmldoc = minidom.parse(path)
		items = xmldoc.getElementsByTagName('markable')
		for line in items:
			try:
				span = line.attributes['span'].value
				main_cat = line.attributes['mmax_level'].value.upper()
				sub_cat = line.attributes['subtype'].value.upper()
				first = span[5:]
				if len(first) >= 8:
					alist = first.split('.')
					index_first = alist[0]
					index_second = alist[-1:][0]
					index_second = index_second[5:]
					range_list = list(range(int(index_first), (int(index_second)+1)))
					for num in range_list:
						tag_dic[float(num)] = "{} {} comb{}".format(main_cat,sub_cat, combination)
				else:
					tag_dic[float(first)] = "{} {}".format(main_cat,sub_cat)
			except:
				continue
			combination += 1
		# misc
		paste = 'misc_level.xml'
		path = '../../../../net/corpora/SoNaRCorpus_NC_1.2/SONAR1/NE/SONAR_1_NE/MMAX/Markables/{}{}'.format(filename_handle,paste)
		xmldoc = minidom.parse(path)
		items = xmldoc.getElementsByTagName('markable')
		for line in items:
			try:
				span = line.attributes['span'].value
				main_cat = line.attributes['mmax_level'].value.upper()
				first = span[5:]
				if len(first) >= 8:
					alist = first.split('.')
					index_first = alist[0]
					index_second = alist[-1:][0]
					index_second = index_second[5:]
					range_list = list(range(int(index_first), (int(index_second)+1)))
					for num in range_list:
						tag_dic[float(num)] = "{} comb{}".format(main_cat, combination)
				else:
					tag_dic[float(first)] = "{}".format(main_cat)
			except:
				continue
			combination += 1

		print("DOCUMENT: ", filename)
		new_sentence = []
		row_id = 1
		for s in itemlist:
			word_id = s.attributes['id'].value
			word_id = float(word_id[5:])
			word = s.childNodes[0].nodeValue
			# sentence parsing
			for index in sentences:
				if index == word_id :
					print(' '.join(new_sentence))					
					new_sentence = []
			new_sentence.append(word)
			
			if word_id in tag_dic:
				print("{}\t{}\t{}\t{}".format(row_id, word_id, word, tag_dic.get(word_id)))
				row_id += 1
			else:
				print("{}\t{}\t{}".format(row_id, word_id, word))
				row_id += 1
			
			# person level


		print(' '.join(new_sentence))
		
		
	
		# filename is de bestandsnaam
		# s.attributes is het id nummer
		# s.childnodes is het bijbehorende woord
		# schrijf woord en id naar tekstbestand onder iedere bestandsnaam
		


if __name__ == '__main__':
	main()


