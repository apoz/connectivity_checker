#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import connCheck.connCheck as connCheck

class TestFileParsing(unittest.TestCase):

  def test_openNonExistingFile(self):
    with self.assertRaises(SystemExit) as cm:
        connCheck.getConnectionsObjFromFilename("nonExistingFilename")
    self.assertEqual(cm.exception.code, connCheck.ExitCodes.UNABLE_TO_READ_FILE)

  def test_parseJsonObjFromString(self):
    with self.assertRaises(SystemExit) as cm:
        connCheck.parseJsonObjFromString("test_String")
    self.assertEqual(cm.exception.code, connCheck.ExitCodes.JSON_DECODING_ERROR)

  def test_getConnectionsObjFromFilename(self):
    connectionsObj=connCheck.getConnectionsObjFromFilename('tests/test_IPsToCheck.json')
    self.assertEqual(connectionsObj['connectionSets'][0]['localIP'],'1.1.1.1')
    self.assertEqual(connectionsObj['connectionSets'][0]['localPort'],111)
    self.assertEqual(connectionsObj['connectionSets'][0]['protocol'],'TCP')
    self.assertEqual(connectionsObj['connectionSets'][0]['remoteIPandPorts'][0]['IP'],'2.2.2.2')
    self.assertEqual(connectionsObj['connectionSets'][0]['remoteIPandPorts'][0]['Port'],2222)
    self.assertEqual(connectionsObj['connectionSets'][0]['remoteIPandPorts'][1]['IP'],'3.3.3.3')
    self.assertEqual(connectionsObj['connectionSets'][0]['remoteIPandPorts'][1]['Port'],3333)

  def test_unableToBindLocalIP(self):
    with self.assertRaises(SystemExit) as cm:
        connCheck.testTCPConnectivity('1.1.1.1', 111, 'TCP', '2.2.2.2', 222)
    self.assertEqual(cm.exception.code, connCheck.ExitCodes.UNABLE_TO_BIND_LOCAL_IP_PORT)

if __name__ == '__main__':
    unittest.main()