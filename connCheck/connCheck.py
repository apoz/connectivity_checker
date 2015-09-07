#!/usr/bin/env python
import argparse
import simplejson as json

class ExitCodes:
    UNABLE_TO_READ_FILE = 1
    JSON_DECODING_ERROR = 2

def main():
    args = readCommandLineOptions()
    connectionsToCheck = getConnectionsObjFromFilename(args.fileName)

def getConnectionsObjFromFilename(filename):
    connectionsString = readStringFromFile(filename)
    connectionsJsonParsed = parseJsonObjFromString(connectionsString)
    return connectionsJsonParsed

def parseJsonObjFromString(connectionString):
    try:
        connectionsJsonParsed = json.loads(connectionString)
    except ValueError:
        print "Decoding JSON data has failed"
        exit(ExitCodes.JSON_DECODING_ERROR)
    
def readStringFromFile(fileName):
    try:
        with open(fileName, 'r') as file:
            readData = file.read()
            return readData
    except IOError:
        print "Unable to read " + fileName
        exit (ExitCodes.UNABLE_TO_READ_FILE)
    return
    
def readCommandLineOptions():
    parser = InitializeCommandLineArgumentsParser()
    parser = addCommandLineArguments(parser)
    args = parser.parse_args()
    return args

def addCommandLineArguments(parser):
    parser.add_argument("fileName", help="Input the filename where the IPs to check are listed (json format)")
    return parser

def InitializeCommandLineArgumentsParser():
    parser = argparse.ArgumentParser(description='Demo')
    return parser

if __name__ == '__main__':
    main()


