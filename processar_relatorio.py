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

def analisar_latencia_por_horario(dados_lista):
    """Analisa latência média por faixa horária"""
    latencia_por_hora = defaultdict(list)
    perda_por_hora = defaultdict(list)

    for d in dados_lista:
        hora_int = int(d['hora'].split(':')[0])

        if d['ping_aghuse']['media']:
            latencia_por_hora[hora_int].append(d['ping_aghuse']['media'])

        if d['ping_aghuse']['perda'] is not None:
            perda_por_hora[hora_int].append(d['ping_aghuse']['perda'])

    # Calcular estatísticas por hora
    stats_por_hora = {}
    for hora in latencia_por_hora.keys():
        latencias = latencia_por_hora[hora]
        perdas = perda_por_hora.get(hora, [])

        testes_com_perda = sum(1 for p in perdas if p > 0)

        stats_por_hora[hora] = {
            'media': sum(latencias) / len(latencias),
            'min': min(latencias),
            'max': max(latencias),
            'testes': len(latencias),
            'testes_com_perda': testes_com_perda,
            'perda_total': sum(perdas)
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
    """Gera tabela de latência por faixa horária com gráfico opcional"""
    if not stats_latencia_hora:
        return "*Nenhum dado disponível.*\n\n"

    md = []

    # Tabela simplificada - apenas o essencial
    md.append("| Horário | Latência (ms) | Status |\n")
    md.append("|---------|---------------|--------|\n")

    for hora in sorted(stats_latencia_hora.keys()):
        s = stats_latencia_hora[hora]
        classificacao, _ = classificar_faixa_horaria(s)

        # Adicionar alerta se tiver perda
        if s['testes_com_perda'] > 0:
            alerta = f" [{s['testes_com_perda']} perda(s)]"
        else:
            alerta = ""

        md.append(f"| {hora:02d}h | {s['media']:.1f} ({s['min']}-{s['max']}) | {classificacao}{alerta} |\n")

    md.append("\n")

    if incluir_grafico:
        md.append("**Gráfico de Latência:**\n\n")
        md.append("```\n")
        valores_latencia = {hora: s['media'] for hora, s in stats_latencia_hora.items()}
        grafico_linhas = gerar_grafico_barras_ascii(valores_latencia)
        for linha in grafico_linhas:
            md.append(linha + "\n")
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
    latencias_aghuse = [d['ping_aghuse']['media'] for d in dados_lista if d['ping_aghuse']['media'] > 0]
    latencias_interno = [d['ping_interno']['media'] for d in dados_lista if d['ping_interno']['media'] > 0]
    latencias_externo = [d['ping_externo']['media'] for d in dados_lista if d['ping_externo']['media'] > 0]

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

    # Análise de Latência por Faixa Horária
    stats_latencia_hora = analisar_latencia_por_horario(todos_dados)
    if stats_latencia_hora:
        md.append("\n## Análise de Latência por Faixa Horária\n\n")
        md.append(f"> **Nota**: Esta análise consolida todos os testes realizados em cada faixa horária\n")
        md.append(f"> ao longo do período completo ({primeira_data} a {ultima_data}).\n")
        md.append(f"> Cada linha representa a média de todos os testes naquela hora em todos os dias.\n\n")
        md.append(gerar_tabela_latencia_horaria(stats_latencia_hora, incluir_grafico=True))

    # Análise de Horários Críticos
    horarios_problemas, horarios_latencia = analisar_horarios_problematicos(dados_por_dia)

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
