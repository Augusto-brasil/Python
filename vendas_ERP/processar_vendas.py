import pandas as pd
import re
import os
import tkinter as tk
from tkinter import filedialog

def escolher_arquivo():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal
    arquivo = filedialog.askopenfilename(
        title="Escolha o arquivo",
        filetypes=[("Text Files", "*.TXT"), ("All Files", "*.*")]
    )
    return arquivo

valores_desejados = [
    '001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012', '013', '014', '015', '016',
    '017', '018', '019', '020', '021', '022', '023', '024', '025', '026', '027', '028', '029', '030', '031', '032',
    '033', '034', '035', '036', '037', '038', '039', '040', '041', '042', '043', '044', '045', '046', '047', '048',
    '049', '050', '051', '052', '053', '054', '055', '056', '057', '058', '059', '060', '061', '062', '063', '064',
    '065', '066', '067', '068', '069', '070', '071', '072', '073', '074', '075', '076', '077', '078', '079', '080',
    '081', '082', '083', '084', '085', '086', '087', '088', '089', '199', '200', '203', '204', '340', '341', '342',
    '343', '344', '345', '346', '347', '348', '349', '350'
]
# Chama a função para escolher o arquivo
caminho_arquivo = escolher_arquivo()

dados = []
with open(caminho_arquivo, 'r', encoding='latin-1') as file:
    for linha in file:
        linhas = linha.strip().split('|')
        dados.append(linhas)

# Cria o DataFrame sem os parâmetros incorretos
df = pd.DataFrame(dados)

# Define a quarta linha como cabeçalho
df.columns = df.iloc[3]  # Define a quarta linha como cabeçalho
df = df[4:]  # Remove as linhas até a quarta

# Manipulação de colunas e linhas
df.columns = df.columns.str.strip()
df['Secao'] = df['Sec/Grp/SGrp'].str.split('/').str[0]
df['Sub_Secao'] = df['Sec/Grp/SGrp'].str.split('/').str[0:2].str.join('/')
df.rename(columns={'Forn.': 'Fornecedor'}, inplace=True)

# Filtra apenas as linhas onde a coluna 'Secao' contém os valores desejados
df = df[df['Secao'].isin(valores_desejados)]

# Define os valores do cabeçalho que você deseja remover
cabecalho = ['E/S', 'Tp.NF', 'Nro Nota', 'Agenda', 'Data', 'Custo Tot', 'Vencimento', 'Filial', 'Orig/Dest', 'Descrição', 'Sec', 'Sub_Secao']
# Filtra as linhas que não contêm os valores do cabeçalho
df = df[~df.isin(cabecalho).any(axis=1)]
df = df.dropna()

# Selecionando apenas as colunas importantes
df = df[['Data', 'Produto', 'Descrição Produto', 'Fornecedor', 'Sec/Grp/SGrp', 'Qtde', 'Custo Tot', 'Secao','Sub_Secao']]

# Converte a coluna 'Data' para o formato de data
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%y', errors='coerce')

# Convertendo a coluna 'Produto' para numérico, e excluindo as linhas 'NaN'
df['Produto'] = df['Produto'].astype(str).str.replace('-', '')
df['Produto_numeric'] = pd.to_numeric(df['Produto'], errors='coerce')
df = df.dropna(subset=['Produto_numeric'])
df = df.drop(columns=['Produto_numeric'])
df['Produto'] = df['Produto'].astype(int)

# Limpeza e conversão das colunas numéricas
def limpar_e_converter(coluna):
    return coluna.str.replace('.', '').str.replace(',', '.').astype(float)

df['Qtde'] = limpar_e_converter(df['Qtde'])
df['Custo Tot'] = limpar_e_converter(df['Custo Tot'])

# Dicionários fornecidos
secoes = {
    'Mercearia': ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012', '013', '014', '015', '016', '017','018', '019', '020', '021', '022', '023', '024', '025', '026', '027', '028', '029', '071'],
    'Bazar': ['051', '052', '053', '054', '055', '060', '061', '062', '065', '072', '074', '075', '199', '200', '203', '204'],
    'Farmácia': ['340', '341', '342', '343', '344', '345', '346', '347', '348', '349', '350'],
    'Floricultura': ['016'],
    'Dieticos_sec16': ['016'],
    'Frios': ['030'],
    'Salgados': ['032'],
    'Laticínios': ['033'],
    'Congelados': ['036'],
    'Frios_Salgados': ['030', '032', '033', '036'],
    'Aves': ['037'],
    'Carne_Bov_Resfriada': ['038'],
    'Carne_Suína': ['041'],
    'Vísceras': ['043'],
    'Açougue': ['037', '038', '041', '043'],
    'Horti': ['031'],
    'Peixaria': ['034'],
    'Padaria': ['035'],
    'Confeitaria': ['045'],
    'Fast Food': ['039'],
    'Restaurante': ['040'],
    'Buffet_Junino': ['046'],
    'Rotisseria': ['047'],
    'Café_da_Manhã': ['048'],
    'Lanchonete': ['056'],
    'Sucos_Polpas': ['058'],
    'Açaí': ['077'],
    'Sushi': ['078'],
    'Pizza': ['083'],
    'Fast_Food_Geral': ['39', '040', '046', '047', '048', '056', '058', '077', '78', '083']
}

sub_secoes = {
    'SucosFast': ['058/001'],
    'Agua Coco': ['058/002'],
    'Cana Açucar': ['058/003'],
    'Bolo': ['045/001'],
    'Tortas': ['045/002'],
    'Salgados': ['045/003'],
    'Doces': ['045/004']
}

tercerizados = {
    'Salg_terc': ['045/003/002'],
    'Doces_terc': ['045/004/002']
}

produtos_acai = {
    'ACAI POPULAR 1L': ['1520695'],
    'ACAI POPULAR 500ML': ['1297600'],
    'ACAI MEDIO 1L': ['2043890'],
    'ACAI MEDIO 500ML': ['1424904'],
    'ACAI GROSSO 1L': ['1464809'],
    'ACAI GROSSO 500ML': ['1465422'],
    'BACABA 1L': ['1464817'],
    'BACABA 500ML': ['1465430'],
    'ACAI MEDIO CONG 1L': ['1464795']
}

produtos_cafe = {
    '1338250': ['1338250'],
    '2044463': ['2044463'],
    '32737998': ['32737998'],
    '48518': ['48518'],
    '1196464': ['1196464'],
    '31987974': ['31987974'],
    '1157752': ['1157752'],
    '31988008': ['31988008'],
    '2292270': ['2292270'],
    '31988024': ['31988024'],
    '32317425': ['32317425']
}

# Função para calcular totais agrupados por seção
def calcular_totais_secoes(df, secoes):
    resultados = []
    for nome_secao, codigos in secoes.items():
        df_secao = df[df['Secao'].isin(codigos)]
        total_quantidade = df_secao['Qtde'].sum()
        total_custo = df_secao['Custo Tot'].sum()
        resultados.append({
            'Seção': nome_secao,
            'Quantidade Vendida': f"{float(total_quantidade):.2f}".replace('.', ','),
            'Valor Vendido': f"{float(total_custo):.2f}".replace('.', ',')
        })
    return pd.DataFrame(resultados)

# Função para calcular totais agrupados por sub-seção (usando Sec/Grp/SGrp)
def calcular_totais_subsecoes(df, sub_secoes):
    resultados = []
    for nome_subsecao, codigos in sub_secoes.items():
        df_subsecao = df[df['Sub_Secao'].isin(codigos)]
        total_quantidade = df_subsecao['Qtde'].sum()
        total_custo = df_subsecao['Custo Tot'].sum()
        resultados.append({
            'Sub-Seção': nome_subsecao,
            'Quantidade Vendida': f"{float(total_quantidade):.3f}".replace('.', ','),
            'Valor Vendido': f"{float(total_custo):.2f}".replace('.', ',')
        })
    return pd.DataFrame(resultados)

#Função para calcular totais agrupados por tercerizados (usando Sec/Grp/SGrp)
def calcular_totais_tercerizados(df, tercerizados):
    resultados = []
    for nome_terceriza, codigos in tercerizados.items():
        df_terceriza = df[df['Sec/Grp/SGrp'].isin(codigos)]
        total_quantidade = df_terceriza['Qtde'].sum()
        total_custo = df_terceriza['Custo Tot'].sum()
        resultados.append({
            'Grupo': nome_terceriza,
            'Quantidade Vendida': f"{float(total_quantidade):.3f}".replace('.', ','),
            'Valor Vendido': f"{float(total_custo):.2f}".replace('.', ',')
        })
    return pd.DataFrame(resultados)

# Função para calcular totais agrupados por produto
def calcular_totais_produtos(df, produtos):
    resultados = []
    for nome_produto, codigos in produtos.items():
        df_produto = df[df['Produto'].isin([int(codigo) for codigo in codigos])]
        total_quantidade = df_produto['Qtde'].sum()
        total_custo = df_produto['Custo Tot'].sum()
        resultados.append({
            'Produto': nome_produto,
            'Quantidade Vendida': f"{float(total_quantidade):.3f}".replace('.', ','),
            'Valor Vendido': f"{float(total_custo):.2f}".replace('.', ',')
        })
    return pd.DataFrame(resultados)

# Função para salvar os resultados em um arquivo txt
def salvar_txt(df, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        for index, row in df.iterrows():
            linha = " | ".join(f"{key}: {value}" for key, value in row.items())
            f.write(linha + '\n')

print("***Processando arquivo****")

# Caminho do arquivo
caminho_arquivo = r'F:\loja40\BaseDadoslj40\venda_diaria\VND2301.TXT'

# Cálculo dos totais
totais_por_secao = calcular_totais_secoes(df, secoes)
totais_por_subsecao = calcular_totais_subsecoes(df, sub_secoes)
totais_por_terceirizados = calcular_totais_tercerizados(df, tercerizados)
totais_por_produtos_acai = calcular_totais_produtos(df, produtos_acai)
totais_por_produtos_cafe = calcular_totais_produtos(df, produtos_cafe)

with open("resultados_totais.txt", 'w', encoding='utf-8') as f:
    f.write("Totais por seção:\n")
    f.write(totais_por_secao.to_string(index=False))
    f.write("\n\nTotais por sub-seção:\n")
    f.write(totais_por_subsecao.to_string(index=False))
    f.write("\n\nTotais por Terceirizados:\n")
    f.write(totais_por_terceirizados.to_string(index=False))
    f.write("\n\nTotais por produtos Açaí:\n")
    f.write(totais_por_produtos_acai.to_string(index=False))
    f.write("\n\nTotais por produtos Café:\n")
    f.write(totais_por_produtos_cafe.to_string(index=False))

os.startfile("resultados_totais.txt")