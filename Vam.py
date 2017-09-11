#---------- Title: Iphone backup extracter
#---------- Author: Michael Boose
#---------- compatibility: Python 2.7 | OS: Mac , Linux
#
# Description: This is a program designed originally to extract all files from
# an iphone backup folder, creates storage folders based on file types detected,
# and places files into coresponding folder. This program, however, is not specific
# to an iphone backup and can literally scan a whole computer starting from C:/ and
# smart sort every file it comes across. (not sure why you would want to do that though)

import subprocess

Tree=[]
def List_Items_In(Dir):
	Items_List=[]
	Items_In=subprocess.check_output(["ls",Dir]).split('\n')
	for x in range(0,len(Items_In)-1):
		Items_List.append(Items_In[x])
	return Items_List
def Is_File(Path_To_Item):
	try:
		List_Items_In(Path_To_Item+'/')
		return False
	except:
		return True
Incomplete_Paths=[]
def File_Path_Handler(Dir):
	Branches=List_Items_In(Dir)
	for branch in Branches:
		Path=Dir+'/'+branch
		if Is_File(Path):
			Tree.append(Path.lower())
		else:
			Incomplete_Paths.append(Path)
def Tree_Builder(Base_Dir):
	File_Path_Handler(Base_Dir)
	for x in Incomplete_Paths:
		File_Path_Handler(x)
def All_Extentions():
	All_Extentions=[]
	for Path in Tree:
		Path=Path.split('/')
		File=Path[len(Path)-1]
		File=File.split('.')
		Extention=File[len(File)-1]
		All_Extentions.append(Extention)
	return All_Extentions
def Amount_Found(Extention,Array):
	Counter=0
	for x in Array:
		if x == Extention:
			Counter=Counter+1
	return float(Counter)
def Avg_Times_Each_Found(All):
	Processed=[]
	To_Divide=0
	for x in All:
		Counter=0
		if x not in Processed:
			for y in All:
				if x == y:
					Counter=Counter+1
			Processed.append(x)
			To_Divide=To_Divide+Counter
	return float(To_Divide)/float(len(Processed))
def Make_Homes(Housing_Folder,Names):
	try:
		subprocess.check_output(['mkdir',Housing_Folder])
	except:
		pass
	for x in Names:
		Path=Housing_Folder+'/'+x
		try:
			subprocess.check_output(['mkdir',Path])
		except:
			pass
def Smart_Sort_Algorithm():
	Common=[]
	Random=[]
	All_Ex=All_Extentions()
	Avg_Appearance=Avg_Times_Each_Found(All_Ex)
	for x in All_Ex:
		if x not in Common:
			if Amount_Found(x,All_Ex) >= Avg_Appearance:
				Common.append(x)
			else:
				Random.append(x)
	Make_Homes('Smart Sorted',Common)
	Counter=0
	for x in Common:
		Home='Smart Sorted/'+x+'/'
		for Path in Tree:
			y=Path.split('/')
			File=y[len(y)-1]
			File=File.split('.')
			Extention=File[len(File)-1]
			if x == Extention:
				Counter=Counter+1
				try:
					print 'Extracting: '+str(Counter)+' of '+str(len(All_Ex))
					subprocess.check_output(['cp',Path,Home])
				except Exception as e:
					print e
	try:
		subprocess.check_output(['mkdir','Smart Sorted/Random'])
	except:
		pass
	for x in Random:
		Counter=Counter+1
		print 'Extracting: '+str(Counter)+' of '+str(len(All_Ex))
		for Path in Tree:
			y=Path.split('/')
			File=y[len(y)-1]
			File=File.split('.')
			Extention=File[len(File)-1]
			if x == Extention:
				try:
					subprocess.check_output(['cp',Path,'Smart Sorted/Random/'])
				except:
					print 'ignored odd file...'


def Start_Extraction(Root_Dir):
	Tree_Builder(Root_Dir)
	Smart_Sort_Algorithm()

def Interface():
	buf='-'*10
	print buf+'Welcome to IBackup Vampire'+buf
	Root_Dir=raw_input('Directory to crawl: ')
	Start_Extraction(Root_Dir)

Interface()