from PySide import QtCore, QtGui
import os
import random
import re
import imp
import sys
import pyseq as seq  
from PyQt4.Qt import QString

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
		b1 = QtGui.QListWidget(display)
		for i in self.listseq4:
			b1.addItem(i)
# 			print i
		

		display.exec_()


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
		self.listseq3.append(itemSelected)
		path = QtCore.QDir.currentPath()

		self.fileSelected.emit(os.path.join( self.path , itemSelected))		
		directory = QtCore.QDir(os.path.join(path,'sequenceFileSelector'))
		self.listseq2 = list(directory.entryList(QtCore.QDir.AllEntries))
		for i in self.listseq2:
			print str(i)
 		
 		
		for i in range(len(self.listseq2)):
			ic = self.listseq2[i]
			
			c = ic.split(".")
			for d in self.listseq3:
				e = d.split(".")
				if str(c[0]) == str(e[0]):
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
        """
        Create gui.
        """
        
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
#         self.listfile.gotoparent.connect(self.goToParent)
        
        
        self.directorylist.doubleClicked.connect(self.selectdirectory)
        self.directorylist.itemSelected.connect(self.selectdirectory)
#         self.directorylist.gotoparent.connect(self.goToParent)


 
        self.setLayout(layout)
        self.setWindowTitle("Sequential File Selector-Isabelle Chen - Generalist / pipeline TD Test")
        pathEdit.setText(self.path)
        
	

	           
    def setCurrentDirPath(self , path ):
    	
# os.path.join(QtCore.QDir.cleanPath(QtCore.QDir.currentPath()), fileRoot)
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
#             for fn in files:
# 				self.addItem(fn ,FileSequenceWidget.FILE)

        if self._splitSequence == False: 
            sequences, others,self.listseq5 = file_seq.find(path)
#             for i in self.listseq2:
#             	print i
            
            for s in sequences:
                self.addItem(str(s), FileSequenceWidget.SEQUENCE)
                self.listseq[str(s)] = s

            for o in others:
				self.addItem(o , FileSequenceWidget.FILE)
        else:
            files = [e for e in os.listdir(path) if os.path.isfile(os.path.join(path, e))]
            for fn in files:
            	self.addItem(fn ,FileSequenceWidget.FILE)
	
    """
    refresh the filelist
    """
    def refresh( self ):
        self.setCurrentDirPath( self.path)



    """
        Set Action for the context Menu of DirectoryList
        @param action list of action.
    """
    def setContextMenuActionDirectoryList( self , action):
        self.directorylist.setContextMenuAction( action )
	
    """
        Set Action for the context Menu of DirectoryList
        @param action list of action.
    """
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
        """Return the filename for the given absolute number in the sequence."""
        if number >= self.first and number <= self.last:
            return "".join([self.head,
                           str(number).zfill(self.padding),
                           self.tail])
        else:
            raise IndexError, "number out of sequence range"

    def format(self, template="{head}%0{padding}d{tail}", padchar="#"):
        """Return the file sequence as a formatted string according to
        the given template. Due to the use of format(), this method requires
        Python 2.6 or later.

        The template supports all the basic sequence attributes, i.e.
        head, tail, first, last, length, padding, path. 

        In addition, it supports the following:

        padchars - character repeated to match padding (at least one)
        range - sequence range as a string, first-last
        """

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
        """
        Find all file sequences at the given path. Returns a tuple (sequences, other_files).
        """
        files = [e for e in os.listdir(search_path)
                 if os.path.isfile(os.path.join(search_path, e))]
        sequences, other_files, oriseq = cls.find_in_list(files)
        for sequence in sequences:
            sequence.path = search_path
        return sequences, other_files, oriseq
       
	

    @classmethod
    def find_in_list(cls, entries):
    	
    	other_files = []
    	
    	origin_sequence = []

    		
        """
        Find all file sequences in a list of files. Returns a tuple (sequences, other_files).
        """
        sequences = []


        # We sort the list to ensure that padded entries are found before any
        # unpadded equivalent.

        entries.sort()

        # Our strategy here is to pop a filename off the list, and search the
        # remaining entries for adjacent files that would indicate it is part of
        # a file sequence.

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

                # Since the list is sorted, we know 0999 will always appear before 1000
                # so this should be safe.

                if components[i].startswith("0"):
                    padding = len(components[i])
                else:
                    padding = 0

                # First, we attempt to find the upper bound of this sequence..
                for filename, number in adjacent_files(components, i, padding):
                    if filename in entries:
                    	origin_sequence.append(filename)
                        entries.remove(filename)
                        last = number
                    else:
                        break

                # ..and then the lower bound.
                for filename, number in adjacent_files(components, i, padding, reverse=True):
                    if filename in entries:
                        entries.remove(filename)
                        first = number
                    else:
                        break

                if (first - last):
                    # We've found what looks like a sequence of files.
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
                # This file is not part of any sequence.
                other_files.append(entry)

        return sequences, other_files, origin_sequence


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

        











