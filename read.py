import lib
import sys

assert(len(sys.argv)==2)
assert(sys.argv[1] in ["r", "k"])

if sys.argv[1] == "k":
    private, public = lib.openssl_secp112r1.genPair()
    with open("read.public_key", "w") as publicKeyFile:
        publicKeyFile.write(str(public.x)+","+str(public.y))
    with open("read.private_key", "w") as privateKeyFile:
        privateKeyFile.write(str(private))
    print(f"Succsess, public key: {public}")

if sys.argv[1] == "r":
    with open("read.private_key", "r") as privateFile:
        private = int(privateFile.read())

    with open("send.public_key", "r") as senderPublicFile:
        senderPublicFileStr = senderPublicFile.read()
    senderPublicSections = senderPublicFileStr.split(",")
    senderPublic = lib.Point(lib.openssl_secp112r1,
                             int(senderPublicSections[0]),
                             int(senderPublicSections[1]))

    with open("mssg.cyphertext","rb") as mssgFile:
        cypherBin = mssgFile.read()

    print(f"Message received as: {(private*senderPublic).unfish(cypherBin)}")
    
