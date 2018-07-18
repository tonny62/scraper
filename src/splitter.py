def chunk_splitter(largechunk, numchunk):
    '''Split larger chunk of data to given number of chunks.'''
    return [largechunk[int(pivot*(len(largechunk)/numchunk)):int((pivot+1)*(len(largechunk)/numchunk))] for pivot in [i for i in range(numchunk)]]

