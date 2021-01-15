from Crypto.Hash import SHA
from Crypto.Util.strxor import strxor 

class TypeError(Exception):
    def __init__(self, message):
        self.message = message

class LengthError(Exception):
    def __init__(self, message):
        self.message = message

def RF(L, R, K):
    sha = SHA.new()
    sha.update(K+R+K)
    return strxor(L, sha.digest()), R

def ENC(X, K):

    if type(K) != bytes:
        raise TypeError("Key must be of type bytes!")
        return
    
    if len(K) != 3:
        raise LengthError("Key length must be of length 6 bytes!")
        return
    
    if type(X) != bytes:
        raise TypeError("Input block must be of type bytes!")
        return
    
    if len(X) != 40:
        raise LengthError("Block length must be of length 40 bytes!")
        return    
    
    K0 = K[0:1]
    K1 = K[1:2]
    K2 = K[2:3]

    L, R = X[0:20], X[20:40]
    R, L = RF(L, R, K0)
    R, L = RF(L, R, K1)
    R, L = RF(L, R, K2)
    Y = L + R
    
    return Y 

def DEC(Y, K):

    if type(K) != bytes:
        raise TypeError("Key must be of type bytes!")
        return
    
    if len(K) != 3:
        raise LengthError("Key length must be of length 6 bytes!")
        return
    
    if type(Y) != bytes:
        raise TypeError("Input block must be of type bytes!")
        return
    
    if len(Y) != 40:
        raise LengthError("Block length must be of length 40 bytes!")
        return    
    
    K5 = K[2:3]
    K4 = K[1:2]
    K3 = K[0:1]

    L, R = Y[0:20], Y[20:40]
    R, L = RF(L, R, K5)
    R, L = RF(L, R, K4)
    R, L = RF(L, R, K3)
    X = R + L 
    
    return X 

def DECRYPT(Y,K):
    if type(K) != bytes:
        raise TypeError("Key must be of type bytes!")
        return
    
    if len(K) != 6:
        raise LengthError("Key length must be of length 6 bytes!")
        return
    
    if type(Y) != bytes:
        raise TypeError("Input block must be of type bytes!")
        return
    
    if len(Y) != 40:
        raise LengthError("Block length must be of length 40 bytes!")
        return    
    
    K0 = K[0:1]
    K1 = K[1:2]
    K2 = K[2:3]
    K3 = K[3:4]
    K4 = K[4:5]
    K5 = K[5:6]

    L, R = Y[0:20], Y[20:40]
    R, L = RF(L, R, K5)
    R, L = RF(L, R, K4)
    R, L = RF(L, R, K3)
    R, L = RF(L, R, K2)
    R, L = RF(L, R, K1)
    L, R = RF(L, R, K0)
    X = L + R
    
    return X 

# ----- actual data ---
first_block = b'\xcdG\x00\xce\x16\x8e\xf9\x12\xfa\x04\xeb~\xbc\xe3<\xe9`\x89l\x8d\xcc)\xb1\x01U\x92\x08\xb1\x03\x042\x8f\xe1\xd0\x85/\x01|\xe1\x19'
encr = b';\xf1\xce>M\xfce\x98\x89UX\xde\xecm\x9d\x00=\xf5 oF\xbeuL\xa8\x06\xa1@\xa9rM\xa2-7\x17d\xc3o\x0eo'

# ----- test data ---
# first_block = b'(\x98\xb7\xb8\xd3D\xbe\x0f\xd05\xbd%\xe9\x0c\xe7\xee\xae\xce\xf7\xcb\xdbu\xdc|\x85\x03!\xad.\x85\x1d\xfd+d\xd1\xc1\xa0\xac\xdc\x01'
# encr = b'P\xb4]1D\xe9\xb3\xe5|\x8d7\x17\x83\xd828\x9fJx\x95\xdd\xac\xed\xb1fm\xee\xb5!m\xe2O\x081hm\x12>\x83\x19'

decr = b'that_may_work_against_weak_ciphers!!!!!}'

# Characters the code can contain only for testing
abc = 'abcdefghijklmnopqrstuvwxyz'

# results in which the partially encrypted values will be stored in
res1 = {}
res2 = {}

step = 0
# try all possible byte values
for i in range(256):
    for k in range(256):
        for j in range(256):
# for i in abc:
#     for k in abc:
#         for j in abc:
            # indicator
            step += 1
            print("phase1 " + str(step))
            # get key bytes
            # K = i.encode() + j.encode() + k.encode()
            K = i.to_bytes(1,'big') + k.to_bytes(1,'big') + j.to_bytes(1,'big')
            # send the partial keys to the enc/dec functions
            # and store the returned values in the partial result set     
            res1[ENC(decr,K)] = K
            res2[DEC(encr,K)] = K

step = 0
# try decoding the encrypted text with all possbile combinations and if the values is found in the result set
# try decoding the first block with the key
for key in res1:
    try:
        step += 1
        print(step)
        fullkey = res1[key] + res2[key]
        print("---" + str(fullkey) + "----")
        # turn all the values into bytes
        # search for partial result in the result set and try to decrypt te
        # if the value is found in the result array try decoding the first bloc
        first = DECRYPT(first_block, fullkey)
        # check if first starts with cd20{
        if first[0:5].decode() == "cd20{":
            print(first)
            exit()
    except KeyError as e:
        # fasz
        step += 1
        step -= 1

flag = b'cd20{M33T-in-the-M1dDLe_i5_a_t3cHN1que_/'