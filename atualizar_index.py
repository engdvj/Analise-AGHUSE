#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar automaticamente o index.html com os relatórios disponíveis
"""

import os
import re
from datetime import datetime

def obter_relatorios_disponiveis():
    """Busca todos os relatórios diários disponíveis"""
    pasta_relatorios = 'relatorios_html'
    relatorios = []

    if not os.path.exists(pasta_relatorios):
        print(f"Pasta {pasta_relatorios} não encontrada!")
        return relatorios

    # Procurar por arquivos RELATORIO_DIARIO_*.html
    for arquivo in os.listdir(pasta_relatorios):
        if arquivo.startswith('RELATORIO_DIARIO_') and arquivo.endswith('.html'):
            # Extrair a data do nome do arquivo
            # Formato: RELATORIO_DIARIO_2025-12-03.html
            match = re.search(r'RELATORIO_DIARIO_(\d{4}-\d{2}-\d{2})\.html', arquivo)
            if match:
                data = match.group(1)
                relatorios.append(data)

    # Ordenar as datas
    relatorios.sort()
    return relatorios

def atualizar_index_html(relatorios):
    """Atualiza o arquivo index.html com a lista de relatórios"""
    arquivo_index = 'index.html'

    if not os.path.exists(arquivo_index):
        print(f"Arquivo {arquivo_index} não encontrado!")
        return False

    # Ler o conteúdo do arquivo
    with open(arquivo_index, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Criar a lista de relatórios no formato JavaScript
    relatorios_js = ',\n            '.join([f"'{r}'" for r in relatorios])

    # Padrão para encontrar a seção de relatórios disponíveis
    padrao = r'(const availableReports = new Set\(\[)(.*?)(\]\);)'

    # Substituir a lista de relatórios
    novo_conteudo = re.sub(
        padrao,
        f'\\1\n            {relatorios_js}\n        \\3',
        conteudo,
        flags=re.DOTALL
    )

    # Salvar o arquivo atualizado
    with open(arquivo_index, 'w', encoding='utf-8') as f:
        f.write(novo_conteudo)

    return True

def main():
    print("=" * 60)
    print("Atualizando index.html com relatórios disponíveis")
    print("=" * 60)

    # Obter relatórios disponíveis
    relatorios = obter_relatorios_disponiveis()

    if not relatorios:
        print("\nNenhum relatório encontrado!")
        return

    print(f"\nRelatórios encontrados: {len(relatorios)}")
    for rel in relatorios:
        print(f"  - {rel}")

    # Atualizar index.html
    if atualizar_index_html(relatorios):
        print(f"\n[OK] index.html atualizado com sucesso!")
        print(f"[OK] Total de {len(relatorios)} relatorios disponiveis")
    else:
        print("\n[ERRO] Erro ao atualizar index.html")

if __name__ == '__main__':
    main()
