from pybitcoin_src import BitcoinPrivateKey
private_key = BitcoinPrivateKey()
public_key = private_key.public_key()

class GarliccoinPrivateKey(BitcoinPrivateKey):
    _pubkeyhash_version_byte = 38

garliccoin_private_key = GarliccoinPrivateKey(private_key.to_hex())
garliccoin_public_key = garliccoin_private_key.public_key()
print(garliccoin_public_key.address())
print(garliccoin_private_key.to_hex())

class generateGarlicAddress(private = False):
    private_key = BitcoinPrivateKey()
    public_key = private_key.public_key()
    garliccoin_private_key = GarliccoinPrivateKey(private_key.to_hex())
    garliccoin_public_key = garliccoin_private_key.public_key()
    if private:
        return [garliccoin_public_key, garliccoin_private_key]
    return garliccoin_public_key