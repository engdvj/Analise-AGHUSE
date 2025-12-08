"""
Script completo para gerar relatórios AGHUSE
- Processa arquivos de teste e gera relatórios MD
- Converte relatórios MD para HTML visual
"""

import re
import json
import subprocess
import sys
import io
from datetime import datetime
from pathlib import Path


# ==================== PARSERS ====================

def parse_relatorio_diario(file_path):
    """Parse relatório diário"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    data = {
        'tipo': 'diario',
        'data': '',
        'conexao': 0.0,
        'status': '',
        'horarios_perda': 0,
        'horarios_lentidao': 0,
        'desempenho': []
    }

    match = re.search(r'# Relatório AGHUSE - (\d{2}/\d{2}/\d{4})', content)
    if match:
        data['data'] = match.group(1)

    match = re.search(r'\*\*Conexão:\s*([\d.]+)%\*\*\s*-\s*(\w+)', content)
    if match:
        data['conexao'] = float(match.group(1))
        data['status'] = match.group(2)

    match = re.search(r'-\s*(\d+)\s*horários com perda', content)
    if match:
        data['horarios_perda'] = int(match.group(1))

    match = re.search(r'-\s*(\d+)\s*horários com lentidão', content)
    if match:
        data['horarios_lentidao'] = int(match.group(1))

    desempenho_section = re.search(r'## Desempenho por Horário.*?(?=\*\*Gráfico|\Z)', content, re.DOTALL)
    if desempenho_section:
        lines = desempenho_section.group().split('\n')
        for line in lines:
            match = re.match(r'\|\s*(\d+)h\s*\|\s*([\d.]+)\s*\(([\d.]+)-([\d.]+)\)\s*\|\s*(.+?)\s*\|', line)
            if match:
                hora = int(match.group(1))
                latencia = float(match.group(2))
                lat_min = float(match.group(3))
                lat_max = float(match.group(4))
                status_text = match.group(5).strip()

                perda_match = re.search(r'\[(\d+)\s*perda', status_text)
                perdas = int(perda_match.group(1)) if perda_match else 0
                status = status_text.split('[')[0].strip()

                data['desempenho'].append({
                    'hora': hora,
                    'latencia': latencia,
                    'lat_min': lat_min,
                    'lat_max': lat_max,
                    'status': status,
                    'perdas': perdas
                })

    return data


def parse_relatorio_semanal(file_path):
    """Parse relatório semanal"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    data = {
        'tipo': 'semanal',
        'periodo': '',
        'metricas': {},
        'dias': [],
        'desempenho': []
    }

    match = re.search(r'\*\*Período\*\*:\s*(.+)', content)
    if match:
        data['periodo'] = match.group(1).strip()

    # Extrair métricas do sumário
    metricas_map = {
        'Total de Testes Executados': 'total_testes',
        'Testes sem Perda': 'testes_sem_perda',
        'Testes com Perda': 'testes_com_perda',
        'Total de Pacotes Enviados': 'pacotes_enviados',
        'Total de Pacotes Perdidos': 'pacotes_perdidos',
        '\\*\\*Disponibilidade\\*\\*': 'disponibilidade',
        'Latência Média': 'latencia_media'
    }

    for label, key in metricas_map.items():
        pattern = f'{label}\\s*\\|\\s*\\*?\\*?([\\d.]+)%?\\*?\\*?'
        match = re.search(pattern, content)
        if match:
            value = match.group(1).replace('ms', '').strip()
            data['metricas'][key] = float(value)

    # Extrair análise por dia
    dias_section = re.search(r'## Análise por Dia.*?##', content, re.DOTALL)
    if dias_section:
        lines = dias_section.group().split('\n')
        for line in lines:
            match = re.match(r'\|\s*(\d{2}/\d{2}/\d{4})\s*\|\s*(\d+)\s*\|.*?\|\s*([\d.]+)%\s*\|\s*([\d.]+)ms', line)
            if match:
                data['dias'].append({
                    'data': match.group(1),
                    'testes': int(match.group(2)),
                    'disponibilidade': float(match.group(3)),
                    'latencia': float(match.group(4))
                })

    # Extrair desempenho por horário
    desempenho_section = re.search(r'## Análise de Latência por Faixa Horária.*?(?=\*\*Gráfico|\Z)', content, re.DOTALL)
    if desempenho_section:
        lines = desempenho_section.group().split('\n')
        for line in lines:
            match = re.match(r'\|\s*(\d+)h\s*\|\s*([\d.]+)\s*\(([\d.]+)-([\d.]+)\)\s*\|\s*(.+?)\s*\|', line)
            if match:
                hora = int(match.group(1))
                latencia = float(match.group(2))
                lat_min = float(match.group(3))
                lat_max = float(match.group(4))
                status_text = match.group(5).strip()

                perda_match = re.search(r'\[(\d+)\s*perda', status_text)
                perdas = int(perda_match.group(1)) if perda_match else 0
                status = status_text.split('[')[0].strip()

                data['desempenho'].append({
                    'hora': hora,
                    'latencia': latencia,
                    'lat_min': lat_min,
                    'lat_max': lat_max,
                    'status': status,
                    'perdas': perdas
                })

    return data


def parse_relatorio_geral(file_path):
    """Parse relatório geral"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    data = {
        'tipo': 'geral',
        'periodo': '',
        'metricas': {},
        'desempenho': []
    }

    match = re.search(r'\*\*Período\*\*:\s*(.+)', content)
    if match:
        data['periodo'] = match.group(1).strip()

    # Extrair métricas
    metricas_map = {
        'Total de Testes Executados': 'total_testes',
        'Média de Testes por Dia': 'media_testes_dia',
        'Testes sem Perda': 'testes_sem_perda',
        'Testes com Perda': 'testes_com_perda',
        'Total de Pacotes Enviados': 'pacotes_enviados',
        'Total de Pacotes Perdidos': 'pacotes_perdidos',
        '\\*\\*Disponibilidade\\*\\*': 'disponibilidade'
    }

    for label, key in metricas_map.items():
        pattern = f'{label}\\s*\\|\\s*\\*?\\*?([\\d.]+)%?\\*?\\*?'
        match = re.search(pattern, content)
        if match:
            data['metricas'][key] = float(match.group(1))

    # Extrair desempenho por horário
    desempenho_section = re.search(r'## Análise de Latência por Faixa Horária.*?(?=##|\Z)', content, re.DOTALL)
    if desempenho_section:
        lines = desempenho_section.group().split('\n')
        for line in lines:
            match = re.match(r'\|\s*(\d+)h\s*\|\s*([\d.]+)\s*\(([\d.]+)-([\d.]+)\)\s*\|\s*(.+?)\s*\|', line)
            if match:
                hora = int(match.group(1))
                latencia = float(match.group(2))
                lat_min = float(match.group(3))
                lat_max = float(match.group(4))
                status_text = match.group(5).strip()

                perda_match = re.search(r'\[(\d+)\s*perda', status_text)
                perdas = int(perda_match.group(1)) if perda_match else 0
                status = status_text.split('[')[0].strip()

                data['desempenho'].append({
                    'hora': hora,
                    'latencia': latencia,
                    'lat_min': lat_min,
                    'lat_max': lat_max,
                    'status': status,
                    'perdas': perdas
                })

    return data


# ==================== GERADORES HTML ====================

def get_html_template():
    """Template HTML base"""
    return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
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
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .metric-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            border-left: 4px solid #dee2e6;
        }}

        .metric-card.primary {{ border-left-color: #3498db; }}
        .metric-card.success {{ border-left-color: #27ae60; }}
        .metric-card.warning {{ border-left-color: #f39c12; }}
        .metric-card.danger {{ border-left-color: #e74c3c; }}
        .metric-card.info {{ border-left-color: #9b59b6; }}

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

        .section-title {{
            font-size: 18px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 15px;
            margin-top: 30px;
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

        .status-otimo {{ background: #d4edda; color: #155724; }}
        .status-bom {{ background: #d1ecf1; color: #0c5460; }}
        .status-regular {{ background: #fff3cd; color: #856404; }}
        .status-ruim {{ background: #f8d7da; color: #721c24; }}

        .perda-indicator {{
            color: #e74c3c;
            font-weight: 500;
        }}

        @media (max-width: 768px) {{
            .header, .content {{ padding: 20px; }}
            .metrics-row {{ grid-template-columns: 1fr; }}
            .chart-wrapper {{ height: 250px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{titulo}</h1>
            <div class="subtitle">{subtitulo}</div>
        </div>

        <div class="content">
            {conteudo}
        </div>
    </div>

    <script>
        Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif";
        Chart.defaults.color = '#7f8c8d';
        {scripts}
    </script>
</body>
</html>
'''


def generate_html_diario(data, output_path):
    """Gera HTML para relatório diário"""
    horas = [d['hora'] for d in data['desempenho']]
    latencias = [d['latencia'] for d in data['desempenho']]
    perdas = [d['perdas'] for d in data['desempenho']]

    lat_media = sum(latencias) / len(latencias) if latencias else 0
    lat_max = max(latencias) if latencias else 0
    total_perdas = sum(perdas)

    # Métricas
    metricas = f'''
            <div class="metrics-row">
                <div class="metric-card success">
                    <div class="metric-label">Disponibilidade</div>
                    <div class="metric-value">{data['conexao']:.2f}<span class="metric-unit">%</span></div>
                    <div class="metric-status">{data['status']}</div>
                </div>

                <div class="metric-card primary">
                    <div class="metric-label">Latência Média</div>
                    <div class="metric-value">{lat_media:.1f}<span class="metric-unit">ms</span></div>
                    <div class="metric-status">Máxima: {lat_max:.1f}ms</div>
                </div>

                <div class="metric-card warning">
                    <div class="metric-label">Horários com Perda</div>
                    <div class="metric-value">{data['horarios_perda']}</div>
                    <div class="metric-status">Total de {total_perdas} perda(s)</div>
                </div>

                <div class="metric-card danger">
                    <div class="metric-label">Horários com Lentidão</div>
                    <div class="metric-value">{data['horarios_lentidao']}</div>
                    <div class="metric-status">Latência &gt; 20ms</div>
                </div>
            </div>
'''

    # Gráficos
    graficos = f'''
            <div class="chart-container">
                <div class="chart-title">Latência por Horário</div>
                <div class="chart-wrapper large">
                    <canvas id="latencyChart"></canvas>
                </div>
            </div>

            <div class="chart-container">
                <div class="chart-title">Perdas de Conexão por Horário</div>
                <div class="chart-wrapper">
                    <canvas id="lossChart"></canvas>
                </div>
            </div>
'''

    # Tabela
    tabela = '''
            <div class="section-title">Desempenho Detalhado por Horário</div>
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
        if 'Bom' in item['status']:
            status_class = 'status-bom'
        elif 'Regular' in item['status']:
            status_class = 'status-regular'
        elif 'Ruim' in item['status']:
            status_class = 'status-ruim'

        perda_text = f'<span class="perda-indicator">{item["perdas"]}</span>' if item['perdas'] > 0 else '0'

        tabela += f'''
                    <tr>
                        <td>{item['hora']:02d}h</td>
                        <td>{item['latencia']:.1f} ms</td>
                        <td>{item['lat_min']:.0f} - {item['lat_max']:.0f} ms</td>
                        <td><span class="status-badge {status_class}">{item['status']}</span></td>
                        <td>{perda_text}</td>
                    </tr>
'''

    tabela += '''
                </tbody>
            </table>
'''

    # Scripts dos gráficos
    scripts = f'''
        const latencyCtx = document.getElementById('latencyChart').getContext('2d');
        new Chart(latencyCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps([f'{h}h' for h in horas])},
                datasets: [{{
                    label: 'Latência (ms)',
                    data: {json.dumps(latencias)},
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.3,
                    pointRadius: 3,
                    pointHoverRadius: 5
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{
                        backgroundColor: 'rgba(44, 62, 80, 0.9)',
                        padding: 12
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{ color: '#ecf0f1' }},
                        ticks: {{
                            callback: function(value) {{ return value + ' ms'; }}
                        }}
                    }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});

        const lossCtx = document.getElementById('lossChart').getContext('2d');
        new Chart(lossCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps([f'{h}h' for h in horas])},
                datasets: [{{
                    label: 'Perdas',
                    data: {json.dumps(perdas)},
                    backgroundColor: function(context) {{
                        const value = context.parsed.y;
                        if (value === 0) return '#95a5a6';
                        if (value <= 2) return '#f39c12';
                        return '#e74c3c';
                    }},
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{
                        backgroundColor: 'rgba(44, 62, 80, 0.9)',
                        padding: 12,
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
                        ticks: {{ stepSize: 1 }},
                        grid: {{ color: '#ecf0f1' }}
                    }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});
'''

    html = get_html_template().format(
        title=f"Relatório AGHUSE - {data['data']}",
        titulo="Relatório de Conectividade AGHUSE",
        subtitulo=f"Análise do dia {data['data']}",
        conteudo=metricas + graficos + tabela,
        scripts=scripts
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


def generate_html_semanal(data, output_path):
    """Gera HTML para relatório semanal"""
    m = data['metricas']

    # Métricas
    metricas = f'''
            <div class="metrics-row">
                <div class="metric-card success">
                    <div class="metric-label">Disponibilidade</div>
                    <div class="metric-value">{m.get('disponibilidade', 0):.2f}<span class="metric-unit">%</span></div>
                </div>

                <div class="metric-card primary">
                    <div class="metric-label">Latência Média</div>
                    <div class="metric-value">{m.get('latencia_media', 0):.1f}<span class="metric-unit">ms</span></div>
                </div>

                <div class="metric-card info">
                    <div class="metric-label">Total de Testes</div>
                    <div class="metric-value">{int(m.get('total_testes', 0))}</div>
                </div>

                <div class="metric-card warning">
                    <div class="metric-label">Testes com Perda</div>
                    <div class="metric-value">{int(m.get('testes_com_perda', 0))}</div>
                    <div class="metric-status">{int(m.get('pacotes_perdidos', 0))} pacote(s)</div>
                </div>
            </div>
'''

    # Gráfico evolução por dia
    dias_labels = [d['data'] for d in data['dias']]
    dias_disp = [d['disponibilidade'] for d in data['dias']]
    dias_lat = [d['latencia'] for d in data['dias']]

    graficos = f'''
            <div class="chart-container">
                <div class="chart-title">Evolução Diária</div>
                <div class="chart-wrapper">
                    <canvas id="evolutionChart"></canvas>
                </div>
            </div>
'''

    # Gráfico latência por horário
    if data['desempenho']:
        horas = [d['hora'] for d in data['desempenho']]
        latencias = [d['latencia'] for d in data['desempenho']]
        perdas = [d['perdas'] for d in data['desempenho']]

        graficos += f'''
            <div class="chart-container">
                <div class="chart-title">Latência Média por Horário (Consolidado)</div>
                <div class="chart-wrapper large">
                    <canvas id="latencyChart"></canvas>
                </div>
            </div>

            <div class="chart-container">
                <div class="chart-title">Perdas por Horário (Consolidado)</div>
                <div class="chart-wrapper">
                    <canvas id="lossChart"></canvas>
                </div>
            </div>
'''

    # Scripts
    scripts = f'''
        const evolutionCtx = document.getElementById('evolutionChart').getContext('2d');
        new Chart(evolutionCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(dias_labels)},
                datasets: [{{
                    label: 'Latência (ms)',
                    data: {json.dumps(dias_lat)},
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    borderWidth: 2,
                    yAxisID: 'y',
                }}, {{
                    label: 'Disponibilidade (%)',
                    data: {json.dumps(dias_disp)},
                    borderColor: '#27ae60',
                    backgroundColor: 'rgba(39, 174, 96, 0.1)',
                    borderWidth: 2,
                    yAxisID: 'y1',
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    tooltip: {{
                        backgroundColor: 'rgba(44, 62, 80, 0.9)',
                        padding: 12
                    }}
                }},
                scales: {{
                    y: {{
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {{ display: true, text: 'Latência (ms)' }},
                        grid: {{ color: '#ecf0f1' }}
                    }},
                    y1: {{
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {{ display: true, text: 'Disponibilidade (%)' }},
                        grid: {{ drawOnChartArea: false }},
                        min: 95,
                        max: 100
                    }}
                }}
            }}
        }});
'''

    if data['desempenho']:
        scripts += f'''
        const latencyCtx = document.getElementById('latencyChart').getContext('2d');
        new Chart(latencyCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps([f'{h}h' for h in horas])},
                datasets: [{{
                    label: 'Latência Média (ms)',
                    data: {json.dumps(latencias)},
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
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
                    y: {{ beginAtZero: true, grid: {{ color: '#ecf0f1' }} }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});

        const lossCtx = document.getElementById('lossChart').getContext('2d');
        new Chart(lossCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps([f'{h}h' for h in horas])},
                datasets: [{{
                    label: 'Total de Perdas',
                    data: {json.dumps(perdas)},
                    backgroundColor: function(context) {{
                        const value = context.parsed.y;
                        if (value === 0) return '#95a5a6';
                        if (value <= 3) return '#f39c12';
                        return '#e74c3c';
                    }}
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ beginAtZero: true, grid: {{ color: '#ecf0f1' }} }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});
'''

    html = get_html_template().format(
        title=f"Relatório Semanal AGHUSE",
        titulo="Relatório Semanal - Conectividade AGHUSE",
        subtitulo=data['periodo'],
        conteudo=metricas + graficos,
        scripts=scripts
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


def generate_html_geral(data, output_path):
    """Gera HTML para relatório geral"""
    m = data['metricas']

    # Métricas
    metricas = f'''
            <div class="metrics-row">
                <div class="metric-card success">
                    <div class="metric-label">Disponibilidade Geral</div>
                    <div class="metric-value">{m.get('disponibilidade', 0):.2f}<span class="metric-unit">%</span></div>
                </div>

                <div class="metric-card info">
                    <div class="metric-label">Total de Testes</div>
                    <div class="metric-value">{int(m.get('total_testes', 0))}</div>
                    <div class="metric-status">Média: {int(m.get('media_testes_dia', 0))}/dia</div>
                </div>

                <div class="metric-card warning">
                    <div class="metric-label">Testes com Perda</div>
                    <div class="metric-value">{int(m.get('testes_com_perda', 0))}</div>
                    <div class="metric-status">{(m.get('testes_com_perda', 0) / m.get('total_testes', 1) * 100):.1f}% do total</div>
                </div>

                <div class="metric-card danger">
                    <div class="metric-label">Pacotes Perdidos</div>
                    <div class="metric-value">{int(m.get('pacotes_perdidos', 0))}</div>
                    <div class="metric-status">de {int(m.get('pacotes_enviados', 0))} enviados</div>
                </div>
            </div>
'''

    # Gráficos
    if data['desempenho']:
        horas = [d['hora'] for d in data['desempenho']]
        latencias = [d['latencia'] for d in data['desempenho']]
        perdas = [d['perdas'] for d in data['desempenho']]

        graficos = f'''
            <div class="chart-container">
                <div class="chart-title">Latência Média por Horário (Todo o Período)</div>
                <div class="chart-wrapper large">
                    <canvas id="latencyChart"></canvas>
                </div>
            </div>

            <div class="chart-container">
                <div class="chart-title">Total de Perdas por Horário</div>
                <div class="chart-wrapper">
                    <canvas id="lossChart"></canvas>
                </div>
            </div>
'''

        scripts = f'''
        const latencyCtx = document.getElementById('latencyChart').getContext('2d');
        new Chart(latencyCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps([f'{h}h' for h in horas])},
                datasets: [{{
                    label: 'Latência Média (ms)',
                    data: {json.dumps(latencias)},
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
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
                    y: {{ beginAtZero: true, grid: {{ color: '#ecf0f1' }} }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});

        const lossCtx = document.getElementById('lossChart').getContext('2d');
        new Chart(lossCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps([f'{h}h' for h in horas])},
                datasets: [{{
                    label: 'Total de Perdas',
                    data: {json.dumps(perdas)},
                    backgroundColor: function(context) {{
                        const value = context.parsed.y;
                        if (value === 0) return '#95a5a6';
                        if (value <= 3) return '#f39c12';
                        return '#e74c3c';
                    }}
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ beginAtZero: true, grid: {{ color: '#ecf0f1' }} }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});
'''
    else:
        graficos = ''
        scripts = ''

    html = get_html_template().format(
        title=f"Relatório Geral AGHUSE",
        titulo="Relatório Geral - Monitoramento AGHUSE",
        subtitulo=data['periodo'],
        conteudo=metricas + graficos,
        scripts=scripts
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


# ==================== MAIN ====================

def main():
    # Configurar encoding
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("=" * 60)
    print(" GERADOR COMPLETO DE RELATORIOS AGHUSE")
    print("=" * 60)
    print()

    # PASSO 1: Gerar relatórios MD
    print("PASSO 1/2: Processando arquivos e gerando relatorios MD...")
    print("-" * 60)

    try:
        result = subprocess.run(
            ['python', 'processar_relatorio.py'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        print(result.stdout)
        if result.returncode != 0:
            print("ERRO ao processar relatorios MD:")
            print(result.stderr)
            return 1
    except Exception as e:
        print(f"ERRO: {e}")
        return 1

    print()
    print("=" * 60)

    # PASSO 2: Gerar HTMLs
    print("PASSO 2/2: Gerando relatorios HTML visuais...")
    print("-" * 60)

    relatorios_dir = Path('relatorios')
    output_dir = Path('relatorios_html')
    output_dir.mkdir(exist_ok=True)

    # Processar relatórios diários
    relatorios_diarios = sorted(relatorios_dir.glob('RELATORIO_DIARIO_*.md'), reverse=True)
    for rel_file in relatorios_diarios:
        try:
            print(f"  Processando {rel_file.name}...")
            data = parse_relatorio_diario(rel_file)
            output_file = output_dir / rel_file.name.replace('.md', '.html')
            generate_html_diario(data, output_file)
            print(f"  [OK] {output_file.name}")
        except Exception as e:
            print(f"  [ERRO] {e}")

    # Processar relatório semanal
    rel_semanal = relatorios_dir / 'RELATORIO_SEMANAL.md'
    if rel_semanal.exists():
        try:
            print(f"  Processando RELATORIO_SEMANAL.md...")
            data = parse_relatorio_semanal(rel_semanal)
            output_file = output_dir / 'RELATORIO_SEMANAL.html'
            generate_html_semanal(data, output_file)
            print(f"  [OK] RELATORIO_SEMANAL.html")
        except Exception as e:
            print(f"  [ERRO] {e}")

    # Processar relatório geral
    rel_geral = relatorios_dir / 'RELATORIO_GERAL.md'
    if rel_geral.exists():
        try:
            print(f"  Processando RELATORIO_GERAL.md...")
            data = parse_relatorio_geral(rel_geral)
            output_file = output_dir / 'RELATORIO_GERAL.html'
            generate_html_geral(data, output_file)
            print(f"  [OK] RELATORIO_GERAL.html")
        except Exception as e:
            print(f"  [ERRO] {e}")

    print()
    print("=" * 60)
    print(" PROCESSAMENTO COMPLETO!")
    print("=" * 60)
    print()
    print("Arquivos gerados:")
    print("  - Relatorios MD -> pasta 'relatorios/'")
    print("  - Relatorios HTML -> pasta 'relatorios_html/'")
    print()

    # Perguntar se quer abrir o último relatório
    relatorios_html = sorted(output_dir.glob('RELATORIO_DIARIO_*.html'), reverse=True)
    if relatorios_html:
        print(f"Ultimo relatorio: {relatorios_html[0].name}")
        try:
            resposta = input("\nDeseja abrir o ultimo relatorio no navegador? (S/N): ")
            if resposta.lower() in ['s', 'sim', 'y', 'yes']:
                import os
                os.startfile(str(relatorios_html[0]))
                print("Abrindo relatorio...")
        except (EOFError, KeyboardInterrupt):
            print("\nFinalizando...")

    return 0


if __name__ == '__main__':
    sys.exit(main())
