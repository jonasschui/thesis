def main():
	infile = open("mid.out", "r")
	full_sentences = []
	sen_lengs = []
	all_lines = []
	for line in infile:
		#print(line)
		
		line = line.rstrip()
		line_as_list = line.split()
		
		if len(line) == 0:
			continue
		# not a combinatory
		elif len(line_as_list) == 5:
			sub = line_as_list[-1].split('-')[-1]
			if sub.isupper() == True:
				line_as_list[-1] = sub
			new_line = '\t'.join(line_as_list)
			all_lines.append(new_line)
		elif len(line_as_list) == 6:
			sub = line_as_list[-2].split('-')[-1]
			if sub.isupper() == True:
				line_as_list[-2] = sub
			new_line = '\t'.join(line_as_list)
			all_lines.append(new_line)

		elif line_as_list[0] != "#":
			full_sentences.append(line)
			sen_lengs.append(len(line))
			all_lines.append(line)
	
		elif line_as_list[0] == "#":
			all_lines.append(line)
		else:
			all_lines.append(line)
	
	infile.close
	print("line_id  markable_id  word  main_cat  subcat")
	# concatenate on combination id
	lines_with_NE_combinations = []
	combination_id_prev = 1899999999999999
	counter = 0
	combined_line = []
	for line in all_lines:
		line = line.split()
		# for person category
		if len(line) == 5 and line[4][:4] == "comb":
			combination_id = int(line[4][4:])
			if counter == 0:
				lines_with_NE_combinations.append("c0 prev {} nu {}".format(combination_id_prev,combination_id))
				combination_id_prev = combination_id
				combined_line = line[:3]
			elif counter >= 1:
				lines_with_NE_combinations.append("c>1 prev {} nu {}".format(combination_id_prev,combination_id))
				if combination_id == combination_id_prev:
					combined_line.append(line[2])
					combination_id_prev = combination_id
					lines_with_NE_combinations.append("prev {} nu {}".format(combination_id_prev,combination_id))
				else:
					lines_with_NE_combinations.append(combined_line)
					ne = ' '.join(combined_line)
					lines_with_NE_combinations.append("deze {} {} {} {} {}".format(ne, line[2], line[3],combination_id_prev,combination_id))
					combined_line = []
					counter = 0
					combination_id_prev = 1999999999999999
					ne = ''
					continue
			counter += 1 
		# for alll other categories
		if len(line) == 6 and line[5][:4] == "comb":
			combination_id = int(line[5][4:])
			if counter == 0:
				combination_id_prev = combination_id
				combined_line = line[:3]
				counter = 1
			elif counter == 1:
				if combination_id == combination_id_prev:
					combined_line.append(line[2])
					#print(line[2])
					combination_id_prev = combination_id
				else:
					
					ne = ' '.join(combined_line)
					lines_with_NE_combinations.append("{} {} {}".format(ne , line[3], line[4]))
					combined_line = []
					counter = 0
		else:
			lines_with_NE_combinations.append(' '.join(line))
	for line in lines_with_NE_combinations:
		print(line)
		
			

if __name__ == '__main__':
	main()


'''
elif len(line_as_list) == 6:
	sub = line_as_list[-2].split('-')[-1]
	if sub.isupper() == True:
	line_as_list[-2] = sub
	combination_id = line_as_list[-1]
			
	new_line = '\t'.join(line_as_list)
	all_lines.append(new_line)
'''
