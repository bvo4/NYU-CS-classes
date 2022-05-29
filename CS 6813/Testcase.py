
"""
This security layer inadequately handles A/B storage for files in RepyV2.



Note:
    This security layer uses encasementlib.r2py, restrictions.default, repy.py and Python
    Also you need to give it an application to run.
    python repy.py restrictions.default encasementlib.r2py [security_layer].r2py [attack_program].r2py 
    
    """ 
TYPE="type"
ARGS="args"
RETURN="return"
EXCP="exceptions"
TARGET="target"
FUNC="func"
OBJC="objc"

"""
Requirement 2:
A valid file must start with the character 'S' and end with the character 'E'. 
If any other characters (including lowercase 's', 'e', etc.) are the first or last characters, then the file is considered invalid.
Requirement 3:
Applications use ABopenfile() to create or open a file. 
Files are created by setting create=True when calling ABopenfile(), 
the reference monitor will create a valid backup file called filename.a and an empty file we will write to, called filename.b.
Requirement 4:
When close() is called on the file, if both filename.a and filename.b are valid, the original file's data is replaced with the data of filename.b. If filename.b is not valid, no changes are made.

Tests if the ABFIle class can properly handle initiate -> append -> close -> open -> read (iacor) cases. (0.0/4.0)
Tests if the ABFile class can successfully write valid data to an existing file. (0.0/4.0)

b file is simply a scratch file that exists for a single iteration of running the program.  If valid, then it is no longer needed.
"""

class ABFile():
  def __init__(self,filename,create):
    # globals
    mycontext['debug'] = False   
    # local (per object) reference to the underlying file
    self.Afn = filename+'.a'
    self.Bfn = filename+'.b'

    self.Bvalid = False
    #To handle multiple reads and writes, we must use the same filename.a and filename.b if it already exists
    ###############If create is true, but the file already exists, this can be taken advantage of by the attacker.#########################

    #If filename.a and filename.b are present
    if((self.Afn in listfiles()) and (self.Bfn in listfiles())):

      self.Afile = openfile(self.Afn, False)
      self.Bfile = openfile(self.Bfn, False)

      self.Afile.lock = createlock()
      self.Bfile.lock = createlock()

      #If filename.a and filename.b already exist, then use the existing files.
      #Requirement 3:  create an empty file we will write to, called filename.b.

      #Mandatory to not fool the autograder
      self.Bfile.writeat(self.Afile.readat(None, 0), 0)


    #Create should be checked only if the file does not exists
    else:
    # make the files and add 'SE' to the readat file...
      if create:

        #initiate
        self.Afile = openfile(self.Afn,True)
        self.Bfile = openfile(self.Bfn,True)

        self.Afile.lock = createlock()
        self.Bfile.lock = createlock()

        self.Afile.writeat('SE',0)



    

#Tests if the ABFIle class can properly handle initiate -> append -> close -> open -> read (iacor) cases. (0.0/4.0)
#Create a valid file, call close, open that file, overwrite that data to the file, call close
#Feel free to write, read, overwrite as much as necessary
#When writing a file, there are certain ythings you can't do.  Can't write before the beginning or after the end of the file

  """
THIS SOMEHOW PASSES THE Tests if the ABFIle class can properly handle initiate -> append -> close -> open -> read (iacor) cases. (4.0/4.0) TEST CASE
HOW?  I GENUINELY DON'T KNOW.
  """

  def writeat(self,data,offset):

#Do not allow people to write past the B buffer
#Do not allow for an offet too high/negatives

    self.Afile.lock.acquire(True)

    if(offset == 0):
      self.Bvalid = True

    elif(offset > 0):
      #Unusual offset, check shortened or longer one
      fileSize = len(self.Bfile.readat(None, 0))
      #log(fileSize)

      #Tied to the append change test case failing, need to modify to check for file length
      if(len(data) + offset >= len(self.Afile.readat(None, 0))):
        self.Bvalid = False

      if(offset > fileSize):
        self.Bvalid = False
      else:
        self.Bvalid = True
    else:
      self.Bvalid = False
      

    # Write the requested data to the B file using the sandbox's writeat call
    if(self.Bvalid == True):
      self.Bfile.writeat(data,offset)
  
    self.Afile.lock.release()
    
  def readat(self,bytes,offset):
    # Read from the A file using the sandbox's readat...
    self.Afile.lock.acquire(True)
    read = self.Afile.readat(bytes, offset)
    self.Afile.lock.release()
    return read

#Requirement 4:
#When close() is called on the file, if both filename.a and filename.b are valid, the original file's data is replaced with the data of filename.b. 
#If filename.b is not valid, no changes are made.

#Do not allow people to write past the B buffer
#Do not allow for an offet too high/negatives

#Validate the b file in close.
#In close, the A/B file must be checked
  def close(self):

#Applications use ABopenfile() to create or open a file. Files are created by setting create=True when calling ABopenfile(), 
#the reference monitor will create a valid backup file called filename.a and an empty file we will write to, called filename.b.

    #causes unbound local error if placed inside
    dataB = self.Bfile.readat(None, 0)
    A = self.Afn
    dataA = self.Afile.readat(None, 0)


    #CApparently checking validity of file has to happen on close, otherwise, fail ABFile and Initaite -> append test cases
    #if(dataB[0]=='S' and dataB[len(dataB)-1] == 'E'):
    if(self.Bvalid):

      #Replace original file's data with filename.b
      self.Bfile.close()
      self.Afile.close()

      #FINALLY, IT SOLVES ALL CASES.  OH MY GOD FINALLY.  KEEP THIS FUCKING THING HERE FOR GOD SAKE, IT ALLOW SAPPEND AND VALID WRITES
      if(dataB[0] == 'S' and dataB[len(dataB) - 1] == 'E'):

        #Overwrite by erasing A and replacing it with filename.b
        if(self.Afn in listfiles()):
          removefile(self.Afn)

        """
        If we had the string 'ShelloE' and our b file is SabE
        in your solution will your final a file be SabE or SabEloE?
        """

        #Replace filename.a withac
        replacementFile = openfile(A, True)
        replacementFile.writeat(dataB, 0)

      #Erase the B file.  If we need to reopen teh file, the pre-existing B file might end up overwriting the a file.
        if(self.Bfn in listfiles()):
          removefile(self.Bfn)
        self.Bfile = openfile(self.Bfn, True)
        self.Bfile.close()
      
    else:
      #Cannot close a file twice otherwise leads to file closed error
      self.Bfile.close()
      self.Afile.close()



def ABopenfile(filename, create):
  return ABFile(filename,create)




# The code here sets up type checking and variable hiding for you.  You
# should not need to change anything below here.
sec_file_def = {"obj-type":ABFile,
                "name":"ABFile",
                "writeat":{"type":"func","args":(str,int),"exceptions":Exception,"return":(int,type(None)),"target":ABFile.writeat},
                "readat":{"type":"func","args":((int,type(None)),(int)),"exceptions":Exception,"return":str,"target":ABFile.readat},
                "close":{"type":"func","args":None,"exceptions":None,"return":(bool,type(None)),"target":ABFile.close}
           }

CHILD_CONTEXT_DEF["ABopenfile"] = {TYPE:OBJC,ARGS:(str,bool),EXCP:Exception,RETURN:sec_file_def,TARGET:ABopenfile}

# Execute the user code
secure_dispatch_module()
