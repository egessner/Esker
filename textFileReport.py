# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 11:15:55 2021

@author: Erik Gessner

Program that takes a txt file as a command line argument and generates a report based on the contents of that txt file
"""
'''
Assumptions:
    	Figures means single digit numbers (i.e. 99 is two figures, 9 and 9)
        Program can take command line arguments
        Program is run from the command line
        File output is the expected output
        Words are any sequence of characters including figures and other special characters
        Whitespaces do not count as characters

'''
import sys #to read off of the command line
import os # since we don't know if this is windows, mac, or linux
import re #for regex use

textReadable = []

'''
Given a filepath, open that file, and set textReadable to its contents the close the file
Takes: fileName, the filePath to the to be opened txt file
Returns: None
'''
def open_file(fileName):
    global textReadable
    textFile = open(fileName, 'r')
    textReadable = textFile.readlines()
    #once contents are read to testReadable we no longer need the file open
    textFile.close()

'''
generateReport() reads textReadable and derives the following information:
    number of lines
    number of letters
    number of figures
    number of other characters
    number of total characters
    number of words
    nummmber of words of increasing length
    the density of each character (how often it occurs)
Takes: none
Returns: a list of all of the above attributes (the report)
'''
def generateReport():
    lineCount = 0
    letterCount = 0
    figureCount = 0
    otherCharCount = 0
    wordCount = 0
    lenWordCount = {} # key = length of word, value = number of words of that length
    charDensity = {} # key = character, value = how often it occurs (density)
    
    for line in textReadable:
        lineCount +=1
        
        # letter count
        letterRegex = re.compile('[a-zA-Z]')
        letterCount += len(letterRegex.findall(line))      
        
        #figure count
        figRegex = re.compile('\d')
        figureCount += len(figRegex.findall(line))
       
        #other Character count
        otherCharRegex = re.compile('[^a-zA-Z\d\s]')
        otherCharCount += len(otherCharRegex.findall(line))
        
        # word count
        line = line.split()
        wordCount += len(line)
        
        #dictionary time!
        for word in line:
            wordLen = len(word)
            if wordLen in lenWordCount:
                lenWordCount[wordLen] += 1
            else:
                lenWordCount[wordLen] = 1
            
            letters = list(word)
             # character density
            for char in letters:
                char = char.lower()
                if char in charDensity:
                    charDensity[char] += 1
                else:
                    charDensity[char] = 1
    
    # total character count
    charCount = letterCount + figureCount + otherCharCount
    
    # sort lenWordCount and charDensity
    tempDict = {}
    for length in sorted(lenWordCount):
        tempDict[length] = lenWordCount[length]
    lenWordCount = tempDict
    
    charDensity = dict(sorted(charDensity.items(), key = lambda item: item[1], reverse = True))
    
    
    #return the descovered information in a report in the following order
    return [lineCount, charCount, letterCount, figureCount, otherCharCount, wordCount, lenWordCount, charDensity]

'''
writeReport(fileName, report) takes the report created from generateReport() and writes the information to a new file named after the old file + Report.txt
Takes: 
    fileName, the filepath to the origional txt file the report is written from 
    report, the report created from the origional txt file from fileName
Returns: None
'''
def writeReport(fileName, report):
    #get the name from the origional txt file
    name = os.path.basename(fileName).split('.')[0]
    with open(name+' Report.txt', 'w') as genReport:
        #file name
        text_report = 'Text Report on: ' + fileName + '\n'
        genReport.write(text_report)
       
        #number of lines
        number_of_lines = 'Number of lines: ' + str(report[0]) + '\n'
        genReport.write(number_of_lines)
        
        #number of characters
        number_of_characters = 'Numer of characters (total): ' + str(report[1]) + '\n'
        genReport.write(number_of_characters)
        
        #number of letters
        number_of_letters = 'Number of letters: ' + str(report[2]) + '\n'
        genReport.write(number_of_letters)
        
        #number of figures
        number_of_figures = 'Number of figures: ' + str(report[3]) + '\n'
        genReport.write(number_of_figures)
        
        #number of other characters
        number_other_characters = 'Number of other characters: ' + str(report[4]) + '\n'
        genReport.write(number_other_characters)
       
        #number of words
        number_of_words = 'Number of words: ' + str(report[5]) + '\n'
        genReport.write(number_of_words)
        
        #space out next section
        genReport.write('\n')
        
        #number of words of length
        lenWordCount = report[6]
        for length in lenWordCount:
            current_len_word_count = 'Number of ' + str(length) + ' letter words: ' + str(lenWordCount[length]) + '\n'
            genReport.write(current_len_word_count)
        
        #space out next section
        genReport.write('\n')
        
        #top 5 most common chars
        charDensity = report[7]
        densityList = list(charDensity)
        #5
        fifth_densist = 'The fifth most dense character is: ' + str(densityList[4]) + ' with ' + str(charDensity[densityList[4]]) + ' appearances' + '\n'
        genReport.write(fifth_densist)
        #4
        fourth_densist = 'The fourth most dense character is: ' + str(densityList[3]) + ' with ' + str(charDensity[densityList[3]]) + ' appearances' + '\n'
        genReport.write(fourth_densist)
        #3
        third_densist = 'The third most dense character is: ' + str(densityList[2]) + ' with ' + str(charDensity[densityList[2]]) + ' appearances' + '\n'
        genReport.write(third_densist)
        #2
        second_densist = 'The second most dense character is: ' + str(densityList[1]) + ' with ' + str(charDensity[densityList[1]]) + ' appearances' + '\n'
        genReport.write(second_densist)
        #1
        first_densist = 'The most dense character is: ' + str(densityList[0]) + ' with ' + str(charDensity[densityList[0]]) + ' appearances' + '\n'
        genReport.write(first_densist)
  
'''
main() calls the other functions to help read, create, and generate a report. Little error handling to help the user get the desired output
Takes: None
Returns: None
'''
def main():
    try:
        # not enough or too many arguments on the command line
        if len(sys.argv) != 2:
            print('Not enough or too many arguments in input, expected:')
            print('\t "py <filepath to textFileReport.py> <filepath of txt file>"')
            exit()
        # get the  filepath of the txt file to create the report on from the command line
        fileName = sys.argv[1];
        # open the file
        open_file(fileName)
        # generate the report
        report = generateReport()
        # write the report
        writeReport(fileName, report)
    except Exception as e:
        print(e)
        pass

if __name__ == "__main__":
   main()