"""
Script para atualizar selecionar_semana.html com lista de relatórios semanais
"""
import os
import re
import json
from pathlib import Path
from datetime import datetime


def listar_relatorios_semanais():
    """Lista todos os relatórios semanais disponíveis"""
    relatorios_html = Path('relatorios_html')
    semanais = sorted(relatorios_html.glob('RELATORIO_SEMANAL_*.html'), reverse=True)

    relatorios = []
    for arquivo in semanais:
        # Extrair datas do nome do arquivo
        match = re.match(r'RELATORIO_SEMANAL_(\d{2}-\d{2}-\d{4})_a_(\d{2}-\d{2}-\d{4})\.html', arquivo.name)
        if match:
            data_inicio = match.group(1)
            data_fim = match.group(2)
            relatorios.append({
                'arquivo': arquivo.name,
                'startDate': data_inicio,
                'endDate': data_fim,
                'data_inicio_obj': datetime.strptime(data_inicio, '%d-%m-%Y')
            })

    # Ordenar por data (mais recente primeiro)
    relatorios.sort(key=lambda x: x['data_inicio_obj'], reverse=True)

    return relatorios


def atualizar_selecao_semanas():
    """Atualiza selecionar_semana.html com a lista mais recente de relatórios"""
    selecionar_path = Path('selecionar_semana.html')

    if not selecionar_path.exists():
        print("[ERRO] selecionar_semana.html não encontrado!")
        return

    # Ler arquivo atual
    with open(selecionar_path, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Listar relatórios
    relatorios = listar_relatorios_semanais()
    print(f"Encontrados {len(relatorios)} relatórios semanais")

    # Criar lista JSON dos relatórios para embedar no HTML
    relatorios_json = []
    for rel in relatorios:
        relatorios_json.append({
            'filename': rel['arquivo'],
            'startDate': rel['startDate'],
            'endDate': rel['endDate']
        })

    # Atualizar a função loadHardcodedReports com a lista atualizada
    relatorios_js = json.dumps(relatorios_json, indent=20)

    # Encontrar e substituir a lista de relatórios no JavaScript
    padrao = r'const reports = \[.*?\];'
    novo_conteudo = f'const reports = {relatorios_js};'

    if re.search(padrao, conteudo, re.DOTALL):
        conteudo = re.sub(padrao, novo_conteudo, conteudo, flags=re.DOTALL)
        print("[OK] Lista de relatórios atualizada")
    else:
        print("[AVISO] Padrão não encontrado, tentando inserir nova lista...")
        # Tentar inserir antes de renderReports(reports)
        if 'renderReports(reports)' in conteudo:
            conteudo = conteudo.replace(
                'renderReports(reports);',
                f'{novo_conteudo}\n                    renderReports(reports);'
            )
            print("[OK] Nova lista inserida")
        else:
            print("[ERRO] Não foi possível atualizar a lista de relatórios")
            return

    # Salvar arquivo atualizado
    with open(selecionar_path, 'w', encoding='utf-8') as f:
        f.write(conteudo)

    print(f"[OK] selecionar_semana.html atualizado com {len(relatorios)} relatórios")


if __name__ == '__main__':
    atualizar_selecao_semanas()
