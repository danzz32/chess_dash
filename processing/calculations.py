import pandas as pd

def calculate_total_games(df: pd.DataFrame) -> int:
    """Calcula o total de partidas únicas."""
    return df.shape[0]

def calculate_win_rates(df: pd.DataFrame) -> dict:
    """Retorna as taxas de vitória das brancas, pretas e empates."""
    results = df['Result'].value_counts(normalize=True) * 100
    return {
        'white_win_rate': round(results.get('1-0', 0), 2),
        'black_win_rate': round(results.get('0-1', 0), 2),
        'draw_rate': round(results.get('1/2-1/2', 0), 2)
    }

def get_top_players(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Calcula os jogadores com mais vitórias (considerando White e Black)."""
    # Vitórias como brancas
    white_wins = df[df['Result'] == '1-0']['White'].value_counts().reset_index()
    white_wins.columns = ['Jogador', 'Vitórias_Brancas']
    
    # Vitórias como pretas
    black_wins = df[df['Result'] == '0-1']['Black'].value_counts().reset_index()
    black_wins.columns = ['Jogador', 'Vitórias_Pretas']
    
    # Combinar e somar
    total_wins = pd.merge(white_wins, black_wins, on='Jogador', how='outer').fillna(0)
    total_wins['Total_Vitórias'] = total_wins['Vitórias_Brancas'] + total_wins['Vitórias_Pretas']
    
    return total_wins.sort_values('Total_Vitórias', ascending=False).head(top_n)

def get_top_openings(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Retorna as aberturas (ECO) mais comuns."""
    return df['ECO'].value_counts().head(top_n).reset_index()

def get_time_distribution(df: pd.DataFrame) -> pd.Series:
    """Distribuição de jogos por hora do dia."""
    return df['UTCTime'].value_counts().sort_index()

def get_most_common_events(df: pd.DataFrame) -> pd.Series:
    """Tipos de evento mais comuns (e.g., Blitz, Bullet)."""
    return df['Event'].value_counts()