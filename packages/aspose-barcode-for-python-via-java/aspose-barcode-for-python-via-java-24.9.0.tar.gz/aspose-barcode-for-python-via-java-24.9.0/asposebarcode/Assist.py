import jpype


class BaseJavaClass(object):

      def __init__(self, javaClass):
            self.javaClass = javaClass
            self.javaClassName = ""

            if self.javaClassName == None or self.javaClassName == "":
                  self.javaClassName = str(self.javaClass.getClass().getName())
            self.init()

      def init(self):
            raise Exception('You have to implement the method init!')

      def getJavaClass(self):
            return self.javaClass

      def setJavaClass(self, javaClass):
            self.javaClass = javaClass
            self.init()

      def getJavaClassName(self):
            return self.javaClassName

      def isNull(self):
            return self.javaClass.isNull()

      def printJavaClassName(self):
            print("Java class name => \'" + self.javaClassName + "\'")


class Rectangle(BaseJavaClass):
      """!
      A Rectangle specifies an area in a coordinate space that is
      enclosed by the Rectangle object's upper-left point
      in the coordinate space, its width, and its height.
      """

      def init(self):
            pass

      javaClassName = "java.awt.Rectangle"

      def __init__(self, x, y, width, height):
            """!
            Rectangle constructor.
           @param x The x-coordinate of the upper-left corner of the rectangle.
           @param y The y-coordinate of the upper-left corner of the rectangle.
           @param width The width of the rectangle.
           @param height The height of the rectangle.
            """
            javaRectangle = jpype.JClass(self.javaClassName)
            self.javaClass = javaRectangle(x, y, width, height)
            super().__init__(self.javaClass)

      @staticmethod
      def construct(arg):
            rectangle = Rectangle(0, 0, 0, 0)
            rectangle.javaClass = arg
            return rectangle

      def getX(self):
            """!
            Returns the X coordinate of the bounding Rectangle in
            double precision.
            @return the X coordinate of the bounding Rectangle.
            """
            return int(self.getJavaClass().getX())

      def getY(self):
            """!
            Returns the Y coordinate of the bounding Rectangle in
           double precision.
            @return the Y coordinate of the bounding Rectangle.
            """
            return int(self.getJavaClass().getY())

      def getLeft(self):
            """!
            Gets the x-coordinate of the left edge of self Rectangle class.
            @returns The x-coordinate of the left edge of self Rectangle class.
            """
            return self.getX()

      def getTop(self):
            """!
            Gets the y-coordinate of the top edge of self Rectangle class.
            @returns The y-coordinate of the top edge of self Rectangle class.
            """
            return self.getY()

      def getRight(self):
            """!
            Gets the x-coordinate that is the sum of X and Width property values of self Rectangle class.
            @returns The x-coordinate that is the sum of X and Width of self Rectangle.
            """
            return self.getX() + self.getWidth()

      def getBottom(self):
            """!
            Gets the y-coordinate that is the sum of the Y and Height property values of self Rectangle class.
            @returns The y-coordinate that is the sum of Y and Height of self Rectangle.
            """
            return self.getY() + self.getHeight()

      def getWidth(self):
            """!
            Returns the width of the bounding Rectangle in
            double precision.
            @return the width of the bounding Rectangle.
            """
            return int(self.getJavaClass().getWidth())

      def getHeight(self):
            """!
            Returns the height of the bounding Rectangle in
            double precision.
            @return the height of the bounding Rectangle.
            """
            return int(self.getJavaClass().getHeight())

      def toString(self):
            return str(int(self.getX())) + ',' + str(int(self.getY())) + ',' + str(int(self.getWidth())) + ',' + str(int(self.getHeight()))

      def equals(self, obj):
            return self.getJavaClass().equals(obj.getJavaClass())

      def intersectsWithInclusive(self, rectangle):
            """!
           Determines if self rectangle intersects with rect.
           @param rectangle
           @returns {boolean
            """
            return not ((self.getLeft() > rectangle.getRight()) | (self.getRight() < rectangle.getLeft()) |
                        (self.getTop() > rectangle.getBottom()) | (self.getBottom() < rectangle.getTop()))

      @staticmethod
      def intersect(a, b):
            """!
            Intersect Shared Method
            Produces a new Rectangle by intersecting 2 existing
            Rectangles. Returns None if there is no    intersection.
            """
            if (not a.intersectsWithInclusive(b)):
                  return Rectangle(0, 0, 0, 0)

            return Rectangle.fromLTRB(max(a.getLeft(), b.getLeft()),
                                      max(a.getTop(), b.getTop()),
                                      min(a.getRight(), b.getRight()),
                                      min(a.getBottom(), b.getBottom()))

      @staticmethod
      def fromLTRB(left, top, right, bottom):
            """!
            FromLTRB Shared Method
            Produces a Rectangle class from left, top, right,
            and bottom coordinates.
            """
            return Rectangle(left, top, right - left, bottom - top)

      def isEmpty(self):
            return (self.getWidth() <= 0) | (self.getHeight() <= 0)


class Point(BaseJavaClass):
      javaClassName = "java.awt.Point"

      def __init__(self, x, y):
            javaRectangle = jpype.JClass(Point.javaClassName)
            self.javaClass = javaRectangle(int(x), int(y))
            super().__init__(self.javaClass)

      @staticmethod
      def construct(arg):
            point = Point(0, 0)
            point.javaClass = arg
            return point

      def init(self):
            pass

      def getX(self):
            """!
            The X coordinate of this <code>Point</code>.
            If no X coordinate is set it will default to 0.
            """
            return int(self.getJavaClass().getX())

      def getY(self):
            """!
            The Y coordinate of this <code>Point</code>.
             If no Y coordinate is set it will default to 0.
            """
            return int(self.getJavaClass().getY())

      def setX(self, x):
            """!
            The Y coordinate of this <code>Point</code>.
             If no Y coordinate is set it will default to 0.
            """
            self.getJavaClass().x = x

      def setY(self, y):
            """!
            The Y coordinate of this <code>Point</code>.
             If no Y coordinate is set it will default to 0.
            """
            self.getJavaClass().y = y

      def toString(self):
            return self.getX() + ',' + self.getY()

      def equals(self, obj):
            return self.getJavaClass().equals(obj.getJavaClass())


class License(BaseJavaClass):
      javaClassName = "com.aspose.python.barcode.license.PythonLicense"

      def __init__(self):
            javaLicense = jpype.JClass(self.javaClassName)
            self.javaClass = javaLicense()
            super().__init__(self.javaClass)

      def setLicense(self, filePath):
            """
            Licenses the component.
            @:param: filePath:  Can be a full or short file name. Use an empty string to switch to evaluation mode.
            """
            try:
                  file_data = License.openFile(filePath)
                  jArray = jpype.JArray(jpype.JString, 1)(file_data)
                  self.getJavaClass().setLicense(jArray)
            except Exception as ex:
                  raise BarCodeException(ex)

      def isLicensed(self):
            javaClass =  self.getJavaClass()
            is_licensed = javaClass.isLicensed()
            return str(is_licensed) == "true"

      def resetLicense(self):
            javaClass =  self.getJavaClass()
            javaClass.resetLicense()


      @staticmethod
      def openFile(filename):
            file = open(filename, "rb")
            image_data_binary = file.read()
            file.close()
            array = []
            array.append('')
            i = 0
            while (i < len(image_data_binary)):
                  array.append(str(image_data_binary[i]))
                  i += 1
            return array

      def init(self):
            return


class BarCodeException(Exception):
      """!
      Represents the exception for creating barcode image.
      """

      @staticmethod
      def MAX_LINES():
            return 4

      def __init__(self, exc):
            """!
            Initializes a new instance of the  BarCodeException class with specified error message.
            """
            self.message = None
            super().__init__(self, exc)
            if (isinstance(exc, str)):
                  self.setMessage(str(exc))
                  return

            exc_message = 'Exception occured in file:line\n'

            self.setMessage(exc_message)

      def setMessage(self, message):
            """!
            Sets message
            """
            self.message = message

      def getMessage(self):
            """!
            Gets message
            """
            return self.message
