"""
Script para atualizar o index.html com lista dinâmica de relatórios semanais
"""
import os
import re
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
                'periodo': f"{data_inicio} a {data_fim}",
                'data_inicio': datetime.strptime(data_inicio, '%d-%m-%Y')
            })

    return relatorios


def gerar_html_semanais(relatorios):
    """Gera HTML para dropdown de relatórios semanais"""
    if not relatorios:
        return '''
                <div class="action-card warning">
                    <div class="action-card-icon">📅</div>
                    <h3>Relatórios Semanais</h3>
                    <p>Nenhum relatório semanal disponível</p>
                </div>
'''

    # Relatório mais recente
    mais_recente = relatorios[0]

    html = f'''
                <div class="dropdown-container">
                    <a href="relatorios_html/{mais_recente['arquivo']}" class="action-card warning">
                        <div class="action-card-icon">📅</div>
                        <h3>Relatório Semanal</h3>
                        <p>{mais_recente['periodo']}</p>
                    </a>
'''

    # Se houver mais de um relatório, adicionar dropdown
    if len(relatorios) > 1:
        html += '''
                    <div class="dropdown-toggle" onclick="toggleDropdown('semanais')">
                        Ver semanas anteriores ▼
                    </div>
                    <div class="dropdown-list" id="semanais-dropdown" style="display: none;">
'''
        for rel in relatorios[1:]:  # Pular o primeiro (já está no link principal)
            html += f'''
                        <a href="relatorios_html/{rel['arquivo']}" class="dropdown-item">
                            Semana de {rel['periodo']}
                        </a>
'''
        html += '''
                    </div>
'''

    html += '''
                </div>
'''

    return html


def atualizar_index():
    """Atualiza o index.html com lista de relatórios semanais"""
    index_path = Path('index.html')

    if not index_path.exists():
        print("[ERRO] index.html não encontrado!")
        return

    # Ler index atual
    with open(index_path, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Listar relatórios
    relatorios = listar_relatorios_semanais()
    print(f"Encontrados {len(relatorios)} relatórios semanais")

    # Gerar novo HTML
    novo_html = gerar_html_semanais(relatorios)

    # Substituir seção de relatório semanal
    # Procurar pela div dropdown-container que contém relatórios semanais
    # O padrão captura desde <div class="dropdown-container"> até o </div> correspondente
    padrao = r'<div class="dropdown-container">.*?<a href="relatorios_html/RELATORIO_SEMANAL.*?</a>\s*</div>'

    if re.search(padrao, conteudo, re.DOTALL):
        conteudo = re.sub(padrao, novo_html.strip(), conteudo, flags=re.DOTALL)
    else:
        print("[AVISO] Padrão não encontrado no index.html")
        return

    # Adicionar CSS para dropdown se não existir
    if '.dropdown-container' not in conteudo:
        css_dropdown = '''
        .dropdown-container {
            position: relative;
            width: 100%;
        }

        .dropdown-toggle {
            margin-top: 10px;
            padding: 8px 12px;
            background: #3498db;
            color: white;
            border-radius: 4px;
            font-size: 13px;
            cursor: pointer;
            text-align: center;
            transition: all 0.2s ease;
        }

        .dropdown-toggle:hover {
            background: #2980b9;
        }

        .dropdown-list {
            margin-top: 10px;
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            overflow: hidden;
            max-height: 300px;
            overflow-y: auto;
        }

        .dropdown-item {
            display: block;
            padding: 12px 15px;
            text-decoration: none;
            color: #2c3e50;
            border-bottom: 1px solid #ecf0f1;
            font-size: 13px;
            transition: all 0.2s ease;
        }

        .dropdown-item:last-child {
            border-bottom: none;
        }

        .dropdown-item:hover {
            background: #f8f9fa;
            color: #3498db;
        }
'''
        # Inserir CSS antes do </style>
        conteudo = conteudo.replace('</style>', css_dropdown + '    </style>')

    # Adicionar JavaScript para toggle se não existir
    if 'function toggleDropdown' not in conteudo:
        js_dropdown = '''
    <script>
        function toggleDropdown(id) {
            const dropdown = document.getElementById(id + '-dropdown');
            const toggle = dropdown.previousElementSibling;

            if (dropdown.style.display === 'none' || dropdown.style.display === '') {
                dropdown.style.display = 'block';
                toggle.textContent = toggle.textContent.replace('▼', '▲');
            } else {
                dropdown.style.display = 'none';
                toggle.textContent = toggle.textContent.replace('▲', '▼');
            }
        }
    </script>
'''
        # Inserir JS antes do </body>
        conteudo = conteudo.replace('</body>', js_dropdown + '</body>')

    # Salvar index atualizado
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(conteudo)

    print(f"[OK] index.html atualizado com {len(relatorios)} relatórios semanais")


if __name__ == '__main__':
    atualizar_index()
