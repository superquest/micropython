from uio import BytesIO
from tx import Tx

raw_tx = b"\x01\x00\x00\x00\x01\x81?y\x01\x1a\xcb\x80\x92]\xfei\xb3\xde\xf3U\xfe\x91K\xd1\xd9j?_q\xbf\x83\x03\xc6\xa9\x89\xc7\xd1\x00\x00\x00\x00kH0E\x02!\x00\xed\x81\xff\x19.u\xa3\xfd#\x04\x00M\xca\xdbto\xa5\xe2LP1\xcc\xfc\xf2\x13 \xb0'tW\xc9\x8f\x02 z\x98m\x95\\n\x0c\xb3]Dj\x89\xd3\xf5a\x00\xf4\xd7\xf6x\x01\xc3\x19gt:\x9c\x8e\x10a[\xed\x01!\x03I\xfcNc\x1e6$\xa5E\xde?\x89\xf5\xd8hL{\x818\xbd\x94\xbd\xd51\xd2\xe2\x13\xbf\x01k'\x8a\xfe\xff\xff\xff\x02\xa15\xef\x01\x00\x00\x00\x00\x19v\xa9\x14\xbc;eM\xca~V\xb0M\xca\x18\xf2Vl\xda\xf0.\x8d\x9a\xda\x88\xac\x99\xc3\x98\x00\x00\x00\x00\x00\x19v\xa9\x14\x1cK\xc7b\xddT#\xe32\x16g\x02\xcbu\xf4\r\xf7\x9f\xea\x12\x88\xac\x19C\x06\x00"

# raw_tx = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')

def test_parse_version():
    stream = BytesIO(raw_tx)
    tx = Tx.parse(stream)
    assert tx.version == 1

def test_parse_inputs():
    stream = BytesIO(raw_tx)
    tx = Tx.parse(stream)
    assert len(tx.tx_ins) == 1
    # want = bytes.fromhex('d1c789a9c60383bf715f3f6ad9d14b91fe55f3deb369fe5d9280cb1a01793f81')
    # assert tx.tx_ins[0].prev_tx == want
    assert tx.tx_ins[0].prev_index == 0
    # want = bytes.fromhex('483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')
    # assert tx.tx_ins[0].script_sig.serialize() == want
    assert tx.tx_ins[0].sequence == 0xfffffffe

def test_parse_outputs():
    stream = BytesIO(raw_tx)
    tx = Tx.parse(stream)
    assert len(tx.tx_outs) == 2
    want = 32454049
    assert tx.tx_outs[0].amount == want
    # want = bytes.fromhex('76a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac')
    # assert tx.tx_outs[0].script_pubkey.serialize() == want
    want = 10011545
    assert tx.tx_outs[1].amount == want
    # want = bytes.fromhex('76a9141c4bc762dd5423e332166702cb75f40df79fea1288ac')
    # assert tx.tx_outs[1].script_pubkey.serialize() == want

test_parse_version()
test_parse_inputs()
test_parse_outputs()

