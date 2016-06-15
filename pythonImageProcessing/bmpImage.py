import struct

import sys

class bmpImage:
	def __init__(self):
		
		self.width = 0
		self.height = 0
		self.red = None
		self.green = None
		self.blue = None
		
	def load(self, fileName):
	
		try:
			print("Loading ", fileName + ".bmp")	
		
			fileObject = open(fileName + ".bmp", "rb") #get the width and height of bmp image

			twoBytes = fileObject.read(2) #read first two bytes to check that this file is a bmp
			
			unpackedTwoBytes = struct.unpack('=H', twoBytes)[0] #interpret first two bytes as an unsigned short
			#if unsigned short of multibyte 'BM' is stored as little endian, it will appear as 'MB'
			#and the unsigned short will be 19778
			
			#if stored as big endian, it will appear as 'BM' which is a multibyte and is an unsigned short of 16973

			#test whether or not the the file is described as a bmp file (first two characters should be 'BM')
			if sys.byteorder ==  'little':
				if unpackedTwoBytes != 19778:
					print(fileName + ".bmp is either corrupt or not a .bmp image")
					return -1
			elif sys.byteorder == 'big':
				if unpackedTwoBytes != 16973:
					print(fileName + ".bmp is either corrupt or not a .bmp image")
					return -1
					
			fileObject.read(16) #read 16 bytes until start of width and height bytes in the bmp header
			width = fileObject.read(4) #store width and height in local variables
			height = fileObject.read(4)
			fileObject.close()
			
			self.width = struct.unpack('<i', width)[0]
			self.height = struct.unpack('<i', height)[0]
			
			#create red, green, and blue character arrays to store pixel data
			try:
				self.red = [[0 for y in range(self.height)] for x in range(self.width)]
				self.green = [[0 for y in range(self.height)] for x in range(self.width)]
				self.blue = [[0 for y in range(self.height)] for x in range(self.width)]
			except:
				print("Could not initialize character arrays in class bmpImage")
				return -1

			#find out how much padding goes on end of each row of data
			pad = 4 - ((self.width * 3) % 4)

			if (pad == 4): #if our image is byte aligned to multiple of 4, then no need to add padding
				pad = 0
					
			fileObject = open(fileName + ".bmp", "rb") #open bmp file to read pixel data into buffers
			fileObject.read(54) #jump past all the header to where the pixel data starts
			
			countPadding = 0 #used to count how many bytes are read in until we hit the padding at the end of the row
					
			#load data from bmp into rgb buffers
			h = self.height - 1 #use h to keep track of when to place padding
			while h >= 0:
				for w in range(self.width):							
					char = fileObject.read(1)
					self.blue[w][h] = struct.unpack('=B', char)[0]
					char = fileObject.read(1)
					self.green[w][h] = struct.unpack('=B', char)[0]
					char = fileObject.read(1)
					self.red[w][h] = struct.unpack('=B', char)[0]
			
					if w == self.width - 1:
						fileObject.read(pad)
				h = h - 1
			fileObject.close()
		except:
			return -1
		return 0
		
	def save(self, fileName):
	
		try:
			fileObject = open(fileName + ".bmp", "wb") #get the width and height of bmp image

			pad = 4 - ((self.width * 3) % 4) #padding of bytes at end of each row of pixel data

			if (pad == 4): #if our image is byte aligned to multiple of 4, then no need to add padding
				pad = 0

			#fill out bitmap file header
			fileObject.write(struct.pack('=B', 66)) #write 'BM' as first to bytes to show it is a bitmap for windows
			fileObject.write(struct.pack('=B', 77))
			fileObject.write(struct.pack('=i', (((self.width * 3) + pad) * self.height) + 54)) #write size in bytes of entire file (pixel data + 54 (size of both headers combined)
			fileObject.write(struct.pack('=H', 0)) #reserved. set to 0
			fileObject.write(struct.pack('=H', 0)) #reserved. set to 0
			fileObject.write(struct.pack('=i', 54)) #the offset from beginning of file to pixel data

			#fill out bitmap information header
			fileObject.write(struct.pack('=i', 40)) #size of this header which is 40 bytes
			fileObject.write(struct.pack('=i', self.width)) #width in pixels of image
			fileObject.write(struct.pack('=i', self.height)) #height in pixels of image
			fileObject.write(struct.pack('=H', 1)) #number of color planes
			fileObject.write(struct.pack('=H', 24)) #number of bits per pixel
			fileObject.write(struct.pack('=i', 0)) #compression method
			fileObject.write(struct.pack('=i', (((self.width * 3) + pad) * self.height))) #image size in bytes
			fileObject.write(struct.pack('=i', 0)) #horizontal resolution of image
			fileObject.write(struct.pack('=i', 0)) #horizontal resolution of image
			fileObject.write(struct.pack('=i', 0)) #number of colors in color palette
			fileObject.write(struct.pack('=i', 0)) #number of important colors used

			#write pixel data
			h = self.height - 1 #height variable
			while h >= 0:
				for w in range(self.width):
					blue = self.blue[w][h]
					fileObject.write(struct.pack('=B', blue))
					green = self.green[w][h]
					fileObject.write(struct.pack('=B', green))
					red = self.red[w][h]
					fileObject.write(struct.pack('=B', red))

					if w == self.width - 1:
						for p in range(pad):
							fileObject.write(struct.pack('=B', 0))

				h = h - 1

			fileObject.close()
		except:
			fileObject.close()
			print("Could not save bmp image")
			return -1

		return 0
		
	def grayscale(self, option):

		print("Applying algorithm...")
	
		if (option == 1):
			#apply quick and dirty grayscale algorithm
			#r = g = b = (r + g + b) / 3
			for x in range(self.width):
				for y in range(self.height):
					avg = int((self.red[x][y] + self.green[x][y] + self.blue[x][y]) / 3.0)
					self.red[x][y] = avg
					self.green[x][y] = avg
					self.blue[x][y] = avg
		elif (option == 2):
			#apply 'fixed' grayscale by weighing each color.
			#the way humans perceive luminosity or brightness is wrong for the averaging algorithm
			#weigh each color according to GIMP or Photoshop standard
			#r = g = b = (r*0.3 + g*0.59 + b*0.11) / 3
			for x in range(self.width):
				for y in range(self.height):
					avg = int(((self.red[x][y]*0.3) + (self.green[x][y]*0.59) + (self.blue[x][y]*0.11)) / 3.0)
					self.red[x][y] = avg
					self.green[x][y] = avg
					self.blue[x][y] = avg
	
	def blurring(self, option, blurRadius):
		print("Applying blurring algorithm...")
		
		if (blurRadius <= 0):
			blurRadius = 1
		
		if (option == 1):
		
			red = [[0 for y in range(self.height)] for x in range(self.width)]
			green = [[0 for y in range(self.height)] for x in range(self.width)]
			blue = [[0 for y in range(self.height)] for x in range(self.width)]
			
			#copy pixel data into seperate buffer so as not to re-use manipulated pixels
			for x in range(self.width):
				for y in range(self.height):
					red[x][y] = self.red[x][y]
					green[x][y] = self.green[x][y]
					blue[x][y] = self.blue[x][y]
					
			#blur pixel with neighboring pixels

			for y in range(self.height):
				for x in range(self.width):
					#calculate top left and bottom right of matrix of square area to blur
					topLeftX = x - blurRadius
					topLeftY = y - blurRadius
					bottomRightX = x + blurRadius
					bottomRightY = y + blurRadius
					
					if topLeftX < 0: topLeftX = 0
					if topLeftY < 0: topLeftY = 0
					if bottomRightX >= self.width: bottomRightX = self.width - 1
					if bottomRightY >= self.height: bottomRightY = self.height - 1
					
					amountOfPixels = ((bottomRightY+1) - topLeftY) * ((bottomRightX+1) - topLeftX)

					if (amountOfPixels <= 0):
						amountOfPixels = 1
				
					redTotal = 0
					greenTotal = 0
					blueTotal = 0
					
					#add up all the red, green, and blue values and divide by length of matrix (average them)
					for yblur in range(topLeftY, bottomRightY + 1):
						for xblur in range(topLeftX, bottomRightX + 1):
							redTotal += self.red[xblur][yblur]
							greenTotal += self.green[xblur][yblur]
							blueTotal += self.blue[xblur][yblur]

					self.red[x][y] = int(redTotal / amountOfPixels)
					self.green[x][y] = int(greenTotal / amountOfPixels)
					self.blue[x][y] = int(blueTotal / amountOfPixels)