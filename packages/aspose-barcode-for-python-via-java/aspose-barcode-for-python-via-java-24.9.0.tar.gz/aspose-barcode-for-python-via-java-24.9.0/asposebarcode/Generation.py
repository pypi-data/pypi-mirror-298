import time
from datetime import datetime

import jpype
from . import Assist
from enum import Enum
import base64
import io
from PIL import Image
import warnings

class BarcodeGenerator(Assist.BaseJavaClass):
      """!
     BarcodeGenerator for backend barcode images generation.

     Supported symbologies:

     1D:
         Codabar, Code11, Code128, Code39Standard, Code39Extended
         Code93Standard, Code93Extended, EAN13, EAN8, Interleaved2of5,
         MSI, Standard2of5, UPCA, UPCE, ISBN, GS1Code128, Postnet, Planet
         EAN14, SCC14, SSCC18, ITF14, SingaporePost ...

     2D:
         Aztec, DataMatrix, PDf417, QR code ...

      This sample shows how to create and save a barcode image.
      \code
        encode_type = Generation.EncodeTypes.CODE_128
		 generator = Generation.BarcodeGenerator(encode_type, None)
		 generator.setCodeText("123ABCDFVC", "UTF-8")
		 generator.save(self.image_path_to_save1,Generation.BarCodeImageFormat.PNG)
      \endcode
        """
      javaClassName = 'com.aspose.mw.barcode.generation.MwBarcodeGenerator'

      def __init__(self, encodeType, codeText):
            """!
            BarcodeGenerator constructor.
            @param args may take the following combinations of arguments:
            1) Barcode symbology type. Use EncodeTypes class to setup a symbology
            2) type EncodeTypes, Text to be encoded.
            \code
              barcodeGenerator = BarcodeGenerator(EncodeTypes.EAN_14, "332211")
            \endcode
            @throws BarCodeException
            """
            javaBarcodeGenerator = jpype.JClass(self.javaClassName)
            if not isinstance(encodeType, EncodeTypes):
                  raise Assist.BarCodeException("Waiting for EncodeTypes type, but got '" + type(encodeType).__name__ + "'")
            self.javaClass = javaBarcodeGenerator(encodeType.value, codeText)
            self.parameters = None
            super().__init__(self.javaClass)

      @staticmethod
      def construct(javaClass):
            barcodeGenerator = BarcodeGenerator(None, None)
            barcodeGenerator.setJavaClass(javaClass)
            return barcodeGenerator

      def init(self):
            self.parameters = BaseGenerationParameters(self.getJavaClass().getParameters())

      def getParameters(self):
            """! Generation parameters.
            @return BaseGenerationParameters """
            return self.parameters

      def getBarcodeType(self):
            """! Barcode symbology type. """
            return EncodeTypes(self.getJavaClass().getBarcodeType())

      def setBarcodeType(self, value):
            """! Barcode symbology type. """
            self.getJavaClass().setBarcodeType(value.value)

      def generateBarCodeImage(self):
            """!  Generate the barcode image under current settings.
            This sample shows how to create and save a barcode image.
            \code
             generator = Generation.BarcodeGenerator(Generation.EncodeTypes.CODE_128,"123ABCDEFG")
		     pillowImage = generator.generateBarCodeImage()
		     pillowImage.save(self.image_path_to_save)
            @return: Pillow Image object of barcode image
            \endcode
            """
            try:
                  bytes = base64.b64decode(str(self.javaClass.generateBarCodeImage(BarCodeImageFormat.PNG.value)))
                  buf = io.BytesIO(bytes)
                  bitmap = Image.open(buf)
                  return bitmap
            except Exception as e:
                  raise Assist.BarCodeException(e)

      def save(self, imagePath, imageFormat):
            """!
            Save barcode image to specific file in specific format.
            @param imagePath Path to save to.
            @param imageFormat Optional format override. If omitted, the format to use is determined from the filename extension. If a file object was used instead of a filename, this parameter should always be used.
            \code
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.CODE_128, "123ABCDEFG")
              generator.save(self.image_path_to_save3, Generation.BarCodeImageFormat.PNG)
            \endcode
            """
            bytes = bytearray(base64.b64decode(str(self.javaClass.generateBarCodeImage(imageFormat.value))))
            file = open(imagePath, "wb")
            file.write(bytes)
            file.close()

      def getCodeText(self):
            """!Text to be encoded."""
            return self.getJavaClass().getCodeText()

      def setCodeText(self, value, encoding):
            """!
            Encodes codetext with byte order mark (BOM) using specified encoding.
            @param value: codeText CodeText string | Bytes of codetext
            @param encoding: Applied encoding
            """
            if isinstance(value, list):
                  byte_data = bytes(value)
                  base64_bytes = base64.b64encode(byte_data)
                  self.getJavaClass().setCodeBytes(base64_bytes)
            else:
                  self.getJavaClass().setCodeText(value, encoding)

      def exportToXml(self, filePath):
            """!
            Exports BarCode properties to the xml-stream specified
            @param filePath: The xml-stream
            @return: Whether or not export completed successfully. Returns <b>True</b> in case of success; <b>False</b> Otherwise
            """
            try:
                  xmlData = self.getJavaClass().exportToXml()
                  isSaved = xmlData != None
                  if isSaved:
                        text_file = open(filePath, "w")
                        text_file.write(xmlData)
                        text_file.close()
                  return isSaved
            except Exception as ex:
                  raise Assist.BarCodeException(ex)

      @staticmethod
      def importFromXml(resource):
            """!
            Imports BarCode properties from the xml-file specified and creates BarcodeGenerator instance.
            @param: resource: The name of the file
            @return: instance
            """
            try:
                  xmlData = BarcodeGenerator.loadFileBase64String(resource)
                  offset = 6
                  xmlData = xmlData.substr(offset)
                  javaBarcodeGenerator = jpype.JClass(BarcodeGenerator.javaClassName)
                  return BarcodeGenerator.construct(javaBarcodeGenerator).importFromXml(xmlData)
            except Exception as ex:
                  raise Assist.BarCodeException(ex)

      @staticmethod
      def loadFileBase64String(filepath):
            with open(filepath, "r") as image_file:
                  return image_file.read().replace('\n','')

class BarcodeParameters(Assist.BaseJavaClass):
      """! Barcode generation parameters."""

      def __init__(self, javaClass):
            """!  """
            self.xDimension = None
            self.barHeight = None
            self.codeTextParameters = None
            self.postal = None
            self.australianPost = None
            self.codablock = None
            self.dataBar = None
            self.gs1CompositeBar = None
            self.dataMatrix = None
            self.code16K = None
            self.itf = None
            self.qr = None
            self.pdf417 = None
            self.maxiCode = None
            self.aztec = None
            self.code128 = None
            self.codabar = None
            self.coupon = None
            self.hanXin = None
            self.supplement = None
            self.dotCode = None
            self.padding = None
            self.patchCode = None
            self.barWidthReduction = None
            super().__init__(javaClass)


      def init(self):
            """! initialize properties """
            self.xDimension = Unit(self.getJavaClass().getXDimension())
            self.barHeight = Unit(self.getJavaClass().getBarHeight())
            self.codeTextParameters = CodetextParameters(self.getJavaClass().getCodeTextParameters())
            self.postal = PostalParameters(self.getJavaClass().getPostal())
            self.australianPost = AustralianPostParameters(self.getJavaClass().getAustralianPost())
            self.codablock = CodablockParameters(self.getJavaClass().getCodablock())
            self.dataBar = DataBarParameters(self.getJavaClass().getDataBar())
            self.gs1CompositeBar = GS1CompositeBarParameters(self.getJavaClass().getGS1CompositeBar())
            self.dataMatrix = DataMatrixParameters(self.getJavaClass().getDataMatrix())
            self.code16K = Code16KParameters(self.getJavaClass().getCode16K())
            self.itf = ITFParameters(self.getJavaClass().getITF())
            self.qr = QrParameters(self.getJavaClass().getQR())
            self.pdf417 = Pdf417Parameters(self.getJavaClass().getPdf417())
            self.maxiCode = MaxiCodeParameters(self.getJavaClass().getMaxiCode())
            self.aztec = AztecParameters(self.getJavaClass().getAztec())
            self.code128 = Code128Parameters(self.getJavaClass().getCode128())
            self.codabar = CodabarParameters(self.getJavaClass().getCodabar())
            self.coupon = CouponParameters(self.getJavaClass().getCoupon())
            self.hanXin = HanXinParameters(self.getJavaClass().getHanXin())
            self.supplement = SupplementParameters(self.getJavaClass().getSupplement())
            self.dotCode = DotCodeParameters(self.getJavaClass().getDotCode())
            self.padding = Padding(self.getJavaClass().getPadding())
            self.patchCode = PatchCodeParameters(self.getJavaClass().getPatchCode())
            self.barWidthReduction = Unit(self.getJavaClass().getBarWidthReduction())

      def getXDimension(self):
            """!
             x-dimension is the smallest width of the unit of BarCode bars or spaces.
             Increase this will increase the whole barcode image width.
            Ignored if AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.  """
            return self.xDimension

      def setXDimension(self, value):
            """!  x-dimension is the smallest width of the unit of BarCode bars or spaces.
            Increase this will increase the whole barcode image width.
            Ignored if AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
            @throws BarCodeException """
            self.getJavaClass().setXDimension(value.getJavaClass())
            self.xDimension = value

      def getBarWidthReduction(self):
            """!  Get bars reduction value that is used to compensate ink spread while printing.
             @return Unit value of BarWidthReduction"""
            try:
                  return self.barWidthReduction
            except Exception as ex:
                  barcode_exception = Assist.BarCodeException(ex)
                  raise barcode_exception

      def setBarWidthReduction(self, value):
            """! Sets bars reduction value that is used to compensate ink spread while printing. """
            try:
                  self.getJavaClass().setBarWidthReduction(value.getJavaClass())
                  self.barWidthReduction = value
            except Exception as ex:
                  barcode_exception = Assist.BarCodeException(ex)
                  raise barcode_exception

      def getBarHeight(self):
            """!
            Height of 1D barcodes' bars in Unit value.
            Ignored if AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
            @throws BarCodeException"""
            return self.barHeight

      def setBarHeight(self, value):
            """!
             Height of 1D barcodes' bars in Unit value.
             Ignored if AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
            @throws BarCodeException
            """
            self.getJavaClass().setBarHeight(value.getJavaClass())
            self.barHeight = value

      def getBarColor(self):
            """!
            Bars color, representation of an RGB tuple.
            Default value: 0
            """
            intColor = self.getJavaClass().getBarColor()
            Blue = intColor & 255
            Green = (intColor >> 8) & 255
            Red = (intColor >> 16) & 255
            rgbColor = (Red, Green, Blue)
            return rgbColor

      def setBarColor(self, value):
            """!
            Bars color, representation of an RGB tuple.
            Default value: 0.
            """
            rgb = 65536 * value[0] + 256 * value[1] + value[2]
            self.getJavaClass().setBarColor(rgb)

      def getPadding(self):
            """!
            Barcode paddings.
            Default value: 5pt 5pt 5pt 5pt.
            """
            return self.padding

      def setPadding(self, value):
            """!
            Barcode paddings.
           Default value: 5pt 5pt 5pt 5pt.
            """
            self.getJavaClass().setPadding(value.getJavaClass())
            self.padding = value

      def getChecksumAlwaysShow(self):
            """!
            Always display checksum digit in the human readable text for Code128 and GS1Code128 barcodes.
            """
            return self.getJavaClass().getChecksumAlwaysShow()

      def setChecksumAlwaysShow(self, value):
            """!
            Always display checksum digit in the human readable text for Code128 and GS1Code128 barcodes.
            """
            self.getJavaClass().setChecksumAlwaysShow(value)

      def isChecksumEnabled(self):
            """!
            Enable checksum during generation 1D barcodes.
            Default is treated as Yes for symbology which must contain checksum, as No where checksum only possible.
            Checksum is possible: Code39 Standard/Extended, Standard2of5, Interleaved2of5, Matrix2of5, ItalianPost25, DeutschePostIdentcode, DeutschePostLeitcode, VIN, Codabar
            Checksum always used: Rest symbology
            """
            return EnableChecksum(self.getJavaClass().isChecksumEnabled())

      def setChecksumEnabled(self, value):
            """!
           Enable checksum during generation 1D barcodes.
           Default is treated as Yes for symbology which must contain checksum, as No where checksum only possible.
           Checksum is possible: Code39 Standard/Extended, Standard2of5, Interleaved2of5, Matrix2of5, ItalianPost25, DeutschePostIdentcode, DeutschePostLeitcode, VIN, Codabar
           Checksum always used: Rest symbology
            """
            self.getJavaClass().setChecksumEnabled(value.value)

      def getEnableEscape(self):
            """!
            Indicates whether explains the character "\" as an escape character in CodeText property. Used for Pdf417, DataMatrix, Code128 only
            If the EnableEscape is True, "\" will be explained as a special escape character. Otherwise, "\" acts as normal characters.
            Aspose.BarCode supports inputing decimal ascii code and mnemonic for ASCII control-code characters. For example, \013 and \\CR stands for CR.
            """
            return self.getJavaClass().getEnableEscape()

      def setEnableEscape(self, value):
            """!
            Indicates whether explains the character "\" as an escape character in CodeText property. Used for Pdf417, DataMatrix, Code128 only
            If the EnableEscape is True, "\" will be explained as a special escape character. Otherwise, "\" acts as normal characters.
            <hr>Aspose.BarCode supports inputing decimal ascii code and mnemonic for ASCII control-code characters. For example, \013 and \\CR stands for CR.
            """
            self.getJavaClass().setEnableEscape(value)

      def getWideNarrowRatio(self):
            """!
            Wide bars to Narrow bars ratio.
            Default value: 3, that is, wide bars are 3 times as wide as narrow bars.
            Used for ITF, PZN, PharmaCode, Standard2of5, Interleaved2of5, Matrix2of5, ItalianPost25, IATA2of5, VIN, DeutschePost, OPC, Code32, DataLogic2of5, PatchCode, Code39Extended, Code39Standard
            The WideNarrowRatio parameter value is less than or equal to 0.
            """
            return float(self.getJavaClass().getWideNarrowRatio())

      def setWideNarrowRatio(self, value):
            """!
            Wide bars to Narrow bars ratio.
            Default value: 3, that is, wide bars are 3 times as wide as narrow bars.
            Used for ITF, PZN, PharmaCode, Standard2of5, Interleaved2of5, Matrix2of5, ItalianPost25, IATA2of5, VIN, DeutschePost, OPC, Code32, DataLogic2of5, PatchCode, Code39Extended, Code39Standard
            The WideNarrowRatio parameter value is less than or equal to 0.
            """
            self.getJavaClass().setWideNarrowRatio(value)

      def getCodeTextParameters(self):
            """!
            Codetext parameters.
            """
            return self.codeTextParameters

      def getFilledBars(self):
            """!
            Gets a value indicating whether bars filled.
            Only for 1D barcodes.
            Default value: True.
            """
            return self.getJavaClass().getFilledBars()

      def setFilledBars(self, value):
            """!
            Sets a value indicating whether bars filled.
            Only for 1D barcodes.
            Default value: True.
            """
            self.getJavaClass().setFilledBars(value)

      def getPostal(self):
            """!
            Postal parameters. Used for Postnet, Planet.
            """
            return self.postal

      def getPatchCode(self):
            """!
            PatchCode parameters.
            """
            return self.patchCode

      def getAustralianPost(self):
            """!
            AustralianPost barcode parameters.
            """
            return self.australianPost

      def getDataBar(self):
            """!
            Databar parameters.
            """
            return self.dataBar


      def getGS1CompositeBar(self):
            """!
            GS1 Composite Bar parameters.

             This sample shows how to create and save a GS1 Composite Bar image.
             Note that 1D codetext and 2D codetext are separated by symbol '/'
             \code
              codetext = "(01)03212345678906|(21)A1B2C3D4E5F6G7H8"
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_COMPOSITE_BAR, codetext)
              generator.getParameters().getBarcode().getGS1CompositeBar().setLinearComponentType(Generation.EncodeTypes.GS_1_CODE_128)
              generator.getParameters().getBarcode().getGS1CompositeBar().setTwoDComponentType(Generation.TwoDComponentType.CC_A)
              # Aspect ratio of 2D component
              generator.getParameters().getBarcode().getPdf417().setAspectRatio(3)
              # X-Dimension of 1D and 2D components
              generator.getParameters().getBarcode().getXDimension().setPixels(3)
              # Height of 1D component
              generator.getParameters().getBarcode().getBarHeight().setPixels(100)
              generator.save(self.image_path_to_save4, Generation.BarCodeImageFormat.PNG)
             \endcode
              @return GS1CompositeBarParameters GS1 Composite Bar parameters.
            """
            return self.gs1CompositeBar

      def setGS1CompositeBar(self, value):
            """!
            GS1 Composite Bar parameters.
            This sample shows how to create and save a GS1 Composite Bar image.
            Note that 1D codetext and 2D codetext are separated by symbol '/'
            \code
             \code
              codetext = "(01)03212345678906|(21)A1B2C3D4E5F6G7H8"
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_COMPOSITE_BAR, codetext)
              generator.getParameters().getBarcode().getGS1CompositeBar().setLinearComponentType(Generation.EncodeTypes.GS_1_CODE_128)
              generator.getParameters().getBarcode().getGS1CompositeBar().setTwoDComponentType(Generation.TwoDComponentType.CC_A)
              # Aspect ratio of 2D component
              generator.getParameters().getBarcode().getPdf417().setAspectRatio(3)
              # X-Dimension of 1D and 2D components
              generator.getParameters().getBarcode().getXDimension().setPixels(3)
              # Height of 1D component
              generator.getParameters().getBarcode().getBarHeight().setPixels(100)
              generator.save(self.image_path_to_save4, Generation.BarCodeImageFormat.PNG)
             \endcode
             \endcode
            """
            self.gs1CompositeBar = value
            self.getJavaClass().setGS1CompositeBar(value.getJavaClass())

      def getCodablock(self):
            """!
            Codablock parameters.
            """
            return self.codablock

      def getDataMatrix(self):
            """!
            DataMatrix parameters.
            """
            return self.dataMatrix

      def getCode16K(self):
            """!
            Code16K parameters.
            """
            return self.code16K

      def getDotCode(self):
            """!
            DotCode parameters.
            """
            return self.dotCode

      def getITF(self):
            """!
            ITF parameters.
            """
            return self.itf

      def getPdf417(self):
            """!
            PDF417 parameters.
            """
            return self.pdf417

      def getQR(self):
            """!
            QR parameters.
            """
            return self.qr

      def getSupplement(self):
            """!
            Supplement parameters. Used for Interleaved2of5, Standard2of5, EAN13, EAN8, UPCA, UPCE, ISBN, ISSN, ISMN.
            """
            return self.supplement

      def getMaxiCode(self):
            """!
            MaxiCode parameters.
            """
            return self.maxiCode

      def getCode128(self):
            """!
            Code128 parameters.
            """
            return self.code128

      def getAztec(self):
            """!
            Aztec parameters.
            """
            return self.aztec

      def getCodabar(self):
            """!
            Codabar parameters.
            """
            return self.codabar

      def getCoupon(self):
            """!
            Coupon parameters. Used for UpcaGs1DatabarCoupon, UpcaGs1Code128Coupon.
            """
            return self.coupon

      def getHanXin(self):
            """!
            HanXin parameters.
            """
            return self.hanXin


class BaseGenerationParameters(Assist.BaseJavaClass):
      """!
      Barcode image generation parameters.
      """

      def __init__(self, javaClass):
            self.captionAbove = None
            self.captionBelow = None
            self.barcodeParameters = None
            self.borderParameters = None
            self.imageWidth = None
            self.imageHeight = None
            super().__init__(javaClass)
            self.init()

      def init(self):
            self.captionAbove = CaptionParameters(self.getJavaClass().getCaptionAbove())
            self.captionBelow = CaptionParameters(self.getJavaClass().getCaptionBelow())
            self.barcodeParameters = BarcodeParameters(self.getJavaClass().getBarcode())
            self.borderParameters = BorderParameters(self.getJavaClass().getBorder())
            self.imageWidth = Unit(self.getJavaClass().getImageWidth())
            self.imageHeight = Unit(self.getJavaClass().getImageHeight())
            self.image = ImageParameters(self.getJavaClass().getImage())

      def getUseAntiAlias(self):
            """
            Gets a value indicating whether is used anti-aliasing mode to render image
            """
            return self.getJavaClass().getUseAntiAlias()

      def setUseAntiAlias(self, value):
            """
            Sets a value indicating whether is used anti-aliasing mode to render image
            """
            self.getJavaClass().setUseAntiAlias(value)

      def getBackColor(self):
            """!
            Background color of the barcode image, representation of an RGB tuple.
            Default value: 0
            """
            intColor = self.getJavaClass().getBackColor()
            Blue = intColor & 255
            Green = (intColor >> 8) & 255
            Red = (intColor >> 16) & 255
            rgbColor = (Red, Green, Blue)
            return rgbColor

      def setBackColor(self, value):
            """!
            Background color of the barcode image, representation of an RGB tuple.
            Default value: 0
            """
            rgb = 65536 * value[0] + 256 * value[1] + value[2]
            if rgb > 16777215:
                  raise Exception("Invalid color")
            self.getJavaClass().setBackColor(rgb)

      def getResolution(self):
            """!
            Gets the resolution of the BarCode image.
            One value for both dimensions.
            Default value: 96 dpi.
            The Resolution parameter value is less than or equal to 0.
            """
            return float(self.getJavaClass().getResolution())

      def getImage(self):
            """
            Image parameters. See ImageParameters
            :return:
            """
            return self.image

      def setResolution(self, value):
            """!
            Sets the resolution of the BarCode image.
            One value for both dimensions.
            Default value: 96 dpi.
            The Resolution parameter value is less than or equal to 0.
            """
            self.getJavaClass().setResolution(value)

      def getRotationAngle(self):
            """!
            BarCode image rotation angle, measured in degree, e.g. RotationAngle = 0 or RotationAngle = 360 means no rotation.
            If RotationAngle NOT equal to 90, 180, 270 or 0, it may increase the difficulty for the scanner to read the image.
            Default value: 0.
            This sample shows how to create and save a BarCode image.
            \code
            generator = Generation.BarcodeGenerator(Generation.EncodeTypes.DATA_MATRIX,"123456789")
		     generator.getParameters().setRotationAngle(7)
		     generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
            \endcode
            """
            return float(self.getJavaClass().getRotationAngle())

      def setRotationAngle(self, value):
            """!
            BarCode image rotation angle, measured in degree, e.g. RotationAngle = 0 or RotationAngle = 360 means no rotation.
            If RotationAngle NOT equal to 90, 180, 270 or 0, it may increase the difficulty for the scanner to read the image.
            Default value: 0.
            \code
            This sample shows how to create and save a BarCode image.
            generator = Generation.BarcodeGenerator(Generation.EncodeTypes.DATA_MATRIX,"123456789")
		     generator.getParameters().setRotationAngle(7)
		     generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
            \endcode
            """
            self.getJavaClass().setRotationAngle(value)

      def getCaptionAbove(self):
            """!
            Caption Above the BarCode image. See CaptionParameters.
            """
            return self.captionAbove

      def setCaptionAbove(self, value):
            """!
            Caption Above the BarCode image. See CaptionParameters.
            """
            self.getJavaClass().setCaptionAbove(value.getJavaClass())
            self.captionAbove.updateCaption(value)

      def getCaptionBelow(self):
            """!
            Caption Below the BarCode image. See CaptionParameters.
            """
            return self.captionBelow

      def setCaptionBelow(self, value):
            """!
            Caption Below the BarCode image. See CaptionParameters.
            """
            self.getJavaClass().setCaptionBelow(value.getJavaClass())
            self.captionBelow.updateCaption(value)

      def getAutoSizeMode(self):
            """!
            Specifies the different types of automatic sizing modes.
            Default value: AutoSizeMode.NONE.
            """
            return AutoSizeMode(self.getJavaClass().getAutoSizeMode())

      def setAutoSizeMode(self, value):
            """!
            Specifies the different types of automatic sizing modes.
            Default value: AutoSizeMode.NONE.
            """
            self.getJavaClass().setAutoSizeMode(value.value)

      def getImageHeight(self):
            """!
            BarCode image height when AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
            """
            return self.imageHeight

      def setImageHeight(self, value):
            """!
            BarCode image height when AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
            """
            self.getJavaClass().setImageHeight(value.getJavaClass())
            self.imageHeight = value

      def getImageWidth(self):
            """!
            BarCode image width when AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
            """
            return self.imageWidth

      def setImageWidth(self, value):
            """!
            BarCode image width when AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
            """
            self.getJavaClass().setImageWidth(value.getJavaClass())
            self.imageWidth = value

      def getBarcode(self):
            """!
            Gets the BarcodeParameters that contains all barcode properties.
            """
            return self.barcodeParameters

      def setBarcode(self, value):
            """!
            Gets the BarcodeParameters that contains all barcode properties.
            """
            self.getJavaClass().setBarcode(value.getJavaClass())
            self.barcodeParameters = value

      def getBorder(self):
            """!
            Gets the BorderParameters that contains all configuration properties for barcode border.
            """
            return self.borderParameters


class BorderParameters(Assist.BaseJavaClass):
      """!
      Barcode image border parameters
      """

      def __init__(self, javaClass):
            self.width = None
            super().__init__(javaClass)

      def init(self):
            self.width = Unit(self.getJavaClass().getWidth())

      def getVisible(self):
            """!
            Border visibility. If false than parameter Width is always ignored (0).
            Default value: false.
            """
            return self.getJavaClass().getVisible()

      def setVisible(self, value):
            """!
            Border visibility. If false than parameter Width is always ignored (0).
            Default value: false.
            """
            self.getJavaClass().setVisible(value)

      def getWidth(self):
            """!
            Border width.
            Default value: 0.
            Ignored if Visible is set to false.
            """
            return self.width

      def setWidth(self, value):
            """!
            Border width.
            Default value: 0.
            Ignored if Visible is set to false.
            """
            self.getJavaClass().setWidth(value.getJavaClass())
            self.width = value

      def toString(self):
            """!
            Returns a human-readable string representation of this BorderParameters.
            @return A string that represents this BorderParameters.
            """
            return self.getJavaClass().toString()

      def getDashStyle(self):
            """!
            Border dash style.
            Default value: BorderDashStyle.SOLID.
            """
            return BorderDashStyle(self.getJavaClass().getDashStyle())

      def setDashStyle(self, value):
            """!
            Border dash style.
            Default value: BorderDashStyle.SOLID.
            """
            self.getJavaClass().setDashStyle(value.value)

      def getColor(self):
            """!
            Border color, representation of an RGB tuple.
            Default value: 0
            """
            intColor = self.getJavaClass().getColor()
            Blue = intColor & 255
            Green = (intColor >> 8) & 255
            Red = (intColor >> 16) & 255
            rgbColor = (Red, Green, Blue)
            return rgbColor

      def setColor(self, value):
            """!
            Border color, representation of an RGB tuple.
            Default value: 0
            """
            rgb = 65536 * value[0] + 256 * value[1] + value[2]
            self.getJavaClass().setColor(rgb)


class CaptionParameters(Assist.BaseJavaClass):
      """!
      Caption parameters.
      """

      def __init__(self, javaClass):
            self.font = None
            self.padding = None
            super().__init__(javaClass)
            self.init()

      def init(self):
            self.padding = Padding(self.getJavaClass().getPadding())
            self.font = FontUnit(self.getJavaClass().getFont())

      def getText(self):
            """!
            Caption text.
            Default value: empty string.
            """
            return self.getJavaClass().getText()

      def setText(self, value):
            """!
            Caption text.
            Default value: empty string.
            """
            self.getJavaClass().setText(value)

      def getFont(self):
            """!
            Caption font.
            Default value: Arial 8pt regular.
            """
            return self.font

      def getVisible(self):
            """!
            Caption text visibility.
            Default value: false.
            """
            return self.getJavaClass().getVisible()

      def setVisible(self, value):
            """!
            Caption text visibility.
            Default value: false.
            """
            self.getJavaClass().setVisible(value)

      def getTextColor(self):
            """!
            Caption text color, representation of an RGB tuple.
            Default value (0,0,0).
            """
            intColor = self.getJavaClass().getTextColor()
            Blue = intColor & 255
            Green = (intColor >> 8) & 255
            Red = (intColor >> 16) & 255
            rgbColor = (Red, Green, Blue)
            return rgbColor

      def setTextColor(self, value):
            """!
            Caption text color, representation of an RGB tuple.
            Default value (0,0,0).
            """
            rgb = 65536 * value[0] + 256 * value[1] + value[2]
            self.getJavaClass().setTextColor(rgb)

      def getPadding(self):
            """!
            Captions paddings.
            Default value for CaptionAbove: 5pt 5pt 0 5pt.
            Default value for CaptionBelow: 0 5pt 5pt 5pt.
            """
            return self.padding

      def setPadding(self, value):
            """!
            Captions paddings.
            Default value for CaptionAbove: 5pt 5pt 0 5pt.
            Default value for CaptionBelow: 0 5pt 5pt 5pt.
            """
            self.getJavaClass().setPadding(value.getJavaClass())
            self.padding = value

      def getAlignment(self):
            """!
            Caption test horizontal alignment.
            Default valueAlignment.Center.
            """
            return TextAlignment(self.getJavaClass().getAlignment())

      def setAlignment(self, value):
            """!
            Caption test horizontal alignment.
            Default valueAlignment.Center.
            """
            self.getJavaClass().setAlignment(value.value)

      def getNoWrap(self):
            """!
            Specify word wraps (line breaks) within text.
            @return bool
            """
            return self.getJavaClass().getNoWrap()

      def setNoWrap(self, value):
            """!
            Specify word wraps (line breaks) within text.
            """
            self.getJavaClass().setNoWrap(value)


class Unit(Assist.BaseJavaClass):
      """!
      Specifies the size value in different units (Pixel, Inches, etc.).

      This sample shows how to create and save a BarCode image.
        \code
         generator = Generation.BarcodeGenerator(Generation.EncodeTypes.CODE_128,"123456789")
		  generator.getParameters().getBarcode().getBarHeight().setMillimeters(10)
		  generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
        \endcode
      """

      def __init__(self, source):
            super().__init__(Unit.initUnit(source))
            self.init()

      @staticmethod
      def initUnit(source):
            if isinstance(source, Unit):
                  return source.getNativeObject()
            return source

      def init(self):
            pass

      def getPixels(self):
            """!
            Gets size value in pixels.
            """
            return self.getJavaClass().getPixels()

      def setPixels(self, value):
            """!
            Sets size value in pixels.
            """
            self.getJavaClass().setPixels(value)

      def getInches(self):
            """!
            Gets size value in inches.
            """
            return self.getJavaClass().getInches()

      def setInches(self, value):
            """!
            Sets size value in inches.
            """
            self.getJavaClass().setInches(value)

      def getMillimeters(self):
            """!
            Gets size value in millimeters.
            """
            return self.getJavaClass().getMillimeters()

      def setMillimeters(self, value):
            """!
            Sets size value in millimeters.
            """
            self.getJavaClass().setMillimeters(value)

      def getPoint(self):
            """!
            Gets size value in point.
            """
            return self.getJavaClass().getPoint()

      def setPoint(self, value):
            """!
            Sets size value in point.
            """
            self.getJavaClass().setPoint(value)

      def getDocument(self):
            """!
            Gets size value in document units.
            """
            return self.getJavaClass().getDocument()

      def setDocument(self, value):
            """!
            Sets size value in document units.
            """
            self.getJavaClass().setDocument(value)

      def toString(self):
            """!
            Returns a human-readable string representation of this Unit.
            @return A string that represents this Unit.
            """
            return self.getJavaClass().toString()

      def equals(self, obj):
            """!
            Determines whether this instance and a specified object,
            which must also be a Unit object, have the same value.
            @param obj The Unit to compare to this instance.
            @return True if obj is a Unit and its value is the same as this instance
            otherwise, false. If obj is None, the method returns false.
            """
            return self.getJavaClass().equals(obj.getJavaClass())


class Padding(Assist.BaseJavaClass):
      """!
      Paddings parameters.
      """
      def __init__(self, javaClass):
            self.top = None
            self.bottom = None
            self.right = None
            self.left = None
            super().__init__(javaClass)
            self.init()

      def init(self):
            self.top = Unit(self.getJavaClass().getTop())
            self.bottom = Unit(self.getJavaClass().getBottom())
            self.right = Unit(self.getJavaClass().getRight())
            self.left = Unit(self.getJavaClass().getLeft())

      def getTop(self):
            """!
            Top padding.
            """
            return self.top

      def setTop(self, value):
            """!
            Top padding.
            """
            self.getJavaClass().setTop(value.getJavaClass())
            self.top = value

      def getBottom(self):
            """!
            Bottom padding.
            """
            return self.bottom

      def setBottom(self, value):
            """!
            Bottom padding.
            """
            self.getJavaClass().setBottom(value.getJavaClass())
            self.bottom = value

      def getRight(self):
            """!
            Right padding.
            """
            return self.right

      def setRight(self, value):
            """!
            Right padding.
            """
            self.getJavaClass().setRight(value.getJavaClass())
            self.right = value

      def getLeft(self):
            """!
            Left padding.
            """
            return self.left

      def setLeft(self, value):
            """!
            Left padding.
            """
            self.getJavaClass().setLeft(value.getJavaClass())
            self.left = value

      def toString(self):
            """!
            Returns a human-readable string representation of this Padding.
            @return A string that represents this Padding.
            """
            return self.getJavaClass().toString()


class CodetextParameters(Assist.BaseJavaClass):
      """!
      Codetext parameters.
      """

      def __init__(self, javaClass):
            self.font = None
            self.space = None
            super().__init__(javaClass)
            self.init()

      def init(self):
            self.font = FontUnit(self.getJavaClass().getFont())
            self.space = Unit(self.getJavaClass().getSpace())

      def getTwoDDisplayText(self):
            """!
            Text that will be displayed instead of codetext in 2D barcodes.
            Used for: Aztec, Pdf417, DataMatrix, QR, MaxiCode, DotCode
            """
            return self.getJavaClass().getTwoDDisplayText()

      def setTwoDDisplayText(self, value):
            """!
            Text that will be displayed instead of codetext in 2D barcodes.
            Used for: Aztec, Pdf417, DataMatrix, QR, MaxiCode, DotCode
            """
            self.getJavaClass().setTwoDDisplayText(value)

      def getFontMode(self):
            """!
            Specify FontMode. If FontMode is set to Auto, font size will be calculated automatically based on xDimension value.
            It is recommended to use FontMode.AUTO especially in AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
            Default value: FontMode.AUTO.
            """
            return FontMode(int(self.getJavaClass().getFontMode()))

      def setFontMode(self, value):
            """!
            Specify FontMode. If FontMode is set to Auto, font size will be calculated automatically based on xDimension value.
            It is recommended to use FontMode.AUTO especially in AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
            Default value: FontMode.AUTO.
            """
            self.getJavaClass().setFontMode(value.value)

      def getFont(self):
            """!
            Specify the displaying CodeText's font.
            Default value: Arial 5pt regular.
            Ignored if FontMode is set to FontMode.AUTO.
            """
            return self.font

      def setFont(self, value):
            """!
            Specify the displaying CodeText's font.
            Default value: Arial 5pt regular.
            Ignored if FontMode is set to FontMode.AUTO.
            """
            self.getJavaClass().setFont(value.getJavaClass())
            self.font = value

      def getSpace(self):
            """!
            Space between the CodeText and the BarCode in Unit value.
            Default value: 2pt.
            Ignored for EAN8, EAN13, UPCE, UPCA, ISBN, ISMN, ISSN, UpcaGs1DatabarCoupon.
            """
            return self.space

      def setSpace(self, value):
            """!
            Space between the CodeText and the BarCode in Unit value.
            Default value: 2pt.
            Ignored for EAN8, EAN13, UPCE, UPCA, ISBN, ISMN, ISSN, UpcaGs1DatabarCoupon.
            """
            self.getJavaClass().setSpace(value.getJavaClass())
            self.space = value

      def getAlignment(self):
            """!
            Gets the alignment of the code text.
            Default value: TextAlignment.CENTER.
            """
            return TextAlignment(self.getJavaClass().getAlignment())

      def setAlignment(self, value):
            """!
            Sets the alignment of the code text.
            Default value: TextAlignment.CENTER.
            """
            self.getJavaClass().setAlignment(value.value)

      def getColor(self):
            """!
            Specify the displaying CodeText's Color, representation of an RGB tuple.
            Default value (0,0,0).
            """
            intColor = self.getJavaClass().getColor()
            Blue = intColor & 255
            Green = (intColor >> 8) & 255
            Red = (intColor >> 16) & 255
            rgbColor = (Red, Green, Blue)
            return rgbColor

      def setColor(self, value):
            """!
            Specify the displaying CodeText's Color, representation of an RGB tuple.
            Default value (0,0,0).
            """
            rgb = 65536 * value[0] + 256 * value[1] + value[2]
            self.getJavaClass().setColor(rgb)

      def getLocation(self):
            """!
            Specify the displaying CodeText Location, set to CodeLocation.NONE to hide CodeText.
            Default value:  CodeLocation.NONE.
            """
            return CodeLocation(self.getJavaClass().getLocation())

      def setLocation(self, value):
            """!
            Specify the displaying CodeText Location, set to  CodeLocation.NONE to hide CodeText.
            Default value:  CodeLocation.NONE.
            """
            self.getJavaClass().setLocation(value.value)

      def getNoWrap(self):
            """!
            Specify word wraps (line breaks) within text.
            @return bool
            """
            return self.getJavaClass().getNoWrap()

      def setNoWrap(self, value):
            """!
            Specify word wraps (line breaks) within text.
            """
            self.getJavaClass().setNoWrap(value)

      def toString(self):
            """!
            Returns a human-readable string representation of this CodetextParameters.
            @return A string that represents this CodetextParameters.
            """
            return self.getJavaClass().toString()


class PostalParameters(Assist.BaseJavaClass):
      """!
      Postal parameters. Used for Postnet, Planet.
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.postalShortBarHeight = None
            self.init()

      def init(self):
            self.postalShortBarHeight = Unit(self.getJavaClass().getPostalShortBarHeight())

      def getPostalShortBarHeight(self):
            """!
            Short bar's height of Postal barcodes.
            """
            return self.postalShortBarHeight

      def setPostalShortBarHeight(self, value):
            """!
            Short bar's height of Postal barcodes.
            """
            self.getJavaClass().setPostalShortBarHeight(value.getJavaClass())
            self.postalShortBarHeight = value

      def toString(self):
            """!
            Returns a human-readable string representation of this PostalParameters.
            @return A string that represents this PostalParameters.
            """
            return self.getJavaClass().toString()


class AustralianPostParameters(Assist.BaseJavaClass):
      """!
      AustralianPost barcode parameters.
      """

      def __init__(self, javaClass):
            self.australianPostShortBarHeight = None
            super().__init__(javaClass)

      def init(self):
            self.australianPostShortBarHeight = Unit(self.getJavaClass().getAustralianPostShortBarHeight())

      def getAustralianPostShortBarHeight(self):
            """!
            Short bar's height of AustralianPost barcode.
            """
            return self.australianPostShortBarHeight

      def setAustralianPostShortBarHeight(self, value):
            """!
            Short bar's height of AustralianPost barcode.
            """
            self.getJavaClass().setAustralianPostShortBarHeight(value.getJavaClass())
            self.australianPostShortBarHeight = value

      def getAustralianPostEncodingTable(self):
            """!
            Interpreting type for the Customer Information of AustralianPost, default to CustomerInformationInterpretingType.Other
            """
            return CustomerInformationInterpretingType(self.getJavaClass().getAustralianPostEncodingTable())

      def setAustralianPostEncodingTable(self, value):
            """!
            Interpreting type for the Customer Information of AustralianPost, default to CustomerInformationInterpretingType.Other"
            """
            self.getJavaClass().setAustralianPostEncodingTable(value.value)

      def toString(self):
            """!
            Returns a human-readable string representation of this AustralianPostParameters.
            @return A string that represents this AustralianPostParameters.
            """
            return self.getJavaClass().toString()


class CodablockParameters(Assist.BaseJavaClass):
      """!
      Codablock parameters.
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            pass

      def getColumns(self):
            """!
            Columns count.
            """
            return self.getJavaClass().getColumns()

      def setColumns(self, value):
            """!
            Columns count.
            """
            self.getJavaClass().setColumns(value)

      def getRows(self):
            """!
            Rows count.
            """
            return self.getJavaClass().getRows()

      def setRows(self, value):
            """!
            Rows count.
            """
            self.getJavaClass().setRows(value)

      def getAspectRatio(self):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            return self.getJavaClass().getAspectRatio()

      def setAspectRatio(self, value):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            self.getJavaClass().setAspectRatio(value)

      def toString(self):
            """!
            Returns a human-readable string representation of this CodablockParameters.
            @return A string that represents this CodablockParameters.
            """
            return self.getJavaClass().toString()


class DataBarParameters(Assist.BaseJavaClass):
      """!
      Databar parameters.
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            pass

      def is2DCompositeComponent(self):
            """!
            Enables flag of 2D composite component with DataBar barcode
            """
            return self.getJavaClass().is2DCompositeComponent()

      def set2DCompositeComponent(self, value):
            """!
            Enables flag of 2D composite component with DataBar barcode
            """
            self.getJavaClass().set2DCompositeComponent(value)

      def isAllowOnlyGS1Encoding(self):
            """!
            If this flag is set, it allows only GS1 encoding standard for Databar barcode types
            """
            return self.getJavaClass().isAllowOnlyGS1Encoding()

      def setAllowOnlyGS1Encoding(self, value):
            """!
            If this flag is set, it allows only GS1 encoding standard for Databar barcode types
            """
            self.getJavaClass().setAllowOnlyGS1Encoding(value)

      def getColumns(self):
            """!
            Columns count.
            """
            return self.getJavaClass().getColumns()

      def setColumns(self, value):
            """!
            Columns count.
            """
            self.getJavaClass().setColumns(value)

      def getRows(self):
            """!
            Rows count.
            """
            return self.getJavaClass().getRows()

      def setRows(self, value):
            """!
            Rows count.
            """
            self.getJavaClass().setRows(value)

      def getAspectRatio(self):
            """!
            Height/Width ratio of 2D BarCode module.
            Used for DataBar stacked.
            """
            return self.getJavaClass().getAspectRatio()

      def setAspectRatio(self, value):
            """!
            Height/Width ratio of 2D BarCode module.
            Used for DataBar stacked.
            """
            self.getJavaClass().setAspectRatio(value)

      def toString(self):
            """!
            Returns a human-readable string representation of this DataBarParameters.
            @return A string that represents this DataBarParameters.
            """
            return self.getJavaClass().toString()


class DataMatrixParameters(Assist.BaseJavaClass):
      """!
      DataMatrix parameters.
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def getDataMatrixVersion(self):
            """!
            Gets Datamatrix symbol size.
            @return: Datamatrix symbol size.
            """
            return DataMatrixVersion(self.getJavaClass().getDataMatrixVersion())

      def setDataMatrixVersion(self, value):
            """!
            Sets Datamatrix symbol size.
            @param value: Datamatrix symbol size.
            """
            self.getJavaClass().setDataMatrixVersion(value.value)

      def init(self):
            pass

      def getDataMatrixEcc(self):
            """!
            Gets a Datamatrix ECC type.
            Default value: DataMatrixEccType.ECC_200.
            """
            return DataMatrixEccType(self.getJavaClass().getDataMatrixEcc())

      def setDataMatrixEcc(self, value):
            """!
            Sets a Datamatrix ECC type.
            Default value: DataMatrixEccType.ECC_200.
            """
            self.getJavaClass().setDataMatrixEcc(value.value)

      def getDataMatrixEncodeMode(self):
            """!
            Encode mode of Datamatrix barcode.
            Default value: DataMatrixEncodeMode.AUTO.
            """
            return DataMatrixEncodeMode(self.getJavaClass().getDataMatrixEncodeMode())

      def setDataMatrixEncodeMode(self, value):
            """!
            Encode mode of Datamatrix barcode.
            Default value: DataMatrixEncodeMode.AUTO.
            """
            self.getJavaClass().setDataMatrixEncodeMode(value.value)

      def getStructuredAppendBarcodeId(self):
            """!
            Barcode ID for Structured Append mode of Datamatrix barcode.
            Default value: 0
            """
            return self.getJavaClass().getStructuredAppendBarcodeId()

      def setStructuredAppendBarcodeId(self, value):
            """!
            Barcode ID for Structured Append mode of Datamatrix barcode.
            Default value: 0
            """
            self.getJavaClass().setStructuredAppendBarcodeId(value)

      def getStructuredAppendBarcodesCount(self):
            """!
            Barcodes count for Structured Append mode of Datamatrix barcode.
            Default value: 0
            """
            return self.getJavaClass().getStructuredAppendBarcodesCount()

      def setStructuredAppendBarcodesCount(self, value):
            """!
            Barcodes count for Structured Append mode of Datamatrix barcode.
            Default value: 0
            """
            self.getJavaClass().setStructuredAppendBarcodesCount(value)

      def getStructuredAppendFileId(self):
            """!
            File ID for Structured Append mode of Datamatrix barcode.
            Default value: 0
            """
            return self.getJavaClass().getStructuredAppendFileId()

      def setStructuredAppendFileId(self, value):
            """!
            File ID for Structured Append mode of Datamatrix barcode.
            Default value: 0
            """
            self.getJavaClass().setStructuredAppendFileId(value)

      def isReaderProgramming(self):
            """!
            Used to instruct the reader to interpret the data contained within the symbol
            """
            return self.getJavaClass().isReaderProgramming()

      def setReaderProgramming(self, value):
            """!
            Used to instruct the reader to interpret the data contained within the symbol
            """
            self.getJavaClass().setReaderProgramming(value)

      def getMacroCharacters(self):
            """!
            ISO/IEC 16022
            5.2.4.7 Macro characters
            11.3 Protocol for Macro characters in the first position (ECC 200 only)
            Macro Characters 05 and 06 values are used to obtain more compact encoding in special modes.
            Can be used only with DataMatrixEccType.Ecc200 or DataMatrixEccType.EccAuto.
            Cannot be used with EncodeTypes.GS_1_DATA_MATRIX
            Default value: MacroCharacter.NONE.
            """
            return MacroCharacter(self.getJavaClass().getMacroCharacters())

      def setMacroCharacters(self, value):
            """!
            ISO/IEC 16022
             5.2.4.7 Macro characters
             11.3 Protocol for Macro characters in the first position (ECC 200 only)
             Macro Characters 05 and 06 values are used to obtain more compact encoding in special modes.
             Can be used only with DataMatrixEccType.Ecc200 or DataMatrixEccType.EccAuto.
             Cannot be used with EncodeTypes.GS_1_DATA_MATRIX
             Default value: MacroCharacter.NONE.
            """
            self.getJavaClass().setMacroCharacters(value.value)

      def getColumns(self):
            """!
            Columns count.
            """
            return self.getJavaClass().getColumns()

      def setColumns(self, value):
            """!
            Columns count.
            """
            self.getJavaClass().setColumns(value)

      def getRows(self):
            """!
            Rows count.
            """
            return self.getJavaClass().getRows()

      def setRows(self, value):
            """!
            Rows count.
            """
            self.getJavaClass().setRows(value)

      def getAspectRatio(self):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            return self.getJavaClass().getAspectRatio()

      def setAspectRatio(self, value):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            self.getJavaClass().setAspectRatio(value)

      def getECIEncoding(self):
            """!
            Gets ECI encoding. Used when DataMatrixEncodeMode is Auto.
            Default value: ISO-8859-1
            """
            return self.getJavaClass().getECIEncoding()

      def setECIEncoding(self, value):
            """!
            Gets ECI encoding. Used when DataMatrixEncodeMode is Auto.
            Default value: ISO-8859-1
            """
            self.getJavaClass().setECIEncoding(value.value)

      def toString(self):
            """!
            Returns a human-readable string representation of this DataMatrixParameters.
            @return presentation of this DataMatrixParameters.
            """
            return self.getJavaClass().toString()


class PatchCodeParameters(Assist.BaseJavaClass):
      """!
      PatchCode parameters.
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            pass

      def getExtraBarcodeText(self):
            """!
            Specifies codetext for an extra QR barcode, when PatchCode is generated in page mode.
            """
            return self.getJavaClass().getExtraBarcodeText()

      def setExtraBarcodeText(self, value):
            """!
            Specifies codetext for an extra QR barcode, when PatchCode is generated in page mode.
            """
            self.getJavaClass().setExtraBarcodeText(value)

      def getPatchFormat(self):
            """!
            PatchCode format. Choose PatchOnly to generate single PatchCode. Use page format to generate Patch page with PatchCodes as borders.
            Default value: PatchFormat.PATCH_ONLY
            @return PatchFormat
            """
            return PatchFormat(self.getJavaClass().getPatchFormat())

      def setPatchFormat(self, value):
            """!
            PatchCode format. Choose PatchOnly to generate single PatchCode. Use page format to generate Patch page with PatchCodes as borders.
            Default value: PatchFormat.PATCH_ONLY
            """
            self.getJavaClass().setPatchFormat(int(value.value))

      def toString(self):
            """!
            Returns a human-readable string representation of this PatchCodeParameters.
            @return A string that represents this PatchCodeParameters.
            """
            return self.getJavaClass().toString()


class Code16KParameters(Assist.BaseJavaClass):
      """!
      Code16K parameters.
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            pass

      def getAspectRatio(self):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            return self.getJavaClass().getAspectRatio()

      def setAspectRatio(self, value):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            self.getJavaClass().setAspectRatio(value)

      def getQuietZoneLeftCoef(self):
            """!
            Size of the left quiet zone in xDimension.
            Default value: 10, meaning if xDimension = 2px than left quiet zone will be 20px.
            """
            return self.getJavaClass().getQuietZoneLeftCoef()

      def setQuietZoneLeftCoef(self, value):
            """!
            Size of the left quiet zone in xDimension.
            Default value: 10, meaning if xDimension = 2px than left quiet zone will be 20px.
            """
            self.getJavaClass().setQuietZoneLeftCoef(value)

      def getQuietZoneRightCoef(self):
            """!
            Size of the right quiet zone in xDimension.
            Default value: 1, meaning if xDimension = 2px than right quiet zone will be 2px.
            """
            return self.getJavaClass().getQuietZoneRightCoef()

      def setQuietZoneRightCoef(self, value):
            """!
            Size of the right quiet zone in xDimension.
            Default value: 1, meaning if xDimension = 2px than right quiet zone will be 2px.
            """
            self.getJavaClass().setQuietZoneRightCoef(value)

      def toString(self):
            """!
            Returns a human-readable string representation of this Code16KParameters.
            @return A string that represents this Code16KParameters.
            """
            return self.getJavaClass().toString()


class DotCodeParameters(Assist.BaseJavaClass):
      """!
      DotCode parameters.
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            pass

      def getDotCodeEncodeMode(self):
            """
            Identifies DotCode encode mode.
            Default value: Auto.
            """
            return DotCodeEncodeMode(self.getJavaClass().getDotCodeEncodeMode())

      def setDotCodeEncodeMode(self, value):
            """!
            Identifies DotCode encode mode.
            Default value: Auto.
            """
            self.getJavaClass().setDotCodeEncodeMode(value.value)

      def isReaderInitialization(self):
            """!
            Indicates whether code is used for instruct reader to interpret the following data as instructions for initialization or reprogramming of the bar code reader.
            Default value is false.
            """
            return self.getJavaClass().isReaderInitialization()

      def setReaderInitialization(self, value):
            """!
            Indicates whether code is used for instruct reader to interpret the following data as instructions for initialization or reprogramming of the bar code reader.
            Default value is false.
            """
            self.getJavaClass().setReaderInitialization(value)

      def getDotCodeStructuredAppendModeBarcodeId(self):
            """!
            Identifies the ID of the DotCode structured append mode barcode. ID starts from 1 and must be less or equal to barcodes count. Default value is -1.
            """
            return self.getJavaClass().getDotCodeStructuredAppendModeBarcodeId()

      def setDotCodeStructuredAppendModeBarcodeId(self, value):
            """!
            Identifies the ID of the DotCode structured append mode barcode. ID starts from 1 and must be less or equal to barcodes count. Default value is -1.
            """
            self.getJavaClass().setDotCodeStructuredAppendModeBarcodeId(value)

      def getDotCodeStructuredAppendModeBarcodesCount(self):
            """!
            Identifies DotCode structured append mode barcodes count. Default value is -1. Count must be a value from 1 to 35.
            """
            return self.getJavaClass().getDotCodeStructuredAppendModeBarcodesCount()

      def setDotCodeStructuredAppendModeBarcodesCount(self, value):
            """!
            Identifies DotCode structured append mode barcodes count. Default value is -1. Count must be a value from 1 to 35.
            """
            self.getJavaClass().setDotCodeStructuredAppendModeBarcodesCount(value)

      def getECIEncoding(self):
            """!
            Identifies ECI encoding. Used when DotCodeEncodeMode is Auto.
            Default value: ISO-8859-1
            """
            return ECIEncodings(self.getJavaClass().getECIEncoding())

      def setECIEncoding(self, value):
            """!
            Identifies ECI encoding. Used when DotCodeEncodeMode is Auto.
            Default value: ISO-8859-1
            """
            self.getJavaClass().setECIEncoding(value.value)

      def getRows(self):
            """!
            Identifies rows count. Sum of the number of rows plus the number of columns of a DotCode symbol must be odd. Number of rows must be at least 5.
            Default value: -1
            """
            return self.getJavaClass().getRows()

      def setRows(self, value):
            """!
            Identifies rows count. Sum of the number of rows plus the number of columns of a DotCode symbol must be odd. Number of rows must be at least 5.
            Default value: -1
            """
            self.getJavaClass().setRows(value)

      def getColumns(self):
            """!
            Identifies columns count. Sum of the number of rows plus the number of columns of a DotCode symbol must be odd. Number of columns must be at least 5.
            Default value: -1
            """
            return self.getJavaClass().getColumns()

      def setColumns(self, value):
            """!
            Identifies columns count. Sum of the number of rows plus the number of columns of a DotCode symbol must be odd. Number of columns must be at least 5.
            Default value: -1
            """
            self.getJavaClass().setColumns(value)

      def getAspectRatio(self):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            return self.getJavaClass().getAspectRatio()

      def setAspectRatio(self, value):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            self.getJavaClass().setAspectRatio(value)

      def toString(self):
            """!
            Returns a human-readable string representation of this DotCodeParameters.
            @return A string that represents this DotCodeParameters.
            """
            return self.getJavaClass().toString()


class GS1CompositeBarParameters(Assist.BaseJavaClass):
      """!
       GS1 Composite bar parameters.
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            pass

      def getLinearComponentType(self):
            """!
            Linear component type
            """
            return EncodeTypes(self.getJavaClass().getLinearComponentType())

      def setLinearComponentType(self, value):
            """!
            Linear component type
            """
            self.getJavaClass().setLinearComponentType(value.value)

      def getTwoDComponentType(self):
            """!
            2D component type
            """
            return TwoDComponentType(int(self.getJavaClass().getTwoDComponentType()))

      def setTwoDComponentType(self, value):
            """!
            2D component type
            """
            self.getJavaClass().setTwoDComponentType(value.value)

      def isAllowOnlyGS1Encoding(self):
            """!
            If this flag is set, it allows only GS1 encoding standard for GS1CompositeBar 2D Component
            """
            return self.getJavaClass().isAllowOnlyGS1Encoding()

      def setAllowOnlyGS1Encoding(self, value):
            """!
            If this flag is set, it allows only GS1 encoding standard for GS1CompositeBar 2D Component
            """
            self.getJavaClass().setAllowOnlyGS1Encoding(value)

      def toString(self):
            """!
            Returns a human-readable string representation of this DataBarParameters
            @return A string that represents this DataBarParameters
            """
            return self.getJavaClass().toString()

class ITFParameters(Assist.BaseJavaClass):
      """!
      ITF parameters.
      """

      def __init__(self, javaClass):
            self.itfBorderThickness = None
            super().__init__(javaClass)
            self.init()

      def init(self):
            self.itfBorderThickness = Unit(self.getJavaClass().getItfBorderThickness())

      def getItfBorderThickness(self):
            """!
            Gets an ITF border (bearer bar) thickness in Unit value.
            Default value: 12pt.
            """
            return self.itfBorderThickness

      def setItfBorderThickness(self, value):
            """!
            Sets an ITF border (bearer bar) thickness in Unit value.
            Default value: 12pt.
            """
            self.getJavaClass().setItfBorderThickness(value.getJavaClass())
            self.itfBorderThickness = value

      def getItfBorderType(self):
            """!
            Border type of ITF barcode.
            Default value: ITF14BorderType.BAR.
            """
            return ITF14BorderType(int(self.getJavaClass().getItfBorderType()))

      def setItfBorderType(self, value):
            """!
            Border type of ITF barcode.
            Default value: ITF14BorderType.BAR.
            """
            self.getJavaClass().setItfBorderType(value.value)

      def getQuietZoneCoef(self):
            """!
            Size of the quiet zones in xDimension.
            Default value: 10, meaning if xDimension = 2px than quiet zones will be 20px.
            @exception IllegalArgumentException
            The QuietZoneCoef parameter value is less than 10.
            """
            return self.getJavaClass().getQuietZoneCoef()

      def setQuietZoneCoef(self, value):
            """!
            Size of the quiet zones in xDimension.
            Default value: 10, meaning if xDimension = 2px than quiet zones will be 20px.
            @exception IllegalArgumentException
            The QuietZoneCoef parameter value is less than 10.
            """
            self.getJavaClass().setQuietZoneCoef(value)

      def toString(self):
            """!
            Returns a human-readable string representation of this ITFParameters.
            @return A string that represents this ITFParameters.
            """
            return self.getJavaClass().toString()


class QrParameters(Assist.BaseJavaClass):
      """!
      QR parameters.
      """

      def __init__(self, javaClass):
            self.structuredAppend = None
            super().__init__(javaClass)
            self.init()

      def init(self):
            self.structuredAppend = QrStructuredAppendParameters(self.getJavaClass().getStructuredAppend())

      def getStructuredAppend(self):
            """!
            QR structured append parameters.
            """
            return self.structuredAppend

      def setStructuredAppend(self, value):
            """!
            QR structured append parameters.
            """
            self.structuredAppend = value
            self.getJavaClass().setStructuredAppend(value.getJavaClass())

      def getQrECIEncoding(self):
            """!
            Extended Channel Interpretation Identifiers. It is used to tell the barcode reader details
            about the used references for encoding the data in the symbol.
            Current implementation consists all well known charset encodings.
            """
            return ECIEncodings(self.getJavaClass().getQrECIEncoding())

      def setQrECIEncoding(self, value):
            """!
            Extended Channel Interpretation Identifiers. It is used to tell the barcode reader details
            about the used references for encoding the data in the symbol.
            Current implementation consists all well known charset encodings.
            """
            self.getJavaClass().setQrECIEncoding(value.value)

      def getQrEncodeMode(self):
            """!
            QR symbology type of BarCode's encoding mode.
            Default value: QREncodeMode.AUTO.
            """
            return QREncodeMode(int(self.getJavaClass().getQrEncodeMode()))

      def setQrEncodeMode(self, value):
            """!
            QR symbology type of BarCode's encoding mode.
            Default value: QREncodeMode.AUTO.
            """
            self.getJavaClass().setQrEncodeMode(value.value)

      def getQrEncodeType(self):
            """!
            QR / MicroQR selector mode. Select ForceQR for standard QR symbols, Auto for MicroQR.
            """
            return QREncodeType(int(self.getJavaClass().getQrEncodeType()))

      def setQrEncodeType(self, value):
            """!
            QR / MicroQR selector mode. Select ForceQR for standard QR symbols, Auto for MicroQR.
            """
            self.getJavaClass().setQrEncodeType(value.value)

      def getQrErrorLevel(self):
            """!
            Level of Reed-Solomon error correction for QR barcode.
            From low to high: LEVEL_L, LEVEL_M, LEVEL_Q, LEVEL_H. see QRErrorLevel.
            """
            return QRErrorLevel(int(self.getJavaClass().getQrErrorLevel()))

      def setQrErrorLevel(self, value):
            """!
            Level of Reed-Solomon error correction for QR barcode.
             From low to high: LEVEL_L, LEVEL_M, LEVEL_Q, LEVEL_H. see QRErrorLevel.
            """
            self.getJavaClass().setQrErrorLevel(value.value)

      def getQrVersion(self):
            """!
            Version of QR Code.
            From Version1 to Version40 for QR code and from M1 to M4 for MicroQr.
            Default value is QRVersion.AUTO.
            """
            return QRVersion(int(self.getJavaClass().getQrVersion()))

      def setQrVersion(self, value):
            """!
            Version of QR Code.
            From Version1 to Version40 for QR code and from M1 to M4 for MicroQr.
            Default value is QRVersion.AUTO.
            """
            self.getJavaClass().setQrVersion(value.value)

      def getMicroQRVersion(self):
            """!
            Version of MicroQR Code. From version M1 to version M4.
            Default value is MicroQRVersion.Auto.
            """
            return MicroQRVersion(self.getJavaClass().getMicroQRVersion())
            
      def setMicroQRVersion(self, value):
            """!
            Version of MicroQR Code. From version M1 to version M4.
            Default value is MicroQRVersion.Auto.
            """
            self.getJavaClass().setMicroQRVersion(value.value)

      def getRectMicroQrVersion(self):
            """!
            Version of RectMicroQR Code. From version R7x59 to version R17x139.
            Default value is RectMicroQRVersion.Auto
            """
            return RectMicroQRVersion(self.getJavaClass().getRectMicroQrVersion())

      def setRectMicroQrVersion(self, value):
            """!
            Version of RectMicroQR Code. From version R7x59 to version R17x139.
            Default value is RectMicroQRVersion.Auto.
            """
            self.getJavaClass().setRectMicroQrVersion(value.value)
      
      def getAspectRatio(self):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            return self.getJavaClass().getAspectRatio()

      def setAspectRatio(self, value):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            self.getJavaClass().setAspectRatio(value)

      def toString(self):
            """!
            Returns a human-readable string representation of this QrParameters.
            @return A string that represents this QrParameters.
            """
            return self.getJavaClass().toString()


class Pdf417Parameters(Assist.BaseJavaClass):
      """!
        PDF417 parameters. Contains PDF417, MacroPDF417, MicroPDF417 and GS1MicroPdf417 parameters.
        MacroPDF417 requires two fields: Pdf417MacroFileID and Pdf417MacroSegmentID. All other fields are optional.
        MicroPDF417 in Structured Append mode (same as MacroPDF417 mode) requires two fields: Pdf417MacroFileID and Pdf417MacroSegmentID. All other fields are optional.
        These samples show how to encode UCC/EAN-128 non Linked modes in GS1MicroPdf417
        \code
        # Encodes GS1 UCC/EAN-128 non Linked mode 905 with AI 01 (GTIN)
         generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_MICRO_PDF_417, "(01)12345678901231")
         reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.GS_1_MICRO_PDF_417)
         results = reader.readBarCodes()
         for result in results:
             print(f"\nBarCode Type: {result.getCodeTypeName()}")
             print(f"BarCode CodeText: {result.getCodeText()}")
        \endcode
        \code
        # Encodes GS1 UCC/EAN-128 non Linked modes 903, 904 with any AI
		  generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_MICRO_PDF_417, "(241)123456789012345(241)ABCD123456789012345")
		  reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.GS_1_MICRO_PDF_417)
		  results = reader.readBarCodes()
		  for result in results:
	       print(f"\nBarCode Type: {result.getCodeTypeName()}")
			print(f"BarCode CodeText: {result.getCodeText()}")
        \endcode
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            pass

      def getPdf417CompactionMode(self):
            """!
            Pdf417 symbology type of BarCode's compaction mode.
            Default value: Pdf417CompactionMode.AUTO.
            """
            warnings.warn("This property is obsolete and will be removed in future releases. Instead, use the Pdf417EncodeMode property.",DeprecationWarning,stacklevel=2)
            return Pdf417CompactionMode(self.getJavaClass().getPdf417CompactionMode())

      def setPdf417CompactionMode(self, value):
            """!
            Pdf417 symbology type of BarCode's compaction mode.
            Default value: Pdf417CompactionMode.AUTO.
            """
            warnings.warn("This property is obsolete and will be removed in future releases. Instead, use the Pdf417EncodeMode property.",DeprecationWarning,stacklevel=2)
            self.getJavaClass().setPdf417CompactionMode(value.value)


      def getPdf417EncodeMode(self):
            """!
            Identifies Pdf417 encode mode.
            Default value: Auto.
            """
            return self.getJavaClass().getPdf417EncodeMode()

      def setPdf417EncodeMode(self, pdf417EncodeMode):
            """!
            Identifies Pdf417 encode mode.
            Default value: Auto.
            """
            self.getJavaClass().setPdf417EncodeMode(pdf417EncodeMode)

      def getPdf417ErrorLevel(self):
            """!
            Gets Pdf417 symbology type of BarCode's error correction level
            ranging from level0 to level8, level0 means no error correction info,
            level8 means the best error correction which means a larger picture.
            """
            return Pdf417ErrorLevel(self.getJavaClass().getPdf417ErrorLevel())

      def setPdf417ErrorLevel(self, value):
            """!
            Sets Pdf417 symbology type of BarCode's error correction level
            ranging from level0 to level8, level0 means no error correction info,
            level8 means the best error correction which means a larger picture.
            """
            self.getJavaClass().setPdf417ErrorLevel(value.value)

      def getPdf417Truncate(self):
            """!
            Whether Pdf417 symbology type of BarCode is truncated (to reduce space).
            """
            return self.getJavaClass().getPdf417Truncate()

      def setPdf417Truncate(self, value):
            """!
            Whether Pdf417 symbology type of BarCode is truncated (to reduce space).
            """
            self.getJavaClass().setPdf417Truncate(value)

      def getColumns(self):
            """!
            Columns count.
            """
            return int(self.getJavaClass().getColumns())

      def setColumns(self, value):
            """!
            Columns count.
            """
            self.getJavaClass().setColumns(value)

      def getRows(self):
            """!
            Rows count.
            """
            return int(self.getJavaClass().getRows())

      def setRows(self, value):
            """!
            Rows count.
            """
            self.getJavaClass().setRows(value)

      def getAspectRatio(self):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            return self.getJavaClass().getAspectRatio()

      def setAspectRatio(self, value):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            self.getJavaClass().setAspectRatio(value)

      def getPdf417MacroFileID(self):
            """!
            Gets macro Pdf417 barcode's file ID.
            Used for MacroPdf417.
            """
            return self.getJavaClass().getPdf417MacroFileID()

      def setPdf417MacroFileID(self, value):
            """!
            Sets macro Pdf417 barcode's file ID.
            Used for MacroPdf417.
            """
            self.getJavaClass().setPdf417MacroFileID(value)

      def getPdf417MacroSegmentID(self):
            """!
            Gets macro Pdf417 barcode's segment ID, which starts from 0, to MacroSegmentsCount - 1.
            """
            return self.getJavaClass().getPdf417MacroSegmentID()

      def setPdf417MacroSegmentID(self, value):
            """!
            Sets macro Pdf417 barcode's segment ID, which starts from 0, to MacroSegmentsCount - 1.
            """
            self.getJavaClass().setPdf417MacroSegmentID(value)

      def getPdf417MacroSegmentsCount(self):
            """!
            Gets macro Pdf417 barcode segments count.
            """
            return self.getJavaClass().getPdf417MacroSegmentsCount()

      def setPdf417MacroSegmentsCount(self, value):
            """!
            Sets macro Pdf417 barcode segments count.
            """
            self.getJavaClass().setPdf417MacroSegmentsCount(value)

      def getPdf417MacroFileName(self):
            """!
            Gets macro Pdf417 barcode file name.
            """
            return self.getJavaClass().getPdf417MacroFileName()

      def setPdf417MacroFileName(self, value):
            """!
            Sets macro Pdf417 barcode file name.
            """
            self.getJavaClass().setPdf417MacroFileName(value)

      def getPdf417MacroTimeStamp(self):
            """!
            Gets macro Pdf417 barcode time stamp.
            """
            return datetime.fromtimestamp(int(str(self.getJavaClass().getPdf417MacroTimeStamp())))

      def setPdf417MacroTimeStamp(self, value):
            """!
            Sets macro Pdf417 barcode time stamp.
            """
            self.getJavaClass().setPdf417MacroTimeStamp(str(int(time.mktime(value.timetuple()))))

      def getPdf417MacroSender(self):
            """!
            Gets macro Pdf417 barcode sender name.
            """
            return self.getJavaClass().getPdf417MacroSender()

      def setPdf417MacroSender(self, value):
            """!
            Sets macro Pdf417 barcode sender name.
            """
            self.getJavaClass().setPdf417MacroSender(value)

      def getPdf417MacroAddressee(self):
            """!
            Gets macro Pdf417 barcode addressee name.
            """
            return self.getJavaClass().getPdf417MacroAddressee()

      def setPdf417MacroAddressee(self, value):
            """!
            Sets macro Pdf417 barcode addressee name.
            """
            self.getJavaClass().setPdf417MacroAddressee(value)

      def getPdf417MacroFileSize(self):
            """!
            Gets macro Pdf417 file size.
            @return The file size field contains the size in bytes of the entire source file.
            """
            return self.getJavaClass().getPdf417MacroFileSize()

      def setPdf417MacroFileSize(self, value):
            """!
            Sets macro Pdf417 file size.
            @param value The file size field contains the size in bytes of the entire source file.
            """
            self.getJavaClass().setPdf417MacroFileSize(value)

      def getPdf417MacroChecksum(self):
            """!
            Gets macro Pdf417 barcode checksum.
            @return The checksum field contains the value of the 16-bit (2 bytes) CRC checksum using the CCITT-16 polynomial.
            """
            return self.getJavaClass().getPdf417MacroChecksum()

      def setPdf417MacroChecksum(self, value):
            """!
            Sets macro Pdf417 barcode checksum.
            @param value The checksum field contains the value of the 16-bit (2 bytes) CRC checksum using the CCITT-16 polynomial.
            """
            self.getJavaClass().setPdf417MacroChecksum(value)

      def getPdf417ECIEncoding(self):
            """!
            Extended Channel Interpretation Identifiers. It is used to tell the barcode reader details
            about the used references for encoding the data in the symbol.
            Current implementation consists all well known charset encodings.
            """
            return ECIEncodings(self.getJavaClass().getPdf417ECIEncoding())

      def setPdf417ECIEncoding(self, value):
            """!
            Extended Channel Interpretation Identifiers. It is used to tell the barcode reader details
            about the used references for encoding the data in the symbol.
            Current implementation consists all well known charset encodings.
            """
            self.getJavaClass().setPdf417ECIEncoding(value.value)

      def getPdf417MacroECIEncoding(self):
            """!
            Extended Channel Interpretation Identifiers. Applies for Macro PDF417 text fields.
            """
            return ECIEncodings(self.getJavaClass().getPdf417MacroECIEncoding())

      def setPdf417MacroECIEncoding(self, value):
            """!
            Extended Channel Interpretation Identifiers. Applies for Macro PDF417 text fields.
            """
            self.getJavaClass().setPdf417MacroECIEncoding(value.value)

      def getPdf417MacroTerminator(self):
            """!
            Used to tell the encoder whether to add Macro PDF417 Terminator (codeword 922) to the segment.
            Applied only for Macro PDF417.
            """
            return Pdf417MacroTerminator(self.getJavaClass().getPdf417MacroTerminator())

      def setPdf417MacroTerminator(self, value):
            """!
            Used to tell the encoder whether to add Macro PDF417 Terminator (codeword 922) to the segment.
            Applied only for Macro PDF417.
            """
            self.getJavaClass().setPdf417MacroTerminator(value.value)

      def isReaderInitialization(self):
            """!
            Used to instruct the reader to interpret the data contained within the symbol
            as programming for reader initialization
            @return
            """
            return self.getJavaClass().isReaderInitialization()

      def setReaderInitialization(self, value):
            """!
            Used to instruct the reader to interpret the data contained within the symbol
            as programming for reader initialization
            @param value
            """
            self.getJavaClass().setReaderInitialization(value)

      def getMacroCharacters(self):
            """!

             Macro Characters 05 and 06 values are used to obtain more compact encoding in special modes.
             Can be used only with MicroPdf417 and encodes 916 and 917 MicroPdf417 modes
             Default value: MacroCharacters.None.
             These samples show how to encode Macro Characters in MicroPdf417
             \code
             # Encodes MicroPdf417 with 05 Macro the string: "[)>\u001E05\u001Dabcde1234\u001E\u0004"
             generator = BarcodeGenerator(EncodeTypes.MICRO_PDF_417, "abcde1234")
             generator.getParameters().getBarcode().getPdf417().setMacroCharacters(MacroCharacter.MACRO_05)
             reader = BarCodeReader(generator.generateBarCodeImage(), None, DecodeType.MICRO_PDF_417)
             for result in reader.readBarCodes():
                  print( result.getCodeText())

             \endcode
             \code
             # Encodes MicroPdf417 with 06 Macro the string: "[)>\u001E06\u001Dabcde1234\u001E\u0004"
             generator = BarcodeGenerator(EncodeTypes.MICRO_PDF_417, "abcde1234")
             generator.getParameters().getBarcode().getPdf417().setMacroCharacters(MacroCharacter.MACRO_06)
             reader = BarCodeReader(generator.generateBarCodeImage(), None, DecodeType.MICRO_PDF_417)
             for result in reader.readBarCodes():
                  print( result.getCodeText())
             \endcode
            """
            return MacroCharacter(self.getJavaClass().getMacroCharacters())

      def setMacroCharacters(self, value):
            """!

             Macro Characters 05 and 06 values are used to obtain more compact encoding in special modes.
             Can be used only with MicroPdf417 and encodes 916 and 917 MicroPdf417 modes
             Default value: MacroCharacters.None.
             
             These samples show how to encode Macro Characters in MicroPdf417


             \code
             # Encodes MicroPdf417 with 05 Macro the string: "[)>\u001E05\u001Dabcde1234\u001E\u0004"
             generator = BarcodeGenerator(EncodeTypes.MICRO_PDF_417, "abcde1234")
             generator.getParameters().getBarcode().getPdf417().setMacroCharacters(MacroCharacter.MACRO_05)
             reader = BarCodeReader(generator.generateBarCodeImage(), None, DecodeType.MICRO_PDF_417)
             for result in reader.readBarCodes():
                  print( result.getCodeText())

             \endcode
             \code
             # Encodes MicroPdf417 with 06 Macro the string: "[)>\u001E06\u001Dabcde1234\u001E\u0004"
             generator = BarcodeGenerator(EncodeTypes.MICRO_PDF_417, "abcde1234")
             generator.getParameters().getBarcode().getPdf417().setMacroCharacters(MacroCharacter.MACRO_06)
             reader = BarCodeReader(generator.generateBarCodeImage(), None, DecodeType.MICRO_PDF_417)
             for result in reader.readBarCodes():
                  print( result.getCodeText())
             \endcode

             

            """
            self.getJavaClass().setMacroCharacters(value.value)

      def isLinked(self):
            """

             Defines linked modes with GS1MicroPdf417, MicroPdf417 and Pdf417 barcodes
             With GS1MicroPdf417 symbology encodes 906, 907, 912, 913, 914, 915 “Linked” UCC/EAN-128 modes
             With MicroPdf417 and Pdf417 symbologies encodes 918 linkage flag to associated linear component other than an EAN.UCC
             
             These samples show how to encode "Linked" UCC/EAN-128 modes in GS1MicroPdf417 and Linkage Flag (918) in MicroPdf417 and Pdf417 barcodes


             \code
             # Encodes GS1 Linked mode 912 with date field AI 11 (Production date) and AI 10 (Lot number)
             generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_MICRO_PDF_417, "(11)991231(10)ABCD")
		     generator.getParameters().getBarcode().getPdf417().setLinked(True)
		     reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.GS_1_MICRO_PDF_417)
		     results = reader.readBarCodes()
		     for result in results:
			   print(f"\nBarCode Type: {result.getCodeTypeName()}")
			   print(f"BarCode CodeText: {result.getCodeText()}")
			   print(f" IsLinked: {str(result.getExtended().getPdf417().isLinked())}")

             \endcode
             \code
             # Encodes GS1 Linked mode 912 with date field AI 13 (Packaging date) and AI 21 (Serial number)
                  generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_MICRO_PDF_417, "(13)991231(21)ABCD")
                  generator.getParameters().getBarcode().getPdf417().setLinked(True)
                  reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.GS_1_MICRO_PDF_417)
                  results = reader.readBarCodes()
                  for result in results:
                      print(f"\nBarCode Type: {result.getCodeTypeName()}")
                      print(f"BarCode CodeText: {result.getCodeText()}")
                      print(f" IsLinked: {str(result.getExtended().getPdf417().isLinked())}")

             \endcode
             \code
             # Encodes GS1 Linked mode 912 with date field AI 15 (Sell-by date) and AI 10 (Lot number)
             generator = BarcodeGenerator(EncodeTypes.GS_1_MICRO_PDF_417, "(15)991231(10)ABCD")
             generator.getParameters().getBarcode().getPdf417().setLinked(True)
             reader = BarCodeReader(generator.generateBarCodeImage(), None, DecodeType.GS_1_MICRO_PDF_417)
             for result in reader.readBarCodes():
                  print(result.getCodeText() + " IsLinked:" + result.getExtended().getPdf417().isLinked())

             \endcode
             \code
             # Encodes GS1 Linked mode 912 with date field AI 17 (Expiration date) and AI 21 (Serial number)
             generator = BarcodeGenerator(EncodeTypes.GS_1_MICRO_PDF_417, "(17)991231(21)ABCD")
             generator.getParameters().getBarcode().getPdf417().setLinked(True)
             reader = BarCodeReader(generator.generateBarCodeImage(), None, DecodeType.GS_1_MICRO_PDF_417)
             for result in reader.readBarCodes():
                  print(result.getCodeText() + " IsLinked:" + result.getExtended().getPdf417().isLinked())
             \endcode
             \code
             # Encodes GS1 Linked mode 914 with AI 10 (Lot number)
             generator = BarcodeGenerator(EncodeTypes.GS_1_MICRO_PDF_417, "(10)ABCD12345")
             generator.getParameters().getBarcode().getPdf417().setLinked(True)
             reader = BarCodeReader(generator.generateBarCodeImage(), None, DecodeType.GS_1_MICRO_PDF_417)
             for result in reader.readBarCodes():
                  print(result.getCodeText() + " IsLinked:" + result.getExtended().getPdf417().isLinked())
             \endcode
             \code
             # Encodes GS1 Linked mode 915 with AI 21 (Serial number)
             generator = BarcodeGenerator(EncodeTypes.GS_1_MICRO_PDF_417, "(21)ABCD12345")
             generator.getParameters().getBarcode().getPdf417().setLinked(True)
             reader = BarCodeReader(generator.generateBarCodeImage(), None, DecodeType.GS_1_MICRO_PDF_417)
             for result in reader.readBarCodes():
                  print(result.getCodeText() + " IsLinked:" + result.getExtended().getPdf417().isLinked())

             \endcode
             \code
             # Encodes GS1 Linked modes 906, 907 with any AI
             generator = BarcodeGenerator(EncodeTypes.GS_1_MICRO_PDF_417, "(240)123456789012345")
             generator.getParameters().getBarcode().getPdf417().setLinked(True)
             reader = BarCodeReader(generator.generateBarCodeImage(), None, DecodeType.GS_1_MICRO_PDF_417)
             for result in reader.readBarCodes():
                  print(result.getCodeText() + " IsLinked:" + result.getExtended().getPdf417().isLinked())

             \endcode
             \code
             # Encodes MicroPdf417 NON EAN.UCC Linked mode 918
             generator = BarcodeGenerator(EncodeTypes.MICRO_PDF_417, "ABCDE123456789012345678")
             generator.getParameters().getBarcode().getPdf417().setLinked(True)
             reader = BarCodeReader(generator.generateBarCodeImage(), None, DecodeType.MICRO_PDF_417)
             for result in reader.readBarCodes():
                  print(result.getCodeText() + " IsLinked:" + result.getExtended().getPdf417().isLinked())
             \endcode
             \code
             # Encodes Pdf417 NON EAN.UCC Linked mode 918
             generator = BarcodeGenerator(EncodeTypes.PDF_417, "ABCDE123456789012345678")
             generator.getParameters().getBarcode().getPdf417().setLinked(True)
             reader = BarCodeReader(generator.generateBarCodeImage(), None, DecodeType.PDF_417)
             for result in reader.readBarCodes():
                  print(result.getCodeText() + " IsLinked:" + result.getExtended().getPdf417().isLinked())
             \endcode

             

            :return:
            """
            return self.getJavaClass().isLinked()

      def setLinked(self, value):
            """!

             Defines linked modes with GS1MicroPdf417, MicroPdf417 and Pdf417 barcodes
             With GS1MicroPdf417 symbology encodes 906, 907, 912, 913, 914, 915 “Linked” UCC/EAN-128 modes
             With MicroPdf417 and Pdf417 symbologies encodes 918 linkage flag to associated linear component other than an EAN.UCC
             
             These samples show how to encode "Linked" UCC/EAN-128 modes in GS1MicroPdf417 and Linkage Flag (918) in MicroPdf417 and Pdf417 barcodes

             \code
             # Encodes GS1 Linked mode 912 with date field AI 11 (Production date) and AI 10 (Lot number)
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_MICRO_PDF_417, "(11)991231(10)ABCD")
              generator.getParameters().getBarcode().getPdf417().setLinked(True)
              reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.GS_1_MICRO_PDF_417)
              results = reader.readBarCodes()
              for result in results:
                  print(f"\nBarCode Type: {result.getCodeTypeName()}")
                  print(f"BarCode CodeText: {result.getCodeText()}")
                  print(f" IsLinked: {str(result.getExtended().getPdf417().isLinked())}")
             \endcode
             \code
              # Encodes GS1 Linked mode 912 with date field AI 13 (Packaging date) and AI 21 (Serial number)
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_MICRO_PDF_417, "(13)991231(21)ABCD")
              generator.getParameters().getBarcode().getPdf417().setLinked(True)
              reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.GS_1_MICRO_PDF_417)
              results = reader.readBarCodes()
              for result in results:
                  print(f"\nBarCode Type: {result.getCodeTypeName()}")
                  print(f"BarCode CodeText: {result.getCodeText()}")
                  print(f" IsLinked: {str(result.getExtended().getPdf417().isLinked())}")
             \endcode
             \code
             		# Encodes GS1 Linked mode 912 with date field AI 15 (Sell-by date) and AI 10 (Lot number)
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_MICRO_PDF_417, "(15)991231(10)ABCD")
              generator.getParameters().getBarcode().getPdf417().setLinked(True)
              reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.GS_1_MICRO_PDF_417)
              results = reader.readBarCodes()
              for result in results:
                  print(f"\nBarCode Type: {result.getCodeTypeName()}")
                  print(f"BarCode CodeText: {result.getCodeText()}")
                  print(f" IsLinked: {str(result.getExtended().getPdf417().isLinked())}")
             \endcode
             \code
              # Encodes GS1 Linked mode 912 with date field AI 17 (Expiration date) and AI 21 (Serial number)
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_MICRO_PDF_417, "(17)991231(21)ABCD")
              generator.getParameters().getBarcode().getPdf417().setLinked(True)
              reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.GS_1_MICRO_PDF_417)
              results = reader.readBarCodes()
              for result in results:
                  print(f"\nBarCode Type: {result.getCodeTypeName()}")
                  print(f"BarCode CodeText: {result.getCodeText()}")
                  print(f" IsLinked: {str(result.getExtended().getPdf417().isLinked())}")
             \endcode
             \code
              	# Encodes GS1 Linked mode 914 with AI 10 (Lot number)
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_MICRO_PDF_417, "(10)ABCD12345")
              generator.getParameters().getBarcode().getPdf417().setLinked(True)
              reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.GS_1_MICRO_PDF_417)
              results = reader.readBarCodes()
              for result in results:
                print(f"\nBarCode Type: {result.getCodeTypeName()}")
                print(f"BarCode CodeText: {result.getCodeText()}")
                print(f" IsLinked: {str(result.getExtended().getPdf417().isLinked())}")
             \endcode
             \code
               # Encodes GS1 Linked mode 915 with AI 21 (Serial number)
               generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_MICRO_PDF_417, "(21)ABCD12345")
               generator.getParameters().getBarcode().getPdf417().setLinked(True)
               reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.GS_1_MICRO_PDF_417)
               results = reader.readBarCodes()
               for result in results:
                   print(f"\nBarCode Type: {result.getCodeTypeName()}")
                   print(f"BarCode CodeText: {result.getCodeText()}")
                   print(f" IsLinked: {str(result.getExtended().getPdf417().isLinked())}")
             \endcode
             \code
               # Encodes GS1 Linked modes 906, 907 with any AI
               generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_MICRO_PDF_417, "(240)123456789012345")
               generator.getParameters().getBarcode().getPdf417().setLinked(True)
               reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.GS_1_MICRO_PDF_417)
               results = reader.readBarCodes()
               for result in results:
                 print(f"\nBarCode Type: {result.getCodeTypeName()}")
                 print(f"BarCode CodeText: {result.getCodeText()}")
                 print(f" IsLinked: {str(result.getExtended().getPdf417().isLinked())}")
             \endcode
             \code
               # Encodes MicroPdf417 NON EAN.UCC Linked mode 918
               generator = Generation.BarcodeGenerator(Generation.EncodeTypes.MICRO_PDF_417, "ABCDE123456789012345678")
               generator.getParameters().getBarcode().getPdf417().setLinked(True)
               reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.MICRO_PDF_417)
               results = reader.readBarCodes()
               for result in results:
                 print(f"\nBarCode Type: {result.getCodeTypeName()}")
                 print(f"BarCode CodeText: {result.getCodeText()}")
                 print(f" IsLinked: {str(result.getExtended().getPdf417().isLinked())}")
             \endcode
             \code
               # Encodes Pdf417 NON EAN.UCC Linked mode 918
               generator = Generation.BarcodeGenerator(Generation.EncodeTypes.PDF_417, "ABCDE123456789012345678")
               generator.getParameters().getBarcode().getPdf417().setLinked(True)
               reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.PDF_417)
               results = reader.readBarCodes()
               for result in results:
                 print(f"\nBarCode Type: {result.getCodeTypeName()}")
                 print(f"BarCode CodeText: {result.getCodeText()}")
                 print(f" IsLinked: {str(result.getExtended().getPdf417().isLinked())}")
             \endcode
            @param value: True or False
            @return:
            """
            self.getJavaClass().setLinked(value)

      def isCode128Emulation(self):
            """!
             Can be used only with MicroPdf417 and encodes Code 128 emulation modes
             Can encode FNC1 in second position modes 908 and 909, also can encode 910 and 911 which just indicate that recognized MicroPdf417 can be interpret as Code 128
             These samples show how to encode Code 128 emulation modes with FNC1 in second position and without. In this way MicroPdf417 can be decoded as Code 128 barcode
             \code
              # Encodes MicroPdf417 in Code 128 emulation mode with FNC1 in second position and Application Indicator "a", mode 908.
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.MICRO_PDF_417, "a\u001d1222322323")
              generator.getParameters().getBarcode().getPdf417().setCode128Emulation(True)
              reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.MICRO_PDF_417)
              results = reader.readBarCodes()
              for result in results:
                print(f"\nBarCode Type: {result.getCodeTypeName()}")
                print(f"BarCode CodeText: {result.getCodeText()}")
                print(f"IsCode128Emulation: {result.getExtended().getPdf417().isCode128Emulation()}")        \endcode
             \code
             		# Encodes MicroPdf417 in Code 128 emulation mode with FNC1 in second position and Application Indicator "99", mode 909.
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.MICRO_PDF_417, "99\u001d1222322323")
              generator.getParameters().getBarcode().getPdf417().setCode128Emulation(True)
              reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.MICRO_PDF_417)
              results = reader.readBarCodes()
              for result in results:
                print(f"\nBarCode Type: {result.getCodeTypeName()}")
                print(f"BarCode CodeText: {result.getCodeText()}")
                print(f"IsCode128Emulation: {result.getExtended().getPdf417().isCode128Emulation()}")
             \endcode
             \code
            		# Encodes MicroPdf417 in Code 128 emulation mode, modes 910, 911
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.MICRO_PDF_417, "123456789012345678")
              generator.getParameters().getBarcode().getPdf417().setCode128Emulation(True)
              reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.MICRO_PDF_417)
              results = reader.readBarCodes()
              for result in results:
                print(f"\nBarCode Type: {result.getCodeTypeName()}")
                print(f"BarCode CodeText: {result.getCodeText()}")
                print(f"IsCode128Emulation: {result.getExtended().getPdf417().isCode128Emulation()}")
             \endcode
            """
            return self.getJavaClass().isCode128Emulation()

      def setCode128Emulation(self, value):
            """!

             Can be used only with MicroPdf417 and encodes Code 128 emulation modes
             Can encode FNC1 in second position modes 908 and 909, also can encode 910 and 911 which just indicate that recognized MicroPdf417 can be interpret as Code 128
             These samples show how to encode Code 128 emulation modes with FNC1 in second position and without. In this way MicroPdf417 can be decoded as Code 128 barcode
             \code
              # Encodes MicroPdf417 in Code 128 emulation mode with FNC1 in second position and Application Indicator "a", mode 908.
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.MICRO_PDF_417, "a\u001d1222322323")
              generator.getParameters().getBarcode().getPdf417().setCode128Emulation(True)
              reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.MICRO_PDF_417)
              results = reader.readBarCodes()
              for result in results:
                print(f"\nBarCode Type: {result.getCodeTypeName()}")
                print(f"BarCode CodeText: {result.getCodeText()}")
                print(f"IsCode128Emulation: {result.getExtended().getPdf417().isCode128Emulation()}")        \endcode
             \code
             		# Encodes MicroPdf417 in Code 128 emulation mode with FNC1 in second position and Application Indicator "99", mode 909.
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.MICRO_PDF_417, "99\u001d1222322323")
              generator.getParameters().getBarcode().getPdf417().setCode128Emulation(True)
              reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.MICRO_PDF_417)
              results = reader.readBarCodes()
              for result in results:
                print(f"\nBarCode Type: {result.getCodeTypeName()}")
                print(f"BarCode CodeText: {result.getCodeText()}")
                print(f"IsCode128Emulation: {result.getExtended().getPdf417().isCode128Emulation()}")
             \endcode
             \code
            		# Encodes MicroPdf417 in Code 128 emulation mode, modes 910, 911
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.MICRO_PDF_417, "123456789012345678")
              generator.getParameters().getBarcode().getPdf417().setCode128Emulation(True)
              reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.MICRO_PDF_417)
              results = reader.readBarCodes()
              for result in results:
                print(f"\nBarCode Type: {result.getCodeTypeName()}")
                print(f"BarCode CodeText: {result.getCodeText()}")
                print(f"IsCode128Emulation: {result.getExtended().getPdf417().isCode128Emulation()}")
             \endcode
            @param value:
            @return
            """

            self.getJavaClass().setCode128Emulation(value)

      def toString(self):
            """!
            Returns a human-readable string representation of this Pdf417Parameters.
            @return A string that represents this Pdf417Parameters.
            """
            return self.getJavaClass().toString()


class SupplementParameters(Assist.BaseJavaClass):
      """!
      Supplement parameters. Used for Interleaved2of5, Standard2of5, EAN13, EAN8, UPCA, UPCE, ISBN, ISSN, ISMN.
      """

      def __init__(self, javaClass):
            self._space = None
            super().__init__(javaClass)
            self.init()

      def init(self):
            self._space = Unit(self.getJavaClass().getSupplementSpace())

      def getSupplementData(self):
            """!
            Supplement data following BarCode.
            """
            return self.getJavaClass().getSupplementData()

      def setSupplementData(self, value):
            """!
            Supplement data following BarCode.
            """
            self.getJavaClass().setSupplementData(value)

      def getSupplementSpace(self):
            """!
            Space between main the BarCode and supplement BarCode in Unit value.
            @exception IllegalArgumentException
            The Space parameter value is less than 0.
            """
            return self._space

      def toString(self):
            """!
            Returns a human-readable string representation of this SupplementParameters.
            @return A string that represents this SupplementParameters.
            """
            return self.getJavaClass().toString()


class MaxiCodeParameters(Assist.BaseJavaClass):
      """!
      MaxiCode parameters.
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            pass


      def getMaxiCodeMode(self):
            """!
            Gets a MaxiCode encode mode.
            """
            return MaxiCodeMode(self.getJavaClass().getMaxiCodeMode())

      def setMaxiCodeMode(self, maxiCodeMode):
            """!
            Sets a MaxiCode encode mode.
            """
            self.getJavaClass().setMaxiCodeMode(maxiCodeMode.value)

      def getMaxiCodeEncodeMode(self):
            """!
            Gets a MaxiCode encode mode.
            """
            return MaxiCodeEncodeMode(self.getJavaClass().getMaxiCodeEncodeMode())

      def setMaxiCodeEncodeMode(self, value):
            """!
            Sets a MaxiCode encode mode.
            """
            self.getJavaClass().setMaxiCodeEncodeMode(value.value)


      def getECIEncoding(self):
            """!
            Gets ECI encoding. Used when MaxiCodeEncodeMode is AUTO.
            Default value: ISO-8859-1
            """
            return ECIEncodings(self.getJavaClass().getECIEncoding())

      def setECIEncoding(self, ECIEncoding):
            """!
            Sets ECI encoding. Used when MaxiCodeEncodeMode is AUTO.
            Default value: ISO-8859-1
            """
            self.getJavaClass().setECIEncoding(ECIEncoding.value)

      def getMaxiCodeStructuredAppendModeBarcodeId(self):
            """!
            Gets a MaxiCode barcode id in structured append mode.
            ID must be a value between 1 and 8.
            Default value: 0
            """
            return self.getJavaClass().getMaxiCodeStructuredAppendModeBarcodeId()

      def setMaxiCodeStructuredAppendModeBarcodeId(self, maxiCodeStructuredAppendModeBarcodeId):
            """!
            Sets a MaxiCode barcode id in structured append mode.
            ID must be a value between 1 and 8.
            Default value: 0
            """
            self.getJavaClass().setMaxiCodeStructuredAppendModeBarcodeId(maxiCodeStructuredAppendModeBarcodeId)

      def getMaxiCodeStructuredAppendModeBarcodesCount(self):
            """!
            Gets a MaxiCode barcodes count in structured append mode.
            Count number must be a value between 2 and 8 (maximum barcodes count).
            Default value: -1
            """
            return self.getJavaClass().getMaxiCodeStructuredAppendModeBarcodesCount()

      def setMaxiCodeStructuredAppendModeBarcodesCount(self, maxiCodeStructuredAppendModeBarcodesCount):
            """!
            Sets a MaxiCode barcodes count in structured append mode.
            Count number must be a value between 2 and 8 (maximum barcodes count).
            Default value: -1
            """
            self.getJavaClass().setMaxiCodeStructuredAppendModeBarcodesCount(maxiCodeStructuredAppendModeBarcodesCount)

      def getAspectRatio(self):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            return self.getJavaClass().getAspectRatio()

      def setAspectRatio(self, value):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            self.getJavaClass().setAspectRatio(value)

      def toString(self):
            """!
            Returns a human-readable string representation of this MaxiCodeParameters.
            @return A string that represents this MaxiCodeParameters.
            """
            return self.getJavaClass().toString()


class AztecParameters(Assist.BaseJavaClass):
      """!
      Aztec parameters.
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            pass

      def getAztecEncodeMode(self):
            """!
            Gets a Aztec encode mode.
            Default value: Auto.
            """
            return AztecEncodeMode(self.getJavaClass().getAztecEncodeMode())

      def setAztecEncodeMode(self, value):
            """
            Sets a Aztec encode mode.
            Default value: Auto.
            """
            self.getJavaClass().setAztecEncodeMode(value.value)

      def getECIEncoding(self):
            """!
            Gets ECI encoding. Used when AztecEncodeMode is Auto. 
            Default value: ISO-8859-1
            """
            return ECIEncodings(self.getJavaClass().getECIEncoding())

      def setECIEncoding(self, value):
            """!
            Sets ECI encoding. Used when AztecEncodeMode is Auto.
            Default value: ISO-8859-1
            """
            self.getJavaClass().setECIEncoding(value.value)

      def getStructuredAppendBarcodeId(self):
            """!
            Barcode ID for Structured Append mode of Aztec barcode. Barcode ID should be in range from 1 to barcodes count.
            Default value: 0
            """
            return self.getJavaClass().getStructuredAppendBarcodeId()

      def setStructuredAppendBarcodeId(self, value):
            """!
            Barcode ID for Structured Append mode of Aztec barcode. Barcode ID should be in range from 1 to barcodes count.
            Default value: 0
            """
            self.getJavaClass().setStructuredAppendBarcodeId(value)

      def getStructuredAppendBarcodesCount(self):
            """!
            Barcodes count for Structured Append mode of Aztec barcode. Barcodes count should be in range from 1 to 26.
            Default value: 0
            """
            return self.getJavaClass().getStructuredAppendBarcodesCount()

      def setStructuredAppendBarcodesCount(self, value):
            """!
            Barcodes count for Structured Append mode of Aztec barcode. Barcodes count should be in range from 1 to 26.
            Default value: 0
            """
            self.getJavaClass().setStructuredAppendBarcodesCount(value)

      def getStructuredAppendFileId(self):
            """!
            File ID for Structured Append mode of Aztec barcode (optional field). File ID should not contain spaces.
            Default value: empty string
            """
            self.getJavaClass().getStructuredAppendFileId()

      def setStructuredAppendFileId(self, value):
            """!
            File ID for Structured Append mode of Aztec barcode (optional field). File ID should not contain spaces.
            Default value: empty string
            """
            self.getJavaClass().setStructuredAppendFileId(value)

      def getAztecErrorLevel(self):
            """!
            Level of error correction of Aztec types of barcode.
            Value should between 5 to 95.
            """
            return self.getJavaClass().getAztecErrorLevel()

      def setAztecErrorLevel(self, value):
            """!
            Level of error correction of Aztec types of barcode.
            Value should between 5 to 95.
            """
            self.getJavaClass().setAztecErrorLevel(value)

      def getAztecSymbolMode(self):
            """!
            Gets a Aztec Symbol mode.
            Default value: AztecSymbolMode.Auto.
            """
            return AztecSymbolMode(self.getJavaClass().getAztecSymbolMode())

      def setAztecSymbolMode(self, value):
            """!
            Sets a Aztec Symbol mode.
            Default value: AztecSymbolMode.Auto.
            """
            self.getJavaClass().setAztecSymbolMode(value.value)

      def getLayersCount(self):
            """!
            Gets layers count of Aztec symbol. Layers count should be in range from 1 to 3 for Compact mode and
            in range from 1 to 32 for Full Range mode.
            Default value: 0 (auto).
            """
            return self.getJavaClass().getLayersCount()

      def setLayersCount(self, value):
            """!
            Sets layers count of Aztec symbol. Layers count should be in range from 1 to 3 for Compact mode and
            in range from 1 to 32 for Full Range mode.
            """
            self.getJavaClass().setLayersCount(value)

      def isReaderInitialization(self):
            """!
            Used to instruct the reader to interpret the data contained within the symbol
            as programming for reader initialization.
            """
            return self.getJavaClass().isReaderInitialization()

      def setReaderInitialization(self, value):
            """!
            Used to instruct the reader to interpret the data contained within the symbol
            as programming for reader initialization.
            """
            self.getJavaClass().setReaderInitialization(value)

      def getAspectRatio(self):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            return self.getJavaClass().getAspectRatio()

      def setAspectRatio(self, value):
            """!
            Height/Width ratio of 2D BarCode module.
            """
            print("DEPRECATED")
            self.getJavaClass().setAspectRatio(value)

      def toString(self):
            """!
            Returns a human-readable string representation of this {@code AztecParameters}.
            @:return:  A string that represents this {@code AztecParameters}.
            """
            self.getJavaClass().toString()

class CodabarParameters(Assist.BaseJavaClass):
      """!
      Codabar parameters.
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            pass

      def getCodabarChecksumMode(self):
            """!
            Get the checksum algorithm for Codabar barcodes.
            Default value: CodabarChecksumMode.MOD_16.
            To enable checksum calculation set value EnableChecksum.YES to property EnableChecksum.
            See CodabarChecksumMode.
            """
            return CodabarChecksumMode(self.getJavaClass().getCodabarChecksumMode())

      def setCodabarChecksumMode(self, value):
            """!
            Set the checksum algorithm for Codabar barcodes.
            Default value: CodabarChecksumMode.MOD_16.
            To enable checksum calculation set value EnableChecksum.YES to property EnableChecksum.
            See CodabarChecksumMode.
            """
            self.getJavaClass().setCodabarChecksumMode(value.value)

      def getCodabarStartSymbol(self):
            """!
            Start symbol (character) of Codabar symbology.
            Default value: CodabarSymbol.A
            """
            return self.getJavaClass().getCodabarStartSymbol()

      def setCodabarStartSymbol(self, value):
            """!
            Start symbol (character) of Codabar symbology.
            Default value: CodabarSymbol.A
            """
            self.getJavaClass().setCodabarStartSymbol(value)

      def getCodabarStopSymbol(self):
            """!
            Stop symbol (character) of Codabar symbology.
            Default value: CodabarSymbol.A
            """
            return self.getJavaClass().getCodabarStopSymbol()

      def setCodabarStopSymbol(self, value):
            """!
            Stop symbol (character) of Codabar symbology.
            Default value: CodabarSymbol.A
            """
            self.getJavaClass().setCodabarStopSymbol(value)

      def toString(self):
            """!
            Returns a human-readable string representation of this CodabarParameters.
            @return A string that represents this CodabarParameters.
            """
            return self.getJavaClass().toString()


class CouponParameters(Assist.BaseJavaClass):
      """!
      Coupon parameters. Used for UpcaGs1DatabarCoupon, UpcaGs1Code128Coupon.
      """

      def __init__(self, javaClass):
            self._space = None
            super().__init__(javaClass)
            self.init()

      def init(self):
            self._space = Unit(self.getJavaClass().getSupplementSpace())

      def getSupplementSpace(self):
            """!
            Space between main the BarCode and supplement BarCode in Unit value.
            @exception IllegalArgumentException
            The Space parameter value is less than 0.
            """
            return self._space

      def setSupplementSpace(self, value):
            """!
            Space between main the BarCode and supplement BarCode in Unit value.
            @exception IllegalArgumentException
            The Space parameter value is less than 0.
            """
            self.getJavaClass().setSupplementSpace(value.getJavaClass())
            self._space = value

      def toString(self):
            """!
            Returns a human-readable string representation of this CouponParameters.
            @return A string that represents this CouponParameters.
            """
            return self.getJavaClass().toString()


class FontUnit(Assist.BaseJavaClass):
      """!
       Defines a particular format for text, including font face, size, and style attributes
       where size in Unit value property.

       This sample shows how to create and save a BarCode image.
       \code
        generator = Generation.BarcodeGenerator(Generation.EncodeTypes.CODE_128,"123456789012345678")
        generator.getParameters().getCaptionAbove().setText("CAPTION ABOOVE")
        generator.getParameters().getCaptionAbove().setVisible(True)
        generator.getParameters().getCaptionAbove().getFont().setStyle(Generation.FontStyle.ITALIC)
        generator.getParameters().getCaptionAbove().getFont().getSize().setPoint(25)
       \endcode
      """

      def __init__(self, source):
            self._size = None
            super().__init__(FontUnit.initFontUnit(source))
            self.init()

      @staticmethod
      def initFontUnit(source):
            if isinstance(source, FontUnit):
                  return source.getJavaClass()
            return source

      def init(self):
            self._size = Unit(self.getJavaClass().getSize())

      def getFamilyName(self):
            """!
            Gets the face name of this Font.
            """
            return self.getJavaClass().getFamilyName()

      def setFamilyName(self, value):
            """!
            Sets the face name of this Font.
            """
            self.getJavaClass().setFamilyName(value)

      def getStyle(self):
            """!
            Gets style information for this FontUnit.
            """
            return FontStyle(self.getJavaClass().getStyle())

      def setStyle(self, value):
            """!
            Sets style information for this FontUnit.
            """
            self.getJavaClass().setStyle(value.value)

      def getSize(self):
            """!
            Gets size of this FontUnit in Unit value.
            @exception IllegalArgumentException
            The Size parameter value is less than or equal to 0.
            """
            return self._size


class ExtCodetextBuilder(Assist.BaseJavaClass):
      """!
      Helper class for automatic codetext generation of the Extended Codetext Mode
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def clear(self):
            """!
            Clears extended codetext items
            """
            self.getJavaClass().clear()

      def addPlainCodetext(self, codetext):
            """!
            Adds plain codetext to the extended codetext items

            @param codetext Codetext in unicode to add as extended codetext item
            """
            self.getJavaClass().addPlainCodetext(codetext)

      def addECICodetext(self, ECIEncoding, codetext):
            """!
            Adds codetext with Extended Channel Identifier

            @param ECIEncoding Extended Channel Identifier
            @param codetext    Codetext in unicode to add as extended codetext item with Extended Channel Identifier
            """
            self.getJavaClass().addECICodetext(ECIEncoding.value, codetext)

      def getExtendedCodetext(self):
            """!
            Generate extended codetext from generation items list

            @return Return string of extended codetext
            """
            return self.getJavaClass().getExtendedCodetext()


class QrExtCodetextBuilder(ExtCodetextBuilder):
      """!
       Extended codetext generator for 2D QR barcodes for ExtendedCodetext Mode of QREncodeMode

       Use Display2DText property of BarCodeBuilder to set visible text to removing managing characters.

       Example how to generate FNC1 first position for Extended Mode
       \code
         # create codetext
         lTextBuilder = QrExtCodetextBuilder()
         lTextBuilder.addFNC1FirstPosition()
         lTextBuilder.addPlainCodetext("000%89%%0")
         lTextBuilder.addFNC1GroupSeparator()
         lTextBuilder.addPlainCodetext("12345&ltFNC1&gt")
         #generate codetext
         lCodetext = lTextBuilder.getExtendedCodetext()
       \endcode

       Example how to generate FNC1 second position for Extended Mode
       \code
          #create codetext
          lTextBuilder = QrExtCodetextBuilder()
          lTextBuilder.addFNC1SecondPosition("12")
          lTextBuilder.addPlainCodetext("TRUE3456")
          #generate codetext
          lCodetext = lTextBuilder.getExtendedCodetext()
       \endcode

       Example how to generate multi ECI mode for Extended Mode
      \code
         #create codetext
         lTextBuilder = Generation.QrExtCodetextBuilder()
         lTextBuilder.addFNC1FirstPosition()
         lTextBuilder.addPlainCodetext("000%89%%0")
         lTextBuilder.addFNC1GroupSeparator()
         lTextBuilder.addPlainCodetext("12345&ltFNC1&gt")
         # generate codetext
         lCodetext = lTextBuilder.getExtendedCodetext()
       \endcode
      """
      javaClassName = "com.aspose.mw.barcode.MwQrExtCodetextBuilder"

      def __init__(self):
            javaQrExtCodetextBuilder = jpype.JClass(self.javaClassName)
            self.javaClass = javaQrExtCodetextBuilder()
            super().__init__(self.javaClass)
            self.init()

      def init(self):
            pass

      def addFNC1FirstPosition(self):
            """!
            Adds FNC1 in first position to the extended codetext items
            """
            self.getJavaClass().addFNC1FirstPosition()

      def addFNC1SecondPosition(self, codetext):
            """!
            Adds FNC1 in second position to the extended codetext items
            @param codetext Value of the FNC1 in the second position
            """
            self.getJavaClass().addFNC1SecondPosition(codetext)

      def addFNC1GroupSeparator(self):
            """!
            Adds Group Separator (GS - '\\u001D') to the extended codetext items
            """
            self.getJavaClass().addFNC1GroupSeparator()

      def getExtendedCodetext(self):
            """!
            Generates Extended codetext from the extended codetext list.
            @return Extended codetext as string
            """
            return self.getJavaClass().getExtendedCodetext()


class QrStructuredAppendParameters(Assist.BaseJavaClass):
      """!
      QR structured append parameters.
      """

      def init(self):
            pass

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def getParityByte(self):
            """!
            Gets the QR structured append mode parity data.
            """
            return self.getJavaClass().getParityByte()

      def setParityByte(self, value):
            """!
            Sets the QR structured append mode parity data.
            """
            self.getJavaClass().setParityByte(value)

      def getSequenceIndicator(self):
            """!
            Gets the index of the QR structured append mode barcode. Index starts from 0.
            """
            return self.getJavaClass().getSequenceIndicator()

      def setSequenceIndicator(self, value):
            """!
            Sets the index of the QR structured append mode barcode. Index starts from 0.
            """
            self.getJavaClass().setSequenceIndicator(value)

      def getTotalCount(self):
            """!
            Gets the QR structured append mode barcodes quantity. Max value is 16.
            """
            return self.getJavaClass().getTotalCount()

      def setTotalCount(self, value):
            """!
            Sets the QR structured append mode barcodes quantity. Max value is 16.
            """
            self.getJavaClass().setTotalCount(value)

      def getStateHash(self):
            return self.getJavaClass().getStateHash()


class MaxiCodeExtCodetextBuilder(ExtCodetextBuilder):
      """!
      Extended codetext generator for MaxiCode barcodes for ExtendedCodetext Mode of MaxiCodeEncodeMode
      Use TwoDDisplayText property of BarcodeGenerator to set visible text to removing managing characters.

      This sample shows how to use MaxiCodeExtCodetextBuilder in Extended Mode.

      \code
        # create codetext
        textBuilder = Generation.MaxiCodeExtCodetextBuilder()
        textBuilder.addECICodetext(Generation.ECIEncodings.Win1251, "Will")
        textBuilder.addECICodetext(Generation.ECIEncodings.UTF8, "犬Right狗")
        textBuilder.addECICodetext(Generation.ECIEncodings.UTF16BE, "犬Power狗")
        textBuilder.addPlainCodetext("Plain text")

        # generate codetext
        codetext = textBuilder.getExtendedCodetext()
        # generate
        generator = Generation.BarcodeGenerator(Generation.EncodeTypes.MAXI_CODE, codetext)
        generator.getParameters().getBarcode().getCodeTextParameters().setTwoDDisplayText("My Text")
        generator.save(self.image_path_to_save5, Generation.BarCodeImageFormat.BMP)
      \endcode
      """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.generation.MwMaxiCodeExtCodetextBuilder"

      def __init__(self):
            try:
                  java_class = jpype.JClass(MaxiCodeExtCodetextBuilder.JAVA_CLASS_NAME)
                  super().__init__(java_class())
            except Exception as ex:
                  raise Assist.BarCodeException(ex)

      def init(self):
            pass


      def getExtendedCodetext(self):
            """!
            Generates Extended codetext from the extended codetext list.
            @return :Extended codetext as string
            """
            return self.getJavaClass().getExtendedCodetext()

class DotCodeExtCodetextBuilder(ExtCodetextBuilder):
      """!
      Extended codetext generator for 2D DotCode barcodes for ExtendedCodetext Mode of DotCodeEncodeMode
      \code
              #Extended codetext mode
              #create codetext
              textBuilder = DotCodeExtCodetextBuilder()
              textBuilder.addFNC1FormatIdentifier()
              textBuilder.addECICodetext(ECIEncodings.Win1251, "Will")
              textBuilder.addFNC1FormatIdentifier()
              textBuilder.addECICodetext(ECIEncodings.UTF8, "犬Right狗")
              textBuilder.addFNC1FormatIdentifier()
              textBuilder.addECICodetext(ECIEncodings.UTF16BE, "犬Power狗")
              textBuilder.addPlainCodetext("Plain text")
              textBuilder.addFNC3SymbolSeparator()
              textBuilder.addFNC3ReaderInitialization()
              textBuilder.addPlainCodetext("Reader initialization info")
              #generate codetext
              codetext = textBuilder.getExtendedCodetext()
              #generate
              generator = BarcodeGenerator(EncodeTypes.DOT_CODE, codetext)
              generator.getParameters().getBarcode().getDotCode().setDotCodeEncodeMode(DotCodeEncodeMode.EXTENDED_CODETEXT)
              generator.save("test.bmp", BarCodeImageFormat.BMP)
      \endcode
      """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.generation.MwDotCodeExtCodetextBuilder"

      def __init__(self):
            java_class_link = jpype.JClass(DotCodeExtCodetextBuilder.JAVA_CLASS_NAME)
            javaClass = java_class_link()
            super().__init__(javaClass)

      @staticmethod
      def construct(javaClass):
            obj = DotCodeExtCodetextBuilder()
            obj.setJavaClass(javaClass)
            return obj

      def addFNC1FormatIdentifier(self):
            """!
            Adds FNC1 format identifier to the extended codetext items
            """
            self.getJavaClass().addFNC1FormatIdentifier()

      def addFNC3SymbolSeparator(self):
            """!
            Adds FNC3 symbol separator to the extended codetext items
            """
            self.getJavaClass().addFNC3SymbolSeparator()

      def addFNC3ReaderInitialization(self):
            """!
            Adds FNC3 reader initialization to the extended codetext items
            """
            self.getJavaClass().addFNC3ReaderInitialization()

      def addStructuredAppendMode(self, barcodeId, barcodesCount):
            """!
            Adds structured append mode to the extended codetext items

            @param: barcodeId: ID of barcode
            @param: barcodesCount:Barcodes count
            """
            self.getJavaClass().addStructuredAppendMode(barcodeId, barcodesCount)

      def getExtendedCodetext(self):
            """!
            Generates Extended codetext from the extended codetext list.
            @return:Extended codetext as string
            """
            return self.getJavaClass().getExtendedCodetext()

      def init(self):
            pass

class Code128Parameters(Assist.BaseJavaClass):
      """!
      Code128 parameters.
      """

      def init(self):
            pass

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def getCode128EncodeMode(self):
            """!
            Gets a Code128 encode mode.
            Default value: Code128EncodeMode.Auto
            """
            return Code128EncodeMode(self.getJavaClass().getCode128EncodeMode())

      def setCode128EncodeMode(self, value):
            """!
             Sets a Code128 encode mode.
             Default value: Code128EncodeMode.Auto
            """
            self.getJavaClass().setCode128EncodeMode(value.value)

      def toString(self):
            """!
            Returns a human-readable string representation of this PatchCodeParameters.
            @return string A string that represents this PatchCodeParameters.
            """
            return self.getJavaClass().toString()

class HanXinParameters(Assist.BaseJavaClass):
      """!
      Han Xin parameters.
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            pass

      def getHanXinVersion(self):
            """!
            Version of HanXin Code.
            From Version01 to Version84 for Han Xin code.
            Default value is HanXinVersion.Auto.
            """
            return HanXinVersion(self.getJavaClass().getHanXinVersion())

      def setHanXinVersion(self, value):
            """!
            Version of HanXin Code.
            From Version01 to Version84 for Han Xin code.
            Default value is HanXinVersion.Auto.
            """
            self.getJavaClass().setHanXinVersion(value.value)

      def getHanXinErrorLevel(self):
            """!
            Level of Reed-Solomon error correction for Han Xin barcode.
            From low to high: L1, L2, L3, L4. see HanXinErrorLevel.
            """
            return HanXinErrorLevel(self.getJavaClass().getHanXinErrorLevel())

      def setHanXinErrorLevel(self, value):
            """!
            Level of Reed-Solomon error correction for Han Xin barcode.
            From low to high: L1, L2, L3, L4. see HanXinErrorLevel.
            """
            self.getJavaClass().setHanXinErrorLevel(value.value)

      def getHanXinEncodeMode(self):
            """!
            HanXin encoding mode.
            Default value: HanXinEncodeMode.Mixed.
            """
            return HanXinEncodeMode(self.getJavaClass().getHanXinEncodeMode())

      def setHanXinEncodeMode(self, value):
            """!
            HanXin encoding mode.
            Default value: HanXinEncodeMode.Mixed.
            """
            self.getJavaClass().setHanXinEncodeMode(value.value)

      def getHanXinECIEncoding(self):
            """!
            Extended Channel Interpretation Identifiers. It is used to tell the barcode reader details
            Current implementation consists all well known charset encodings.
            """
            return ECIEncodings(self.getJavaClass().getHanXinECIEncoding())

      def setHanXinECIEncoding(self, value):
            """!
            Extended Channel Interpretation Identifiers. It is used to tell the barcode reader details

            Current implementation consists all well known charset encodings.
            """
            self.getJavaClass().setHanXinECIEncoding(value.value)

      def toString(self):
            """!
            Returns a human-readable string representation of this {@code HanXinParameters}.
            @return:  A string that represents this {@code HanXinParameters}.
            """
            return self.getJavaClass().toString()

class DataMatrixExtCodetextBuilder(ExtCodetextBuilder):
      """!
       Extended codetext generator for 2D DataMatrix barcodes for ExtendedCodetext Mode of DataMatrixEncodeMode

       \code
		# Extended codetext mode
		# create codetext
		codetextBuilder = Generation.DataMatrixExtCodetextBuilder()
		codetextBuilder.addECICodetextWithEncodeMode(Generation.ECIEncodings.Win1251, Generation.DataMatrixEncodeMode.BYTES, "World")
		codetextBuilder.addPlainCodetext("Will")
		codetextBuilder.addECICodetext(Generation.ECIEncodings.UTF8, "犬Right狗")
		codetextBuilder.addCodetextWithEncodeMode(Generation.DataMatrixEncodeMode.C40, "ABCDE")
		# generate codetext
		codetext = codetextBuilder.getExtendedCodetext()
		# generate
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.DATA_MATRIX, codetext)
		generator.getParameters().getBarcode().getDataMatrix().setDataMatrixEncodeMode(Generation.DataMatrixEncodeMode.EXTENDED_CODETEXT)
		generator.save(self.image_path_to_save5, Generation.BarCodeImageFormat.BMP)
      \endcode
      """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.generation.MwDataMatrixExtCodetextBuilder"

      def __init__(self):
            java_class_link = jpype.JClass(DataMatrixExtCodetextBuilder.JAVA_CLASS_NAME)
            javaClass = java_class_link()
            super().__init__(javaClass)

      @staticmethod
      def construct(javaClass):
            obj = DataMatrixExtCodetextBuilder()
            obj.setJavaClass(javaClass)
            return obj

      def init(self):
            pass

      def addECICodetextWithEncodeMode(self, ECIEncoding, encodeMode, codetext):
            """!
            Adds codetext with Extended Channel Identifier with defined encode mode
            @param ECIEncoding: Extended Channel Identifier
            @param encodeMode: Encode mode value
            @param codetext: Codetext in unicode to add as extended codetext item with Extended Channel Identifier with defined encode mode
            """
            self.getJavaClass().addECICodetextWithEncodeMode(ECIEncoding.value, encodeMode.value, codetext)

      def addCodetextWithEncodeMode(self, encodeMode, codetext):
            """!
            Adds codetext with defined encode mode to the extended codetext items
            @param encodeMode: Encode mode value
            @param codetext: Codetext in unicode to add as extended codetext item
            """
            self.getJavaClass().addCodetextWithEncodeMode(encodeMode.value, codetext)

      def getExtendedCodetext(self):
            """!
            Generates Extended codetext from the extended codetext list.
            @return: Extended codetext as string
            """
            return self.getJavaClass().getExtendedCodetext()

class HanXinExtCodetextBuilder(Assist.BaseJavaClass):
      """!
      Extended codetext generator for Han Xin Code for Extended Mode of HanXinEncodeMode
      \code
		# Extended codetext mode
		# create codetext
		codeTextBuilder = Generation.HanXinExtCodetextBuilder()
		codeTextBuilder.addGB18030TwoByte("漄")
		codeTextBuilder.addGB18030FourByte("㐁")
		codeTextBuilder.addCommonChineseRegionOne("全")
		codeTextBuilder.addCommonChineseRegionTwo("螅")
		codeTextBuilder.addNumeric("123")
		codeTextBuilder.addText("qwe")
		codeTextBuilder.addUnicode("ıntəˈnæʃənəl")
		codeTextBuilder.addECI("ΑΒΓΔΕ", 9)
		codeTextBuilder.addAuto("abc")
		codeTextBuilder.addBinary("abc")
		codeTextBuilder.addURI("backslashes_should_be_doubled\000555:test")
		# generate codetext
		codetext = codeTextBuilder.getExtendedCodetext()
		# generate
		bg = Generation.BarcodeGenerator(Generation.EncodeTypes.HAN_XIN, codetext)
		bg.getParameters().getBarcode().getHanXin().setHanXinEncodeMode(Generation.HanXinEncodeMode.EXTENDED)
		img = bg.generateBarCodeImage()
		reader = Recognition.BarCodeReader(img, None, Recognition.DecodeType.HAN_XIN)
		foundBarcodes = reader.readBarCodes()
		print(f"found Barcodes: {len(foundBarcodes)}")
		print(f"codetext:  {foundBarcodes[0].getCodeText()}")

      \endcode
      """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.generation.MwHanXinExtCodetextBuilder"

      def __init__(self):
            java_class_link = jpype.JClass(HanXinExtCodetextBuilder.JAVA_CLASS_NAME)
            javaClass = java_class_link()
            super().__init__(javaClass)

      def init(self):
            pass

      def addECI(self, text, encoding):
            """!
             Adds codetext fragment in ECI mode
            @param text:  text Codetext string
            @param encoding:  encoding ECI encoding in integer format
            """
            self.getJavaClass().addECI(text, encoding)


      def addAuto(self, text):
            """!
             Adds codetext fragment in Auto mode
            @param text:  text Codetext string
            """
            self.getJavaClass().addAuto(text)

      def addBinary(self, text):
            """!
             Adds codetext fragment in Binary mode
            @param text:  text Codetext string
            """
            self.getJavaClass().addBinary(text)

      def addURI(self, text):
            """!
             Adds codetext fragment in URI mode
            @param text:  text Codetext string
            """
            self.getJavaClass().addURI(text)

      def addText(self, text):
            """!
             Adds codetext fragment in Text mode
            @param text:  text Codetext string
            """
            self.getJavaClass().addText(text)

      def addNumeric(self, text):
            """!
            Adds codetext fragment in Numeric mode
            @param text:  text Codetext string
            """
            self.getJavaClass().addNumeric(text)

      def addUnicode(self, text):
            """!
            Adds codetext fragment in Unicode mode
            @param text: text Codetext string
            """
            self.getJavaClass().addUnicode(text)

      def addCommonChineseRegionOne(self, text):
            """!
            Adds codetext fragment in Common Chinese Region One mode
            @param text: text Codetext string
            """
            self.getJavaClass().addCommonChineseRegionOne(text)

      def addCommonChineseRegionTwo(self, text):
            """!
            Adds codetext fragment in Common Chinese Region Two mode
            @param text: text Codetext string
            """
            self.getJavaClass().addCommonChineseRegionTwo(text)

      def addGB18030TwoByte(self, text):
            """!
            Adds codetext fragment in GB18030 Two Byte mode
            @param text: text Codetext string
            """
            self.getJavaClass().addGB18030TwoByte(text)

      def addGB18030FourByte(self, text):
            """!
            Adds codetext fragment in GB18030 Four Byte mode
            @param text: text Codetext string
            """
            self.getJavaClass().addGB18030FourByte(text)

      def addGS1(self, text):
            """!
            Adds codetext fragment in GS1 mode
            @param text: text Codetext string
            """
            self.getJavaClass().addGS1(text)

      def getExtendedCodetext(self):
            """!
            Returns codetext from Extended mode codetext builder
            @return: Codetext in Extended mode
            """
            return self.getJavaClass().getExtendedCodetext()

class AztecExtCodetextBuilder(ExtCodetextBuilder):
      """!
       Extended codetext generator for Aztec barcodes for ExtendedCodetext Mode of AztecEncodeMode
       Use TwoDDisplayText property of BarcodeGenerator to set visible text to removing managing characters.

       This sample shows how to use AztecExtCodetextBuilder in Extended Mode.

       \code
		# create codetext
		textBuilder = Generation.AztecExtCodetextBuilder()
		textBuilder.addECICodetext(Generation.ECIEncodings.Win1251, "Will")
		textBuilder.addECICodetext(Generation.ECIEncodings.UTF8, "犬Right狗")
		textBuilder.addECICodetext(Generation.ECIEncodings.UTF16BE, "犬Power狗")
		textBuilder.addPlainCodetext("Plain text")
		# generate codetext
		codetext = textBuilder.getExtendedCodetext()
		# generate
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.AZTEC, codetext)
		generator.getParameters().getBarcode().getCodeTextParameters().setTwoDDisplayText("My Text")
		generator.save(self.image_path_to_save5, Generation.BarCodeImageFormat.BMP)
       \endcode
      """
      JAVA_CLASS_NAME = "com.aspose.mw.barcode.generation.MwAztecExtCodetextBuilder"

      def __init__(self):
            java_class_link = jpype.JClass(AztecExtCodetextBuilder.JAVA_CLASS_NAME)
            javaClass = java_class_link()
            super().__init__(javaClass)

      def init(self):
            pass

      def getExtendedCodetext(self):
            """!
            Generates Extended codetext from the extended codetext list.
            @return: Extended codetext as string
            """
            return self.getJavaClass().getExtendedCodetext()

class ImageParameters(Assist.BaseJavaClass):
      """!
      Image parameters.
      """

      def __init__(self, javaClass):
          self.svg = None
          super().__init__(javaClass)



      def init(self):
            self.svg = SvgParameters(self.getJavaClass().getSvg())

      def getSvg(self):
            """!
            SVG parameters
            """
            # self.svg = self.getJavaClass().getSvg()
            return self.svg

      def setSvg(self, svg):
            """!
            SVG parameters
            """
            self.svg = svg
            self.getJavaClass().setSvg(svg.getJavaClass())

class SvgParameters(Assist.BaseJavaClass):
      """!
      SVG parameters.
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)

      def init(self):
            pass

      def isExplicitSizeInPixels(self):
            """!
            Does SVG image contain explicit size in pixels (recommended)
            Default value: True.
            """
            return self.getJavaClass().isExplicitSizeInPixels()

      def setExplicitSizeInPixels(self, explicitSizeInPixels):
            """!
            Does SVG image contain explicit size in pixels (recommended)
            Default value: True.
            """
            self.getJavaClass().setExplicitSizeInPixels(explicitSizeInPixels)

      def isTextDrawnInTextElement(self):
            """!
            Does SVG image contain text as text element rather than paths (recommended)
            Default value: True.
            """
            return self.getJavaClass().isTextDrawnInTextElement()

      def setTextDrawnInTextElement(self, textDrawnInTextElement):
            """!
            Does SVG image contain text as text element rather than paths (recommended)
            Default value: True.
            """
            self.getJavaClass().setTextDrawnInTextElement(textDrawnInTextElement)


      def setSvgColorMode(self,svgColorMode):
           """!
          Possible modes for filling color in svg file, RGB is default and supported by SVG 1.1.
          RGBA, HSL, HSLA is allowed in SVG 2.0 standard.
          Even in RGB opacity will be set through "fill-opacity" parameter
          """
           self.getJavaClass().setSvgColorMode(svgColorMode.value)

      def getSvgColorMode(self):
            """!
           Possible modes for filling color in svg file, RGB is default and supported by SVG 1.1.
           RGBA, HSL, HSLA is allowed in SVG 2.0 standard.
           Even in RGB opacity will be set through "fill-opacity" parameter
           """
            return SvgColorMode(self.getJavaClass().getSvgColorMode())

class HslaColor:
      """!
      Class for representing HSLA color (Hue, Saturation, Lightness, Alpha)
      """

      def __init__(self, h, s, l, a):
            """!
            Constructor for HslaColor
            @param h: Hue [0, 360]
            @param s: Saturation [0, 100]
            @param l: Lightness [0, 100]
            @param a: Alpha (opacity) [0.0f, 1.0f]
            """
            self.checkHue(h)
            self.checkSatLight(s)
            self.checkSatLight(l)
            self.checkAlpha(a)

            self.H = h
            self.S = s
            self.L = l
            self.A = a

      @staticmethod
      def checkHue(value):
            if (value < 0 or value > 360):
                  raise Exception("Wrong color value")

      @staticmethod
      def checkSatLight(value):
            if (value < 0 or value > 100):
                  raise Exception("Wrong color value")

      @staticmethod
      def checkAlpha(value):
            if ((value < 0.0) or (value > 1.0)):
                  raise Exception("Wrong color value")

      @staticmethod
      def convertHslaToRgba(hslaColor):
            r = 0
            g = 0
            b = 0

            hueF = hslaColor.H / 360.0
            satF = hslaColor.S / 100.0
            lightF = hslaColor.L / 100.0

            if (satF == 0):
                  r = g = b = lightF
            else :
                  if lightF < 0.5:
                        q = lightF * (1 + satF)
                  else:
                        q = lightF + satF - lightF * satF
                        p = 2 * lightF - q

                        r = HslaColor.hueToRgb(p, q, hueF + 1.0 / 3.0)
                        g = HslaColor.hueToRgb(p, q, hueF)
                        b = HslaColor.hueToRgb(p, q, hueF - 1.0 / 3.0)

            rI = int(r * 255 + 0.5)
            gI = int(g * 255 + 0.5)
            bI = int(b * 255 + 0.5)
            aI = int(hslaColor.A * 255 + 0.5)

            return ( rI, gI, bI, aI)

      @staticmethod
      def hueToRgb(p, q, t):
            if (t < 0.0):
                  t += 1.0
            if (t > 1.0):
                  t -= 1.0
            if (t < 1.0 / 6.0):
                  return p + (q - p) * 6.0 * t
            if (t < 1.0 / 2.0):
                  return q
            if (t < 2.0 / 3.0):
                  return p + (q - p) * (2.0 / 3.0 - t) * 6.0
            return p

class MacroCharacter(Enum):
      """!
        Macro Characters 05 and 06 values are used to obtain more compact encoding in special modes.
        05 Macro craracter is translated to "[)>\u001E05\u001D" as decoded data header and "\u001E\u0004" as decoded data trailer.
        06 Macro craracter is translated to "[)>\u001E06\u001D" as decoded data header and "\u001E\u0004" as decoded data trailer.
        here samples show how to encode Macro Characters in MicroPdf417 and DataMatrix
        \code
		# to generate autoidentified GS1 message like this "(10)123ABC(10)123ABC" in ISO 15434 format you need:
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.DATA_MATRIX, "10123ABC\u001D10123ABC")
		generator.getParameters().getBarcode().getDataMatrix().setMacroCharacters(Generation.MacroCharacter.MACRO_05)
		reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.GS_1_DATA_MATRIX)
		for result in reader.readBarCodes():
		print("\nBarCode CodeText: " + result.getCodeText())

		# Encodes MicroPdf417 with 05 Macro the string: "[)>\u001E05\u001Dabcde1234\u001E\u0004"
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.MICRO_PDF_417, "abcde1234")
		generator.getParameters().getBarcode().getPdf417().setMacroCharacters(Generation.MacroCharacter.MACRO_05)
		reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.MICRO_PDF_417)
		for result in reader.readBarCodes():
	    print("BarCode CodeText: " + result.getCodeText())

		# Encodes MicroPdf417 with 06 Macro the string: "[)>\u001E06\u001Dabcde1234\u001E\u0004"
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.MICRO_PDF_417, "abcde1234")
		generator.getParameters().getBarcode().getPdf417().setMacroCharacters(Generation.MacroCharacter.MACRO_06)
		reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None, Recognition.DecodeType.MICRO_PDF_417)
		for result in reader.readBarCodes():
		print("BarCode CodeText: " + result.getCodeText())
       \endcode
      """

      ## None of Macro Characters are added to barcode data
      NONE = 0
      ##
      # 05 Macro craracter is added to barcode data in first position.
      #  GS1 Data Identifier ISO 15434
      #  Character is translated to "[)>\u001E05\u001D" as decoded data header and "\u001E\u0004" as decoded data trailer.
      #  to generate autoidentified GS1 message like this "(10)123ABC(10)123ABC" in ISO 15434 format you need:
      #  \code
      #   generator = Generation.BarcodeGenerator(Generation.EncodeTypes.DATA_MATRIX, "10123ABC\u001D10123ABC")
      #  #to generate autoidentified GS1 message like this "(10)123ABC(10)123ABC" in ISO 15434 format you need:
      #   generator.getParameters().getBarcode().getDataMatrix().setMacroCharacters(Generation.MacroCharacter.MACRO_05)
        # #to generate autoidentified GS1 message like this "(10)123ABC(10)123ABC" in ISO 15434 format you need:
        # reader = Recognition.BarCodeReader(generator.generateBarCodeImage(), None,Recognition.DecodeType.GS_1_DATA_MATRIX)
        # #to generate autoidentified GS1 message like this "(10)123ABC(10)123ABC" in ISO 15434 format you need:
        # results = reader.readBarCodes()
        # for result in results:
        #     print(f"\nBarCode Type: {result.getCodeTypeName()}")
        #     print(f"BarCode CodeText: {result.getCodeText()}")
       # \endcode
      MACRO_05 = 5

      ## 06 Macro craracter is added to barcode data in first position.
      # ASC MH10 Data Identifier ISO 15434
      # Character is translated to "[)>\u001E06\u001D" as decoded data header and "\u001E\u0004" as decoded data trailer.
      MACRO_06 = 6

class BarcodeClassifications(Enum):
      """!
      BarcodeClassifications EncodeTypes classification
      """
      ## Unspecified classification
      NONE = 0

      ## Specifies 1D-barcode
      TYPE_1D = 1

      ## Specifies 2D-barcode
      TYPE_2D = 2

      ## Specifies POSTAL-barcode
      POSTAL = 3

      ## Specifies DataBar-barcode
      DATABAR = 4

      ## Specifies COUPON-barcode
      COUPON = 5

class FontStyle(Enum):
      """!
      Specifies style information applied to text.
      """

      ## Normal text
      REGULAR = 0

      ## Bold text
      BOLD = 1

      ## Italic text
      ITALIC = 2

      ## Underlined text
      UNDERLINE = 4

      ## Text with a line through the middle
      STRIKEOUT = 8

class CodabarSymbol:
      """!
      Specifies the start or stop symbol of the Codabar barcode specification.
      """

      ## Specifies character A as the start or stop symbol of the Codabar barcode specification.
      A = 65

      ## Specifies character B as the start or stop symbol of the Codabar barcode specification.
      B = 66

      ## Specifies character C as the start or stop symbol of the Codabar barcode specification.
      C = 67

      ## Specifies character D as the start or stop symbol of the Codabar barcode specification.
      D = 68


class DataMatrixEncodeMode(Enum):
      """!
       DataMatrix encoder's encoding mode, default to Auto
       
       This sample shows how to do codetext in Extended Mode.

       #Auto mode
		codetext = "犬Right狗"
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.DATA_MATRIX, codetext)
		generator.getParameters().getBarcode().getDataMatrix().setECIEncoding(Generation.ECIEncodings.UTF8)
		generator.save(self.image_path_to_save5, Generation.BarCodeImageFormat.PNG)
		# Binary mode
		encodedArr = [0xFF, 0xFE, 0xFD, 0xFC, 0xFB, 0xFA, 0xF9]
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.DATA_MATRIX, None)
		generator.setCodeText(encodedArr, None)
		generator.getParameters().getBarcode().getDataMatrix().setDataMatrixEncodeMode(
		Generation.DataMatrixEncodeMode.BINARY)
		generator.save(self.image_path_to_save5, Generation.BarCodeImageFormat.PNG)
		# Extended codetext mode
		# create codetext
		codetextBuilder = Generation.DataMatrixExtCodetextBuilder()
		codetextBuilder.addECICodetextWithEncodeMode(Generation.ECIEncodings.Win1251, Generation.DataMatrixEncodeMode.BYTES, "World")
		codetextBuilder.addPlainCodetext("Will")
		codetextBuilder.addECICodetext(Generation.ECIEncodings.UTF8, "犬Right狗")
		codetextBuilder.addCodetextWithEncodeMode(Generation.DataMatrixEncodeMode.C40, "ABCDE")
		# generate codetext
		codetext = codetextBuilder.getExtendedCodetext()
		# generate
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.DATA_MATRIX, codetext)
		generator.getParameters().getBarcode().getDataMatrix().setDataMatrixEncodeMode(
			Generation.DataMatrixEncodeMode.EXTENDED_CODETEXT)
		generator.save(self.image_path_to_save5, Generation.BarCodeImageFormat.PNG)
      """

      ## In Auto mode, the CodeText is encoded with maximum data compactness.
      # Unicode characters are re-encoded in the ECIEncoding specified encoding with the insertion of an ECI identifier.
      # If a character is found that is not supported by the selected ECI encoding, an exception is thrown.
      AUTO = 0
      
      ## Encodes one alphanumeric or two numeric characters per byte
      ASCII = 1
      
      ## Encode 8 bit values
      # @deprecated This property is obsolete and will be removed in future releases. Instead, use Base256 option.
      BYTES = 6
      
      ## Uses C40 encoding. Encodes Upper-case alphanumeric, Lower case and special characters
      C40 = 8
      
      ## Uses Text encoding. Encodes Lower-case alphanumeric, Upper case and special characters
      TEXT = 9
      
      ## Uses EDIFACT encoding. Uses six bits per character, encodes digits, upper-case letters, and many punctuation marks, but has no support for lower-case letters.
      EDIFACT = 10
      
      ## Uses ANSI X12 encoding.
      ANSIX12 = 11
      
      ## ExtendedCodetext mode allows to manually switch encodation schemes and ECI encodings in codetext.
      # It is better to use DataMatrixExtCodetextBuilder for extended codetext generation.
      # Use Display2DText property to set visible text to removing managing characters.
      # ECI identifiers are set as single slash and six digits identifier "\000026" - UTF8 ECI identifier
      # All unicode characters after ECI identifier are automatically encoded into correct character codeset.
      #
      # Encodation schemes are set in the next format : "\Encodation_scheme_name:text\Encodation_scheme_name:text".
      # Allowed encodation schemes are: EDIFACT, ANSIX12, ASCII, C40, Text, Auto.
      #
      # All backslashes (\) must be doubled in text.
      #
      # @deprecated This property is obsolete and will be removed in future releases. Instead, use the 'Extended' encode mode
      EXTENDED_CODETEXT = 12
      
      ## ExtendedCodetext mode allows to manually switch encodation schemes and ECI encodings in codetext.
      # It is better to use DataMatrixExtCodetextBuilder for extended codetext generation.
      # Use Display2DText property to set visible text to removing managing characters.
      # ECI identifiers are set as single slash and six digits identifier "\000026" - UTF8 ECI identifier
      # All unicode characters after ECI identifier are automatically encoded into correct character codeset.
      #
      # Encodation schemes are set in the next format : "\Encodation_scheme_name:text\Encodation_scheme_name:text".
      # Allowed encodation schemes are: EDIFACT, ANSIX12, ASCII, C40, Text, Auto.
      #
      # All backslashes (\) must be doubled in text.
      EXTENDED = 13
      
      ## Encode 8 bit values
      BASE_256 = 14
      
      ## In Binary mode, the CodeText is encoded with maximum data compactness.
      # If a Unicode character is found, an exception is thrown.
      BINARY = 15
      
      ## In ECI mode, the entire message is re-encoded in the ECIEncoding specified encoding with the insertion of an ECI identifier.
      # If a character is found that is not supported by the selected ECI encoding, an exception is thrown.
      # Please note that some old (pre 2006) scanners may not support this mode.
      ECI = 16

class BorderDashStyle(Enum):
      """!
      Specifies the style of dashed border lines.
      """

      ## Specifies a solid line.
      SOLID = 0

      ## Specifies a line consisting of dashes.
      DASH = 1

      ## Specifies a line consisting of dots.
      DOT = 2

      ## Specifies a line consisting of a repeating pattern of dash-dot.
      DASH_DOT = 3

      ## Specifies a line consisting of a repeating pattern of dash-dot-dot.
      DASH_DOT_DOT = 4

class ITF14BorderType(Enum):
      """!
      ITF14 barcode's border type
      """

      ## NO border enclosing the barcode
      NONE = 0

      ## FRAME enclosing the barcode
      FRAME = 1

      ## Tow horizontal bars enclosing the barcode
      BAR = 2

      ## FRAME enclosing the barcode
      FRAME_OUT = 3

      ## Tow horizontal bars enclosing the barcode
      BAR_OUT = 4


class QREncodeMode(Enum):
      """!
       Encoding mode for QR barcodes.
		# Example how to use ECI encoding
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.QR, "12345TEXT")
		generator.getParameters().getBarcode().getQR().setQrEncodeMode(Generation.QREncodeMode.ECI_ENCODING)
		generator.getParameters().getBarcode().getQR().setQrECIEncoding(Generation.ECIEncodings.UTF8)
		generator.save(self.image_path_to_save4, Generation.BarCodeImageFormat.PNG)

		# Example how to use FNC1 first position in Extended Mode
		textBuilder = Generation.QrExtCodetextBuilder()
		textBuilder.addPlainCodetext("000%89%%0")
		textBuilder.addFNC1GroupSeparator()
		textBuilder.addPlainCodetext("12345&lt;FNC1&gt;")
		# generate barcode
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.QR, None)
		generator.setCodeText(textBuilder.getExtendedCodetext(),"UTF-8")
		generator.getParameters().getBarcode().getQR().setQrEncodeMode(Generation.QREncodeMode.EXTENDED_CODETEXT)
		generator.getParameters().getBarcode().getCodeTextParameters().setTwoDDisplayText("My Text")
		generator.save(self.image_path_to_save6, Generation.BarCodeImageFormat.PNG)

		# This sample shows how to use FNC1 second position in Extended Mode.
		# create codetext
		textBuilder = Generation.QrExtCodetextBuilder()
		textBuilder.addFNC1SecondPosition("12")
		textBuilder.addPlainCodetext("TRUE3456")
		# generate barcode
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.QR, None)
		generator.setCodeText(textBuilder.getExtendedCodetext(), "UTF-8")
		generator.getParameters().getBarcode().getCodeTextParameters().setTwoDDisplayText("My Text")
		generator.save(self.image_path_to_save7, Generation.BarCodeImageFormat.PNG)

		# This sample shows how to use multi ECI mode in Extended Mode.
		# create codetext
		textBuilder = Generation.QrExtCodetextBuilder()
		textBuilder.addECICodetext(Generation.ECIEncodings.Win1251, "Will")
		textBuilder.addECICodetext(Generation.ECIEncodings.UTF8, "Right")
		textBuilder.addECICodetext(Generation.ECIEncodings.UTF16BE, "Power")
		textBuilder.addPlainCodetext("t\e\\st")
		# generate barcode
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.QR, "12345")
		generator.setCodeText(textBuilder.getExtendedCodetext(),"UTF-8")
		generator.getParameters().getBarcode().getQR().setQrEncodeMode(Generation.QREncodeMode.EXTENDED_CODETEXT)
		generator.getParameters().getBarcode().getCodeTextParameters().setTwoDDisplayText("My Text")
		generator.save(self.image_path_to_save8, Generation.BarCodeImageFormat.PNG)
       """

      ## In Auto mode, the CodeText is encoded with maximum data compactness.
      # Unicode characters are encoded in kanji mode if possible, or they are re-encoded in the ECIEncoding specified encoding with the insertion of an ECI identifier.
      # If a character is found that is not supported by the selected ECI encoding, an exception is thrown.
      AUTO = 0

      ## Encode codetext as plain bytes. If it detects any Unicode character, the character will be encoded as two bytes, lower byte first.
      # @deprecated This property is obsolete and will be removed in future releases. Instead, use the 'SetCodeText' method to convert the message to byte array with specified encoding.
      BYTES = 1

      ## Encode codetext with UTF8 encoding with first ByteOfMark character.
      # @deprecated This property is obsolete and will be removed in future releases. Instead, use the 'SetCodeText' method with UTF8 encoding to add a byte order mark (BOM) and encode the message. After that, the CodeText can be encoded using the 'Auto' mode.
      UTF_8_BOM = 2


      ## Encode codetext with UTF8 encoding with first ByteOfMark character. It can be problems with some barcode scanners.
      # @deprecated This property is obsolete and will be removed in future releases. Instead, use the 'SetCodeText' method with BigEndianUnicode encoding to add a byte order mark (BOM) and encode the message. After that, the CodeText can be encoded using the 'Auto' mode.
      UTF_16_BEBOM = 3

      ## Encode codetext with value set in the ECIEncoding property. It can be problems with some old (pre 2006) barcode scanners.
      # This mode is not supported by MicroQR barcodes.
      # @deprecated This property is obsolete and will be removed in future releases. Instead, use ECI option.
      ECI_ENCODING = 4

      ## Extended Channel mode which supports FNC1 first position, FNC1 second position and multi ECI modes.</para>
      # It is better to use QrExtCodetextBuilder for extended codetext generation.</para>
      # Use Display2DText property to set visible text to removing managing characters.</para>
      # Encoding Principles:</para>
      # All symbols "\" must be doubled "\\" in the codetext.</para>
      # FNC1 in first position is set in codetext as as "&lt;FNC1&gt;"</para>
      # FNC1 in second position is set in codetext as as "&lt;FNC1(value)&gt;". The value must be single symbols (a-z, A-Z) or digits from 0 to 99.</para>
      # Group Separator for FNC1 modes is set as 0x1D character '\\u001D' </para>
      # If you need to insert "&lt;FNC1&gt;" string into barcode write it as "&lt;\FNC1&gt;" </para>
      # ECI identifiers are set as single slash and six digits identifier "\000026" - UTF8 ECI identifier</para>
      # To disable current ECI mode and convert to default JIS8 mode zero mode ECI indetifier is set. "\000000"</para>
      # All unicode characters after ECI identifier are automatically encoded into correct character codeset.</para>
      # This mode is not supported by MicroQR barcodes.</para>
      # @deprecated This property is obsolete and will be removed in future releases. Instead, use the 'Extended' encode mode.
      EXTENDED_CODETEXT = 5

      ## Extended Channel mode which supports FNC1 first position, FNC1 second position and multi ECI modes.</para>
      # It is better to use QrExtCodetextBuilder for extended codetext generation.</para>
      # Use Display2DText property to set visible text to removing managing characters.</para>
      # Encoding Principles:</para>
      # All symbols "\" must be doubled "\\" in the codetext.</para>
      # FNC1 in first position is set in codetext as as "&lt;FNC1&gt;"</para>
      # FNC1 in second position is set in codetext as as "&lt;FNC1(value)&gt;". The value must be single symbols (a-z, A-Z) or digits from 0 to 99.</para>
      # Group Separator for FNC1 modes is set as 0x1D character '\\u001D' </para>
      # If you need to insert "&lt;FNC1&gt;" string into barcode write it as "&lt;\FNC1&gt;" </para>
      # ECI identifiers are set as single slash and six digits identifier "\000026" - UTF8 ECI identifier</para>
      # To disable current ECI mode and convert to default JIS8 mode zero mode ECI indetifier is set. "\000000"</para>
      # All unicode characters after ECI identifier are automatically encoded into correct character codeset.</para>
      # This mode is not supported by MicroQR barcodes.</para>
      EXTENDED = 6

      ## In Binary mode, the CodeText is encoded with maximum data compactness.
      # If a Unicode character is found, an exception is thrown.
      BINARY = 7

      ## In ECI mode, the entire message is re-encoded in the ECIEncoding specified encoding with the insertion of an ECI identifier.
      # If a character is found that is not supported by the selected ECI encoding, an exception is thrown.
      # Please note that some old (pre 2006) scanners may not support this mode.
      # This mode is not supported by MicroQR barcodes.
      ECI = 8

class DataMatrixEccType(Enum):
      """!
      Specify the type of the ECC to encode.
      """

      ## Specifies that encoded Ecc type is defined by default Reed-Solomon error correction or ECC 200.
      ECC_AUTO = 0

      ## Specifies that encoded Ecc type is defined ECC 000.
      ECC_000 = 1

      ## Specifies that encoded Ecc type is defined ECC 050.
      ECC_050 = 2

      ## Specifies that encoded Ecc type is defined ECC 080.
      ECC_080 = 3

      ## Specifies that encoded Ecc type is defined ECC 100.
      ECC_100 = 4

      ## Specifies that encoded Ecc type is defined ECC 140.
      ECC_140 = 5

      ## Specifies that encoded Ecc type is defined ECC 200. Recommended to use.
      ECC_200 = 6

class QRVersion(Enum):
      """!
      Version of QR Code.
      From Version1 to Version40 for QR code and from M1 to M4 for MicroQr.
      """

      ## Specifies to automatically pick up the best version for QR.
      #This is default value.
      AUTO = 0

      ## Specifies version 1 with 21 x 21 modules.
      VERSION_01 = 1

      ## Specifies version 2 with 25 x 25 modules.
      VERSION_02 = 2

      ## Specifies version 3 with 29 x 29 modules
      VERSION_03 = 3

      ## Specifies version 4 with 33 x 33 modules.
      VERSION_04 = 4

      ## Specifies version 5 with 37 x 37 modules.
      VERSION_05 = 5

      ## Specifies version 6 with 41 x 41 modules.
      VERSION_06 = 6

      ## Specifies version 7 with 45 x 45 modules.
      VERSION_07 = 7

      ## Specifies version 8 with 49 x 49 modules.
      VERSION_08 = 8

      ## Specifies version 9 with 53 x 53 modules.
      VERSION_09 = 9

      ## Specifies version 10 with 57 x 57 modules.
      VERSION_10 = 10

      ## Specifies version 11 with 61 x 61 modules.
      VERSION_11 = 11

      ## Specifies version 12 with 65 x 65 modules.
      VERSION_12 = 12

      ## Specifies version 13 with 69 x 69 modules.
      VERSION_13 = 13

      ## Specifies version 14 with 73 x 73 modules.
      VERSION_14 = 14

      ## Specifies version 15 with 77 x 77 modules.
      VERSION_15 = 15

      ## Specifies version 16 with 81 x 81 modules.
      VERSION_16 = 16

      ## Specifies version 17 with 85 x 85 modules.
      VERSION_17 = 17

      ## Specifies version 18 with 89 x 89 modules.
      VERSION_18 = 18

      ## Specifies version 19 with 93 x 93 modules.
      VERSION_19 = 19

      ## Specifies version 20 with 97 x 97 modules.
      VERSION_20 = 20

      ## Specifies version 21 with 101 x 101 modules.
      VERSION_21 = 21

      ## Specifies version 22 with 105 x 105 modules
      VERSION_22 = 22

      ## Specifies version 23 with 109 x 109 modules.
      VERSION_23 = 23

      ## Specifies version 24 with 113 x 113 modules.
      VERSION_24 = 24

      ## Specifies version 25 with 117 x 117 modules.
      VERSION_25 = 25

      ## Specifies version 26 with 121 x 121 modules.
      VERSION_26 = 26

      ## Specifies version 27 with 125 x 125 modules.
      VERSION_27 = 27

      ## Specifies version 28 with 129 x 129 modules.
      VERSION_28 = 28

      ## Specifies version 29 with 133 x 133 modules.
      VERSION_29 = 29

      ## Specifies version 30 with 137 x 137 modules.
      VERSION_30 = 30

      ## Specifies version 31 with 141 x 141 modules.
      VERSION_31 = 31

      ## Specifies version 32 with 145 x 145 modules.
      VERSION_32 = 32

      ## Specifies version 33 with 149 x 149 modules.
      VERSION_33 = 33

      ## Specifies version 34 with 153 x 153 modules.
      VERSION_34 = 34

      ## Specifies version 35 with 157 x 157 modules.
      VERSION_35 = 35

      ## Specifies version 36 with 161 x 161 modules.
      VERSION_36 = 36

      ## Specifies version 37 with 165 x 165 modules
      VERSION_37 = 37

      ## Specifies version 38 with 169 x 169 modules.
      VERSION_38 = 38

      ## Specifies version 39 with 173 x 173 modules.
      VERSION_39 = 39

      ## Specifies version 40 with 177 x 177 modules.
      VERSION_40 = 40

      ## Specifies version M1 for Micro QR with 11 x 11 modules.
      VERSION_M1 = 101

      ## Specifies version M2 for Micro QR with 13 x 13 modules.
      VERSION_M2 = 102

      ## Specifies version M3 for Micro QR with 15 x 15 modules.
      VERSION_M3 = 103

      ## Specifies version M4 for Micro QR with 17 x 17 modules.
      VERSION_M4 = 104


class AztecSymbolMode(Enum):
      """!
      Specifies the Aztec symbol mode.

      \code
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.AZTEC, None)
		generator.setCodeText("154",None)
		generator.getParameters().getBarcode().getAztec().setAztecSymbolMode(Generation.AztecSymbolMode.RUNE)
		generator.save(self.image_path_to_save4, Generation.BarCodeImageFormat.PNG)
      \endcode
      """
      ## Specifies to automatically pick up the best symbol (COMPACT or FULL-range) for Aztec.
      # This is default value.
      AUTO = 0

      ## Specifies the COMPACT symbol for Aztec.
      # Aztec COMPACT symbol permits only 1, 2, 3 or 4 layers.
      COMPACT = 1

      ## Specifies the FULL-range symbol for Aztec.
      # Aztec FULL-range symbol permits from 1 to 32 layers.
      FULL_RANGE = 2

      ## Specifies the RUNE symbol for Aztec.
      # Aztec Runes are a series of small but distinct machine-readable marks. It permits only number value from 0 to 255.
      RUNE = 3


class Pdf417ErrorLevel(Enum):
      """!
      pdf417 barcode's error correction level, from level 0 to level 9, level 0 means no error correction, level 9 means best error correction
      """
      ## level = 0.
      LEVEL_0 = 0

      ## level = 1.
      LEVEL_1 = 1

      ## level = 2.
      LEVEL_2 = 2

      ## level = 3.
      LEVEL_3 = 3

      ## level = 4.
      LEVEL_4 = 4

      ## level = 5.
      LEVEL_5 = 5

      ## level = 6.
      LEVEL_6 = 6

      ## level = 7.
      LEVEL_7 = 7

      ## level = 8.
      LEVEL_8 = 8


class Pdf417CompactionMode(Enum):
      """!
      Pdf417 barcode's compation mode
      """

      ## auto detect compation mode
      AUTO = 0

      ## text compaction
      TEXT = 1

      ## numeric compaction mode
      NUMERIC = 2

      ## binary compaction mode
      BINARY = 3


class QRErrorLevel(Enum):
      """!
      Level of Reed-Solomon error correction. From low to high: LEVEL_L, LEVEL_M, LEVEL_Q, LEVEL_H.
      """

      ## Allows recovery of 7% of the code text
      LEVEL_L = 0

      ## Allows recovery of 15% of the code text
      LEVEL_M = 1

      ## Allows recovery of 25% of the code text
      LEVEL_Q = 2

      ## Allows recovery of 30% of the code text
      LEVEL_H = 3


class QREncodeType(Enum):
      """!
      QR / MicroQR selector mode. Select FORCE_QR for standard QR symbols, AUTO for MicroQR.
      FORCE_MICRO_QR is used for strongly MicroQR symbol generation if it is possible.
      """

      ## Mode starts barcode version negotiation from MicroQR V1
      AUTO = 0

      ## Mode starts barcode version negotiation from QR V1
      FORCE_QR = 1

      ## Mode starts barcode version negotiation from from MicroQR V1 to V4. If data cannot be encoded into MicroQR, exception is thrown.
      FORCE_MICRO_QR = 2


class CodabarChecksumMode(Enum):
      """!
      Specifies the checksum algorithm for Codabar
      """

      ## Specifies Mod 10 algorithm for Codabar.
      MOD_10 = 0

      ## Specifies Mod 16 algorithm for Codabar (recomended AIIM).
      MOD_16 = 1


class CodeLocation(Enum):
      """!
      Codetext location
      """

      ## Codetext below barcode.
      BELOW = 0

      ## Codetext above barcode.
      ABOVE = 1

      ## Hide codetext.
      NONE = 2

class FontMode(Enum):
      """!
      Font size mode.
      """

      ## Automatically calculate Font size based on barcode size.
      AUTO = 0

      ## Use Font sized defined by user.
      MANUAL = 1


class TextAlignment(Enum):
      """!
      Text alignment.
      """

      ## Left position.
      LEFT = 0

      ## Center position.
      CENTER = 1

      ## Right position.
      RIGHT = 2

class AutoSizeMode(Enum):
      """!
      Specifies the different types of automatic sizing modes.
      Default value is AutoSizeMode.NONE.
      This sample shows how to create and save a BarCode image.

      \code
           generator = BarcodeGenerator(EncodeTypes.DATA_MATRIX)
           generator.setAutoSizeMode(AutoSizeMode.NEAREST)
           generator.getBarCodeWidth().setMillimeters(50)
           generator.getBarCodeHeight().setInches(1.3f)
           generator.save("test.png", BarCodeImageFormat.PNG)
      \endcode
      """

      ## Automatic resizing is disabled. Default value.
      NONE = 0

      ## Barcode resizes to nearest lowest possible size
      # which are specified by BarCodeWidth and BarCodeHeight properties.
      ## Resizes barcode to specified size with little scaling
      # but it can be little damaged in some cases
      # because using interpolation for scaling.
      # Size can be specified by BarcodeGenerator.BarCodeWidth
      # and BarcodeGenerator.BarCodeHeight properties.
      #
      # This sample shows how to create and save a BarCode image in Scale mode.
      # \code
      # generator = Generation.BarcodeGenerator(Generation.EncodeTypes.DATA_MATRIX,"12345")
      # generator.getParameters().setAutoSizeMode(Generation.AutoSizeMode.NEAREST)
      # generator.getParameters().getImageWidth().setMillimeters(10)
      # generator.getParameters().getImageHeight().setInches(1.3)
      # generator.save(self.image_path_to_save4, Generation.BarCodeImageFormat.PNG)
      # \endcode
      NEAREST = 1

      INTERPOLATION = 2

class GraphicsUnit(Enum):
      """!
      Specifies the unit of measure for the given data.

      WORLD = 0 - Specifies the world coordinate system unit as the unit of measure.
      DISPLAY = 1 - Specifies the unit of measure of the display device. Typically pixels for video displays, and 1/100 inch for printers.
      PIXEL = 2 - Specifies a device pixel as the unit of measure.
      POINT = 3 - Specifies a printer's point  = 1/72 inch) as the unit of measure.
      INCH = 4 - Specifies the inch as the unit of measure.
      DOCUMENT = 5 - Specifies the document unit  = 1/300 inch) as the unit of measure.
      MILLIMETER = 6 - Specifies the millimeter as the unit of measure.
      """

      ## Specifies the world coordinate system unit as the unit of measure.
      WORLD = 0

      ## Specifies the unit of measure of the display device. Typically pixels for video displays, and 1/100 inch for printers.
      DISPLAY = 1

      ## Specifies a device pixel as the unit of measure.
      PIXEL = 2

      ## Specifies a printer's point  = 1/72 inch) as the unit of measure.
      POINT = 3
      ## Specifies the inch as the unit of measure.
      INCH = 4

      ## Specifies the document unit  = 1/300 inch) as the unit of measure.
      DOCUMENT = 5

      ## Specifies the millimeter as the unit of measure.
      MILLIMETER = 6


class EncodeTypes(Enum):
      """!
      Specifies the type of barcode to encode.
      """
      ## Unspecified encode type.
      NONE = -1

      ## Specifies that the data should be encoded with CODABAR barcode specification
      CODABAR = 0

      ## Specifies that the data should be encoded with CODE 11 barcode specification
      CODE_11 = 1

      ## Specifies that the data should be encoded with {@code <b>Code 39</b>} basic charset barcode specification: ISO/IEC 16388
      CODE_39 = 2

      ## Specifies that the data should be encoded with {@code <b>Code 39</b>} full ASCII charset barcode specification: ISO/IEC 16388
      CODE_39_FULL_ASCII = 3

      ## Specifies that the data should be encoded with {@code <b>CODE 93</b>} barcode specification
      CODE_93 = 5

      ## Specifies that the data should be encoded with CODE 128 barcode specification
      CODE_128 = 6

      ## Specifies that the data should be encoded with GS1 Code 128 barcode specification. The codetext must contains parentheses for AI.
      GS_1_CODE_128 = 7

      ## Specifies that the data should be encoded with EAN-8 barcode specification
      EAN_8 = 8

      ## Specifies that the data should be encoded with EAN-13 barcode specification
      EAN_13 = 9

      ## Specifies that the data should be encoded with EAN14 barcode specification
      EAN_14 = 10

      ## Specifies that the data should be encoded with SCC14 barcode specification
      SCC_14 = 11

      ## Specifies that the data should be encoded with SSCC18 barcode specification
      SSCC_18 = 12

      ## Specifies that the data should be encoded with UPC-A barcode specification
      UPCA = 13

      ## Specifies that the data should be encoded with UPC-E barcode specification
      UPCE = 14

      ## Specifies that the data should be encoded with isBN barcode specification
      ISBN = 15

      ## Specifies that the data should be encoded with ISSN barcode specification
      ISSN = 16

      ## Specifies that the data should be encoded with ISMN barcode specification
      ISMN = 17
      ## Specifies that the data should be encoded with Standard 2 of 5 barcode specification
      STANDARD_2_OF_5 = 18

      ## Specifies that the data should be encoded with INTERLEAVED 2 of 5 barcode specification
      INTERLEAVED_2_OF_5 = 19

      ## Represents Matrix 2 of 5 BarCode
      MATRIX_2_OF_5 = 20

      ## Represents Italian Post 25 barcode.
      ITALIAN_POST_25 = 21

      ## Represents IATA 2 of 5 barcode.IATA (International Air Transport Assosiation) uses this barcode for the management of air cargo.
      IATA_2_OF_5 = 22

      ## Specifies that the data should be encoded with ITF14 barcode specification
      ITF_14 = 23

      ## Represents ITF-6  Barcode.
      ITF_6 = 24

      ## Specifies that the data should be encoded with MSI Plessey barcode specification
      MSI = 25

      ## Represents VIN (Vehicle Identification Number) Barcode.
      VIN = 26

      ## Represents Deutsch Post barcode, This EncodeType is also known as Identcode,CodeIdentcode,German Postal 2 of 5 Identcode,
      ## Deutsch Post AG Identcode, Deutsch Frachtpost Identcode,  Deutsch Post AG (DHL)
      DEUTSCHE_POST_IDENTCODE = 27

      ## Represents Deutsch Post Leitcode Barcode,also known as German Postal 2 of 5 Leitcode, CodeLeitcode, Leitcode, Deutsch Post AG (DHL).
      DEUTSCHE_POST_LEITCODE = 28

      ## Represents OPC(Optical Product Code) Barcode,also known as , VCA Barcode VCA OPC, Vision Council of America OPC Barcode.
      OPC = 29

      ## Represents PZN barcode.This EncodeType is also known as Pharmacy central number, Pharmazentralnummer
      PZN = 30

      ## Represents Code 16K barcode.
      CODE_16_K = 31

      ## Represents Pharmacode barcode.
      PHARMACODE = 32

      ## 2D barcode symbology DataMatrix
      DATA_MATRIX = 33

      ## Specifies that the data should be encoded with QR Code barcode specification
      QR = 34

      ## Specifies that the data should be encoded with Aztec barcode specification
      AZTEC = 35

      ## Specifies that the data should be encoded with {@code <b>GS1 Aztec</b>} barcode specification. The codetext must contains parentheses for AI.
      GS_1_AZTEC = 81

      ## Specifies that the data should be encoded with Pdf417 barcode specification
      PDF_417 = 36

      ## Specifies that the data should be encoded with MacroPdf417 barcode specification
      MACRO_PDF_417 = 37

      ## 2D barcode symbology DataMatrix with GS1 string format
      GS_1_DATA_MATRIX = 48

      ## Specifies that the data should be encoded with MicroPdf417 barcode specification
      MICRO_PDF_417 = 55

      ## Specifies that the data should be encoded with <b>GS1MicroPdf417</b> barcode specification
      GS_1_MICRO_PDF_417 = 82

      ## 2D barcode symbology QR with GS1 string format
      GS_1_QR = 56

      ## Specifies that the data should be encoded with MaxiCode barcode specification
      MAXI_CODE = 57

      ## Specifies that the data should be encoded with DotCode barcode specification
      DOT_CODE = 60

      ## Represents Australia Post Customer BarCode
      AUSTRALIA_POST = 38

      ## Specifies that the data should be encoded with Postnet barcode specification
      POSTNET = 39

      ## Specifies that the data should be encoded with Planet barcode specification
      PLANET = 40

      ## Specifies that the data should be encoded with USPS OneCode barcode specification
      ONE_CODE = 41

      ## Represents RM4SCC barcode. RM4SCC (Royal Mail 4-state Customer Code) is used for automated mail sort process in UK.
      RM_4_SCC = 42

      ## Represents Royal Mail Mailmark barcode.
      MAILMARK = 66

      ## Specifies that the data should be encoded with GS1 Databar omni-directional barcode specification.
      DATABAR_OMNI_DIRECTIONAL = 43

      ## Specifies that the data should be encoded with GS1 Databar truncated barcode specification.
      DATABAR_TRUNCATED = 44

      ## Represents GS1 DATABAR limited barcode
      DATABAR_LIMITED = 45

      ## Represents GS1 Databar expanded barcode.
      DATABAR_EXPANDED = 46

      ## Represents GS1 Databar expanded stacked barcode.
      DATABAR_EXPANDED_STACKED = 52

      ## Represents GS1 Databar stacked barcode.
      DATABAR_STACKED = 53

      ## Represents GS1 Databar stacked omni-directional barcode.
      DATABAR_STACKED_OMNI_DIRECTIONAL = 54

      ## Specifies that the data should be encoded with Singapore Post Barcode barcode specification
      SINGAPORE_POST = 47

      ## Specifies that the data should be encoded with Australian Post Domestic eParcel Barcode barcode specification
      AUSTRALIAN_POSTE_PARCEL = 49

      ## Specifies that the data should be encoded with Swiss Post Parcel Barcode barcode specification. Supported types: Domestic Mail, International Mail, Additional Services (new)
      SWISS_POST_PARCEL = 50

      ## Represents Patch code barcode
      PATCH_CODE = 51

      ## Specifies that the data should be encoded with Code32 barcode specification
      CODE_32 = 58

      ## Specifies that the data should be encoded with DataLogic 2 of 5 barcode specification
      DATA_LOGIC_2_OF_5 = 59

      ## Specifies that the data should be encoded with Dutch KIX barcode specification
      DUTCH_KIX = 61

      ## Specifies that the data should be encoded with UPC coupon with GS1-128 Extended Code barcode specification.
      # An example of the input string:
      # <br><b>generator.setCodeText("514141100906(8102)03", None)</b><br>
      # where UPCA part is "514141100906", GS1Code128 part is (8102)03.
      # \code
      # generator = Generation.BarcodeGenerator(Generation.EncodeTypes.CODE_128, None)
      # generator.setCodeText("514141100906(8102)03", None),
      # generator.save(self.image_path_to_save4, Generation.BarCodeImageFormat.PNG)
      # \endcode
      UPCA_GS_1_CODE_128_COUPON = 62

      ## Specifies that the data should be encoded with UPC coupon with GS1 DataBar addition barcode specification.
      # An example of the input string:<br>
      # <b>generator.setCodeText("514141100906(8110)106141416543213500110000310123196000", None),</b><br>
      # where UPCA part is "514141100906", DATABAR part is "(8110)106141416543213500110000310123196000".
      # To change the caption, use<br>
      # <b>generator.getParameters().getCaptionAbove().setText("company prefix + offer code")</b><br>
      # \code
      # generator = Generation.BarcodeGenerator(Generation.EncodeTypes.CODE_128, None)
      # generator.setCodeText("514141100906(8110)106141416543213500110000310123196000", None)
      # generator.getParameters().getCaptionAbove().setText("company prefix + offer code")
      # generator.save(self.image_path_to_save4, Generation.BarCodeImageFormat.PNG)
      # \endcode
      UPCA_GS_1_DATABAR_COUPON = 63

      ## Specifies that the data should be encoded with Codablock-F barcode specification.
      CODABLOCK_F = 64

      ## Specifies that the data should be encoded with GS1 Codablock-F barcode specification. The codetext must contains parentheses for AI.
      GS_1_CODABLOCK_F = 65

      ## Specifies that the data should be encoded with <b>GS1 Composite Bar</b> barcode specification. The codetext must contains parentheses for AI. 1D codetext and 2D codetext must be separated with symbol '/'
      GS_1_COMPOSITE_BAR = 67

      ## Specifies that the data should be encoded with {@code <b>HIBC LIC Code39Standart</b>} barcode specification.
      HIBC_CODE_39_LIC = 68

      ## Specifies that the data should be encoded with {@code <b>HIBC LIC Code128</b>} barcode specification.
      HIBC_CODE_128_LIC = 69

      ## Specifies that the data should be encoded with {@code <b>HIBC LIC Aztec</b>} barcode specification.
      HIBC_AZTEC_LIC = 70

      ## Specifies that the data should be encoded with {@code <b>HIBC LIC DataMatrix</b>} barcode specification.
      HIBC_DATA_MATRIX_LIC = 71

      ## Specifies that the data should be encoded with {@code <b>HIBC LIC QR</b>} barcode specification.
      HIBCQRLIC = 72

      ## Specifies that the data should be encoded with {@code <b>HIBC PAS Code39Standart</b>} barcode specification.
      HIBC_CODE_39_PAS = 73

      ## Specifies that the data should be encoded with {@code <b>HIBC PAS Code128</b>} barcode specification.
      HIBC_CODE_128_PAS = 74

      ## Specifies that the data should be encoded with {@code <b>HIBC PAS Aztec</b>} barcode specification.
      HIBC_AZTEC_PAS = 75

      ## Specifies that the data should be encoded with {@code <b>HIBC PAS DataMatrix</b>} barcode specification.
      HIBC_DATA_MATRIX_PAS = 76

      ## Specifies that the data should be encoded with {@code <b>HIBC PAS QR</b>} barcode specification.
      HIBCQRPAS = 77

      ## Specifies that the data should be encoded with {@code <b>GS1 DotCode</b>} barcode specification. The codetext must contains parentheses for AI.
      GS_1_DOT_CODE = 78

      ## Specifies that the data should be encoded with <b>Han Xin</b> barcode specification
      HAN_XIN = 79

      ## 2D barcode symbology QR with GS1 string format
      GS_1_HAN_XIN = 80
      
      ## Specifies that the data should be encoded with <b>MicroQR Code</b> barcode specification
      MICRO_QR = 83

      ## Specifies that the data should be encoded with <b>RectMicroQR (rMQR) Code</b> barcode specification
      RECT_MICRO_QR = 84

      @staticmethod
      def parse(encodeTypeName):
            if encodeTypeName == "CODABAR":
                  return 0

            elif encodeTypeName == "CODE_11":
                  return 1

            elif encodeTypeName == "CODE_39":
                  return 2

            elif encodeTypeName == "CODE_39_FULL_ASCII":
                  return 3

            elif encodeTypeName == "CODE_93":
                  return 5

            elif encodeTypeName == "CODE_128":
                  return 6

            elif encodeTypeName == "GS_1_CODE_128":
                  return 7

            elif encodeTypeName == "EAN_8":
                  return 8

            elif encodeTypeName == "EAN_13":
                  return 9

            elif encodeTypeName == "EAN_14":
                  return 10

            elif encodeTypeName == "SCC_14":
                  return 11

            elif encodeTypeName == "SSCC_18":
                  return 12

            elif encodeTypeName == "UPCA":
                  return 13

            elif encodeTypeName == "UPCE":
                  return 14

            elif encodeTypeName == "ISBN":
                  return 15

            elif encodeTypeName == "ISSN":
                  return 16

            elif encodeTypeName == "ISMN":
                  return 17

            elif encodeTypeName == "STANDARD_2_OF_5":
                  return 18

            elif encodeTypeName == "INTERLEAVED_2_OF_5":
                  return 19

            elif encodeTypeName == "MATRIX_2_OF_5":
                  return 20

            elif encodeTypeName == "ITALIAN_POST_25":
                  return 21

            elif encodeTypeName == "IATA_2_OF_5":
                  return 22

            elif encodeTypeName == "ITF_14":
                  return 23

            elif encodeTypeName == "ITF_6":
                  return 24

            elif encodeTypeName == "MSI":
                  return 25

            elif encodeTypeName == "VIN":
                  return 26

            elif encodeTypeName == "DEUTSCHE_POST_IDENTCODE":
                  return 27

            elif encodeTypeName == "DEUTSCHE_POST_LEITCODE":
                  return 28

            elif encodeTypeName == "OPC":
                  return 29

            elif encodeTypeName == "PZN":
                  return 30

            elif encodeTypeName == "CODE_16_K":
                  return 31

            elif encodeTypeName == "PHARMACODE":
                  return 32

            elif encodeTypeName == "DATA_MATRIX":
                  return 33

            elif encodeTypeName == "QR":
                  return 34

            elif encodeTypeName == "AZTEC":
                  return 35

            elif encodeTypeName == "GS_1_AZTEC":
                  return 81

            elif encodeTypeName == "PDF_417":
                  return 36

            elif encodeTypeName == "MACRO_PDF_417":
                  return 37

            elif encodeTypeName == "GS_1_DATA_MATRIX":
                  return 48

            elif encodeTypeName == "MICRO_PDF_417":
                  return 55

            elif encodeTypeName == "GS_1_QR":
                  return 56

            elif encodeTypeName == "MAXI_CODE":
                  return 57

            elif encodeTypeName == "DOT_CODE":
                  return 60

            elif encodeTypeName == "AUSTRALIA_POST":
                  return 38

            elif encodeTypeName == "POSTNET":
                  return 39

            elif encodeTypeName == "PLANET":
                  return 40

            elif encodeTypeName == "ONE_CODE":
                  return 41

            elif encodeTypeName == "RM_4_SCC":
                  return 42

            elif encodeTypeName == "MAILMARK":
                  return 66

            elif encodeTypeName == "DATABAR_OMNI_DIRECTIONAL":
                  return 43

            elif encodeTypeName == "DATABAR_TRUNCATED":
                  return 44

            elif encodeTypeName == "DATABAR_LIMITED":
                  return 45

            elif encodeTypeName == "DATABAR_EXPANDED":
                  return 46

            elif encodeTypeName == "DATABAR_EXPANDED_STACKED":
                  return 52

            elif encodeTypeName == "DATABAR_STACKED":
                  return 53

            elif encodeTypeName == "DATABAR_STACKED_OMNI_DIRECTIONAL":
                  return 54

            elif encodeTypeName == "SINGAPORE_POST":
                  return 47

            elif encodeTypeName == "AUSTRALIAN_POSTE_PARCEL":
                  return 49

            elif encodeTypeName == "SWISS_POST_PARCEL":
                  return 50

            elif encodeTypeName == "PATCH_CODE":
                  return 51

            elif encodeTypeName == "CODE_32":
                  return 58

            elif encodeTypeName == "DATA_LOGIC_2_OF_5":
                  return 59

            elif encodeTypeName == "DUTCH_KIX":
                  return 61

            elif encodeTypeName == "UPCA_GS_1_CODE_128_COUPON":
                  return 62

            elif encodeTypeName == "UPCA_GS_1_DATABAR_COUPON":
                  return 63

            elif encodeTypeName == "CODABLOCK_F":
                  return 64

            elif encodeTypeName == "GS_1_CODABLOCK_F":
                  return 65

            elif encodeTypeName == "GS_1_COMPOSITE_BAR":
                  return 67

            elif encodeTypeName == "HIBC_CODE_39_LIC":
                  return 68

            elif encodeTypeName == "HIBC_CODE_128_LIC":
                  return 69

            elif encodeTypeName == "HIBC_AZTEC_LIC":
                  return 70

            elif encodeTypeName == "HIBC_DATA_MATRIX_LIC":
                  return 71

            elif encodeTypeName == "HIBCQRLIC":
                  return 72

            elif encodeTypeName == "HIBC_CODE_39_PAS":
                  return 73

            elif encodeTypeName == "HIBC_CODE_128_PAS":
                  return 74

            elif encodeTypeName == "HIBC_AZTEC_PAS":
                  return 75

            elif encodeTypeName == "HIBC_DATA_MATRIX_PAS":
                  return 76

            elif encodeTypeName == "HIBCQRPAS":
                  return 77

            elif encodeTypeName == "GS_1_DOT_CODE":
                  return 78

            elif encodeTypeName == "HAN_XIN":
                  return 79

            elif encodeTypeName == "GS_1_HAN_XIN":
                  return 80

            elif encodeTypeName == "MICRO_QR":
                  return 83

            elif encodeTypeName == "RECT_MICRO_QR":
                  return 84

            else:
                  return -1

class PatchFormat(Enum):
      """!
      PatchCode format. Choose PatchOnly to generate single PatchCode. Use page format to generate Patch page with PatchCodes as borders
      """

      ## Generates PatchCode only
      PATCH_ONLY = 0

      ## Generates A4 format page with PatchCodes as borders and optional QR in the center
      A4 = 1

      ## Generates A4 landscape format page with PatchCodes as borders and optional QR in the center
      A4_LANDSCAPE = 2

      ## Generates US letter format page with PatchCodes as borders and optional QR in the center
      US_LETTER = 3

      ## Generates US letter landscape format page with PatchCodes as borders and optional QR in the center
      US_LETTER_LANDSCAPE = 4


class ECIEncodings(Enum):
      """!
      Extended Channel Interpretation Identifiers. It is used to tell the barcode reader details
      about the used references for encoding the data in the symbol.

      Example how to use ECI encoding
      \code
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.QR, None)
		generator.setCodeText("12345TEXT", "UTF-8")
		generator.getParameters().getBarcode().getQR().setQrEncodeMode(Generation.QREncodeMode.ECI_ENCODING)
		generator.getParameters().getBarcode().getQR().setQrECIEncoding(Generation.ECIEncodings.UTF8)
		generator.save(self.image_path_to_save4, Generation.BarCodeImageFormat.PNG)
      \endcode
      """

      ## ISO/IEC 8859-1 Latin alphabet No. 1 encoding. ECI Id:"\000003"
      ISO_8859_1 = 3

      ## ISO/IEC 8859-2 Latin alphabet No. 2 encoding. ECI Id:"\000004"
      ISO_8859_2 = 4

      ## ISO/IEC 8859-3 Latin alphabet No. 3 encoding. ECI Id:"\000005"
      ISO_8859_3 = 5

      ## ISO/IEC 8859-4 Latin alphabet No. 4 encoding. ECI Id:"\000006"
      ISO_8859_4 = 6

      ## ISO/IEC 8859-5 Latin/Cyrillic alphabet encoding. ECI Id:"\000007"
      ISO_8859_5 = 7

      ## ISO/IEC 8859-6 Latin/Arabic alphabet encoding. ECI Id:"\000008"
      ISO_8859_6 = 8

      ## ISO/IEC 8859-7 Latin/Greek alphabet encoding. ECI Id:"\000009"
      ISO_8859_7 = 9

      ## ISO/IEC 8859-8 Latin/Hebrew alphabet encoding. ECI Id:"\000010"
      ISO_8859_8 = 10

      ## ISO/IEC 8859-9 Latin alphabet No. 5 encoding. ECI Id:"\000011"
      ISO_8859_9 = 11

      ## ISO/IEC 8859-10 Latin alphabet No. 6 encoding. ECI Id:"\000012"
      ISO_8859_10 = 12

      ## ISO/IEC 8859-11 Latin/Thai alphabet encoding. ECI Id:"\000013"
      ISO_8859_11 = 13

      ## ISO/IEC 8859-13 Latin alphabet No. 7 (Baltic Rim) encoding. ECI Id:"\000015"
      ISO_8859_13 = 15

      ## ISO/IEC 8859-14 Latin alphabet No. 8 (Celtic) encoding. ECI Id:"\000016"
      ISO_8859_14 = 16

      ## ISO/IEC 8859-15 Latin alphabet No. 9 encoding. ECI Id:"\000017"
      ISO_8859_15 = 17

      ## ISO/IEC 8859-16 Latin alphabet No. 10 encoding. ECI Id:"\000018"
      ISO_8859_16 = 18

      ## Shift JIS (JIS X 0208 Annex 1 + JIS X 0201) encoding. ECI Id:"\000020"
      Shift_JIS = 20

      ## Windows 1250 Latin 2 (Central Europe) encoding. ECI Id:"\000021"
      Win1250 = 21

      ## Windows 1251 Cyrillic encoding. ECI Id:"\000022"
      Win1251 = 22

      ## Windows 1252 Latin 1 encoding. ECI Id:"\000023"
      Win1252 = 23

      ## Windows 1256 Arabic encoding. ECI Id:"\000024"
      Win1256 = 24

      ## ISO/IEC 10646 UCS-2 (High order byte first) encoding. ECI Id:"\000025"
      UTF16BE = 25

      ## ISO/IEC 10646 UTF-8 encoding. ECI Id:"\000026"
      UTF8 = 26

      ## ISO/IEC 646:1991 International Reference Version of ISO 7-bit coded character set encoding. ECI Id:"\000027"
      US_ASCII = 27

      ## Big 5 (Taiwan) Chinese Character Set encoding. ECI Id:"\000028"
      Big5 = 28
      ## GB2312 Chinese Character Set encoding. ECI Id:"\000029"
      
      GB2312 = 29
      ## Korean Character Set encoding. ECI Id:"\000030"
      EUC_KR = 30
      ## GBK (extension of GB2312 for Simplified Chinese)  encoding. ECI Id:"\000031"
      GBK = 31
      ## GGB18030 Chinese Character Set encoding. ECI Id:"\000032"
      GB18030 = 32
      ##  ISO/IEC 10646 UTF-16LE encoding. ECI Id:"\000033"
      UTF16LE = 33
      ##  ISO/IEC 10646 UTF-32BE encoding. ECI Id:"\000034"
      UTF32BE = 34
      ##  ISO/IEC 10646 UTF-32LE encoding. ECI Id:"\000035"
      UTF32LE = 35
      ##  ISO/IEC 646: ISO 7-bit coded character set - Invariant Characters set encoding. ECI Id:"\000170"
      INVARIANT = 170
      ##  8-bit binary data. ECI Id:"\000899"
      BINARY = 899

      ## No Extended Channel Interpretation
      NONE = 0

class EnableChecksum(Enum):
      """!
          Enable checksum during generation for 1D barcodes.

          Default is treated as Yes for symbologies which must contain checksum, as No where checksum only possible.
          Checksum never used: Codabar
          Checksum is possible: Code39 Standard/Extended, Standard2of5, Interleaved2of5, Matrix2of5, ItalianPost25, DeutschePostIdentcode, DeutschePostLeitcode, VIN
          Checksum always used: Rest symbologies

      DEFAULT = 0 - If checksum is required by the specification - it will be attached.
      YES = 1 - Always use checksum if possible.
      NO = 2 -Do not use checksum.

      """
      ## If checksum is required by the specification - it will be attached.
      DEFAULT = 0

      ## Always use checksum if possible.
      YES = 1

      ## Do not use checksum.
      NO = 2

class BarCodeImageFormat(Enum):
      """!
          Specifies the file format of the image.
      """
      ## Specifies the bitmap (BMP) image format.
      BMP = 0

      ## Specifies the Graphics Interchange Format (GIF) image format.
      GIF = 1

      ## Specifies the Joint Photographic Experts Group (JPEG) image format.
      JPEG = 2

      ## Specifies the W3C Portable Network Graphics (PNG) image format.
      PNG = 3

      ## Specifies the Tagged Image File Format (TIFF) image format.
      TIFF = 4

      ## Specifies the Tagged Image File Format (TIFF) image format in CMYK color model.
      TIFF_IN_CMYK = 5

      ## Specifies the Enhanced Metafile (EMF) image format.
      EMF = 6

      ## Specifies the Scalable Vector Graphics (SVG) image format.
      SVG = 7

      ##
class CustomerInformationInterpretingType(Enum):
      """!
          Defines the interpreting type(C_TABLE or N_TABLE) of customer information for AustralianPost BarCode.
      """
      ##
      # Use C_TABLE to interpret the customer information. Allows A..Z, a..z, 1..9, space and     sing.
      # \code
      # generator = Generation.BarcodeGenerator(Generation.EncodeTypes.AUSTRALIA_POST, "5912345678ABCde")
      # generator.getParameters().getBarcode().getAustralianPost().setAustralianPostEncodingTable(
      #       Generation.CustomerInformationInterpretingType.C_TABLE)
      # image = generator.generateBarCodeImage()
      # reader = Recognition.BarCodeReader(image, None, Recognition.DecodeType.AUSTRALIA_POST)
      # reader.getBarcodeSettings().getAustraliaPost().setCustomerInformationInterpretingType(
      #       Recognition.CustomerInformationInterpretingType.C_TABLE)
      # results = reader.readBarCodes()
      # for result in results:
      #       print(f"\nBarCode Type: {result.getCodeTypeName()}")
      #       print(f"BarCode CodeText: {result.getCodeText()}")
      # \endcode
      C_TABLE = 0
      ##
      # Use N_TABLE to interpret the customer information. Allows digits.
      # \code
      # generator = Generation.BarcodeGenerator(Generation.EncodeTypes.AUSTRALIA_POST, "59123456781234567")
      # generator.getParameters().getBarcode().getAustralianPost().setAustralianPostEncodingTable(
      #       Generation.CustomerInformationInterpretingType.N_TABLE)
      # image = generator.generateBarCodeImage()
      # reader = Recognition.BarCodeReader(image, None, Recognition.DecodeType.AUSTRALIA_POST)
      # reader.getBarcodeSettings().getAustraliaPost().setCustomerInformationInterpretingType(
      #       Recognition.CustomerInformationInterpretingType.N_TABLE)
      # results = reader.readBarCodes()
      # for result in results:
      #       print(f"\nBarCode Type: {result.getCodeTypeName()}")
      #       print(f"BarCode CodeText: {result.getCodeText()}")
      # \endcode
      N_TABLE = 1
      ##
      # Do not interpret the customer information. Allows 0, 1, 2 or 3 symbol only.
      # \code
      # generator = Generation.BarcodeGenerator(Generation.EncodeTypes.AUSTRALIA_POST, "59123456780123012301230123")
      # generator.getParameters().getBarcode().getAustralianPost().setAustralianPostEncodingTable(
      #       Generation.CustomerInformationInterpretingType.OTHER)
      # image = generator.generateBarCodeImage()
      # reader = Recognition.BarCodeReader(image, None, Recognition.DecodeType.AUSTRALIA_POST)
      # reader.getBarcodeSettings().getAustraliaPost().setCustomerInformationInterpretingType(
      #       Recognition.CustomerInformationInterpretingType.OTHER)
      # results = reader.readBarCodes()
      # for result in results:
      #       print(f"\nBarCode Type: {result.getCodeTypeName()}")
      #       print(f"BarCode CodeText: {result.getCodeText()}")
      # \endcode
      OTHER = 2

class TwoDComponentType(Enum):
      """!
      Type of 2D component
      This sample shows how to create and save a GS1 Composite Bar image.
      Note that 1D codetext and 2D codetext are separated by symbol '/'
      \code
 		codetext = "(01)03212345678906|(21)A1B2C3D4E5F6G7H8"
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_COMPOSITE_BAR, codetext)
		generator.getParameters().getBarcode().getGS1CompositeBar().setLinearComponentType(Generation.EncodeTypes.GS_1_CODE_128)
		generator.getParameters().getBarcode().getGS1CompositeBar().setTwoDComponentType(Generation.TwoDComponentType.CC_A)
		# Aspect ratio of 2D component
		generator.getParameters().getBarcode().getPdf417().setAspectRatio(3)
		# X-Dimension of 1D and 2D components
		generator.getParameters().getBarcode().getXDimension().setPixels(3)
		# Height of 1D component
		generator.getParameters().getBarcode().getBarHeight().setPixels(100)
		generator.save(self.image_path_to_save4, Generation.BarCodeImageFormat.PNG)
      \endcode
      """

      ## Auto select type of 2D component
      AUTO = 0

      ## CC-A type of 2D component. It is a structural variant of MicroPDF417
      CC_A = 1

      ## CC-B type of 2D component. It is a MicroPDF417 symbol.
      CC_B = 2

      ## CC-C type of 2D component. It is a PDF417 symbol.
      CC_C= 3


class Pdf417MacroTerminator(Enum):
      """!
      Used to tell the encoder whether to add Macro PDF417 Terminator (codeword 922) to the segment.
      Applied only for Macro PDF417.
      """
      ## The terminator will be added automatically if the number of segments is provided
      ## and the current segment is the last one. In other cases, the terminator will not be added.
      AUTO = 0
      ## The terminator will not be added.
      NONE = 1
      ## The terminator will be added.
      SET = 2

class MaxiCodeEncodeMode(Enum):
      """!
      Encoding mode for MaxiCode barcodes.
      \code
      # Auto mode
		codetext = "犬Right狗"
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.MAXI_CODE, codetext)
		generator.getParameters().getBarcode().getMaxiCode().setECIEncoding(Generation.ECIEncodings.UTF8)
		generator.save(self.image_path_to_save5, Generation.BarCodeImageFormat.BMP)
      \endcode
      \code
      #Bytes mode
 		encodedArr = [0xFF, 0xFE, 0xFD, 0xFC, 0xFB, 0xFA, 0xF9]
		# encode array to string
		strBld = ""
		for bval in encodedArr:
			strBld += str(bval)
		codetext = strBld
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.MAXI_CODE, codetext)
		generator.getParameters().getBarcode().getMaxiCode().setMaxiCodeEncodeMode(Generation.MaxiCodeEncodeMode.BYTES)
		generator.save(self.image_path_to_save5, Generation.BarCodeImageFormat.BMP)
      \endcode
      \code
      # Extended codetext mode
      # create codetext
		textBuilder = Generation.MaxiCodeExtCodetextBuilder()
		textBuilder.addECICodetext(Generation.ECIEncodings.Win1251, "Will")
		textBuilder.addECICodetext(Generation.ECIEncodings.UTF8, "犬Right狗")
		textBuilder.addECICodetext(Generation.ECIEncodings.UTF16BE, "犬Power狗")
		textBuilder.addPlainCodetext("Plain text")
		# generate codetext
		codetext = textBuilder.getExtendedCodetext()
		# generate
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.MAXI_CODE, codetext)
		generator.getParameters().getBarcode().getMaxiCode().setMaxiCodeEncodeMode(Generation.MaxiCodeEncodeMode.EXTENDED_CODETEXT)
		generator.getParameters().getBarcode().getCodeTextParameters().setTwoDDisplayText("My Text")
		generator.save(self.image_path_to_save5, Generation.BarCodeImageFormat.BMP)
      \endcode
      """

      ## In Auto mode, the CodeText is encoded with maximum data compactness.
      # Unicode characters are re-encoded in the ECIEncoding specified encoding with the insertion of an ECI identifier.
      # If a character is found that is not supported by the selected ECI encoding, an exception is thrown.
      AUTO = 0
      
     ## Encode codetext as plain bytes. If it detects any Unicode character, the character will be encoded as two bytes, lower byte first.
     # @deprecated
      BYTES = 1
      
     ##
     # Extended mode which supports multi ECI modes.
     # It is better to use MaxiCodeExtCodetextBuilder for extended codetext generation.
     # Use Display2DText property to set visible text to removing managing characters.
     # ECI identifiers are set as single slash and six digits identifier "\000026" - UTF8 ECI identifier
     # All unicode characters after ECI identifier are automatically encoded into correct character codeset.
     # @deprecated
      EXTENDED_CODETEXT = 2
      
      ##
      # Extended mode which supports multi ECI modes.
      # It is better to use MaxiCodeExtCodetextBuilder for extended codetext generation.
      # Use Display2DText property to set visible text to removing managing characters.
      # ECI identifiers are set as single slash and six digits identifier "\000026" - UTF8 ECI identifier
      # All unicode characters after ECI identifier are automatically encoded into correct character codeset.
      EXTENDED = 3
      
      ##
      # In Binary mode, the CodeText is encoded with maximum data compactness.
      # If a Unicode character is found, an exception is thrown.
      BINARY = 4
      
     ## In ECI mode, the entire message is re-encoded in the ECIEncoding specified encoding with the insertion of an ECI identifier.
      # If a character is found that is not supported by the selected ECI encoding, an exception is thrown.
      # Please note that some old (pre 2006) scanners may not support this mode.
      #
      ECI = 5

class MaxiCodeMode(Enum):
      """!
      Encoding mode for MaxiCode barcodes.
      This sample shows how to genereate MaxiCode barcodes using ComplexBarcodeGenerator
      \code
       # Mode 2 with standard second message
		maxiCodeCodetext = ComplexBarcode.MaxiCodeCodetextMode2()
		maxiCodeCodetext.setPostalCode("524032140")
		maxiCodeCodetext.setCountryCode(560)
		maxiCodeCodetext.setServiceCategory(999)
		maxiCodeStandartSecondMessage = ComplexBarcode.MaxiCodeStandartSecondMessage()
		maxiCodeStandartSecondMessage.setMessage("Test message")
		maxiCodeCodetext.setSecondMessage(maxiCodeStandartSecondMessage)
		complexGenerator = ComplexBarcode.ComplexBarcodeGenerator(maxiCodeCodetext)
		complexGenerator.generateBarCodeImage()
       \endcode

       \code
       # Mode 2 with structured second message
		maxiCodeCodetext = ComplexBarcode.MaxiCodeCodetextMode2()
		maxiCodeCodetext.setPostalCode("524032140")
		maxiCodeCodetext.setCountryCode(560)
		maxiCodeCodetext.setServiceCategory(999)
		maxiCodeStructuredSecondMessage = ComplexBarcode.MaxiCodeStructuredSecondMessage()
		maxiCodeStructuredSecondMessage.add("634 ALPHA DRIVE")
		maxiCodeStructuredSecondMessage.add("PITTSBURGH")
		maxiCodeStructuredSecondMessage.add("PA")
		maxiCodeStructuredSecondMessage.setYear(99)
		maxiCodeCodetext.setSecondMessage(maxiCodeStructuredSecondMessage)
		complexGenerator = ComplexBarcode.ComplexBarcodeGenerator(maxiCodeCodetext)
		complexGenerator.generateBarCodeImage()

       \endcode

       \code
       # Mode 3 with standart second message
		maxiCodeCodetext = ComplexBarcode.MaxiCodeCodetextMode3()
		maxiCodeCodetext.setPostalCode("B1050")
		maxiCodeCodetext.setCountryCode(560)
		maxiCodeCodetext.setServiceCategory(999)
		maxiCodeStandartSecondMessage = ComplexBarcode.MaxiCodeStandartSecondMessage()
		maxiCodeStandartSecondMessage.setMessage("Test message")
		maxiCodeCodetext.setSecondMessage(maxiCodeStandartSecondMessage)
		complexGenerator = ComplexBarcode.ComplexBarcodeGenerator(maxiCodeCodetext)
		complexGenerator.generateBarCodeImage()

       \endcode

       \code
		maxiCodeCodetext = ComplexBarcode.MaxiCodeCodetextMode3()
		maxiCodeCodetext.setPostalCode("B1050")
		maxiCodeCodetext.setCountryCode(560)
		maxiCodeCodetext.setServiceCategory(999)
		maxiCodeStructuredSecondMessage = ComplexBarcode.MaxiCodeStructuredSecondMessage()
		maxiCodeStructuredSecondMessage.add("634 ALPHA DRIVE")
		maxiCodeStructuredSecondMessage.add("PITTSBURGH")
		maxiCodeStructuredSecondMessage.add("PA")
		maxiCodeStructuredSecondMessage.setYear(99)
		maxiCodeCodetext.setSecondMessage(maxiCodeStructuredSecondMessage)
		complexGenerator = ComplexBarcode.ComplexBarcodeGenerator(maxiCodeCodetext)
		complexGenerator.generateBarCodeImage()
       \endcode

       \code
       # Mode 4
		maxiCodeCodetext = ComplexBarcode.MaxiCodeStandardCodetext()
		maxiCodeCodetext.setMode(Generation.MaxiCodeMode.MODE_4)
		maxiCodeCodetext.setMessage("Test message")
		complexGenerator = ComplexBarcode.ComplexBarcodeGenerator(maxiCodeCodetext)
		complexGenerator.generateBarCodeImage()
       \endcode

       \code
       # Mode 5
		maxiCodeCodetext = ComplexBarcode.MaxiCodeStandardCodetext()
		maxiCodeCodetext.setMode(Generation.MaxiCodeMode.MODE_5)
		maxiCodeCodetext.setMessage("Test message")
		complexGenerator = ComplexBarcode.ComplexBarcodeGenerator(maxiCodeCodetext)
		complexGenerator.generateBarCodeImage()
       \endcode

       \code
       # Mode 6
		maxiCodeCodetext = ComplexBarcode.MaxiCodeStandardCodetext()
		maxiCodeCodetext.setMode(Generation.MaxiCodeMode.MODE_6)
		maxiCodeCodetext.setMessage("Test message")
		complexGenerator = ComplexBarcode.ComplexBarcodeGenerator(maxiCodeCodetext)
		complexGenerator.generateBarCodeImage()

       \endcode
      """

      ## Mode 2 encodes postal information in first message and data in second message.
      ## Has 9 digits postal code (used only in USA).
      MODE_2 = 2
      ## Mode 3 encodes postal information in first message and data in second message.
      ## Has 6 alphanumeric postal code, used in the world.
      MODE_3 = 3
      ## Mode 4 encodes data in first and second message, with short ECC correction.
      MODE_4 = 4
      ## Mode 5 encodes data in first and second message, with long ECC correction.
      MODE_5 = 5
      ## Mode 6 encodes data in first and second message, with short ECC correction.
      ## Used to encode device.
      MODE_6 = 6

class DotCodeEncodeMode(Enum):
      """!
      Encoding mode for DotCode barcodes.
      \code
		# Auto mode with macros
		codetext = "[) > \u001E05\u001DCodetextWithMacros05\u001E\u0004"
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.DOT_CODE, codetext)
		generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.BMP)
      \endcode
      \code
		# Auto mode
		codetext = "犬Right狗"
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.DOT_CODE, codetext)
		generator.getParameters().getBarcode().getDotCode().setECIEncoding(Generation.ECIEncodings.UTF8)
		generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.BMP)
      \endcode
      \code
		# Bytes mode
		encodedArr = [0xFF, 0xFE, 0xFD, 0xFC, 0xFB, 0xFA, 0xF9]
		# encode array to string
		codetext = ""
		for bval in encodedArr:
			codetext += str(bval)
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.DOT_CODE, None)
		generator.setCodeText(encodedArr, None)
		generator.getParameters().getBarcode().getDotCode().setDotCodeEncodeMode(Generation.DotCodeEncodeMode.BINARY)
		generator.save(self.image_path_to_save4, Generation.BarCodeImageFormat.PNG)
      \endcode
      \code
		# Extended codetext mode
		# create codetext
		textBuilder = Generation.DotCodeExtCodetextBuilder()
		textBuilder.addFNC1FormatIdentifier()
		textBuilder.addECICodetext(Generation.ECIEncodings.Win1251, "Will")
		textBuilder.addFNC1FormatIdentifier()
		textBuilder.addECICodetext(Generation.ECIEncodings.UTF8, "犬Right狗")
		textBuilder.addFNC3SymbolSeparator()
		textBuilder.addFNC1FormatIdentifier()
		textBuilder.addECICodetext(Generation.ECIEncodings.UTF16BE, "犬Power狗")
		textBuilder.addPlainCodetext("Plain text")
		# generate codetext
		codetext = textBuilder.getExtendedCodetext()
		# generate
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.DOT_CODE, codetext)
		generator.getParameters().getBarcode().getDotCode().setDotCodeEncodeMode(Generation.DotCodeEncodeMode.EXTENDED_CODETEXT)
		generator.save(self.image_path_to_save5, Generation.BarCodeImageFormat.BMP)
      \endcode
      """

      ##
      # In Auto mode, the CodeText is encoded with maximum data compactness.
      # Unicode characters are re-encoded in the ECIEncoding specified encoding with the insertion of an ECI identifier.
      # If a character is found that is not supported by the selected ECI encoding, an exception is thrown.
      #
      AUTO = 0

      ##
      # Encode codetext as plain bytes. If it detects any Unicode character, the character will be encoded as two bytes, lower byte first.
      #
      # @deprecated
      BYTES = 1

      ## Extended mode which supports multi ECI modes.
     # It is better to use DotCodeExtCodetextBuilder for extended codetext generation.
     # Use Display2DText property to set visible text to removing managing characters.
     # ECI identifiers are set as single slash and six digits identifier "\000026" - UTF8 ECI identifier
     # All unicode characters after ECI identifier are automatically encoded into correct character codeset.
     # @deprecated
      EXTENDED_CODETEXT = 2

      ##
      # In Binary mode, the CodeText is encoded with maximum data compactness.
      # If a Unicode character is found, an exception is thrown.
      BINARY = 3

      ##
      # In ECI mode, the entire message is re-encoded in the ECIEncoding specified encoding with the insertion of an ECI identifier.
      # If a character is found that is not supported by the selected ECI encoding, an exception is thrown.
      # Please note that some old (pre 2006) scanners may not support this mode.
      ECI = 4

      ## Extended mode which supports multi ECI modes.
     # It is better to use DotCodeExtCodetextBuilder for extended codetext generation.
     # Use Display2DText property to set visible text to removing managing characters.
     # ECI identifiers are set as single slash and six digits identifier "\000026" - UTF8 ECI identifier
     # All unicode characters after ECI identifier are automatically encoded into correct character codeset.
      EXTENDED = 5


class Pdf417EncodeMode(Enum):
      """!
      Pdf417 barcode encode mode
      """

      ## In Auto mode, the CodeText is encoded with maximum data compactness.
      # Unicode characters are re-encoded in the ECIEncoding specified encoding with the insertion of an ECI identifier.
      # If a character is found that is not supported by the selected ECI encoding, an exception is thrown.
      #
      AUTO = 0

      ## In Binary mode, the CodeText is encoded with maximum data compactness.
      # If a Unicode character is found, an exception is thrown.
      BINARY = 1

      ##
      # In ECI mode, the entire message is re-encoded in the ECIEncoding specified encoding with the insertion of an ECI identifier.
      # If a character is found that is not supported by the selected ECI encoding, an exception is thrown.
      # Please note that some old (pre 2006) scanners may not support this mode.
      ECI = 2

      ## Extended mode which supports multi ECI modes.
      # It is better to use Pdf417ExtCodetextBuilder for extended codetext generation.
      # Use Display2DText property to set visible text to removing managing characters.
      # ECI identifiers are set as single slash and six digits identifier "\000026" - UTF8 ECI identifier
      # All unicode characters after ECI identifier are automatically encoded into correct character codeset.
      EXTENDED = 3

class HanXinVersion(Enum):
      """!
      Version of Han Xin Code.
      From Version01 - 23 x 23 modules to Version84 - 189 x 189 modules, increasing in steps of 2 modules per side.
      """
      ## Specifies to automatically pick up the best version.
      # This is default value.
      AUTO = 0,

      ## Specifies version 1 with 23 x 23 modules.
      VERSION_01 = 1

      ## Specifies version 2 with 25 x 25 modules.
      VERSION_02 = 2

      ##  Specifies version 3 with 27 x 27 modules.
      VERSION_03 = 3

      ##  Specifies version 4 with 29 x 29 modules.
      VERSION_04 = 4

      ##  Specifies version 5 with 31 x 31 modules.
      VERSION_05 = 5

      ##  Specifies version 6 with 33 x 33 modules.
      VERSION_06 = 6

      ##  Specifies version 7 with 35 x 35 modules.
      VERSION_07 = 7

      ##  Specifies version 8 with 37 x 37 modules.
      VERSION_08 = 8

      ##  Specifies version 9 with 39 x 39 modules.
      VERSION_09 = 9

      ##  Specifies version 10 with 41 x 41 modules.
      VERSION_10 = 10

      ##  Specifies version 11 with 43 x 43 modules.
      VERSION_11 = 11

      ##  Specifies version 12 with 45 x 45 modules.
      VERSION_12 = 12

      ##  Specifies version 13 with 47 x 47 modules.
      VERSION_13 = 13

      ##  Specifies version 14 with 49 x 49 modules.
      VERSION_14 = 14

      ##  Specifies version 15 with 51 x 51 modules.
      VERSION_15 = 15

      ##  Specifies version 16 with 53 x 53 modules.
      VERSION_16 = 16

      ##  Specifies version 17 with 55 x 55 modules.
      VERSION_17 = 17

      ##  Specifies version 18 with 57 x 57 modules.
      VERSION_18 = 18

      ##  Specifies version 19 with 59 x 59 modules.
      VERSION_19 = 19

      ##  Specifies version 20 with 61 x 61 modules.
      VERSION_20 = 20

      ##  Specifies version 21 with 63 x 63 modules.
      VERSION_21 = 21

      ##  Specifies version 22 with 65 x 65 modules.
      VERSION_22 = 22

      ##  Specifies version 23 with 67 x 67 modules.
      VERSION_23 = 23

      ##  Specifies version 24 with 69 x 69 modules.
      VERSION_24 = 24

      ##  Specifies version 25 with 71 x 71 modules.
      VERSION_25 = 25

      ##  Specifies version 26 with 73 x 73 modules.
      VERSION_26 = 26

      ##  Specifies version 27 with 75 x 75 modules.
      VERSION_27 = 27

      ##  Specifies version 28 with 77 x 77 modules.
      VERSION_28 = 28

      ##  Specifies version 29 with 79 x 79 modules.
      VERSION_29 = 29

      ##  Specifies version 30 with 81 x 81 modules.
      VERSION_30 = 30

      ##  Specifies version 31 with 83 x 83 modules.
      VERSION_31 = 31

      ##  Specifies version 32 with 85 x 85 modules.
      VERSION_32 = 32

      ##  Specifies version 33 with 87 x 87 modules.
      VERSION_33 = 33

      ##  Specifies version 34 with 89 x 89 modules.
      VERSION_34 = 34

      ##  Specifies version 35 with 91 x 91 modules.
      VERSION_35 = 35

      ##  Specifies version 36 with 93 x 93 modules.
      VERSION_36 = 36

      ##  Specifies version 37 with 95 x 95 modules.
      VERSION_37 = 37

      ##  Specifies version 38 with 97 x 97 modules.
      VERSION_38 = 38

      ##  Specifies version 39 with 99 x 99 modules.
      VERSION_39 = 39

      ##  Specifies version 40 with 101 x 101 modules.
      VERSION_40 = 40

      ##  Specifies version 41 with 103 x 103 modules.
      VERSION_41 = 41

      ##  Specifies version 42 with 105 x 105 modules.
      VERSION_42 = 42

      ##  Specifies version 43 with 107 x 107 modules.
      VERSION_43 = 43

      ##  Specifies version 44 with 109 x 109 modules.
      VERSION_44 = 44

      ##  Specifies version 45 with 111 x 111 modules.
      VERSION_45 = 45

      ##  Specifies version 46 with 113 x 113 modules.
      VERSION_46 = 46

      ##  Specifies version 47 with 115 x 115 modules.
      VERSION_47 = 47

      ##  Specifies version 48 with 117 x 117 modules.
      VERSION_48 = 48

      ##  Specifies version 49 with 119 x 119 modules.
      VERSION_49 = 49

      ##  Specifies version 50 with 121 x 121 modules.
      VERSION_50 = 50

      ##  Specifies version 51 with 123 x 123 modules.
      VERSION_51 = 51

      ##  Specifies version 52 with 125 x 125 modules.
      VERSION_52 = 52

      ##  Specifies version 53 with 127 x 127 modules.
      VERSION_53 = 53

      ##  Specifies version 54 with 129 x 129 modules.
      VERSION_54 = 54

      ##  Specifies version 55 with 131 x 131 modules.
      VERSION_55 = 55

      ##  Specifies version 56 with 133 x 133 modules.
      VERSION_56 = 56

      ##  Specifies version 57 with 135 x 135 modules.
      VERSION_57 = 57

      ##  Specifies version 58 with 137 x 137 modules.
      VERSION_58 = 58

      ##  Specifies version 59 with 139 x 139 modules.
      VERSION_59 = 59

      ##  Specifies version 60 with 141 x 141 modules.
      VERSION_60 = 60

      ##  Specifies version 61 with 143 x 143 modules.
      VERSION_61 = 61

      ##  Specifies version 62 with 145 x 145 modules.
      VERSION_62 = 62

      ##  Specifies version 63 with 147 x 147 modules.
      VERSION_63 = 63

      ##  Specifies version 64 with 149 x 149 modules.
      VERSION_64 = 64

      ##  Specifies version 65 with 151 x 151 modules.
      VERSION_65 = 65

      ##  Specifies version 66 with 153 x 153 modules.
      VERSION_66 = 66

      ##  Specifies version 67 with 155 x 155 modules.
      VERSION_67 = 67

      ##  Specifies version 68 with 157 x 157 modules.
      VERSION_68 = 68

      ##  Specifies version 69 with 159 x 159 modules.
      VERSION_69 = 69

      ##  Specifies version 70 with 161 x 161 modules.
      VERSION_70 = 70

      ##  Specifies version 71 with 163 x 163 modules.
      VERSION_71 = 71

      ##  Specifies version 72 with 165 x 165 modules.
      VERSION_72 = 72

      ##  Specifies version 73 with 167 x 167 modules.
      VERSION_73 = 73

      ##  Specifies version 74 with 169 x 169 modules.
      VERSION_74 = 74

      ##  Specifies version 75 with 171 x 171 modules.
      VERSION_75 = 75

      ##  Specifies version 76 with 173 x 173 modules.
      VERSION_76 = 76

      ##  Specifies version 77 with 175 x 175 modules.
      VERSION_77 = 77

      ##  Specifies version 78 with 177 x 177 modules.
      VERSION_78 = 78

      ##  Specifies version 79 with 179 x 179 modules.
      VERSION_79 = 79

      ##  Specifies version 80 with 181 x 181 modules.
      VERSION_80 = 80

      ##  Specifies version 81 with 183 x 183 modules.
      VERSION_81 = 81

      ##  Specifies version 82 with 185 x 185 modules.
      VERSION_82 = 82

      ##  Specifies version 83 with 187 x 187 modules.
      VERSION_83 = 83

      ##  Specifies version 84 with 189 x 189 modules.
      VERSION_84 = 84,

class HanXinErrorLevel(Enum):
      """!
      Level of Reed-Solomon error correction. From low to high =  L1, L2, L3, L4.
      """

      ## Allows recovery of 8% of the code text
      L1 = 0

      ## Allows recovery of 15% of the code text
      L2 = 1

      ## Allows recovery of 23% of the code text
      L3 = 2

      ## Allows recovery of 30% of the code text
      L4 = 3

class HanXinEncodeMode(Enum):
      """!
      Han Xin Code encoding mode. It is recommended to use Auto with ASCII / Chinese characters or Unicode for Unicode characters.
       # Auto mode
       \code
		codetext = "1234567890ABCDEFGabcdefg,Han Xin Code"
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.HAN_XIN, codetext)
		generator.save(self.image_path_to_save5, Generation.BarCodeImageFormat.BMP)
       \endcode
       \code
		# Binary mode
		encodedArr = [0xFF, 0xFE, 0xFD, 0xFC, 0xFB, 0xFA, 0xF9]
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.HAN_XIN, None)
		generator.setCodeText(encodedArr, None)
		generator.getParameters().getBarcode().getHanXin().setHanXinEncodeMode(Generation.HanXinEncodeMode.BINARY)
		generator.save(self.image_path_to_save5, Generation.BarCodeImageFormat.BMP)
       \endcode
       \code
		# ECI mode
		codetext = "ΑΒΓΔΕ"
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.HAN_XIN, codetext)
		generator.getParameters().getBarcode().getHanXin().setHanXinEncodeMode(Generation.HanXinEncodeMode.ECI)
		generator.getParameters().getBarcode().getHanXin().setHanXinECIEncoding(Generation.ECIEncodings.ISO_8859_7)
		generator.save(self.image_path_to_save5, Generation.BarCodeImageFormat.BMP)
       \endcode
       \code
		# URI mode
		codetext = "https://www.test.com/%BC%DE%%%ab/search=test"
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.HAN_XIN, codetext)
		generator.getParameters().getBarcode().getHanXin().setHanXinEncodeMode(Generation.HanXinEncodeMode.URI)
		generator.save(self.image_path_to_save5, Generation.BarCodeImageFormat.BMP)
       \endcode
      """
      ##  Sequence of Numeric, Text, ECI, Binary Bytes and 4 GB18030 modes changing automatically.
      AUTO = 0

      ##  Binary byte mode encodes binary data in any form and encodes them in their binary byte. Every byte in
      # Binary Byte mode is represented by 8 bits.
      BINARY = 1

      ##  Extended Channel Interpretation (ECI) mode
      ECI = 2

      ##  Unicode mode designs a way to represent any text data reference to UTF8 encoding/charset in Han Xin Code.
      UNICODE = 3

      ##  URI mode indicates the data represented in Han Xin Code is Uniform Resource Identifier (URI)
      # reference to RFC 3986.
      URI = 4

      ##  Extended mode  will allow more flexible combinations of other modes, this mode is currently not implemented.
      EXTENDED = 5

class Code128EncodeMode(Enum):
      """!
      Encoding mode for Code128 barcodes.
      {@code Code 128} specification.
      This code demonstrates how to generate code 128 with different encodings
      \code
		# Generate code 128 with ISO 15417 encoding
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.CODE_128, "ABCD1234567890")
		generator.getParameters().getBarcode().getCode128().setCode128EncodeMode(Generation.Code128EncodeMode.AUTO)
		generator.save(self.image_path_to_save4, Generation.BarCodeImageFormat.PNG)
		# Generate code 128 only with Codeset A encoding
		generator = Generation.BarcodeGenerator(Generation.EncodeTypes.CODE_128, "ABCD1234567890")
		generator.getParameters().getBarcode().getCode128().setCode128EncodeMode(Generation.Code128EncodeMode.CODE_A)
		generator.save(self.image_path_to_save41, Generation.BarCodeImageFormat.PNG)
      \endcode
      """

      ## Encode codetext in classic ISO 15417 mode. The mode should be used in all ordinary cases.
      AUTO =  0

      ## Encode codetext only in 128A codeset.
      CODE_A = 1

      ## Encode codetext only in 128B codeset.
      CODE_B = 2

      ## Encode codetext only in 128C codeset.
      CODE_C = 4

      ## Encode codetext only in 128A and 128B codesets.
      CODE_AB =  3

      ## Encode codetext only in 128A and 128C codesets.
      CODE_AC = 5

      ## Encode codetext only in 128B and 128C codesets.
      CODE_BC = 6

class DataMatrixVersion(Enum):
      """!
      Specify the type of the ECC to encode.
      """

      ## Specifies to automatically pick up the smallest size for DataMatrix.
      AUTO = 0

      ## Instructs to get symbol sizes from Rows And Columns parameters. Note that DataMatrix does not support
      ROWS_COLUMNS = 1

      ## Specifies size of 9 x 9 modules for ECC000 type.
      ECC000_9x9 = 2

      ## Specifies size of 11 x 11 modules for ECC000-ECC050 types.
      ECC000_050_11x11 = 3

      ## Specifies size of 13 x 13 modules for ECC000-ECC100 types.
      ECC000_100_13x13 = 4

      ## Specifies size of 15 x 15 modules for ECC000-ECC100 types.
      ECC000_100_15x15 = 5

      ## Specifies size of 17 x 17 modules for ECC000-ECC140 types.
      ECC000_140_17x17 = 6

      ## Specifies size of 19 x 19 modules for ECC000-ECC140 types.
      ECC000_140_19x19 = 7

      ## Specifies size of 21 x 21 modules for ECC000-ECC140 types.
      ECC000_140_21x21 = 8

      ## Specifies size of 23 x 23 modules for ECC000-ECC140 types.
      ECC000_140_23x23 = 9

      ## Specifies size of 25 x 25 modules for ECC000-ECC140 types.
      ECC000_140_25x25 = 10

      ## Specifies size of 27 x 27 modules for ECC000-ECC140 types.
      ECC000_140_27x27 = 11

      ## Specifies size of 29 x 29 modules for ECC000-ECC140 types.
      ECC000_140_29x29 = 12

      ## Specifies size of 31 x 31 modules for ECC000-ECC140 types.
      ECC000_140_31x31 = 13

      ## Specifies size of 33 x 33 modules for ECC000-ECC140 types.
      ECC000_140_33x33 = 14

      ## Specifies size of 35 x 35 modules for ECC000-ECC140 types.
      ECC000_140_35x35 = 15

      ## Specifies size of 37 x 37 modules for ECC000-ECC140 types.
      ECC000_140_37x37 = 16

      ## Specifies size of 39 x 39 modules for ECC000-ECC140 types.
      ECC000_140_39x39 = 17

      ## Specifies size of 41 x 41 modules for ECC000-ECC140 types.
      ECC000_140_41x41 = 18

      ## Specifies size of 43 x 43 modules for ECC000-ECC140 types.
      ECC000_140_43x43 = 19

      ## Specifies size of 45 x 45 modules for ECC000-ECC140 types.
      ECC000_140_45x45 = 20

      ## Specifies size of 47 x 47 modules for ECC000-ECC140 types.
      ECC000_140_47x47 = 21

      ## Specifies size of 49 x 49 modules for ECC000-ECC140 types.
      ECC000_140_49x49 = 22

      ## Specifies size of 10 x 10 modules for ECC200 type.
      ECC200_10x10 = 23

      ## Specifies size of 12 x 12 modules for ECC200 type.
      ECC200_12x12 = 24

      ## Specifies size of 14 x 14 modules for ECC200 type.
      ECC200_14x14 = 25

      ## Specifies size of 16 x 16 modules for ECC200 type.
      ECC200_16x16 = 26

      ## Specifies size of 18 x 18 modules for ECC200 type.
      ECC200_18x18 = 27

      ## Specifies size of 20 x 20 modules for ECC200 type.
      ECC200_20x20 = 28

      ## Specifies size of 22 x 22 modules for ECC200 type.
      ECC200_22x22 = 29

      ## Specifies size of 24 x 24 modules for ECC200 type.
      ECC200_24x24 = 30

      ## Specifies size of 26 x 26 modules for ECC200 type.
      ECC200_26x26 = 31

      ## Specifies size of 32 x 32 modules for ECC200 type.
      ECC200_32x32 = 32

      ## Specifies size of 36 x 36 modules for ECC200 type.
      ECC200_36x36 = 33

      ## Specifies size of 40 x 40 modules for ECC200 type.
      ECC200_40x40 = 34

      ## Specifies size of 44 x 44 modules for ECC200 type.
      ECC200_44x44 = 35

      ## Specifies size of 48 x 48 modules for ECC200 type.
      ECC200_48x48 = 36

      ## Specifies size of 52 x 52 modules for ECC200 type.
      ECC200_52x52 = 37

      ## Specifies size of 64 x 64 modules for ECC200 type.
      ECC200_64x64 = 38

      ## Specifies size of 72 x 72 modules for ECC200 type.
      ECC200_72x72 = 39

      ## Specifies size of 80 x 80 modules for ECC200 type.
      ECC200_80x80 = 40

      ## Specifies size of 88 x 88 modules for ECC200 type.
      ECC200_88x88 = 41

      ## Specifies size of 96 x 96 modules for ECC200 type.
      ECC200_96x96 = 42

      ## Specifies size of 104 x 104 modules for ECC200 type.
      ECC200_104x104 = 43

      ## Specifies size of 120 x 120 modules for ECC200 type.
      ECC200_120x120 = 44

      ## Specifies size of 132 x 132 modules for ECC200 type.
      ECC200_132x132 = 45

      ## Specifies size of 144 x 144 modules for ECC200 type.
      ECC200_144x144 = 46

      ## Specifies size of 8 x 18 modules for ECC200 type.
      ECC200_8x18 = 47

      ## Specifies size of 8 x 32 modules for ECC200 type.
      ECC200_8x32 = 48

      ## Specifies size of 12 x 26 modules for ECC200 type.
      ECC200_12x26 = 49

      ## Specifies size of 12 x 36 modules for ECC200 type.
      ECC200_12x36 = 50

      ## Specifies size of 16 x 36 modules for ECC200 type.
      ECC200_16x36 = 51

      ## Specifies size of 16 x 48 modules for ECC200 type.
      ECC200_16x48 = 52

      ## Specifies size of 8 x 48 modules for DMRE barcodes.
      DMRE_8x48 = 53

      ## Specifies size of 8 x 64 modules for DMRE barcodes.
      DMRE_8x64 = 54

      ## Specifies size of 8 x 80 modules for DMRE barcodes.
      DMRE_8x80 = 55

      ## Specifies size of 8 x 96 modules for DMRE barcodes.
      DMRE_8x96 = 56

      ## Specifies size of 8 x 120 modules for DMRE barcodes.
      DMRE_8x120 = 57

      ## Specifies size of 8 x 144 modules for DMRE barcodes.
      DMRE_8x144 = 58

      ## Specifies size of 12 x 64 modules for DMRE barcodes.
      DMRE_12x64 = 59

      ## Specifies size of 12 x 88 modules for DMRE barcodes.
      DMRE_12x88 = 60

      ## Specifies size of 16 x 64 modules for DMRE barcodes.
      DMRE_16x64 = 61

      ## Specifies size of 20 x 36 modules for DMRE barcodes.
      DMRE_20x36 = 62

      ## Specifies size of 20 x 44 modules for DMRE barcodes.
      DMRE_20x44 = 63

      ## Specifies size of 20 x 64 modules for DMRE barcodes.
      DMRE_20x64 = 64

      ## Specifies size of 22 x 48 modules for DMRE barcodes.
      DMRE_22x48 = 65

      ## Specifies size of 24 x 48 modules for DMRE barcodes.
      DMRE_24x48 = 66

      ## Specifies size of 24 x 64 modules for DMRE barcodes.
      DMRE_24x64 = 67

      ## Specifies size of 26 x 40 modules for DMRE barcodes.
      DMRE_26x40 = 68

      ## Specifies size of 26 x 48 modules for DMRE barcodes.
      DMRE_26x48 = 69

      ## Specifies size of 26 x 64 modules for DMRE barcodes.
      DMRE_26x64 = 70

class AztecEncodeMode(Enum):
      ## In Auto mode, the CodeText is encoded with maximum data compactness.
      # Unicode characters are re-encoded in the ECIEncoding specified encoding with the insertion of an ECI identifier.
      # If a character is found that is not supported by the selected ECI encoding, an exception is thrown.
      AUTO = 0

      ##
      # Encode codetext as plain bytes. If it detects any Unicode character, the character will be encoded as two bytes, lower byte first.
      #
      # @deprecated
      BYTES = 1

      ## Extended mode which supports multi ECI modes.
      # It is better to use AztecExtCodetextBuilder for extended codetext generation.
      # Use Display2DText property to set visible text to removing managing characters.
      # ECI identifiers are set as single slash and six digits identifier "\000026" - UTF8 ECI identifier
      # All unicode characters after ECI identifier are automatically encoded into correct character codeset.
      # @deprecated
      EXTENDED_CODETEXT = 2
      ## Extended mode which supports multi ECI modes.
      # It is better to use AztecExtCodetextBuilder for extended codetext generation.
      # Use Display2DText property to set visible text to removing managing characters.
      # ECI identifiers are set as single slash and six digits identifier "\000026" - UTF8 ECI identifier
      # All unicode characters after ECI identifier are automatically encoded into correct character codeset.
      EXTENDED = 3

      ##
      # In Binary mode, the CodeText is encoded with maximum data compactness.
      # If a Unicode character is found, an exception is thrown.
      BINARY = 4

      ## In ECI mode, the entire message is re-encoded in the ECIEncoding specified encoding with the insertion of an ECI identifier.
      # If a character is found that is not supported by the selected ECI encoding, an exception is thrown.
      # Please note that some old (pre 2006) scanners may not support this mode.
      ECI = 5

class MicroQRVersion(Enum):
      """!
      Version of MicroQR Code.
      From M1 to M4.
      """
      
      ## Specifies to automatically pick up the best version for MicroQR.
      # This is default value.
      AUTO = 0
      
      ## Specifies version M1 for Micro QR with 11 x 11 modules.
      M1 = 1
      
      ## Specifies version M2 for Micro QR with 13 x 13 modules.
      M2 = 2
      
      ## Specifies version M3 for Micro QR with 15 x 15 modules.
      M3 = 3
      
      ## Specifies version M4 for Micro QR with 17 x 17 modules.
      M4 = 4

class RectMicroQRVersion(Enum):
      """
       Version of RectMicroQR Code.
       From version R7x43 to version R17x139.
      """

      # Specifies to automatically pick up the best version for RectMicroQR.
      AUTO = 0
      # Specifies version with 7 x 43 modules.
      R7x43 = 1
      # Specifies version with 7 x 59 modules.
      R7x59 = 2
      # Specifies version with 7 x 77 modules.
      R7x77 = 3
      # Specifies version with 7 x 99 modules.
      R7x99 = 4
      # Specifies version with 7 x 139 modules.
      R7x139 = 5
      # Specifies version with 9 x 43 modules.
      R9x43 = 6
      # Specifies version with 9 x 59 modules.
      R9x59 = 7
      # Specifies version with 9 x 77 modules.
      R9x77 = 8
      # Specifies version with 9 x 99 modules.
      R9x99 = 9
      # Specifies version with 9 x 139 modules.
      R9x139 = 10
      # Specifies version with 11 x 27 modules.
      R11x27 = 11
      # Specifies version with 11 x 43 modules.
      R11x43 = 12
      # Specifies version with 11 x 59 modules.
      R11x59 = 13
      # Specifies version with 11 x 77 modules.
      R11x77 = 14
      # Specifies version with 11 x 99 modules.
      R11x99 = 15
      # Specifies version with 11 x 139 modules.
      R11x139 = 16
      # Specifies version with 13 x 27 modules.
      R13x27 = 17
      # Specifies version with 13 x 43 modules.
      R13x43 = 18
      # Specifies version with 13 x 59 modules.
      R13x59 = 19
      # Specifies version with 13 x 77 modules.
      R13x77 = 20
      # Specifies version with 13 x 99 modules.
      R13x99 = 21
      # Specifies version with 13 x 139 modules.
      R13x139 = 22
      # Specifies version with 15 x 43 modules.
      R15x43 = 23
      # Specifies version with 15 x 59 modules.
      R15x59 = 24
      # Specifies version with 15 x 77 modules.
      R15x77 = 25
      # Specifies version with 15 x 99 modules.
      R15x99 = 26
      # Specifies version with 15 x 139 modules.
      R15x139 = 27
      # Specifies version with 17 x 43 modules.
      R17x43 = 28
      # Specifies version with 17 x 59 modules.
      R17x59 = 29
      # Specifies version with 17 x 77 modules.
      R17x77 = 30
      # Specifies version with 17 x 99 modules.
      R17x99 = 31
      # Specifies version with 17 x 139 modules.
      R17x139 = 32

class SvgColorMode(Enum):
      """!
       Possible modes for filling color in svg file, RGB is default and supported by SVG 1.1.
       RGBA, HSL, HSLA is allowed in SVG 2.0 standard.
       Even in RGB opacity will be set through "fill-opacity" parameter
      """

      ## RGB mode, example: fill="#ff5511" fill-opacity="0.73". Default mode.
      RGB = 0

      ## RGBA mode, example: fill="rgba(255, 85, 17, 0.73)"
      RGBA = 1

      ## HSL mode, example: fill="hsl(17, 100%, 53%)" fill-opacity="0.73"
      HSL = 2

      ## HSLA mode, example: fill="hsla(30, 50%, 70%, 0.8)"
      HSLA = 3
