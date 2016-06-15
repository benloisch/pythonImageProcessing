import sys
import bmpImage

print("\nStarting image processing application...")
print("This system is ", sys.byteorder, "endian")

#create image object
bmp = bmpImage.bmpImage()

#select image menu
pickImage = "none"
while (pickImage != "Exit"):
	print("\nCopy your image to the folder where the Python files are.")
	print("Type in the name of the image or type 'Exit' to quit.\n")
	
	pickImage = input()
	
	try:
		testFileName = open(pickImage + ".bmp", "rb")
		testFileName.read(1)
		testFileName.close()
	except:
		print("Wrong file name or file not located.")
		print("Enter file name or type 'Exit', then press enter to quit.")
		continue
	
	if (pickImage == "Exit"):
		sys.exit(0)
	
	break

#run code that loads image data
if (bmp.load(pickImage) == -1):
	print("Error in bmpImage.loadData()")
	print("Could not load image")
	sys.exit(-1)

#sub menus
def grayscale():
	userChoice = 0
	while (userChoice != 2):
		
		print("\nType the name of the grayscale algorithm to perform on the image...\n")
		
		print("1 Averaging Algorithm")
		print("2 Luminance Algorithm (Fix brightness for more accurate grayscale)")
		print("3 Return to main menu\n")
		
		try:
			userChoice = int(input())
		except:
			print("Please type in an integer and press enter.")
			continue
		
		if (userChoice == 1):
			bmp.grayscale(1)
			return
		if (userChoice == 2):
			bmp.grayscale(2)
			return
		elif (userChoice == 3):
			return
		else:
			print("Type in a number from the list of options.")
	
def blurring():
	userChoice = 0
	while (userChoice != 2):
		
		print("\nType the name of the blurring algorithm to perform on the image...\n")
		
		print("1 Simple Blurring Algorithm")
		print("2 Return to main menu\n")
		
		try:
			userChoice = int(input())
		except:
			print("Please type in an integer and press enter.")
			continue
		
		if (userChoice == 1):
			blurAmnt = 0
			while (True):
				print("\nPlease enter the pixel blur radius for a pixel...\n")
				try:
					blurAmnt = int(input())
					break
				except:
					print("Please type in an integer and press enter.")
					continue
			bmp.blurring(1, blurAmnt)
			return
		elif (userChoice == 2):
			return
		else:
			print("Type in a number from the list of options.")
			
#main menu
userChoice = 0
while (userChoice != 3):
	print("\nType the number of the image processing algorithm to apply to the image...\n")
	
	print("1 Grayscale")
	print("2 Blurring")
	print("3 Exit\n")
	
	try:
		userChoice = int(input())
	except:
		print("Please type in an integer and press enter.")
		continue
	
	if (userChoice == 1):
		grayscale()
	elif (userChoice == 2):
		blurring()
	elif (userChoice == 3):
		print("Saving image...")
	else:
		print("Type in a number from the list of options.")

#save image to computer
if (bmp.save("output") == -1):
	print("Error saving bmp")
	sys.exit(-1)