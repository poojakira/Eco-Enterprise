import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DATA_PATH = r"c:\Users\pooja\Downloads\EcoTrack-Enterprise-main (3)\EcoTrack-Enterprise-main\EcoTrack-Enterprise\EcoTrack-Enterprise\backend\data\dpp_data.csv"

def enrich():
    df = pd.read_csv(DATA_PATH)
    
    categories = ['Industrial Aerospace', 'Medical Hardware', 'Data Center infrastructure', 'Heavy Machinery', 'Renewable Energy Systems']
    regions = ['EMEA Hub-01', 'APAC Nexus-04', 'North America High-Tech', 'Latin America Operations', 'Scandinavian Green Hub']
    vendors = ['Global Dynamics', 'Standard Manufacturing', 'Apex Logistics', 'EcoSystems Inc', 'Precision Parts']
    
    df['Category'] = np.random.choice(categories, len(df))
    df['Region'] = np.random.choice(regions, len(df))
    df['Vendor'] = np.random.choice(vendors, len(df))
    
    # Generate realistic timestamps over the last year
    base = datetime.now() - timedelta(days=365)
    df['Timestamp'] = [base + timedelta(hours=i*2) for i in range(len(df))]
    
    df.to_csv(DATA_PATH, index=False)
    print(f"✅ Dataset enriched with {len(df)} professional records.")

if __name__ == "__main__":
    enrich()
