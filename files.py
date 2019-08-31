# Files I/O functions (files.py)

import enum
import os.path
import io

import ui
import structs

class ext(enum.Enum):
    TXT    = enum.auto()
    JSON   = enum.auto()
    CONFIG = enum.auto()
    XML    = enum.auto()
    LOG    = enum.auto()
    BMP    = enum.auto()
    JPEG   = enum.auto()
    PNG    = enum.auto()
    ANY    = enum.auto()

def Wildcard(extension):
    exts = {
        ext.TXT    : [ 'Ext_TXT', '(*.txt)|*.txt' ],
        ext.JSON   : [ 'Ext_JSON', '(*.json)|*.json' ],
        ext.CONFIG : [ 'Ext_CONFIG', '(*.config)|*.config' ],
        ext.XML    : [ 'Ext_XML', '(*.xml)|*.xml' ],
        ext.LOG    : [ 'Ext_LOG', '(*.log)|*.log' ],
        ext.BMP    : [ 'Ext_BMP', '(*.bmp)|*.bmp' ],
        ext.JPEG   : [ 'Ext_JPEG', '(*.jpg;*.jpeg)|*.jpg;*.jpeg' ],
        ext.PNG    : [ 'Ext_PNG', '(*.png)|*.png' ],
        ext.ANY    : [ 'Ext_ANY', '(*.*)|*.*' ]
    }
    return structs.CurLang('Files', exts[extension][0]) + ' ' + exts[extension][1]

def FileName(filePath, lquote = '', rquote = ''):
    return lquote + os.path.split(filePath)[1] + rquote

def CheckExisting(filePath):
    if not os.path.isfile(filePath):
        return False
    return True

def __OpenFile(filePath,
               dia = False,
               msg = False,
               errStr = structs.CurLang('Files', 'OpenFileDefaultErrStr'),
               extension = ext.ANY):
    if not CheckExisting(filePath):
        msgAns = True
        if msg:
            msgAns = ui.QueDia(structs.CurLang('Files', 'OpenFileTitle'),
                               errStr + structs.CurLang('Files', 'OpenFileContent'))
        if dia and msgAns:
            filePath = ui.FileOpenDia(extension)
        else:
            return None
    if filePath == None:
        return None
    mode = {
        'mode' : 'r'
    }
    if extension in [ext.JSON, ext.LOG, ext.TXT, ext.XML, ext.CONFIG]:
        mode['mode'] = 'r'
        mode['encoding'] = 'utf8'
    else:
        mode['mode'] = 'rb'
    with open(filePath, **mode) as content:
        data = content.read()
    return data

def __SaveFile(data, extension, filePath = None):
    if filePath == None:
        filePath = ui.FileSaveDia(extension)
    
    if filePath != None:
        with open(filePath, 'w', encoding = 'utf8') as content:
            content.write(data)
        return True
    return False

def Open      (filePath,
               dia = False,
               msg = False,
               errStr = structs.CurLang('Files', 'Ext_ANY'),
               extension = ext.ANY):
    return __OpenFile(filePath,
                      dia,
                      msg,
                      errStr,
                      extension)

def OpenJSON  (filePath, dia = False, msg = False, errStr = structs.CurLang('Files', 'Ext_JSON')):
    return Open(filePath,
                dia,
                msg,
                errStr,
                extension = ext.JSON)

def SaveJSON  (data, filePath = None):
    return __SaveFile(data, ext.JSON, filePath)

def OpenPNG   (filePath, dia = False, msg = False, errStr = structs.CurLang('Files', 'Ext_PNG')):
    return Open(filePath,
                dia,
                msg,
                errStr,
                extension = ext.PNG)