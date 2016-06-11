import sys
import bmpImage

print("Starting image processing application...")
print("This system is ", sys.byteorder, "endian")

bmp = bmpImage.bmpImage("image")

if (bmp.loadData() == -1):
	print("Error in bmpImage.loadData()")
	sys.exit(-1)

for i in range(2):
	for j in range(2):
		print("red: ", bmp.red[j][i], "green: ", bmp.green[i][j], "blue: ", bmp.blue[i][j])