import sys
import bmpImage

print("Starting image processing application...")
print("This system is ", sys.byteorder, "endian")

bmp = bmpImage.bmpImage()

if (bmp.load("bmpRayTrace") == -1):
	print("Error in bmpImage.loadData()")
	sys.exit(-1)
	
if (bmp.save("output") == -1):
	print("Error saving bmp")
	sys.exit(-1)
		