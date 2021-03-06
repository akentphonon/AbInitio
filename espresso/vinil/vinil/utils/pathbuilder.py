#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

# Builds path (navigation path) for vinil

# Example of Input:
# list = [["Home","greet","link"], [label, actor, routine]]
# Example of Output
# <a href="###">Home</a> > Settings

# TODO: You can pass only 'actor', 'routine' and 'id' parameters
# Problem:  How to pass arbitrary parameters?


class PathItem:
    def __init__(self, label, actor=None, routine=None, id=None): 
        self.label      = label
        self.actor      = actor
        self.routine    = routine
        self.id         = id

    def isLink(self):
        if self.actor is not None:
            return True
        return False

class Path:
    def __init__(self, list):
        self.populatePath(list)

    def append(self, pathitem):
        self.path.append(pathitem)

    def item(self, idx):
        if self.withinRange(idx, self.path):
            return self.path[idx]
        
        return None

    def size(self):
        return len(self.path)

    def withinRange(self, index, list):
        if index < len(list) and index >= 0:
            return True

        return False
        
    # Populate path from list of tuples in format
    # [["Home", "greet", "link"], [label, actor, routine]]
    def populatePath(self, list):
        self.path       = [] # Empty path
        for i in range(len(list)):
            l   = list[i]
            # Silly way of handling indeces id
            if len(l) == 3:
                self.path.append(PathItem(label=l[0], actor=l[1], routine=l[2]))
            elif len(l) == 4:
                self.path.append(PathItem(label=l[0], actor=l[1], routine=l[2], id=l[3]))

class PathBuilder:
    def __init__(self, list, separator=">"):
        self.separator  = separator
        self.path       = Path(list)
        #self.pathlist   = list # Do I need pathlist?


    def buildPath(self):
        from luban.content.Paragraph import Paragraph
        from luban.content.Document import Document
        from luban.content import load
        from luban.content.Link import Link

        doc     = Document(id='path-content')

        for i in range(self.path.size()):
            item    = self.path.item(i)
            if item.isLink():
                if item.id:     # Handling id
                    pi = Link(label=item.label, onclick=load(actor=item.actor, routine=item.routine, id=item.id))
                else:
                    pi = Link(label=item.label, onclick=load(actor=item.actor, routine=item.routine))
                    
                sep = Paragraph(text=self.separator)
                doc.add(pi)
                doc.add(sep)
            else:
                pi = Paragraph(text=item.label)
                doc.add(pi)

        return doc

    def toString(self):

        s = ""
        for i in range(self.path.size() - 1):
            item    = self.path.item(i)
            s       += "%s %s " % (item.label, self.separator)

        s   += self.path.item(self.path.size() - 1).label
        
        print s
 

if __name__ == "__main__":
    list = [["Home","greet","link"], ["Settings", None, None]]

    pb  = PathBuilder(list)
    pb.toString()
    
__date__ = "$Sep 27, 2009 6:04:06 AM$"


