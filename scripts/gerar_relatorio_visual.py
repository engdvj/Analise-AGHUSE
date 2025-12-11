import re
import json
from datetime import datetime
from pathlib import Path

def is_relatorio_diario(content):
    """Verifica se é um relatório diário"""
    return 'Relatório AGHUSE -' in content and re.search(r'\d{2}/\d{2}/\d{4}', content.split('\n')[0])

def parse_relatorio_md(file_path):
    """Parse o relatório Markdown e extrai os dados"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    data = {
        'data': '',
        'conexao': 0.0,
        'status': '',
        'horarios_perda': 0,
        'horarios_lentidao': 0,
        'desempenho': [],
        'tipo': 'diario'  # default
    }

    # Detectar tipo de relatório
    if 'Relatório Semanal' in content:
        data['tipo'] = 'semanal'
    elif 'Relatório Geral' in content:
        data['tipo'] = 'geral'

    # Extrair data do título
    match = re.search(r'# Relatório AGHUSE - (\d{2}/\d{2}/\d{4})', content)
    if match:
        data['data'] = match.group(1)

    # Extrair conexão e status
    match = re.search(r'\*\*Conexão:\s*([\d.]+)%\*\*\s*-\s*(\w+)', content)
    if match:
        data['conexao'] = float(match.group(1))
        data['status'] = match.group(2)

    # Extrair problemas
    match = re.search(r'-\s*(\d+)\s*horários com perda', content)
    if match:
        data['horarios_perda'] = int(match.group(1))

    match = re.search(r'-\s*(\d+)\s*horários com lentidão', content)
    if match:
        data['horarios_lentidao'] = int(match.group(1))

    # Extrair desempenho por horário (agora com AGHUSE e Rede Externa)
    desempenho_section = re.search(r'## Desempenho por Horário.*?(?=\*\*Gráfico|\Z)', content, re.DOTALL)
    if desempenho_section:
        lines = desempenho_section.group().split('\n')
        for line in lines:
            # Regex atualizada para capturar AGHUSE e Rede Externa
            match = re.match(r'\|\s*(\d+)h\s*\|\s*([\d.]+)\s*\(([\d.]+)-([\d.]+)\)\s*\|\s*([\d.]+)\s*\(([\d.]+)-([\d.]+)\)\s*\|\s*(.+?)\s*\|', line)
            if not match:
                # Tentar com N/A para rede externa
                match = re.match(r'\|\s*(\d+)h\s*\|\s*([\d.]+)\s*\(([\d.]+)-([\d.]+)\)\s*\|\s*N/A\s*\|\s*(.+?)\s*\|', line)
            if match:
                hora = int(match.group(1))
                latencia = float(match.group(2))
                lat_min = float(match.group(3))
                lat_max = float(match.group(4))

                # Verificar se tem dados de rede externa (8 grupos) ou N/A (5 grupos)
                if len(match.groups()) >= 8:
                    # Tem dados da rede externa
                    latencia_ext = float(match.group(5))
                    lat_min_ext = float(match.group(6))
                    lat_max_ext = float(match.group(7))
                    status_text = match.group(8).strip()
                else:
                    # N/A para rede externa
                    latencia_ext = 0
                    lat_min_ext = 0
                    lat_max_ext = 0
                    status_text = match.group(5).strip()

                # Extrair perdas de AGHUSE e Rede Externa
                perdas_aghuse = 0
                perdas_externo = 0

                # Buscar padrão novo: [AG:Xpkt, EX:Ypkt] (pacotes perdidos)
                perda_ag_match = re.search(r'AG:(\d+)pkt', status_text)
                if perda_ag_match:
                    perdas_aghuse = int(perda_ag_match.group(1))
                else:
                    # Fallback para formato intermediário [AG:X perda(s)]
                    perda_ag_match = re.search(r'AG:(\d+)\s*perda', status_text)
                    if perda_ag_match:
                        perdas_aghuse = int(perda_ag_match.group(1))
                    else:
                        # Fallback para formato muito antigo [N perda(s)]
                        perda_match = re.search(r'\[(\d+)\s*perda', status_text)
                        if perda_match and 'AG:' not in status_text and 'EX:' not in status_text:
                            perdas_aghuse = int(perda_match.group(1))

                perda_ex_match = re.search(r'EX:(\d+)pkt', status_text)
                if perda_ex_match:
                    perdas_externo = int(perda_ex_match.group(1))
                else:
                    # Fallback para formato intermediário [EX:X perda(s)]
                    perda_ex_match = re.search(r'EX:(\d+)\s*perda', status_text)
                    if perda_ex_match:
                        perdas_externo = int(perda_ex_match.group(1))

                # Remover a parte de perdas do status
                status = status_text.split('[')[0].strip()

                data['desempenho'].append({
                    'hora': hora,
                    'latencia': latencia,
                    'lat_min': lat_min,
                    'lat_max': lat_max,
                    'latencia_externo': latencia_ext,
                    'lat_min_externo': lat_min_ext,
                    'lat_max_externo': lat_max_ext,
                    'status': status,
                    'perdas': perdas_aghuse,
                    'perdas_externo': perdas_externo
                })
            else:
                # Fallback para formato antigo (sem rede externa)
                match_old = re.match(r'\|\s*(\d+)h\s*\|\s*([\d.]+)\s*\(([\d.]+)-([\d.]+)\)\s*\|\s*(.+?)\s*\|', line)
                if match_old:
                    hora = int(match_old.group(1))
                    latencia = float(match_old.group(2))
                    lat_min = float(match_old.group(3))
                    lat_max = float(match_old.group(4))
                    status_text = match_old.group(5).strip()

                    perda_match = re.search(r'\[(\d+)\s*perda', status_text)
                    perdas = int(perda_match.group(1)) if perda_match else 0
                    status = status_text.split('[')[0].strip()

                    data['desempenho'].append({
                        'hora': hora,
                        'latencia': latencia,
                        'lat_min': lat_min,
                        'lat_max': lat_max,
                        'latencia_externo': 0,
                        'lat_min_externo': 0,
                        'lat_max_externo': 0,
                        'status': status,
                        'perdas': perdas,
                        'perdas_externo': 0
                    })

    return data


def parse_relatorio_semanal(file_path):
    """Parse relatório semanal e extrai dados para gráficos"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    data = {
        'periodo': '',
        'disponibilidade': 0.0,
        'latencia_media': 0.0,
        'latencia_max': 0,
        'total_testes': 0,
        'testes_com_perda': 0,
        'dias': [],
        'horarios': [],
        # Análises avançadas
        'regressao': {},
        'picos': [],
        'scores_horario': [],
        'analise_dias_semana': [],
        'analise_dias_semana_externo': [],
        'total_anomalias': 0,
        'anomalias': [],
        'distribuicao': [],
        'distribuicao_externo': [],
        # Análise de rotas (tracert)
        'rotas_total': 0,
        'rotas': [],
        'correlacao_rotas': '',
        'mudancas_rota': {
            'total': 0,
            'com_perda': 0,
            'ultimas': []
        }
    }

    # Extrair período
    match = re.search(r'\*\*Período\*\*:\s*(.+)', content)
    if match:
        data['periodo'] = match.group(1).strip()

    # Extrair métricas do sumário
    match = re.search(r'\|\s*\*\*Disponibilidade\*\*\s*\|\s*\*\*([\d.]+)%', content)
    if match:
        data['disponibilidade'] = float(match.group(1))

    match = re.search(r'\|\s*Latência Média\s*\|\s*([\d.]+)\s*ms', content)
    if match:
        data['latencia_media'] = float(match.group(1))

    match = re.search(r'\|\s*Latência Mín/Máx\s*\|\s*\d+/([\d]+)ms', content)
    if match:
        data['latencia_max'] = int(match.group(1))

    match = re.search(r'\|\s*Total de Testes Executados\s*\|\s*(\d+)', content)
    if match:
        data['total_testes'] = int(match.group(1))

    match = re.search(r'\|\s*Testes com Perda\s*\|\s*(\d+)', content)
    if match:
        data['testes_com_perda'] = int(match.group(1))

    # Extrair análise por dia
    dias_section = re.search(r'## Análise por Dia\s*\n\n.*?\n\|---.*?\n((?:\|.*?\n)+)', content, re.DOTALL)
    if dias_section:
        for line in dias_section.group(1).strip().split('\n'):
            # Tentar regex novo formato com AGHUSE e Rede Externa
            match = re.match(r'\|\s*(\d{2}/\d{2}/\d{4})\s*\|\s*(\d+)\s*\|.*?\|\s*\d+\s*\|\s*([\d.]+)%\s*\|\s*([\d.]+)ms\s*\|\s*([\d.]+)ms', line)
            if match:
                data['dias'].append({
                    'data': match.group(1),
                    'testes': int(match.group(2)),
                    'disponibilidade': float(match.group(3)),
                    'latencia': float(match.group(4)),
                    'latencia_externo': float(match.group(5))
                })
            else:
                # Fallback: formato antigo sem rede externa
                match_old = re.match(r'\|\s*(\d{2}/\d{2}/\d{4})\s*\|\s*(\d+)\s*\|.*?\|\s*\d+\s*\|\s*([\d.]+)%\s*\|\s*([\d.]+)ms', line)
                if match_old:
                    data['dias'].append({
                        'data': match_old.group(1),
                        'testes': int(match_old.group(2)),
                        'disponibilidade': float(match_old.group(3)),
                        'latencia': float(match_old.group(4)),
                        'latencia_externo': 0.0
                    })

    # Se latência média não foi encontrada no sumário, calcular a partir dos dias (média ponderada)
    if data['latencia_media'] == 0.0 and data['dias']:
        total_latencia_ponderada = sum(d['latencia'] * d['testes'] for d in data['dias'])
        total_testes = sum(d['testes'] for d in data['dias'])
        data['latencia_media'] = total_latencia_ponderada / total_testes if total_testes > 0 else 0.0

    # Extrair latência por horário (AGHUSE e Rede Externa)
    horario_section = re.search(r'## Análise de Latência por Faixa Horária.*?\n\|.*?\n\|---.*?\n((?:\|.*?\n)+)', content, re.DOTALL)
    if horario_section:
        for line in horario_section.group(1).strip().split('\n'):
            # Tentar regex com dados de rede externa
            match = re.match(r'\|\s*(\d+)h\s*\|\s*([\d.]+)\s*\(([\d.]+)-([\d.]+)\)\s*\|\s*([\d.]+)\s*\(([\d.]+)-([\d.]+)\)\s*\|\s*(.+?)\s*\|', line)
            if not match:
                # Tentar com N/A para rede externa
                match = re.match(r'\|\s*(\d+)h\s*\|\s*([\d.]+)\s*\(([\d.]+)-([\d.]+)\)\s*\|\s*N/A\s*\|\s*(.+?)\s*\|', line)
            if match:
                hora = int(match.group(1))
                latencia = float(match.group(2))
                lat_min = float(match.group(3))
                lat_max = float(match.group(4))

                # Verificar se tem dados de rede externa (8 grupos) ou N/A (5 grupos)
                if len(match.groups()) >= 8:
                    # Tem dados da rede externa
                    latencia_ext = float(match.group(5))
                    lat_min_ext = float(match.group(6))
                    lat_max_ext = float(match.group(7))
                    status_text = match.group(8).strip()
                else:
                    # N/A para rede externa
                    latencia_ext = 0
                    lat_min_ext = 0
                    lat_max_ext = 0
                    status_text = match.group(5).strip()

                # Extrair perdas de AGHUSE e Rede Externa
                perdas_aghuse = 0
                perdas_externo = 0

                # Buscar padrão novo: [AG:Xpkt, EX:Ypkt] (pacotes perdidos)
                perda_ag_match = re.search(r'AG:(\d+)pkt', status_text)
                if perda_ag_match:
                    perdas_aghuse = int(perda_ag_match.group(1))
                else:
                    # Fallback para formato intermediário [AG:X perda(s)]
                    perda_ag_match = re.search(r'AG:(\d+)\s*perda', status_text)
                    if perda_ag_match:
                        perdas_aghuse = int(perda_ag_match.group(1))
                    else:
                        # Fallback para formato muito antigo [N perda(s)]
                        perda_match = re.search(r'\[(\d+)\s*perda', status_text)
                        if perda_match and 'AG:' not in status_text and 'EX:' not in status_text:
                            perdas_aghuse = int(perda_match.group(1))

                perda_ex_match = re.search(r'EX:(\d+)pkt', status_text)
                if perda_ex_match:
                    perdas_externo = int(perda_ex_match.group(1))
                else:
                    # Fallback para formato intermediário [EX:X perda(s)]
                    perda_ex_match = re.search(r'EX:(\d+)\s*perda', status_text)
                    if perda_ex_match:
                        perdas_externo = int(perda_ex_match.group(1))

                status = status_text.split('[')[0].strip()

                data['horarios'].append({
                    'hora': hora,
                    'latencia': latencia,
                    'lat_min': lat_min,
                    'lat_max': lat_max,
                    'latencia_externo': latencia_ext,
                    'lat_min_externo': lat_min_ext,
                    'lat_max_externo': lat_max_ext,
                    'status': status,
                    'perdas': perdas_aghuse,
                    'perdas_externo': perdas_externo
                })
            else:
                # Fallback para formato antigo
                match_old = re.match(r'\|\s*(\d+)h\s*\|\s*([\d.]+)\s*\(([\d.]+)-([\d.]+)\)\s*\|\s*(.+?)\s*\|', line)
                if match_old:
                    hora = int(match_old.group(1))
                    latencia = float(match_old.group(2))
                    lat_min = float(match_old.group(3))
                    lat_max = float(match_old.group(4))
                    status_text = match_old.group(5).strip()

                    perda_match = re.search(r'\[(\d+)\s*perda', status_text)
                    perdas = int(perda_match.group(1)) if perda_match else 0
                    status = status_text.split('[')[0].strip()

                    data['horarios'].append({
                        'hora': hora,
                        'latencia': latencia,
                        'lat_min': lat_min,
                        'lat_max': lat_max,
                        'latencia_externo': 0,
                        'lat_min_externo': 0,
                        'lat_max_externo': 0,
                        'status': status,
                        'perdas': perdas,
                        'perdas_externo': 0
                    })

    # ============================================================
    # PARSING DE ANÁLISES AVANÇADAS
    # ============================================================

    # 1. Regressão Linear
    regressao_match = re.search(r'Regressão Linear.*?([+-]?[\d.]+)ms/dia.*?R² = ([\d.]+).*?Tendência: (\w+)', content)
    if regressao_match:
        data['regressao']['slope'] = float(regressao_match.group(1))
        data['regressao']['r_squared'] = float(regressao_match.group(2))
        data['regressao']['tendencia'] = regressao_match.group(3)

    previsao_match = re.search(r'Previsão 7 dias.*?([\d.]+)ms', content)
    if previsao_match:
        data['regressao']['previsao_7d'] = float(previsao_match.group(1))

    # 2. Horários de Pico
    pico_section = re.search(r'### Horários de Pico.*?\n\n(.*?)(?=### |\Z)', content, re.DOTALL)
    if pico_section:
        for line in pico_section.group(1).splitlines():
            line = line.strip()
            if not line.startswith('-'):
                continue

            pico_match = re.match(
                r'- \*\*(.+?)\*\*:\s*(\d+)h-(\d+)h\s*\(latência média ([\d.,]+)ms(?:,\s*([+-]?[\d.,]+)ms .*?)?(?:,\s*(\d+)h consecutivas)?',
                line
            )
            if pico_match:
                lat_media = float(pico_match.group(4).replace(',', '.'))
                delta = pico_match.group(5)
                duracao = pico_match.group(6)

                # Fallback para pegar duração se o grupo opcional não capturar
                if not duracao:
                    dur_match = re.search(r'(\d+)h consecutivas', line)
                    if dur_match:
                        duracao = int(dur_match.group(1))

                data['picos'].append({
                    'nome': pico_match.group(1),
                    'inicio': int(pico_match.group(2)),
                    'fim': int(pico_match.group(3)),
                    'latencia_media': lat_media,
                    'delta_media': float(delta.replace(',', '.')) if delta else None,
                    'duracao': int(duracao) if duracao else None
                })

    if not data['picos']:
        picos_section = re.findall(r'\*\*(.+?)\*\*:\s*(\d+)h-(\d+)h\s*\(latência média ([\d.]+)ms', content)
        for nome, inicio, fim, lat in picos_section:
            data['picos'].append({
                'nome': nome,
                'inicio': int(inicio),
                'fim': int(fim),
                'latencia_media': float(lat),
                'delta_media': None,
                'duracao': None
            })

    # 3. Scores por Horário (AGHUSE e Rede Externa)
    scores_section = re.search(r'## Score de Qualidade por Horário.*?\n\|.*?\n\|---.*?\n((?:\|.*?\n)+)', content, re.DOTALL)
    if scores_section:
        for line in scores_section.group(1).strip().split('\n'):
            # Tentar formato novo com AGHUSE e Rede Externa
            score_match = re.match(r'\|\s*(\d+)h\s*\|\s*([\d.]+|N/A)\s*\|\s*(\w+|N/A)\s*\|\s*([\d.]+|N/A)\s*\|\s*(\w+|N/A)', line)
            if score_match:
                score_ag = float(score_match.group(2)) if score_match.group(2) != 'N/A' else 0
                class_ag = score_match.group(3) if score_match.group(3) != 'N/A' else ''
                score_ext = float(score_match.group(4)) if score_match.group(4) != 'N/A' else 0
                class_ext = score_match.group(5) if score_match.group(5) != 'N/A' else ''

                data['scores_horario'].append({
                    'hora': int(score_match.group(1)),
                    'score': score_ag,
                    'classificacao': class_ag,
                    'score_externo': score_ext,
                    'classificacao_externo': class_ext
                })
            else:
                # Fallback para formato antigo (sem rede externa)
                score_match_old = re.match(r'\|\s*(\d+)h\s*\|\s*([\d.]+)\s*\|\s*(\w+)', line)
                if score_match_old:
                    data['scores_horario'].append({
                        'hora': int(score_match_old.group(1)),
                        'score': float(score_match_old.group(2)),
                        'classificacao': score_match_old.group(3),
                        'score_externo': 0,
                        'classificacao_externo': ''
                    })

    # 4. Análise por Dia da Semana
    dias_semana_section = re.search(r'## Análise por Dia da Semana.*?\n\|.*?\n\|---.*?\n((?:\|.*?\n)+)', content, re.DOTALL)
    if dias_semana_section:
        for line in dias_semana_section.group(1).strip().split('\n'):
            # Pular linhas de aviso (que contêm ⚠️)
            if '⚠️' in line or 'Poucos dados' in line:
                continue

            # Tentar match com dados completos (com ⚠️ inline é ok, pois regex só captura números)
            dia_match = re.match(r'\|\s*(\w+)\s*\|\s*([\d.]+)ms(?:\s*⚠️)?\s*\|\s*([+-][\d.]+)%\s*\|\s*(\d+)h\s*\(([\d.]+)ms\)', line)
            if dia_match:
                data['analise_dias_semana'].append({
                    'dia': dia_match.group(1),
                    'latencia_media': float(dia_match.group(2)),
                    'vs_media': float(dia_match.group(3)),
                    'pior_horario': int(dia_match.group(4)),
                    'pior_latencia': float(dia_match.group(5))
                })
                continue

            # Tentar match com linha sem dados (-)
            dia_sem_dados_match = re.match(r'\|\s*(\w+)\s*\|\s*-\s*\|\s*-\s*\|\s*-\s*\|\s*0\s*\|', line)
            if dia_sem_dados_match:
                data['analise_dias_semana'].append({
                    'dia': dia_sem_dados_match.group(1),
                    'latencia_media': 0,
                    'vs_media': 0,
                    'pior_horario': 0,
                    'pior_latencia': 0
                })

    # Análise por Dia da Semana - Rede Externa (tabela adicional)
    dias_semana_ext_section = re.search(r'Análise por Dia da Semana - Rede Externa.*?\n\|.*?\n\|---.*?\n((?:\|.*?\n)+)', content, re.DOTALL)
    if dias_semana_ext_section:
        for line in dias_semana_ext_section.group(1).strip().split('\n'):
            if '⚠️' in line or 'Poucos dados' in line:
                continue

            dia_match = re.match(r'\|\s*(\w+)\s*\|\s*([\d.]+)ms(?:\s*⚠️)?\s*\|\s*([+-][\d.]+)%\s*\|\s*(\d+)h\s*\(([\d.]+)ms\)\s*\|\s*(\d+)', line)
            if dia_match:
                data['analise_dias_semana_externo'].append({
                    'dia': dia_match.group(1),
                    'latencia_media': float(dia_match.group(2)),
                    'vs_media': float(dia_match.group(3)),
                    'pior_horario': int(dia_match.group(4)),
                    'pior_latencia': float(dia_match.group(5)),
                    'testes': int(dia_match.group(6))
                })
                continue

            dia_sem_dados_match = re.match(r'\|\s*(\w+)\s*\|\s*-\s*\|\s*-\s*\|\s*-\s*\|\s*0', line)
            if dia_sem_dados_match:
                data['analise_dias_semana_externo'].append({
                    'dia': dia_sem_dados_match.group(1),
                    'latencia_media': 0,
                    'vs_media': 0,
                    'pior_horario': 0,
                    'pior_latencia': 0,
                    'testes': 0
                })

    # 5. Análise de Rotas (Tracert)
    rotas_section = re.search(r'### Análise de Rotas.*?\n\n(.*?)(?=### |\Z)', content, re.DOTALL)
    if rotas_section:
        rotas_text = rotas_section.group(1)

        total_rotas_match = re.search(r'Total de rotas detectadas\*\*:\s*(\d+)', rotas_text)
        if total_rotas_match:
            data['rotas_total'] = int(total_rotas_match.group(1))

        tabela_rotas = re.search(r'\| Rota \| Ocorr.*?\n\|[-|]+\n((?:\|.*?\n)+)', rotas_text, re.DOTALL)
        if tabela_rotas:
            for line in tabela_rotas.group(1).strip().split('\n'):
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                if len(cells) < 5:
                    continue

                nome_rota = cells[0]
                principal = 'principal' in nome_rota.lower()
                taxa_raw = cells[4].replace('%', '').replace(',', '.')

                data['rotas'].append({
                    'nome': nome_rota,
                    'principal': principal,
                    'ocorrencias': int(cells[1]) if cells[1].isdigit() else 0,
                    'com_perda': int(cells[2]) if cells[2].isdigit() else 0,
                    'sem_perda': int(cells[3]) if cells[3].isdigit() else 0,
                    'taxa_perda': float(taxa_raw) if taxa_raw else 0.0
                })

        correlacao_match = re.search(r'Correla.+?Pacotes\*\*:\s*(.+)', rotas_text)
        if correlacao_match:
            data['correlacao_rotas'] = correlacao_match.group(1).strip()

        mudancas_match = re.search(r'Mudanças de rota detectadas\*\*:\s*(\d+)(?:\s*\((\d+)\s+associadas.*?\))?', rotas_text)
        if mudancas_match:
            data['mudancas_rota']['total'] = int(mudancas_match.group(1))
            data['mudancas_rota']['com_perda'] = int(mudancas_match.group(2)) if mudancas_match.group(2) else 0

        ultimas_section = re.search(r'(mudan[cç]as de rota com perda|O que mudou).*?\n\n((?:-.*\n)+)', rotas_text, re.IGNORECASE | re.DOTALL)
        if ultimas_section:
            for line in ultimas_section.group(2).splitlines():
                line = line.strip()
                if line.startswith('-'):
                    data['mudancas_rota']['ultimas'].append(line.lstrip('-').strip())

    # 6. Anomalias
    anomalias_count_match = re.search(r'Total de (\d+) anomalia', content)
    if anomalias_count_match:
        data['total_anomalias'] = int(anomalias_count_match.group(1))

    # Extrair lista de anomalias
    anomalias_section = re.search(r'### Anomalias de Latência.*?\n\n(.*?)(?=## |\Z)', content, re.DOTALL)
    if anomalias_section:
        for line in anomalias_section.group(1).strip().split('\n'):
            line = line.strip()
            if not line:
                continue

            anom_match = re.search(r'(?:⚠️\s*)?\*\*(.+?)\*\*:\s*Latência\s*([\d.]+)ms', line)
            if anom_match:
                severidade = 'media'
                sev_match = re.search(r'Severidade[:\]]\s*(alta|m[ée]dia|baixa)', line, re.IGNORECASE)
                if sev_match:
                    sev_val = sev_match.group(1).lower()
                    if 'alta' in sev_val:
                        severidade = 'alta'
                    elif 'baixa' in sev_val:
                        severidade = 'baixa'
                elif '🔴' in line:
                    severidade = 'alta'

                data['anomalias'].append({
                    'timestamp': anom_match.group(1),
                    'latencia': float(anom_match.group(2)),
                    'severidade': severidade
                })

    # 7. Distribuição (buscar tabelas de AGHUSE e Rede Externa) - robusto a acentuação e linhas
    dist_block = ""
    lines = content.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith('## ') and ('Distribui' in line) and ('Lat' in line):
            # Coletar linhas até o próximo título de nível 2 (## )
            block_lines = []
            for sub in lines[idx + 1:]:
                if sub.startswith('## '):
                    break
                block_lines.append(sub)
            dist_block = "\n".join(block_lines)
            break

    if dist_block:
        tabela_aghuse = re.search(r'\|\s*Faixa\s*\|.*?\n\|[-|]+\n((?:\|.*?\n)+)', dist_block, re.DOTALL)
        if tabela_aghuse:
            for line in tabela_aghuse.group(1).strip().split('\n'):
                dist_match = re.match(r'\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*([\d.]+)%', line)
                if dist_match:
                    data['distribuicao'].append({
                        'faixa': dist_match.group(1).strip(),
                        'frequencia': int(dist_match.group(2)),
                        'percentual': float(dist_match.group(3))
                    })

        tabela_externo = re.search(r'Rede Externa.*?\n\|\s*Faixa\s*\|.*?\n\|[-|]+\n((?:\|.*?\n)+)', dist_block, re.DOTALL)
        if tabela_externo:
            for line in tabela_externo.group(1).strip().split('\n'):
                dist_match = re.match(r'\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*([\d.]+)%', line)
                if dist_match:
                    data['distribuicao_externo'].append({
                        'faixa': dist_match.group(1).strip(),
                        'frequencia': int(dist_match.group(2)),
                        'percentual': float(dist_match.group(3))
                    })

    return data


def generate_html_semanal(data, output_path):
    """Gera HTML visual para relatório semanal/geral com gráficos e abas para análises avançadas"""

    # Preparar dados para gráficos básicos
    dias_labels = [d['data'] for d in data['dias']]
    dias_disp = [d['disponibilidade'] for d in data['dias']]
    dias_lat = [d['latencia'] for d in data['dias']]
    dias_lat_externo = [d.get('latencia_externo', 0) for d in data['dias']]

    horas_labels = [f"{h['hora']:02d}h" for h in data['horarios']]
    horas_lat = [h['latencia'] for h in data['horarios']]
    horas_lat_externo = [h.get('latencia_externo', 0) for h in data['horarios']]
    horas_perdas = [h['perdas'] for h in data['horarios']]
    horas_perdas_externo = [h.get('perdas_externo', 0) for h in data['horarios']]

    # Calcular estatísticas específicas para AGHUSE e Rede Externa
    latencia_media_aghuse = data['latencia_media']  # Já calculado no parse
    latencia_media_externo = sum([l for l in horas_lat_externo if l > 0]) / len([l for l in horas_lat_externo if l > 0]) if any(l > 0 for l in horas_lat_externo) else 0

    total_perdas_aghuse = sum(horas_perdas)
    total_perdas_externo = sum(horas_perdas_externo)

    horarios_perda_aghuse = sum(1 for p in horas_perdas if p > 0)
    horarios_perda_externo = sum(1 for p in horas_perdas_externo if p > 0)

    # Preparar dados para análises avançadas
    scores_horas_aghuse = [s['score'] for s in data.get('scores_horario', [])]
    scores_horas_externo = [s.get('score_externo', 0) for s in data.get('scores_horario', [])]
    scores_labels = [f"{s['hora']:02d}h" for s in data.get('scores_horario', [])]

    # Dados da distribuição
    dist_aghuse = data.get('distribuicao', [])
    dist_externo = data.get('distribuicao_externo', [])
    dist_labels = [d['faixa'] for d in dist_aghuse] or [d['faixa'] for d in dist_externo]
    dist_map_aghuse = {d['faixa']: d['frequencia'] for d in dist_aghuse}
    dist_map_externo = {d['faixa']: d['frequencia'] for d in dist_externo}
    dist_valores_aghuse = [dist_map_aghuse.get(label, 0) for label in dist_labels]
    dist_valores_externo = [dist_map_externo.get(label, 0) for label in dist_labels]

    # Dados de dias da semana
    dias_semana_aghuse = {d['dia']: d.get('latencia_media', 0) for d in data.get('analise_dias_semana', [])}
    dias_semana_externo = {d['dia']: d.get('latencia_media', 0) for d in data.get('analise_dias_semana_externo', [])}
    ordem_dias = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
    if dias_semana_aghuse or dias_semana_externo:
        dias_semana_labels = [d for d in ordem_dias if d in dias_semana_aghuse or d in dias_semana_externo]
    else:
        dias_semana_labels = []
    dias_semana_lat = [dias_semana_aghuse.get(dia, 0) for dia in dias_semana_labels]
    dias_semana_lat_externo = [dias_semana_externo.get(dia, 0) for dia in dias_semana_labels]

    # Montar blocos HTML para aba de anomalias
    picos_html = ""
    if data.get('picos'):
        for pico in data['picos']:
            detalhes = []
            if pico.get('delta_media') is not None:
                detalhes.append(f"{pico['delta_media']:+.1f}ms vs média")
            if pico.get('duracao'):
                detalhes.append(f"{pico['duracao']}h consecutivas")
            info_extra = ', '.join(detalhes) if detalhes else '>=2h consecutivas'
            picos_html += f"<p><strong>{pico['nome']}:</strong> {pico['inicio']:02d}h-{pico['fim']:02d}h (média {pico['latencia_media']:.1f}ms, {info_extra})</p>"
    else:
        picos_html = "<p>Nenhum período de pico identificado (mínimo 2h consecutivas).</p>"

    rotas = data.get('rotas', [])
    ANOMALIAS_PER_PAGE = 10
    anomalias_lista = data.get('anomalias', [])
    anomalias_data_js = json.dumps(anomalias_lista)
    total_paginas_anomalias = max(1, (len(anomalias_lista) + ANOMALIAS_PER_PAGE - 1) // ANOMALIAS_PER_PAGE)

    def format_anomalia_item(anom):
        sev = (anom.get('severidade') or 'média').upper()
        cls = 'high' if sev == 'ALTA' else ''
        lat = anom.get('latencia')
        lat_txt = f"{lat:.1f}".rstrip('0').rstrip('.') if isinstance(lat, (int, float)) else lat
        return (
            f'<li class="anomaly-item {cls}">'
            f'<div class="anomaly-timestamp">{anom.get("timestamp")}</div>'
            f'<div class="anomaly-details">Latência: {lat_txt}ms - Severidade: {sev}</div>'
            f'</li>'
        )

    anomalias_initial_html = ''.join([format_anomalia_item(a) for a in anomalias_lista[:ANOMALIAS_PER_PAGE]])
    if not anomalias_initial_html:
        anomalias_initial_html = '<li class="anomaly-item"><div class="anomaly-timestamp">Nenhuma anomalia detectada</div></li>'

    pagination_initial = ""
    if total_paginas_anomalias > 1:
        buttons = []
        buttons.append('<button disabled>Anterior</button>')
        for i in range(1, min(total_paginas_anomalias, 5) + 1):
            active = ' class="active"' if i == 1 else ''
            buttons.append(f'<button{active}>{i}</button>')
        if total_paginas_anomalias > 5:
            buttons.append('<span style="padding:6px 8px;">...</span>')
            buttons.append(f'<button>{total_paginas_anomalias}</button>')
        buttons.append('<button>Próximo</button>')
        pagination_initial = ''.join(buttons)
    rotas_total = data.get('rotas_total', 0)
    correlacao_texto = (data.get('correlacao_rotas') or '').strip() or 'Dados de tracert insuficientes para análise.'
    mudancas_info = data.get('mudancas_rota', {})
    mudancas_total = mudancas_info.get('total', 0)
    mudancas_com_perda = mudancas_info.get('com_perda', 0)
    ultimas_mudancas = mudancas_info.get('ultimas', [])

    rotas_table_html = ""
    if rotas:
        rotas_table_html = '<table class="rotas-table"><thead><tr><th>Rota</th><th>Ocorrências</th><th>Com Perda</th><th>Sem Perda</th><th>Taxa de Perda</th></tr></thead><tbody>'
        for idx, rota in enumerate(rotas, 1):
            nome_rota = rota.get('nome') or f"Rota {idx}"
            if rota.get('principal') and 'Principal' not in nome_rota:
                nome_rota = f"{nome_rota} (Principal)"
            rotas_table_html += (
                f"<tr><td>{nome_rota}</td>"
                f"<td>{rota.get('ocorrencias', 0)}</td>"
                f"<td>{rota.get('com_perda', 0)}</td>"
                f"<td>{rota.get('sem_perda', 0)}</td>"
                f"<td>{rota.get('taxa_perda', 0):.1f}%</td></tr>"
            )
        rotas_table_html += '</tbody></table>'
    else:
        rotas_table_html = "<p>Dados de tracert insuficientes para análise.</p>"

    mudancas_html = ""
    if mudancas_total:
        mudancas_html = f"<p><strong>Mudanças de rota detectadas:</strong> {mudancas_total} ({mudancas_com_perda} com perda)</p>"
        if ultimas_mudancas:
            mudancas_html += "<p>Últimas mudanças com perda:</p><ul class=\"change-list\">" + ''.join([f"<li>{m}</li>" for m in ultimas_mudancas]) + "</ul>"
    else:
        mudancas_html = "<p>Nenhuma mudança de rota registrada.</p>"

    anomalias_html = ''.join([
        f"""
                        <li class="anomaly-item {'high' if anom.get('severidade') == 'alta' else ''}">
                            <div class="anomaly-timestamp">{anom['timestamp']}</div>
                            <div class="anomaly-details">Latência: {anom['latencia']}ms - Severidade: {anom.get('severidade', 'média').upper()}</div>
                        </li>
        """ for anom in data.get('anomalias', [])[:10]
    ])
    if not anomalias_html:
        anomalias_html = '<li class="anomaly-item"><div class="anomaly-timestamp">Nenhuma anomalia detectada</div></li>'

    html_content = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório Semanal AGHUSE - {data['periodo']}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa;
            padding: 20px;
            color: #2c3e50;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px 40px;
            border-radius: 8px 8px 0 0;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 8px;
        }}
        .header .subtitle {{
            font-size: 16px;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px 40px;
        }}
        .metrics-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}

        @media (min-width: 1200px) {{
            .metrics-row {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}

        @media (max-width: 768px) {{
            .metrics-row {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        @media (max-width: 480px) {{
            .metrics-row {{
                grid-template-columns: 1fr;
            }}
        }}
        .metric-card {{
            background: #f8f9fa;
            padding: 18px;
            border-radius: 6px;
            border-left: 4px solid #3498db;
            min-height: 100px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        .metric-card.success {{ border-left-color: #27ae60; }}
        .metric-card.warning {{ border-left-color: #f39c12; }}
        .metric-card.danger {{ border-left-color: #e74c3c; }}
        .metric-label {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #7f8c8d;
            margin-bottom: 6px;
            font-weight: 600;
        }}
        .metric-value {{
            font-size: 28px;
            font-weight: 600;
            color: #2c3e50;
            line-height: 1.2;
        }}
        .metric-unit {{
            font-size: 16px;
            color: #95a5a6;
            margin-left: 4px;
        }}
        .chart-container {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 6px;
            margin-bottom: 20px;
        }}
        .chart-title {{
            font-size: 16px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #dee2e6;
        }}
        .chart-wrapper {{
            position: relative;
            height: 350px;
        }}
        /* Estilos para Abas */
        .tabs {{
            display: flex;
            border-bottom: 2px solid #dee2e6;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        .tab-button {{
            padding: 14px 28px;
            background: none;
            border: none;
            cursor: pointer;
            font-size: 15px;
            font-weight: 500;
            color: #7f8c8d;
            transition: all 0.3s;
            border-bottom: 3px solid transparent;
            margin-bottom: -2px;
        }}
        .tab-button:hover {{
            color: #3498db;
            background: #f8f9fa;
        }}
        .tab-button.active {{
            color: #3498db;
            border-bottom-color: #3498db;
        }}
        .tab-content {{
            display: none;
            animation: fadeIn 0.3s;
        }}
        .tab-content.active {{
            display: block;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(-10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        /* Estilos para cartões de análise */
        .analysis-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            margin-bottom: 20px;
            border-left: 4px solid #3498db;
        }}
        .analysis-card h3 {{
            font-size: 16px;
            margin-bottom: 12px;
            color: #2c3e50;
        }}
        .analysis-card p {{
            font-size: 14px;
            line-height: 1.6;
            color: #5a6c7d;
        }}
        .anomaly-list {{
            list-style: none;
            padding: 0;
        }}
        .anomaly-item {{
            background: white;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 4px;
            border-left: 3px solid #f39c12;
        }}
        .anomaly-item.high {{
            border-left-color: #e74c3c;
        }}
        .anomaly-timestamp {{
            font-weight: 600;
            color: #2c3e50;
        }}
        .anomaly-details {{
            font-size: 13px;
            color: #7f8c8d;
            margin-top: 4px;
        }}
        .rotas-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            background: white;
            border-radius: 6px;
            overflow: hidden;
        }}
        .rotas-table th {{
            background: #ecf0f1;
            text-align: left;
            padding: 10px 12px;
            font-size: 12px;
            text-transform: uppercase;
            color: #2c3e50;
            letter-spacing: 0.5px;
        }}
        .rotas-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #dee2e6;
            font-size: 14px;
        }}
        .rotas-table tr:last-child td {{
            border-bottom: none;
        }}
        .change-list {{
            margin: 8px 0 0 16px;
            padding: 0;
        }}
        .change-list li {{
            margin-bottom: 4px;
            font-size: 14px;
            color: #5a6c7d;
        }}
        .pagination {{
            display: flex;
            gap: 8px;
            margin-top: 12px;
            flex-wrap: wrap;
        }}
        .pagination button {{
            border: 1px solid #dee2e6;
            background: white;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            color: #2c3e50;
            transition: all 0.2s ease;
        }}
        .pagination button:hover {{
            background: #f1f3f5;
        }}
        .pagination button.active {{
            background: #3498db;
            color: white;
            border-color: #3498db;
        }}
        .pagination {{
            display: flex;
            gap: 8px;
            margin-top: 12px;
            flex-wrap: wrap;
        }}
        .pagination button {{
            border: 1px solid #dee2e6;
            background: white;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            color: #2c3e50;
            transition: all 0.2s ease;
        }}
        .pagination button:hover {{
            background: #f1f3f5;
        }}
        .pagination button.active {{
            background: #3498db;
            color: white;
            border-color: #3498db;
        }}

        .btn-voltar {{
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
        }}

        .btn-voltar:hover {{
            background: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}

        .btn-voltar::before {{
            content: '← ';
        }}

        .back-button-container {{
            text-align: center;
            padding: 20px 40px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Relatório Semanal - Monitoramento AGHUSE</h1>
            <div class="subtitle">Período: {data['periodo']}</div>
        </div>

        <div class="back-button-container">
            <a href="../index.html" class="btn-voltar">Voltar para Central de Relatórios</a>
        </div>

        <div class="content">
            <div class="metrics-row">
                <div class="metric-card success">
                    <div class="metric-label">Disponibilidade</div>
                    <div class="metric-value">{data['disponibilidade']:.2f}<span class="metric-unit">%</span></div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Latência Média (AGHUSE)</div>
                    <div class="metric-value">{latencia_media_aghuse:.1f}<span class="metric-unit">ms</span></div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Latência Média (Rede Externa)</div>
                    <div class="metric-value">{latencia_media_externo:.1f}<span class="metric-unit">ms</span></div>
                </div>
                <div class="metric-card warning">
                    <div class="metric-label">Horários com Perda (AGHUSE)</div>
                    <div class="metric-value">{horarios_perda_aghuse}</div>
                    <div class="metric-unit" style="font-size: 14px;">({total_perdas_aghuse}pkt perdidos)</div>
                </div>
                <div class="metric-card warning">
                    <div class="metric-label">Horários com Perda (Rede Externa)</div>
                    <div class="metric-value">{horarios_perda_externo}</div>
                    <div class="metric-unit" style="font-size: 14px;">({total_perdas_externo}pkt perdidos)</div>
                </div>
                <div class="metric-card danger">
                    <div class="metric-label">Total de Testes</div>
                    <div class="metric-value">{data['total_testes']}</div>
                </div>
            </div>

            <!-- Sistema de Abas -->
            <div class="tabs">
                <button class="tab-button active" data-tab="visao-geral">Visão Geral</button>
                <button class="tab-button" data-tab="analise-avancada">Análise Avançada</button>
                <button class="tab-button" data-tab="anomalias">Anomalias</button>
            </div>

            <!-- Aba 1: Visão Geral -->
            <div class="tab-content active" id="visao-geral">
                <div class="chart-container">
                    <div class="chart-title">Evolução da Disponibilidade por Dia</div>
                    <div class="chart-wrapper">
                        <canvas id="dispChart"></canvas>
                    </div>
                </div>

                <div class="chart-container">
                    <div class="chart-title">Evolução da Latência por Dia - AGHUSE vs Rede Externa</div>
                    <div class="chart-wrapper">
                        <canvas id="latDiaChart"></canvas>
                    </div>
                </div>

                <div class="chart-container">
                    <div class="chart-title">Latência Média por Horário - AGHUSE vs Rede Externa (Todo o Período)</div>
                    <div class="chart-wrapper">
                        <canvas id="latHoraChart"></canvas>
                    </div>
                </div>

                <div class="chart-container">
                    <div class="chart-title">Perdas por Horário - AGHUSE vs Rede Externa</div>
                    <div class="chart-wrapper">
                        <canvas id="perdasChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Aba 2: Análise Avançada -->
            <div class="tab-content" id="analise-avancada">
                <div class="chart-container">
                    <div class="chart-title">Score de Qualidade por Horário - AGHUSE vs Rede Externa (0-10)</div>
                    <div class="chart-wrapper">
                        <canvas id="scoresChart"></canvas>
                    </div>
                </div>

                <div class="chart-container">
                    <div class="chart-title">Distribuição de Latência - AGHUSE vs Rede Externa</div>
                    <div class="chart-wrapper">
                        <canvas id="distribuicaoChart"></canvas>
                    </div>
                </div>

                <div class="chart-container">
                    <div class="chart-title">Comparação por Dia da Semana</div>
                    <div class="chart-wrapper">
                        <canvas id="diasSemanaChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Aba 3: Anomalias -->
            <div class="tab-content" id="anomalias">
                <div class="analysis-card">
                    <h3>Horários de Pico</h3>
                    {picos_html}
                </div>

                <div class="analysis-card">
                    <h3>Análise de Rotas (Tracert)</h3>
                    <p><strong>Total de rotas detectadas:</strong> {rotas_total}</p>
                    <p><strong>Correlação rota x perda:</strong> {correlacao_texto}</p>
                    {rotas_table_html}
                    {mudancas_html}
                </div>

                <div class="analysis-card">
                    <h3>Anomalias de Latência</h3>
                    <p><strong>Total de anomalias detectadas:</strong> {data.get('total_anomalias', 0)}</p>
                    <ul class="anomaly-list" id="anomalias-container">{anomalias_initial_html}</ul>
                    <div class="pagination" id="anomalias-pagination">{pagination_initial}</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
        Chart.defaults.color = '#7f8c8d';

        // Gráfico de Disponibilidade por Dia
        new Chart(document.getElementById('dispChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(dias_labels)},
                datasets: [{{
                    label: 'Disponibilidade (%)',
                    data: {json.dumps(dias_disp)},
                    borderColor: '#27ae60',
                    backgroundColor: 'rgba(39, 174, 96, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.3
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ beginAtZero: false, min: 98, max: 100 }}
                }}
            }}
        }});

        // Gráfico de Latência por Dia
        new Chart(document.getElementById('latDiaChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(dias_labels)},
                datasets: [
                    {{
                        label: 'AGHUSE (10.252.17.132)',
                        data: {json.dumps(dias_lat)},
                        backgroundColor: '#3498db',
                        borderWidth: 0
                    }},
                    {{
                        label: 'Rede Externa (8.8.8.8)',
                        data: {json.dumps(dias_lat_externo)},
                        backgroundColor: '#e74c3c',
                        borderWidth: 0
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }}
                }},
                scales: {{ y: {{ beginAtZero: true }} }}
            }}
        }});

        // Gráfico de Latência por Horário - Comparativo AGHUSE vs Rede Externa
        new Chart(document.getElementById('latHoraChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(horas_labels)},
                datasets: [
                    {{
                        label: 'AGHUSE (10.252.17.132)',
                        data: {json.dumps(horas_lat)},
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.3,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }},
                    {{
                        label: 'Rede Externa (8.8.8.8)',
                        data: {json.dumps(horas_lat_externo)},
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231, 76, 60, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.3,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }}
                }},
                scales: {{ y: {{ beginAtZero: true }} }}
            }}
        }});

        // Gráfico de Perdas por Horário - Comparativo AGHUSE vs Rede Externa
        new Chart(document.getElementById('perdasChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(horas_labels)},
                datasets: [
                    {{
                        label: 'AGHUSE (10.252.17.132)',
                        data: {json.dumps(horas_perdas)},
                        backgroundColor: '#3498db',
                        borderWidth: 0
                    }},
                    {{
                        label: 'Rede Externa (8.8.8.8)',
                        data: {json.dumps(horas_perdas_externo)},
                        backgroundColor: '#e74c3c',
                        borderWidth: 0
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }}
                }},
                scales: {{ y: {{ beginAtZero: true, ticks: {{ stepSize: 1 }} }} }}
            }}
        }});

        // ============================================================
        // Gráficos das Abas Avançadas
        // ============================================================

        // Gráfico de Scores de Qualidade
        new Chart(document.getElementById('scoresChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(scores_labels)},
                datasets: [
                    {{
                        label: 'Score AGHUSE',
                        data: {json.dumps(scores_horas_aghuse)},
                        backgroundColor: '#FF8C00',
                        borderWidth: 0
                    }},
                    {{
                        label: 'Score Rede Externa',
                        data: {json.dumps(scores_horas_externo)},
                        backgroundColor: '#DC143C',
                        borderWidth: 0
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                const score = context.parsed.y;
                                let classificacao = 'Ruim';
                                if (score >= 8.5) classificacao = 'Excelente';
                                else if (score >= 7.0) classificacao = 'Muito Bom';
                                else if (score >= 5.5) classificacao = 'Bom';
                                else if (score >= 4.0) classificacao = 'Regular';
                                return context.dataset.label + ': ' + score.toFixed(1) + ' (' + classificacao + ')';
                            }}
                        }}
                    }}
                }},
                scales: {{ y: {{ beginAtZero: true, max: 10 }} }}
            }}
        }});

        // Gráfico de Distribuição
        new Chart(document.getElementById('distribuicaoChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(dist_labels)},
                datasets: [
                    {{
                        label: 'AGHUSE (10.252.17.132)',
                        data: {json.dumps(dist_valores_aghuse)},
                        backgroundColor: 'rgba(52, 152, 219, 0.7)',
                        borderWidth: 0
                    }},
                    {{
                        label: 'Rede Externa (8.8.8.8)',
                        data: {json.dumps(dist_valores_externo)},
                        backgroundColor: 'rgba(231, 76, 60, 0.7)',
                        borderWidth: 0
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: true, position: 'top' }}
                }},
                scales: {{ y: {{ beginAtZero: true }} }}
            }}
        }});

        // Gráfico Comparativo Dias da Semana
        new Chart(document.getElementById('diasSemanaChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(dias_semana_labels)},
                datasets: [
                    {{
                        label: 'AGHUSE (10.252.17.132)',
                        data: {json.dumps(dias_semana_lat)},
                        backgroundColor: '#3498db',
                        borderWidth: 0
                    }},
                    {{
                        label: 'Rede Externa (8.8.8.8)',
                        data: {json.dumps(dias_semana_lat_externo)},
                        backgroundColor: '#e74c3c',
                        borderWidth: 0
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: true, position: 'top' }}
                }},
                scales: {{ y: {{ beginAtZero: true }} }}
            }}
        }});

        // ============================================================
        // Paginação de Anomalias
        // ============================================================
        const anomaliasData = {anomalias_data_js};
        const ANOMALIAS_PER_PAGE = 10;
        let anomaliaPage = 1;

        function renderAnomalias(page = 1) {{
            const container = document.getElementById('anomalias-container');
            const pagination = document.getElementById('anomalias-pagination');
            if (!container || !pagination) return;

            const total = anomaliasData.length;
            const totalPages = Math.max(1, Math.ceil(total / ANOMALIAS_PER_PAGE));
            anomaliaPage = Math.min(Math.max(page, 1), totalPages);

            const start = (anomaliaPage - 1) * ANOMALIAS_PER_PAGE;
            const slice = anomaliasData.slice(start, start + ANOMALIAS_PER_PAGE);

            if (!slice.length) {{
                container.innerHTML = '<li class="anomaly-item"><div class="anomaly-timestamp">Nenhuma anomalia detectada</div></li>';
            }} else {{
                container.innerHTML = slice.map(anom => {{
                    const sev = (anom.severidade || 'média').toUpperCase();
                    const cls = sev === 'ALTA' ? 'high' : '';
                    const lat = typeof anom.latencia === 'number'
                        ? anom.latencia.toFixed(1).replace('.0', '')
                        : anom.latencia;
                    return `
                        <li class="anomaly-item ${{cls}}">
                            <div class="anomaly-timestamp">${{anom.timestamp}}</div>
                            <div class="anomaly-details">Latência: ${{lat}}ms - Severidade: ${{sev}}</div>
                        </li>
                    `;
                }}).join('');
            }}

            pagination.innerHTML = '';
            if (totalPages <= 1) return;

            const prevBtn = document.createElement('button');
            prevBtn.textContent = 'Anterior';
            prevBtn.disabled = anomaliaPage === 1;
            prevBtn.onclick = () => renderAnomalias(anomaliaPage - 1);
            pagination.appendChild(prevBtn);

            for (let i = 1; i <= totalPages; i++) {{
                if (i > 3 && i < totalPages - 1 && Math.abs(i - anomaliaPage) > 2) {{
                    if (i === 4 || i === totalPages - 2) {{
                        const ellipsis = document.createElement('span');
                        ellipsis.textContent = '...';
                        ellipsis.style.padding = '6px 8px';
                        pagination.appendChild(ellipsis);
                    }}
                    continue;
                }}
                const btn = document.createElement('button');
                btn.textContent = i;
                if (i === anomaliaPage) btn.classList.add('active');
                btn.onclick = () => renderAnomalias(i);
                pagination.appendChild(btn);
            }}

            const nextBtn = document.createElement('button');
            nextBtn.textContent = 'Próximo';
            nextBtn.disabled = anomaliaPage === totalPages;
            nextBtn.onclick = () => renderAnomalias(anomaliaPage + 1);
            pagination.appendChild(nextBtn);
        }}

        // ============================================================
        // Sistema de Abas - Troca de Tabs
        // ============================================================
        document.querySelectorAll('.tab-button').forEach(button => {{
            button.addEventListener('click', () => {{
                const tabId = button.dataset.tab;

                // Remove active de todos
                document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

                // Ativa o selecionado
                button.classList.add('active');
                document.getElementById(tabId).classList.add('active');
            }});
        }});

        // Render inicial das anomalias
        renderAnomalias(1);
    </script>
</body>
</html>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def markdown_to_html_simple(md_content):
    """Converte Markdown simples para HTML"""
    html = md_content

    # Títulos
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

    # Negrito
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

    # Itálico/Citações
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

    # Listas
    html = re.sub(r'^\- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)

    # Tabelas (simplificado)
    lines = html.split('\n')
    result = []
    in_table = False

    for i, line in enumerate(lines):
        if '|' in line and not line.strip().startswith('|---'):
            if not in_table:
                result.append('<table>')
                in_table = True

            cells = [cell.strip() for cell in line.split('|')[1:-1]]

            # Primeira linha é header
            if i > 0 and '|---' in lines[i-1]:
                result.append('<tr>' + ''.join(f'<td>{cell}</td>' for cell in cells) + '</tr>')
            elif i < len(lines)-1 and '|---' in lines[i+1]:
                result.append('<thead><tr>' + ''.join(f'<th>{cell}</th>' for cell in cells) + '</tr></thead><tbody>')
            else:
                result.append('<tr>' + ''.join(f'<td>{cell}</td>' for cell in cells) + '</tr>')
        elif in_table and '|' not in line:
            result.append('</tbody></table>')
            in_table = False
            result.append(line)
        elif '|---' not in line:
            result.append(line)

    if in_table:
        result.append('</tbody></table>')

    html = '\n'.join(result)

    # Parágrafos
    html = re.sub(r'\n\n', '</p><p>', html)
    html = '<p>' + html + '</p>'
    html = html.replace('<p><h', '<h').replace('</h1></p>', '</h1>')
    html = html.replace('</h2></p>', '</h2>').replace('</h3></p>', '</h3>')
    html = html.replace('<p><table>', '<table>').replace('</table></p>', '</table>')
    html = html.replace('<p><ul>', '<ul>').replace('</ul></p>', '</ul>')
    html = html.replace('<p><blockquote>', '<blockquote>').replace('</blockquote></p>', '</blockquote>')
    html = html.replace('<p></p>', '')

    return html


def generate_html_simple(md_path, output_path):
    """Gera HTML simples a partir de Markdown (para relatórios semanal/geral)"""
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extrair título
    title_match = re.search(r'^# (.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else 'Relatório AGHUSE'

    html_content = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            padding: 20px;
            color: #2c3e50;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 40px;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: #f8f9fa;
            border-radius: 6px;
            overflow: hidden;
        }}
        th {{
            background: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #dee2e6;
        }}
        tr:hover {{
            background: #ecf0f1;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        p {{
            margin: 10px 0;
        }}
        strong {{
            color: #2c3e50;
            font-weight: 600;
        }}
        blockquote {{
            border-left: 4px solid #f39c12;
            padding-left: 15px;
            margin: 15px 0;
            color: #7f8c8d;
            font-style: italic;
        }}
        ul {{
            margin: 15px 0 15px 30px;
        }}
        li {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
{markdown_to_html_simple(md_content)}
    </div>
</body>
</html>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def generate_html_report(data, output_path):
    """Gera relatório HTML com design limpo e profissional"""

    # Preparar dados para gráficos - AGHUSE e Rede Externa
    horas = [d['hora'] for d in data['desempenho']]
    latencias = [d['latencia'] for d in data['desempenho']]
    latencias_externo = [d.get('latencia_externo', 0) for d in data['desempenho']]
    perdas = [d['perdas'] for d in data['desempenho']]
    perdas_externo = [d.get('perdas_externo', 0) for d in data['desempenho']]

    # Calcular estatísticas - AGHUSE
    lat_media = sum(latencias) / len(latencias) if latencias else 0
    lat_max = max(latencias) if latencias else 0
    total_perdas = sum(perdas)

    # Calcular estatísticas - Rede Externa
    lat_media_externo = sum([l for l in latencias_externo if l > 0]) / len([l for l in latencias_externo if l > 0]) if any(l > 0 for l in latencias_externo) else 0
    lat_max_externo = max(latencias_externo) if latencias_externo else 0
    total_perdas_externo = sum(perdas_externo)

    # Contar horários com perda para cada destino
    horarios_perda_aghuse = sum(1 for p in perdas if p > 0)
    horarios_perda_externo = sum(1 for p in perdas_externo if p > 0)

    html_content = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório AGHUSE - {data['data']}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            padding: 20px;
            color: #2c3e50;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px 40px;
            border-radius: 8px 8px 0 0;
        }}

        .header h1 {{
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .header .subtitle {{
            font-size: 16px;
            opacity: 0.9;
        }}

        .content {{
            padding: 30px 40px;
        }}

        .metrics-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}

        @media (min-width: 1200px) {{
            .metrics-row {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}

        @media (max-width: 768px) {{
            .metrics-row {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        @media (max-width: 480px) {{
            .metrics-row {{
                grid-template-columns: 1fr;
            }}
        }}

        .metric-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            border-left: 4px solid #dee2e6;
        }}

        .metric-card.primary {{
            border-left-color: #3498db;
        }}

        .metric-card.success {{
            border-left-color: #27ae60;
        }}

        .metric-card.warning {{
            border-left-color: #f39c12;
        }}

        .metric-card.danger {{
            border-left-color: #e74c3c;
        }}

        .metric-label {{
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #7f8c8d;
            margin-bottom: 8px;
            font-weight: 500;
        }}

        .metric-value {{
            font-size: 32px;
            font-weight: 600;
            color: #2c3e50;
            line-height: 1;
        }}

        .metric-unit {{
            font-size: 16px;
            color: #95a5a6;
            margin-left: 4px;
        }}

        .metric-status {{
            font-size: 14px;
            margin-top: 6px;
            color: #7f8c8d;
            font-weight: 500;
        }}

        .charts-section {{
            margin-bottom: 30px;
        }}

        .chart-container {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 6px;
            margin-bottom: 20px;
        }}

        .chart-title {{
            font-size: 16px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #dee2e6;
        }}

        .chart-wrapper {{
            position: relative;
            height: 300px;
        }}

        .chart-wrapper.large {{
            height: 400px;
        }}

        .table-section {{
            margin-top: 30px;
        }}

        .section-title {{
            font-size: 18px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #dee2e6;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: #f8f9fa;
            border-radius: 6px;
            overflow: hidden;
        }}

        th {{
            background: #ecf0f1;
            padding: 12px 15px;
            text-align: left;
            font-size: 13px;
            font-weight: 600;
            color: #2c3e50;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #dee2e6;
            font-size: 14px;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:hover {{
            background: #ffffff;
        }}

        .status-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }}

        .status-otimo {{
            background: #d4edda;
            color: #155724;
        }}

        .status-bom {{
            background: #d1ecf1;
            color: #0c5460;
        }}

        .status-regular {{
            background: #fff3cd;
            color: #856404;
        }}

        .status-ruim {{
            background: #f8d7da;
            color: #721c24;
        }}

        .perda-indicator {{
            color: #e74c3c;
            font-weight: 500;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
            }}
        }}

        @media (max-width: 768px) {{
            .header, .content {{
                padding: 20px;
            }}
            .metrics-row {{
                grid-template-columns: 1fr;
            }}
            .chart-wrapper {{
                height: 250px;
            }}
        }}

        .btn-voltar {{
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
        }}

        .btn-voltar:hover {{
            background: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}

        .btn-voltar::before {{
            content: '← ';
        }}

        .back-button-container {{
            text-align: center;
            padding: 20px 40px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Relatório de Conectividade AGHUSE</h1>
            <div class="subtitle">Análise do dia {data['data']}</div>
        </div>

        <div class="back-button-container">
            <a href="../index.html" class="btn-voltar">Voltar para Central de Relatórios</a>
        </div>

        <div class="content">
            <div class="metrics-row">
                <div class="metric-card success">
                    <div class="metric-label">Disponibilidade</div>
                    <div class="metric-value">{data['conexao']:.2f}<span class="metric-unit">%</span></div>
                    <div class="metric-status">{data['status']}</div>
                </div>

                <div class="metric-card primary">
                    <div class="metric-label">Latência Média (AGHUSE)</div>
                    <div class="metric-value">{lat_media:.1f}<span class="metric-unit">ms</span></div>
                    <div class="metric-status">Máxima: {lat_max:.1f}ms</div>
                </div>

                <div class="metric-card primary">
                    <div class="metric-label">Latência Média (Rede Externa)</div>
                    <div class="metric-value">{lat_media_externo:.1f}<span class="metric-unit">ms</span></div>
                    <div class="metric-status">Máxima: {lat_max_externo:.1f}ms</div>
                </div>

                <div class="metric-card warning">
                    <div class="metric-label">Horários com Perda (AGHUSE)</div>
                    <div class="metric-value">{horarios_perda_aghuse}</div>
                    <div class="metric-status">Total de {total_perdas}pkt perdidos</div>
                </div>

                <div class="metric-card warning">
                    <div class="metric-label">Horários com Perda (Rede Externa)</div>
                    <div class="metric-value">{horarios_perda_externo}</div>
                    <div class="metric-status">Total de {total_perdas_externo}pkt perdidos</div>
                </div>

                <div class="metric-card danger">
                    <div class="metric-label">Horários com Lentidão</div>
                    <div class="metric-value">{data['horarios_lentidao']}</div>
                    <div class="metric-status">Latência > 20ms</div>
                </div>
            </div>

            <div class="charts-section">
                <div class="chart-container">
                    <div class="chart-title">Latência por Horário - AGHUSE vs Rede Externa</div>
                    <div class="chart-wrapper large">
                        <canvas id="latencyChart"></canvas>
                    </div>
                </div>

                <div class="chart-container">
                    <div class="chart-title">Perdas de Conexão por Horário - AGHUSE vs Rede Externa</div>
                    <div class="chart-wrapper">
                        <canvas id="lossChart"></canvas>
                    </div>
                </div>
            </div>

            <div class="table-section">
                <div class="section-title">Desempenho Detalhado por Horário - AGHUSE vs Rede Externa</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <!-- Tabela AGHUSE -->
                    <div>
                        <h3 style="color: #3498db; font-size: 16px; margin-bottom: 10px; text-align: center;">AGHUSE (10.252.17.132)</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th>Horário</th>
                                    <th>Latência Média</th>
                                    <th>Mín - Máx</th>
                                    <th>Status</th>
                                    <th>Perdas</th>
                                </tr>
                            </thead>
                            <tbody>
'''

    for item in data['desempenho']:
        status_class = 'status-otimo'
        if item['status'] == 'Bom':
            status_class = 'status-bom'
        elif item['status'] == 'Regular':
            status_class = 'status-regular'
        elif item['status'] == 'Ruim':
            status_class = 'status-ruim'

        perda_aghuse = f'<span class="perda-indicator">{item["perdas"]}</span>' if item['perdas'] > 0 else '0'

        html_content += f'''
                                <tr>
                                    <td>{item['hora']:02d}h</td>
                                    <td>{item['latencia']:.1f} ms</td>
                                    <td>{item['lat_min']:.0f} - {item['lat_max']:.0f} ms</td>
                                    <td><span class="status-badge {status_class}">{item['status']}</span></td>
                                    <td>{perda_aghuse}</td>
                                </tr>
'''

    html_content += f'''
                            </tbody>
                        </table>
                    </div>
                    <!-- Tabela Rede Externa -->
                    <div>
                        <h3 style="color: #e74c3c; font-size: 16px; margin-bottom: 10px; text-align: center;">Rede Externa (8.8.8.8)</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th>Horário</th>
                                    <th>Latência Média</th>
                                    <th>Mín - Máx</th>
                                    <th>Status</th>
                                    <th>Perdas</th>
                                </tr>
                            </thead>
                            <tbody>
'''

    for item in data['desempenho']:
        status_class = 'status-otimo'
        if item['status'] == 'Bom':
            status_class = 'status-bom'
        elif item['status'] == 'Regular':
            status_class = 'status-regular'
        elif item['status'] == 'Ruim':
            status_class = 'status-ruim'

        perda_externo = f'<span class="perda-indicator">{item.get("perdas_externo", 0)}</span>' if item.get('perdas_externo', 0) > 0 else '0'

        lat_externo = item.get('latencia_externo', 0)
        lat_min_externo = item.get('lat_min_externo', 0)
        lat_max_externo = item.get('lat_max_externo', 0)

        if lat_externo > 0:
            lat_externo_text = f'{lat_externo:.1f} ms'
            lat_range_text = f'{lat_min_externo:.0f} - {lat_max_externo:.0f} ms'
        else:
            lat_externo_text = 'N/A'
            lat_range_text = 'N/A'

        html_content += f'''
                                <tr>
                                    <td>{item['hora']:02d}h</td>
                                    <td>{lat_externo_text}</td>
                                    <td>{lat_range_text}</td>
                                    <td><span class="status-badge {status_class}">{item['status']}</span></td>
                                    <td>{perda_externo}</td>
                                </tr>
'''

    html_content += f'''
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif";
        Chart.defaults.color = '#7f8c8d';

        // Gráfico de Latência - Comparativo AGHUSE vs Rede Externa
        const latencyCtx = document.getElementById('latencyChart').getContext('2d');
        new Chart(latencyCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps([f'{h}h' for h in horas])},
                datasets: [
                    {{
                        label: 'AGHUSE (10.252.17.132)',
                        data: {json.dumps(latencias)},
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.3,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }},
                    {{
                        label: 'Rede Externa (8.8.8.8)',
                        data: {json.dumps(latencias_externo)},
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231, 76, 60, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.3,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }},
                    tooltip: {{
                        backgroundColor: 'rgba(44, 62, 80, 0.9)',
                        padding: 12,
                        titleFont: {{
                            size: 14
                        }},
                        bodyFont: {{
                            size: 13
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{
                            color: '#ecf0f1'
                        }},
                        ticks: {{
                            callback: function(value) {{
                                return value + ' ms';
                            }}
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }}
                    }}
                }}
            }}
        }});

        // Gráfico de Perdas - Comparativo AGHUSE vs Rede Externa
        const lossCtx = document.getElementById('lossChart').getContext('2d');
        new Chart(lossCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps([f'{h}h' for h in horas])},
                datasets: [
                    {{
                        label: 'AGHUSE (10.252.17.132)',
                        data: {json.dumps(perdas)},
                        backgroundColor: '#3498db',
                        borderWidth: 0
                    }},
                    {{
                        label: 'Rede Externa (8.8.8.8)',
                        data: {json.dumps(perdas_externo)},
                        backgroundColor: '#e74c3c',
                        borderWidth: 0
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }},
                    tooltip: {{
                        backgroundColor: 'rgba(44, 62, 80, 0.9)',
                        padding: 12,
                        titleFont: {{
                            size: 14
                        }},
                        bodyFont: {{
                            size: 13
                        }},
                        callbacks: {{
                            label: function(context) {{
                                return context.parsed.y + ' perda(s)';
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 1
                        }},
                        grid: {{
                            color: '#ecf0f1'
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


if __name__ == '__main__':
    import sys
    import io

    # Configurar encoding para UTF-8
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # Diretórios
    relatorios_dir = Path('relatorios')
    output_dir = Path('relatorios_html')
    output_dir.mkdir(exist_ok=True)

    # Processar o relatório mais recente ou todos
    if len(sys.argv) > 1:
        # Arquivo específico
        relatorio_file = Path(sys.argv[1])
        if relatorio_file.exists():
            print(f"Processando {relatorio_file.name}...")
            data = parse_relatorio_md(relatorio_file)
            output_file = output_dir / relatorio_file.name.replace('.md', '.html')
            generate_html_report(data, output_file)
            print(f"[OK] Relatorio HTML gerado: {output_file}")
        else:
            print(f"[ERRO] Arquivo nao encontrado: {relatorio_file}")
    else:
        # Processar todos os relatórios (diários, semanais e geral)
        relatorios_diarios = sorted(relatorios_dir.glob('RELATORIO_DIARIO_*.md'), reverse=True)
        relatorios_semanais = sorted(relatorios_dir.glob('RELATORIO_SEMANAL_*.md'), reverse=True)
        relatorio_geral = relatorios_dir / 'RELATORIO_GERAL.md'

        todos_relatorios = list(relatorios_diarios) + list(relatorios_semanais)
        if relatorio_geral.exists():
            todos_relatorios.append(relatorio_geral)

        if not todos_relatorios:
            print("[ERRO] Nenhum relatorio encontrado!")
        else:
            for relatorio_file in todos_relatorios:
                print(f"Processando {relatorio_file.name}...")
                try:
                    output_file = output_dir / relatorio_file.name.replace('.md', '.html')

                    # Verificar tipo de relatório
                    if 'DIARIO' in relatorio_file.name:
                        # Relatório diário - usar parser completo com gráficos
                        data = parse_relatorio_md(relatorio_file)
                        generate_html_report(data, output_file)
                    elif 'SEMANAL' in relatorio_file.name or 'GERAL' in relatorio_file.name:
                        # Relatório semanal/geral - usar parser específico com gráficos
                        data = parse_relatorio_semanal(relatorio_file)
                        generate_html_semanal(data, output_file)
                    else:
                        # Fallback - converter Markdown simples
                        generate_html_simple(relatorio_file, output_file)

                    print(f"[OK] {output_file.name}")
                except Exception as e:
                    print(f"[ERRO] Erro ao processar {relatorio_file.name}: {e}")

            print(f"\nProcessamento concluido! {len(todos_relatorios)} relatorios convertidos.")
            print(f"Relatorios HTML salvos em: {output_dir.absolute()}")

            # Atualizar index.html com lista de relatórios
            print(f"\nAtualizando index.html...")
            try:
                import subprocess
                subprocess.run(['python', 'scripts/atualizar_index_completo.py'], check=True)
                print("[OK] index.html atualizado com sucesso")
            except Exception as e:
                print(f"[AVISO] Erro ao atualizar index.html: {e}")
