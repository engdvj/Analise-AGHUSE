"""
Script para adicionar a seção de Critérios e Metodologia nos relatórios HTML existentes
"""
import os
import re
from pathlib import Path

# Importar funções do módulo de critérios
import sys
sys.path.insert(0, 'scripts')
from adicionar_secao_criterios import gerar_secao_criterios_html, gerar_css_criterios

def adicionar_criterios_no_html(html_path):
    """Adiciona a seção de critérios em um arquivo HTML existente"""

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Verificar se já tem a seção de critérios
    if 'id="criterios"' in html_content:
        print(f"  [SKIP] {html_path.name} - Já contém seção de critérios")
        return False

    # 1. Adicionar CSS no <style>
    css_adicional = gerar_css_criterios()
    html_content = html_content.replace('</style>', f'{css_adicional}\n    </style>')

    # 2. Adicionar botão de aba "Critérios" no menu de tabs
    # Procurar pelo último tab-button e adicionar após ele
    tab_button_criterios = '<button class="tab-button" data-tab="criterios">Critérios e Metodologia</button>'

    # Inserir antes do fechamento da div.tabs
    html_content = html_content.replace(
        '</div>\n\n            <!-- Aba 1',
        f'                {tab_button_criterios}\n            </div>\n\n            <!-- Aba 1'
    )

    # Caso alternativo - inserir após o último tab-button
    if tab_button_criterios not in html_content:
        match = re.search(r'(<button class="tab-button"[^>]*>[^<]+</button>)(\s*</div>)', html_content)
        if match:
            html_content = html_content.replace(
                match.group(0),
                f'{match.group(1)}\n                {tab_button_criterios}{match.group(2)}'
            )

    # 3. Adicionar conteúdo da seção de critérios
    secao_criterios = gerar_secao_criterios_html()

    # Inserir antes do fechamento da div.content
    html_content = html_content.replace(
        '</div>\n    </div>\n\n    <script>',
        f'{secao_criterios}\n        </div>\n    </div>\n\n    <script>'
    )

    # 4. Salvar arquivo modificado
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return True

def processar_todos_relatorios():
    """Processa todos os relatórios HTML na pasta relatorios_html"""
    relatorios_dir = Path('relatorios_html')

    if not relatorios_dir.exists():
        print(f"Pasta {relatorios_dir} não encontrada!")
        return

    arquivos_html = list(relatorios_dir.glob('*.html'))

    if not arquivos_html:
        print("Nenhum arquivo HTML encontrado!")
        return

    print(f"Encontrados {len(arquivos_html)} relatórios HTML\n")

    processados = 0
    for html_file in sorted(arquivos_html):
        try:
            # Processar apenas relatórios SEMANAL e GERAL (que têm abas)
            if 'SEMANAL' in html_file.name or 'GERAL' in html_file.name:
                print(f"Processando: {html_file.name}...")
                if adicionar_criterios_no_html(html_file):
                    processados += 1
                    print(f"  [OK] Seção adicionada com sucesso!")
            else:
                print(f"  [SKIP] {html_file.name} - Relatório diário (sem abas)")
        except Exception as e:
            print(f"  [ERRO] {html_file.name}: {e}")

    print(f"\n{'='*60}")
    print(f"Processamento concluído!")
    print(f"Total processado: {processados}/{len([f for f in arquivos_html if 'SEMANAL' in f.name or 'GERAL' in f.name])} relatórios")
    print(f"{'='*60}")

if __name__ == '__main__':
    print("=" * 60)
    print("Adicionando Seção de Critérios e Metodologia")
    print("=" * 60)
    print()

    processar_todos_relatorios()

    print("\nPróximos passos:")
    print("1. Abra um relatório semanal ou geral no navegador")
    print("2. Clique na nova aba 'Critérios e Metodologia'")
    print("3. Verifique se a documentação está clara e completa")
