import random
import string
import hashlib
from twofish import Twofish

def pad(_string, size):
    """
    Adds padding to string so twofish algorithm can work on it.
    """
    numPadLetters = size - ((len(_string)+1)%size)
    padding = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(numPadLetters))
    return padding+"\n"+_string


def extendedEuclideanAlgorithm(small, big):
    old_s, s = 1, 0
    old_t, t = 0, 1
    while not(small==0):
        quotient = big//small
        big, small = small, big%small
        old_s, s = s, old_s - s*quotient
        old_t, t = t, old_t - t*quotient
    return (big, old_s, old_t)

def scalarMultFromPowersOfTwo(obj, scalar, double):
    acc = obj
    binarryArray = [i=="1" for i in reversed("{0:b}".format(scalar))][1:]
    powerOfTwoTimesObj = obj
    for power in binarryArray:
        powerOfTwoTimesObj = double(powerOfTwoTimesObj)
        if power:
            acc += powerOfTwoTimesObj

    return acc
    

class FiniteFeild:
    def __init__(self, n):
        self.size = n

    def toFeild(self, n):
        return n % self.size

    def isInFeild(self, n):
        return n >= 0 and n < self.size and n == int(n)

    def multInverse(self, n):
        return extendedEuclideanAlgorithm(self.size, n)[1] % self.size
        
    def range(self):
        return range(self.size)

    def __str__(self):
        return f"size: self.size"


class Curve():
    def __init__(self, feild, a, b, genX, genY, order):
        self.feild = feild
        self.a = a
        self.b = b
        self.gen = Point(self, genX, genY)
        self.order = order

    def isOnCurve(self, point):
        isInRange = self.feild.isInFeild(point.x) and self.feild.isInFeild(point.y)
        return isInRange and self.feild.toFeild(point.y**2) == self.feild.toFeild(point.x**3 + self.a*point.x + self.b) 

    def genPair(self):
        private = random.randint(1, self.order-1)
        public = private*self.gen
        return (private, public)

    def __eq__(self, other):
        return self.a == other.a and self.b==other.b
    
class Point():
    def __init__(self, curve, x,y):
        self.x = x
        self.y = y
        self.curve = curve

    def __str__(self):
        return f"({self.x, self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.curve == other.curve

    def __mul__(self, other):
        if not(isinstance(other, int)):
            return ValueError("Can only multiply by a point by an integer")
        return scalarMultFromPowersOfTwo(self, other, lambda point: point.double())

    def __rmul__(self, other):
        if not(isinstance(other, int)):
            return ValueError("Can only multiply by a point by an integer")
        return scalarMultFromPowersOfTwo(self, other, lambda point: point.double())

    def __add__(self, other):
        if self == other:
            return self.double()

        curve = self.curve
        feild = curve.feild
        s = feild.toFeild(feild.toFeild(self.y-other.y)*feild.multInverse(feild.toFeild(self.x-other.x)))
        resultX = feild.toFeild(s**2 - self.x - other.x)
        resultY = feild.toFeild(s*(self.x-resultX) - self.y)
        return Point(curve, resultX, resultY)

    def double(self):
        curve = self.curve
        feild = curve.feild
        s = feild.toFeild((3*self.x**2+curve.a)*feild.multInverse(feild.toFeild(2*self.y)))
        doubledX = feild.toFeild(s**2 - 2*self.x)
        doubledY = feild.toFeild(s*(self.x-doubledX) - self.y)
        return Point(curve, doubledX, doubledY) 

    def keyGen(self):
        hasher = hashlib.sha256()
        hasher.update(self.x.to_bytes(112, "big"))
        return hasher.digest()

    def twoFish(self, _string):
        encryptor = Twofish(self.keyGen())
        return encryptor.encrypt(pad(_string,16).encode("utf-8"))

    def unfish(self, cyperbits):
        encryptor = Twofish(self.keyGen())
        padded = encryptor.decrypt(cyperbits).decode()
        return "\n".join(padded.split("\n")[1:])

    def realismCheck(self):
        return self.curve.isOnCurve(self)

openssl_secp112r1_feild = FiniteFeild(4451685225093714772084598273548427)
openssl_secp112r1 = Curve(openssl_secp112r1_feild,
                          4451685225093714772084598273548424,
                          2061118396808653202902996166388514,
                          188281465057972534892223778713752,
                          3419875491033170827167861896082688,
                          4451685225093714776491891542548933)

def test_suite():
    print("Check point doubling: ")
    F = FiniteFeild(263)
    C = Curve(F, 2,3, 126,76, 6)
    print(f"C.gen: ({C.gen.x}, {C.gen.y})")
    print(f"Is gen on point: {C.isOnCurve(C.gen)}")
    doubled = C.gen.double()
    print(f"Doubled point: ({doubled.x}, {doubled.y})")
    threeTimesGen = doubled+C.gen
    print(f"Three times the generator point: ({threeTimesGen.x}, {threeTimesGen.y})")
    print(f"5 constructed using scalarMultFromPowersOfTwo: {scalarMultFromPowersOfTwo(1,5,lambda x: x*2)}")
    print(f"All points: [{', '.join([str(i*C.gen) for i in range(1,6)])}]")


    testPoint = Point(openssl_secp112r1,
              random.randint(0, openssl_secp112r1.feild.size-1),
              random.randint(0, openssl_secp112r1.feild.size-1))
    print(f"Is Gen on curve: {openssl_secp112r1.isOnCurve(openssl_secp112r1.gen)}")
    print(f"Is testPoint on curve: {openssl_secp112r1.isOnCurve(testPoint)}")
    print(f"x: {testPoint.x}, y: {testPoint.y}")
    print(f"key from testPoint: {testPoint.keyGen()}")
    cypherbits = testPoint.twoFish('Billy')
    print(f"Billy encrypted using point: {cypherbits}")
    print(f"De-encryption using Cypher text and point: {testPoint.unfish(cypherbits)}")
    print()

    print(f"Generating test pair: {openssl_secp112r1.genPair()}")
    print(f"Check public key on curve: {openssl_secp112r1.genPair()[1].realismCheck()}")

if __name__ == "__main__":
    test_suite()
