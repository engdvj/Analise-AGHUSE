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

    # Extrair desempenho por horário
    desempenho_section = re.search(r'## Desempenho por Horário.*?(?=\*\*Gráfico|\Z)', content, re.DOTALL)
    if desempenho_section:
        lines = desempenho_section.group().split('\n')
        for line in lines:
            # Regex mais flexível para capturar a linha
            match = re.match(r'\|\s*(\d+)h\s*\|\s*([\d.]+)\s*\(([\d.]+)-([\d.]+)\)\s*\|\s*(.+?)\s*\|', line)
            if match:
                hora = int(match.group(1))
                latencia = float(match.group(2))
                lat_min = float(match.group(3))
                lat_max = float(match.group(4))
                status_text = match.group(5).strip()

                # Extrair status e perdas
                perda_match = re.search(r'\[(\d+)\s*perda', status_text)
                perdas = int(perda_match.group(1)) if perda_match else 0

                # Remover a parte de perdas do status
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
        'horarios': []
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
            match = re.match(r'\|\s*(\d{2}/\d{2}/\d{4})\s*\|\s*(\d+)\s*\|.*?\|\s*\d+\s*\|\s*([\d.]+)%\s*\|\s*([\d.]+)ms', line)
            if match:
                data['dias'].append({
                    'data': match.group(1),
                    'testes': int(match.group(2)),
                    'disponibilidade': float(match.group(3)),
                    'latencia': float(match.group(4))
                })

    # Se latência média não foi encontrada no sumário, calcular a partir dos dias (média ponderada)
    if data['latencia_media'] == 0.0 and data['dias']:
        total_latencia_ponderada = sum(d['latencia'] * d['testes'] for d in data['dias'])
        total_testes = sum(d['testes'] for d in data['dias'])
        data['latencia_media'] = total_latencia_ponderada / total_testes if total_testes > 0 else 0.0

    # Extrair latência por horário
    horario_section = re.search(r'## Análise de Latência por Faixa Horária.*?\n\|.*?\n\|---.*?\n((?:\|.*?\n)+)', content, re.DOTALL)
    if horario_section:
        for line in horario_section.group(1).strip().split('\n'):
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

                data['horarios'].append({
                    'hora': hora,
                    'latencia': latencia,
                    'lat_min': lat_min,
                    'lat_max': lat_max,
                    'status': status,
                    'perdas': perdas
                })

    return data


def generate_html_semanal(data, output_path):
    """Gera HTML visual para relatório semanal com gráficos"""

    # Preparar dados para gráficos
    dias_labels = [d['data'] for d in data['dias']]
    dias_disp = [d['disponibilidade'] for d in data['dias']]
    dias_lat = [d['latencia'] for d in data['dias']]

    horas_labels = [f"{h['hora']:02d}h" for h in data['horarios']]
    horas_lat = [h['latencia'] for h in data['horarios']]
    horas_perdas = [h['perdas'] for h in data['horarios']]

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
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            border-left: 4px solid #3498db;
        }}
        .metric-card.success {{ border-left-color: #27ae60; }}
        .metric-card.warning {{ border-left-color: #f39c12; }}
        .metric-card.danger {{ border-left-color: #e74c3c; }}
        .metric-label {{
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #7f8c8d;
            margin-bottom: 8px;
        }}
        .metric-value {{
            font-size: 32px;
            font-weight: 600;
            color: #2c3e50;
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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Relatório Semanal - Monitoramento AGHUSE</h1>
            <div class="subtitle">Período: {data['periodo']}</div>
        </div>

        <div class="content">
            <div class="metrics-row">
                <div class="metric-card success">
                    <div class="metric-label">Disponibilidade</div>
                    <div class="metric-value">{data['disponibilidade']:.2f}<span class="metric-unit">%</span></div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Latência Média</div>
                    <div class="metric-value">{data['latencia_media']:.1f}<span class="metric-unit">ms</span></div>
                </div>
                <div class="metric-card warning">
                    <div class="metric-label">Total de Testes</div>
                    <div class="metric-value">{data['total_testes']}</div>
                </div>
                <div class="metric-card danger">
                    <div class="metric-label">Testes com Perda</div>
                    <div class="metric-value">{data['testes_com_perda']}</div>
                </div>
            </div>

            <div class="chart-container">
                <div class="chart-title">Evolução da Disponibilidade por Dia</div>
                <div class="chart-wrapper">
                    <canvas id="dispChart"></canvas>
                </div>
            </div>

            <div class="chart-container">
                <div class="chart-title">Evolução da Latência por Dia</div>
                <div class="chart-wrapper">
                    <canvas id="latDiaChart"></canvas>
                </div>
            </div>

            <div class="chart-container">
                <div class="chart-title">Latência Média por Horário (Todo o Período)</div>
                <div class="chart-wrapper">
                    <canvas id="latHoraChart"></canvas>
                </div>
            </div>

            <div class="chart-container">
                <div class="chart-title">Perdas por Horário</div>
                <div class="chart-wrapper">
                    <canvas id="perdasChart"></canvas>
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
                datasets: [{{
                    label: 'Latência (ms)',
                    data: {json.dumps(dias_lat)},
                    backgroundColor: '#3498db',
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{ y: {{ beginAtZero: true }} }}
            }}
        }});

        // Gráfico de Latência por Horário
        new Chart(document.getElementById('latHoraChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(horas_labels)},
                datasets: [{{
                    label: 'Latência (ms)',
                    data: {json.dumps(horas_lat)},
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
                scales: {{ y: {{ beginAtZero: true }} }}
            }}
        }});

        // Gráfico de Perdas por Horário
        new Chart(document.getElementById('perdasChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(horas_labels)},
                datasets: [{{
                    label: 'Perdas',
                    data: {json.dumps(horas_perdas)},
                    backgroundColor: function(context) {{
                        const value = context.parsed.y;
                        if (value === 0) return '#95a5a6';
                        if (value <= 5) return '#f39c12';
                        return '#e74c3c';
                    }},
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{ y: {{ beginAtZero: true, ticks: {{ stepSize: 1 }} }} }}
            }}
        }});
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

    # Preparar dados para gráficos
    horas = [d['hora'] for d in data['desempenho']]
    latencias = [d['latencia'] for d in data['desempenho']]
    perdas = [d['perdas'] for d in data['desempenho']]

    # Calcular estatísticas
    lat_media = sum(latencias) / len(latencias) if latencias else 0
    lat_max = max(latencias) if latencias else 0
    total_perdas = sum(perdas)

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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Relatório de Conectividade AGHUSE</h1>
            <div class="subtitle">Análise do dia {data['data']}</div>
        </div>

        <div class="content">
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
                    <div class="metric-status">Latência > 20ms</div>
                </div>
            </div>

            <div class="charts-section">
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
            </div>

            <div class="table-section">
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
        if item['status'] == 'Bom':
            status_class = 'status-bom'
        elif item['status'] == 'Regular':
            status_class = 'status-regular'
        elif item['status'] == 'Ruim':
            status_class = 'status-ruim'

        perda_text = f'<span class="perda-indicator">{item["perdas"]}</span>' if item['perdas'] > 0 else '0'

        html_content += f'''
                        <tr>
                            <td>{item['hora']:02d}h</td>
                            <td>{item['latencia']:.1f} ms</td>
                            <td>{item['lat_min']:.0f} - {item['lat_max']:.0f} ms</td>
                            <td><span class="status-badge {status_class}">{item['status']}</span></td>
                            <td>{perda_text}</td>
                        </tr>
'''

    html_content += f'''
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif";
        Chart.defaults.color = '#7f8c8d';

        // Gráfico de Latência
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
                    legend: {{
                        display: false
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

        // Gráfico de Perdas
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
                    legend: {{
                        display: false
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
        # Processar todos os relatórios (diários, semanal e geral)
        relatorios_diarios = sorted(relatorios_dir.glob('RELATORIO_DIARIO_*.md'), reverse=True)
        relatorio_semanal = relatorios_dir / 'RELATORIO_SEMANAL.md'
        relatorio_geral = relatorios_dir / 'RELATORIO_GERAL.md'

        todos_relatorios = list(relatorios_diarios)
        if relatorio_semanal.exists():
            todos_relatorios.append(relatorio_semanal)
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
