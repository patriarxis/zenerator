import os
import numpy as np
import urllib.request
import zipfile
from tqdm import tqdm

glove_url = 'https://nlp.stanford.edu/data/glove.840B.300d.zip'
glove_zip = 'glove.840B.300d.zip'
glove_file = 'glove.840B.300d.txt'


if not os.path.exists(glove_file):
    print("File does not exist. Downloading...")

    u = urllib.request.urlopen(glove_url)
    file_size = int(u.headers["Content-Length"])

    with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, total=file_size, desc="Download Progress") as t:
        urllib.request.urlretrieve(
            glove_url, glove_zip, reporthook=lambda b, bsize, tsize: t.update(bsize))

    print("File downloaded successfully.")
    print("Extracting file...")

    with zipfile.ZipFile(glove_zip, 'r') as zip_ref:
        zip_ref.extract(glove_file)

    print("Extraction completed.")
    print("Deleting zip file...")

    os.remove(glove_zip)

    print("Zip file deleted.")
else:
    print("File already exists.")


embeddings = []
counter = 0
total_lines = sum(1 for line in open(glove_file, 'r', encoding='utf-8'))

with open(glove_file, 'r', encoding='utf-8') as f:
    for line in tqdm(f, total=total_lines, desc="Processing"):
        counter += 1
        values = line.split()
        word = values[0]
        try:
            vector = np.array(values[1:], dtype=np.float32)
            if vector.shape[0] == 300:
                embeddings.append(vector)
        except ValueError:
            continue

embeddings = np.vstack(embeddings)
np.save('glove_embeddings.npy', embeddings)
