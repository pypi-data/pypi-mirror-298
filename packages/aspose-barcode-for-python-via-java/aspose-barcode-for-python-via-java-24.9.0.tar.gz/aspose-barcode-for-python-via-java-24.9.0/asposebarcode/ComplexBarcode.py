import time
from datetime import datetime

import jpype
import base64
import io
from PIL import Image
from enum import Enum
from . import Generation, ComplexBarcode, Assist

class IComplexCodetext(Assist.BaseJavaClass):
      """!
      Interface for complex codetext used with ComplexBarcodeGenerator.
      """
      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def getConstructedCodetext(self):
            """!
            Construct codetext for complex barcode
            @return Constructed codetext
            """
            raise Assist.BarCodeException('You have to implement the method getConstructedCodetext!')

      def initFromString(self, constructedCodetext):
            """!
            Initializes instance with constructed codetext.
            @param constructedCodetext Constructed codetext.
            """
            raise Assist.BarCodeException('You have to implement the method initFromString!')

      def getBarcodeType(self):
            """!
            Gets barcode type.
            @return Barcode type.
            """
            raise Assist.BarCodeException('You have to implement the method getBarcodeType!')

class ComplexBarcodeGenerator(Assist.BaseJavaClass):
      """!
      ComplexBarcodeGenerator for backend complex barcode (e.g. SwissQR) images generation.
      This sample shows how to create and save a SwissQR image.
      \code
        swissQRCodetext = ComplexBarcode.SwissQRCodetext(None)
        swissQRCodetext.getBill().setAccount("CH450023023099999999A")
        swissQRCodetext.getBill().setBillInformation("BillInformation")
        swissQRCodetext.getBill().setAmount(1024)
        swissQRCodetext.getBill().getCreditor().setName("Creditor.Name")
        swissQRCodetext.getBill().getCreditor().setAddressLine1("Creditor.AddressLine1")
        swissQRCodetext.getBill().getCreditor().setAddressLine2("Creditor.AddressLine2")
        swissQRCodetext.getBill().getCreditor().setCountryCode("Nl")
        swissQRCodetext.getBill().setUnstructuredMessage("UnstructuredMessage")
        swissQRCodetext.getBill().setReference("Reference")
        swissQRCodetext.getBill().setAlternativeSchemes([ComplexBarcode.AlternativeScheme("AlternativeSchemeInstruction1"), ComplexBarcode.AlternativeScheme("AlternativeSchemeInstruction2")])
        swissQRCodetext.getBill().setDebtor(ComplexBarcode.Address())
        swissQRCodetext.getBill().getDebtor().setName("Debtor.Name")
        swissQRCodetext.getBill().getDebtor().setAddressLine1("Debtor.AddressLine1")
        swissQRCodetext.getBill().getDebtor().setAddressLine2("Debtor.AddressLine2")
        swissQRCodetext.getBill().getDebtor().setCountryCode("LU")
        cg = ComplexBarcode.ComplexBarcodeGenerator(swissQRCodetext)
        res = cg.generateBarCodeImage()
       \endcode
      """
      javaClassName = "com.aspose.mw.barcode.complexbarcode.MwComplexBarcodeGenerator"

      def init(self):
            self.parameters = Generation.BaseGenerationParameters(self.getJavaClass().getParameters())

      def getParameters(self):
            """!
            Generation parameters.
            """
            return self.parameters

      def __init__(self, complexCodetext):
            """!
            Creates an instance of ComplexBarcodeGenerator.
            @param complexCodetext Complex codetext
            """
            try:
                  self.parameters = None
                  javaComplexBarcodeGenerator = jpype.JClass(ComplexBarcodeGenerator.javaClassName)
                  super().__init__(javaComplexBarcodeGenerator(complexCodetext.getJavaClass()))
            except Exception as e:
                  raise Assist.BarCodeException(e)
            self.init()

      def generateBarCodeImage(self):
            """!
            Generates complex barcode image under current settings.
            @param value of BarCodeImageFormat (PNG, BMP, JPEG, GIF, TIFF)
            default value is BarCodeImageFormat.PNG
            @return  Pillow Image object of barcode image
            """
            bytes = base64.b64decode(str(self.javaClass.generateBarCodeImage(Generation.BarCodeImageFormat.PNG.value)))
            buf = io.BytesIO(bytes)
            return Image.open(buf)

      def save(self, imagePath, imageFormat):
            """!
            Save barcode image to specific file in specific format.
            @param imagePath Path to save to.
            @param imageFormat of BarCodeImageFormat enum (PNG, BMP, JPEG, GIF, TIFF)
            \code
            generator = Generation.BarcodeGenerator(Generation.EncodeTypes.CODE_128, "12345678")
            generator.save(path_to_save, Generation.BarCodeImageFormat.PNG)
            \endcode
            """
            self.generateBarCodeImage().save(imagePath, str(imageFormat))


class Address(Assist.BaseJavaClass):
      """!
      Address of creditor or debtor.
      You can either set street, house number, postal code and town (type structured address)
      or address line 1 and 2 (type combined address elements). The type is automatically set
      once any of these fields is set. Before setting the fields, the address type is undetermined.
      If fields of both types are set, the address type becomes conflicting.
      Name and country code must always be set unless all fields are empty.
      """
      javaClassName = "com.aspose.mw.barcode.complexbarcode.MwAddress"

      def __init__(self):
            jclass = jpype.JClass(Address.javaClassName)
            super().__init__(jclass())
            self.init()

      @staticmethod
      def construct(javaClass):
            address = Address()
            address.setJavaClass(javaClass)
            address.init()
            return address

      def getType(self):
            """!
            Gets the address type.
            The address type is automatically set by either setting street / house number
            or address line 1 and 2. Before setting the fields, the address type is Undetermined.
            If fields of both types are set, the address type becomes Conflicting.
            @return: The address type.
            """
            return self.getJavaClass().getType()

      def getName(self):
            """!
            Gets the name, either the first and last name of a natural person or the
            company name of a legal person.
            @return:The name.
            """
            return self.getJavaClass().getName()

      def setName(self, value):
            """!
            Sets the name, either the first and last name of a natural person or the
            company name of a legal person.
            @:param:The name.
            """
            self.getJavaClass().setName(value)

      def getAddressLine1(self):
            """!
            Gets the address line 1.
            Address line 1 contains street name, house number or P.O. box.
            Setting this field sets the address type to AddressType.CombinedElements unless it's already
            AddressType.Structured, in which case it becomes AddressType.Conflicting.
            This field is only used for combined elements addresses and is optional.
            @return:The address line 1.
            """
            return self.getJavaClass().getAddressLine1()

      def setAddressLine1(self, value):
            """!
            Sets the address line 1.
            Address line 1 contains street name, house number or P.O. box.
            Setting this field sets the address type to AddressType.CombinedElements unless it's already
            AddressType.Structured, in which case it becomes AddressType.Conflicting.
            This field is only used for combined elements addresses and is optional.
            @:param:The address line 1.
            """
            self.getJavaClass().setAddressLine1(value)

      def getAddressLine2(self):
            """!
            Gets the address line 2.
            Address line 2 contains postal code and town.
            Setting this field sets the address type to AddressType.CombinedElements unless it's already
            AddressType.Structured, in which case it becomes AddressType.Conflicting.
            This field is only used for combined elements addresses. For this type, it's mandatory.
            @return: The address line 2.
            """
            return self.getJavaClass().getAddressLine2()

      def setAddressLine2(self, value):
            """!
            Sets the address line 2.
            Address line 2 contains postal code and town.
            Setting this field sets the address type to AddressType.CombinedElements unless it's already
            AddressType.Structured, in which case it becomes AddressType.Conflicting.
            This field is only used for combined elements addresses. For this type, it's mandatory.
            @:param:The address line 2.
            """
            self.getJavaClass().setAddressLine2(value)

      def getStreet(self):
            """!
            Gets the street.
            The street must be speicfied without house number.
            Setting this field sets the address type to AddressType.Structured unless it's already
            AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
            This field is only used for structured addresses and is optional.
            @return:The street.
            """
            return self.getJavaClass().getStreet()

      def setStreet(self, value):
            """!
            Sets the street.
            The street must be speicfied without house number.
            Setting this field sets the address type to AddressType.Structured unless it's already
            AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
            This field is only used for structured addresses and is optional.
            @:param:The street.
            """
            self.getJavaClass().setStreet(value)

      def getHouseNo(self):
            """!
            Gets the house number.
            Setting this field sets the address type to AddressType.Structured unless it's already
            AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
            This field is only used for structured addresses and is optional.
            @return:The house number.
            """
            return self.getJavaClass().getHouseNo()

      def setHouseNo(self, value):
            """!
            Sets the house number.
            Setting this field sets the address type to AddressType.Structured unless it's already
            AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
            This field is only used for structured addresses and is optional.
            @:param:The house number.
            """
            self.getJavaClass().setHouseNo(value)

      def getPostalCode(self):
            """!
            Gets the postal code.
            Setting this field sets the address type to AddressType.Structured unless it's already
            AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
            This field is only used for structured addresses. For this type, it's mandatory.
            @return:The postal code.
            """
            return self.getJavaClass().getPostalCode()

      def setPostalCode(self, value):
            """!
            Sets the postal code.
            Setting this field sets the address type to AddressType.Structured unless it's already
            AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
            This field is only used for structured addresses. For this type, it's mandatory.
            @:param:The postal code.
            """
            self.getJavaClass().setPostalCode(value)

      def getTown(self):
            """!
            Gets the town or city.
            Setting this field sets the address type to AddressType.Structured unless it's already
            AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
            This field is only used for structured addresses. For this type, it's mandatory.
            @return:The town or city.
            """
            return self.getJavaClass().getTown()

      def setTown(self, value):
            """!
            Sets the town or city.
            Setting this field sets the address type to AddressType.Structured unless it's already
            AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
            This field is only used for structured addresses. For this type, it's mandatory.
            @:param:The town or city.
            """
            self.getJavaClass().setTown(value)

      def getCountryCode(self):
            """!
            Gets the two-letter ISO country code.
            The country code is mandatory unless the entire address contains None or emtpy values.
            @return:The ISO country code.
            """
            return self.getJavaClass().getCountryCode()

      def setCountryCode(self, value):
            """!
            Sets the two-letter ISO country code.
            The country code is mandatory unless the entire address contains None or emtpy values.
            @:param:The ISO country code.
            """
            self.getJavaClass().setCountryCode(value)

      def clear(self):
            """!
            Clears all fields and sets the type to AddressType.Undetermined.
            """
            self.setName(None)
            self.setAddressLine1(None)
            self.setaddressLine2(None)
            self.setStreet(None)
            self.setHouseNo(None)
            self.setPostalCode(None)
            self.setTown(None)
            self.setCountryCode(None)

      def equals(self, obj):
            """!
            Determines whether the specified object is equal to the current object.
            @return True if the specified object is equal to the current object; otherwise, false.
            @param obj The object to compare with the current object.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Gets the hash code for this instance.
            @return A hash code for the current object.
            """
            return self.getJavaClass().hashCode()

      def init(self):
            return


class AddressType(Enum):
      """!
      Address type
      """

      ## Undetermined
      UNDETERMINED = 0

      ## Structured address
      STRUCTURED = 1

      ## Combined address elements
      COMBINED_ELEMENTS = 2

      ## Conflicting
      CONFLICTING = 3


class AlternativeScheme(Assist.BaseJavaClass):
      """!
      Alternative payment scheme instructions
      """
      javaClassName = "com.aspose.mw.barcode.complexbarcode.MwAlternativeScheme"

      def __init__(self, instruction):
            javaAlternativeScheme = jpype.JClass(AlternativeScheme.javaClassName)
            super().__init__(javaAlternativeScheme(instruction))

      @staticmethod
      def construct(javaClass):
            jsClass = AlternativeScheme("")
            jsClass.setJavaClass(javaClass)
            return jsClass

      def getInstruction(self):
            """!
            Gets the payment instruction for a given bill.
            The instruction consists of a two letter abbreviation for the scheme, a separator characters
            and a sequence of parameters(separated by the character at index 2).
            @return:The payment instruction.
            """
            return self.getJavaClass().getInstruction()

      def setInstruction(self, value):
            """!
            Gets the payment instruction for a given bill.
            The instruction consists of a two letter abbreviation for the scheme, a separator characters
            and a sequence of parameters(separated by the character at index 2).
            @:param:The payment instruction.
            """
            self.getJavaClass().setInstruction(value)

      def equals(self, obj):
            """!
            Determines whether the specified object is equal to the current object.
            @return True if the specified object is equal to the current object; otherwise, false.
            @param obj The object to compare with the current object.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Gets the hash code for this instance.
            @return  hash code for the current object.
            """
            return self.getJavaClass().hashCode()

      def init(self):
            return


class ComplexCodetextReader(Assist.BaseJavaClass):
      """!
      ComplexCodetextReader decodes codetext to specified complex barcode type.
      This sample shows how to recognize and decode SwissQR image.
       \code
         barCodeReader = Recognition.BarCodeReader("SwissQRCodetext.png", None, Recognition.DecodeType.QR)
         results = barCodeReader.readBarCodes()
         result = ComplexBarcode.ComplexCodetextReader.tryDecodeSwissQR(results[0].getCodeText())
       \endcode
      """
      javaClassName = "com.aspose.mw.barcode.complexbarcode.MwComplexCodetextReader"

      @staticmethod
      def tryDecodeSwissQR(encodedCodetext):
            """!
            Decodes SwissQR codetext.
            @return decoded SwissQRCodetext or None.
            @param encodedCodetext encoded codetext
            """
            javaPythonComplexCodetextReader = jpype.JClass(ComplexCodetextReader.javaClassName)
            return SwissQRCodetext.construct(javaPythonComplexCodetextReader.tryDecodeSwissQR(encodedCodetext))

      @staticmethod
      def tryDecodeMailmark2D(encodedCodetext):
            """!
            Decodes Royal Mail Mailmark 2D codetext.
            @param encodedCodetext encoded codetext
            @return decoded Royal Mail Mailmark 2D or None.
            """
            javaPythonComplexCodetextReader = jpype.JClass(ComplexCodetextReader.javaClassName)
            return Mailmark2DCodetext.construct(javaPythonComplexCodetextReader.tryDecodeMailmark2D(encodedCodetext))

      @staticmethod
      def tryDecodeMailmark(encodedCodetext):
            """!
            Decodes Mailmark Barcode C and L codetext.
            @param encodedCodetext encoded codetext
            @return Decoded Mailmark Barcode C and L or None.
            """
            res = ComplexBarcode.MailmarkCodetext(None)
            try:
                  res.initFromString(encodedCodetext)
            except Exception as e:
                  return None
            return res

      @staticmethod
      def tryDecodeMaxiCode(maxiCodeMode, encodedCodetext):
            """!
            Decodes MaxiCode codetext.
            @param: maxiCodeMode:  MaxiCode mode
            @param: encodedCodetext:  encoded codetext
            @return:  Decoded MaxiCode codetext.
            """
            javaComplexCodetextReaderClass = jpype.JClass(ComplexCodetextReader.javaClassName)
            javaMaxiCodeCodetextMode2Class = jpype.JClass(MaxiCodeCodetextMode2.JAVA_CLASS_NAME)
            javaMaxiCodeCodetextMode3Class = jpype.JClass(MaxiCodeCodetextMode3.JAVA_CLASS_NAME)
            javaMaxiCodeCodetext =  javaComplexCodetextReaderClass.tryDecodeMaxiCode(maxiCodeMode, encodedCodetext)

            if javaMaxiCodeCodetext.getClass().equals(javaMaxiCodeCodetextMode2Class().getClass()):
                  return MaxiCodeCodetextMode2.construct(javaMaxiCodeCodetext)
            elif javaMaxiCodeCodetext.getClass().equals(javaMaxiCodeCodetextMode3Class().getClass()):
                  return MaxiCodeCodetextMode3.construct(javaMaxiCodeCodetext)
            else:
                  return MaxiCodeStandardCodetext.construct(javaMaxiCodeCodetext)

      @staticmethod
      def tryDecodeHIBCLIC(encodedCodetext):
            """!
            Decodes HIBC LIC codetext.
            @param: encodedCodetext:encoded codetext
            @return:decoded HIBC LIC Complex Codetext or None.
            """
            javaHIBCLICSecondaryAndAdditionalDataCodetextClass = jpype.JClass(HIBCLICSecondaryAndAdditionalDataCodetext.JAVA_CLASS_NAME)
            javaHIBCLICPrimaryDataCodetextClass = jpype.JClass(HIBCLICPrimaryDataCodetext.JAVA_CLASS_NAME)
            javaHIBCLICCombinedCodetextClass = jpype.JClass(HIBCLICCombinedCodetext.JAVA_CLASS_NAME)
            javaPhpComplexCodetextReaderJavaClass = jpype.JClass(ComplexCodetextReader.javaClassName)
            hibclicComplexCodetext = javaPhpComplexCodetextReaderJavaClass.tryDecodeHIBCLIC(encodedCodetext)
            if hibclicComplexCodetext is None:
                  return hibclicComplexCodetext
            if hibclicComplexCodetext.getClass().equals(javaHIBCLICSecondaryAndAdditionalDataCodetextClass().getClass()):
                  return HIBCLICSecondaryAndAdditionalDataCodetext.construct(hibclicComplexCodetext)
            elif hibclicComplexCodetext.getClass().equals(javaHIBCLICPrimaryDataCodetextClass().getClass()):
                  return HIBCLICPrimaryDataCodetext.construct(hibclicComplexCodetext)
            elif hibclicComplexCodetext.getClass().equals(javaHIBCLICCombinedCodetextClass().getClass()):
                  return HIBCLICCombinedCodetext.construct(hibclicComplexCodetext)
            return None

      @staticmethod
      def tryDecodeHIBCPAS(encodedCodetext):
            """!
            Decodes HIBC PAS codetext.
            @param: encodedCodetext:  encoded codetext
            @return: decoded HIBC PAS Complex Codetext or None.
            """
            javaComplexCodetextReader = jpype.JClass(ComplexCodetextReader.javaClassName)
            javaHIBCPAS = javaComplexCodetextReader.tryDecodeHIBCPAS(encodedCodetext)
            if javaHIBCPAS is None:
                  return None
            return HIBCPASCodetext.construct(javaHIBCPAS)

class QrBillStandardVersion(Enum):
      """!
      SwissQR bill standard version
      """

      ## Version 2.0
      V2_0 = 0


class SwissQRBill(Assist.BaseJavaClass):
      """!
      SwissQR bill data
      """

      def init(self):
            self.creditor = Address.construct(self.getJavaClass().getCreditor())
            self.debtor = Address.construct(self.getJavaClass().getDebtor())

      def __init__(self, javaClass):
            self.creditor = None
            self.debtor = None
            super().__init__(javaClass)
            self.init()

      @staticmethod
      def convertAlternativeSchemes(javaAlternativeSchemes):
            alternativeSchemes = []
            i = 0
            while i < javaAlternativeSchemes.size():
                  alternativeSchemes.append(AlternativeScheme.construct(javaAlternativeSchemes.get(i)))
                  i += 1
            return alternativeSchemes

      def getVersion(self):
            """!
            Gets the version of the SwissQR bill standard.
            @return:The SwissQR bill standard version.
            """
            return QrBillStandardVersion(self.getJavaClass().getVersion())

      def setVersion(self, value):
            """!
            Sets the version of the SwissQR bill standard.
            @:param:The SwissQR bill standard version.
            """
            self.getJavaClass().setVersion(value.value)

      def getAmount(self):
            """!
            Gets the payment amount.
            Valid values are between 0.01 and 999,999,999.99.
            @return:The payment amount.
            """
            return self.getJavaClass().getAmount()

      def setAmount(self, value):
            """!
            Sets the payment amount.
            Valid values are between 0.01 and 999,999,999.99.
            @:param:The payment amount.
            """
            self.getJavaClass().setAmount(value)

      def getCurrency(self):
            """!
            Gets the payment currency.
            Valid values are "CHF" and "EUR".
            @return:The payment currency.
            """
            return self.getJavaClass().getCurrency()

      def setCurrency(self, value):
            """!
            Sets the payment currency.
            Valid values are "CHF" and "EUR".
            @:param:The payment currency.
            """
            self.getJavaClass().setCurrency(value)

      def getAccount(self):
            """!
            Gets the creditor's account number.
            Account numbers must be valid IBANs of a bank of Switzerland or
            Liechtenstein. Spaces are allowed in the account number.
            @return:The creditor account number.
            """
            return self.getJavaClass().getAccount()

      def setAccount(self, value):
            """!
            Sets the creditor's account number.
            Account numbers must be valid IBANs of a bank of Switzerland or
            Liechtenstein. Spaces are allowed in the account number.
            @:param:The creditor account number.
            """
            self.getJavaClass().setAccount(value)

      def getCreditor(self):
            """!
            Gets the creditor address.
            @return:The creditor address.
            """
            return self.creditor

      def setCreditor(self, value):
            """!
            Sets the creditor address.
            @:param:The creditor address.
            """
            self.creditor = value
            self.getJavaClass().setCreditor(value.getJavaClass())

      def getReference(self):
            """!
            Gets the creditor payment reference.
            The reference is mandatory for SwissQR IBANs, i.e.IBANs in the range
            CHxx30000xxxxxx through CHxx31999xxxxx.
            If specified, the reference must be either a valid SwissQR reference
            (corresponding to ISR reference form) or a valid creditor reference
             according to ISO 11649 ("RFxxxx"). Both may contain spaces for formatting.
            @return:The creditor payment reference.
            """
            return self.getJavaClass().getReference()

      def setReference(self, value):
            """!
            Sets the creditor payment reference.
            The reference is mandatory for SwissQR IBANs, i.e.IBANs in the range
            CHxx30000xxxxxx through CHxx31999xxxxx.
            If specified, the reference must be either a valid SwissQR reference
            (corresponding to ISR reference form) or a valid creditor reference
            according to ISO 11649 ("RFxxxx"). Both may contain spaces for formatting.
            @:param:The creditor payment reference.
            """
            self.getJavaClass().setReference(value)

      def createAndSetCreditorReference(self, rawReference):
            """!
            Creates and sets a ISO11649 creditor reference from a raw string by prefixing
            the String with "RF" and the modulo 97 checksum.
            Whitespace is removed from the reference
            @exception ArgumentException rawReference contains invalid characters.
            @param rawReference The raw reference.
            """
            self.getJavaClass().createAndSetCreditorReference(rawReference)

      def getDebtor(self):
            """!
            Gets the debtor address.
            The debtor is optional. If it is omitted, both setting this field to
            None or setting an address with all None or empty values is ok.
            @return:The debtor address.
            """
            return self.debtor

      def setDebtor(self, value):
            """!
            Sets the debtor address.
            The debtor is optional. If it is omitted, both setting this field to
            None or setting an address with all None or empty values is ok.
            @:param:The debtor address.
            """
            self.debtor = value
            self.getJavaClass().setDebtor(value.getJavaClass())

      def getUnstructuredMessage(self):
            """!
            Gets the additional unstructured message.
            @return:The unstructured message.
            """
            return self.getJavaClass().getUnstructuredMessage()

      def setUnstructuredMessage(self, value):
            """!
            Sets the additional unstructured message.
            @:param:The unstructured message.
            """
            self.getJavaClass().setUnstructuredMessage(value)

      def getBillInformation(self):
            """!
            Gets the additional structured bill information.
            @return:The structured bill information.
            """
            return self.getJavaClass().getBillInformation()

      def setBillInformation(self, value):
            """!
            Sets the additional structured bill information.
            @:param:The structured bill information.
            """
            self.getJavaClass().setBillInformation(value)

      def getAlternativeSchemes(self):
            """!
            Gets the alternative payment schemes.
            A maximum of two schemes with parameters are allowed.
            @return:The alternative payment schemes.
            """
            return SwissQRBill.convertAlternativeSchemes(self.getJavaClass().getAlternativeSchemes())

      def setAlternativeSchemes(self, value):
            """!
            Sets the alternative payment schemes.
            A maximum of two schemes with parameters are allowed.
            @:param:The alternative payment schemes.
            """
            ArrayList = jpype.JClass('java.util.ArrayList')
            javaArray = ArrayList()
            i = 0
            while (i < len(value)):
                  javaArray.add(value[i].getJavaClass())
                  i += 1
            self.getJavaClass().setAlternativeSchemes(javaArray)

      def equals(self, obj):
            """!
            Determines whether the specified object is equal to the current object.
            @return True if the specified object is equal to the current object; otherwise, false.
            @param obj The object to compare with the current object.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Gets the hash code for this instance.
            @return A hash code for the current object.
            """
            return self.getJavaClass().hashCode()


class SwissQRCodetext(IComplexCodetext):
      """!
      Class for encoding and decoding the text embedded in the SwissQR code.
      """
      javaClassName = "com.aspose.mw.barcode.complexbarcode.MwSwissQRCodetext"

      def init(self):
            self.bill = SwissQRBill(self.getJavaClass().getBill())

      def getBill(self):
            """!
            SwissQR bill data
            """
            return self.bill

      def __init__(self, bill):
            """!
            Creates an instance of SwissQRCodetext.
            @param bill SwissQR bill data
            @throws BarCodeException
            """
            javaClass = jpype.JClass(SwissQRCodetext.javaClassName)

            self.bill = None
            javaBill = None

            if bill == None:
                  javaBill = javaClass()
            else:
                  javaBill = javaClass(bill.getJavaClass())
            super().__init__(javaBill)
            self.init()

      @staticmethod
      def construct(javaClass):
            phpClass = SwissQRCodetext(None)
            phpClass.setJavaClass(javaClass)
            return phpClass

      def getConstructedCodetext(self):
            """!
            Construct codetext from SwissQR bill data
            @return Constructed codetext
            """
            return self.getJavaClass().getConstructedCodetext()

      def initFromString(self, constructedCodetext):
            """!
            Initializes Bill with constructed codetext.
            @param constructedCodetext Constructed codetext.
            """
            self.getJavaClass().initFromString(constructedCodetext)
            self.init()

      def getBarcodeType(self):
            """!
            Gets barcode type.
            @return Barcode type.
            """
            return Generation.EncodeTypes(self.getJavaClass().getBarcodeType())

class MailmarkCodetext(IComplexCodetext):
      """!
      Class for encoding and decoding the text embedded in the 4-state Royal Mailmark code.
      """
      javaClassName = "com.aspose.mw.barcode.complexbarcode.MwMailmarkCodetext"

      def getFormat(self):
            """!
            "0" – None or Test
            "1" – Letter
            "2" – Large Letter
            """
            return self.getJavaClass().getFormat()

      def setFormat(self, value):
            """!
            "0" – None or Test
            "1" – LetterN
            "2" – Large Letter
            """
            self.getJavaClass().setFormat(value)

      def getVersionID(self):
            """!
            Currently "1" – For Mailmark barcode (0 and 2 to 9 and A to Z spare for future use)
            @return:
            """
            return self.getJavaClass().getVersionID()

      def setVersionID(self, value):
            """!
            Currently "1" – For Mailmark barcode (0 and 2 to 9 and A to Z spare for future use)
            """
            self.getJavaClass().setVersionID(value)

      def getClass_(self):
            """!
            "0" - None or Test
            "1" - 1C (Retail)
            "2" - 2C (Retail)
            "3" - 3C (Retail)
            "4" - Premium (RetailPublishing Mail) (for potential future use)
            "5" - Deferred (Retail)
            "6" - Air (Retail) (for potential future use)
            "7" - Surface (Retail) (for potential future use)
            "8" - Premium (Network Access)
            "9" - Standard (Network Access)
            """
            return self.getJavaClass().getClass_()

      def setClass(self, value):
            """!
            "0" - None or Test
            "1" - 1C (Retail)
            "2" - 2C (Retail)
            "3" - 3C (Retail)
            "4" - Premium (RetailPublishing Mail) (for potential future use)
            "5" - Deferred (Retail)
            "6" - Air (Retail) (for potential future use)
            "7" - Surface (Retail) (for potential future use)
            "8" - Premium (Network Access)
            "9" - Standard (Network Access)
            """
            self.getJavaClass().setClass(value)

      def getSupplychainID(self):
            """!
            Maximum values are 99 for Barcode C and 999999 for Barcode L.
            @return:
            """
            return self.getJavaClass().getSupplychainID()

      def setSupplychainID(self, value):
            """!
            Maximum values are 99 for Barcode C and 999999 for Barcode L.
            @param: value:
            @return:
            """
            self.getJavaClass().setSupplychainID(value)

      def getItemID(self):
            """!
            Maximum value is 99999999.
            @return:
            """
            return self.getJavaClass().getItemID()

      def setItemID(self, value):
            """!
            Maximum value is 99999999.
            @param: value:
            @return:
            """
            self.getJavaClass().setItemID(value)

      def getDestinationPostCodePlusDPS(self):
            """!
            The PC and DP must comply with a PAF format.
            Nine character string denoting international "XY11     " (note the 5 trailing spaces) or a pattern
            of characters denoting a domestic sorting code.
            A domestic sorting code consists of an outward postcode, an inward postcode, and a Delivery Point Suffix.

            @return:
            """
            return self.getJavaClass().getDestinationPostCodePlusDPS()

      def setDestinationPostCodePlusDPS(self, value):
            """!
            The PC and DP must comply with a PAF format.
            Nine character string denoting international "XY11     " (note the 5 trailing spaces) or a pattern
            of characters denoting a domestic sorting code.
            A domestic sorting code consists of an outward postcode, an inward postcode, and a Delivery Point Suffix.

            @param: value:
            @return:
            """
            self.getJavaClass().setDestinationPostCodePlusDPS(value)

      def __init__(self, mailmarkCodetext):
            """!
            Initializes a new instance of the MailmarkCodetext class.
            @param: mailmarkCodetext:
            """

            java_class_link = jpype.JClass(self.javaClassName)
            javaClass = None
            if mailmarkCodetext == None:
                  javaClass = java_class_link()
            else:
                  javaClass = java_class_link(mailmarkCodetext.getJavaClass())
            super().__init__(javaClass)

      def init(self):
            pass

      def getConstructedCodetext(self):
            """!
            Construct codetext from Mailmark data.

            @return: Constructed codetext
            """
            return str(self.getJavaClass().getConstructedCodetext())

      def initFromString(self, constructedCodetext):
            """!
            Initializes Mailmark data from constructed codetext.
            @param: constructedCodetext: Constructed codetext
            @return:
            """
            self.getJavaClass().initFromString(constructedCodetext)

      def getBarcodeType(self):
            """!
            Gets barcode type.
            @return: Barcode type.
            """
            return int(self.getJavaClass().getBarcodeType())

class Mailmark2DCodetext(IComplexCodetext):

      javaClassName = "com.aspose.mw.barcode.complexbarcode.MwMailmark2DCodetext"

      @staticmethod
      def construct(javaClass):
            jsClass = Mailmark2DCodetext()
            jsClass.setJavaClass(javaClass)
            return jsClass

      def getUPUCountryID(self):
            """!
            Identifies the UPU Country ID.Max length: 4 characters.
            @return Country ID
            """
            return self.getJavaClass().getUPUCountryID()

      def setUPUCountryID(self, value):
            """!
                Identifies the UPU Country ID.Max length: 4 characters.
                @param value Country ID
            """
            self.getJavaClass().setUPUCountryID(value)

      def getInformationTypeID(self):
            """!
            Identifies the Royal Mail Mailmark barcode payload for each product type.
            Valid Values:

            “0” - Domestic Sorted &amp; Unsorted
            “A” - Online Postage
            “B” - Franking
            “C” - Consolidation

            @return Information type ID
            """
            return self.getJavaClass().getInformationTypeID()

      def setInformationTypeID(self, value):
            """!
            Identifies the Royal Mail Mailmark barcode payload for each product type.
            Valid Values:

            “0” - Domestic Sorted &amp; Unsorted
            “A” - Online Postage
            “B” - Franking
            “C” - Consolidation

            @param value Information type ID
            """
            self.getJavaClass().setInformationTypeID(value)

      def getVersionID(self):
            """!
            Identifies the  barcode version as relevant to each Information Type ID.
            Valid Values:

            Currently “1”.
            “0” &amp; “2” to “9” and “A” to “Z” spare reserved for potential future use.

            @return Version ID
            """
            return self.getJavaClass().getVersionID()

      def setVersionID(self, value):
            """!
            Identifies the  barcode version as relevant to each Information Type ID.
            Valid Values:

            Currently “1”.
            “0” &amp; “2” to “9” and “A” to “Z” spare reserved for potential future use.

            @param value Version ID
            """
            self.getJavaClass().setVersionID(value)

      def getclass(self):
            """!
            Identifies the class of the item.

            Valid Values:
            “1” - 1C (Retail)
            “2” - 2C (Retail)
            “3” - Economy (Retail)
            “5” - Deffered (Retail)
            “8” - Premium (Network Access)
            “9” - Standard (Network Access)

            @return class of the item
            """
            return self.getJavaClass().getclass()

      def setclass(self, value):
            """!
            Identifies the class of the item.
            @param  Valid Values:
            “1” - 1C (Retail)
            “2” - 2C (Retail)
            “3” - Economy (Retail)
            “5” - Deffered (Retail)
            “8” - Premium (Network Access)
            “9” - Standard (Network Access)
            @return: class of the item
            """
            self.getJavaClass().setclass(value)

      def getSupplyChainID(self):
            """!
            Identifies the unique group of customers involved in the mailing.
            Max value: 9999999.

            @return Supply chain ID
            """
            return self.getJavaClass().getSupplyChainID()

      def setSupplyChainID(self, value):
            """!
            Identifies the unique group of customers involved in the mailing.
            Max value: 9999999.
            @@param:: value: Supply chain ID
            """
            self.getJavaClass().setSupplyChainID(value)

      def getItemID(self):
            """!
            Every Mailmark barcode is required to carry an ID
            Max value: 99999999.

            @return: item within the Supply Chain ID
            """
            return self.getJavaClass().getItemID()

      def setItemID(self, value):
            """!
            Identifies the unique item within the Supply Chain ID.
            Every Mailmark barcode is required to carry an ID
            Max value: 99999999.
            """
            self.getJavaClass().setItemID(value)

      def getDestinationPostCodeAndDPS(self):
            """!
            Contains the Postcode of the Delivery Address with DPS
            If inland the Postcode/DP contains the following number of characters.
            Area (1 or 2 characters) District(1 or 2 characters)
            Sector(1 character) Unit(2 characters) DPS (2 characters).
            The Postcode and DPS must comply with a valid PAF® format.

            @return the Postcode of the Delivery Address with DPS
            """
            return self.getJavaClass().getDestinationPostCodeAndDPS()

      def setDestinationPostCodeAndDPS(self, value):
            """!
            Contains the Postcode of the Delivery Address with DPS
            If inland the Postcode/DP contains the following number of characters.
            Area (1 or 2 characters) District(1 or 2 characters)
            Sector(1 character) Unit(2 characters) DPS (2 characters).
            The Postcode and DPS must comply with a valid PAF® format.
            @param: value: the Postcode of the Delivery Address with DPS
            """
            self.getJavaClass().setDestinationPostCodeAndDPS(value)

      def getRTSFlag(self):
            """!
            Flag which indicates what level of Return to Sender service is being requested.
            @return RTS Flag
            """
            return self.getJavaClass().getRTSFlag()

      def setRTSFlag(self, value):
            """!
            Flag which indicates what level of Return to Sender service is being requested.
            @param: value: RTS Flag
            """
            self.getJavaClass().setRTSFlag(value)

      def getReturnToSenderPostCode(self):
            """!
            Contains the Return to Sender Post Code but no DPS.
            The PC(without DPS) must comply with a PAF® format.
            @return: Return to Sender Post Code but no DPS
            """
            return self.getJavaClass().getReturnToSenderPostCode()

      def setReturnToSenderPostCode(self, value):
            """!
            Contains the Return to Sender Post Code but no DPS.
            The PC(without DPS) must comply with a PAF® format.
            @param: value: Return to Sender Post Code but no DPS
            """
            self.getJavaClass().setReturnToSenderPostCode(value)

      def getCustomerContent(self):
            """!
             Optional space for use by customer.

             Max length by Type:
             Type 7: 6 characters
             Type 9: 45 characters
             Type 29: 25 characters

            @return: Customer content
            """
            return self.getJavaClass().getCustomerContent()

      def setCustomerContent(self, value):
            """!
            Optional space for use by customer.

            Max length by Type:
            Type 7: 6 characters
            Type 9: 45 characters
            Type 29: 25 characters

            @param value  Customer content
            """
            self.getJavaClass().setCustomerContent(value)

      def getCustomerContentEncodeMode(self):
            """!
            Encode mode of Datamatrix barcode.
            Default value: DataMatrixEncodeMode.C40.

            @return Encode mode of Datamatrix barcode.
            """
            return Generation.DataMatrixEncodeMode(self.getJavaClass().getCustomerContentEncodeMode())

      def setCustomerContentEncodeMode(self, value):
            """!
            Encode mode of Datamatrix barcode.
            Default value: DataMatrixEncodeMode.C40.
            @param: value: Encode mode of Datamatrix barcode.
            """
            self.getJavaClass().setCustomerContentEncodeMode(value.value)

      def getDataMatrixType(self):
            """!
            2D Mailmark Type defines size of Data Matrix barcode.
            @return: Size of Data Matrix barcode
            """
            return Mailmark2DType(self.getJavaClass().getDataMatrixType())

      def setDataMatrixType(self, value):
            """!
            2D Mailmark Type defines size of Data Matrix barcode.
            @param: value: Size of Data Matrix barcode
            """
            self.getJavaClass().setDataMatrixType(value.value)

      def __init__(self):
            """!
            Create default instance of Mailmark2DCodetext class.
            """
            javaMailmark2DCodetext = jpype.JClass(self.javaClassName)
            self.javaClass = javaMailmark2DCodetext()
            super().__init__(self.javaClass)
            self.init()

      def init(self):
            pass

      def getConstructedCodetext(self):
            """!
            Construct codetext from Mailmark data.
            @return: Constructed codetext
            """
            return self.getJavaClass().getConstructedCodetext()

      def initFromString(self, constructedCodetext):
            """!
            Initializes Mailmark data from constructed codetext.
            @param: constructedCodetext: constructedCodetext Constructed codetext.
            """
            self.getJavaClass().initFromString(constructedCodetext)

      def getBarcodeType(self):
            """!
            Gets barcode type.
            @return: Barcode type.
            """
            return Generation.EncodeTypes.DATA_MATRIX


class MaxiCodeCodetext(IComplexCodetext):
      """!
      Base class for encoding and decoding the text embedded in the MaxiCode code.

      This sample shows how to decode raw MaxiCode codetext to MaxiCodeCodetext instance.
      \code
        reader = Recognition.BarCodeReader(imagePath, None, Recognition.DecodeType.MAXI_CODE)
        for result in reader.readBarCodes():
            resultMaxiCodeCodetext = ComplexBarcode.ComplexCodetextReader.tryDecodeMaxiCode(
                result.getExtended().getMaxiCode().getMaxiCodeMode(), result.getCodeText())
            print("BarCode Type: " + str(resultMaxiCodeCodetext.getBarcodeType()))
            print("MaxiCode mode: " + str(resultMaxiCodeCodetext.getMode()))
      \endcode
      """
      def getMode(self):
            """!
            Gets MaxiCode mode.
            @return: MaxiCode mode
            """
            pass


      def getMaxiCodeEncodeMode(self):
            """!
            Gets a MaxiCode encode mode.
            """
            return self.getJavaClass().getMaxiCodeEncodeMode()


      def setMaxiCodeEncodeMode(self, value):
            """!
            Sets a MaxiCode encode mode.
            """
            self.getJavaClass().setMaxiCodeEncodeMode(value)

      def getECIEncoding(self):
            """!
            Gets ECI encoding. Used when MaxiCodeEncodeMode is AUTO.
            """
            return self.getJavaClass().getECIEncoding()


      def setECIEncoding(self, value):
            """!
            Sets ECI encoding. Used when MaxiCodeEncodeMode is AUTO.
            """
            self.getJavaClass().setECIEncoding(value)

      def getBarcodeType(self):
            """!
            Gets barcode type.
            @return:Barcode type
            """
            return self.getJavaClass().getBarcodeType()

class MaxiCodeSecondMessage(Assist.BaseJavaClass):
      """!
      Base class for encoding and decoding second message for MaxiCode barcode.
      """
      def getMessage(self):
            """!
            Gets constructed second message
            @return:  Constructed second message
            """
            pass

class MaxiCodeStandardCodetext(MaxiCodeCodetext):
      """!
       Class for encoding and decoding MaxiCode codetext for modes 4, 5 and 6.

       # Mode 4
         \code
            maxiCodeCodetext = MaxiCodeStandardCodetext()
            maxiCodeCodetext.setMode(MaxiCodeMode.MODE_4)
            maxiCodeCodetext.setMessage("Test message")
            complexGenerator = ComplexBarcodeGenerator(maxiCodeCodetext.getConstructedCodetext())
            complexGenerator.generateBarCodeImage()
         \endcode

         \code

              # Mode 5
              maxiCodeCodetext = MaxiCodeStandardCodetext()
              maxiCodeCodetext.setMode(MaxiCodeMode.MODE_5)
              maxiCodeCodetext.setMessage("Test message")
              complexGenerator = ComplexBarcodeGenerator(maxiCodeCodetext.getConstructedCodetext())
              complexGenerator.generateBarCodeImage()

         \endcode

         \code

              # Mode 6
              maxiCodeCodetext = MaxiCodeStandardCodetext()
              maxiCodeCodetext.setMode(MaxiCodeMode.MODE_6)
              maxiCodeCodetext.setMessage("Test message")
              complexGenerator = ComplexBarcodeGenerator(maxiCodeCodetext.getConstructedCodetext())
              complexGenerator.generateBarCodeImage()
         \endcode
      """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.complexbarcode.MwMaxiCodeStandardCodetext"

      def __init__(self):
            try:
                  java_class = jpype.JClass(MaxiCodeStandardCodetext.JAVA_CLASS_NAME)
                  super().__init__(java_class())
            except Exception as ex:
                  raise Assist.BarCodeException(ex)

      @staticmethod
      def construct(javaClass):
            _class = MaxiCodeStandardCodetext()
            _class.setJavaClass(javaClass)

            return _class

      def getMessage(self):
            """!
             Gets message.
            """
            return self.getJavaClass().getMessage()

      def setMessage(self, value):
            """!
             Sets message.
            """
            self.getJavaClass().setMessage(value)

      def setMode(self, mode):
            """!
            Sets MaxiCode mode. Standart codetext can be used only with modes 4, 5 and 6.
            """
            self.getJavaClass().setMode(mode.value)

      def getMode(self):
            """!
            Gets MaxiCode mode.
            @return:MaxiCode mode
            """
            return Generation.MaxiCodeMode(self.getJavaClass().getMode())

      def getConstructedCodetext(self):
            """!
            Constructs codetext
            @return:Constructed codetext
            """
            return self.getJavaClass().getConstructedCodetext()

      def initFromString(self, constructedCodetext):
            """!
            Initializes instance from constructed codetext.
            @param: constructedCodetext:Constructed codetext.
            """
            self.getJavaClass().initFromString(constructedCodetext)

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified MaxiCodeStandardCodetext value.
            @param: obj:An MaxiCodeStandardCodetext value to compare to this instance.
            @return:<b>True</b> if obj has the same value as this instance; otherwise, <b>false</b>.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def getHashCode(self):
            """!
            Returns the hash code for this instance.
            @return:A 32-bit signed integer hash code.
            """
            return self.getJavaClass().getHashCode()

      def init(self):
            pass

class MaxiCodeStandartSecondMessage(MaxiCodeSecondMessage):
      """!
      Class for encoding and decoding standart second message for MaxiCode barcode.
      """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.complexbarcode.MwMaxiCodeStandartSecondMessage"

      def __init__(self):
            try:
                  java_class = jpype.JClass(MaxiCodeStandartSecondMessage.JAVA_CLASS_NAME)
                  super().__init__(java_class())
            except Exception as ex:
                  raise Assist.BarCodeException(ex)

      def setMessage(self, value):
            """!
            Sets second message
            """
            self.getJavaClass().setMessage(value)

      def getMessage(self):
            """!
            Gets constructed second message
            @return:Constructed second message
            """
            return self.getJavaClass().getMessage()

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified MaxiCodeStandartSecondMessage value.

            @param: obj:An MaxiCodeStandartSecondMessage value to compare to this instance.
            @return:<b>True</b> if obj has the same value as this instance; otherwise, <b>false</b>
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def getHashCode(self):
            """!
            Returns the hash code for this instance.
            @return:A 32-bit signed integer hash code.
            """
            return self.getJavaClass().getHashCode()

      def init(self):
            pass


class MaxiCodeStructuredCodetext(MaxiCodeCodetext):
      """!
      Base class for encoding and decoding the text embedded in the MaxiCode code for modes 2 and 3.

         This sample shows how to decode raw MaxiCode codetext to MaxiCodeStructuredCodetext instance.
         \code

         reader = Recognition.BarCodeReader(imagePath, None, DecodeType.MAXI_CODE)
         for result in reader.readBarCodes():
            resultMaxiCodeCodetext = ComplexCodetextReader.tryDecodeMaxiCode(
                result.getExtended().getMaxiCode().getMaxiCodeMode(), result.getCodeText())
            if resultMaxiCodeCodetext is MaxiCodeStructuredCodetext:
                maxiCodeStructuredCodetext = resultMaxiCodeCodetext
                print("BarCode Type: " + maxiCodeStructuredCodetext.getPostalCode())
                print("MaxiCode mode: " + maxiCodeStructuredCodetext.getCountryCode())
                print("BarCode CodeText: " + maxiCodeStructuredCodetext.getServiceCategory())
         \endcode
      """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.complexbarcode.MwMaxiCodeStructuredCodetext"

      def __init__(self, javaClass):
            try:
                  super().__init__(javaClass)
                  self.maxiCodeSecondMessage = None
            except Exception as ex:
                  raise Assist.BarCodeException(ex)

      def init(self):
            javaMaxiCodeSecondMessage = self.getJavaClass().getSecondMessage()
            javaMaxiCodeStandartSecondMessageClass = jpype.JClass("com.aspose.mw.barcode.complexbarcode.MwMaxiCodeStandartSecondMessage")
            javaMaxiCodeStandartSecondMessage = javaMaxiCodeStandartSecondMessageClass()
            javaMaxiCodeStructuredSecondMessageClass = jpype.JClass("com.aspose.mw.barcode.complexbarcode.MwMaxiCodeStructuredSecondMessage")
            javaMaxiCodeStructuredSecondMessage = javaMaxiCodeStructuredSecondMessageClass()

            if javaMaxiCodeSecondMessage is javaMaxiCodeStandartSecondMessage:
                  self.maxiCodeSecondMessage = MaxiCodeStandartSecondMessage(self.getJavaClass().getSecondMessage())
            elif javaMaxiCodeSecondMessage is javaMaxiCodeStructuredSecondMessage:
                  self.maxiCodeSecondMessage = MaxiCodeStructuredSecondMessage(self.getJavaClass().getSecondMessage())

      def getPostalCode(self):
            """!
            Identifies the postal code. Must be 9 digits in mode 2 or
            6 alphanumeric symbols in mode 3.
            """
            return self.getJavaClass().getPostalCode()

      def setPostalCode(self, value):
            """!
             Identifies the postal code. Must be 9 digits in mode 2 or
             6 alphanumeric symbols in mode 3.
            """
            self.getJavaClass().setPostalCode(value)

      def getCountryCode(self):
            """!
            Identifies 3 digit country code.
            """
            return self.getJavaClass().getCountryCode()

      def setCountryCode(self, value):
            """!
            Identifies 3 digit country code.
            """
            self.getJavaClass().setCountryCode(value)

      def getServiceCategory(self):
            """!
            Identifies 3 digit service category.
            """
            return self.getJavaClass().getServiceCategory()

      def setServiceCategory(self, value):
            """!
            Identifies 3 digit service category.
            """
            self.getJavaClass().setServiceCategory(value)

      def getSecondMessage(self):
            """!
            Identifies second message of the barcode.
            """
            return self.maxiCodeSecondMessage

      def setSecondMessage(self, value):
            """!
            Identifies second message of the barcode.
            """
            self.maxiCodeSecondMessage = value
            self.getJavaClass().setSecondMessage(value.getJavaClass())

      def getConstructedCodetext(self):
            """
            Constructs codetext
            @return:Constructed codetext
            """
            return str(self.getJavaClass().getConstructedCodetext())

      def initFromString(self, constructedCodetext):
            """
            Initializes instance from constructed codetext.
            @param: constructedCodetext:Constructed codetext.
            """
            self.getJavaClass().initFromString(constructedCodetext)

      def equals(self, obj):
            """
            Returns a value indicating whether this instance is equal to a specified MaxiCodeStructuredCodetext value.

            @param: obj:An MaxiCodeStructuredCodetext value to compare to this instance.
            @return:<b>True</b> if obj has the same value as this instance; otherwise, <b>false</b>.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def getHashCode(self):
            """!
            Returns the hash code for this instance.
            @return: A 32-bit signed integer hash code.
            """
            return self.getJavaClass().getHashCode()



class MaxiCodeCodetextMode2(MaxiCodeStructuredCodetext):
      """!
        Class for encoding and decoding the text embedded in the MaxiCode code for modes 2.

         This sample shows how to encode and decode MaxiCode codetext for mode 2.

         \code
         maxiCodeCodetext = MaxiCodeCodetextMode2()
         maxiCodeCodetext.setPostalCode("524032140")
         maxiCodeCodetext.setCountryCode(056)
         maxiCodeCodetext.setServiceCategory(999)
         maxiCodeStandartSecondMessage = MaxiCodeStandartSecondMessage()
         maxiCodeStandartSecondMessage.setMessage("Test message")
         maxiCodeCodetext.setSecondMessage(maxiCodeStandartSecondMessage)
         complexGenerator = ComplexBarcodeGenerator(maxiCodeCodetext)
         complexGenerator.generateBarCodeImage()

         \code
         \endcode

         maxiCodeCodetext = MaxiCodeCodetextMode2()
         maxiCodeCodetext.setPostalCode("524032140")
         maxiCodeCodetext.setCountryCode(056)
         maxiCodeCodetext.setServiceCategory(999)
         maxiCodeStructuredSecondMessage = MaxiCodeStructuredSecondMessage()
         maxiCodeStructuredSecondMessage.add("634 ALPHA DRIVE")
         maxiCodeStructuredSecondMessage.add("PITTSBURGH")
         maxiCodeStructuredSecondMessage.add("PA")
         maxiCodeStructuredSecondMessage.setYear(99)
         maxiCodeCodetext.setSecondMessage(maxiCodeStructuredSecondMessage)
         complexGenerator = ComplexBarcodeGenerator(maxiCodeCodetext)
         complexGenerator.generateBarCodeImage()

         \code
         \endcode

         reader = Recognition.BarCodeReader(imagePath, None, DecodeType.MAXI_CODE)
         for result in reader.readBarCodes():
            resultMaxiCodeCodetext = ComplexCodetextReader.tryDecodeMaxiCode(
                result.getExtended().getMaxiCode().getMaxiCodeMode(), result.getCodeText())
            if resultMaxiCodeCodetext is MaxiCodeCodetextMode2:
                maxiCodeStructuredCodetext = resultMaxiCodeCodetext
                print("BarCode Type: " + maxiCodeStructuredCodetext.getPostalCode())
                print("MaxiCode mode: " + maxiCodeStructuredCodetext.getCountryCode())
                print("BarCode CodeText: " + maxiCodeStructuredCodetext.getServiceCategory())
                if maxiCodeStructuredCodetext.SecondMessage is MaxiCodeStandartSecondMessage:
                    secondMessage = maxiCodeStructuredCodetext.getSecondMessage()
                    print("Message: " + secondMessage.getMessage())

         \code
         \endcode
        reader = Recognition.BarCodeReader(imagePath, None, DecodeType.MAXI_CODE)
        for result in reader.readBarCodes():
            resultMaxiCodeCodetext = ComplexCodetextReader.tryDecodeMaxiCode(
                result.getExtended().getMaxiCode().getMaxiCodeMode(), result.getCodeText())
            if resultMaxiCodeCodetext is MaxiCodeCodetextMode2:
                maxiCodeStructuredCodetext = resultMaxiCodeCodetext
                print("BarCode Type: " + maxiCodeStructuredCodetext.getPostalCode())
                print("MaxiCode mode: " + maxiCodeStructuredCodetext.getCountryCode())
                print("BarCode CodeText: " + maxiCodeStructuredCodetext.getServiceCategory())
                if maxiCodeStructuredCodetext.SecondMessage is MaxiCodeStructuredSecondMessage:
                    secondMessage = maxiCodeStructuredCodetext.getSecondMessage()
                    print("Message:")
                    for identifier in secondMessage.getIdentifiers():
                        print(identifier)
         \endcode
      """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.complexbarcode.MwMaxiCodeCodetextMode2"

      def __init__(self):
            try:
                  java_class = jpype.JClass(MaxiCodeCodetextMode2.JAVA_CLASS_NAME)
                  super().__init__(java_class())
            except Exception as ex:
                  raise Assist.BarCodeException(ex)

      @staticmethod
      def construct(javaClass):
            _class = MaxiCodeCodetextMode2()
            _class.setJavaClass(javaClass)

            return _class

      def getMode(self):
            """!
            Gets MaxiCode mode.
            @return:  MaxiCode mode
            """
            return self.getJavaClass().getMode()

      def init(self):
            super().init()

class MaxiCodeCodetextMode3(MaxiCodeStructuredCodetext):
      """!
        Class for encoding and decoding the text embedded in the MaxiCode code for modes 3.
        This sample shows how to encode and decode MaxiCode codetext for mode 3.

         \code
         # Mode 3 with standart second message
         maxiCodeCodetext = MaxiCodeCodetextMode3()
         maxiCodeCodetext.setPostalCode("B1050")
         maxiCodeCodetext.setCountryCode(056)
         maxiCodeCodetext.setServiceCategory(999)
         maxiCodeStandartSecondMessage = MaxiCodeStandartSecondMessage()
         maxiCodeStandartSecondMessage.setMessage("Test message")
         maxiCodeCodetext.setSecondMessage(maxiCodeStandartSecondMessage)
         complexGenerator = ComplexBarcodeGenerator(maxiCodeCodetext)
         complexGenerator.generateBarCodeImage()

         \endcode
         \code

         # Mode 3 with structured second message
         maxiCodeCodetext = MaxiCodeCodetextMode3()
         maxiCodeCodetext.setPostalCode("B1050")
         maxiCodeCodetext.setCountryCode(156)
         maxiCodeCodetext.setServiceCategory(999)
         maxiCodeStructuredSecondMessage = MaxiCodeStructuredSecondMessage()
         maxiCodeStructuredSecondMessage.add("634 ALPHA DRIVE")
         maxiCodeStructuredSecondMessage.add("PITTSBURGH")
         maxiCodeStructuredSecondMessage.add("PA")
         maxiCodeStructuredSecondMessage.setYear(99)
         maxiCodeCodetext.setSecondMessage(maxiCodeStructuredSecondMessage)
         complexGenerator = ComplexBarcodeGenerator(maxiCodeCodetext)
         complexGenerator.generateBarCodeImage()

         \endcode
         \code
         # Decoding raw codetext with standart second message
        reader = Recognition.BarCodeReader(imagePath, None, DecodeType.MAXI_CODE)
        for result in reader.readBarCodes():
            resultMaxiCodeCodetext = ComplexCodetextReader.tryDecodeMaxiCode(
                result.getExtended().getMaxiCode().getMaxiCodeMode(), result.getCodeText())
            if resultMaxiCodeCodetext is MaxiCodeCodetextMode3:
                maxiCodeStructuredCodetext = resultMaxiCodeCodetext
                print("BarCode Type: " + maxiCodeStructuredCodetext.getPostalCode())
                print("MaxiCode mode: " + maxiCodeStructuredCodetext.getCountryCode())
                print("BarCode CodeText: " + maxiCodeStructuredCodetext.getServiceCategory())
                if maxiCodeStructuredCodetext.getSecondMessage() is MaxiCodeStandartSecondMessage:
                    secondMessage = maxiCodeStructuredCodetext.getSecondMessage()
                    print("Message: " + secondMessage.getMessage())
         \endcode
         \code
         reader = Recognition.BarCodeReader(imagePath, None, DecodeType.MAXI_CODE)
         for result in reader.readBarCodes():
            resultMaxiCodeCodetext = ComplexCodetextReader.tryDecodeMaxiCode(
                result.getExtended().getMaxiCode().getMaxiCodeMode(), result.getCodeText())
            if resultMaxiCodeCodetext is MaxiCodeCodetextMode3:
                maxiCodeStructuredCodetext = resultMaxiCodeCodetext
                print("BarCode Type: " + maxiCodeStructuredCodetext.getPostalCode())
                print("MaxiCode mode: " + maxiCodeStructuredCodetext.getCountryCode())
                print("BarCode CodeText: " + maxiCodeStructuredCodetext.getServiceCategory())
                if maxiCodeStructuredCodetext.getSecondMessage() is MaxiCodeStructuredSecondMessage:
                    secondMessage = maxiCodeStructuredCodetext.getSecondMessage()
                    print("Message:")
                    for identifier in secondMessage.getIdentifiers():
                        print(identifier)
         \endcode
      """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.complexbarcode.MwMaxiCodeCodetextMode3"

      def __init__(self):
            try:
                  java_class = jpype.JClass(MaxiCodeCodetextMode3.JAVA_CLASS_NAME)
                  super().__init__(java_class())
            except Exception as ex:
                  raise Assist.BarCodeException(ex)

      @staticmethod
      def construct(javaClass):
            _class = MaxiCodeCodetextMode3()
            _class.setJavaClass(javaClass)

            return _class


      def getMode(self):
            """!
            Gets MaxiCode mode.
            @return:MaxiCode mode
            """
            return self.getJavaClass().getMode()

      def init(self):
            super().init()

class MaxiCodeStructuredSecondMessage(MaxiCodeSecondMessage):
      """!
      Class for encoding and decoding structured second message for MaxiCode barcode.
      """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.complexbarcode.MwMaxiCodeStructuredSecondMessage"

      def __init__(self):
            try:
                  java_class = jpype.JClass(MaxiCodeStructuredSecondMessage.JAVA_CLASS_NAME)
                  super().__init__(java_class())
                  self.maxiCodeSecondMessage = None
            except Exception as ex:
                  raise Assist.BarCodeException(ex)

      def getYear(self):
            """!
            Gets year. Year must be 2 digit integer value.
            """
            return self.getJavaClass().getYear()

      def setYear(self, value):
            """!
            Sets year. Year must be 2 digit integer value.
            """
            self.getJavaClass().setYear(value)

      def getIdentifiers(self):
            """!
            Gets identifiers list
            @return: List of identifiers
            """
            identifiers_string = self.getJavaClass().getIdentifiers()
            delimeter = "\\/\\"
            identifiers = identifiers_string.split(delimeter)

            return identifiers


      def add(self, identifier):
            """!
            Adds new identifier
            @param: identifier: Identifier to be added
            """
            self.getJavaClass().add(identifier)


      def clear(self):
            """!
            Clear identifiers list
            """
            self.getJavaClass().clear()

      def getMessage(self):
            """!
            Gets constructed second message
            @return: Constructed second message
            """
            return self.getJavaClass().getMessage()


      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified MaxiCodeStructuredSecondMessage value.

            @param: obj: An MaxiCodeStructuredSecondMessage value to compare to this instance
            @return: <b>True</b> if obj has the same value as this instance; otherwise, <b>false</b>.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def getHashCode(self):
            """!
            Returns the hash code for this instance.
            @return: A 32-bit signed integer hash code.
            """
            return self.getJavaClass().getHashCode()

      def init(self):
            pass

class HIBCLICComplexCodetext(IComplexCodetext):
      """!
       Base class for encoding and decoding the text embedded in the HIBC LIC code.

       This sample shows how to decode raw HIBC LIC codetext to HIBCLICComplexCodetext instance.
       \code
        reader = Recognition.BarCodeReader(imagePath, None, DecodeType.HIBC_AZTEC_LIC)
        for result in reader.readBarCodes():
            resultHIBCLICComplexCodetext = ComplexCodetextReader.tryDecodeHIBCLIC(result.getCodeText())
            print("BarCode Type: " + resultHIBCLICComplexCodetext.getBarcodeType())
            print("BarCode CodeText: " + resultHIBCLICComplexCodetext.getConstructedCodetext())
       \endcode
      """
      def __init__(self, javaClass):
            super().__init__(javaClass)

      def getConstructedCodetext(self):
            """!
            Constructs codetext
            @return:Constructed codetext
            """
            pass

      def initFromString(self,constructedCodetext):
            """!
            Initializes instance from constructed codetext.
            @param: constructedCodetext:Constructed codetext.
            """
            pass

      def getBarcodeType(self):
            """!
            Gets barcode type. HIBC LIC codetext can be encoded using HIBCCode39LIC, HIBCCode128LIC, HIBCAztecLIC, HIBCDataMatrixLIC and HIBCQRLIC encode types.
            Default value: HIBCCode39LIC.
            @return:Barcode type.
            """
            return Generation.EncodeTypes(self.getJavaClass().getBarcodeType())

      def setBarcodeType(self, value):
            """!
            Sets barcode type. HIBC LIC codetext can be encoded using HIBCCode39LIC, HIBCCode128LIC, HIBCAztecLIC, HIBCDataMatrixLIC and HIBCQRLIC encode types.
            Default value: HIBCCode39LIC.
            @return:Barcode type.
            """
            self.getJavaClass().setBarcodeType(value.value)

class HIBCLICCombinedCodetext(HIBCLICComplexCodetext):
      """!
      Class for encoding and decoding the text embedded in the HIBC LIC code which stores primary and secodary data.

      This sample shows how to encode and decode HIBC LIC using HIBCLICCombinedCodetext.
             \code
              combinedCodetext = HIBCLICCombinedCodetext()
              combinedCodetext.setBarcodeType(EncodeTypes.HIBCQRLIC)
              combinedCodetext.setPrimaryData(PrimaryData())
              combinedCodetext.getPrimaryData().setProductOrCatalogNumber("12345")
              combinedCodetext.getPrimaryData().setLabelerIdentificationCode("A999")
              combinedCodetext.getPrimaryData().setUnitOfMeasureID(1)
              combinedCodetext.setSecondaryAndAdditionalData(SecondaryAndAdditionalData())
              combinedCodetext.getSecondaryAndAdditionalData().setExpiryDate(datetime.now())
              combinedCodetext.getSecondaryAndAdditionalData().setExpiryDateFormat(HIBCLICDateFormat.MMDDYY)
              combinedCodetext.getSecondaryAndAdditionalData().setQuantity(30)
              combinedCodetext.getSecondaryAndAdditionalData().setLotNumber("LOT123")
              combinedCodetext.getSecondaryAndAdditionalData().setSerialNumber("SERIAL123")
              combinedCodetext.getSecondaryAndAdditionalData().setDateOfManufacture(datetime.now())
              generator = ComplexBarcode.ComplexBarcodeGenerator(combinedCodetext)
              image = generator.generateBarCodeImage()
              reader = Recognition.BarCodeReader(image, None, DecodeType.HIBCQRLIC)
              reader.readBarCodes()
              codetext = reader.getFoundBarCodes()[0].getCodeText()
              result = ComplexCodetextReader.tryDecodeHIBCLIC(codetext)
              if result is not None:
                  print("Product or catalog number: " + result.getPrimaryData().getProductOrCatalogNumber())
                  print("Labeler identification code: " + result.getPrimaryData().getLabelerIdentificationCode())
                  print("Unit of measure ID: " + result.getPrimaryData().getUnitOfMeasureID())
                  print("Expiry date: " + result.getSecondaryAndAdditionalData().getExpiryDate())
                  print("Quantity: " + result.getSecondaryAndAdditionalData().getQuantity())
                  print("Lot number: " + result.getSecondaryAndAdditionalData().getLotNumber())
                  print("Serial number: " + result.getSecondaryAndAdditionalData().getSerialNumber())
                  print("Date of manufacture: " + result.getSecondaryAndAdditionalData().getDateOfManufacture())
             \endcode
      """

      JAVA_CLASS_NAME = "com.aspose.mw.barcode.complexbarcode.MwHIBCLICCombinedCodetext"

      def __init__(self):
            java_class_link = jpype.JClass(HIBCLICCombinedCodetext.JAVA_CLASS_NAME)
            javaClass = java_class_link()
            self.auto_PrimaryData = None
            self.auto_SecondaryAndAdditionalData = None
            super().__init__(javaClass)

      @staticmethod
      def construct(javaClass):
            obj = HIBCLICCombinedCodetext()
            obj.setJavaClass(javaClass)
            return obj

      def init(self):
            self.auto_PrimaryData = PrimaryData.construct(self.getJavaClass().getPrimaryData())
            self.auto_SecondaryAndAdditionalData = SecondaryAndAdditionalData.construct(self.getJavaClass().getSecondaryAndAdditionalData())

      def getPrimaryData(self):
            """!
            Identifies primary data.
            """
            return self.auto_PrimaryData

      def setPrimaryData(self, value):
            """!
            Identifies primary data.
            """
            self.getJavaClass().setPrimaryData(value.getJavaClass())
            self.auto_PrimaryData = value


      def getSecondaryAndAdditionalData(self):
            """!
            Identifies secondary and additional supplemental data.
            """
            return self.auto_SecondaryAndAdditionalData

      def setSecondaryAndAdditionalData(self, value):
            """!
            Identifies secondary and additional supplemental data.
            """
            self.getJavaClass().setSecondaryAndAdditionalData(value.getJavaClass())
            self.auto_SecondaryAndAdditionalData = value


      def getConstructedCodetext(self):
            """!
            Constructs codetext
            @return:Constructed codetext
            """
            return self.getJavaClass().getConstructedCodetext()

      def initFromString(self, constructedCodetext):
            """!
            Initializes instance from constructed codetext.
            @param: constructedCodetext:Constructed codetext.
            """
            self.getJavaClass().initFromString(constructedCodetext)

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified HIBCLICCombinedCodetext value.
            @param: obj:An  HIBCLICCombinedCodetext value to compare to this instance.
            @return: <b>True</b> if obj has the same value as this instance; otherwise,  <b>false</b>.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return:A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

class HIBCLICPrimaryDataCodetext(HIBCLICComplexCodetext):
      """!
      Class for encoding and decoding the text embedded in the HIBC LIC code which stores primary data.

      This sample shows how to encode and decode HIBC LIC using HIBCLICPrimaryDataCodetext.
             \code
             complexCodetext = ComplexBarcode.HIBCLICPrimaryDataCodetext()
             complexCodetext.setBarcodeType(EncodeTypes.HIBCQRLIC)
             complexCodetext.setData(PrimaryData())
             complexCodetext.getData().setProductOrCatalogNumber("12345")
             complexCodetext.getData().setLabelerIdentificationCode("A999")
             complexCodetext.getData().setUnitOfMeasureID(1)
             generator = ComplexBarcode.ComplexBarcodeGenerator(complexCodetext)
             image = generator.generateBarCodeImage()
             reader = Recognition.BarCodeReader(image, None, DecodeType.HIBCQRLIC)
             reader.readBarCodes()
             codetext = reader.getFoundBarCodes()[0].getCodeText()
             result = ComplexBarcode.ComplexCodetextReader.tryDecodeHIBCLIC(codetext)
             print("Product or catalog number: " + result.getData().getProductOrCatalogNumber())
             print("Labeler identification code: " + result.getData().getLabelerIdentificationCode())
             print("Unit of measure ID: " + result.getData().getUnitOfMeasureID())
             \endcode
      """

      JAVA_CLASS_NAME = "com.aspose.mw.barcode.complexbarcode.MwHIBCLICPrimaryDataCodetext"

      def __init__(self):
            java_class_link = jpype.JClass(HIBCLICPrimaryDataCodetext.JAVA_CLASS_NAME)
            javaClass = java_class_link()
            self.data = None
            super().__init__(javaClass)

      @staticmethod
      def construct(java_class):
            obj = HIBCLICPrimaryDataCodetext()
            obj.setJavaClass(java_class)
            return obj

      def init(self):
            self.data = PrimaryData.construct(self.getJavaClass().getData())

      def getData(self):
            """!
            Identifies primary data.
            """
            return self.data

      def setData(self, value):
            """!
            Identifies primary data.
            """
            self.getJavaClass().setData(value.getJavaClass())
            self.data = value

      def getConstructedCodetext(self):
            """!
            Constructs codetext
            @return:Constructed codetext
            """
            return self.getJavaClass().getConstructedCodetext()

      def initFromString(self, constructedCodetext):
            """!
            Initializes instance from constructed codetext.
            @param: constructedCodetext:Constructed codetext.
            """
            self.getJavaClass().initFromString(constructedCodetext)

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified HIBCLICPrimaryDataCodetext value.
            @param: obj:An  HIBCLICPrimaryDataCodetext value to compare to this instance.
            @return:<b>True</b> if obj has the same value as this instance; otherwise, <b>False</b>.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return:A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

class HIBCLICSecondaryAndAdditionalDataCodetext(HIBCLICComplexCodetext):
      """!
         Class for encoding and decoding the text embedded in the HIBC LIC code which stores seconday data.

         This sample shows how to encode and decode HIBC LIC using HIBCLICSecondaryAndAdditionalDataCodetext.

               \code
                    complexCodetext = HIBCLICSecondaryAndAdditionalDataCodetext()
                    complexCodetext.setBarcodeType(EncodeTypes.HIBCQRLIC)
                    complexCodetext.setLinkCharacter('L')
                    complexCodetext.setData(SecondaryAndAdditionalData())
                    complexCodetext.getData().setExpiryDate(datetime.now())
                    complexCodetext.getData().setExpiryDateFormat(HIBCLICDateFormat.MMDDYY)
                    complexCodetext.getData().setQuantity(30)
                    complexCodetext.getData().setLotNumber("LOT123")
                    complexCodetext.getData().setSerialNumber("SERIAL123")
                    complexCodetext.getData().setDateOfManufacture(datetime.now())
                    generator = ComplexBarcodeGenerator(complexCodetext)
                    image = generator.generateBarCodeImage()
                    reader = Recognition.BarCodeReader(image, None, DecodeType.HIBCQRLIC)
                    reader.readBarCodes()
                    codetext = reader.getFoundBarCodes()[0].getCodeText()
                    result = ComplexCodetextReader.tryDecodeHIBCLIC(codetext)
                    if result is not None:
                        print("Expiry date: " + result.getData().getExpiryDate())
                        print("Quantity: " + result.getData().getQuantity())
                        print("Lot number: " + result.getData().getLotNumber())
                        print("Serial number: " + result.getData().getSerialNumber())
                        print("Date of manufacture: " + result.getData().getDateOfManufacture())
               \endcode
      """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.complexbarcode.MwHIBCLICSecondaryAndAdditionalDataCodetext"

      def __init__(self):
            java_class_link = jpype.JClass(HIBCLICSecondaryAndAdditionalDataCodetext.JAVA_CLASS_NAME)
            javaClass = java_class_link()
            self.data = None
            super().__init__(javaClass)

      @staticmethod
      def construct(java_class):
            obj = HIBCLICSecondaryAndAdditionalDataCodetext()
            obj.setJavaClass(java_class)
            return obj

      def getData(self):
            """!
            Identifies secodary and additional supplemental data.
            """
            return self.data

      def setData(self, value):
            """!
            Identifies secodary and additional supplemental data.
            """
            self.getJavaClass().setData(value.getJavaClass())
            self.data = value

      def getLinkCharacter(self):
            """!
            Identifies link character.
            """
            return self.getJavaClass().getLinkCharacter()

      def setLinkCharacter(self, value):
            """!
            Identifies link character.
            """
            self.getJavaClass().setLinkCharacter(value)

      def getConstructedCodetext(self):
            """!
            Constructs codetext
            @return:Constructed codetext
            """
            return self.getJavaClass().getConstructedCodetext()

      def initFromString(self, constructedCodetext):
            """!
            Initializes instance from constructed codetext.
            @param: constructedCodetext:Constructed codetext.
            """
            self.getJavaClass().initFromString(constructedCodetext)

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified HIBCLICSecondaryAndAdditionalDataCodetext value.
            @param: obj:An HIBCLICSecondaryAndAdditionalDataCodetext value to compare to this instance.
            @return: <b>True</b> if obj has the same value as this instance; otherwise, <b>false</b>.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return:A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def init(self):
            self.data = SecondaryAndAdditionalData.construct(self.getJavaClass().getData())

class HIBCPASCodetext(IComplexCodetext):
      """!
       Class for encoding and decoding the text embedded in the HIBC PAS code.
       This sample shows how to encode and decode HIBC PAS using HIBCPASCodetext.
        \code
        complexCodetext = ComplexBarcode.HIBCPASCodetext()
        complexCodetext.setDataLocation(ComplexBarcode.HIBCPASDataLocation.PATIENT)
        complexCodetext.addRecord(ComplexBarcode.HIBCPASDataType.LABELER_IDENTIFICATION_CODE, "A123")
        complexCodetext.addRecord(ComplexBarcode.HIBCPASDataType.MANUFACTURER_SERIAL_NUMBER, "SERIAL123")
        complexCodetext.setBarcodeType(EncodeTypes.HIBC_DATA_MATRIX_PAS)
        generator = ComplexBarcodeGenerator(complexCodetext)
        reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, DecodeType.HIBC_DATA_MATRIX_PAS)
        reader.readBarCodes()
        codetext = reader.getFoundBarCodes()[0].getCodeText()
        if codetext is not None:
            readCodetext = ComplexCodetextReader.tryDecodeHIBCPAS(codetext)
            print("Data location: " + readCodetext.getDataLocation())
            print("Data type: " + readCodetext.getRecords()[0].getDataType())
            print("Data: " + readCodetext.getRecords()[0].getData())
            print("Data type: " + readCodetext.getRecords()[1].getDataType())
            print("Data: " + readCodetext.getRecords()[1].getData())
        \endcode
       """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.complexbarcode.MwHIBCPASCodetext"

      def __init__(self):
            """!
            HIBCPASRecord constructor
            """
            java_class_link = jpype.JClass(HIBCPASCodetext.JAVA_CLASS_NAME)
            javaClass = java_class_link()
            super().__init__(javaClass)

      @staticmethod
      def construct(javaClass):
            obj = HIBCPASCodetext()
            obj.setJavaClass(javaClass)
            return obj

      def init(self):
            pass

      def setBarcodeType(self, value):
            """!
            Gets or sets barcode type. HIBC PAS codetext can be encoded using HIBCCode39PAS, HIBCCode128PAS, HIBCAztec:PAS, HIBCDataMatrixPAS and HIBCQRPAS encode types.
            Default value: HIBCCode39PAS.
            @return:Barcode type.
            """
            self.getJavaClass().setBarcodeType(value.value)

      def getDataLocation(self):
            """!
            Identifies data location.
            """
            return HIBCPASDataLocation(self.getJavaClass().getDataLocation())

      def setDataLocation(self, value):
            """!
            Identifies data location.
            """
            self.getJavaClass().setDataLocation(value.value)

      def getRecords(self):
            """!
            Gets records list
            @return:List of records
            """
            _array = []
            mwRecordsList = self.getJavaClass().getRecords()
            listSize = mwRecordsList.size()
            for i in range(listSize):
                  mwhibcpasRecord = mwRecordsList.get(i)
                  _array.append(HIBCPASRecord.construct(mwhibcpasRecord))
            return _array

      def addRecord(self, dataType, data):
            """!
            Adds new record
            @param: dataType:Type of data
            @param: data:Data string
            """
            self.getJavaClass().addRecord(dataType.value, data)

      def addHIBCPASRecord(self, record):
            """!
            Adds new record
            @param: record: record Record to be added
            """
            self.getJavaClass().addRecord(record.getJavaClass())

      def clear(self):
            """!
            Clears records list
            """
            self.getJavaClass().clear()

      def getBarcodeType(self):
            """!
            Gets barcode type.
            @return:Barcode type.
            """
            return self.getJavaClass().getBarcodeType()

      def getConstructedCodetext(self):
            """!
            Constructs codetext
            @return:Constructed codetext
            """
            return self.getJavaClass().getConstructedCodetext()

      def initFromString(self, constructedCodetext):
            """!
            Initializes instance from constructed codetext.
            @param: constructedCodetext:Constructed codetext.
            """
            self.getJavaClass().initFromString(constructedCodetext)

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified HIBCPASCodetext value.
            @param: obj:An HIBCPASCodetext value to compare to this instance.
            @return:<b>True</b> if obj has the same value as this instance; otherwise, <b>False</b>.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return:A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

class HIBCPASRecord(Assist.BaseJavaClass):
      """!
      Class for storing HIBC PAS record.
      """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.complexbarcode.MwHIBCPASRecord"

      def __init__(self, dataType, data):
            """!
            HIBCPASRecord constructor
            @param: dataType:Type of data.
            @param: data:Data string.
            """
            java_class_link = jpype.JClass(HIBCPASRecord.JAVA_CLASS_NAME)
            javaClass = java_class_link(dataType.value, data)
            super().__init__(javaClass)

      @staticmethod
      def construct(javaClass):
            obj = HIBCPASRecord(ComplexBarcode.HIBCPASDataType.LABELER_IDENTIFICATION_CODE,"")
            obj.setJavaClass(javaClass)
            return obj

      def init(self):
            pass

      def getDataType(self):
            """!
            Identifies data type.
            """
            return HIBCPASDataType(self.getJavaClass().getDataType())

      def setDataType(self, value):
            """!
            Identifies data type.
            """
            self.getJavaClass().setDataType(value)

      def getData(self):
            """!
            Identifies data.
            """
            return self.getJavaClass().getData()

      def setData(self, value):
            """!
            Identifies data.
            """
            self.getJavaClass().setData(value)

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified HIBCPASDataType value.
            @param: obj:An HIBCPASDataType value to compare to this instance.
            @return: <b>True</b> if obj has the same value as this instance; otherwise, <b>False</b>.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return:A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

class PrimaryData(Assist.BaseJavaClass):
      """!
      Class for storing HIBC LIC primary data.
      """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.complexbarcode.MwPrimaryData"

      def __init__(self):
            java_class_link = jpype.JClass(PrimaryData.JAVA_CLASS_NAME)
            javaClass = java_class_link()
            super().__init__(javaClass)

      @staticmethod
      def construct(java_class):
            obj = PrimaryData()
            obj.setJavaClass(java_class)
            return obj

      def getLabelerIdentificationCode(self):
            """!
            Identifies date of labeler identification code.
            Labeler identification code must be 4 symbols alphanumeric string, with first character always being alphabetic.
            """
            return self.getJavaClass().getLabelerIdentificationCode()

      def setLabelerIdentificationCode(self, value):
            """!
            Identifies date of labeler identification code.
            Labeler identification code must be 4 symbols alphanumeric string, with first character always being alphabetic.
            """
            self.getJavaClass().setLabelerIdentificationCode(value)

      def getProductOrCatalogNumber(self):
            """!
            Identifies product or catalog number. Product or catalog number must be alphanumeric string up to 18 sybmols length.
            """
            return self.getJavaClass().getProductOrCatalogNumber()

      def setProductOrCatalogNumber(self, value):
            """!
            Identifies product or catalog number. Product or catalog number must be alphanumeric string up to 18 sybmols length.
            """
            self.getJavaClass().setProductOrCatalogNumber(value)

      def getUnitOfMeasureID(self):
            """!
            Identifies unit of measure ID. Unit of measure ID must be integer value from 0 to 9.
            """
            return self.getJavaClass().getUnitOfMeasureID()

      def setUnitOfMeasureID(self, value):
            """!
            Identifies unit of measure ID. Unit of measure ID must be integer value from 0 to 9.
            """
            self.getJavaClass().setUnitOfMeasureID(value)

      def toString(self):
            """!
            Converts data to string format according HIBC LIC specification.
            @return:Formatted string.
            """
            return self.getJavaClass().toString()

      def parseFromString(self, primaryDataCodetext):
            """!
            Instantiates primary data from string format according HIBC LIC specification.
            @param: primaryDataCodetext:Formatted string.
            """
            self.getJavaClass().parseFromString(primaryDataCodetext)

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified PrimaryData value.
            @param: obj:An PrimaryData value to compare to this instance.
            @return: <b>True</b> if obj has the same value as this instance; otherwise,  <b>False</b>.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return:A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def init(self):
            pass

class SecondaryAndAdditionalData(Assist.BaseJavaClass):
      """!
      Class for storing HIBC LIC secondary and additional data.
      """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.complexbarcode.MwSecondaryAndAdditionalData"

      def __init__(self):
            java_class_link = jpype.JClass(SecondaryAndAdditionalData.JAVA_CLASS_NAME)
            javaClass = java_class_link()
            super().__init__(javaClass)

      @staticmethod
      def construct(java_class):
            obj = SecondaryAndAdditionalData()
            obj.setJavaClass(java_class)
            return obj

      def getExpiryDateFormat(self):
            """!
            Identifies expiry date format.
            """
            return HIBCLICDateFormat(self.getJavaClass().getExpiryDateFormat())

      def setExpiryDateFormat(self, value):
            """!
            Identifies expiry date format.
            """
            self.getJavaClass().setExpiryDateFormat(value.value)

      def getExpiryDate(self):
            """!
            Identifies expiry date. Will be used if ExpiryDateFormat is not set to None.
            """
            return datetime.fromtimestamp(int(str(self.getJavaClass().getExpiryDate())))

      def setExpiryDate(self, value):
            """!
            Identifies expiry date. Will be used if ExpiryDateFormat is not set to None.
            """
            self.getJavaClass().setExpiryDate(str(int(time.mktime(value.timetuple()))))

      def getLotNumber(self):
            """!
            Identifies lot or batch number. Lot/batch number must be alphanumeric string with up to 18 sybmols length.
            """
            return self.getJavaClass().getLotNumber()

      def setLotNumber(self, value):
            """!
            Identifies lot or batch number. Lot/batch number must be alphanumeric string with up to 18 sybmols length.
            """
            if value is None:
                  value = "null"
            self.getJavaClass().setLotNumber(value)

      def getSerialNumber(self):
            """!
            Identifies serial number. Serial number must be alphanumeric string up to 18 sybmols length.
            """
            return self.getJavaClass().getSerialNumber()

      def setSerialNumber(self, value):
            """!
            Identifies serial number. Serial number must be alphanumeric string up to 18 sybmols length.
            """
            if value is None:
                  value = "null"
            self.getJavaClass().setSerialNumber(value)

      def getDateOfManufacture(self):
            """!
            Identifies date of manufacture.
            Date of manufacture can be set to DateTime.MinValue in order not to use this field.
            Default value: DateTime.MinValue
            """
            return datetime.fromtimestamp(int(str(self.getJavaClass().getDateOfManufacture())))

      def setDateOfManufacture(self, value):
            """!
            Identifies date of manufacture.
            Date of manufacture can be set to DateTime.MinValue in order not to use this field.
            Default value: DateTime.MinValue
            """
            self.getJavaClass().setDateOfManufacture(str(int(time.mktime(value.timetuple()))))

      def getQuantity(self):
            """!
            Identifies quantity, must be integer value from 0 to 500.
            Quantity can be set to -1 in order not to use this field.
            Default value: -1
            """
            return self.getJavaClass().getQuantity()

      def setQuantity(self, value):
            """!
            Identifies quantity, must be integer value from 0 to 500.
            Quantity can be set to -1 in order not to use this field.
            Default value: -1
            """
            self.getJavaClass().setQuantity(value)

      def toString(self):
            """!
            Converts data to string format according HIBC LIC specification.
            @return:Formatted string.
            """
            return self.getJavaClass().toString()

      def parseFromString(self, secondaryDataCodetext):
            """!
            Instantiates secondary and additional supplemental data from string format according HIBC LIC specification.
            @param: secondaryDataCodetext:Formatted string.
            """
            self.getJavaClass().parseFromString(secondaryDataCodetext)

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified  SecondaryAndAdditionalData value.
            @param: obj:An SecondaryAndAdditionalData value to compare to this instance.
            @return: True if obj has the same value as this instance; otherwise, False.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return: A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def init(self):
            pass

class Mailmark2DType(Enum):
      """!
      2D Mailmark Type defines size of Data Matrix barcode
      """

      ## Auto determine
      AUTO = 0

      ## 24 x 24 modules
      TYPE_7 = 1

      ## 32 x 32 modules
      TYPE_9 = 2

      ## 16 x 48 modules
      TYPE_29 = 3

class HIBCLICDateFormat(Enum):
      """!
      Specifies the different types of date formats for HIBC LIC.
      """

      ## YYYYMMDD format. Will be encoded in additional supplemental data.
      YYYYMMDD = 0

      ## MMYY format.
      MMYY =  1

      ## MMDDYY format.
      MMDDYY = 2

      ## YYMMDD format.
      YYMMDD =  3

      ## YYMMDDHH format.
      YYMMDDHH = 4

      ## Julian date format.
      YYJJJ = 5

      ## Julian date format with hours.
      YYJJJHH = 6

      ## Do not encode expiry date.
      NONE = 7

class HIBCPASDataLocation(Enum):
      """!
      HIBC PAS data location types.
      """

      ## A - Patient
      PATIENT = 0

      ## B - Patient Care Record
      PATIENT_CARE_RECORD = 1

      ## C - Specimen Container
      SPECIMEN_CONTAINER = 2

      ## D - Direct Patient Image Item
      DIRECT_PATIENT_IMAGE_ITEM = 3
      """         
      """

      ## E - Business Record
      BUSINESS_RECORD = 4

      ## F - Medical Administration Record
      MEDICAL_ADMINISTRATION_RECORD = 5

      ## G - Library Reference Material
      LIBRARY_REFERENCE_MATERIAL = 6

      ## H - Devices and Materials
      DEVICES_AND_MATERIALS = 7

      ## I - Identification Card
      IDENTIFICATION_CARD = 8

      ## J - Product Container
      PRODUCT_CONTAINER = 9

      ## K - Asset data type
      ASSET = 10

      ## L - Surgical Instrument
      SURGICAL_INSTRUMENT = 11

      ## Z - User Defined
      USER_DEFINED = 25


class HIBCPASDataType(Enum):
      """!
      HIBC PAS record's data types.
      """
      ## A - Labeler Identification Code
      LABELER_IDENTIFICATION_CODE = 0

      ## B - Service Identification
      SERVICE_IDENTIFICATION = 1

      ## C - Patient Identification
      PATIENT_IDENTIFICATION = 2

      ## D - Specimen Identification
      SPECIMEN_IDENTIFICATION = 3

      ## E - Personnel Identification
      PERSONNEL_IDENTIFICATION = 4

      ## F - Administrable Product Identification
      ADMINISTRABLE_PRODUCT_IDENTIFICATION = 5

      ## G - Implantable Product Information
      IMPLANTABLE_PRODUCT_INFORMATION = 6

      ## H - Hospital Item Identification
      HOSPITAL_ITEM_IDENTIFICATION = 7

      ## I - Medical Procedure Identification
      MEDICAL_PROCEDURE_IDENTIFICATION = 8

      ## J - Reimbursement Category
      REIMBURSEMENT_CATEGORY = 9

      ## K - Blood Product Identification
      BLOOD_PRODUCT_IDENTIFICATION = 10

      ## L - Demographic Data
      DEMOGRAPHIC_DATA = 11

      ## M - DateTime in YYYDDDHHMMG format
      DATE_TIME = 12

      ## N - Asset Identification
      ASSET_IDENTIFICATION = 13

      ## O - Purchase Order Number
      PURCHASE_ORDER_NUMBER = 14

      ## P - Dietary Item Identification
      DIETARY_ITEM_IDENTIFICATION = 15

      ## Q - Manufacturer Serial Number
      MANUFACTURER_SERIAL_NUMBER = 16

      ## R - Library Materials Identification
      LIBRARY_MATERIALS_IDENTIFICATION = 17

      ## S - Business Control Number
      BUSINESS_CONTROL_NUMBER = 18

      ## T - Episode of Care Identification
      EPISODE_OF_CARE_IDENTIFICATION = 19

      ## U - Health Industry Number
      HEALTH_INDUSTRY_NUMBER = 20

      ## V - Patient Visit ID
      PATIENT_VISIT_ID = 21

      ## X - XML Document
      XML_DOCUMENT = 22

      ## Z - User Defined
      USER_DEFINED = 25