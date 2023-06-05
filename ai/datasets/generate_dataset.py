import pandas as pd

csv_file = 'poetry.csv'
df = pd.read_csv(csv_file)

poems = df['Poem'].tolist()

text_file = 'poems.txt'
with open(text_file, 'w') as file:
    for poem in poems:
        file.write(poem + '\n-\n')
