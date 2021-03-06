""""

Ing****ty Programming Test

Sequential File Selector

A small gui program for displaying and selecting sequential files.

Use "createFiles.py" to create a batch of test files.  Modify the fileRoot as necessary for your system.

Should run as follows:
- User browses their computer and selects a folder
- This populates a list widget with the files in that folder
- Sequential files should be collapsed to the following format:

	[baseName].%[framePadding].[extension] [startFrame]-[endFrame]

	Frame padding is always separated from the filename by a period.

	for example:
	taco.0001.jpg
	taco.0002.jpg
	taco.0003.jpg
	
	would collapse to:
	taco.%04d.jpg 1-3

	but:
	comp_v001.mb
	comp_v002.mb

	would not collapse as there is no frame padding

- User can multi select files in this list
- A pressable button displays a message box listing the actual files the user selected

	ex: If the user selected taco.%04d.jpg 1-3, the message box would display
	taco.0001.jpg, taco.0002.jpg, taco.0003.jpg

The program should be created in Python 2.7 with the gui done in PySide.  Please refrain from using other third party libraries outside of PySide as we may not have them installed.
""""

from PySide import QtCore, QtGui
import os
import random
import re
import imp
import sys
from PyQt4.Qt import QString, QListWidget

# root where the files will be created
fileRoot = '/sequenceFileSelector/'

# make the directory if it doesn't exist
try:
	os.makedirs(fileRoot)
except Exception as err:
	# raise the error only if the directory doesn't exist
	if not os.path.isdir(fileRoot):
		raise err
	



class LineEditWidget(QtGui.QLineEdit):

    def keyPressEvent(self, e):
        if ( e.key() == QtCore.Qt.Key_Return or 
           e.key() == QtCore.Qt.Key_Enter ) :
            return

        return QtGui.QLineEdit.keyPressEvent(self, e)


class ListWidget(QtGui.QListWidget):

    itemSelected = QtCore.Signal()
    gotoparent = QtCore.Signal()
    _actioncontentmenu = []
	
    def keyPressEvent(self, e):
        if ( e.key() == QtCore.Qt.Key_Return or 
           e.key() == QtCore.Qt.Key_Enter  or		
           e.key() == QtCore.Qt.Key_Right) : 
            self.itemSelected.emit()
            return
				
        if ( e.key() == QtCore.Qt.Key_Backspace or 
            e.key() == QtCore.Qt.Key_Left) :
                self.gotoparent.emit()
                return 
			
        return QtGui.QListWidget.keyPressEvent(self, e)



    def isSelectedSequence(self ):
        if len( self.currentIndex().data().split("[") ) > 1:
            return True
        else:
            return False



		
class FileSequenceWidget(QtGui.QWidget):
		 
    FOLDER = 0
    FILE = 1 
    SEQUENCE =2 

    fileSelected = QtCore.Signal(str)
    pathChanged = QtCore.Signal(str)
    
    def saveDialog(self, force=True):

		display = QtGui.QDialog()
		display.setWindowTitle("List Sequence Files")
		display.setFixedWidth(250)
		display.setFixedHeight(190)
	
		b1 = QtGui.QListWidget(display)
		b1.reset()
		for i in self.listseq4:
			print i
			print'--'
			b1.addItem(i)
		
		
		display.exec_()
		self.listseq2[:] = []
		self.listseq3[:] = []
		self.listseq4[:] = []
	


    def getFilenameSelected( self ):
    	
        itemSelected = self.listfile.currentIndex().data()
        return os.path.join( self.path , itemSelected )

    def getDirectorySelected( self ):
    	
        dirSelected = self.directorylist.currentIndex().data()
        return os.path.join( self.path , dirSelected )


    def selectdirectory(self):
    	
        rows =  self.directorylist.selectionModel().selectedRows()
        itemSelected = rows[0].data()
        if  os.path.isdir(os.path.join( self.path , itemSelected)) :
			self.path = os.path.normpath( os.path.join( self.path , itemSelected) ) 
			self.pathEdit.setText( self.path )


    def selectfile(self, number):
    	
		itemSelected = self.listfile.currentIndex().data()
		if itemSelected in self.listseq3 :
			pass
		else:

			self.listseq3.append(itemSelected)

		path = QtCore.QDir.currentPath()

		self.fileSelected.emit(os.path.join( self.path , itemSelected))		
		directory = QtCore.QDir(os.path.join(path,'sequenceFileSelector'))
		self.listseq2 = list(directory.entryList(QtCore.QDir.AllEntries))

 		
 		
		for i in range(len(self.listseq2)):
			ic = self.listseq2[i]
			c = ic.split(".")
			for d in self.listseq3:
				e = d.split(".")
				if str(c[0]) == str(e[0]):
					if ic in self.listseq4 :
						pass
					else:
						print 'append'
						print ic
						self.listseq4.append(ic)

					
  					 
		
		
		files = [e for e in os.listdir(path) if os.path.isfile(os.path.join(path, e))]
		


    def addItem(self, fn,typefile ):
    	
    	item = QtGui.QListWidgetItem()
        item.setText(fn)
        item.setIcon(self.icons[typefile])
        if typefile == FileSequenceWidget.FOLDER:
        	self.directorylist.addItem(item)
        else:
        	self.listfile.addItem(item)


    
    def initInternalVar(self ):
    	
        self._splitSequence = False
        self.iconFile = QtGui.QIcon("icons\\file.png")
        self.iconFolder = QtGui.QIcon("icons\\folder.png")
        self.iconSequence = QtGui.QIcon("icons\\sequence.png")
        self.icons = {} 
        self.icons[FileSequenceWidget.FOLDER] = self.iconFolder
        self.icons[FileSequenceWidget.FILE] = self.iconFile
        self.icons[FileSequenceWidget.SEQUENCE] = self.iconSequence
        


    def __init__(self, path, parent=None):
    
        super(FileSequenceWidget, self).__init__(parent)
        self.path = QtCore.QDir.currentPath()
        self.listseq = {}
        self.listseq2=[]
        self.listseq3=[]
        self.listseq4=[]
        self.listseq5=[]
        self.initInternalVar()
        
        pathEdit = LineEditWidget()
        self.pathEdit = pathEdit

		

        self.listfile = ListWidget()
        self.listfile.setSelectionMode(QtGui.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.directorylist = ListWidget()
        label = QtGui.QLabel("Directory")	

        splitter = QtGui.QSplitter()
        splitter.addWidget(self.directorylist)
        splitter.addWidget(self.listfile)
                
        self.listing_btn = QtGui.QPushButton("List Selected")


		
        layout = QtGui.QGridLayout()

        layout.addWidget(splitter,1,0,1,3)
        layout.addWidget(self.listing_btn,3,2)
        layout.addWidget(pathEdit, 3.5, 0.5,1,1)
        

        label.setBuddy(pathEdit)
        self.listing_btn.clicked.connect(self.saveDialog)



        self.pathEdit.textChanged.connect(self.setCurrentDirPath)
        self.listfile.clicked.connect(self.selectfile)
        
        
        self.directorylist.doubleClicked.connect(self.selectdirectory)
#         self.directorylist.itemSelected.connect(self.selectdirectory)
        



 
        self.setLayout(layout)
        self.setWindowTitle("Sequential File Selector-Isabelle Chen - Generalist / pipeline TD Test")
        pathEdit.setText(self.path)
        
	

	           
    def setCurrentDirPath(self , path ):
    	
        self.path = path
        
        
        self.directorylist.clear()
        self.listfile.clear()
        self.listseq.clear()

        self.pathChanged.emit( path )

        directory = QtCore.QDir(path)
        files = list(directory.entryList(QtCore.QDir.AllDirs))
        for fn in files:
       	    if fn == ".":
        	    continue
        	
            self.addItem(fn ,FileSequenceWidget.FOLDER)
            files = [e for e in os.listdir(path) if os.path.isfile(os.path.join(path, e))]

        if self._splitSequence == False: 
            sequences, others = file_seq.find(path)

            
            for s in sequences:
                self.addItem(str(s), FileSequenceWidget.SEQUENCE)
                self.listseq[str(s)] = s

            for o in others:
				self.addItem(o , FileSequenceWidget.FILE)
        else:
            files = [e for e in os.listdir(path) if os.path.isfile(os.path.join(path, e))]
            for fn in files:
            	self.addItem(fn ,FileSequenceWidget.FILE)
	

    def refresh( self ):
        self.setCurrentDirPath( self.path)


    def setContextMenuActionDirectoryList( self , action):
        self.directorylist.setContextMenuAction( action )
	

    def setContextMenuActionFileList( self , action):
        self.listfile.setContextMenuAction( action )

    def getSequenseObj( self , filename):
        return self.listseq[filename]

    def isSequence(self, filename):
        return filename in self.listseq 
    
    @property
    def selectedpath( self):
        return self.getDirectorySelected()

class file_seq():



    NUMBER_PATTERN = re.compile("([0-9]{1,8})")

    def __init__(self, path = "", head = "", tail = "", first = 0, last = 0, padding = 0):
        self.path = ""
        self.head = head
        self.tail = tail
        self.first = first
        self.last = last
        self.padding = padding

    def __len__(self):
        return (self.last - self.first) + 1

    def __repr__(self):
        return "".join([self.head,
                        "[",
                        str(self.first).zfill(self.padding), 
                        "-", 
                        str(self.last).zfill(self.padding),
                        "]",
                        self.tail])

    def __iter__(self):
        def filesequence_iter_generator():
            for n in range(self.first, self.last + 1):
                yield self.filename(n)
        return filesequence_iter_generator()

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self.__getitem__(i)
                    for i in xrange(*key.indices(len(self)))]
        else:
            if isinstance(key, int):
                if key >= 0:
                    return self.filename(self.first + key)
                else:
                    return self.filename(self.last - (key * -1) + 1)
            else:
                raise TypeError, "sequence indexes must be integers"
            
    def filename(self, number):
    	
        if number >= self.first and number <= self.last:
            return "".join([self.head,
                           str(number).zfill(self.padding),
                           self.tail])
        else:
            raise IndexError, "number out of sequence range"

    def format(self, template="{head}%0{padding}d{tail}", padchar="#"):


        values = {"head": self.head,
                  "tail": self.tail,
                  "first": self.first,
                  "last": self.last,
                  "length": len(self),
                  "padding": self.padding,
                  "padchars": padchar * self.padding or padchar,
                  "range": "-".join([str(self.first), str(self.last)]),
                  "path": self.path}

        return template.format(**values)

    @property
    def name(self):
        return self.head.rstrip('.')

    @property
    def extension(self):
        return self.tail.split('.')[-1]

    @property
    def files(self):
        for filename in iter(self):
            yield os.path.join(self.path, filename)

    @classmethod
    def find(cls, search_path):

        files = [e for e in os.listdir(search_path)
                 if os.path.isfile(os.path.join(search_path, e))]
        sequences, other_files = cls.find_in_list(files)
        for sequence in sequences:
            sequence.path = search_path
        return sequences, other_files
       
	

    @classmethod
    def find_in_list(cls, entries):
    	
    	other_files = []  		
        sequences = []
        entries.sort()


        while entries:

            entry = entries.pop(0)
            sequence = None

            def adjacent_files(components, index, padding, reverse=False):
                adj_components = components[:]
                number = long(components[index])

                if reverse:
                    for n in xrange(number - 1, 0, -1):
                        adj_components[index] = str(n).zfill(padding)
                        yield ''.join(adj_components), n
                else:
                    for n in xrange(number + 1, number + len(entries) + 1):
                        adj_components[index] = str(n).zfill(padding)
                        yield ''.join(adj_components), n

            components = cls.NUMBER_PATTERN.split(entry)
 
            for i in range(len(components) - 2, 0, -2):


                first = int(components[i])
                last = int(components[i])

                if components[i].startswith("0"):
                    padding = len(components[i])
                else:
                    padding = 0
                
                w = -1
                for filename in components:
                	w = str(filename)
                	a = os.path.splitext(w)
               	
                	if '.pdf' in a:
                		components.remove(filename)
                	elif '.mb' in a :
                		components.remove(filename)
						
					
                for filename, number in adjacent_files(components, i, padding):
                    if filename in entries:
                        entries.remove(filename)
                        last = number
                    else:
                        break

                for filename, number in adjacent_files(components, i, padding, reverse=True):
                    if filename in entries :
                        entries.remove(filename)
                        first = number
                    else:
                        break

                if (first - last):

                    sequence = file_seq("",
                                            "".join(components[:i]), 
                                            "".join(components[i + 1:]),
                                            first,
                                            last,
                                            padding)
                    break
                else:
                    pass

            if sequence:
                sequences.append(sequence)
            else:

                other_files.append(entry)

        return sequences, other_files


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    model = FileSequenceWidget(QtCore.QDir.homePath())
    model.show()



    sys.exit(app.exec_())

        
        
        
        


        
             
# filenames
files = {
	'taco.%04d.jpg': 5,
	'tuesday.%02d.jpg': 2,
	'reel.mov': 1,
	'box.mb': 1,
	'box2.mb': 1,
	'box3.mb': 1,
	'comp_v001.mb': 1,
	'comp_v002.mb': 1,
	'comp_v003.mb': 1,
	'split.001.jpg': 1,
	'split.003.jpg': 1,
	'split.004.jpg': 1,
	'underOverTen.0009.png': 1,
	'underOverTen.0010.png': 1,
	'underOverTen.0011.png':1,
	'underOverTen.0012.png':1,
	'long.file.name.%04d.pdf': 4,
	'another.one.%01d.jpg': 3,
}

# make the files
for name, count in files.iteritems():
	if count == 1:
		open(fileRoot + name, 'w+')
	else:
		for i in range(1, count+1):
			open(fileRoot + name % i, 'w+')

        











