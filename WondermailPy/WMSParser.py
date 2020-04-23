# 	The WMSParser object

# 	This file is placed in the public domain and may be freely used, reproduced, modified, sold or whatever you want.
# 	However, it may or may not work; use at your own risk.


# /* types of data we handle:
# - scrambled wondermail (as given by game)
# - unscrambled wondermail
# - encrypted bitstring (final result data)
# - decrypted bitstring (parseable data)
# - raw bitstream (no leading bits, no checksum)
# - wmstruct data parse
# */
import WMSConstants
from WMSConstants import WMS_STRING_LEN
from WMSConstants import WMSStruct


class WMSParser:
    # Byte-swap patterns
    # 07 1B 0D 1F 15 1A 06 01 17 1C 09 1E 0A 20 10 21 0F 08 1D 11 14 00 13 16 05 12 0E 04 03 18 02 0B 0C 19
    # http:#www.gamefaqs.com/boards/detail.php?board=955859&topic=51920426&message=571612360
    byteSwap = [0x07, 0x1B, 0x0D, 0x1F, 0x15, 0x1A, 0x06,
                0x01, 0x17, 0x1C, 0x09, 0x1E, 0x0A, 0x20,
                0x10, 0x21, 0x0F, 0x08, 0x1D, 0x11, 0x14,
                0x00, 0x13, 0x16, 0x05, 0x12, 0x0E, 0x04,
                0x03, 0x18, 0x02, 0x0B, 0x0C, 0x19]
    byteSwapEU = [0x0E, 0x04, 0x03, 0x18, 0x09, 0x1E, 0x0A,
                  0x20, 0x10, 0x21, 0x14, 0x00, 0x13, 0x16,
                  0x05, 0x12, 0x06, 0x01, 0x17, 0x1C, 0x07,
                  0x1B, 0x0D, 0x1F, 0x15, 0x1A, 0x02, 0x0B,
                  0x0C, 0x19, 0x0F, 0x08, 0x1D, 0x11]
    # Each WM byte maps to these bit values
    # http://www.gamefaqs.com/boards/genmessage.php?board=938931&topic=42726909&page=9
    # http://www.gamefaqs.com/boards/genmessage.php?board=938931&topic=42949038
    bitValues = "&67NPR89F0+#STXY45MCHJ-K12=%3Q@W"
    # Encryption data from:
    # http://docs.google.com/Doc?id=ddpvsk95_17fr7qpmgc
    encryptionData = [
        # # Listed vertical: first part of the 2-character hex code range
        # # Listed horizontal: second part of the 2-character hex code
        # # 0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F
        0x2E, 0x75, 0x3F, 0x99, 0x09, 0x6C, 0xBC, 0x61, 0x7C, 0x2A, 0x96, 0x4A, 0xF4, 0x6D, 0x29, 0xFA,  # 00-0F
        0x90, 0x14, 0x9D, 0x33, 0x6F, 0xCB, 0x49, 0x3C, 0x48, 0x80, 0x7B, 0x46, 0x67, 0x01, 0x17, 0x59,  # 10-1F
        0xB8, 0xFA, 0x70, 0xC0, 0x44, 0x78, 0x48, 0xFB, 0x26, 0x80, 0x81, 0xFC, 0xFD, 0x61, 0x70, 0xC7,  # 20-2F
        0xFE, 0xA8, 0x70, 0x28, 0x6C, 0x9C, 0x07, 0xA4, 0xCB, 0x3F, 0x70, 0xA3, 0x8C, 0xD6, 0xFF, 0xB0,  # 30-3F
        0x7A, 0x3A, 0x35, 0x54, 0xE9, 0x9A, 0x3B, 0x61, 0x16, 0x41, 0xE9, 0xA3, 0x90, 0xA3, 0xE9, 0xEE,  # 40-4F
        0x0E, 0xFA, 0xDC, 0x9B, 0xD6, 0xFB, 0x24, 0xB5, 0x41, 0x9A, 0x20, 0xBA, 0xB3, 0x51, 0x7A, 0x36,  # 50-5F
        0x3E, 0x60, 0x0E, 0x3D, 0x02, 0xB0, 0x34, 0x57, 0x69, 0x81, 0xEB, 0x67, 0xF3, 0xEB, 0x8C, 0x47,  # 60-6F
        0x93, 0xCE, 0x2A, 0xAF, 0x35, 0xF4, 0x74, 0x87, 0x50, 0x2C, 0x39, 0x68, 0xBB, 0x47, 0x1A, 0x02,  # 70-7F
        0xA3, 0x93, 0x64, 0x2E, 0x8C, 0xAD, 0xB1, 0xC4, 0x61, 0x04, 0x5F, 0xBD, 0x59, 0x21, 0x1C, 0xE7,  # 80-8F
        0x0E, 0x29, 0x26, 0x97, 0x70, 0xA9, 0xCD, 0x18, 0xA3, 0x7B, 0x74, 0x70, 0x96, 0xDE, 0xA6, 0x72,  # 90-9F
        0xDD, 0x13, 0x93, 0xAA, 0x90, 0x6C, 0xA7, 0xB5, 0x76, 0x2F, 0xA8, 0x7A, 0xC8, 0x81, 0x06, 0xBB,  # A0-AF
        0x85, 0x75, 0x11, 0x0C, 0xD2, 0xD1, 0xC9, 0xF8, 0x81, 0x70, 0xEE, 0xC8, 0x71, 0x53, 0x3D, 0xAF,  # B0-BF
        0x76, 0xCB, 0x0D, 0xC1, 0x56, 0x28, 0xE8, 0x3C, 0x61, 0x64, 0x4B, 0xB8, 0xEF, 0x3B, 0x41, 0x09,  # C0-CF
        0x72, 0x07, 0x50, 0xAD, 0xF3, 0x2E, 0x5C, 0x43, 0xFF, 0xC3, 0xB3, 0x32, 0x7A, 0x3E, 0x9C, 0xA3,  # D0-DF
        0xC2, 0xAB, 0x10, 0x60, 0x99, 0xFB, 0x08, 0x8A, 0x90, 0x57, 0x8A, 0x7F, 0x61, 0x90, 0x21, 0x88,  # E0-EF
        0x55, 0xE8, 0xFC, 0x4B, 0x0D, 0x4A, 0x7A, 0x48, 0xC9, 0xB0, 0xC7, 0xA6, 0xD0, 0x04, 0x7E, 0x05   # F0-FF
    ]
    # Data used when calculating a checksum in Sky. Calculated below.
    skyChecksumData = []

    def Sanitize(self, wmString: str):
        # If dontSanitize is there and is checked, return our input.
        # NOTE: currently getOption always returns false
        # if(getOption("dontSanitize")) return wmString
        wmString = wmString.upper()
        sanitizedWMString = ""
        for letter in wmString:
            if letter in WMSParser.bitValues:
                sanitizedWMString += letter
        if len(sanitizedWMString) is not WMS_STRING_LEN:
            raise RuntimeError(
                f"Sanitized Wonder Mail string length is not equal to required length: {WMS_STRING_LEN}\nRecieved length: {len(sanitizedWMString)}")
        return sanitizedWMString

    # Unscrambles a scrambled WMS string.
    # @param string Scrambled WMS string
    # @returns string Unscrambled WMS string
    def UnscrambleString(self, wmString: str, swapArray=WMSParser.byteSwap):
        outString = ""
        for index in swapArray:
            outString += wmString[index]
        return outString

    # Scrambles a unscrambled WMS string.
    # @param string Unscrambled WMS string
    # @param array Swap Array (optional)
    # @returns string Scrambled WMS string
    def ScrambleString(self, wmString, swapArray=WMSParser.byteSwap):
        outArray = []
        for index, value in zip(swapArray, wmString):
            outArray.insert(index, value)
        return "".join(outArray)

    # Returns the encryption entries for a given checksum.
    # NOTE: python datatype sizes might affect the result of this
    # @param number Checksum to get bytes for
    # @return array Array with encryption entries
    def GetEncryptionEntries(self, checksum: int):
        entries = []
        encPointer = checksum
        backwards = ~(checksum & 0x01)
        for _ in range(17):
            entries.append(WMSParser.encryptionData[encPointer])
            if backwards:
                encPointer = (encPointer - 1) % len(WMSParser.encryptionData)
            else:
                encPointer = (encPointer + 1) % len(WMSParser.encryptionData)
        return entries

    # NOTE: python adds 0b automagically...take into account
    # @param number Number
    # @returns string Bits
    @staticmethod
    def NumToBits(num, outputSize):
        bits = str(bin(num))
        return "0" + bits[2:outputSize]

    # Converts the unscrambled representation of a mail string to an encrypted bitstream.
    # In Sky, this is reversed.
    # @param string Unscrambled mail string
    # @returns string Encrypted bitStream
    def BytesToBits(self, wmIntString):
        outString = ""
        for letter in wmIntString:
            if letter in WMSParser.bitValues:
                index = WMSParser.bitValues.index(letter)
                outString += WMSParser.NumToBits(index, 5)
            else:
                raise RuntimeError(
                    f"BytesToBits: Unknown character: {letter} in string {wmIntString}")
        return outString

    # Converts an encrypted bitStream to an unscrambled mail.
    # @param string Encrypted bitStream
    # @returns string Unscrambled mail
    def BitsToBytes(self, bitStream):
        blockCount = len(bitStream)  # 34
        outString = ""
        for i in range(blockCount):
            bitStreamIdx = (blockCount - i - 1) * 5
            currentCharacters = bitStream[bitStreamIdx:bitStreamIdx + 5]
            bitValsIdx = int(currentCharacters, 2)
            if bitValsIdx not in range(0, 32):
                raise RuntimeError(
                    f"BitsToBytes: Could not find {currentCharacters} in the reversed table")
            else:
                outString += WMSParser.bitValues[bitValsIdx]
        return outString

    # Returns the resetByte for a given checksum.
    # @param Number checksum
    # @return Number Reset byte or -1
    def GetResetByte(self, checksum):
        checksumByte = checksum % 256
        resetByte = (checksumByte // 16) + 8 + (checksumByte % 16)
        return resetByte if resetByte < 17 else -1

    # Decrypts or encrypts a bitstream according to the encryption data.
    # @param String current bitstream
    # @param boolean if given and true, encrypt; else decrypt
    # @return String decrypted or encrypted bitstream
    def DecryptBitStream(self, bitStream, encrypt=False):
        bitPtr = 0

        # This will contain the 8-bit blocks as numbers (0-255), each representing one byte.
        # The checksum byte is NOT included in these blocks.
        # The first block in the array is the last block in the bitstream (we work backwards).
        blocks = []
        origBlocks = []

        # Checksum data
        checksumByte = 0
        checksumBits = ""
        skyChecksumBits = ""
        fullChecksum = ""

        # Go 8 bits back from the end. We'll read the next 8 bits as our checksum.
        bitPtr = len(bitStream) - 8
        checksumBits = bitStream[bitPtr:bitPtr + 8]
        checksumByte = int(checksumBits, base=2)

        # The Sky Checksum is 24 bits.
        bitPtr -= 24
        skyChecksumBits = bitStream[bitPtr: bitPtr + 24]
        # This is supposed to concat the checksum to skychecksum
        # Likely broken
        fullChecksum = int(skyChecksumBits + checksumBits, base=2)

        # http://www.gamefaqs.com/boards/genmessage.php?board=938931&topic=42949038&page=6
        # "At the moment, I figured out what the game is doing with the other half of the encryption.
        # Apparently, if you have an even checksum, you go backwards through the encryption bytes.
        # With an odd checksum, you go forwards through the encryption bytes."
        backwards = not (checksumByte & 0x01)
        print(f'CHECKSUM: {checksumByte}, encPtr goes backwards: {backwards}')

        # Parse everything into blocks.
        # Sky: 1 2-bit block + 16 8-bit blocks + 24-bit skyChecksum + 8-bit checksum.
        while(bitPtr > 7):
            bitPtr -= 8
            data = int(bitStream[bitPtr: bitPtr + 8], base=2)
            blocks[len(blocks)] = data
            origBlocks[len(origBlocks)] = data

        # Handle the 2-bit block at the beginning (should always be 00?)
        twoBitsStart = bitStream[:2]
        bitPtr -= 2

        # Get our encryption entries.
        entries = self.GetEncryptionEntries(checksumByte)

        # Figure out the resetByte.
        resetByte = 255
        resetByte = self.GetResetByte(fullChecksum)
        print(f'resetByte used for this code: {resetByte}')

        # Do the decryption.
        tblPtr = 0
        encPtr = 0
        for i in range(len(blocks)):
            if encPtr is resetByte:
                remaining = len(blocks) - i
                print(
                    f'Resetting at {encPtr}. {remaining} blocks remain for decryption.')
                encPtr = 0
            inputByte = blocks[tblPtr]
            result
            if encrypt:
                result = (inputByte + entries[encPtr]) & 0xFF
            else:
                result = (inputByte - entries[encPtr]) & 0xFF
            print(
                f'pos {tblPtr}, value {inputByte} {hex(inputByte)}, encbyte {entries[encPtr]}, result is {result}')
            # Update the data in the block.
            blocks[i] = result
            # Update blockPtr.
            tblPtr += 1
            encPtr += 1

        # String everything together. If we use twoBitsStart, that will be our base point.
        outString = twoBitsStart

        # We start at the end and work backwards; the last encryption block is the first 8 bits in the bitstream.
        # That's just how it works.
        for block in blocks.reverse():
            outString += WMSParser.NumToBits(block, 8)

        # Re-add the checksums to the data.
        outString += skyChecksumBits + checksumBits
        return outString

    # Encrypts a bitstream according to the encryption data by calling
    # <code>decryptBitStream(stream, true)</code>
    # @param String decrypted bitstream
    # @return String encrypted bitstream
    def EncryptBitStream(self, currentBitStream):
        return self.DecryptBitStream(currentBitStream, True)

    # Converts a bit string to our internal structure.
    # @param string Unencrypted bitStream
    # @returns object WMSStruct data
    def BitsToStructure(self, bitString):
        # Where to start reading in the bitString
        bitPtr = 0
        # Our eventual output structure
        outputStruct = {}

        # Contains the bit streams rather than integers - for debug use
        outputStructBit = {}

        # structInfo contains the name, the size and a note which we'll add at some point somehow.
        for structure in WMSStruct:
            # Read "size" bits from the bitString and increment the bitPtr by the same amount
            bitData = bitString[bitPtr: bitPtr + structure["size"]]
            bitPtr += structure["size"]
            # Convert our bit data to a number
            numData = int(bitData, base=2)
            # Add it to the outputStruct
            outputStruct[structure["name"]] = numData
            outputStructBit[structure["name"]] = bitData

        # We should be at the end now
        if bitPtr is not len(bitString):
            print(
                f'WARNING: Not all available data was parsed into struct. Final bitPtr is {bitPtr}, length is {len(bitString)}')

        print(f'outStruct: {outputStruct}, bitStruct: {outputStructBit}')
        return outputStruct

    # Calculates the checksum for a given bitStream.
    # @param String bitStream in 136-bit raw format or 170-bit full format
    # @return Number Checksum as decimal number
    def CalculateChecksum(self, bitStream):
        # Calculate the checksum - Sky. This is simple CRC32.
        # http://www.gamefaqs.com/boards/detail.php?board=955859&topic=51920426&message=582176885
        print(
            f'Sky Checksum calculation - bitStream of length {len(bitStream)}')
        if len(bitStream) is 170:
            print(f'Truncating the 170-long bitStream for you. By golly, I\'m so nice.')
            bitStream = bitStream[2:138]
        if len(bitStream) is not 136:
            print(f'WARNING: bitStream should be 136 bits long!')

        # Start with 0xFFFFFFFF.
        checksum = 0xFFFFFFFF

        # We have 17 blocks of 8 bits in the bitStream (136 bits).
        data = ""
        for i in range(16).__reversed__():
            # Grab 8 bits from the stream and convert it to a number.
            bits = bitStream[i*8:(i*8)+8]
            num = int(bits, base=2)
            data += chr(num)
            # Grab a entry from the data table. The entry gotten is equal to
            entry = self.skyChecksumData[(checksum ^ num) & 0xFF]
            # The entry is NOT'ed with our current checksum rsl'd 8 times. The result of this will be the new checksum
            # for this round.
            checksum = (checksum >> 8) ^ entry

        # Our final checksum is NOT'ed with 0xFFFFFFFF.
        checksum = checksum ^ 0xFFFFFFFF
        # Make the checksum positive (WHY MUST YOU DO THIS TO ME JAVASCRIPT!?!?!?)
        if checksum < 0:
            # Might not be necessary in python
            checksum += 4294967296
        print(f'Generated a Sky checksum of {checksum} ({hex(checksum)}).')
        return checksum


# var WMSParser = {

# 	// Converts an object to an unencrypted bitstream.
# 	// @param object Object containing a key for each key in WMSStruct.
# 	// @returns string Unencrypted bitStream
# 	"structureToBits": function(inputStruct) {
# 		var bitStream = "";
# 		var totalSize = 0;
# 		for(var i = 0; i < WMSStruct.length; ++i) {
# 			var key = WMSStruct[i];
# 			if(key.noinclude) {
# 				continue;
# 			}

# 			if(typeof inputStruct[key.name] == "undefined") {
# 				console.error("The key %s was not defined in inputStruct %o.", key.name, inputStruct);
# 			}

# 			var data = inputStruct[key.name];
# 			var binData = numToBits(data, key.size);
# 			bitStream += binData;
# 			totalSize += key.size;
# 		}

# 		// For Sky, our "null" byte is 8 bits in length. However, 2 of those bits aren't encrypted. To make it easier on ourselves,
# 		// we chop those two off here and re-add them later. These will always be zero so it's ok.
# 		bitStream = bitStream.substr(2);

# 		console.info("Generated a %d-length bitStream: %s.", bitStream.length, bitStream);

# 		var checksum = this.calculateChecksum(bitStream);

# 		// Add the two chopped-off zero bits and the checksum.
# 		bitStream = "00" + bitStream + numToBits(checksum, 32);

# 		return bitStream;
# 	}
# };

# /**
#  * This code generates a CRC32 table.
#  * http://www.gamefaqs.com/boards/detail.php?board=955859&topic=51920426&message=582176885
#  */
# (function() {
# 	for(var i = 0; i < 256; i++) {
# 		var entry = i;

# 		for(var j = 0; j < 8; j++) {
# 			if(!(entry & 1)) {
# 				entry = entry >>> 1;
# 			}
# 			else {
# 				entry = 0xEDB88320 ^ (entry >>> 1);
# 			}

# 			WMSParser.skyChecksumData[i] = entry;
# 		}
# 	}
# })();

# /**
#  * Convert a set of bits to a number.
#  * @param String Bits
#  * @returns Number Number
#  */
# function bitsToNum(bits) {
# 	return parseInt(bits, 2);
# }

# /**
#  * Converts a number to a hex string.
#  * @param Number Number to convert
#  * @param Number Minimum size of the hex string
#  * @returns String Hex string
#  */
# function numToHex(num, minSize) {
# 	var hex = num.toString(16).toUpperCase();
# 	while(hex.length < minSize) {
# 		hex = "0" + hex;
# 	}
# 	return hex;
# }
