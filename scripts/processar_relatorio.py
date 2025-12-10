import os
import re
from datetime import datetime, timedelta
from collections import defaultdict

# ============================================================================
# CONFIGURAÇÕES DE ANÁLISE AVANÇADA
# ============================================================================

# Baseline Ideal de Latência
LATENCIA_IDEAL = 15      # ms - valor de referência ideal
LATENCIA_BOA = 30        # ms - aceitável
LATENCIA_REGULAR = 50    # ms - atenção
# > 50ms = Ruim

# Detecção de Horários de Pico
THRESHOLD_PICO = 1.10    # 10% acima da média geral = pico
MIN_DURACAO_PICO = 2     # Mínimo 2 horas consecutivas para ser considerado pico

# Detecção de Anomalias
DESVIO_ANOMALIA = 2.5    # 2.5 desvios padrão = anomalia
PERCENTUAL_ANOMALIA = 200  # 200% acima do horário = anomalia

# ============================================================================

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

    # Contar saltos do tracert e extrair rotas
    tracert_section = re.search(r'\[4/7\] TRACERT.*?Rastreamento conclu.do', conteudo, re.DOTALL)
    if tracert_section:
        saltos = len(re.findall(r'^\s*\d+\s+', tracert_section.group(0), re.MULTILINE))
        dados['tracert_saltos'] = saltos

        # Extrair rotas completas do tracert
        dados['tracert_rota'] = extrair_rotas_tracert(tracert_section.group(0))

    return dados

def extrair_rotas_tracert(tracert_text):
    """
    Extrai a rota completa do tracert (sequência de IPs)

    Args:
        tracert_text: texto da seção do tracert

    Returns:
        tuple: (rota_hash, lista_ips) onde rota_hash é uma string única identificadora da rota
    """
    ips = []

    # Extrair IPs de cada salto (formato: "  1    <1 ms    <1 ms    <1 ms  10.17.201.254")
    linhas = re.findall(r'^\s*\d+\s+.*?\s+([\d\.]+)\s*$', tracert_text, re.MULTILINE)

    for ip in linhas:
        ips.append(ip)

    # Criar hash da rota (sequência de IPs separados por ->)
    rota_hash = ' -> '.join(ips) if ips else None

    return {'hash': rota_hash, 'ips': ips, 'num_saltos': len(ips)}

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

def analisar_latencia_por_horario(dados_lista):
    """Analisa latência média por faixa horária - AGHUSE e Rede Externa"""
    latencia_aghuse_por_hora = defaultdict(list)
    latencia_externo_por_hora = defaultdict(list)
    perda_aghuse_por_hora = defaultdict(list)
    perda_externo_por_hora = defaultdict(list)

    for d in dados_lista:
        hora_int = int(d['hora'].split(':')[0])

        # Coletar latência AGHUSE (10.252.17.132)
        if d['ping_interno']['media']:
            latencia_aghuse_por_hora[hora_int].append(d['ping_interno']['media'])

        # Coletar latência Rede Externa (8.8.8.8)
        if d['ping_externo']['media']:
            latencia_externo_por_hora[hora_int].append(d['ping_externo']['media'])

        # Coletar perdas AGHUSE
        if d['ping_interno']['perda'] is not None:
            perda_aghuse_por_hora[hora_int].append(d['ping_interno']['perda'])

        # Coletar perdas Rede Externa
        if d['ping_externo']['perda'] is not None:
            perda_externo_por_hora[hora_int].append(d['ping_externo']['perda'])

    # Calcular estatísticas por hora
    stats_por_hora = {}
    for hora in latencia_aghuse_por_hora.keys():
        latencias_aghuse = latencia_aghuse_por_hora[hora]
        latencias_externo = latencia_externo_por_hora.get(hora, [])
        perdas_aghuse = perda_aghuse_por_hora.get(hora, [])
        perdas_externo = perda_externo_por_hora.get(hora, [])

        testes_com_perda_aghuse = sum(1 for p in perdas_aghuse if p > 0)
        testes_com_perda_externo = sum(1 for p in perdas_externo if p > 0)

        # Calcular total de pacotes perdidos (cada teste envia 20 pacotes)
        perda_percentual_total_aghuse = sum(perdas_aghuse)
        perda_percentual_total_externo = sum(perdas_externo) if perdas_externo else 0

        # Converter porcentagem em número de pacotes
        # Se temos N testes com perda total de X%, então perdemos (X/100) * 20 pacotes por teste em média
        pacotes_perdidos_aghuse = int((perda_percentual_total_aghuse / 100) * 20) if perdas_aghuse else 0
        pacotes_perdidos_externo = int((perda_percentual_total_externo / 100) * 20) if perdas_externo else 0

        stats_por_hora[hora] = {
            'media': sum(latencias_aghuse) / len(latencias_aghuse),
            'min': min(latencias_aghuse),
            'max': max(latencias_aghuse),
            'testes': len(latencias_aghuse),
            'total_testes': len(latencias_aghuse),
            'testes_com_perda': testes_com_perda_aghuse,
            'perda_total': sum(perdas_aghuse),
            'pacotes_perdidos': pacotes_perdidos_aghuse,
            # Dados da rede externa
            'media_externo': sum(latencias_externo) / len(latencias_externo) if latencias_externo else 0,
            'min_externo': min(latencias_externo) if latencias_externo else 0,
            'max_externo': max(latencias_externo) if latencias_externo else 0,
            'testes_com_perda_externo': testes_com_perda_externo,
            'perda_total_externo': sum(perdas_externo) if perdas_externo else 0,
            'pacotes_perdidos_externo': pacotes_perdidos_externo
        }

    return stats_por_hora

def gerar_grafico_barras_ascii(valores, largura_max=40):
    """Gera gráfico de barras ASCII"""
    if not valores:
        return []

    max_valor = max(v for v in valores.values() if v is not None)
    if max_valor == 0:
        max_valor = 1

    linhas = []
    for hora in sorted(valores.keys()):
        valor = valores[hora]
        if valor is None:
            continue

        barra_tamanho = int((valor / max_valor) * largura_max)
        barra = '█' * barra_tamanho
        linhas.append(f"{hora:02d}h │{barra} {valor:.1f}ms")

    return linhas

def classificar_faixa_horaria(stats):
    """Classifica uma faixa horária com base em múltiplos critérios"""
    latencia = stats['media']
    perda = stats['testes_com_perda']

    # Pontuação baseada em latência
    if latencia < 10:
        score_latencia = 4
    elif latencia < 20:
        score_latencia = 3
    elif latencia < 50:
        score_latencia = 2
    else:
        score_latencia = 1

    # Pontuação baseada em perda
    if perda == 0:
        score_perda = 4
    elif perda <= 2:
        score_perda = 3
    elif perda <= 5:
        score_perda = 2
    else:
        score_perda = 1

    # Score final (média ponderada: latência 60%, perda 40%)
    score_final = (score_latencia * 0.6) + (score_perda * 0.4)

    if score_final >= 3.5:
        return "Ótimo", "excelente"
    elif score_final >= 2.5:
        return "Bom", "boa"
    elif score_final >= 1.5:
        return "Regular", "regular"
    else:
        return "Ruim", "ruim"

# ============================================
# FUNÇÕES AUXILIARES REUTILIZÁVEIS
# ============================================

def gerar_analise_disponibilidade(disponibilidade):
    """Gera análise de disponibilidade reutilizável para todos os relatórios"""
    if disponibilidade >= 99.9:
        return f"**Conexão**: {disponibilidade:.2f}% - Ótima\n\n"
    elif disponibilidade >= 99.0:
        return f"**Conexão**: {disponibilidade:.2f}% - Boa\n\n"
    elif disponibilidade >= 95.0:
        return f"**Conexão**: {disponibilidade:.2f}% - Regular\n\n"
    else:
        return f"**Conexão**: {disponibilidade:.2f}% - Ruim\n\n"

def gerar_analise_qualidade_horaria(stats_latencia_hora, titulo="**Resumo por Horário**"):
    """Gera análise de qualidade por faixa horária reutilizável"""
    if not stats_latencia_hora:
        return ""

    md = []
    contagem_categorias = {"excelente": [], "boa": [], "regular": [], "ruim": []}

    for hora, s in stats_latencia_hora.items():
        _, categoria = classificar_faixa_horaria(s)
        contagem_categorias[categoria].append(hora)

    total_faixas = len(stats_latencia_hora)

    # Mostrar apenas resumo compacto
    md.append(f"{titulo}: ")

    partes = []
    if contagem_categorias['excelente']:
        partes.append(f"{len(contagem_categorias['excelente'])}/{total_faixas} ótimo")
    if contagem_categorias['boa']:
        partes.append(f"{len(contagem_categorias['boa'])}/{total_faixas} bom")
    if contagem_categorias['regular']:
        partes.append(f"{len(contagem_categorias['regular'])}/{total_faixas} regular")
    if contagem_categorias['ruim']:
        partes.append(f"{len(contagem_categorias['ruim'])}/{total_faixas} ruim")

    md.append(" | ".join(partes))
    md.append("\n\n")

    return ''.join(md)

def gerar_tabela_latencia_horaria(stats_latencia_hora, incluir_grafico=True):
    """Gera tabela de latência por faixa horária com comparativo AGHUSE vs Rede Externa"""
    if not stats_latencia_hora:
        return "*Nenhum dado disponível.*\n\n"

    md = []

    # Tabela com comparativo AGHUSE vs Rede Externa
    md.append("| Horário | AGHUSE (ms) | Rede Externa (ms) | Status |\n")
    md.append("|---------|-------------|-------------------|--------|\n")

    for hora in sorted(stats_latencia_hora.keys()):
        s = stats_latencia_hora[hora]
        classificacao, _ = classificar_faixa_horaria(s)

        # Adicionar alertas de perda para AGHUSE e Rede Externa
        alertas = []
        if s['testes_com_perda'] > 0:
            alertas.append(f"AG:{s.get('pacotes_perdidos', 0)}pkt")
        if s.get('testes_com_perda_externo', 0) > 0:
            alertas.append(f"EX:{s.get('pacotes_perdidos_externo', 0)}pkt")

        alerta = f" [{', '.join(alertas)}]" if alertas else ""

        # Formatar dados AGHUSE e Rede Externa
        aghuse_str = f"{s['media']:.1f} ({s['min']}-{s['max']})"
        externo_str = f"{s['media_externo']:.1f} ({s['min_externo']}-{s['max_externo']})" if s.get('media_externo', 0) > 0 else "N/A"

        md.append(f"| {hora:02d}h | {aghuse_str} | {externo_str} | {classificacao}{alerta} |\n")

    md.append("\n")

    if incluir_grafico:
        md.append("**Gráfico Comparativo de Latência:**\n\n")
        md.append("```\n")
        md.append("AGHUSE vs Rede Externa\n")
        for hora in sorted(stats_latencia_hora.keys()):
            s = stats_latencia_hora[hora]
            # Escala para visualização
            max_val = max(s['media'], s.get('media_externo', 0))
            if max_val > 0:
                barra_aghuse = '█' * int((s['media'] / max_val) * 30)
                barra_externo = '█' * int((s.get('media_externo', 0) / max_val) * 30) if s.get('media_externo', 0) > 0 else ''
                md.append(f"{hora:02d}h │AG: {barra_aghuse} {s['media']:.1f}ms\n")
                md.append(f"     │EX: {barra_externo} {s.get('media_externo', 0):.1f}ms\n")
        md.append("```\n\n")

    return ''.join(md)

# ============================================
# FUNÇÕES DE MÉTRICAS AVANÇADAS
# ============================================

def calcular_jitter_e_estabilidade(dados_lista):
    """Calcula jitter (variação de latência) e métricas de estabilidade"""
    import statistics

    if not dados_lista or len(dados_lista) < 2:
        return None

    # Extrair latências válidas
    latencias = [d['ping_aghuse']['media'] for d in dados_lista if d['ping_aghuse']['media'] > 0]

    if len(latencias) < 2:
        return None

    # Calcular jitter (variação entre medições consecutivas)
    jitters = [abs(latencias[i] - latencias[i-1]) for i in range(1, len(latencias))]
    jitter_medio = statistics.mean(jitters) if jitters else 0

    # Calcular desvio padrão e coeficiente de variação
    media_latencia = statistics.mean(latencias)
    desvio_padrao = statistics.stdev(latencias) if len(latencias) > 1 else 0
    coef_variacao = (desvio_padrao / media_latencia * 100) if media_latencia > 0 else 0

    # Score de estabilidade (0-10, onde 10 é mais estável)
    # Baseado em jitter e coeficiente de variação
    if jitter_medio < 2 and coef_variacao < 10:
        score_estabilidade = 10
    elif jitter_medio < 5 and coef_variacao < 20:
        score_estabilidade = 8
    elif jitter_medio < 10 and coef_variacao < 30:
        score_estabilidade = 6
    elif jitter_medio < 15 and coef_variacao < 40:
        score_estabilidade = 4
    else:
        score_estabilidade = 2

    return {
        'jitter_medio': round(jitter_medio, 2),
        'jitter_min': min(jitters) if jitters else 0,
        'jitter_max': max(jitters) if jitters else 0,
        'desvio_padrao': round(desvio_padrao, 2),
        'coef_variacao': round(coef_variacao, 2),
        'score_estabilidade': score_estabilidade,
        'classificacao': 'Excelente' if score_estabilidade >= 8 else 'Boa' if score_estabilidade >= 6 else 'Regular' if score_estabilidade >= 4 else 'Ruim'
    }

def calcular_percentis_sla(latencias):
    """Calcula percentis de latência para compliance SLA"""
    import statistics

    if not latencias:
        return None

    latencias_ordenadas = sorted(latencias)
    n = len(latencias_ordenadas)

    def percentil(p):
        """Calcula o percentil p (0-100)"""
        if n == 0:
            return 0
        k = (n - 1) * p / 100
        f = int(k)
        c = k - f
        if f + 1 < n:
            return latencias_ordenadas[f] + c * (latencias_ordenadas[f + 1] - latencias_ordenadas[f])
        return latencias_ordenadas[f]

    return {
        'p50': round(percentil(50), 1),   # Mediana
        'p95': round(percentil(95), 1),   # SLA comum
        'p99': round(percentil(99), 1),   # SLA rigoroso
        'p99_9': round(percentil(99.9), 1)  # SLA muito rigoroso
    }

# ============================================
# FUNÇÕES DE VISUALIZAÇÃO AVANÇADAS
# ============================================

def gerar_gauge_sla(disponibilidade, target=99.5):
    """Gera visualização gauge de SLA em ASCII"""
    md = []
    md.append("```\n")
    md.append("═══════════════════════════════════════\n")
    md.append("    DISPONIBILIDADE vs SLA TARGET\n")
    md.append("═══════════════════════════════════════\n\n")
    md.append(f"Target: {target}%    Atual: {disponibilidade:.2f}%\n\n")

    # Criar barra de progresso
    largura_total = 30
    posicao_atual = int((disponibilidade / 100) * largura_total)
    posicao_target = int((target / 100) * largura_total)

    barra = ""
    for i in range(largura_total):
        if i < posicao_atual:
            barra += "█"
        elif i == posicao_atual:
            barra += "▓"
        else:
            barra += "░"

    md.append(f"   |{barra}| {disponibilidade:.2f}%\n")
    md.append("   0%        50%      99.5%    100%\n")
    md.append(" " * (posicao_target + 3) + "↑\n")
    md.append(" " * (posicao_target + 1) + "Target\n\n")

    # Status
    diferenca = disponibilidade - target
    if diferenca >= 0:
        md.append(f"Status: ✅ ACIMA DO SLA (+{diferenca:.2f}%)\n")
    else:
        md.append(f"Status: ❌ ABAIXO DO SLA ({diferenca:.2f}%)\n")

    md.append("```\n\n")
    return ''.join(md)

def gerar_sparkline(valores, largura=30):
    """Gera sparkline (mini gráfico inline) para tendências"""
    if not valores or len(valores) < 2:
        return "─" * largura

    # Normalizar valores para 0-7 (8 níveis de blocos)
    min_val = min(valores)
    max_val = max(valores)
    range_val = max_val - min_val if max_val > min_val else 1

    blocos = " ▁▂▃▄▅▆▇█"

    sparkline = ""
    for v in valores:
        nivel = int(((v - min_val) / range_val) * 7)
        sparkline += blocos[nivel + 1]

    # Ajustar ao tamanho desejado
    if len(sparkline) > largura:
        # Amostrar valores uniformemente
        step = len(valores) / largura
        sparkline = "".join([blocos[int(((valores[int(i * step)] - min_val) / range_val) * 7) + 1] for i in range(largura)])
    elif len(sparkline) < largura:
        # Preencher com espaços
        sparkline += " " * (largura - len(sparkline))

    return sparkline

def analisar_comparacao_endpoints(dados_lista):
    """Compara AGHUSE vs Interno vs Externo para identificar origem do problema"""
    if not dados_lista:
        return None

    # Coletar latências de cada endpoint
    latencias_aghuse = [d['ping_aghuse']['media'] for d in dados_lista if d['ping_aghuse']['media'] is not None and d['ping_aghuse']['media'] > 0]
    latencias_interno = [d['ping_interno']['media'] for d in dados_lista if d['ping_interno']['media'] is not None and d['ping_interno']['media'] > 0]
    latencias_externo = [d['ping_externo']['media'] for d in dados_lista if d['ping_externo']['media'] is not None and d['ping_externo']['media'] > 0]

    if not (latencias_aghuse and latencias_interno and latencias_externo):
        return None

    import statistics

    # Calcular médias
    media_aghuse = statistics.mean(latencias_aghuse)
    media_interno = statistics.mean(latencias_interno)
    media_externo = statistics.mean(latencias_externo)

    # Calcular diferenças percentuais
    diff_aghuse_interno = ((media_aghuse - media_interno) / media_interno * 100) if media_interno > 0 else 0
    diff_aghuse_externo = ((media_aghuse - media_externo) / media_externo * 100) if media_externo > 0 else 0
    diff_interno_externo = ((media_interno - media_externo) / media_externo * 100) if media_externo > 0 else 0

    # Diagnosticar causa provável
    diagnostico = "Normal"
    if media_aghuse > media_externo * 1.5:  # AGHUSE 50% mais lento que externo
        diagnostico = "AGHUSE"
    elif media_interno > media_externo * 1.3:  # Rede interna 30% mais lenta
        diagnostico = "Rede Interna"
    elif media_externo > 50:  # Internet muito lenta
        diagnostico = "ISP/Internet"

    return {
        'media_aghuse': round(media_aghuse, 1),
        'media_interno': round(media_interno, 1),
        'media_externo': round(media_externo, 1),
        'diff_aghuse_interno': round(diff_aghuse_interno, 1),
        'diff_aghuse_externo': round(diff_aghuse_externo, 1),
        'diff_interno_externo': round(diff_interno_externo, 1),
        'diagnostico': diagnostico
    }

def gerar_comparacao_3_endpoints(comparacao):
    """Gera visualização de comparação entre 3 endpoints"""
    if not comparacao:
        return ""

    md = []
    md.append("### Comparação Multi-Endpoint (Diagnóstico de Causa)\n\n")
    md.append("```\n")
    md.append("Latência Média por Destino\n\n")

    # Encontrar valor máximo para escalar as barras
    max_val = max(comparacao['media_aghuse'], comparacao['media_interno'], comparacao['media_externo'])
    largura_max = 30

    def gerar_barra(valor, max_valor, largura):
        tamanho = int((valor / max_valor) * largura) if max_valor > 0 else 0
        return "█" * tamanho + "░" * (largura - tamanho)

    md.append(f"AGHUSE     {gerar_barra(comparacao['media_aghuse'], max_val, largura_max)} {comparacao['media_aghuse']}ms\n")
    md.append(f"Interno    {gerar_barra(comparacao['media_interno'], max_val, largura_max)} {comparacao['media_interno']}ms\n")
    md.append(f"Externo    {gerar_barra(comparacao['media_externo'], max_val, largura_max)} {comparacao['media_externo']}ms\n\n")

    # Diagnóstico
    if comparacao['diagnostico'] == "AGHUSE":
        md.append(f"Diagnóstico: ⚠️ AGHUSE +{abs(comparacao['diff_aghuse_externo']):.0f}% acima do externo → Problema no servidor\n")
    elif comparacao['diagnostico'] == "Rede Interna":
        md.append(f"Diagnóstico: ⚠️ Rede interna +{abs(comparacao['diff_interno_externo']):.0f}% acima do externo → Problema na rede local\n")
    elif comparacao['diagnostico'] == "ISP/Internet":
        md.append(f"Diagnóstico: ⚠️ Latência externa elevada ({comparacao['media_externo']}ms) → Problema no ISP/Internet\n")
    else:
        md.append("Diagnóstico: ✅ Todos os endpoints com latência normal\n")

    md.append("```\n\n")
    return ''.join(md)


# ============================================================================
# FUNÇÕES DE ANÁLISE AVANÇADA
# ============================================================================

def calcular_regressao_linear(dados_lista, usar_externo=False):
    """
    Calcula regressão linear y = ax + b para tendências de latência

    Args:
        dados_lista: Lista de dicionários com dados de testes contendo 'datetime' e 'ping_interno'/'ping_externo'
        usar_externo: Se True, usa ping_externo (8.8.8.8), senão usa ping_interno (10.252.17.132)

    Returns:
        dict: {'slope', 'intercept', 'r_squared', 'previsao_7d', 'tendencia'}
    """
    if not dados_lista or len(dados_lista) < 2:
        return {
            'slope': 0,
            'intercept': 0,
            'r_squared': 0,
            'previsao_7d': 0,
            'tendencia': 'indisponível'
        }

    # Filtrar dados válidos - usar ping_interno (AGHUSE) ou ping_externo
    campo_ping = 'ping_externo' if usar_externo else 'ping_interno'
    dados_validos = [(d['datetime'], d[campo_ping]['media'])
                     for d in dados_lista
                     if d.get('datetime') and d.get(campo_ping, {}).get('media') is not None]

    if len(dados_validos) < 2:
        return {
            'slope': 0,
            'intercept': 0,
            'r_squared': 0,
            'previsao_7d': 0,
            'tendencia': 'dados insuficientes'
        }

    # Converter timestamps para dias numéricos (desde o primeiro dado)
    tempo_inicial = dados_validos[0][0]
    x = []
    y = []

    for timestamp, latencia in dados_validos:
        dias = (timestamp - tempo_inicial).days + (timestamp - tempo_inicial).seconds / 86400.0
        x.append(dias)
        y.append(latencia)

    # Calcular regressão linear: y = slope * x + intercept
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi ** 2 for xi in x)

    # Evitar divisão por zero
    denominador = (n * sum_x2 - sum_x ** 2)
    if denominador == 0:
        return {
            'slope': 0,
            'intercept': sum_y / n if n > 0 else 0,
            'r_squared': 0,
            'previsao_7d': sum_y / n if n > 0 else 0,
            'tendencia': 'estável'
        }

    slope = (n * sum_xy - sum_x * sum_y) / denominador
    intercept = (sum_y - slope * sum_x) / n

    # Calcular R² (coeficiente de determinação)
    y_mean = sum_y / n
    ss_tot = sum((yi - y_mean) ** 2 for yi in y)
    ss_res = sum((yi - (slope * xi + intercept)) ** 2 for xi, yi in zip(x, y))
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    # Previsão para próximos 7 dias
    ultimo_x = x[-1]
    previsao_7d = slope * (ultimo_x + 7) + intercept

    # Classificar tendência
    if slope > 0.5:
        tendencia = 'alta'
    elif slope < -0.5:
        tendencia = 'queda'
    else:
        tendencia = 'estável'

    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'previsao_7d': max(0, previsao_7d),  # Latência não pode ser negativa
        'tendencia': tendencia
    }


def detectar_horarios_pico(latencia_por_hora, threshold=None, min_duracao=None):
    """
    Identifica períodos de pico baseado em threshold

    Args:
        latencia_por_hora: dict {hora: {'media': float, ...}}
        threshold: float, percentual acima da média para ser considerado pico (ex: 1.15 = 15%)
        min_duracao: int, mínimo de horas consecutivas

    Returns:
        list: [{'nome', 'inicio', 'fim', 'latencia_media', 'diferenca_media'}]
    """
    if threshold is None:
        threshold = THRESHOLD_PICO
    if min_duracao is None:
        min_duracao = MIN_DURACAO_PICO

    if not latencia_por_hora:
        return []

    # Calcular média geral
    latencias = [h['media'] for h in latencia_por_hora.values() if h.get('media') is not None]
    if not latencias:
        return []

    media_geral = sum(latencias) / len(latencias)

    picos = []
    periodo_atual = None

    for hora in sorted(latencia_por_hora.keys()):
        lat = latencia_por_hora[hora].get('media')
        if lat is None:
            continue

        is_pico = lat >= media_geral * threshold

        if is_pico:
            if periodo_atual is None:
                # Inicia novo período de pico
                periodo_atual = {
                    'inicio': hora,
                    'fim': hora,
                    'latencia_soma': lat,
                    'count': 1
                }
            else:
                # Estende período atual
                periodo_atual['fim'] = hora
                periodo_atual['latencia_soma'] += lat
                periodo_atual['count'] += 1
        else:
            # Finaliza período se existir e atende mínimo
            if periodo_atual and periodo_atual['count'] >= min_duracao:
                periodo_atual['latencia_media'] = periodo_atual['latencia_soma'] / periodo_atual['count']
                periodo_atual['diferenca_media'] = periodo_atual['latencia_media'] - media_geral
                del periodo_atual['latencia_soma']  # Remove dados temporários
                picos.append(periodo_atual)
            periodo_atual = None

    # Finalizar último período se existir
    if periodo_atual and periodo_atual['count'] >= min_duracao:
        periodo_atual['latencia_media'] = periodo_atual['latencia_soma'] / periodo_atual['count']
        periodo_atual['diferenca_media'] = periodo_atual['latencia_media'] - media_geral
        del periodo_atual['latencia_soma']
        picos.append(periodo_atual)

    # Classificar e nomear picos
    for pico in picos:
        if 8 <= pico['inicio'] <= 12:
            pico['nome'] = 'Pico Matinal'
        elif 14 <= pico['inicio'] <= 18:
            pico['nome'] = 'Pico Vespertino'
        elif 20 <= pico['inicio'] or pico['fim'] <= 6:
            pico['nome'] = 'Pico Noturno'
        else:
            pico['nome'] = f"Pico {pico['inicio']:02d}h-{pico['fim']:02d}h"

    return picos


def calcular_score_qualidade_horario(latencia, perda_percentual, baseline=None):
    """
    Calcula score 0-10 baseado em latência e perda de pacotes

    Args:
        latencia: float, latência média em ms
        perda_percentual: float, percentual de perda (0-100)
        baseline: float, latência ideal de referência

    Returns:
        dict: {'score', 'classificacao', 'componente_latencia', 'componente_perda'}
    """
    if baseline is None:
        baseline = LATENCIA_IDEAL

    # Score de latência (0-6 pontos, 60% do total)
    if latencia <= baseline:
        score_lat = 6.0
    elif latencia <= baseline * 2:
        # Linear de 6.0 a 3.0
        score_lat = 6.0 - ((latencia - baseline) / baseline) * 3.0
    elif latencia <= baseline * 3:
        # Linear de 3.0 a 1.0
        score_lat = 3.0 - ((latencia - baseline * 2) / baseline) * 2.0
    else:
        # Decai rapidamente após 3x baseline
        score_lat = max(0, 1.0 - ((latencia - baseline * 3) / baseline) * 0.5)

    # Score de perda (0-4 pontos, 40% do total)
    if perda_percentual == 0:
        score_perda = 4.0
    elif perda_percentual <= 2:
        # Linear de 4.0 a 3.0
        score_perda = 4.0 - (perda_percentual / 2.0) * 1.0
    elif perda_percentual <= 5:
        # Linear de 3.0 a 1.0
        score_perda = 3.0 - ((perda_percentual - 2.0) / 3.0) * 2.0
    else:
        # Decai rapidamente após 5%
        score_perda = max(0, 1.0 - ((perda_percentual - 5.0) / 5.0) * 0.5)

    score_final = score_lat + score_perda

    # Classificação
    if score_final >= 8.5:
        classificacao = 'Excelente'
    elif score_final >= 7.0:
        classificacao = 'Muito Bom'
    elif score_final >= 5.5:
        classificacao = 'Bom'
    elif score_final >= 4.0:
        classificacao = 'Regular'
    else:
        classificacao = 'Ruim'

    return {
        'score': round(score_final, 1),
        'classificacao': classificacao,
        'componente_latencia': round(score_lat, 1),
        'componente_perda': round(score_perda, 1)
    }


def detectar_anomalias(dados_lista, latencia_por_hora, desvio_threshold=None, percentual_threshold=None):
    """
    Detecta anomalias baseado em desvio padrão e percentual acima do normal

    Args:
        dados_lista: Lista de dados de testes
        latencia_por_hora: dict com estatísticas por hora
        desvio_threshold: float, número de desvios padrão para anomalia
        percentual_threshold: float, percentual acima da média para anomalia

    Returns:
        list: [{'timestamp', 'tipo', 'latencia', 'esperado', 'z_score'/'percentual', 'severidade'}]
    """
    if desvio_threshold is None:
        desvio_threshold = DESVIO_ANOMALIA
    if percentual_threshold is None:
        percentual_threshold = PERCENTUAL_ANOMALIA

    anomalias = []

    # Calcular média e desvio padrão por hora
    estatisticas_hora = {}
    for hora in range(24):
        if hora in latencia_por_hora:
            h_data = latencia_por_hora[hora]
            # Coletar todas as latências válidas daquela hora
            lats = []
            for dado in dados_lista:
                if (dado.get('datetime') and dado['datetime'].hour == hora and
                    dado.get('ping_aghuse', {}).get('media') is not None):
                    lats.append(dado['ping_aghuse']['media'])

            if lats:
                media = sum(lats) / len(lats)
                # Desvio padrão
                if len(lats) > 1:
                    variancia = sum((x - media) ** 2 for x in lats) / len(lats)
                    desvio = variancia ** 0.5
                else:
                    desvio = 0

                estatisticas_hora[hora] = {
                    'media': media,
                    'desvio': desvio
                }

    # Verificar cada teste
    for dado in dados_lista:
        if not dado.get('datetime') or dado.get('ping_aghuse', {}).get('media') is None:
            continue

        hora = dado['datetime'].hour
        lat = dado['ping_aghuse']['media']

        if hora in estatisticas_hora:
            stats = estatisticas_hora[hora]

            # Anomalia por desvio padrão (apenas latências ALTAS são anomalias ruins)
            if stats['desvio'] > 0:
                z_score = (lat - stats['media']) / stats['desvio']

                # Detectar apenas z_score POSITIVO (latência acima da média)
                if z_score > desvio_threshold:
                    anomalias.append({
                        'timestamp': dado['datetime'],
                        'tipo': 'desvio_padrao',
                        'latencia': lat,
                        'esperado': stats['media'],
                        'z_score': z_score,
                        'severidade': 'alta' if z_score > 3 else 'media'
                    })
                    continue  # Não duplicar anomalia

            # Anomalia por percentual
            if stats['media'] > 0:
                percentual = (lat / stats['media']) * 100

                if percentual > percentual_threshold:
                    anomalias.append({
                        'timestamp': dado['datetime'],
                        'tipo': 'percentual',
                        'latencia': lat,
                        'esperado': stats['media'],
                        'percentual': percentual,
                        'severidade': 'alta' if percentual > 300 else 'media'
                    })

    return sorted(anomalias, key=lambda x: x['timestamp'])


def analisar_rotas_tracert(dados_lista):
    """
    Analisa padrões de rotas do tracert e correlaciona com perda de pacotes

    Args:
        dados_lista: Lista de dados de testes

    Returns:
        dict: {
            'rotas_unicas': {rota_hash: {'count': int, 'com_perda': int, 'sem_perda': int, 'exemplos': [dados]}},
            'mudancas_rota': [{'timestamp', 'rota_anterior', 'rota_nova', 'teve_perda'}],
            'correlacao': {'texto': str, 'percentual_perda_rota_alternativa': float}
        }
    """
    from collections import defaultdict

    # Identificar todas as rotas únicas
    rotas_unicas = defaultdict(lambda: {'count': 0, 'com_perda': 0, 'sem_perda': 0, 'exemplos': []})

    # Rastrear mudanças de rota
    mudancas_rota = []
    rota_anterior = None

    # Agrupar testes por rota
    for dado in dados_lista:
        if not dado.get('tracert_rota') or not dado.get('tracert_rota', {}).get('hash'):
            continue

        rota_hash = dado['tracert_rota']['hash']
        perda_valor = dado.get('ping_interno', {}).get('perda')
        tem_perda = perda_valor is not None and perda_valor > 0

        # Contar ocorrências
        rotas_unicas[rota_hash]['count'] += 1

        if tem_perda:
            rotas_unicas[rota_hash]['com_perda'] += 1
        else:
            rotas_unicas[rota_hash]['sem_perda'] += 1

        # Guardar exemplo
        if len(rotas_unicas[rota_hash]['exemplos']) < 3:
            rotas_unicas[rota_hash]['exemplos'].append({
                'timestamp': dado.get('datetime'),
                'perda': dado.get('ping_interno', {}).get('perda', 0),
                'latencia': dado.get('ping_interno', {}).get('media', 0)
            })

        # Detectar mudanças de rota
        if rota_anterior is not None and rota_anterior != rota_hash:
            mudancas_rota.append({
                'timestamp': dado.get('datetime'),
                'rota_anterior': rota_anterior,
                'rota_nova': rota_hash,
                'teve_perda': tem_perda
            })

        rota_anterior = rota_hash

    # Calcular correlação
    total_testes = sum(r['count'] for r in rotas_unicas.values())
    rota_principal = max(rotas_unicas.items(), key=lambda x: x[1]['count']) if rotas_unicas else None

    correlacao = {'texto': '', 'percentual_perda_rota_alternativa': 0}

    if rota_principal and len(rotas_unicas) > 1:
        rota_principal_hash, rota_principal_stats = rota_principal

        # Calcular percentual de perda na rota principal
        perda_principal = (rota_principal_stats['com_perda'] / rota_principal_stats['count'] * 100) if rota_principal_stats['count'] > 0 else 0

        # Calcular percentual de perda em rotas alternativas
        rotas_alternativas = {k: v for k, v in rotas_unicas.items() if k != rota_principal_hash}
        testes_alternativos = sum(r['count'] for r in rotas_alternativas.values())
        perdas_alternativas = sum(r['com_perda'] for r in rotas_alternativas.values())
        perda_alternativas = (perdas_alternativas / testes_alternativos * 100) if testes_alternativos > 0 else 0

        correlacao['percentual_perda_rota_principal'] = round(perda_principal, 2)
        correlacao['percentual_perda_rota_alternativa'] = round(perda_alternativas, 2)
        correlacao['mudancas_com_perda'] = sum(1 for m in mudancas_rota if m['teve_perda'])
        correlacao['total_mudancas'] = len(mudancas_rota)

        # Análise textual
        if perda_alternativas > perda_principal * 1.5:
            correlacao['texto'] = f"Rotas alternativas apresentam {perda_alternativas:.1f}% de perda vs {perda_principal:.1f}% na rota principal. Possível instabilidade em rotas alternativas."
        elif len(mudancas_rota) > 0:
            pct_mudancas_com_perda = (correlacao['mudancas_com_perda'] / len(mudancas_rota) * 100)
            correlacao['texto'] = f"Detectadas {len(mudancas_rota)} mudanças de rota, sendo {pct_mudancas_com_perda:.0f}% associadas a perda de pacotes."
        else:
            correlacao['texto'] = "Rota estável durante todo o período analisado."

    elif rota_principal:
        # Apenas uma rota detectada
        correlacao['texto'] = "Rota única estável durante todo o período. Sem mudanças de caminho detectadas."
    else:
        correlacao['texto'] = "Dados de tracert insuficientes para análise."

    return {
        'rotas_unicas': dict(rotas_unicas),
        'mudancas_rota': mudancas_rota,
        'correlacao': correlacao,
        'rota_principal': rota_principal[0] if rota_principal else None
    }


def analisar_dia_semana(dados_lista):
    """
    Agrupa dados por dia da semana e compara padrões

    Args:
        dados_lista: Lista de dados de testes

    Returns:
        list: [{'dia', 'latencia_media', 'vs_media_geral', 'pior_horario', 'pior_latencia', 'testes'}]
    """
    dias_semana = {i: {'latencias': [], 'testes': 0} for i in range(7)}
    nomes_dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']

    # Agrupar dados por dia da semana
    for dado in dados_lista:
        if not dado.get('datetime') or dado.get('ping_aghuse', {}).get('media') is None:
            continue

        dia = dado['datetime'].weekday()  # 0=Segunda, 6=Domingo
        lat = dado['ping_aghuse']['media']

        dias_semana[dia]['latencias'].append(lat)
        dias_semana[dia]['testes'] += 1

    # Calcular média geral
    todas_latencias = [lat for dia in dias_semana.values() for lat in dia['latencias']]
    if not todas_latencias:
        return []

    media_geral = sum(todas_latencias) / len(todas_latencias)

    # Calcular estatísticas por dia - INCLUIR TODOS OS DIAS (com ou sem dados)
    resultado = []
    for i, nome in enumerate(nomes_dias):
        # Se não tem dados, adicionar com zeros
        if dias_semana[i]['testes'] == 0:
            resultado.append({
                'dia': nome,
                'latencia_media': 0,
                'vs_media_geral': 0,
                'pior_horario': 0,
                'pior_latencia': 0,
                'testes': 0
            })
            continue

        lats = dias_semana[i]['latencias']
        media_dia = sum(lats) / len(lats)

        # Encontrar pior horário desse dia da semana
        piores = [(dado['datetime'].hour, dado['ping_aghuse']['media'])
                  for dado in dados_lista
                  if (dado.get('datetime') and
                      dado['datetime'].weekday() == i and
                      dado.get('ping_aghuse', {}).get('media') is not None)]

        if piores:
            pior = max(piores, key=lambda x: x[1])
            pior_horario = pior[0]
            pior_latencia = pior[1]
        else:
            pior_horario = 0
            pior_latencia = 0

        resultado.append({
            'dia': nome,
            'latencia_media': media_dia,
            'vs_media_geral': ((media_dia - media_geral) / media_geral * 100) if media_geral > 0 else 0,
            'pior_horario': pior_horario,
            'pior_latencia': pior_latencia,
            'testes': dias_semana[i]['testes']
        })

    # Retornar na ordem da semana (Segunda a Domingo) - NÃO ordenar por latência
    return resultado


def calcular_distribuicao(latencias, bins=None):
    """
    Calcula histograma de distribuição de latências

    Args:
        latencias: list de valores de latência
        bins: list de tuplas (min, max) definindo faixas

    Returns:
        list: [{'faixa', 'min', 'max', 'frequencia', 'percentual'}]
    """
    if bins is None:
        bins = [(0, 20), (20, 40), (40, 60), (60, 80), (80, float('inf'))]

    if not latencias:
        return []

    distribuicao = []
    total = len(latencias)

    for min_val, max_val in bins:
        count = sum(1 for lat in latencias if min_val <= lat < max_val)
        percentual = (count / total * 100) if total > 0 else 0

        # Formatar label
        if max_val == float('inf'):
            label = f"{min_val}+ms"
        else:
            label = f"{min_val}-{max_val}ms"

        distribuicao.append({
            'faixa': label,
            'min': min_val,
            'max': max_val,
            'frequencia': count,
            'percentual': round(percentual, 1)
        })

    return distribuicao

# ============================================================================


def gerar_relatorio_diario(dia, dados_dia, stats):
    """Gera relatório diário em formato markdown"""
    md = []

    data_formatada = dia.strftime("%d/%m/%Y")
    md.append(f"# Relatório AGHUSE - {data_formatada}\n\n")

    # Status Geral
    md.append("## Status do Dia\n\n")

    # Disponibilidade em destaque
    if stats['disponibilidade'] >= 99.9:
        status_disp = "ÓTIMO"
    elif stats['disponibilidade'] >= 99.0:
        status_disp = "BOM"
    elif stats['disponibilidade'] >= 95.0:
        status_disp = "REGULAR"
    else:
        status_disp = "RUIM"

    md.append(f"**Conexão: {stats['disponibilidade']:.2f}%** - {status_disp}\n\n")

    # Problemas detectados (se houver)
    problemas = []
    if stats['testes_com_perda'] > 0:
        problemas.append(f"{stats['testes_com_perda']} horários com perda de conexão")
    if stats['latencia_alta_count'] > 0:
        problemas.append(f"{stats['latencia_alta_count']} horários com lentidão")

    if problemas:
        md.append("**Problemas:**\n")
        for p in problemas:
            md.append(f"- {p}\n")
        md.append("\n")

    # Análise por Horário (usando função reutilizável)
    md.append("## Desempenho por Horário\n\n")
    stats_latencia_hora = analisar_latencia_por_horario(dados_dia)
    md.append(gerar_tabela_latencia_horaria(stats_latencia_hora, incluir_grafico=True))

    # Métricas de Qualidade (simplificado)
    jitter_stats = calcular_jitter_e_estabilidade(dados_dia)
    latencias = [d['ping_aghuse']['media'] for d in dados_dia if d['ping_aghuse']['media'] > 0]
    percentis = calcular_percentis_sla(latencias)
    comparacao = analisar_comparacao_endpoints(dados_dia)

    if jitter_stats or percentis or comparacao:
        md.append("## Análise Técnica\n\n")

        if percentis:
            md.append(f"**Tempo de resposta:** Típico {percentis['p50']}ms | 95% dos casos abaixo de {percentis['p95']}ms\n\n")

        if jitter_stats:
            md.append(f"**Estabilidade:** {jitter_stats['classificacao']} (variação {jitter_stats['jitter_medio']}ms)\n\n")

        if comparacao:
            md.append(f"**Comparativo de destinos:**\n")
            md.append(f"- AGHUSE: {comparacao['media_aghuse']}ms\n")
            md.append(f"- Rede interna: {comparacao['media_interno']}ms\n")
            md.append(f"- Internet: {comparacao['media_externo']}ms\n")

            if comparacao['diagnostico'] != "Normal":
                md.append(f"\n")
                if comparacao['diagnostico'] == "AGHUSE":
                    md.append(f"Problema identificado: AGHUSE {abs(comparacao['diff_aghuse_externo']):.0f}% mais lento que o normal\n")
                elif comparacao['diagnostico'] == "Rede Interna":
                    md.append(f"Problema identificado: Rede interna com lentidão\n")
                elif comparacao['diagnostico'] == "ISP/Internet":
                    md.append(f"Problema identificado: Conexão com internet lenta\n")
            md.append("\n")

    # Detalhes de problemas (se houver)
    if stats['testes_com_perda'] > 0:
        md.append("## Detalhes de Problemas\n\n")
        md.append(f"**Perda de Pacotes:** {stats['testes_com_perda']} ocorrências\n")
        horarios_perda = [d['hora'] for d in stats['lista_testes_com_perda'][:8]]
        md.append(f"- {', '.join(horarios_perda)}")
        if len(stats['lista_testes_com_perda']) > 8:
            md.append(f" e mais {len(stats['lista_testes_com_perda']) - 8}")
        md.append("\n\n")

    # Conclusão
    md.append("## Resumo\n\n")
    md.append(gerar_analise_disponibilidade(stats['disponibilidade']))
    md.append(gerar_analise_qualidade_horaria(stats_latencia_hora))

    return ''.join(md)

def gerar_relatorio_semanal(dados_por_dia, domingo=None, sabado=None):
    """Gera relatório semanal consolidado

    Args:
        dados_por_dia: Dicionário com dados por dia
        domingo: Data do domingo (início da semana). Se None, usa semana atual
        sabado: Data do sábado (fim da semana). Se None, calcula a partir do domingo
    """
    md = []

    # Se domingo não foi fornecido, calcular semana atual
    if domingo is None:
        hoje = datetime.now().date()
        dias_desde_domingo = (hoje.weekday() + 1) % 7
        domingo = hoje - timedelta(days=dias_desde_domingo)

    # Se sábado não foi fornecido, calcular a partir do domingo
    if sabado is None:
        sabado = domingo + timedelta(days=6)

    # Gerar lista dos 7 dias da semana (domingo a sábado)
    dias_da_semana = [domingo + timedelta(days=i) for i in range(7)]

    primeira_data = domingo.strftime("%d/%m/%Y")
    ultima_data = sabado.strftime("%d/%m/%Y")

    md.append(f"# Relatório Semanal - Monitoramento de Conectividade AGHUSE\n")
    md.append(f"**Período**: {primeira_data} a {ultima_data}\n\n")

    # Filtrar dados apenas desta semana
    dados_semana = {}
    for dia in dias_da_semana:
        # Usar date diretamente, pois as chaves em dados_por_dia são date objects
        if dia in dados_por_dia:
            dados_semana[dia] = dados_por_dia[dia]
        else:
            dados_semana[dia] = []  # Dia sem dados

    # Estatísticas gerais do período (apenas dias com dados)
    todos_dados = []
    for dados_dia in dados_semana.values():
        if dados_dia:  # Se há dados no dia
            todos_dados.extend(dados_dia)

    # Se não há nenhum dado na semana
    if not todos_dados:
        md.append("**Aviso**: Nenhum dado coletado para esta semana ainda.\n\n")
        md.append("## Análise por Dia\n\n")
        md.append("| Data | Testes | Sem Perda / Com Perda | Pacotes Perdidos | Disponibilidade | AGHUSE (ms) | Rede Externa (ms) |\n")
        md.append("|------|--------|-----------------------|------------------|-----------------|-------------|-------------------|\n")
        for dia in dias_da_semana:
            data_fmt = dia.strftime("%d/%m/%Y")
            md.append(f"| {data_fmt} | - | - | - | - | - | - |\n")
        return ''.join(md)

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
    md.append("| Data | Testes | Sem Perda / Com Perda | Pacotes Perdidos | Disponibilidade | AGHUSE (ms) | Rede Externa (ms) |\n")
    md.append("|------|--------|-----------------------|------------------|-----------------|-------------|-------------------|\n")

    # Iterar pelos 7 dias da semana (domingo a sábado)
    for dia in dias_da_semana:
        data_fmt = dia.strftime("%d/%m/%Y")

        if dados_semana[dia]:  # Se há dados para este dia
            stats = calcular_estatisticas_dia(dados_semana[dia])
            md.append(f"| {data_fmt} | {stats['total_testes']} | {stats['testes_sem_perda']} / {stats['testes_com_perda']} | {stats['total_pacotes_perdidos']} | {stats['disponibilidade']:.2f}% | {stats['aghuse_media']:.1f}ms | {stats['externo_media']:.1f}ms |\n")
        else:  # Dia sem dados
            md.append(f"| {data_fmt} | - | - | - | - | - | - |\n")

    # Análise de Latência por Faixa Horária
    stats_latencia_hora = analisar_latencia_por_horario(todos_dados)
    if stats_latencia_hora:
        md.append("\n## Análise de Latência por Faixa Horária\n\n")
        md.append(f"> **Nota**: Esta análise consolida todos os testes realizados em cada faixa horária\n")
        md.append(f"> ao longo do período completo ({primeira_data} a {ultima_data}).\n")
        md.append(f"> Cada linha representa a média de todos os testes naquela hora em todos os dias.\n\n")
        md.append(gerar_tabela_latencia_horaria(stats_latencia_hora, incluir_grafico=True))

    # Análise de Horários Críticos (apenas da semana atual)
    # Converter dados_semana para formato esperado por analisar_horarios_problematicos
    dados_semana_para_analise = {}
    for dia, dados in dados_semana.items():
        if dados:  # Apenas dias com dados
            dados_semana_para_analise[dia] = dados

    horarios_problemas, horarios_latencia = analisar_horarios_problematicos(dados_semana_para_analise)

    if horarios_problemas:
        md.append("## Análise de Horários Críticos\n\n")
        md.append("### Distribuição de Perda de Pacotes por Horário\n\n")
        md.append("| Faixa Horária | Ocorrências | Porcentagem do Total |\n")
        md.append("|---------------|-------------|---------------------|\n")

        for hora in sorted(horarios_problemas.keys(), key=lambda h: horarios_problemas[h], reverse=True):
            count = horarios_problemas[hora]
            percent = (count / stats_geral['testes_com_perda']) * 100
            md.append(f"| {hora:02d}:00 - {hora:02d}:59 | {count} | {percent:.1f}% |\n")
        md.append("\n")

    if horarios_latencia:
        md.append("### Distribuição de Latência Elevada (>20ms) por Horário\n\n")
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

    # ========================================================================
    # ANÁLISES AVANÇADAS
    # ========================================================================

    # 1. Score de Qualidade por Horário
    scores_horario = {}
    for hora in range(24):
        if hora in stats_latencia_hora:
            h_data = stats_latencia_hora[hora]
            media_lat = h_data['media']

            # Calcular percentual de perda naquela hora
            testes_hora = [d for d in todos_dados if d.get('datetime') and d['datetime'].hour == hora]
            testes_com_perda_hora = sum(1 for d in testes_hora if d.get('ping_aghuse', {}).get('perda', 0) > 0)
            total_testes_hora = len(testes_hora)
            perda_pct = (testes_com_perda_hora / total_testes_hora * 100) if total_testes_hora > 0 else 0

            scores_horario[hora] = calcular_score_qualidade_horario(media_lat, perda_pct, LATENCIA_IDEAL)

    md.append("## Score de Qualidade por Horário\n\n")
    md.append("| Horário | Score | Classificação | Componente Latência | Componente Perda |\n")
    md.append("|---------|-------|---------------|---------------------|------------------|\n")
    for hora in sorted(scores_horario.keys()):
        s = scores_horario[hora]
        md.append(f"| {hora:02d}h | {s['score']} | {s['classificacao']} | ")
        md.append(f"{s['componente_latencia']} | {s['componente_perda']} |\n")
    md.append("\n")

    # 4. Análise por Dia da Semana
    analise_dias_semana = analisar_dia_semana(todos_dados)
    if analise_dias_semana:
        md.append("## Análise por Dia da Semana\n\n")
        md.append("| Dia | Latência Média | vs. Média Geral | Pior Horário | Testes |\n")
        md.append("|-----|----------------|-----------------|--------------|--------|\n")
        for dia in analise_dias_semana:
            if dia['testes'] == 0:
                # Dia sem dados - mostrar zeros e aviso na mesma linha
                md.append(f"| {dia['dia']} | - | - | - | 0 |\n")
            elif dia['testes'] < 10:
                # Poucos dados - mostrar com aviso
                md.append(f"| {dia['dia']} | {dia['latencia_media']:.1f}ms ⚠️ | ")
                md.append(f"{dia['vs_media_geral']:+.1f}% | ")
                md.append(f"{dia['pior_horario']:02d}h ({dia['pior_latencia']:.1f}ms) | ")
                md.append(f"{dia['testes']} |\n")
            else:
                # Dados suficientes - mostrar normalmente
                md.append(f"| {dia['dia']} | {dia['latencia_media']:.1f}ms | ")
                md.append(f"{dia['vs_media_geral']:+.1f}% | ")
                md.append(f"{dia['pior_horario']:02d}h ({dia['pior_latencia']:.1f}ms) | ")
                md.append(f"{dia['testes']} |\n")
        md.append("\n")

    # 5. Detecção de Anomalias, Horários de Pico e Análise de Rotas
    anomalias = detectar_anomalias(todos_dados, stats_latencia_hora)
    picos = detectar_horarios_pico(stats_latencia_hora)
    analise_rotas = analisar_rotas_tracert(todos_dados)

    md.append("## Alertas de Anomalias\n\n")

    # 5.1 Horários de Pico
    md.append("### Horários de Pico\n\n")
    if picos:
        md.append("Períodos com latência significativamente acima da média (>10%):\n\n")
        for pico in picos:
            md.append(f"- **{pico['nome']}**: {pico['inicio']:02d}h-{pico['fim']:02d}h ")
            md.append(f"(latência média {pico['latencia_media']:.1f}ms, ")
            md.append(f"+{pico['diferenca_media']:.1f}ms acima da média, {pico['count']}h consecutivas)\n")
        md.append("\n")
    else:
        md.append("Nenhum período de pico identificado. ✅\n\n")

    # 5.2 Análise de Rotas e Correlação com Perda de Pacotes
    md.append("### Análise de Rotas (Tracert)\n\n")

    if analise_rotas['rota_principal']:
        num_rotas = len(analise_rotas['rotas_unicas'])
        md.append(f"**Total de rotas detectadas**: {num_rotas}\n\n")

        if num_rotas > 1:
            md.append("**Rotas identificadas**:\n\n")
            md.append("| Rota | Ocorrências | Com Perda | Sem Perda | Taxa de Perda |\n")
            md.append("|------|-------------|-----------|-----------|---------------|\n")

            # Ordenar rotas por ocorrência
            rotas_ordenadas = sorted(
                analise_rotas['rotas_unicas'].items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )

            for idx, (rota_hash, stats) in enumerate(rotas_ordenadas[:5], 1):
                # Simplificar rota para exibição
                ips = rota_hash.split(' -> ')
                rota_simples = f"{ips[0]} -> ... -> {ips[-1]}" if len(ips) > 3 else rota_hash
                taxa_perda = (stats['com_perda'] / stats['count'] * 100) if stats['count'] > 0 else 0
                principal = " (Principal)" if rota_hash == analise_rotas['rota_principal'] else ""

                md.append(f"| Rota {idx}{principal} | {stats['count']} | {stats['com_perda']} | {stats['sem_perda']} | {taxa_perda:.1f}% |\n")

            md.append("\n")

        # Correlação
        md.append(f"**Correlação Rota vs Perda de Pacotes**: {analise_rotas['correlacao']['texto']}\n\n")

        # Mudanças de rota
        if analise_rotas['mudancas_rota']:
            total_mudancas = len(analise_rotas['mudancas_rota'])
            mudancas_com_perda = sum(1 for m in analise_rotas['mudancas_rota'] if m['teve_perda'])

            md.append(f"**Mudanças de rota detectadas**: {total_mudancas} ")
            md.append(f"({mudancas_com_perda} associadas a perda de pacotes)\n\n")

            if mudancas_com_perda > 0:
                md.append("*Últimas mudanças de rota com perda*:\n\n")
                mudancas_recentes = [m for m in analise_rotas['mudancas_rota'] if m['teve_perda']][-5:]
                for mudanca in mudancas_recentes:
                    timestamp = mudanca['timestamp'].strftime('%d/%m às %H:%M')
                    md.append(f"- {timestamp}\n")
                md.append("\n")
    else:
        md.append("Dados de tracert insuficientes para análise.\n\n")

    # 5.3 Anomalias de Latência
    md.append("### Anomalias de Latência\n\n")
    if anomalias:
        md.append(f"Total de {len(anomalias)} anomalia(s) detectada(s):\n\n")
        for anomalia in anomalias[:10]:  # Top 10
            timestamp = anomalia['timestamp'].strftime('%d/%m às %H:%M')
            if anomalia['tipo'] == 'desvio_padrao':
                md.append(f"⚠️ **{timestamp}**: Latência {anomalia['latencia']}ms ")
                md.append(f"({abs(anomalia['z_score']):.1f}σ acima do esperado {anomalia['esperado']:.1f}ms) ")
                md.append(f"[Severidade: {anomalia['severidade']}]\n")
            else:
                md.append(f"⚠️ **{timestamp}**: Latência {anomalia['latencia']}ms ")
                md.append(f"({anomalia['percentual']:.0f}% do esperado {anomalia['esperado']:.1f}ms) ")
                md.append(f"[Severidade: {anomalia['severidade']}]\n")

        if len(anomalias) > 10:
            md.append(f"\n*Exibindo 10 de {len(anomalias)} anomalias. Anomalias indicam desvios significativos do padrão normal.*\n")
    else:
        md.append("Nenhuma anomalia de latência detectada no período. ✅\n")
    md.append("\n")

    # 6. Distribuição de Latência
    todas_latencias = [d['ping_aghuse']['media'] for d in todos_dados
                       if d.get('ping_aghuse', {}).get('media') is not None]
    distribuicao = calcular_distribuicao(todas_latencias)
    md.append("## Distribuição de Latência\n\n")
    md.append("| Faixa | Frequência | Percentual |\n")
    md.append("|-------|-----------|------------|\n")
    for bin in distribuicao:
        md.append(f"| {bin['faixa']} | {bin['frequencia']} | {bin['percentual']}% |\n")
    md.append("\n")

    # ========================================================================

    # Análise e Conclusão (usando funções reutilizáveis)
    md.append("## Análise e Conclusão\n\n")
    md.append(gerar_analise_disponibilidade(stats_geral['disponibilidade']))
    md.append(gerar_analise_qualidade_horaria(stats_latencia_hora, titulo="**Qualidade por Faixa Horária no Período**"))

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

    # Análise de Latência por Faixa Horária
    md.append("## Análise de Latência por Faixa Horária\n\n")
    md.append(f"> **Nota**: Esta análise consolida todos os testes realizados em cada faixa horária\n")
    md.append(f"> ao longo do período completo ({primeira_data} a {ultima_data}, {total_dias} dias).\n")
    md.append(f"> Cada linha representa a média de todos os testes naquela hora em todos os dias.\n\n")

    stats_latencia_hora = analisar_latencia_por_horario(todos_dados)
    md.append(gerar_tabela_latencia_horaria(stats_latencia_hora, incluir_grafico=True))

    # Análise por Dia
    md.append("## Análise por Dia\n\n")
    md.append("| Data | Testes | Sem Perda / Com Perda | Pacotes Perdidos | Disponibilidade | AGHUSE (ms) | Rede Externa (ms) |\n")
    md.append("|------|--------|-----------------------|------------------|-----------------|-------------|-------------------|\n")

    for dia in dias_ordenados:
        dados_dia = dados_por_dia[dia]
        stats = calcular_estatisticas_dia(dados_dia)
        data_fmt = dia.strftime("%d/%m/%Y")

        md.append(f"| {data_fmt} | {stats['total_testes']} | {stats['testes_sem_perda']} / {stats['testes_com_perda']} | {stats['total_pacotes_perdidos']} | {stats['disponibilidade']:.2f}% | {stats['aghuse_media']:.1f}ms | {stats['externo_media']:.1f}ms |\n")

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

    # ============================================================
    # ANÁLISES AVANÇADAS
    # ============================================================

    # 1. Score de Qualidade por Horário (AGHUSE e Rede Externa)
    scores_horario_aghuse = {}
    scores_horario_externo = {}

    for hora in range(24):
        if hora in stats_latencia_hora:
            h_data = stats_latencia_hora[hora]

            # Score AGHUSE
            media_lat = h_data['media']
            testes_perda = h_data.get('testes_com_perda', 0)
            total_testes = h_data.get('total_testes', 1)
            perda_pct = (testes_perda / total_testes * 100) if total_testes > 0 else 0

            scores_horario_aghuse[hora] = calcular_score_qualidade_horario(
                media_lat, perda_pct, LATENCIA_IDEAL
            )

            # Score Rede Externa (usando dados do mesmo h_data)
            media_lat_ext = h_data.get('media_externo', 0)
            testes_perda_ext = h_data.get('testes_com_perda_externo', 0)
            perda_pct_ext = (testes_perda_ext / total_testes * 100) if total_testes > 0 else 0

            if media_lat_ext > 0:  # Só calcular se há dados
                scores_horario_externo[hora] = calcular_score_qualidade_horario(
                    media_lat_ext, perda_pct_ext, LATENCIA_IDEAL
                )

    md.append("## Score de Qualidade por Horário\n\n")
    md.append("| Horário | Score AGHUSE | Class. AGHUSE | Score Rede Ext. | Class. Rede Ext. |\n")
    md.append("|---------|--------------|---------------|-----------------|------------------|\n")

    for hora in range(24):
        if hora in scores_horario_aghuse or hora in scores_horario_externo:
            # Score AGHUSE
            if hora in scores_horario_aghuse:
                s_ag = scores_horario_aghuse[hora]
                score_ag_text = f"{s_ag['score']}"
                class_ag_text = s_ag['classificacao']
            else:
                score_ag_text = "N/A"
                class_ag_text = "N/A"

            # Score Rede Externa
            if hora in scores_horario_externo:
                s_ext = scores_horario_externo[hora]
                score_ext_text = f"{s_ext['score']}"
                class_ext_text = s_ext['classificacao']
            else:
                score_ext_text = "N/A"
                class_ext_text = "N/A"

            md.append(f"| {hora:02d}h | {score_ag_text} | {class_ag_text} | ")
            md.append(f"{score_ext_text} | {class_ext_text} |\n")

    md.append("\n")

    # 4. Análise por Dia da Semana
    analise_dias = analisar_dia_semana(todos_dados)
    md.append("## Análise por Dia da Semana\n\n")
    md.append("| Dia | Latência Média | vs. Média Geral | Pior Horário | Testes |\n")
    md.append("|-----|----------------|-----------------|--------------|--------|\n")
    for dia in analise_dias:
        if dia['testes'] == 0:
            # Dia sem dados - mostrar traços
            md.append(f"| {dia['dia']} | - | - | - | 0 |\n")
        elif dia['testes'] < 10:
            # Poucos dados - mostrar com aviso
            md.append(f"| {dia['dia']} | {dia['latencia_media']:.1f}ms ⚠️ | ")
            md.append(f"{dia['vs_media_geral']:+.1f}% | ")
            md.append(f"{dia['pior_horario']:02d}h ({dia['pior_latencia']:.1f}ms) | ")
            md.append(f"{dia['testes']} |\n")
        else:
            # Dados suficientes - mostrar normalmente
            md.append(f"| {dia['dia']} | {dia['latencia_media']:.1f}ms | ")
            md.append(f"{dia['vs_media_geral']:+.1f}% | ")
            md.append(f"{dia['pior_horario']:02d}h ({dia['pior_latencia']:.1f}ms) | ")
            md.append(f"{dia['testes']} |\n")
    md.append("\n")

    # 5. Detecção de Anomalias, Horários de Pico e Análise de Rotas
    anomalias = detectar_anomalias(todos_dados, stats_latencia_hora)
    picos = detectar_horarios_pico(stats_latencia_hora)
    analise_rotas = analisar_rotas_tracert(todos_dados)

    md.append("## Alertas de Anomalias\n\n")

    # 5.1 Horários de Pico
    md.append("### Horários de Pico\n\n")
    if picos:
        md.append("Períodos com latência significativamente acima da média (>10%):\n\n")
        for pico in picos:
            md.append(f"- **{pico['nome']}**: {pico['inicio']:02d}h-{pico['fim']:02d}h ")
            md.append(f"(latência média {pico['latencia_media']:.1f}ms, ")
            md.append(f"+{pico['diferenca_media']:.1f}ms acima da média, {pico['count']}h consecutivas)\n")
        md.append("\n")
    else:
        md.append("Nenhum período de pico identificado. ✅\n\n")

    # 5.2 Análise de Rotas e Correlação com Perda de Pacotes
    md.append("### Análise de Rotas (Tracert)\n\n")

    if analise_rotas['rota_principal']:
        num_rotas = len(analise_rotas['rotas_unicas'])
        md.append(f"**Total de rotas detectadas**: {num_rotas}\n\n")

        if num_rotas > 1:
            md.append("**Rotas identificadas**:\n\n")
            md.append("| Rota | Ocorrências | Com Perda | Sem Perda | Taxa de Perda |\n")
            md.append("|------|-------------|-----------|-----------|---------------|\n")

            # Ordenar rotas por ocorrência
            rotas_ordenadas = sorted(
                analise_rotas['rotas_unicas'].items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )

            for idx, (rota_hash, stats) in enumerate(rotas_ordenadas[:5], 1):
                # Simplificar rota para exibição
                ips = rota_hash.split(' -> ')
                rota_simples = f"{ips[0]} -> ... -> {ips[-1]}" if len(ips) > 3 else rota_hash
                taxa_perda = (stats['com_perda'] / stats['count'] * 100) if stats['count'] > 0 else 0
                principal = " (Principal)" if rota_hash == analise_rotas['rota_principal'] else ""

                md.append(f"| Rota {idx}{principal} | {stats['count']} | {stats['com_perda']} | {stats['sem_perda']} | {taxa_perda:.1f}% |\n")

            md.append("\n")

        # Correlação
        md.append(f"**Correlação Rota vs Perda de Pacotes**: {analise_rotas['correlacao']['texto']}\n\n")

        # Mudanças de rota
        if analise_rotas['mudancas_rota']:
            total_mudancas = len(analise_rotas['mudancas_rota'])
            mudancas_com_perda = sum(1 for m in analise_rotas['mudancas_rota'] if m['teve_perda'])

            md.append(f"**Mudanças de rota detectadas**: {total_mudancas} ")
            md.append(f"({mudancas_com_perda} associadas a perda de pacotes)\n\n")

            if mudancas_com_perda > 0:
                md.append("*Últimas mudanças de rota com perda*:\n\n")
                mudancas_recentes = [m for m in analise_rotas['mudancas_rota'] if m['teve_perda']][-5:]
                for mudanca in mudancas_recentes:
                    timestamp = mudanca['timestamp'].strftime('%d/%m às %H:%M')
                    md.append(f"- {timestamp}\n")
                md.append("\n")
    else:
        md.append("Dados de tracert insuficientes para análise.\n\n")

    # 5.3 Anomalias de Latência
    md.append("### Anomalias de Latência\n\n")
    if anomalias:
        md.append(f"Total de {len(anomalias)} anomalia(s) detectada(s):\n\n")
        for anomalia in anomalias[:10]:  # Top 10
            timestamp = anomalia['timestamp'].strftime('%d/%m às %H:%M')
            if anomalia['tipo'] == 'desvio_padrao':
                md.append(f"⚠️ **{timestamp}**: Latência {anomalia['latencia']}ms ")
                md.append(f"({anomalia['z_score']:.1f}σ acima do esperado {anomalia['esperado']:.1f}ms)")
                if anomalia['severidade'] == 'alta':
                    md.append(" 🔴 **ALTA**")
                md.append("\n")
            else:
                md.append(f"⚠️ **{timestamp}**: Latência {anomalia['latencia']}ms ")
                md.append(f"({anomalia['percentual']:.0f}% do esperado {anomalia['esperado']:.1f}ms)")
                if anomalia['severidade'] == 'alta':
                    md.append(" 🔴 **ALTA**")
                md.append("\n")
        if len(anomalias) > 10:
            md.append(f"\n*Exibindo 10 de {len(anomalias)} anomalias. Anomalias indicam desvios significativos do padrão normal.*\n")
    else:
        md.append("Nenhuma anomalia de latência detectada no período. ✅\n")
    md.append("\n")

    # 6. Distribuição de Latência
    todas_latencias = [d['ping_aghuse']['media'] for d in todos_dados if d['ping_aghuse']['media'] is not None]
    distribuicao = calcular_distribuicao(todas_latencias)
    md.append("## Distribuição de Latência\n\n")
    md.append("| Faixa | Frequência | Percentual |\n")
    md.append("|-------|-----------|------------|\n")
    for bin_data in distribuicao:
        md.append(f"| {bin_data['faixa']} | {bin_data['frequencia']} | {bin_data['percentual']}% |\n")
    md.append("\n")

    # Análise e Conclusão
    md.append("## Análise e Conclusão\n\n")

    # Análise de disponibilidade com recomendações (usando função reutilizável + recomendações)
    md.append(gerar_analise_disponibilidade(stats_geral['disponibilidade']).rstrip('\n'))

    # Adicionar recomendações específicas baseadas na disponibilidade
    if stats_geral['disponibilidade'] >= 99.9:
        md.append("- Manter monitoramento contínuo\n\n")
    elif stats_geral['disponibilidade'] >= 99.0:
        md.append("- Acompanhar tendências\n\n")
    elif stats_geral['disponibilidade'] >= 95.0:
        md.append("- Recomenda-se análise dos horários críticos\n")
        md.append("- Implementar monitoramento mais granular\n\n")
    else:
        md.append("- Requer ação corretiva imediata\n")
        md.append("- Revisar infraestrutura de rede\n")
        md.append("- Analisar logs e traceroutes dos horários críticos\n\n")

    # Análise de qualidade por faixa horária (usando função reutilizável)
    md.append(gerar_analise_qualidade_horaria(stats_latencia_hora, titulo="**Qualidade por Faixa Horária no Período Completo**"))

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

    # Gerar relatórios semanais para todas as semanas que tenham dados
    print("\nGerando relatorios semanais...")

    # Identificar todas as semanas presentes nos dados
    if dados_por_dia:
        datas_disponiveis = sorted(dados_por_dia.keys())
        primeira_data = datas_disponiveis[0]
        ultima_data = datas_disponiveis[-1]

        # Encontrar o domingo da primeira semana
        dias_desde_domingo = (primeira_data.weekday() + 1) % 7
        primeiro_domingo = primeira_data - timedelta(days=dias_desde_domingo)

        # Gerar relatório para cada semana completa
        domingo_atual = primeiro_domingo
        relatorios_semanais_gerados = 0

        while domingo_atual <= ultima_data:
            sabado_atual = domingo_atual + timedelta(days=6)

            # Filtrar dados da semana (domingo a sábado)
            dados_semana = {
                dia: dados for dia, dados in dados_por_dia.items()
                if domingo_atual <= dia <= sabado_atual
            }

            # Só gerar relatório se houver pelo menos 1 dia de dados nesta semana
            if dados_semana:
                relatorio_semanal = gerar_relatorio_semanal(dados_por_dia, domingo_atual, sabado_atual)

                # Nome do arquivo com o período: RELATORIO_SEMANAL_DD-MM-AAAA_a_DD-MM-AAAA.md
                nome_semanal = f"RELATORIO_SEMANAL_{domingo_atual.strftime('%d-%m-%Y')}_a_{sabado_atual.strftime('%d-%m-%Y')}.md"
                caminho_semanal = os.path.join(pasta_relatorios, nome_semanal)

                with open(caminho_semanal, 'w', encoding='utf-8') as f:
                    f.write(relatorio_semanal)
                print(f"  [OK] {nome_semanal}")
                relatorios_semanais_gerados += 1

            # Avançar para próxima semana
            domingo_atual += timedelta(days=7)

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
    print(f"  - {relatorios_semanais_gerados} relatorio(s) semanal(is)")
    print(f"  - 1 relatorio geral")

    # Atualizar index.html com lista de relatórios
    print(f"\nAtualizando index.html...")
    try:
        import subprocess
        subprocess.run(['python', 'scripts/atualizar_index_completo.py'], check=True)
    except Exception as e:
        print(f"[AVISO] Erro ao atualizar index.html: {e}")

if __name__ == '__main__':
    main()
