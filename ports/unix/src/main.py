import tcc
import keys

def main():
    path = [0, 0, 0, 0]
    message = b"test"

    node = keys.derive_node(path)
    sig = keys.sign_message(node, message)

    print("verifies?", keys.verify(node, sig, message))

if __name__ == '__main__':
    main()
