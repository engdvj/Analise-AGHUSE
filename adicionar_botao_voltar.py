#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar botão de voltar ao index.html em todos os relatórios HTML
"""

import os
import re

def adicionar_botao_voltar(caminho_arquivo):
    """Adiciona botão de voltar ao HTML se ainda não existir"""

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Verificar se já tem o botão
    if 'Voltar para Central' in conteudo or 'btn-voltar' in conteudo:
        return False

    # CSS para o botão
    css_botao = """
        .btn-voltar {
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
            margin: 20px 0;
        }

        .btn-voltar:hover {
            background: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        .btn-voltar::before {
            content: '← ';
        }

        .back-button-container {
            text-align: center;
            padding: 20px 40px 0;
        }
"""

    # Inserir CSS antes do </style>
    conteudo = conteudo.replace('</style>', css_botao + '    </style>')

    # HTML do botão
    html_botao = '''
    <div class="back-button-container">
        <a href="../index.html" class="btn-voltar">Voltar para Central de Relatórios</a>
    </div>
'''

    # Inserir botão após o header (dentro do container)
    # Procurar por </div> logo após o header
    padrao = r'(</div>\s*<div class="content">)'
    substituicao = r'</div>' + html_botao + r'<div class="content">'

    conteudo_novo = re.sub(padrao, substituicao, conteudo, count=1)

    # Se não encontrou o padrão, tentar inserir no início do content
    if conteudo_novo == conteudo:
        padrao = r'(<div class="content">)'
        substituicao = html_botao + r'\1'
        conteudo_novo = re.sub(padrao, substituicao, conteudo, count=1)

    # Salvar arquivo atualizado
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo_novo)

    return True

def processar_todos_relatorios():
    """Processa todos os relatórios HTML"""
    pasta = 'relatorios_html'

    if not os.path.exists(pasta):
        print(f"Pasta {pasta} não encontrada!")
        return

    arquivos_atualizados = 0
    arquivos_ja_tinham = 0

    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.html'):
            caminho = os.path.join(pasta, arquivo)

            if adicionar_botao_voltar(caminho):
                print(f"  [OK] {arquivo}")
                arquivos_atualizados += 1
            else:
                print(f"  [--] {arquivo} (já tinha botão)")
                arquivos_ja_tinham += 1

    print(f"\n{arquivos_atualizados} arquivos atualizados")
    if arquivos_ja_tinham > 0:
        print(f"{arquivos_ja_tinham} arquivos já tinham o botão")

def main():
    print("=" * 60)
    print("Adicionando botão 'Voltar' aos relatórios HTML")
    print("=" * 60)
    print()

    processar_todos_relatorios()

    print()
    print("=" * 60)
    print("Concluído!")
    print("=" * 60)

if __name__ == '__main__':
    main()
