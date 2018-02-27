from pybitcoin_src import BitcoinPrivateKey

class GarlicoinPrivateKey(BitcoinPrivateKey):
    _pubkeyhash_version_byte = 38

def generateGarlicAddress(private = False):
    private_key = BitcoinPrivateKey()
    public_key = private_key.public_key()
    garlicoin_private_key = GarlicoinPrivateKey(private_key.to_hex())
    garlicoin_public_key = garlicoin_private_key.public_key()
    if private:
        return [garlicoin_public_key.address(), garlicoin_private_key.to_hex()]
    return garlicoin_public_key.address()