# program SoNaR_neatly.py
# author: Jonas Schuitemaker
# studentnumber: s2698617
# program to neatly format the SoNaR 1 million database together with data_format.py (which is a crude format for xml retrieval)
# date 16-04-2019

def main():
	infile = open("mid2.out", "r")
	all_lines = []
	for line in infile:
		#print(line)
		
		line = line.rstrip()
		line_as_list = line.split()
		
		if len(line_as_list) == 1 and line_as_list[0] == "SENTENCE":
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
		# combinatory (person has no subcat)
		elif len(line_as_list) == 6 and line[5][:4] == "comb":
			sub = line_as_list[-2].split('-')[-1]
			if sub.isupper() == True:
				line_as_list[-2] = sub
			new_line = '\t'.join(line_as_list)
			all_lines.append(new_line)

		elif line_as_list[0] == "DOCUMENT":
			all_lines.append(line)
		else:
			all_lines.append(line)
	
	infile.close
	print("line_id  markable_id  word  main_cat  subcat")
	# concatenate on combination id
	lines_with_NE_combinations = []
	combination_id_prev = 1899999999999999
	combined_line = []
	state = False
	for line in all_lines:
		line = line.split()
		# for person category
		if len(line) == 5 and line[4][:4] == "comb":
			combination_id = int(line[4][4:])
			# aankomst
			if state == False and combination_id != combination_id_prev:
				combination_id_prev = combination_id
				combined_line = line[:3]
		
			# tweede item
			elif state == False and combination_id == combination_id_prev:
				combined_line.append(line[2])
				# sla categorie (en mogelijk subcat) op
				cat = line[3]
				subcat = ''
				state = True

			# mogelijk volgende item
			elif state == True and combination_id == combination_id_prev:
				combined_line.append(line[2])

			# niet dezelfde ne maar wel een combinatie ne
			elif state == True and combination_id != combination_id_prev:
				# vorige item
				ne = ' '.join(combined_line)
				lines_with_NE_combinations.append("{} {}".format(ne, cat))
				# item waar je nu in zit
				combination_id_prev = combination_id
				combined_line = line[:3]
				state = False

		# for other categories
		elif len(line) == 6 and line[5][:4] == "comb":
			combination_id = int(line[5][4:])
			# aankomst
			if state == False and combination_id != combination_id_prev:
				combination_id_prev = combination_id
				combined_line = line[:3]
		
			# tweede item
			elif state == False and combination_id == combination_id_prev:
				combined_line.append(line[2])
				# sla categorie (en mogelijk subcat) op
				cat = line[3]
				subcat = line[4]
				state = True

			# mogelijk volgende item
			elif state == True and combination_id == combination_id_prev:
				combined_line.append(line[2])

			# niet dezelfde ne maar wel een combinatie ne
			elif state == True and combination_id != combination_id_prev:
				# vorige item
				ne = ' '.join(combined_line)
				lines_with_NE_combinations.append("{} {} {}".format(ne, cat, subcat))
				# item waar je nu in zit
				combination_id_prev = combination_id
				combined_line = line[:3]
				state = False
			
		else:
			# komt na ne
			if state == True:
				# vorige item
				ne = ' '.join(combined_line)
				lines_with_NE_combinations.append("{} {} {}".format(ne, cat, subcat))
				combination_id_prev = 1899999999999999
				combined_line = []
				state = False
			if state == False:
				lines_with_NE_combinations.append(' '.join(line))

	formatted = []
	for line in lines_with_NE_combinations:
		line = line.rstrip().split()
		if line[0] == "SENTENCE":
			formatted_line = "{}\t{}".format(line[0], ' '.join(line[1:]))
			formatted.append(formatted_line)
		elif line[0] == "DOCUMENT":
			formatted_line = "{}\t{}".format(line[0], ' '.join(line[1:]))
			formatted.append(formatted_line)
		elif len(line) == 3:
			formatted_line = "{}\t{}\t{}".format(line[0], line[1], ' '.join(line[2:]))
			formatted.append(formatted_line)
		elif line[-1] in ['PER', 'MISC', 'ORG', 'LOC', 'PRO', 'EVE'] and line[-2] not in ['PER', 'MISC', 'ORG', 'LOC', 'PRO', 'EVE']:
			formatted_line = "{}\t{}\t{}\t{}".format(line[0], line[1], ' '.join(line[2:-1]), line[-1])
			formatted.append(formatted_line)
		elif line[-2] in ['ORG', 'LOC', 'PRO', 'EVE']:
			formatted_line = "WEL HIER {}\t{}\t{}\t{}\t{}".format(line[0], line[1], ' '.join(line[2:-2]), line[-2], line[-1])
			formatted.append((line[0], line[1], ' '.join(line[2:-2]), line[-2], line[-1]))
			formatted.append(formatted_line)
		else:
			formatted_line = "UITZONDERING!!! {}".format(line)
			formatted.append(formatted_line)
	for line in formatted:
		print(line)
			
if __name__ == '__main__':
	main()
