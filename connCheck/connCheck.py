#!/usr/bin/env python
import argparse
import simplejson as json

class ExitCodes:
    UNABLE_TO_READ_FILE = 1
    JSON_DECODING_ERROR = 2

def main():
    args = readCommandLineOptions()
    connectionsToCheck = getConnectionsObjFromFilename(args.fileName)
    iterateOverConnections(connectionsToCheck)

def iterateOverConnections(connectionsToCheck):
    for connectionSet in connectionsToCheck['connectionSets']:
        printConnectionSetLocalSummary(connectionSet)
        localIP = connectionSet['localIP']
        localPort = connectionSet['localPort']
        for remoteIPandPort in connectionSet['remoteIPandPorts']:
            remoteIP=remoteIPandPort['IP']
            remotePort=remoteIPandPort['Port']
            print "Local IP" + localIP
            print " LocalPort " + str(localPort)
            print "Remote IP" + remoteIP
            print "Remote Port " + str(remotePort)

            
def printConnectionSetLocalSummary(connectionSet):
    print "Connection set summary"
    print "======================"
    print "\tLocal IP: " + connectionSet['localIP']
    print "\tLocal Port: " + str(connectionSet['localPort'])
    print "======================"
    print connectionSet
    
def getConnectionsObjFromFilename(filename):
    connectionsString = readStringFromFile(filename)
    print connectionsString
    connectionsJsonParsed = parseJsonObjFromString(connectionsString)
    return connectionsJsonParsed

def parseJsonObjFromString(connectionsString):
    try:
        connectionsJsonParsed = json.loads(connectionsString)
        return connectionsJsonParsed
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


