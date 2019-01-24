import lib
import sys

assert(len(sys.argv)==2)

private, public = lib.openssl_secp112r1.genPair()
with open("read.public_key", "r") as publicKeyFile:
    readerPublicStr = publicKeyFile.read()
    readerPublicSections = readerPublicStr.split(",")
    readerPublic = lib.Point(lib.openssl_secp112r1,
                             int(readerPublicSections[0]),
                             int(readerPublicSections[1]))

with open("send.public_key", "w") as senderPublicFile:
    senderPublicFile.write(str(public.x)+","+str(public.y))

with open("mssg.cyphertext", "wb") as mssgFile:
    mssgFile.write((private*readerPublic).twoFish(sys.argv[1]))
