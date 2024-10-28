import pandas as pd

def read_sheet(filepath):
    """Carrega os dados da planilha e retorna um DataFrame."""
    try:
        dataframe = pd.read_excel(filepath)
        print("Dados da planilha carregados com sucesso:")
        print(dataframe.head())  # Exibe as primeiras linhas para verificação
        return dataframe.to_string(index=False)
    except FileNotFoundError:
        print("Erro: O arquivo da planilha não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao ler a planilha: {e}")
        return None