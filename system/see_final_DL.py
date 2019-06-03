import pickle
from collections import defaultdict
import operator

def load_final_DL():
	pickle_in = open("../data/final_DL.pkl","rb")
	final_DL = pickle.load(pickle_in)
	return final_DL

def main():
	final_DL = load_final_DL()
	access = defaultdict(list)
	for key, value in final_DL.items():
		feat = key.split("_")[-1]
		cat = key.split("_")[1]
		print(cat)
		if feat != "unique" and (cat == "heelal" or cat == "fictief") :
			for item in value:
				featx, w = item
				if w != 0.99:
					if key not in access:
						access[key] = [item]
					else:
						value = access.get(key)
						value.append(item)
						access[key] = value
	count = 0
	for key, value in access.items():
		value.sort(key=lambda x: x[1], reverse=True)
		print(key,value, "\n")
		count += len(value)
		
	print(count)

if __name__ == '__main__':
	main()
