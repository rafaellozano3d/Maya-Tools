'''
Created on 25 oct. 2017

@author: rafaellozano3d.com/devBlog
'''

import Tkinter
import tkFileDialog
import os


class Structure:

    def __init__(self):
        # Initializing parameters
        self.folders = 0
        self.files = 0
        self.dic = {}

    def createDefaultData(self):
        # Generate and return a default dictionary
        self.dic = {
                        "root":
                        {
                            "a":
                            {
                                "file1": None
                            },
                            "b":
                            {
                                "file1": None,
                                "x": {},
                                "y":
                                {
                                    "file1": None,
                                    "file2": None
                                }
                            },
                            "c":
                            {
                                "file1": None,
                                "file2": None,
                                "file3": None
                            },
                            "d":
                            {
                                "file1": None,
                                "x":
                                {
                                    "xx":
                                    {
                                        "file1": None
                                    }
                                },
                                "file2": None
                            }
                        }
                    }

        return self.dic

    '''
    createDataFromPath: Method to get a path to request a dictionary
        - path:         OS root path from which to generate a dictionary
    '''
    def createDataFromPath(self):
        # TODO
        root = Tkinter.Tk()

        # Hide Tkinter window
        root.withdraw()

        currdir = os.getcwd()
        tempdir = tkFileDialog.askdirectory(
            parent=root, initialdir=currdir,
            title='Please select a directory')

        self.dic = self.createStructure(tempdir)

        return self.dic

    '''
    createStructure: Method to create a dictionary from received path
        - rootdir:   path to analyze
    '''
    def createStructure(self, rootdir):
        # Create a dictionary from input path
        tempDir = {}
        rootdir = rootdir.rstrip(os.sep)
        start = rootdir.rfind(os.sep) + 1
        for path, dirs, files in os.walk(rootdir):
            folders = path[start:].split(os.sep)
            subdir = dict.fromkeys(files)
            parent = reduce(dict.get, folders[:-1], tempDir)
            parent[folders[-1]] = subdir

        return tempDir

    '''
    tabs: Method to return a number of spaces according to the depth
          of the item
        - n:         depth of item
    '''
    def tabs(self, n):
        return ' ' * n * 4

    '''
    listDictionary: Method to print the full dictionary recursively
        - src:        path to analyze
        - dpth:       Depth of the current item
        - key:        Key that identifies the current item
        - father:     Element that identifies the father of the current item
    '''
    def listDictionary(self, src, dpth=0, key='', father=''):

        if isinstance(src, dict):
            for key, value in src.iteritems():
                # If the item has no parent, it is the root item
                if father == '':
                    print key
                else:
                    if value is not None:
                        # In this case, it is a parent item
                        print "" + self.tabs(dpth) + key

                self.listDictionary(value, dpth + 1, key, key)

        else:
            if src is not None:
                # It is a child item
                print self.tabs(dpth) + '- ' + src

    '''
    setNumElements: Method to set the number of elements
                    contained in the current item
        - src:        path to analyze
        - dpth:       Depth of the current item
        - key:        Key that identifies the current item
        - father:     Element that identifies the father of the current item
    '''
    def setNumElements(self, src, dpth=0, toSearch='', key='', father=''):

        if isinstance(src, dict):
            if toSearch in src:
                self.countElements(src, toSearch)
                return

            for key, value in src.iteritems():
                self.setNumElements(value, dpth + 1, toSearch, key, key)

    '''
    countElements:     Method to count the number of times an item
                       appears in a dictionary
        - src:         path to analyze
        - toSearch:    Element to search
    '''
    def countElements(self, src, toSearch):

        self.files = 0
        self.folders = 0
        fol = 0
        fil = 0

        if src[toSearch] is not None:
            keys = src[toSearch].keys()

            for key in keys:
                if src[toSearch][key] is None:
                    fil = fil + 1
                else:
                    fol = fol + 1

        self.setNumFiles(fil)
        self.setNumFolders(fol)

    '''
    setNumFiles: Method to set the number of files
                 contained in the current item
        - fil:   Number files to set
    '''
    def setNumFiles(self, fil):
        self.files = fil

    '''
    setNumFolders: Method to set the number of folders
                   contained in the current item
        - folder:  Number files to set
    '''
    def setNumFolders(self, fol):
        self.folders = fol

    '''
    getNumFiles: Method to get the number of files
                 contained in the current item
    '''
    def getNumFiles(self):
        return self.files

    '''
    getNumFolders: Method to get the number of files
                   contained in the current item
    '''
    def getNumFolders(self):
        return self.folders
