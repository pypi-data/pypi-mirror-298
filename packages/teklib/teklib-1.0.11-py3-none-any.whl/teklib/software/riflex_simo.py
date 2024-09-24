import struct
import pandas as pd
import numpy as np

def parse_riflex_binary(bin, columns=None, column_expected=None):
    if bin is None:
        return None

    row_content_bytes = int.from_bytes(bin[:4], 'little')
    column_count = row_content_bytes // 4

    if column_expected is not None:
        assert(column_expected == column_count+2)

    row_bytes = column_count*4 + 4 + 4 # starts and ends with row length

    row_fmt = 'i{}fi'.format(column_count)
    row_itr = (
        struct.unpack(row_fmt, bin[cursor:cursor + row_bytes])
        for cursor in range(0, len(bin), row_bytes)
    )

    df = pd.DataFrame([row for row in row_itr])

    assert (df.iloc[:, [0, column_count + 1]] == row_content_bytes).all().all(
        ), 'sima binary invariance error'

    if columns is not None:
        keep = sorted(columns.keys())
        df = df.iloc[:, keep].copy()
        df.rename(columns=columns, inplace=True)

    return df


def parse_simo_binary(bin, columns=None, column_expected=None):
    if bin is None:
        return None

    row_fmt = 'if'
    header = struct.unpack(row_fmt, bin[0:8])
    column_count = int(len(bin)/4/header[1]) - 1
    if column_expected is not None:
        assert(column_expected == column_count+1)

    row_bytes = column_count*4 + 4# starts row length

    row_fmt = 'i{}f'.format(column_count)
    row_itr = (
        struct.unpack(row_fmt, bin[cursor:cursor + row_bytes])
        for cursor in range(0, len(bin), row_bytes)
    )

    df = pd.DataFrame([row for row in row_itr])
    df = df.transpose()

    if columns is not None:
        keep = sorted(columns.keys())
        df = df.iloc[:, keep].copy()
        df.rename(columns=columns, inplace=True)

    return df


def read_data_file(filename:str, simo=False, riflex=False)->np.ndarray:
    if riflex: func = parse_riflex_binary
    elif simo: func = parse_simo_binary
    else: raise NotImplementedError("Need to set simo or riflex to True")
    with open(filename, 'rb') as fp: 
        data = func(fp.read()).to_numpy()
    return data