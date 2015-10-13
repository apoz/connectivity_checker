#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import simplejson as json
import socket
import os

class ExitCodes:
    UNABLE_TO_READ_FILE = 1
    JSON_DECODING_ERROR = 2
    UNABLE_TO_BIND_LOCAL_IP_PORT = 3

def main():
    args = readCommandLineOptions()
    connectionsToCheck = getConnectionsObjFromFilename(args.fileName)
    iterateOverConnections(connectionsToCheck)

def iterateOverConnections(connectionsToCheck):
    for connectionSet in connectionsToCheck['connectionSets']:
        #printConnectionSetLocalSummary(connectionSet)
        try:
            localIP = connectionSet['localIP']
        except:
            localIP=''
        try:
            locallPort = connectionSet['localPort']
        except:
            localPort = ''
        try:
            protocol = connectionSet['protocol']
        except:
            protocol = 'TCP'  #default protocol

        for remoteIPandPort in connectionSet['remoteIPandPorts']:
            testConnectivity(localIP,localPort,protocol,remoteIPandPort['IP'],remoteIPandPort['Port'])

def testConnectivity(localIP,localPort,protocol,remoteIP,remotePort):
    if protocol == "TCP":
        testTCPConnectivity(localIP, localPort, remoteIP, remotePort)    
    return

def testTCPConnectivity(localIP, localPort, remoteIP, remotePort):
    #local IP/PORT not binded for now
    socket.setdefaulttimeout(2)
    sock = socket.socket()
    #local port and IP binding
    try:
        if localIP or localPort:
            sock.bind((localIP,localPort))
    except socket.error , msg:
        print  'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        exit(ExitCodes.UNABLE_TO_BIND_LOCAL_IP_PORT)

    try:
        result = sock.connect_ex((remoteIP, remotePort))
        sock.close()
    except:
        sock.close()
    printTCPConnectionSummaryAndResult(localIP, localPort, remoteIP, remotePort, result)
    return

def printTCPConnectionSummaryAndResult(localIP, localPort, remoteIP, remotePort, result):
    printTCPConnectionSummary(localIP, localPort, remoteIP, remotePort)
    printTCPConnectionResult(result)

def printTCPConnectionResult(result):
    print '\n' + os.strerror(result)

def printTCPConnectionSummary(localIP, localPort, remoteIP, remotePort):
    if localIP:
        print "\tLocal IP: " + localIP
    if localPort:
        print "\tLocal Port: " + str(localPort)    
    print "\tRemote IP: " + remoteIP
    print "\tRemote Port: " + str(remotePort)

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
    parser.add_argument('-o','--outputFormat', help='Format required for the output (CSV or TEXT for now)', required=True)
    return parser

def InitializeCommandLineArgumentsParser():
    parser = argparse.ArgumentParser(description='Ridiculously overengineered connectivity checker')
    return parser

if __name__ == '__main__':
    main()


