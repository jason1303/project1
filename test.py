from tqdm import tqdm
from random import randint

def int_to_bitlist(n, length = None):
    if length == None:
        length = n.bit_length()
    l = [int(i) for i in bin(n)[2:].zfill(length)]
    return l

class LFSR:
    def __init__(self, key, taps):
        d = max(taps)
        assert len(key) == d
        self._s = key
        self._t = [d - t for t in taps]

    def _sum(self, L):
        s = 0
        for x in L:
            s ^= x
        return s

    def _clock(self):
        b = self._s[0]
        self._s = self._s[1:] + [self._sum(self._s[p] for p in self._t)]
        return b

    def bit(self):
        return self._clock()

key= [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1]

def construct_key(bit_length:int, key_stream:list):
    unrecoverd_key = [i  for i  in range(bit_length) if key_stream[i]==-1]
    if len(unrecoverd_key)>=13:
        return []
    stream_temp = key_stream.copy()
    recovered_key = []
    
    def check():
        percent_match = 0
        for i in range(256):
            recovered_bit = stream_temp[i-bit_length]^stream_temp[i-bit_length+1]^stream_temp[i-bit_length+2]^stream_temp[i-bit_length+5]
            if key_stream[i]==-1:
                stream_temp[i] = recovered_bit
            else:
                if stream_temp!=recovered_bit:
                    return 0 
        #print(percent_match/256)           
        return 1

    def Try(pos:int):
        if pos==len(unrecoverd_key):
            if check():
                recovered_key.append(stream_temp[:bit_length])
        else:
            for i in [0,1]:
                stream_temp[unrecoverd_key[pos]] = i
                Try(pos+1)
            return
        
    Try(0)
    return recovered_key

    
dic = dict()

for i in tqdm(range(20000,30000)):
    key1 = int_to_bitlist(i,19)
    lfsr1 = LFSR(key1,[19,18,17,14])
    key_stream1 = [lfsr1.bit() for _ in range(256)] 
    key_stream2 = [key[j] if key_stream1[j]==1 else -1 for j in range(256)]
    key_stream3 = [key[j] if key_stream1[j]==0 else -1 for j in range(256)]
    a = construct_key(23,key_stream3)
    if len(a)!=0:
        print(a)
        break
    
    
        
        


    



    
        




