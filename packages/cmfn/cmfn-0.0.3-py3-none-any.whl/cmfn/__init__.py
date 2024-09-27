# SPDX-FileCopyrightText: 2024-present Hao Wu <haowu@dataset.sh>
#
# SPDX-License-Identifier: MIT


import os
import json

def listdir(folder):
    return [os.path.join(folder, x) for x in os.listdir(folder)]

def chunk_it(iterator, chunk_size = 50):
    """
    Yield successive chunks of a given size from an iterator.

    :param iterator: The input iterator.
    :param chunk_size: The number of items per chunk.
    :yield: A list containing the chunk of items.
    """
    chunk = []
    for item in iterator:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk  # Yield the last chunk if it's not empty

def read_file(fn):
    with open(fn) as fd:
        return fd.read()

def iter_jsonl(fn):
    with open(fn) as fd:
        for line in fd:
            line=line.strip()
            if line:
                yield json.loads(line)