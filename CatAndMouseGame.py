import pprp
import gzip


def ASEDecrypt(key, s, iv, block_size=pprp.config.DEFAULT_BLOCK_SIZE_B):
    r = pprp.crypto_3.rijndael(key, block_size=32)
    i = 0
    for block in s:
        decrypted = r.decrypt(block)
        decrypted = xor(decrypted, iv)
        iv = block
        yield decrypted
        i += 1


def xor(block, iv):
    resultList = [(a ^ b) for (a, b) in zip(block, iv)]
    return bytes(resultList)


def MouseInfoMsgPack(data):
    key = b'nn33CYId2J1ggv0bYDMbYuZ60m4GZt5P'
    iv = data[:32]
    array = data[32:]
    sg = pprp.data_source_gen(array, 32)
    dg = ASEDecrypt(key, sg, iv)
    decrypted = pprp.decrypt_sink(dg, 32)
    decbytes = gzip.decompress(decrypted)
    return decbytes[0xD:0x16].decode('utf-8')


if __name__ == "__main__":
    main()
