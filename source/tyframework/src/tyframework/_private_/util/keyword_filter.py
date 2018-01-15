# -*- coding: utf-8 -*-
'''
Created on 2014年2月12日

@author: zjgzzz@126.com
'''
import codecs
from sre_compile import isstring


class KeywordFilter(object):
    '''
    敏感词过滤器，使用方法
    1. 构造
    1.1 从文件加载(敏感词文件中每行一个词，默认utf8编码，也可以指定其它编码)
        kwf = KeywordFilter.loadFromFile('./keywords.txt', 'utf16')
    1.2 自己构造并添加敏感词
        kfw = KeywordFilter()
        kfw.addKeywords(['hello', 'keyword'])

    2. 替换关键词,
        kfw = KeywordFilter()
        kfw.addKeywords(['hello', 'keyword'])
        content = 'hello-keyword'
        kfw.replace(content) == u'*****-*******'

    3. 检测给定的内容是否存在关键词
        kfw = KeywordFilter()
        kfw.addKeywords(['hello', 'keyword'])
        content = 'hello-keyword'
        kfw.isContains(content) == True
    '''

    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.__d = dict()
        self.__keywords = set()

    def _init_singleton_(self):
        fpath = self.__ctx__.TYGlobal.path_webroot() + '/filter_keywords.txt'
        if self.__ctx__.fileutil.file_exists(fpath):
            self.loadFromFile(fpath)
            self.__ctx__.ftlog.info('load filter keywords from file=', fpath,
                                    'keyword count=', self.count())
        else:
            self.__ctx__.ftlog.error('load filter keywords from file=', fpath,
                                     'file not found !!')

    def getKeywords(self):
        return self.__keywords

    def addKeywords(self, keywords):
        for keyword in keywords:
            self.addKeyword(keyword)

    def addKeyword(self, keyword):
        '''添加一个关键词'''
        if not isstring(keyword):
            return False
        keyword = self.__ensureUnicode(keyword)
        if keyword in self.__keywords:
            return False
        self.__keywords.add(keyword)
        keyword += unichr(11)

        q = {}
        k = u''
        d = self.__d

        for uchar in keyword:
            uchar = uchar.lower()
            if d == '':
                q[k] = {}
                d = q[k]
            if not (uchar in d):
                d[uchar] = ''
                q = d
                k = uchar
            d = d[uchar]
        return True

    def isContains(self, content):
        if not isstring(content):
            return False
        for _ in self._matchIter(content):
            return True
        return False

    def replace(self, content, mask=u'*'):
        '''
        替换content中的所有敏感词为mask*len(关键词)
        '''
        if not isstring(content):
            return content
        content = self.__ensureUnicode(content)
        mask = self.__ensureUnicode(mask)
        result = self._match(content)
        if not result:
            return content
        startIndex = 0
        subList = []
        for matched in result:
            if startIndex < matched[0]:
                subList.append(content[startIndex:matched[0]])
            subList.append(mask * matched[1])
            startIndex = matched[0] + matched[1]
        if startIndex < len(content):
            subList.append(content[startIndex:])
        return ''.join(subList)

    def count(self):
        '''返回关键字个数'''
        return len(self.__keywords)

    def loadFromFile(self, path, encoding='utf16'):
        '''从文件中加载关键词库'''
        f = None
        self.__d = dict()
        self.__keywords = set()
        try:
            f = codecs.open(path, 'r', encoding)
            keyword = f.readline()
            while keyword:
                keyword = keyword.strip()
                self.addKeyword(keyword)
                keyword = f.readline()
        finally:
            if f:
                f.close()
        return self

    def _match(self, content):
        result = []
        for match in self._matchIter(content):
            result.append(match)
        return result

    def _matchIter(self, content):
        i = 0
        j = 0
        d = self.__d
        content = self.__ensureUnicode(content)
        ln = len(content)

        while i + j < ln:
            t = content[i + j].lower()
            if not (t in d):
                j = 0
                i += 1
                d = self.__d
                continue
            d = d[t]
            j += 1

            if chr(11) in d:
                d = self.__d
                yield (i, j, content[i:i + j])
                i = i + j
                j = 0

    def __ensureUnicode(self, content):
        if not isinstance(content, unicode):
            return content.decode()
        return content


KeywordFilter = KeywordFilter()
