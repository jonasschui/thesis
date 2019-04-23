def main():
	infile = open("../data/SoNaR1_training.txt", "r",encoding="utf8")
	count = 0
	for line in infile:
		line = line.split('\t')
		if line[0] == "UITZONDERING!!!":
			print(line)
	#print(count)


if __name__ == '__main__':
	main()