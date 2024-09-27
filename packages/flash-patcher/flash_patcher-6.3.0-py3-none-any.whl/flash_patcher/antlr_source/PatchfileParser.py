# Generated from ../flash_patcher/antlr_source/PatchfileParser.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,30,157,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,1,0,1,0,1,0,1,0,1,1,4,1,
        42,8,1,11,1,12,1,43,1,1,1,1,1,1,1,1,1,2,4,2,51,8,2,11,2,12,2,52,
        1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,6,4,6,
        70,8,6,11,6,12,6,71,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,7,1,8,
        4,8,85,8,8,11,8,12,8,86,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,9,4,9,97,8,
        9,11,9,12,9,98,1,10,1,10,1,11,1,11,1,11,1,11,1,11,1,12,1,12,1,12,
        1,12,1,12,1,13,1,13,1,13,1,14,1,14,1,14,1,15,1,15,1,15,1,15,1,15,
        1,15,1,15,1,15,1,15,5,15,128,8,15,10,15,12,15,131,9,15,1,16,3,16,
        134,8,16,1,16,1,16,1,16,3,16,139,8,16,1,16,3,16,142,8,16,1,16,1,
        16,1,16,1,16,1,16,3,16,149,8,16,1,16,1,16,3,16,153,8,16,1,17,1,17,
        1,17,0,0,18,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,0,2,
        3,0,17,17,22,22,30,30,2,0,22,22,30,30,159,0,36,1,0,0,0,2,41,1,0,
        0,0,4,50,1,0,0,0,6,54,1,0,0,0,8,58,1,0,0,0,10,64,1,0,0,0,12,69,1,
        0,0,0,14,80,1,0,0,0,16,84,1,0,0,0,18,96,1,0,0,0,20,100,1,0,0,0,22,
        102,1,0,0,0,24,107,1,0,0,0,26,112,1,0,0,0,28,115,1,0,0,0,30,129,
        1,0,0,0,32,152,1,0,0,0,34,154,1,0,0,0,36,37,5,1,0,0,37,38,5,10,0,
        0,38,39,3,32,16,0,39,1,1,0,0,0,40,42,3,0,0,0,41,40,1,0,0,0,42,43,
        1,0,0,0,43,41,1,0,0,0,43,44,1,0,0,0,44,45,1,0,0,0,45,46,5,11,0,0,
        46,47,3,4,2,0,47,48,5,25,0,0,48,3,1,0,0,0,49,51,5,26,0,0,50,49,1,
        0,0,0,51,52,1,0,0,0,52,50,1,0,0,0,52,53,1,0,0,0,53,5,1,0,0,0,54,
        55,5,2,0,0,55,56,3,34,17,0,56,57,3,34,17,0,57,7,1,0,0,0,58,59,5,
        3,0,0,59,60,5,10,0,0,60,61,3,32,16,0,61,62,5,18,0,0,62,63,3,32,16,
        0,63,9,1,0,0,0,64,65,5,4,0,0,65,66,5,10,0,0,66,67,3,32,16,0,67,11,
        1,0,0,0,68,70,3,10,5,0,69,68,1,0,0,0,70,71,1,0,0,0,71,69,1,0,0,0,
        71,72,1,0,0,0,72,73,1,0,0,0,73,74,5,12,0,0,74,75,3,18,9,0,75,76,
        5,27,0,0,76,77,5,11,0,0,77,78,3,4,2,0,78,79,5,25,0,0,79,13,1,0,0,
        0,80,81,5,5,0,0,81,82,5,10,0,0,82,15,1,0,0,0,83,85,3,14,7,0,84,83,
        1,0,0,0,85,86,1,0,0,0,86,84,1,0,0,0,86,87,1,0,0,0,87,88,1,0,0,0,
        88,89,5,12,0,0,89,90,3,18,9,0,90,91,5,27,0,0,91,92,5,11,0,0,92,93,
        3,4,2,0,93,94,5,25,0,0,94,17,1,0,0,0,95,97,5,28,0,0,96,95,1,0,0,
        0,97,98,1,0,0,0,98,96,1,0,0,0,98,99,1,0,0,0,99,19,1,0,0,0,100,101,
        7,0,0,0,101,21,1,0,0,0,102,103,5,6,0,0,103,104,5,22,0,0,104,105,
        5,20,0,0,105,106,3,20,10,0,106,23,1,0,0,0,107,108,5,7,0,0,108,109,
        5,22,0,0,109,110,5,20,0,0,110,111,3,20,10,0,111,25,1,0,0,0,112,113,
        5,8,0,0,113,114,3,34,17,0,114,27,1,0,0,0,115,116,5,9,0,0,116,117,
        3,34,17,0,117,29,1,0,0,0,118,128,3,2,1,0,119,128,3,6,3,0,120,128,
        3,8,4,0,121,128,3,12,6,0,122,128,3,16,8,0,123,128,3,22,11,0,124,
        128,3,24,12,0,125,128,3,26,13,0,126,128,3,28,14,0,127,118,1,0,0,
        0,127,119,1,0,0,0,127,120,1,0,0,0,127,121,1,0,0,0,127,122,1,0,0,
        0,127,123,1,0,0,0,127,124,1,0,0,0,127,125,1,0,0,0,127,126,1,0,0,
        0,128,131,1,0,0,0,129,127,1,0,0,0,129,130,1,0,0,0,130,31,1,0,0,0,
        131,129,1,0,0,0,132,134,5,15,0,0,133,132,1,0,0,0,133,134,1,0,0,0,
        134,135,1,0,0,0,135,136,5,13,0,0,136,138,5,22,0,0,137,139,5,17,0,
        0,138,137,1,0,0,0,138,139,1,0,0,0,139,141,1,0,0,0,140,142,5,16,0,
        0,141,140,1,0,0,0,141,142,1,0,0,0,142,153,1,0,0,0,143,144,5,12,0,
        0,144,145,3,18,9,0,145,148,5,27,0,0,146,147,5,19,0,0,147,149,5,17,
        0,0,148,146,1,0,0,0,148,149,1,0,0,0,149,153,1,0,0,0,150,153,5,17,
        0,0,151,153,5,14,0,0,152,133,1,0,0,0,152,143,1,0,0,0,152,150,1,0,
        0,0,152,151,1,0,0,0,153,33,1,0,0,0,154,155,7,1,0,0,155,35,1,0,0,
        0,12,43,52,71,86,98,127,129,133,138,141,148,152
    ]

class PatchfileParser ( Parser ):

    grammarFileName = "PatchfileParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'('", "')'", 
                     "<INVALID>", "'-'", "'+'", "'='", "'\"'" ]

    symbolicNames = [ "<INVALID>", "ADD", "ADD_ASSET", "REMOVE", "REPLACE", 
                      "REPLACE_ALL", "SET_VAR", "EXPORT_VAR", "EXEC_PATCHER", 
                      "EXEC_PYTHON", "FILENAME", "BEGIN_PATCH", "BEGIN_CONTENT", 
                      "FUNCTION", "END", "OPEN_BLOCK", "CLOSE_BLOCK", "INTEGER", 
                      "DASH", "PLUS", "EQUALS", "QUOTE", "TEXT_BLOCK", "WHITESPACE", 
                      "COMMENT", "END_PATCH", "AS_TEXT", "END_CONTENT", 
                      "CONTENT_TEXT", "END_QUOTE", "QUOTED_TEXT" ]

    RULE_addBlockHeader = 0
    RULE_addBlock = 1
    RULE_addBlockText = 2
    RULE_addAssetBlock = 3
    RULE_removeBlock = 4
    RULE_replaceNthBlockHeader = 5
    RULE_replaceNthBlock = 6
    RULE_replaceAllBlockHeader = 7
    RULE_replaceAllBlock = 8
    RULE_replaceBlockText = 9
    RULE_varValue = 10
    RULE_setVarBlock = 11
    RULE_exportVarBlock = 12
    RULE_execPatcherBlock = 13
    RULE_execPythonBlock = 14
    RULE_root = 15
    RULE_locationToken = 16
    RULE_file_name = 17

    ruleNames =  [ "addBlockHeader", "addBlock", "addBlockText", "addAssetBlock", 
                   "removeBlock", "replaceNthBlockHeader", "replaceNthBlock", 
                   "replaceAllBlockHeader", "replaceAllBlock", "replaceBlockText", 
                   "varValue", "setVarBlock", "exportVarBlock", "execPatcherBlock", 
                   "execPythonBlock", "root", "locationToken", "file_name" ]

    EOF = Token.EOF
    ADD=1
    ADD_ASSET=2
    REMOVE=3
    REPLACE=4
    REPLACE_ALL=5
    SET_VAR=6
    EXPORT_VAR=7
    EXEC_PATCHER=8
    EXEC_PYTHON=9
    FILENAME=10
    BEGIN_PATCH=11
    BEGIN_CONTENT=12
    FUNCTION=13
    END=14
    OPEN_BLOCK=15
    CLOSE_BLOCK=16
    INTEGER=17
    DASH=18
    PLUS=19
    EQUALS=20
    QUOTE=21
    TEXT_BLOCK=22
    WHITESPACE=23
    COMMENT=24
    END_PATCH=25
    AS_TEXT=26
    END_CONTENT=27
    CONTENT_TEXT=28
    END_QUOTE=29
    QUOTED_TEXT=30

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class AddBlockHeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ADD(self):
            return self.getToken(PatchfileParser.ADD, 0)

        def FILENAME(self):
            return self.getToken(PatchfileParser.FILENAME, 0)

        def locationToken(self):
            return self.getTypedRuleContext(PatchfileParser.LocationTokenContext,0)


        def getRuleIndex(self):
            return PatchfileParser.RULE_addBlockHeader

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddBlockHeader" ):
                listener.enterAddBlockHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddBlockHeader" ):
                listener.exitAddBlockHeader(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddBlockHeader" ):
                return visitor.visitAddBlockHeader(self)
            else:
                return visitor.visitChildren(self)




    def addBlockHeader(self):

        localctx = PatchfileParser.AddBlockHeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_addBlockHeader)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.match(PatchfileParser.ADD)
            self.state = 37
            self.match(PatchfileParser.FILENAME)
            self.state = 38
            self.locationToken()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AddBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_PATCH(self):
            return self.getToken(PatchfileParser.BEGIN_PATCH, 0)

        def addBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.AddBlockTextContext,0)


        def END_PATCH(self):
            return self.getToken(PatchfileParser.END_PATCH, 0)

        def addBlockHeader(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.AddBlockHeaderContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.AddBlockHeaderContext,i)


        def getRuleIndex(self):
            return PatchfileParser.RULE_addBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddBlock" ):
                listener.enterAddBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddBlock" ):
                listener.exitAddBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddBlock" ):
                return visitor.visitAddBlock(self)
            else:
                return visitor.visitChildren(self)




    def addBlock(self):

        localctx = PatchfileParser.AddBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_addBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 40
                self.addBlockHeader()
                self.state = 43 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1):
                    break

            self.state = 45
            self.match(PatchfileParser.BEGIN_PATCH)
            self.state = 46
            self.addBlockText()
            self.state = 47
            self.match(PatchfileParser.END_PATCH)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AddBlockTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AS_TEXT(self, i:int=None):
            if i is None:
                return self.getTokens(PatchfileParser.AS_TEXT)
            else:
                return self.getToken(PatchfileParser.AS_TEXT, i)

        def getRuleIndex(self):
            return PatchfileParser.RULE_addBlockText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddBlockText" ):
                listener.enterAddBlockText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddBlockText" ):
                listener.exitAddBlockText(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddBlockText" ):
                return visitor.visitAddBlockText(self)
            else:
                return visitor.visitChildren(self)




    def addBlockText(self):

        localctx = PatchfileParser.AddBlockTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_addBlockText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 49
                self.match(PatchfileParser.AS_TEXT)
                self.state = 52 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==26):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AddAssetBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.local = None # File_nameContext
            self.swf = None # File_nameContext

        def ADD_ASSET(self):
            return self.getToken(PatchfileParser.ADD_ASSET, 0)

        def file_name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.File_nameContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.File_nameContext,i)


        def getRuleIndex(self):
            return PatchfileParser.RULE_addAssetBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddAssetBlock" ):
                listener.enterAddAssetBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddAssetBlock" ):
                listener.exitAddAssetBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddAssetBlock" ):
                return visitor.visitAddAssetBlock(self)
            else:
                return visitor.visitChildren(self)




    def addAssetBlock(self):

        localctx = PatchfileParser.AddAssetBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_addAssetBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54
            self.match(PatchfileParser.ADD_ASSET)
            self.state = 55
            localctx.local = self.file_name()
            self.state = 56
            localctx.swf = self.file_name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RemoveBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REMOVE(self):
            return self.getToken(PatchfileParser.REMOVE, 0)

        def FILENAME(self):
            return self.getToken(PatchfileParser.FILENAME, 0)

        def locationToken(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.LocationTokenContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.LocationTokenContext,i)


        def DASH(self):
            return self.getToken(PatchfileParser.DASH, 0)

        def getRuleIndex(self):
            return PatchfileParser.RULE_removeBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRemoveBlock" ):
                listener.enterRemoveBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRemoveBlock" ):
                listener.exitRemoveBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRemoveBlock" ):
                return visitor.visitRemoveBlock(self)
            else:
                return visitor.visitChildren(self)




    def removeBlock(self):

        localctx = PatchfileParser.RemoveBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_removeBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self.match(PatchfileParser.REMOVE)
            self.state = 59
            self.match(PatchfileParser.FILENAME)
            self.state = 60
            self.locationToken()
            self.state = 61
            self.match(PatchfileParser.DASH)
            self.state = 62
            self.locationToken()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReplaceNthBlockHeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REPLACE(self):
            return self.getToken(PatchfileParser.REPLACE, 0)

        def FILENAME(self):
            return self.getToken(PatchfileParser.FILENAME, 0)

        def locationToken(self):
            return self.getTypedRuleContext(PatchfileParser.LocationTokenContext,0)


        def getRuleIndex(self):
            return PatchfileParser.RULE_replaceNthBlockHeader

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReplaceNthBlockHeader" ):
                listener.enterReplaceNthBlockHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReplaceNthBlockHeader" ):
                listener.exitReplaceNthBlockHeader(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReplaceNthBlockHeader" ):
                return visitor.visitReplaceNthBlockHeader(self)
            else:
                return visitor.visitChildren(self)




    def replaceNthBlockHeader(self):

        localctx = PatchfileParser.ReplaceNthBlockHeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_replaceNthBlockHeader)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self.match(PatchfileParser.REPLACE)
            self.state = 65
            self.match(PatchfileParser.FILENAME)
            self.state = 66
            self.locationToken()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReplaceNthBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_CONTENT(self):
            return self.getToken(PatchfileParser.BEGIN_CONTENT, 0)

        def replaceBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.ReplaceBlockTextContext,0)


        def END_CONTENT(self):
            return self.getToken(PatchfileParser.END_CONTENT, 0)

        def BEGIN_PATCH(self):
            return self.getToken(PatchfileParser.BEGIN_PATCH, 0)

        def addBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.AddBlockTextContext,0)


        def END_PATCH(self):
            return self.getToken(PatchfileParser.END_PATCH, 0)

        def replaceNthBlockHeader(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.ReplaceNthBlockHeaderContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.ReplaceNthBlockHeaderContext,i)


        def getRuleIndex(self):
            return PatchfileParser.RULE_replaceNthBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReplaceNthBlock" ):
                listener.enterReplaceNthBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReplaceNthBlock" ):
                listener.exitReplaceNthBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReplaceNthBlock" ):
                return visitor.visitReplaceNthBlock(self)
            else:
                return visitor.visitChildren(self)




    def replaceNthBlock(self):

        localctx = PatchfileParser.ReplaceNthBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_replaceNthBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 68
                self.replaceNthBlockHeader()
                self.state = 71 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==4):
                    break

            self.state = 73
            self.match(PatchfileParser.BEGIN_CONTENT)
            self.state = 74
            self.replaceBlockText()
            self.state = 75
            self.match(PatchfileParser.END_CONTENT)
            self.state = 76
            self.match(PatchfileParser.BEGIN_PATCH)
            self.state = 77
            self.addBlockText()
            self.state = 78
            self.match(PatchfileParser.END_PATCH)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReplaceAllBlockHeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REPLACE_ALL(self):
            return self.getToken(PatchfileParser.REPLACE_ALL, 0)

        def FILENAME(self):
            return self.getToken(PatchfileParser.FILENAME, 0)

        def getRuleIndex(self):
            return PatchfileParser.RULE_replaceAllBlockHeader

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReplaceAllBlockHeader" ):
                listener.enterReplaceAllBlockHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReplaceAllBlockHeader" ):
                listener.exitReplaceAllBlockHeader(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReplaceAllBlockHeader" ):
                return visitor.visitReplaceAllBlockHeader(self)
            else:
                return visitor.visitChildren(self)




    def replaceAllBlockHeader(self):

        localctx = PatchfileParser.ReplaceAllBlockHeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_replaceAllBlockHeader)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self.match(PatchfileParser.REPLACE_ALL)
            self.state = 81
            self.match(PatchfileParser.FILENAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReplaceAllBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_CONTENT(self):
            return self.getToken(PatchfileParser.BEGIN_CONTENT, 0)

        def replaceBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.ReplaceBlockTextContext,0)


        def END_CONTENT(self):
            return self.getToken(PatchfileParser.END_CONTENT, 0)

        def BEGIN_PATCH(self):
            return self.getToken(PatchfileParser.BEGIN_PATCH, 0)

        def addBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.AddBlockTextContext,0)


        def END_PATCH(self):
            return self.getToken(PatchfileParser.END_PATCH, 0)

        def replaceAllBlockHeader(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.ReplaceAllBlockHeaderContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.ReplaceAllBlockHeaderContext,i)


        def getRuleIndex(self):
            return PatchfileParser.RULE_replaceAllBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReplaceAllBlock" ):
                listener.enterReplaceAllBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReplaceAllBlock" ):
                listener.exitReplaceAllBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReplaceAllBlock" ):
                return visitor.visitReplaceAllBlock(self)
            else:
                return visitor.visitChildren(self)




    def replaceAllBlock(self):

        localctx = PatchfileParser.ReplaceAllBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_replaceAllBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 84 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 83
                self.replaceAllBlockHeader()
                self.state = 86 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==5):
                    break

            self.state = 88
            self.match(PatchfileParser.BEGIN_CONTENT)
            self.state = 89
            self.replaceBlockText()
            self.state = 90
            self.match(PatchfileParser.END_CONTENT)
            self.state = 91
            self.match(PatchfileParser.BEGIN_PATCH)
            self.state = 92
            self.addBlockText()
            self.state = 93
            self.match(PatchfileParser.END_PATCH)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReplaceBlockTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONTENT_TEXT(self, i:int=None):
            if i is None:
                return self.getTokens(PatchfileParser.CONTENT_TEXT)
            else:
                return self.getToken(PatchfileParser.CONTENT_TEXT, i)

        def getRuleIndex(self):
            return PatchfileParser.RULE_replaceBlockText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReplaceBlockText" ):
                listener.enterReplaceBlockText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReplaceBlockText" ):
                listener.exitReplaceBlockText(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReplaceBlockText" ):
                return visitor.visitReplaceBlockText(self)
            else:
                return visitor.visitChildren(self)




    def replaceBlockText(self):

        localctx = PatchfileParser.ReplaceBlockTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_replaceBlockText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 96 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 95
                self.match(PatchfileParser.CONTENT_TEXT)
                self.state = 98 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==28):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TEXT_BLOCK(self):
            return self.getToken(PatchfileParser.TEXT_BLOCK, 0)

        def QUOTED_TEXT(self):
            return self.getToken(PatchfileParser.QUOTED_TEXT, 0)

        def INTEGER(self):
            return self.getToken(PatchfileParser.INTEGER, 0)

        def getRuleIndex(self):
            return PatchfileParser.RULE_varValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarValue" ):
                listener.enterVarValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarValue" ):
                listener.exitVarValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarValue" ):
                return visitor.visitVarValue(self)
            else:
                return visitor.visitChildren(self)




    def varValue(self):

        localctx = PatchfileParser.VarValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_varValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 100
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1078067200) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SetVarBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.var_name = None # Token

        def SET_VAR(self):
            return self.getToken(PatchfileParser.SET_VAR, 0)

        def EQUALS(self):
            return self.getToken(PatchfileParser.EQUALS, 0)

        def varValue(self):
            return self.getTypedRuleContext(PatchfileParser.VarValueContext,0)


        def TEXT_BLOCK(self):
            return self.getToken(PatchfileParser.TEXT_BLOCK, 0)

        def getRuleIndex(self):
            return PatchfileParser.RULE_setVarBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetVarBlock" ):
                listener.enterSetVarBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetVarBlock" ):
                listener.exitSetVarBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetVarBlock" ):
                return visitor.visitSetVarBlock(self)
            else:
                return visitor.visitChildren(self)




    def setVarBlock(self):

        localctx = PatchfileParser.SetVarBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_setVarBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 102
            self.match(PatchfileParser.SET_VAR)
            self.state = 103
            localctx.var_name = self.match(PatchfileParser.TEXT_BLOCK)
            self.state = 104
            self.match(PatchfileParser.EQUALS)
            self.state = 105
            self.varValue()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExportVarBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.var_name = None # Token

        def EXPORT_VAR(self):
            return self.getToken(PatchfileParser.EXPORT_VAR, 0)

        def EQUALS(self):
            return self.getToken(PatchfileParser.EQUALS, 0)

        def varValue(self):
            return self.getTypedRuleContext(PatchfileParser.VarValueContext,0)


        def TEXT_BLOCK(self):
            return self.getToken(PatchfileParser.TEXT_BLOCK, 0)

        def getRuleIndex(self):
            return PatchfileParser.RULE_exportVarBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExportVarBlock" ):
                listener.enterExportVarBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExportVarBlock" ):
                listener.exitExportVarBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExportVarBlock" ):
                return visitor.visitExportVarBlock(self)
            else:
                return visitor.visitChildren(self)




    def exportVarBlock(self):

        localctx = PatchfileParser.ExportVarBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_exportVarBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self.match(PatchfileParser.EXPORT_VAR)
            self.state = 108
            localctx.var_name = self.match(PatchfileParser.TEXT_BLOCK)
            self.state = 109
            self.match(PatchfileParser.EQUALS)
            self.state = 110
            self.varValue()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExecPatcherBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EXEC_PATCHER(self):
            return self.getToken(PatchfileParser.EXEC_PATCHER, 0)

        def file_name(self):
            return self.getTypedRuleContext(PatchfileParser.File_nameContext,0)


        def getRuleIndex(self):
            return PatchfileParser.RULE_execPatcherBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExecPatcherBlock" ):
                listener.enterExecPatcherBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExecPatcherBlock" ):
                listener.exitExecPatcherBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExecPatcherBlock" ):
                return visitor.visitExecPatcherBlock(self)
            else:
                return visitor.visitChildren(self)




    def execPatcherBlock(self):

        localctx = PatchfileParser.ExecPatcherBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_execPatcherBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 112
            self.match(PatchfileParser.EXEC_PATCHER)
            self.state = 113
            self.file_name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExecPythonBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EXEC_PYTHON(self):
            return self.getToken(PatchfileParser.EXEC_PYTHON, 0)

        def file_name(self):
            return self.getTypedRuleContext(PatchfileParser.File_nameContext,0)


        def getRuleIndex(self):
            return PatchfileParser.RULE_execPythonBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExecPythonBlock" ):
                listener.enterExecPythonBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExecPythonBlock" ):
                listener.exitExecPythonBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExecPythonBlock" ):
                return visitor.visitExecPythonBlock(self)
            else:
                return visitor.visitChildren(self)




    def execPythonBlock(self):

        localctx = PatchfileParser.ExecPythonBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_execPythonBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.match(PatchfileParser.EXEC_PYTHON)
            self.state = 116
            self.file_name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RootContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def addBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.AddBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.AddBlockContext,i)


        def addAssetBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.AddAssetBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.AddAssetBlockContext,i)


        def removeBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.RemoveBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.RemoveBlockContext,i)


        def replaceNthBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.ReplaceNthBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.ReplaceNthBlockContext,i)


        def replaceAllBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.ReplaceAllBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.ReplaceAllBlockContext,i)


        def setVarBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.SetVarBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.SetVarBlockContext,i)


        def exportVarBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.ExportVarBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.ExportVarBlockContext,i)


        def execPatcherBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.ExecPatcherBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.ExecPatcherBlockContext,i)


        def execPythonBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.ExecPythonBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.ExecPythonBlockContext,i)


        def getRuleIndex(self):
            return PatchfileParser.RULE_root

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoot" ):
                listener.enterRoot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoot" ):
                listener.exitRoot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoot" ):
                return visitor.visitRoot(self)
            else:
                return visitor.visitChildren(self)




    def root(self):

        localctx = PatchfileParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_root)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 129
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1022) != 0):
                self.state = 127
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [1]:
                    self.state = 118
                    self.addBlock()
                    pass
                elif token in [2]:
                    self.state = 119
                    self.addAssetBlock()
                    pass
                elif token in [3]:
                    self.state = 120
                    self.removeBlock()
                    pass
                elif token in [4]:
                    self.state = 121
                    self.replaceNthBlock()
                    pass
                elif token in [5]:
                    self.state = 122
                    self.replaceAllBlock()
                    pass
                elif token in [6]:
                    self.state = 123
                    self.setVarBlock()
                    pass
                elif token in [7]:
                    self.state = 124
                    self.exportVarBlock()
                    pass
                elif token in [8]:
                    self.state = 125
                    self.execPatcherBlock()
                    pass
                elif token in [9]:
                    self.state = 126
                    self.execPythonBlock()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 131
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LocationTokenContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return PatchfileParser.RULE_locationToken

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class FunctionContext(LocationTokenContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PatchfileParser.LocationTokenContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FUNCTION(self):
            return self.getToken(PatchfileParser.FUNCTION, 0)
        def TEXT_BLOCK(self):
            return self.getToken(PatchfileParser.TEXT_BLOCK, 0)
        def OPEN_BLOCK(self):
            return self.getToken(PatchfileParser.OPEN_BLOCK, 0)
        def INTEGER(self):
            return self.getToken(PatchfileParser.INTEGER, 0)
        def CLOSE_BLOCK(self):
            return self.getToken(PatchfileParser.CLOSE_BLOCK, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction" ):
                listener.enterFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction" ):
                listener.exitFunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunction" ):
                return visitor.visitFunction(self)
            else:
                return visitor.visitChildren(self)


    class EndContext(LocationTokenContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PatchfileParser.LocationTokenContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def END(self):
            return self.getToken(PatchfileParser.END, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnd" ):
                listener.enterEnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnd" ):
                listener.exitEnd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnd" ):
                return visitor.visitEnd(self)
            else:
                return visitor.visitChildren(self)


    class TextContext(LocationTokenContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PatchfileParser.LocationTokenContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BEGIN_CONTENT(self):
            return self.getToken(PatchfileParser.BEGIN_CONTENT, 0)
        def replaceBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.ReplaceBlockTextContext,0)

        def END_CONTENT(self):
            return self.getToken(PatchfileParser.END_CONTENT, 0)
        def PLUS(self):
            return self.getToken(PatchfileParser.PLUS, 0)
        def INTEGER(self):
            return self.getToken(PatchfileParser.INTEGER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterText" ):
                listener.enterText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitText" ):
                listener.exitText(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitText" ):
                return visitor.visitText(self)
            else:
                return visitor.visitChildren(self)


    class LineNumberContext(LocationTokenContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PatchfileParser.LocationTokenContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INTEGER(self):
            return self.getToken(PatchfileParser.INTEGER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLineNumber" ):
                listener.enterLineNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLineNumber" ):
                listener.exitLineNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLineNumber" ):
                return visitor.visitLineNumber(self)
            else:
                return visitor.visitChildren(self)



    def locationToken(self):

        localctx = PatchfileParser.LocationTokenContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_locationToken)
        self._la = 0 # Token type
        try:
            self.state = 152
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [13, 15]:
                localctx = PatchfileParser.FunctionContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 133
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==15:
                    self.state = 132
                    self.match(PatchfileParser.OPEN_BLOCK)


                self.state = 135
                self.match(PatchfileParser.FUNCTION)
                self.state = 136
                self.match(PatchfileParser.TEXT_BLOCK)
                self.state = 138
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==17:
                    self.state = 137
                    self.match(PatchfileParser.INTEGER)


                self.state = 141
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==16:
                    self.state = 140
                    self.match(PatchfileParser.CLOSE_BLOCK)


                pass
            elif token in [12]:
                localctx = PatchfileParser.TextContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 143
                self.match(PatchfileParser.BEGIN_CONTENT)
                self.state = 144
                self.replaceBlockText()
                self.state = 145
                self.match(PatchfileParser.END_CONTENT)
                self.state = 148
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==19:
                    self.state = 146
                    self.match(PatchfileParser.PLUS)
                    self.state = 147
                    self.match(PatchfileParser.INTEGER)


                pass
            elif token in [17]:
                localctx = PatchfileParser.LineNumberContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 150
                self.match(PatchfileParser.INTEGER)
                pass
            elif token in [14]:
                localctx = PatchfileParser.EndContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 151
                self.match(PatchfileParser.END)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class File_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TEXT_BLOCK(self):
            return self.getToken(PatchfileParser.TEXT_BLOCK, 0)

        def QUOTED_TEXT(self):
            return self.getToken(PatchfileParser.QUOTED_TEXT, 0)

        def getRuleIndex(self):
            return PatchfileParser.RULE_file_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFile_name" ):
                listener.enterFile_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFile_name" ):
                listener.exitFile_name(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFile_name" ):
                return visitor.visitFile_name(self)
            else:
                return visitor.visitChildren(self)




    def file_name(self):

        localctx = PatchfileParser.File_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_file_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 154
            _la = self._input.LA(1)
            if not(_la==22 or _la==30):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





