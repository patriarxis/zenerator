import pandas as pd

csv_file = 'haikus.csv'
df = pd.read_csv(csv_file)

haikus = df['Haiku'].tolist()

text_file = 'haikus.txt'
with open(text_file, 'w') as file:
    for haiku in haikus:
        file.write(haiku + '\n-\n')
