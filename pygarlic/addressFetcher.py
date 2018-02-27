from pybitcoin import BitcoinPrivateKey

class GarlicoinPrivateKey(BitcoinPrivateKey):
    _pubkeyhash_version_byte = 38

class LitecoinPrivateKey(BitcoinPrivateKey):
    _pubkeyhash_version_byte = 48

def generateGarlicAddress(private = False):
    private_key = BitcoinPrivateKey()
    public_key = private_key.public_key()
    garlicoin_private_key = GarlicoinPrivateKey(private_key.to_hex())
    garlicoin_public_key = garlicoin_private_key.public_key()
    f = open('../addresses.txt','a')
    if private:
        f.write('\nPublic, private key: ' + str([garlicoin_public_key.address(), garlicoin_private_key.to_hex()]))
        f.close()  
        return [garlicoin_public_key.address(), garlicoin_private_key.to_hex()]
    f.write('\nPublic key: ' + str(garlicoin_public_key.address()))
    f.close()
    return garlicoin_public_key.address()

def generateLiteAddress(private = False):
    private_key = BitcoinPrivateKey()
    public_key = private_key.public_key()
    litecoin_private_key = LitecoinPrivateKey(private_key.to_hex())
    litecoin_public_key = litecoin_private_key.public_key()
    f = open('../addresses.txt','a')
    if private:
        f.write('\nPublic, private key: ' + str([litecoin_public_key.address(), litecoin_private_key.to_hex()]))
        f.close()  
        return [litecoin_public_key.address(), litecoin_private_key.to_hex()]
    f.write('\nPublic key: ' + str(litecoin_public_key.address()))
    f.close()
    return litecoin_public_key.address()

generateGarlicAddress()