import pandas as pd
import lxml

df = pd.read_html('gegevens.txt')

print(df[3])