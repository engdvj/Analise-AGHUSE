"""
Script para remover a seção de Critérios e Metodologia dos relatórios HTML
Agora que está centralizado no index.html, não precisa mais nos relatórios individuais
"""
import os
import re
from pathlib import Path

def remover_criterios_do_html(html_path):
    """Remove a aba e conteúdo de critérios de um arquivo HTML"""

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Verificar se tem a seção de critérios
    if 'id="criterios"' not in html_content:
        print(f"  [SKIP] {html_path.name} - Não contém seção de critérios")
        return False

    # 1. Remover o botão da aba "Critérios e Metodologia"
    html_content = re.sub(
        r'\s*<button class="tab-button" data-tab="criterios">.*?</button>',
        '',
        html_content,
        flags=re.DOTALL
    )

    # 2. Remover todo o conteúdo da aba de critérios
    # Procurar desde <!-- Aba X: até o próximo </div> que fecha a tab-content
    html_content = re.sub(
        r'<!-- Aba \d+: Critérios e Metodologia -->.*?<div class="tab-content" id="criterios">.*?</div>\s*</div>\s*</div>',
        '',
        html_content,
        flags=re.DOTALL
    )

    # Caso alternativo - remover diretamente a div com id="criterios"
    html_content = re.sub(
        r'<div class="tab-content" id="criterios">.*?</div>\s*</div>',
        '',
        html_content,
        flags=re.DOTALL
    )

    # 3. Remover CSS específico de critérios (se existir)
    css_patterns = [
        r'\.criteria-section\s*\{[^}]*\}',
        r'\.criteria-table\s*\{[^}]*\}',
        r'\.criteria-row\s*\{[^}]*\}',
        r'\.criteria-status\s*\{[^}]*\}',
        r'\.criteria-value\s*\{[^}]*\}',
        r'\.criteria-desc\s*\{[^}]*\}',
        r'\.criteria-note\s*\{[^}]*\}',
        r'\.formula\s*\{[^}]*\}'
    ]

    for pattern in css_patterns:
        html_content = re.sub(pattern, '', html_content, flags=re.DOTALL)

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
                if remover_criterios_do_html(html_file):
                    processados += 1
                    print(f"  [OK] Seção removida com sucesso!")
            else:
                print(f"  [SKIP] {html_file.name} - Relatório diário (sem abas)")
        except Exception as e:
            print(f"  [ERRO] {html_file.name}: {e}")

    print(f"\n{'='*60}")
    print(f"Processamento concluído!")
    print(f"Total processado: {processados} relatórios")
    print(f"{'='*60}")

if __name__ == '__main__':
    print("=" * 60)
    print("Removendo Seção de Critérios dos Relatórios HTML")
    print("(Agora centralizado no index.html)")
    print("=" * 60)
    print()

    processar_todos_relatorios()

    print("\n✅ Seção de Critérios agora está apenas no index.html!")
    print("💡 Abra index.html e clique no card 'Critérios e Metodologia'")
