**Automação de Análise de Vendas ERP TOTVS (Python)**  

Este projeto Python oferece uma solução de automação para extrair, limpar e analisar dados de vendas brutos gerados por um sistema ERP TOTVS (presumivelmente no formato TXT).
O script foi desenvolvido para transformar dados complexos em insights de vendas estruturados por categorias (seções, sub-seções, produtos específicos) para facilitar a análise de desempenho de departamentos.

**Sobre o Projeto**  

A necessidade de extrair informações detalhadas de vendas de sistemas ERP frequentemente envolve manipulação manual de arquivos brutos. Este script automatiza esse processo,
permitindo que usuários selecionem um arquivo TXT de vendas diárias e obtenham relatórios consolidados de quantidade e valor vendido por diversas categorias de produtos e departamentos.

-----------------------------------------------------------------------------------------------------------------------------------------

**Funcionalidades Principais**  

Seleção de Arquivo Interativa: Utiliza tkinter para permitir que o usuário selecione visualmente o arquivo TXT de entrada.  
Processamento de Dados Brutos: Lê arquivos TXT com delimitador | (pipe), limpa linhas indesejadas e define o cabeçalho correto.
Engenharia de Features: Extrai informações hierárquicas (Seção, Sub-Seção) de uma coluna combinada (Sec/Grp/SGrp).
Filtragem Inteligente: Remove dados irrelevantes ou incorretos (linhas de cabeçalho duplicadas, valores não numéricos).
Limpeza e Conversão de Tipos: Padroniza e converte colunas para tipos de dados apropriados (datetime, int, float), tratando formatos numéricos brasileiros (vírgula como decimal).
Classificação de Dados: Utiliza dicionários predefinidos para agrupar e categorizar produtos e departamentos (Mercearia, Bazar, Açougue, etc.).
Cálculo de Totais: Funções dedicadas para somar quantidades e custos por Seção, Sub-Seção e Grupos específicos (terceirizados, produtos como Açaí e Café).
Geração de Relatórios: Salva os resultados das análises em um arquivo de texto (resultados_totais.txt) e o abre automaticamente para visualização.  

**Tecnologias Utilizadas**  

Python: Linguagem de programação principal.  
Pandas: Biblioteca robusta para manipulação e análise de dados em DataFrames.  
re (Regular Expressions): Para operações de string (embora não diretamente visível no código fornecido, é comum em manipulação de texto).  
os: Para interação com o sistema operacional (abrir o arquivo de resultados).  
tkinter: Para criar a interface gráfica simples de seleção de arquivo.  

