



import os
from xml.dom import minidom


def main():
	
	# get the words in documents from the basedata
	directory = os.fsencode('../../../../net/corpora/SoNaRCorpus_NC_1.2/SONAR1/NE/SONAR_1_NE/MMAX/Markables/')
	filenames = []
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if filename.endswith(".xml"): 
			# print(os.path.join(directory, filename))
			#print(filename)
			filenames.append(filename)
		else:
			continue
	for filename in filenames:
		doc_path = '../../../../net/corpora/SoNaRCorpus_NC_1.2/SONAR1/NE/SONAR_1_NE/MMAX/Markables/{}'.format(filename)
		xmldoc = minidom.parse(doc_path)
		# print(xmldoc)
		itemlist = xmldoc.getElementsByTagName('word')
		# print(len(itemlist))
		
		#print(itemlist[0].attributes['id'].value)
		print("# ", filename)
		for s in itemlist:
			word_id = s.attributes['id'].value
			word = s.childNodes[0].nodeValue
			print("{}	{}".format(word_id, word))
	
		# filename is de bestandsnaam
		# s.attributes is het id nummer
		# s.childnodes is het bijbehorende woord
		# schrijf woord en id naar tekstbestand onder iedere bestandsnaam
		


if __name__ == '__main__':
	main()
