#-*- coding: utf-8 -*-
import re
import urllib
import xbmc
import xbmcgui
import htmlentitydefs
import unicodedata

class cUtil:
    
    def CheckOccurence(self,str1,str2):
        str1 = str1.replace('+',' ').replace('%20',' ')
        str1 = str1.lower()
        str2 = str2.lower()
        try:
            str1 = unicode(str1, 'utf-8')
        except:
            pass
        try:
            str2 = unicode(str2, 'utf-8')
        except:
            pass
        str1 = unicodedata.normalize('NFKD', str1).encode('ASCII', 'ignore')
        str2 = unicodedata.normalize('NFKD', str2).encode('ASCII', 'ignore')
        i = 0
        for part in str1.split(' '):
            if part in str2:
                i = i + 1
        return i

    def removeHtmlTags(self, sValue, sReplace = ''):
        p = re.compile(r'<.*?>')
        return p.sub(sReplace, sValue)


    def formatTime(self, iSeconds):
        iSeconds = int(iSeconds)

        iMinutes = int(iSeconds / 60)
        iSeconds = iSeconds - (iMinutes * 60)
        if (iSeconds < 10):
            iSeconds = '0' + str(iSeconds)

        if (iMinutes < 10):
            iMinutes = '0' + str(iMinutes)

        return str(iMinutes) + ':' + str(iSeconds)

    def urlDecode(self, sUrl):
        return urllib.unquote(sUrl)

    def urlEncode(self, sUrl):
        return urllib.quote(sUrl)

    def unquotePlus(self, sUrl):
        return urllib.unquote_plus(sUrl)

    def quotePlus(self, sUrl):
        return urllib.quote_plus(sUrl)
        
    def dialog(self, sName):
        oDialog = xbmcgui.DialogProgress()
        oDialog.create(sName)
        return oDialog
        
    def DecoTitle(self, string):

        #on vire ancienne deco en cas de bug
        string = re.sub('\[\/*COLOR.*?\]','',str(string))
        
        #pr les tag Crochet
        string = re.sub('([\[].+?[\]])',' [COLOR coral]\\1[/COLOR] ', string)
        #pr les tag parentheses
        string = re.sub('([\(](?![0-9]{4}).{1,7}[\)])',' [COLOR coral]\\1[/COLOR] ', string)
        #pr les series
        string = self.FormatSerie(string)
        string = re.sub('(?i)(.*) ((?:[S|E][0-9]+){1,2})','\\1 [COLOR coral]\\2[/COLOR] ', string)
            
        #vire doubles espaces
        string = re.sub(' +',' ',string)
            
        return string

    def unescape(self,text):
        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text # leave as is
        return re.sub("&#?\w+;", fixup, text)
            
            
    def CleanName(self,str):
        #vire accent et '\'
        try:
            str = unicode(str, 'utf-8')#converti en unicode pour aider aux convertions
        except:
            pass
        str = unicodedata.normalize('NFD', str).encode('ascii', 'ignore').decode("unicode_escape")
        str = str.encode("utf-8") #on repasse en utf-8
        
        #on cherche l'annee
        annee = ''
        m = re.search('(\([0-9]{4}\))', str)
        if m:
            annee = str(m.group(0))
            str = str.replace(annee,'')
       
        #vire tag
        str = re.sub('[\(\[].+?[\)\]]','', str)
        #vire caractere special
        str = re.sub("[^a-zA-Z0-9 ]", "",str)
        #tout en minuscule
        str = str.lower()
        #vire espace double
        str = re.sub(' +',' ',str)
     
        #vire espace a la fin
        if str.endswith(' '):
            str = str[:-1]
           
        #on remet l'annee
        if annee:
            str = str + ' ' + annee
           
        return str
        
    def FormatSerie(self,string):
        #convertion unicode
        string = string.decode("utf-8")
        
        SXEX = ''
        m = re.search( r'(?i)(\wpisode ([0-9]+))',string,re.UNICODE)
        if m:
            #ok y a des episodes
            string = string.replace(m.group(1),'')
            SXEX = 'E' + "%02d" % int(m.group(2))
            
            #pr les saisons
            m = re.search('(?i)(saison ([0-9]+))', string)
            if m:
                string = string.replace(m.group(1),'')
                SXEX = 'S' + "%02d" % int(m.group(2)) + SXEX
            string = string + ' ' + SXEX
        
        else:
            #pas d'episode mais y a t il des saisons ?
            m = re.search('(?i)(saison ([0-9]+))', string)
            if m:
                string = string.replace(m.group(1),'')
                SXEX = 'S' + "%02d" % int(m.group(2))
            
                string = string + ' ' + SXEX
        
        #reconvertion utf-8
        return string.encode('utf-8')
 
