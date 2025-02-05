import pandas as pd
from faker import Faker
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine
import numpy as np

fake = Faker()
model = SentenceTransformer('all-MiniLM-L6-v2')


def generate_magazine_data(n_records: int):
    magazines = []
    contents = []
    
    categories = ['Technology', 'Science', 'Arts', 'Business', 'Sports']
    
    for i in range(n_records):
        # Generate magazine info
        magazine = {
            'id': i + 1,
            'title': fake.catch_phrase(),
            'author': fake.name(),
            'publication_date': fake.date_between(start_date='-5y'),
            'category': np.random.choice(categories)
        }
        magazines.append(magazine)
        
        # Generate content and vector representation
        # TODO: crawl possible sources from the web.
        content = fake.text(max_nb_chars=1000)
        vector = model.encode(content)
        
        content_record = {
            'id': i + 1,
            'magazine_id': i + 1,
            'content': content,
            'vector_representation': vector
        }
        contents.append(content_record)
    
    return pd.DataFrame(magazines), pd.DataFrame(contents)

if __name__ == '__main__':
    engine = create_engine('postgresql://user:password@localhost/magazine_db')
    # Generate 1M records.
    magazines_df, contents_df = generate_magazine_data(100)
    magazines_df.to_sql('magazine_info', engine, if_exists='append', index=False)
    contents_df.to_sql('magazine_content', engine, if_exists='append', index=False)

    print("CSV files generated successfully.")
