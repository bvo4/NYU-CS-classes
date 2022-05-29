def main():
	string = str(input("string: "))
	totalOccurrences = 0
	previousCharValue = ""
	result = ''
	dupe = False
	
	for letter in string:
		print("Letter is " + letter)
		if (letter == previousCharValue):
			totalOccurrences = totalOccurrences + 1
			dupe = True
		else:
			result = result + previousCharValue + str(totalOccurrences)
			totalOccurrences = 1
			previousCharValue = letter
			dupe = False
		
	if not dupe:
		result = result + previousCharValue + str(totalOccurrences)
		totalOccurrences = 1
		previousCharValue = letter			
		
	print("Compressed string: " + result)
	print("Old string #: " + str(len(string)) + " characters.")
	print("Compressed string #: " + str(len(result)) + " characters.")
	print("The compresstion ratio: " + str(len(result) / len(string)))

main()