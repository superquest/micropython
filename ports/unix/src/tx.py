"""
Required changes:
* PrivateKey class

How to proceed?
1. Implement the helpers
2. Classes and de/serialization
3. Signatures
"""

from uio import BytesIO
from helpers import *

class Tx:

    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.testnet = testnet

    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'
        return 'tx:{}\nversion: {}\ntx_ins:\n{}\ntx_outs:\n{}\nlocktime: {}\n'.format(
            self.hash().hex(),
            self.version,
            tx_ins,
            tx_outs,
            self.locktime,
        )

    def hash(self):
        # return double_sha256(self.serialize())[::-1]
        return reverse_bytes(double_sha256(self.serialize()))

    @classmethod
    def parse(cls, s, testnet=False):
        '''Takes a byte stream and parses the transaction at the start
        return a Tx object
        '''
        # s.read(n) will return n bytes
        # version has 4 bytes, little-endian, interpret as int
        version = little_endian_to_int(s.read(4))
        # num_inputs is a varint, use read_varint(s)
        num_inputs = read_varint(s)
        # each input needs parsing
        inputs = []
        for _ in range(num_inputs):
            inputs.append(TxIn.parse(s))
        # num_outputs is a varint, use read_varint(s)
        num_outputs = read_varint(s)
        # each output needs parsing
        outputs = []
        for _ in range(num_outputs):
            outputs.append(TxOut.parse(s))
        # locktime is 4 bytes, little-endian
        locktime = little_endian_to_int(s.read(4))
        # return an instance of the class (cls(...))
        return cls(version, inputs, outputs, locktime, testnet=testnet)

    def serialize(self):
        '''Returns the byte serialization of the transaction'''
        # serialize version (4 bytes, little endian)
        result = int_to_little_endian(self.version, 4)
        # encode_varint on the number of inputs
        result += encode_varint(len(self.tx_ins))
        # iterate inputs
        for tx_in in self.tx_ins:
            # serialize each input
            result += tx_in.serialize()
        # encode_varint on the number of inputs
        result += encode_varint(len(self.tx_outs))
        # iterate outputs
        for tx_out in self.tx_outs:
            # serialize each output
            result += tx_out.serialize()
        # serialize locktime (4 bytes, little endian)
        result += int_to_little_endian(self.locktime, 4)
        return result

class TxIn:

    cache = {}

    def __init__(self, prev_tx, prev_index, script_sig, sequence):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        self.script_sig = Script.parse(script_sig)
        self.sequence = sequence

    def __repr__(self):
        return '{}:{}'.format(
            self.prev_tx.hex(),
            self.prev_index,
        )

    @classmethod
    def parse(cls, s):
        '''Takes a byte stream and parses the tx_input at the start
        return a TxIn object
        '''
        # s.read(n) will return n bytes
        # prev_tx is 32 bytes, little endian
        # prev_tx = s.read(32)[::-1]
        prev_tx = reverse_bytes(s.read(32))
        # prev_index is 4 bytes, little endian, interpret as int
        prev_index = little_endian_to_int(s.read(4))
        # script_sig is a variable field (length followed by the data)
        # get the length by using read_varint(s)
        script_sig_length = read_varint(s)
        script_sig = s.read(script_sig_length)
        # sequence is 4 bytes, little-endian, interpret as int
        sequence = little_endian_to_int(s.read(4))
        # return an instance of the class (cls(...))
        return cls(prev_tx, prev_index, script_sig, sequence)

    def serialize(self):
        '''Returns the byte serialization of the transaction input'''
        # serialize prev_tx, little endian
        result = reverse_bytes(self.prev_tx)
        # serialize prev_index, 4 bytes, little endian
        result += int_to_little_endian(self.prev_index, 4)
        # get the scriptSig ready (use self.script_sig.serialize())
        raw_script_sig = self.script_sig.serialize()
        # encode_varint on the length of the scriptSig
        result += encode_varint(len(raw_script_sig))
        # add the scriptSig
        result += raw_script_sig
        # serialize sequence, 4 bytes, little endian
        result += int_to_little_endian(self.sequence, 4)
        return result

class TxOut:

    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = Script.parse(script_pubkey)

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_pubkey.address())

    @classmethod
    def parse(cls, s):
        '''Takes a byte stream and parses the tx_output at the start
        return a TxOut object
        '''
        # s.read(n) will return n bytes
        # amount is 8 bytes, little endian, interpret as int
        amount = little_endian_to_int(s.read(8))
        # script_pubkey is a variable field (length followed by the data)
        # get the length by using read_varint(s)
        script_pubkey_length = read_varint(s)
        script_pubkey = s.read(script_pubkey_length)
        # return an instance of the class (cls(...))
        return cls(amount, script_pubkey)

    def serialize(self):
        '''Returns the byte serialization of the transaction output'''
        # serialize amount, 8 bytes, little endian
        result = int_to_little_endian(self.amount, 8)
        # get the scriptPubkey ready (use self.script_pubkey.serialize())
        raw_script_pubkey = self.script_pubkey.serialize()
        # encode_varint on the length of the scriptPubkey
        result += encode_varint(len(raw_script_pubkey))
        # add the scriptPubKey
        result += raw_script_pubkey
        return result


class Script:

    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        result = ''
        for element in self.elements:
            if type(element) == int:
                result += '{} '.format(OP_CODES[element])
            else:
                result += '{} '.format(element.hex())
        return result

    @classmethod
    def parse(cls, binary):
        s = BytesIO(binary)
        elements = []
        current = s.read(1)
        while current != b'':
            op_code = current[0]
            if op_code > 0 and op_code <= 75:
                # we have an element
                elements.append(s.read(op_code))
            else:
                elements.append(op_code)
            current = s.read(1)
        return cls(elements)

    def type(self):
        '''Some standard pay-to type scripts.'''
        if len(self.elements) == 0:
            return 'blank'
        elif self.elements[0] == 0x76 \
           and self.elements[1] == 0xa9 \
           and type(self.elements[2]) == bytes \
           and len(self.elements[2]) == 0x14 \
           and self.elements[3] == 0x88 \
           and self.elements[4] == 0xac:
            # p2pkh:
            # OP_DUP OP_HASH160 <20-byte hash> <OP_EQUALVERIFY> <OP_CHECKSIG>
            return 'p2pkh'
        elif self.elements[0] == 0xa9 \
             and type(self.elements[1]) == bytes \
             and len(self.elements[1]) == 0x14 \
           and self.elements[-1] == 0x87:
            # p2sh:
            # OP_HASH160 <20-byte hash> <OP_EQUAL>
            return 'p2sh'
        elif type(self.elements[0]) == bytes \
             and len(self.elements[0]) in (0x47, 0x48, 0x49) \
             and type(self.elements[1]) == bytes \
             and len(self.elements[1]) in (0x21, 0x41):
            # p2pkh scriptSig:
            # <signature> <pubkey>
            return 'p2pkh sig'
        elif len(self.elements) > 1 \
             and type(self.elements[1]) == bytes \
             and len(self.elements[1]) in (0x47, 0x48, 0x49) \
             and self.elements[-1][-1] == 0xae:
            # HACK: assumes p2sh is a multisig
            # p2sh multisig:
            # <x> <sig1> ... <sigm> <redeemscript ends with OP_CHECKMULTISIG>
            return 'p2sh sig'
        else:
            return 'unknown'

    def serialize(self):
        result = b''
        for element in self.elements:
            if type(element) == int:
                result += bytes([element])
            else:
                result += bytes([len(element)]) + element
        return result



