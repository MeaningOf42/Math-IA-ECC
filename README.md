# Math-IA-ECC

This is the Repository for the code for my IB maths IA that I did on [eliptic curve cryptography](https://en.wikipedia.org/wiki/Elliptic-curve_cryptography). The aim of the project was to simulate securly sending an encoded message over an insecure data chanel. This process requires two seperate parties: one to send a message and one to recieve a message. In order to simulate this I created two seperate programs: writer.py that represents the sending party and read.py which represents the recieving party. In order to simulate communication through the network, each program writes to files which can be examined manually as if they were intercepted, or read by the other program. The communication also requires the reader to remeber it's private key, this is written to a file, but is not considered part of the communications, and is never read by the writer party.

In order to run the test you must:
* Clone this directory.
* Generate a keypair for the recieving party using: `$ python3 read.py k`
  This creates a public key and saves it to 'read.public_key'. This is later read by the writer program, and is fair game to look at should you attempt to try decoding the message.
  It also creates the reader's private key and saves it to 'read.private_key'. This is never read by the writer program, and is shouldn't be looked at if you try decoding the message.

*Create the encrypted message using the command `$ python3 writer.py "your hidden message"`
  This reads the readers public key.
  It then creates it's own keypair.
  It uses it's private key and the readers public key to encrypt the message, which it saves to "mssg.cyphertext"
  It also saves its public key as "send.public_key"
  If you want to check that the code is very hard to crack, you can try decrypting "send.public_key", using only the two public keys.
  
  *You can then decrypt the message from the reader program using `$ python3 read.py r`
  
  The repository also contains a small library I wrote for the project which does the eliptical curve math called "lib.py", and a few programs used to create visualisations for the essay I wrote about eliptical curve cryptography.
