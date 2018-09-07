import urandom
import tcc

def entropy(n: int):
    return urandom.getrandbits(n)



def derive_node(path: list, curve_name: str = "secp256k1") -> tcc.bip32.HDNode:
    # Pretend we're reading the seed from secure storage
    seed = b'\x98Y\xcc0\xc5\xcd%\x81\xda\x950\x8a~\xe3\xc3l\xf0\xd2KA0\x1f\xdei\xd1\xa4j\x95\xc6\x1cW\x8d\x80\xbfc(|\xba\xde\xfa\x1a\xfc\xc2d7\t9\xaa_#\xe6|j\x18\xa2S\x8b\x97=\xd2\xe9Z\x13k'
    node = tcc.bip32.from_seed(seed, curve_name)
    print(node)






