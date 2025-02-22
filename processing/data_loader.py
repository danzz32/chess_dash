import pandas as pd
from tqdm import tqdm  # Opcional para progress bar

def load_and_process_data(filepath: str) -> pd.DataFrame:
    """
    Carrega o dataset em chunks e filtra colunas essenciais.
    Otimizado para grandes arquivos (>4GB).
    """
    # Lista de colunas relevantes para o dashboard
    relevant_columns = [
        'White', 'Black', 'Result', 'UTCDate', 'UTCTime',
        'WhiteElo', 'BlackElo', 'ECO', 'Event', 'Termination'
    ]
    
    # Parâmetros para leitura em chunks
    chunk_size = 10**6  # 1 milhão de linhas por chunk
    chunks = pd.read_csv(filepath, chunksize=chunk_size, usecols=relevant_columns)
    
    processed_chunks = []
    for chunk in tqdm(chunks, desc="Processando chunks"):
        # Converter tempo para datetime
        chunk['UTCTime'] = pd.to_datetime(chunk['UTCTime'], format='%H:%M:%S').dt.hour
        
        # Filtrar linhas inválidas
        chunk = chunk.dropna(subset=['Result', 'White', 'Black'])
        processed_chunks.append(chunk)
    
    return pd.concat(processed_chunks)