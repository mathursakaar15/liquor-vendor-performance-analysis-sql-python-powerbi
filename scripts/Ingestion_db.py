import pandas as pd
from sqlalchemy import create_engine
import os
import logging
import time

# Absolute path to repo root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
LOGS_DIR = os.path.join(ROOT_DIR, "logs")

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Logging config
logging.basicConfig(
    filename=os.path.join(LOGS_DIR, "ingestion_db.log"),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine = create_engine(f"sqlite:///{os.path.join(ROOT_DIR, 'inventory.db')}")

def ingest_db(df, table_name, engine):
    """Ingest dataframe into SQLite database"""
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)

def load_raw_data(): 
    """Load CSVs from /data and ingest into db"""
    
    # Progress Counter
    total = len([f for f in os.listdir(DATA_DIR) if f.endswith(".csv")])
    index = 0
    
    start = time.time()
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            index += 1
            file_path = os.path.join(DATA_DIR, file)
            df = pd.read_csv(file_path)
            print(f"Ingesting {file} in db:  {index}/{total}")
            logging.info(f"Ingesting {file} in db")
            ingest_db(df, file[:-4], engine)
    end = time.time()
    total_time = (end - start) / 60
    logging.info("----------------Ingestion Complete----------------")
    print("----------------Ingestion Complete----------------")
    logging.info(f"Total time taken: {total_time:.2f} minutes")

if __name__ == "__main__":
    load_raw_data()