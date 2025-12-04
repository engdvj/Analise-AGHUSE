import os
import re
from datetime import datetime, timedelta
from collections import defaultdict

def extrair_dados_teste(conteudo):
    """Extrai os dados principais de um arquivo de teste"""
    dados = {
        'timestamp': None,
        'data': None,
        'hora': None,
        'datetime': None,
        'ping_aghuse': {'min': None, 'max': None, 'media': None, 'perda': None},
        'ping_interno': {'min': None, 'max': None, 'media': None, 'perda': None},
        'ping_externo': {'min': None, 'max': None, 'media': None, 'perda': None},
        'tracert_saltos': 0
    }

    # Extrair timestamp
    match = re.search(r'ID_TESTE\s+:\s+(.+)', conteudo)
    if match:
        dados['timestamp'] = match.group(1).strip()

    # Extrair data e hora
    match = re.search(r'DATA_TESTE\s+:\s+(\d+/\d+/\d+)', conteudo)
    if match:
        dados['data'] = match.group(1)

    match = re.search(r'HORA_TESTE\s+:\s+(\d+:\d+:\d+)', conteudo)
    if match:
        dados['hora'] = match.group(1)

    # Criar objeto datetime para facilitar ordenação e agrupamento
    if dados['data'] and dados['hora']:
        try:
            dados['datetime'] = datetime.strptime(f"{dados['data']} {dados['hora']}", "%d/%m/%Y %H:%M:%S")
        except:
            pass

    # Extrair dados do ping aghuse.saude.ba.gov.br
    match = re.search(r'\[3/7\] PING.*?M.nimo = (\d+)ms.*?M.ximo = (\d+)ms.*?M.dia = (\d+)ms', conteudo, re.DOTALL)
    if match:
        dados['ping_aghuse']['min'] = int(match.group(1))
        dados['ping_aghuse']['max'] = int(match.group(2))
        dados['ping_aghuse']['media'] = int(match.group(3))

    match = re.search(r'\[3/7\] PING.*?Perdidos = (\d+) \((\d+)%', conteudo, re.DOTALL)
    if match:
        dados['ping_aghuse']['perda'] = int(match.group(2))

    # Extrair dados do ping interno (10.252.17.132)
    match = re.search(r'\[5/7\] PING 10\.252\.17\.132.*?M.nimo = (\d+)ms.*?M.ximo = (\d+)ms.*?M.dia = (\d+)ms', conteudo, re.DOTALL)
    if match:
        dados['ping_interno']['min'] = int(match.group(1))
        dados['ping_interno']['max'] = int(match.group(2))
        dados['ping_interno']['media'] = int(match.group(3))

    match = re.search(r'\[5/7\] PING 10\.252\.17\.132.*?Perdidos = (\d+) \((\d+)%', conteudo, re.DOTALL)
    if match:
        dados['ping_interno']['perda'] = int(match.group(2))

    # Extrair dados do ping externo (8.8.8.8)
    match = re.search(r'\[6/7\] PING 8\.8\.8\.8.*?M.nimo = (\d+)ms.*?M.ximo = (\d+)ms.*?M.dia = (\d+)ms', conteudo, re.DOTALL)
    if match:
        dados['ping_externo']['min'] = int(match.group(1))
        dados['ping_externo']['max'] = int(match.group(2))
        dados['ping_externo']['media'] = int(match.group(3))

    match = re.search(r'\[6/7\] PING 8\.8\.8\.8.*?Perdidos = (\d+) \((\d+)%', conteudo, re.DOTALL)
    if match:
        dados['ping_externo']['perda'] = int(match.group(2))

    # Contar saltos do tracert
    tracert_section = re.search(r'\[4/7\] TRACERT.*?Rastreamento conclu.do', conteudo, re.DOTALL)
    if tracert_section:
        saltos = len(re.findall(r'^\s*\d+\s+', tracert_section.group(0), re.MULTILINE))
        dados['tracert_saltos'] = saltos

    return dados

def processar_todos_arquivos(pasta):
    """Processa todos os arquivos de teste na pasta e subpastas"""
    todos_dados = []

    # Procurar arquivos .txt diretamente na pasta
    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)

        # Se for um diretório, processar recursivamente
        if os.path.isdir(caminho):
            for sub_arquivo in os.listdir(caminho):
                if sub_arquivo.endswith('.txt'):
                    caminho_completo = os.path.join(caminho, sub_arquivo)
                    try:
                        with open(caminho_completo, 'r', encoding='cp1252', errors='ignore') as f:
                            conteudo = f.read()
                            dados = extrair_dados_teste(conteudo)
                            if dados['timestamp'] and dados['datetime']:
                                todos_dados.append(dados)
                    except Exception as e:
                        print(f"  [ERRO] Falha ao processar {sub_arquivo}: {e}")

        # Se for arquivo .txt diretamente na pasta
        elif arquivo.endswith('.txt'):
            try:
                with open(caminho, 'r', encoding='cp1252', errors='ignore') as f:
                    conteudo = f.read()
                    dados = extrair_dados_teste(conteudo)
                    if dados['timestamp'] and dados['datetime']:
                        todos_dados.append(dados)
            except Exception as e:
                print(f"  [ERRO] Falha ao processar {arquivo}: {e}")

    return sorted(todos_dados, key=lambda x: x['datetime'])

def agrupar_por_dia(dados_lista):
    """Agrupa dados por dia"""
    dados_por_dia = defaultdict(list)
    for dados in dados_lista:
        dia = dados['datetime'].date()
        dados_por_dia[dia].append(dados)
    return dict(dados_por_dia)

def calcular_estatisticas_dia(dados_dia):
    """Calcula estatísticas para um dia específico"""
    if not dados_dia:
        return None

    testes_com_perda = [d for d in dados_dia if d['ping_aghuse']['perda'] and d['ping_aghuse']['perda'] > 0]
    testes_latencia_alta = [d for d in dados_dia if d['ping_aghuse']['media'] and d['ping_aghuse']['media'] > 20]

    # Calcular disponibilidade real baseada na perda de pacotes
    # Cada teste envia 20 pacotes, então calculamos a disponibilidade real
    total_pacotes_enviados = len(dados_dia) * 20
    total_pacotes_perdidos = sum(
        (d['ping_aghuse']['perda'] / 100) * 20
        for d in dados_dia if d['ping_aghuse']['perda']
    )
    disponibilidade = ((total_pacotes_enviados - total_pacotes_perdidos) / total_pacotes_enviados) * 100

    stats = {
        'total_testes': len(dados_dia),
        'testes_com_perda': len(testes_com_perda),
        'testes_sem_perda': len(dados_dia) - len(testes_com_perda),
        'total_pacotes_enviados': total_pacotes_enviados,
        'total_pacotes_perdidos': int(total_pacotes_perdidos),
        'disponibilidade': disponibilidade,
        'aghuse_media': sum(d['ping_aghuse']['media'] for d in dados_dia if d['ping_aghuse']['media']) / len(dados_dia),
        'aghuse_min': min(d['ping_aghuse']['min'] for d in dados_dia if d['ping_aghuse']['min']),
        'aghuse_max': max(d['ping_aghuse']['max'] for d in dados_dia if d['ping_aghuse']['max']),
        'interno_media': sum(d['ping_interno']['media'] for d in dados_dia if d['ping_interno']['media']) / len(dados_dia),
        'externo_media': sum(d['ping_externo']['media'] for d in dados_dia if d['ping_externo']['media']) / len(dados_dia),
        'horarios_com_perda': [d['hora'] for d in testes_com_perda],
        'horarios_latencia_alta': [d['hora'] for d in testes_latencia_alta],
        'lista_testes_com_perda': testes_com_perda,
        'latencia_alta_count': len(testes_latencia_alta)
    }

    return stats

def calcular_estatisticas_geral(dados_lista):
    """Calcula estatísticas gerais dos testes"""
    if not dados_lista:
        return {}

    testes_com_perda = [d for d in dados_lista if d['ping_aghuse']['perda'] and d['ping_aghuse']['perda'] > 0]
    testes_latencia_alta = [d for d in dados_lista if d['ping_aghuse']['media'] and d['ping_aghuse']['media'] > 20]

    # Calcular disponibilidade real baseada na perda de pacotes
    total_pacotes_enviados = len(dados_lista) * 20
    total_pacotes_perdidos = sum(
        (d['ping_aghuse']['perda'] / 100) * 20
        for d in dados_lista if d['ping_aghuse']['perda']
    )
    disponibilidade = ((total_pacotes_enviados - total_pacotes_perdidos) / total_pacotes_enviados) * 100

    stats = {
        'total_testes': len(dados_lista),
        'testes_com_perda': len(testes_com_perda),
        'testes_sem_perda': len(dados_lista) - len(testes_com_perda),
        'total_pacotes_enviados': total_pacotes_enviados,
        'total_pacotes_perdidos': int(total_pacotes_perdidos),
        'disponibilidade': disponibilidade,
        'aghuse_media': sum(d['ping_aghuse']['media'] for d in dados_lista if d['ping_aghuse']['media']) / len(dados_lista),
        'aghuse_min': min(d['ping_aghuse']['min'] for d in dados_lista if d['ping_aghuse']['min']),
        'aghuse_max': max(d['ping_aghuse']['max'] for d in dados_lista if d['ping_aghuse']['max']),
        'interno_media': sum(d['ping_interno']['media'] for d in dados_lista if d['ping_interno']['media']) / len(dados_lista),
        'externo_media': sum(d['ping_externo']['media'] for d in dados_lista if d['ping_externo']['media']) / len(dados_lista),
        'lista_testes_com_perda': testes_com_perda,
        'latencia_alta_count': len(testes_latencia_alta)
    }

    return stats

def analisar_horarios_problematicos(dados_por_dia):
    """Analisa padrões de horários com problemas"""
    horarios_problemas = defaultdict(int)
    horarios_latencia_alta = defaultdict(int)

    for dados_dia in dados_por_dia.values():
        for d in dados_dia:
            hora_int = int(d['hora'].split(':')[0])

            # Contar problemas por hora
            if d['ping_aghuse']['perda'] and d['ping_aghuse']['perda'] > 0:
                horarios_problemas[hora_int] += 1

            # Contar latência alta por hora
            if d['ping_aghuse']['media'] and d['ping_aghuse']['media'] > 20:
                horarios_latencia_alta[hora_int] += 1

    return dict(horarios_problemas), dict(horarios_latencia_alta)

def gerar_relatorio_diario(dia, dados_dia, stats):
    """Gera relatório diário em formato markdown"""
    md = []

    data_formatada = dia.strftime("%d/%m/%Y")
    md.append(f"# Relatório Diário - Conectividade AGHUSE\n")
    md.append(f"**Data**: {data_formatada}\n\n")

    # Sumário Executivo
    md.append("## Sumário Executivo\n\n")
    md.append("| Métrica | Valor |\n")
    md.append("|---------|-------|\n")
    md.append(f"| Total de Testes Executados | {stats['total_testes']} |\n")
    md.append(f"| Testes sem Perda | {stats['testes_sem_perda']} |\n")
    md.append(f"| Testes com Perda | {stats['testes_com_perda']} |\n")
    md.append(f"| Total de Pacotes Enviados | {stats['total_pacotes_enviados']} |\n")
    md.append(f"| Total de Pacotes Perdidos | {stats['total_pacotes_perdidos']} |\n")
    md.append(f"| **Disponibilidade** | **{stats['disponibilidade']:.2f}%** |\n\n")

    # Métricas de Latência
    md.append("## Métricas de Latência\n\n")
    md.append("| Destino | Latência Média (ms) | Mínima (ms) | Máxima (ms) |\n")
    md.append("|---------|---------------------|-------------|-------------|\n")
    md.append(f"| AGHUSE (10.252.17.132) | {stats['aghuse_media']:.1f} | {stats['aghuse_min']} | {stats['aghuse_max']} |\n")
    md.append(f"| IP Interno (10.252.17.132) | {stats['interno_media']:.1f} | - | - |\n")
    md.append(f"| Google DNS (8.8.8.8) | {stats['externo_media']:.1f} | - | - |\n\n")

    # Incidentes com Perda de Pacotes
    if stats['testes_com_perda'] > 0:
        md.append("## Incidentes com Perda de Pacotes\n\n")
        md.append(f"Total de {stats['testes_com_perda']} teste(s) apresentaram perda de pacotes:\n\n")
        md.append("| Horário | Latência Média (ms) | Perda (%) | Latência Min/Max (ms) |\n")
        md.append("|---------|---------------------|-----------|----------------------|\n")
        for d in stats['lista_testes_com_perda']:
            md.append(f"| {d['hora']} | {d['ping_aghuse']['media']} | {d['ping_aghuse']['perda']} | {d['ping_aghuse']['min']}/{d['ping_aghuse']['max']} |\n")
        md.append("\n")

    # Testes com Latência Elevada
    if stats['latencia_alta_count'] > 0:
        md.append("## Testes com Latência Elevada\n\n")
        md.append(f"- **Quantidade**: {stats['latencia_alta_count']} teste(s) com latência superior a 20ms\n")
        horarios = ', '.join(stats['horarios_latencia_alta'][:10])
        if len(stats['horarios_latencia_alta']) > 10:
            horarios += f" (e mais {len(stats['horarios_latencia_alta']) - 10})"
        md.append(f"- **Horários**: {horarios}\n\n")

    # Detalhamento por Horário
    md.append("## Detalhamento por Horário\n\n")
    md.append("| Horário | Latência (ms) | Min/Max (ms) | Perda (%) |\n")
    md.append("|---------|---------------|--------------|----------|\n")

    for d in dados_dia:
        perda_text = "0" if d['ping_aghuse']['perda'] == 0 else str(d['ping_aghuse']['perda'])
        md.append(f"| {d['hora']} | {d['ping_aghuse']['media']} | {d['ping_aghuse']['min']}/{d['ping_aghuse']['max']} | {perda_text} |\n")

    # Análise e Conclusão
    md.append(f"\n## Análise e Conclusão\n\n")

    # Análise de disponibilidade
    if stats['disponibilidade'] >= 99.9:
        md.append(f"**Disponibilidade**: {stats['disponibilidade']:.2f}% - Excelente. Sistema operando dentro dos parâmetros SLA.\n\n")
    elif stats['disponibilidade'] >= 99.0:
        md.append(f"**Disponibilidade**: {stats['disponibilidade']:.2f}% - Boa. Sistema operacional com pequenos desvios.\n\n")
    elif stats['disponibilidade'] >= 95.0:
        md.append(f"**Disponibilidade**: {stats['disponibilidade']:.2f}% - Aceitável. Recomenda-se monitoramento.\n\n")
    else:
        md.append(f"**Disponibilidade**: {stats['disponibilidade']:.2f}% - Crítica. Requer investigação imediata.\n\n")

    # Análise de latência
    if stats['aghuse_media'] < 10:
        md.append(f"**Latência**: Média de {stats['aghuse_media']:.1f}ms - Excelente performance de rede.\n\n")
    elif stats['aghuse_media'] < 20:
        md.append(f"**Latência**: Média de {stats['aghuse_media']:.1f}ms - Performance adequada.\n\n")
    elif stats['aghuse_media'] < 50:
        md.append(f"**Latência**: Média de {stats['aghuse_media']:.1f}ms - Performance aceitável, monitorar tendências.\n\n")
    else:
        md.append(f"**Latência**: Média de {stats['aghuse_media']:.1f}ms - Performance degradada, investigação necessária.\n\n")

    return ''.join(md)

def gerar_relatorio_semanal(dados_por_dia):
    """Gera relatório semanal consolidado"""
    md = []

    # Validar se há dados
    if not dados_por_dia:
        md.append("# Relatório Semanal - Monitoramento de Conectividade AGHUSE\n\n")
        md.append("**Aviso**: Nenhum dado disponível para gerar o relatório.\n")
        return ''.join(md)

    dias_ordenados = sorted(dados_por_dia.keys())
    primeira_data = dias_ordenados[0].strftime("%d/%m/%Y")
    ultima_data = dias_ordenados[-1].strftime("%d/%m/%Y")

    md.append(f"# Relatório Semanal - Monitoramento de Conectividade AGHUSE\n")
    md.append(f"**Período**: {primeira_data} a {ultima_data}\n\n")

    # Estatísticas gerais do período
    todos_dados = []
    for dados_dia in dados_por_dia.values():
        todos_dados.extend(dados_dia)

    stats_geral = calcular_estatisticas_geral(todos_dados)

    # Sumário Executivo
    md.append("## Sumário Executivo\n\n")
    md.append("| Métrica | Valor |\n")
    md.append("|---------|-------|\n")
    md.append(f"| Total de Testes Executados | {stats_geral['total_testes']} |\n")
    md.append(f"| Testes sem Perda | {stats_geral['testes_sem_perda']} |\n")
    md.append(f"| Testes com Perda | {stats_geral['testes_com_perda']} |\n")
    md.append(f"| Total de Pacotes Enviados | {stats_geral['total_pacotes_enviados']} |\n")
    md.append(f"| Total de Pacotes Perdidos | {stats_geral['total_pacotes_perdidos']} |\n")
    md.append(f"| **Disponibilidade** | **{stats_geral['disponibilidade']:.2f}%** |\n")
    md.append(f"| Latência Média | {stats_geral['aghuse_media']:.1f}ms |\n")
    md.append(f"| Latência Mín/Máx | {stats_geral['aghuse_min']}/{stats_geral['aghuse_max']}ms |\n\n")

    # Análise por Dia
    md.append("## Análise por Dia\n\n")
    md.append("| Data | Testes | Sem Perda / Com Perda | Pacotes Perdidos | Disponibilidade | Latência Média |\n")
    md.append("|------|--------|-----------------------|------------------|-----------------|----------------|\n")

    for dia in dias_ordenados:
        dados_dia = dados_por_dia[dia]
        stats = calcular_estatisticas_dia(dados_dia)
        data_fmt = dia.strftime("%d/%m/%Y")

        md.append(f"| {data_fmt} | {stats['total_testes']} | {stats['testes_sem_perda']} / {stats['testes_com_perda']} | {stats['total_pacotes_perdidos']} | {stats['disponibilidade']:.2f}% | {stats['aghuse_media']:.1f}ms |\n")

    # Análise de Horários Críticos
    horarios_problemas, horarios_latencia = analisar_horarios_problematicos(dados_por_dia)

    if horarios_problemas:
        md.append("\n## Análise de Horários Críticos\n\n")
        md.append("### Distribuição de Perda de Pacotes por Horário\n\n")
        md.append("| Faixa Horária | Ocorrências | Porcentagem do Total |\n")
        md.append("|---------------|-------------|---------------------|\n")

        for hora in sorted(horarios_problemas.keys(), key=lambda h: horarios_problemas[h], reverse=True):
            count = horarios_problemas[hora]
            percent = (count / stats_geral['testes_com_perda']) * 100
            md.append(f"| {hora:02d}:00 - {hora:02d}:59 | {count} | {percent:.1f}% |\n")
        md.append("\n")

    if horarios_latencia:
        md.append("### Distribuição de Latência Elevada por Horário\n\n")
        md.append("| Faixa Horária | Ocorrências |\n")
        md.append("|---------------|-------------|\n")

        for hora in sorted(horarios_latencia.keys(), key=lambda h: horarios_latencia[h], reverse=True)[:10]:
            count = horarios_latencia[hora]
            md.append(f"| {hora:02d}:00 - {hora:02d}:59 | {count} |\n")
        md.append("\n")

    # Registro de Incidentes
    if stats_geral['testes_com_perda'] > 0:
        md.append("## Registro de Incidentes\n\n")
        md.append(f"Total de {stats_geral['testes_com_perda']} teste(s) com perda de pacotes:\n\n")
        md.append("| Data | Horário | Latência (ms) | Perda (%) |\n")
        md.append("|------|---------|---------------|----------|\n")

        for d in stats_geral['lista_testes_com_perda'][:20]:
            data_fmt = d['datetime'].strftime("%d/%m")
            md.append(f"| {data_fmt} | {d['hora']} | {d['ping_aghuse']['media']} | {d['ping_aghuse']['perda']} |\n")

        if len(stats_geral['lista_testes_com_perda']) > 20:
            md.append(f"\n*Exibindo 20 de {len(stats_geral['lista_testes_com_perda'])} incidentes. Consulte relatórios diários para detalhes completos.*\n")
        md.append("\n")

    # Análise e Conclusão
    md.append("## Análise e Conclusão\n\n")

    if stats_geral['disponibilidade'] >= 99.9:
        md.append(f"**Disponibilidade**: {stats_geral['disponibilidade']:.2f}% - Excelente. Sistema operando conforme SLA.\n\n")
    elif stats_geral['disponibilidade'] >= 99.0:
        md.append(f"**Disponibilidade**: {stats_geral['disponibilidade']:.2f}% - Boa. Sistema operacional dentro dos parâmetros.\n\n")
    elif stats_geral['disponibilidade'] >= 95.0:
        md.append(f"**Disponibilidade**: {stats_geral['disponibilidade']:.2f}% - Aceitável. Requer monitoramento contínuo.\n\n")
    else:
        md.append(f"**Disponibilidade**: {stats_geral['disponibilidade']:.2f}% - Crítica. Requer ação corretiva imediata.\n\n")

    if stats_geral['aghuse_media'] < 20:
        md.append(f"**Latência**: Média de {stats_geral['aghuse_media']:.1f}ms - Performance adequada.\n\n")
    else:
        md.append(f"**Latência**: Média de {stats_geral['aghuse_media']:.1f}ms - Monitorar tendências.\n\n")

    return ''.join(md)

def gerar_relatorio_geral(dados_por_dia):
    """Gera relatório geral de todo o período"""
    md = []

    # Validar se há dados
    if not dados_por_dia:
        md.append("# Relatório Geral - Monitoramento AGHUSE\n\n")
        md.append("**Aviso**: Nenhum dado disponível para gerar o relatório.\n")
        return ''.join(md)

    dias_ordenados = sorted(dados_por_dia.keys())
    primeira_data = dias_ordenados[0].strftime("%d/%m/%Y")
    ultima_data = dias_ordenados[-1].strftime("%d/%m/%Y")
    total_dias = len(dias_ordenados)

    md.append(f"# Relatório Geral - Monitoramento AGHUSE\n")
    md.append(f"**Período**: {primeira_data} a {ultima_data} ({total_dias} dias)\n\n")

    # Estatísticas gerais
    todos_dados = []
    for dados_dia in dados_por_dia.values():
        todos_dados.extend(dados_dia)

    stats_geral = calcular_estatisticas_geral(todos_dados)

    # Sumário Executivo
    md.append("## Sumário Executivo\n\n")
    md.append("| Métrica | Valor |\n")
    md.append("|---------|-------|\n")
    md.append(f"| Total de Testes Executados | {stats_geral['total_testes']} |\n")
    md.append(f"| Média de Testes por Dia | {stats_geral['total_testes'] / total_dias:.0f} |\n")
    md.append(f"| Testes sem Perda | {stats_geral['testes_sem_perda']} |\n")
    md.append(f"| Testes com Perda | {stats_geral['testes_com_perda']} |\n")
    md.append(f"| Total de Pacotes Enviados | {stats_geral['total_pacotes_enviados']} |\n")
    md.append(f"| Total de Pacotes Perdidos | {stats_geral['total_pacotes_perdidos']} |\n")
    md.append(f"| **Disponibilidade** | **{stats_geral['disponibilidade']:.2f}%** |\n\n")

    # Métricas de Latência
    md.append("## Métricas de Latência\n\n")
    md.append("| Destino | Latência Média (ms) | Mínima (ms) | Máxima (ms) |\n")
    md.append("|---------|---------------------|-------------|-------------|\n")
    md.append(f"| AGHUSE (10.252.17.132) | {stats_geral['aghuse_media']:.1f} | {stats_geral['aghuse_min']} | {stats_geral['aghuse_max']} |\n")
    md.append(f"| IP Interno (10.252.17.132) | {stats_geral['interno_media']:.1f} | - | - |\n")
    md.append(f"| Google DNS (8.8.8.8) | {stats_geral['externo_media']:.1f} | - | - |\n\n")

    # Análise por Dia
    md.append("## Análise por Dia\n\n")
    md.append("| Data | Testes | Sem Perda / Com Perda | Pacotes Perdidos | Disponibilidade | Latência Média |\n")
    md.append("|------|--------|-----------------------|------------------|-----------------|----------------|\n")

    for dia in dias_ordenados:
        dados_dia = dados_por_dia[dia]
        stats = calcular_estatisticas_dia(dados_dia)
        data_fmt = dia.strftime("%d/%m/%Y")

        md.append(f"| {data_fmt} | {stats['total_testes']} | {stats['testes_sem_perda']} / {stats['testes_com_perda']} | {stats['total_pacotes_perdidos']} | {stats['disponibilidade']:.2f}% | {stats['aghuse_media']:.1f}ms |\n")

    # Análise de Horários Críticos
    horarios_problemas, horarios_latencia = analisar_horarios_problematicos(dados_por_dia)

    if horarios_problemas:
        md.append("\n## Análise de Horários Críticos\n\n")
        md.append("### Distribuição de Perda de Pacotes por Horário\n\n")
        md.append("| Faixa Horária | Ocorrências | Porcentagem do Total |\n")
        md.append("|---------------|-------------|---------------------|\n")

        for hora in sorted(horarios_problemas.keys(), key=lambda h: horarios_problemas[h], reverse=True):
            count = horarios_problemas[hora]
            percent = (count / stats_geral['testes_com_perda']) * 100
            md.append(f"| {hora:02d}:00 - {hora:02d}:59 | {count} | {percent:.1f}% |\n")
        md.append("\n")

        # Identificar padrão
        horas_pico = [h for h, c in horarios_problemas.items() if c >= max(horarios_problemas.values()) * 0.5]
        if horas_pico:
            md.append(f"**Padrão Identificado**: Concentração de problemas entre {min(horas_pico):02d}:00 e {max(horas_pico):02d}:59\n\n")

    if horarios_latencia:
        md.append("### Distribuição de Latência Elevada por Horário\n\n")
        md.append("| Faixa Horária | Ocorrências |\n")
        md.append("|---------------|-------------|\n")

        for hora in sorted(horarios_latencia.keys(), key=lambda h: horarios_latencia[h], reverse=True)[:10]:
            count = horarios_latencia[hora]
            md.append(f"| {hora:02d}:00 - {hora:02d}:59 | {count} |\n")
        md.append("\n")

    # Registro de Incidentes
    if stats_geral['testes_com_perda'] > 0:
        md.append("## Registro de Incidentes\n\n")
        md.append(f"Total de {stats_geral['testes_com_perda']} teste(s) com perda de pacotes:\n\n")
        md.append("| Data | Horário | Latência (ms) | Perda (%) | Min/Max (ms) |\n")
        md.append("|------|---------|---------------|-----------|-------------|\n")

        for d in stats_geral['lista_testes_com_perda'][:30]:
            data_fmt = d['datetime'].strftime("%d/%m")
            md.append(f"| {data_fmt} | {d['hora']} | {d['ping_aghuse']['media']} | {d['ping_aghuse']['perda']} | {d['ping_aghuse']['min']}/{d['ping_aghuse']['max']} |\n")

        if len(stats_geral['lista_testes_com_perda']) > 30:
            md.append(f"\n*Exibindo 30 de {len(stats_geral['lista_testes_com_perda'])} incidentes. Consulte relatórios diários para informações completas.*\n")
        md.append("\n")

    # Análise e Conclusão
    md.append("## Análise e Conclusão\n\n")

    if stats_geral['disponibilidade'] >= 99.9:
        md.append(f"**Disponibilidade**: {stats_geral['disponibilidade']:.2f}% - Excelente. Sistema operando conforme SLA.\n")
        md.append("- Manter monitoramento contínuo\n\n")
    elif stats_geral['disponibilidade'] >= 99.0:
        md.append(f"**Disponibilidade**: {stats_geral['disponibilidade']:.2f}% - Boa. Sistema operando dentro dos parâmetros.\n")
        md.append("- Acompanhar tendências\n\n")
    elif stats_geral['disponibilidade'] >= 95.0:
        md.append(f"**Disponibilidade**: {stats_geral['disponibilidade']:.2f}% - Aceitável. Sistema apresenta instabilidades.\n")
        md.append("- Recomenda-se análise dos horários críticos\n")
        md.append("- Implementar monitoramento mais granular\n\n")
    else:
        md.append(f"**Disponibilidade**: {stats_geral['disponibilidade']:.2f}% - Crítica. Sistema apresenta problemas significativos.\n")
        md.append("- Requer ação corretiva imediata\n")
        md.append("- Revisar infraestrutura de rede\n")
        md.append("- Analisar logs e traceroutes dos horários críticos\n\n")

    if stats_geral['aghuse_media'] < 10:
        md.append(f"**Latência**: Média de {stats_geral['aghuse_media']:.1f}ms - Excelente performance de rede.\n\n")
    elif stats_geral['aghuse_media'] < 20:
        md.append(f"**Latência**: Média de {stats_geral['aghuse_media']:.1f}ms - Performance adequada.\n\n")
    elif stats_geral['aghuse_media'] < 50:
        md.append(f"**Latência**: Média de {stats_geral['aghuse_media']:.1f}ms - Performance aceitável. Monitorar tendências.\n\n")
    else:
        md.append(f"**Latência**: Média de {stats_geral['aghuse_media']:.1f}ms - Performance degradada. Investigação necessária.\n\n")

    if stats_geral['latencia_alta_count'] > 0:
        percent_alta = (stats_geral['latencia_alta_count'] / stats_geral['total_testes']) * 100
        md.append(f"**Obs**: {stats_geral['latencia_alta_count']} testes ({percent_alta:.1f}%) apresentaram latência superior a 20ms.\n\n")

    md.append("---\n")
    md.append(f"*Relatório gerado automaticamente a partir de {stats_geral['total_testes']} testes realizados em {total_dias} dias*\n")

    return ''.join(md)

def main():
    pasta_arquivos = 'arquivos'
    pasta_relatorios = 'relatorios'

    # Criar pasta de relatórios se não existir
    if not os.path.exists(pasta_relatorios):
        os.makedirs(pasta_relatorios)
        print(f"Pasta '{pasta_relatorios}' criada")

    print("Processando arquivos de teste...")
    dados = processar_todos_arquivos(pasta_arquivos)
    print(f"Total de arquivos processados: {len(dados)}")

    print("Agrupando dados por dia...")
    dados_por_dia = agrupar_por_dia(dados)
    print(f"Total de dias com dados: {len(dados_por_dia)}")

    # Gerar relatórios diários
    print("\nGerando relatórios diários...")
    for dia, dados_dia in sorted(dados_por_dia.items()):
        stats = calcular_estatisticas_dia(dados_dia)
        relatorio = gerar_relatorio_diario(dia, dados_dia, stats)

        nome_arquivo = f"RELATORIO_DIARIO_{dia.strftime('%Y-%m-%d')}.md"
        caminho_arquivo = os.path.join(pasta_relatorios, nome_arquivo)

        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(relatorio)

        print(f"  [OK] {nome_arquivo}")

    # Gerar relatório semanal
    print("\nGerando relatorio semanal...")
    relatorio_semanal = gerar_relatorio_semanal(dados_por_dia)
    caminho_semanal = os.path.join(pasta_relatorios, 'RELATORIO_SEMANAL.md')
    with open(caminho_semanal, 'w', encoding='utf-8') as f:
        f.write(relatorio_semanal)
    print(f"  [OK] RELATORIO_SEMANAL.md")

    # Gerar relatório geral
    print("\nGerando relatorio geral...")
    relatorio_geral = gerar_relatorio_geral(dados_por_dia)
    caminho_geral = os.path.join(pasta_relatorios, 'RELATORIO_GERAL.md')
    with open(caminho_geral, 'w', encoding='utf-8') as f:
        f.write(relatorio_geral)
    print(f"  [OK] RELATORIO_GERAL.md")

    print(f"\nProcesso concluido!")
    print(f"\nRelatorios gerados na pasta '{pasta_relatorios}':")
    print(f"  - {len(dados_por_dia)} relatorios diarios")
    print(f"  - 1 relatorio semanal")
    print(f"  - 1 relatorio geral")

if __name__ == '__main__':
    main()
