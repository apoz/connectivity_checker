#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import simplejson as json
import socket

class ExitCodes:
    UNABLE_TO_READ_FILE = 1
    JSON_DECODING_ERROR = 2

def main():
    args = readCommandLineOptions()
    connectionsToCheck = getConnectionsObjFromFilename(args.fileName)
    iterateOverConnections(connectionsToCheck)

def iterateOverConnections(connectionsToCheck):
    for connectionSet in connectionsToCheck['connectionSets']:
        #printConnectionSetLocalSummary(connectionSet)
        localIP = connectionSet['localIP']
        localPort = connectionSet['localPort']
        protocol = connectionSet['protocol']
        for remoteIPandPort in connectionSet['remoteIPandPorts']:
            testConnectivity(localIP,localPort,protocol,remoteIPandPort['IP'],remoteIPandPort['Port'])

def testConnectivity(localIP,localPort,protocol,remoteIP,remotePort):
    if protocol == "TCP":
        testTCPConnectivity(localIP, localPort, protocol, remoteIP, remotePort)    
    return

def testTCPConnectivity(localIP, localPort, protocol, remoteIP, remotePort):
    #local IP/PORT not binded for now
    socket.setdefaulttimeout(2)
    sock = socket.socket()
    try:
        result = sock.connect_ex((remoteIP, remotePort))
        sock.close()
        printTCPConnectionSummaryAndResult(localIP, localPort, remoteIP, remotePort, result)
    except:
        printTCPConnectionSummaryAndResult(localIP, localPort, remoteIP, remotePort, result)
    return

def printTCPConnectionSummaryAndResult(localIP, localPort, remoteIP, remotePort, result):
    printTCPConnectionSummary(localIP, localPort, remoteIP, remotePort)
    printTCPConnectionResult(result)

def printTCPConnectionResult(result):
    print '\nANDRES->' + str(result)

def printTCPConnectionSummary(localIP, localPort, remoteIP, remotePort):
    print "\tLocal IP: " + localIP
    print "\tLocal Port: " + str(localPort)    
    print "\tRemote IP: " + remoteIP
    print "\tLocal Port: " + str(remotePort)

def printConnectionSetLocalSummary(connectionSet):
    print "Connection set summary"
    print "======================"
    print "\tLocal IP: " + connectionSet['localIP']
    print "\tLocal Port: " + str(connectionSet['localPort'])
    print "======================"
    print connectionSet
    
def getConnectionsObjFromFilename(filename):
    connectionsString = readStringFromFile(filename)
    #print connectionsString
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


