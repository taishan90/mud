from types import StringType, FunctionType, BooleanType

import util
from exceptions import Match, NoMatch

# could call "parser" CmdContext
class CmdMap:

    def __init__(self):
        self.possibleNext = {}
        self.callback = None
        self.nextTokenNode = None
        self.abbrev = True

    def addCmd(self, cmd, callback, abbrev = True ):
        addCmdCheckPreconds( cmd, callback, abbrev)
        addCmdFromNextToken( self, cmd, callback, abbrev )
        return self

    # rename to map?
    # rename exceptions to "CallbackFound" "NoCallbackFound"
    # str is cmd to be matched
    def match( self, cmd ):

         #print " match started!"

         assert type(cmd) == StringType, "CmdMap.match received a cmd that wasn't a string"

         if len(cmd) == 0:
             raise NoMatch
    
         (first, cmd) = util.first_token(cmd)

         #print " match with first=", first
         #print " cmd=", cmd

         assert len(first) > 0, "CmdMap.match received a first of length 0 from util.first_token"

         node = self

         for nextChar in first:
             if nextChar in node.possibleNext:
                 node = node.possibleNext[ nextChar ]
             else:
                 raise NoMatch

             if len(cmd) > 0 and node.nextTokenNode:
                 node.nextTokenNode.match( cmd )

         if node.noAbbrev:
             raise NoMatch

         #print "raising match with callback ", node.callback

         #print "raising match with first %s, remaining %s" % (first, cmd)

         cmd = cmd.lstrip()

         if len(cmd) == 0:
             cmd = None

         raise Match(node.callback, cmd)


    def __init__(self):
        self.possibleNext = {}
        self.callback = None
        self.nextTokenNode = None
        self.noAbbrev = False


    # @todo add noAbbrev and callback data to str
    #       without breaking unit tests
    def __str__helper(self, prefix=""):
        #print "toString on CmdMap id %i with prefix %sEND" % (id(self), prefix)
        toReturn = ""

        for char in self.possibleNext:
            toReturn += prefix + char + "\n"
        
        if self.nextTokenNode:
            assert len(prefix) > 0, "trie.__str__ len(prefix) == 0 (no chars matched) but a nextTokenNode exists"
            toReturn += self.nextTokenNode.__str__helper( prefix + " " )
        else:
            #print "nextTokenNode null for prefix %s" % prefix
            pass

        for char in self.possibleNext:
            toReturn += self.possibleNext[char].__str__helper( prefix + char )

        return toReturn


    def __str__(self):
        return self.__str__helper()





################################
###### Internal ###############
################################

def addCmdCheckPreconds( cmd, callback, abbrev):
    assert type(cmd) == StringType, "CmdMap.addCmd received cmd that wasn't a string"
    assert len(cmd) > 0, "CmdMap.addCmd received cmd of length 0"
    assert type(callback) == FunctionType, "CmdMap.addCmd received callback that wasn't a function"
    assert type(abbrev) == BooleanType, "CmdMap.addCmd received noAbbrev that wasn't a bool"


def addCmdFromNextChar( cmdMap, char, cmdRemainingTokens, callback, abbrev):

    #print "next char: ", nextChar
    if char not in cmdMap.possibleNext:
        cmdMap.possibleNext[ char ] = CmdMap()
        #print "adding callback", callback
        cmdMap.possibleNext[ char ].callback = callback
        cmdMap.possibleNext[ char ].abbrev = abbrev
    else:
        if not cmdMap.possibleNext[ char ].abbrev and abbrev:
            cmdMap.possibleNext[ char ].callback = callback
            cmdMap.possibleNext[ char ].abbrev = True

    if len(cmdRemainingTokens) > 0:
        #print "should add next token node"
        if not cmdMap.possibleNext[ char ].nextTokenNode:
            cmdMap.possibleNext[ char ].nextTokenNode = CmdMap()

        cmdMap.possibleNext[ char ].nextTokenNode.addCmd( cmdRemainingTokens, callback, abbrev )

    return cmdMap.possibleNext[ char ]
    

def addCmdFromNextToken( cmdMap, cmd, callback, abbrev ):

    (cmdFirstToken, cmdRemainingTokens) = util.first_token(cmd)

    assert len(cmdFirstToken) > 0, "CmdMap.addCmdFromNextToken received length 0 cmdFirstToken from util.firstToken. This should never happen... @Todo unless cmd is all whitespace"
        
    for char in cmdFirstToken:
        cmdMap = addCmdFromNextChar( cmdMap, char, cmdRemainingTokens, callback, abbrev )

    if len(cmdRemainingTokens) == 0:
        cmdMap.abbrev = True
            
 

def mapFromNextToken( cmdMap, cmd):
    (cmdFirstToken, cmdRemainingTokens) = util.first_token(cmd)

    assert len(cmdFirstToken) > 0, "CmdMap.mapFromNextToken received length 0 cmdFirstToken from util.firstToken. This should never happen... @Todo unless cmd is all whitespace"
  
    for char in cmdFirstToken:





def mapFromNextChar( cmdMap, cmd):
    pass
