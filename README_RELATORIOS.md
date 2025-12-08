# Sistema de Relatórios AGHUSE

Sistema completo para análise de conectividade AGHUSE com relatórios em Markdown e visualizações HTML.

## Como Usar

### Opção 1: Script Batch (Recomendado)

Execute o arquivo:
```
gerar_relatorios.bat
```

Isso vai:
1. Processar todos os arquivos de teste
2. Gerar relatórios MD (diário, semanal, geral)
3. Criar visualizações HTML interativas

### Opção 2: Python Direto

```bash
python gerar_relatorios_completo.py
```

### Opção 3: Apenas Processar (MD)

```bash
python processar_relatorio.py
```

## Estrutura de Arquivos

```
Analise-AGHUSE/
├── arquivos/                           # Arquivos de teste (.txt)
├── relatorios/                         # Relatórios Markdown
│   ├── RELATORIO_DIARIO_2025-12-*.md
│   ├── RELATORIO_SEMANAL.md
│   └── RELATORIO_GERAL.md
├── relatorios_html/                    # Relatórios HTML visuais
│   ├── RELATORIO_DIARIO_2025-12-*.html
│   ├── RELATORIO_SEMANAL.html
│   └── RELATORIO_GERAL.html
│
├── processar_relatorio.py              # Processa arquivos e gera MD
├── gerar_relatorios_completo.py        # Script unificado (MD + HTML)
├── gerar_relatorios.bat                # Atalho Windows
└── aghuse.bat                          # Script de coleta de dados
```

## Tipos de Relatórios

### 1. Relatório Diário
- Análise de um dia específico
- Disponibilidade, latência por hora
- Gráficos de latência e perdas
- Tabela detalhada por horário

### 2. Relatório Semanal
- Consolidado de vários dias
- Evolução diária (gráfico)
- Latência média por horário (consolidado)
- Comparação entre dias

### 3. Relatório Geral
- Visão geral do período completo
- Estatísticas totais
- Análise por horário (média geral)

## Características dos Relatórios HTML

- **Design Limpo**: Sem emojis, cores profissionais
- **Responsivo**: Funciona em desktop, tablet e mobile
- **Gráficos Interativos**: Passe o mouse para detalhes
- **Cards de Métricas**: Disponibilidade, latência, perdas, etc.
- **Exportável**: Pode salvar como PDF ou compartilhar

## Automação

Para executar automaticamente todo dia:

1. Abrir "Agendador de Tarefas" do Windows
2. Criar Nova Tarefa
3. **Acionadores**: Diário às 23:30
4. **Ações**:
   - Programa: `C:\Windows\System32\cmd.exe`
   - Argumentos: `/c "cd /d C:\Users\davi.costa\Desktop\repositorios\Analise-AGHUSE && gerar_relatorios.bat"`

## Solução de Problemas

### "Python não encontrado"
Instale Python 3.x e adicione ao PATH do sistema.

### "Nenhum relatório encontrado"
Primeiro execute `aghuse.bat` para coletar dados.

### Gráficos não aparecem
Verifique conexão com internet (Chart.js é carregado via CDN).
