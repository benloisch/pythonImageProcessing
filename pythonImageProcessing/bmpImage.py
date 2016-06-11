import struct

import sys

class bmpImage:
	def __init__(self, fileName):
		
		self.fileName = fileName
		self.width = 0
		self.height = 0
		self.red = None
		self.green = None
		self.blue = None
		
	def loadData(self):
	
		print("Loading ", self.fileName + ".bmp")	
	
		fileObject = open("testbmp.bmp", "rb") #get the width and height of bmp image

		twoBytes = fileObject.read(2) #read first two bytes to check that this file is a bmp
		
		unpackedTwoBytes = struct.unpack('=H', twoBytes)[0] #interpret first two bytes as an unsigned short
		#if unsigned short of multibyte 'BM' is stored as little endian, it will appear as 'MB' 
		#and the unsigned short will be 19778
		
		#if stored as big endian, it will appear as 'BM' which is a multibyte and is an unsigned short of 16973

		#test whether or not the the file is described as a bmp file (first two characters should be 'BM')
		if sys.byteorder ==  'little':
			if unpackedTwoBytes != 19778:
				print(self.fileName + ".bmp is either corrupt or not a .bmp image")
				return -1
		elif sys.byteorder == 'big':
			if unpackedTwoBytes != 16973:
				print(self.fileName + ".bmp is either corrupt or not a .bmp image")
				return -1
				
		fileObject.read(16) #read 16 bytes until start of width and height bytes in the bmp header
		width = fileObject.read(4) #store width and height in local variables
		height = fileObject.read(4)
		fileObject.close()
		
		self.width = struct.unpack('<i', width)[0]
		self.height = struct.unpack('<i', height)[0]
		
		#create red, green, and blue character arrays to store pixel data
		try:
			self.red = [[0 for x in range(self.width)] for y in range(self.height)]
			self.green = [[0 for x in range(self.width)] for y in range(self.height)]
			self.blue = [[0 for x in range(self.width)] for y in range(self.height)]
		except:
			print("Could not initialize character arrays in class bmpImage")
			return -1
			
		#find out how much padding goes on end of each row of data
		pad = 4 - ((self.width * 3) % 4)

		fileObject = open("testbmp.bmp", "rb") #open bmp file to read pixel data into buffers
		fileObject.read(54) #jump past all the header to where the pixel data starts
		
		countPadding = 0 #used to count how many bytes are read in until we hit the padding at the end of the row
		
		#load data from bmp into rgb buffers
		h = self.height - 1
		while h >= 0:
			for w in range(self.width):
				char = fileObject.read(1)
				self.blue[w][h] = struct.unpack('=B', char)[0]
				char = fileObject.read(1)
				self.green[w][h] = struct.unpack('=B', char)[0]
				char = fileObject.read(1)
				self.red[w][h] = struct.unpack('=B', char)[0]
		
				if w == self.width - 1:
					for p in range(pad):
						fileObject.read(1)
			h = h - 1
		fileObject.close()