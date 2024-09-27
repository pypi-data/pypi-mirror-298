"""
"""

class FriendImporter(object):
	#NOTE: not used anymore.
	"""
	"""
	friendClass=None
	friendImportNames=[]
	
	#Import normal ATTRIBUTES, i.e. the ones handeled by the objects.
	def __init__(self,*args,**kwargs):
		friendObject=self.friendClass(*args,**kwargs)
		for name in self.friendImportNames:
			if name in friendObject.__dict__.keys(): # so "name" is handeled by the object (like attributes)
				self.__dict__[name]=friendObject.__dict__[name]
	
	#Import METHOD and CLASS ATTRIBUTES that are handeled by the class, not the objects.
	#This is called at PlatRock launch early state, when FriendImporter class is subclassed (not sub-instanciated).
	def __init_subclass__(child_class):
		for name in child_class.friendImportNames:
			if name in child_class.friendClass.__dict__.keys(): #so "name" is handeled by the class (like methods and class attributes)
				exec('child_class.'+name+'=child_class.friendClass.'+name)

def getRestructuredTextTableString(L,title='',header=True):
	s='\n\n.. list-table:: '+title+'\n'
	if(header):
		s+='   :header-rows: 1\n\n'
	for l in L:
		s+='   * - '+l[0]+'\n'
		for c in l[1:]:
			s+='     - '+c+'\n'
	s+='\n'
	return s

import re
def pyDocPrint(cls):
	entities=[cls]
	for attrName in dir(cls):
		if not attrName.startswith('__'):
			attr=getattr(cls,attrName)
			if callable(attr):
				entities.append(attr)
	for entity in entities:
		s=entity.__doc__
		if (s is None):
			continue
		RE=re.compile(':pyDocPrint:`([_a-zA-Z0-9]*)`')
		matches=re.finditer(RE,s)
		indexes=[]
		varNames=[]
		for m in matches:
			indexes.append(slice(*m.span(0)))
			varNames.append(m.group(1))
		indexes.reverse() #start replacements below by the docstring end to the docstring start to avoid slices to be modified at each replacement.
		varNames.reverse()
		for i,idx in enumerate(indexes):
			indentation = re.search('^[\t ]*', s[:idx.start].split('\n')[-1])
			if indentation:
				indentation=indentation.group(0)
			varName = varNames[i]
			var = getattr(cls,varName)
			varStr = var.__str__()
			varStr=varStr.replace('\n','\n'+indentation)
			s = s[:idx.start]+varStr+s[idx.stop:]
		entity.__doc__ = s

from pygments import formatters, highlight, lexers
def colorPythonError(errStr):
	lexer = lexers.get_lexer_by_name("pytb", stripall=True)
	formatter = formatters.get_formatter_by_name("terminal")
	return highlight(errStr, lexer, formatter)