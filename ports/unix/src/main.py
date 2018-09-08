import tcc
import keys


def sign_and_verify(seed):
    path = [0, 0, 0, 0]
    message = b"test"
    node = keys.derive_node(seed, path)
    print("signing...")
    sig = keys.sign_message(node, message)
    print("verifies?", keys.verify(node, sig, message))

def init():
    keys.init_device()
    print("saved seed to disk")

def boot():
    seed = keys.load_seed_from_disk()
    print("read seed from disk")
    return seed

def main():
    init()
    seed = boot()
    sign_and_verify(seed)


if __name__ == '__main__':
    main()
