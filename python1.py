import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import *
import VU_encrypt
import os

#sizes for the widgets (not in pixels)
buttonWidth = 15
buttonHeight = 1

#Grid pos
GridX = 130
GridY = 40

help_text="""
Only one of the check boxes can be activated at once

Make Key: Only the Key Field is required.
extension must be .key

Encrypt a File: All 3 fields are required.
Select an existing Key
Select a file as input
Provide an unused name.

Decrypt a File: All 3 field are required.
Select an existing Key
Select an existing .enc file as input
Provide an unused name.

Make sure you have the correct check box selected, then
When requirements are met, click the
'Generate File Button'
to create an output file
Output is dependent on the checkbox marked

BUTTONS:
Select a key: Opens window to select an existing .key file
Select a File: Opens window to provide an exising file

Test Sample: This creates a sample key, file, and then encrypts.
The key's value is always the same

Help

Clear History: Clears both text boxes, but doesn't delete history already saved to file

Save and close: Saves history into 2 files then Quits the program
"""

tmpHistory = None
history_text={}
history_text2=[]
tkwindow = tkinter.Tk()

class Window1:
	entry_width = 40
	input_text1 = StringVar()
	input_text2 = StringVar()
	input_text3 = StringVar()
	var1 = tkinter.BooleanVar(value=True)
	var3 = tkinter.BooleanVar(value=False)
	var2 = tkinter.BooleanVar(value=False)

	def __init__(self, window):
		#The check boxes
		self.checkMakeKey = tkinter.Checkbutton(window, text = "Make Key", variable=self.var1, command = lambda: self.checkState(self.var1))
		self.set_size(self.checkMakeKey)
		self.set_pos(self.checkMakeKey, 0, 0, 50, 10)
		self.checkEncrypting = tkinter.Checkbutton(window, text = "Encrpyt a File", variable=self.var2, command = lambda: self.checkState(self.var2))
		self.set_size(self.checkEncrypting)
		self.set_pos(self.checkEncrypting, 1, 0, 50, 10)
		self.checkDecrypting = tkinter.Checkbutton(window, text = "Decrypt a File", variable=self.var3, command = lambda: self.checkState(self.var3))
		self.set_size(self.checkDecrypting)
		self.set_pos(self.checkDecrypting, 2, 0, 50, 10)

		#The buttons
		self.buttonKey = tkinter.Button(window, text = "Select a key: ",command = lambda: self.fileDialog(self.entryKey, self.input_text1))
		self.set_size(self.buttonKey)
		self.set_pos(self.buttonKey, 0, 1, 50)
		self.buttonFile = tkinter.Button(window, text = "Select a File",command = lambda: self.fileDialog(self.entryFile, self.input_text2))
		self.set_size(self.buttonFile)
		self.set_pos(self.buttonFile, 0, 2, 50)
		self.buttonOutput = tkinter.Button(window, text = "Generate File",command = self.getOutput)
		self.set_size(self.buttonOutput)
		self.set_pos(self.buttonOutput, 0, 4, 50)

		#Plain labels
		self.label1 = tkinter.Label(window, text = "Key Field")
		self.set_pos(self.label1, 1, 1, 80)
		self.label2 = tkinter.Label(window, text = "Input Field")
		self.set_pos(self.label2, 1, 2, 80)
		self.label3 = tkinter.Label(window, text = "Output Field")
		self.set_pos(self.label3, 1, 4, 80)

		#Text input fields
		self.entryKey = tkinter.Entry(window, textvariable = self.input_text1, width=self.entry_width)
		self.set_pos(self.entryKey, 2, 1, 20)
		self.entryFile = tkinter.Entry(window, textvariable = self.input_text2, width=self.entry_width)
		self.set_pos(self.entryFile, 2, 2, 20)
		self.entryFile1 = tkinter.Entry(window, textvariable = self.input_text3, width=self.entry_width)
		self.set_pos(self.entryFile1, 2, 4, 20)

		#Other buttons
		self.sample_btn = tkinter.Button(window, text = "Test Sample", command = self.make_sample) # create key test file and encrypted file
		self.set_pos(self.sample_btn, 0, 5, 50, 10)
		self.set_size(self.sample_btn)
		self.clear_btn = tkinter.Button(window, text = "Clear History", command = self.delete_history) # Display history
		self.set_pos(self.clear_btn, 2, 5, 50, 10)
		self.set_size(self.clear_btn)
		self.help_btn = tkinter.Button(window, text = "Help", command = self.display_help) # display help window
		self.set_pos(self.help_btn, 3, 5, 50, 10)
		self.set_size(self.help_btn)

		#Display history
		self.displayHidstory = scrolledtext.ScrolledText(window, width = 30, height = 10, wrap = tkinter.WORD)
		self.set_pos(self.displayHidstory, 0, 6, 50)
		self.displayHidstory2 = scrolledtext.ScrolledText(window, width = 30, height = 10, wrap = tkinter.WORD)
		self.set_pos(self.displayHidstory2, 2, 6, 50)

		self.close_btn = tkinter.Button(window, text = "Save and Close", command =self.close_window) # closing the 'window' when you click the button
		self.set_pos(self.close_btn, 3, 11, 50, 10)
		self.set_size(self.close_btn)

	#Only allows 1 checkbox to be activate at one time
	def checkState(self, theCheck):
		self.var1.set(value=False)
		self.var2.set(value=False)
		self.var3.set(value=False)
		theCheck.set(value=True)


	def save_history(self):
		#Save key and encrypted into file
		tempToSave = ""
		tempToLine = ""
		tmpHistory = open("historyEncrypt.txt", "w")
		for aa, bb in history_text.items():
			if (tempToLine == ""):
				tempToLine=aa
			for cc in bb:
				tempToLine+= " " + cc + " "
			tempToLine+="\n"
			tempToSave+=tempToLine
			tempToLine=""
		tmpHistory.write(tempToSave)
		tmpHistory.close()

	def save_history1(self):
		#Save decrypted into file
		tmpHistory = open("historyDecrpyt.txt", "w")
		tmpHistory.write(" ".join(history_text2))
		tmpHistory.close()

	#Exits the program
	def close_window(self):
		self.save_history()
		self.save_history1()
		exit()

	#Clears the history boxes
	def delete_history(self):
		self.displayHidstory.delete(1.0, tkinter.END)
		self.displayHidstory2.delete(1.0, tkinter.END)
		history_text = {}
		history_text2 = []
		self.save_history()
		self.save_history1()

	#Helper function to set the sizes for some of the widgets
	def set_size(self, a):
		a["width"] = buttonWidth
		a["height"] = buttonHeight

	#help function to set position
	def set_pos(self, a, dx, dy, ddx=10, ddy=10):
		a.place(x=dx*GridX+ ddx, y =dy*GridY+ddy)

	#Open file dialog box
	def fileDialog(self, selectedWidget, selectedEntry):
		self.filename = filedialog.askopenfilename(initialdir =os.getcwd(), title = "Select A File", filetype =(("all files","*.*"),("all files","*.*")) )
		selectedEntry.set(self.filename)

	#Opens up another window with helpful information
	def display_help(self):
		window2 = tkinter.Toplevel(tkwindow)
		tkinter.Label(window2, text = help_text).grid()

		window2.geometry("520x560")
		window2.resizable(0,0)
		window2.mainloop()

	#Case function, based on which check is ticked
	def getOutput(self):
		if (self.var1.get()):
			self.createKey()
		elif (self.var2.get()):
			self.encrpytFile()
		else:
			self.decrpytFile()

	#Creates a key file
	def createKey(self):
		fileKey = self.input_text1.get()
		if (len(fileKey) == 0):
			fileKey="SampleKey.key"
			self.input_text1.set(fileKey)
		self.input_text3.set(fileKey)
		VU_encrypt.make_key(fileKey)
		messagebox.showinfo("Success","Key created")

	#Wrapper function for VU_encrpyt to encrpyt a file
	def encrpytFile(self):
		fileKey = self.input_text1.get()
		filePlainText = self.input_text2.get()
		fileEncrypted = self.input_text3.get()

		if (self.no_error(fileKey, filePlainText, fileEncrypted)):
			try:
				if (fileEncrypted != "SampleEncryptedFile.enc"):
					f = open(fileEncrypted, "x")
					f.close()

				# VU_encrypt.encrypt_file("myfile.txt", "myfile.enc", "mykey")
				VU_encrypt.encrypt_file(filePlainText, fileEncrypted, fileKey)

				if (fileKey not in history_text):
					history_text[fileKey] = [fileEncrypted]
				else:
					history_text[fileKey].append(fileEncrypted)
				self.displayHidstory.insert(1.0, "\n" + fileKey + " " + fileEncrypted)

				self.save_history()

				messagebox.showinfo("Success","Encryption complete: " + fileEncrypted)
			except Exception as e:
				messagebox.showinfo("Error 1",e)

	#Wrapper function for VU_encrpyt to decrpyt a file
	def decrpytFile(self):
		fileKey = self.input_text1.get()
		fileEncrypted = self.input_text2.get()
		filePlainText = self.input_text3.get()

		#Check for errors
		if (self.no_error(fileKey, filePlainText, fileEncrypted)):
			try:
				if (filePlainText != "SamplePlainFile.txt"):
					f = open(filePlainText, "x")
					f.close()

					# VU_encrypt.decrypt_file("myfile.enc", "myfile.txt", "mykey")
				VU_encrypt.decrypt_file(fileEncrypted, filePlainText, fileKey)

				if(len(history_text2) == 0):
					history_text2.append("0")
				history_text2[0]= str(int(history_text2[0]) + 1)
				history_text2.append(filePlainText)
				self.displayHidstory2.insert(1.0, "\n" + str(history_text2[0]) + " " + filePlainText)

				self.save_history1()

				messagebox.showinfo("Success","Decryption complete: " + filePlainText)
			except Exception as e:
				messagebox.showinfo("Error 2",e)

	#Create a sample key, file, and encrypted file for testing
	def make_sample(self):
		try:
			f = open("SampleKey", "w")
			f.write("eCs68ie73NyjaaJSbEG6PCFeIjXuesOcxAyDQFqO5JI=")
			self.input_text1.set("SampleKey.key")
			f = open("SamplePlainFile.txt", "w")
			f.write("This is a secret message")
			self.input_text2.set("SamplePlainFile.txt")
			f = open("SampleEncryptedFile.enc", "w")
			self.input_text3.set("SampleEncryptedFile.enc")
			f.close()

			fileKey = self.input_text1.get()
			filePlainText = self.input_text2.get()
			fileEncrypted = self.input_text3.get()

			if (self.no_error(fileKey, filePlainText, fileEncrypted)):
				self.encrpytFile()
		except Exception as e:
			messagebox.showinfo("Error 3",e)

	#Check for errors
	def no_error(self, fileKey, filePlainText, fileEncrypted):
		self.entryKey["bg"]="SystemButtonFace"
		self.entryFile["bg"]="SystemButtonFace"
		self.entryFile1["bg"]="SystemButtonFace"

		error_check = True

		#Check if key input field is empty
		if (len(fileKey) == 0):
		#check if file exist
			try:
				f = open(fileKey, "r")
				a = f.read()
				#Check if key is the correct length in characters
				if (len(a) != 44):
					self.entryKey["bg"] = "red"
					messagebox.showinfo("Error 4", "Key is invalid")
					f.close()
					error_check = False
				f.close()
			except Exception as e:
				messagebox.showinfo("Error 5",e)
				error_check = False
				#Check if unencrpyted file field is empty
		if (len(filePlainText) == 0):
			self.entryFile["bg"] = "red"

			messagebox.showinfo("Error 6","Must select a valid 'file'.txt")
			error_check = False
			#Check if the encrypted field is empty
		if (len(fileEncrypted) == 0 or fileEncrypted[-4:] != ".enc"):
			if (self.var2.get()):
				self.entryFile1["bg"] = "red"
				messagebox.showinfo("Error 7","File must have extension .enc and file must not already exist")
			elif(self.var3.get()):
				self.entryFile["bg"] = "red"
				messagebox.showinfo("Error 7","File must have extension .enc")
			error_check = False
		return error_check

tkwindow.title("Cryptography GUI")
tkwindow.geometry("600x500")
tkwindow.resizable(0,0)
mainWindow = Window1(tkwindow)
tkwindow.update()

tkwindow.mainloop()
