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

if __name__ == '__main__':
    unittest.main()