import urandom
import tcc

def entropy(n: int):
    return urandom.getrandbits(n)


def double_sha256(message: bytes) -> bytes:
    return tcc.sha256(tcc.sha256(message).digest()).digest()


def read_seed():
    # this would come from disk
    return b'\x98Y\xcc0\xc5\xcd%\x81\xda\x950\x8a~\xe3\xc3l\xf0\xd2KA0\x1f\xdei\xd1\xa4j\x95\xc6\x1cW\x8d\x80\xbfc(|\xba\xde\xfa\x1a\xfc\xc2d7\t9\xaa_#\xe6|j\x18\xa2S\x8b\x97=\xd2\xe9Z\x13k'


def derive_node(path: list, curve_name: str = "secp256k1") -> tcc.bip32.HDNode:
    seed = read_seed()
    old = node = tcc.bip32.from_seed(seed, curve_name)
    node.derive_path(path)
    return node


def sign_message(node: tcc.bip32.HDNode, message: bytes) -> bytes:
    private_key = node.private_key()
    message_digest = double_sha256(message)

    print("SIGNING...")
    print("private_key=", private_key)
    print("message_digest=", message_digest)

    sig = tcc.secp256k1.sign(private_key, message_digest)
    return sig

def verify(node: tcc.bip32.HDNode, signature: bytes, message: bytes) -> bool:
    public_key = node.public_key()
    message_digest = double_sha256(message)
    return tcc.secp256k1.verify(public_key, signature, message_digest)

