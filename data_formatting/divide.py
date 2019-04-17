# program divide.py
# author: Jonas Schuitemaker
# studentnumber: s2698617
# program to divide the retrieved SoNaR1 corpus into a training and a test dataset of 80%/20% percent
# date 16-04-2019

from random import randint

def main():
	infile = open("SoNaR1_total.out", "r")
	doc_titles = []
	train_docs = []
	training = []
	test_docs = []
	test = []
	counter = 0
	for line in infile:
		line = line.rstrip()
		line_as_list = line.split()
		if line_as_list[0] == "DOCUMENT:":
			counter = randint(0, 9) 
			if counter <= 7:
				train_docs.append("num")
				training.append(line)
			else:
				test_docs.append("num")
				test.append(line)
			continue
		if counter <= 7:
			training.append(line)
		else:
			test.append(line)
	
	with open('SoNaR1_training.txt', 'w') as f:
		for line in training:
			f.write(line)
			f.write("\n")
	with open('SoNaR1_test.txt', 'w') as f:
		for line in test:
			f.write(line)
			f.write("\n")

	# check division	
	#print(len(train_docs))
	#print(len(test_docs))
		

			

if __name__ == '__main__':
	main()

