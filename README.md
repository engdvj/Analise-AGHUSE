# Sistema de Monitoramento AGHUSE

Sistema automatizado para monitorar conectividade com o servidor AGHUSE (10.252.17.132) e gerar relatórios simplificados de disponibilidade.

## 📁 Estrutura

```
├── aghuse.bat                  # Coleta de dados (executar a cada 5 min)
├── gerar_relatorios.bat        # Gera todos os relatórios (MD + HTML)
├── scripts/                    # Scripts Python
│   ├── processar_relatorio.py       # Processa dados e gera MD
│   └── gerar_relatorio_visual.py    # Gera relatórios HTML
├── arquivos/                   # Dados de testes (.txt)
│   ├── 2025-12-03/            # Arquivos organizados por dia
│   ├── 2025-12-04/
│   └── ...
├── relatorios/                 # Relatórios Markdown (.md)
│   ├── RELATORIO_DIARIO_*.md
│   ├── RELATORIO_SEMANAL.md
│   └── RELATORIO_GERAL.md
└── relatorios_html/            # Relatórios HTML visuais
    ├── RELATORIO_DIARIO_*.html
    ├── RELATORIO_SEMANAL.html
    └── RELATORIO_GERAL.html
```

## 🚀 Como Usar

### 1. Coletar Dados

Execute `aghuse.bat` a cada 5 minutos (manualmente ou via Agendador de Tarefas):
- Testa conectividade com AGHUSE
- Salva resultados em `arquivos/YYYY-MM-DD/`

### 2. Gerar Relatórios

**Executar tudo de uma vez (recomendado):**

Duplo clique em `gerar_relatorios.bat` - isso irá:
1. Processar todos os arquivos de teste
2. Gerar relatórios Markdown (diários, semanal e geral)
3. Criar relatórios HTML visuais e interativos

**Ou executar manualmente:**
```bash
# Gerar apenas relatórios MD
python scripts\processar_relatorio.py

# Gerar apenas relatórios HTML
python scripts\gerar_relatorio_visual.py
```

### 3. Visualizar Relatórios

**Opção 1 - HTML Visual (Recomendado):**
Abra os arquivos `.html` na pasta `relatorios_html/` em qualquer navegador web.
- Interface visual moderna
- Gráficos interativos
- Melhor para apresentações

**Opção 2 - Markdown:**
Abra os arquivos `.md` na pasta `relatorios/` com qualquer editor de texto ou visualizador Markdown.
- Formato texto
- Fácil de copiar/compartilhar
- Melhor para documentação

## 📊 O que os Relatórios Mostram

### Relatório Diário
- **Status geral** da conexão do dia
- **Desempenho por horário** (tabela e gráfico)
- **Análise técnica** (tempo de resposta, estabilidade)
- **Comparativo** entre AGHUSE, rede interna e internet
- **Detalhes de problemas** (perdas de pacotes, horários com lentidão)

### Relatório Semanal
- Consolidação dos últimos 7 dias
- Análise por dia
- Horários críticos da semana
- Incidentes principais

### Relatório Geral
- Visão completa de todo o período monitorado
- Estatísticas gerais
- Tendências e padrões

## 📈 Como Interpretar

### Status de Conexão

| Percentual | Status |
|------------|--------|
| ≥ 99.9% | Ótimo |
| ≥ 99.0% | Bom |
| ≥ 95.0% | Regular |
| < 95.0% | Ruim |

### Tempo de Resposta (Latência)

| Tempo | Qualidade |
|-------|-----------|
| < 10ms | Ótimo |
| < 20ms | Bom |
| < 50ms | Regular |
| ≥ 50ms | Ruim |

### Estabilidade

Mede a variação do tempo de resposta:
- **Ótimo/Bom**: Conexão estável
- **Regular/Ruim**: Conexão instável, com oscilações

## 🔧 Requisitos

- Windows
- Python 3.6+
- Conectividade de rede

## ❓ Problemas Comuns

**"Python não encontrado"**
→ Instale Python e adicione ao PATH

**"Total de arquivos processados: 0"**
→ Execute `aghuse.bat` para gerar dados primeiro

**Relatórios vazios**
→ Verifique se há arquivos `.txt` em `arquivos/`

## 📝 Observações

- Os dados são coletados a cada 5 minutos, mas organizados e apresentados por hora nos relatórios
- Arquivos são salvos em subpastas por data: `arquivos/YYYY-MM-DD/`
- Relatórios são gerados em formato Markdown (`.md`) para fácil leitura
- Recomenda-se manter dados dos últimos 30 dias para análise de tendências

---

**Versão**: 3.0
**Atualização**: Dezembro 2025
**Mudanças**:
- Estrutura de diretórios otimizada (scripts organizados em pasta separada)
- Geração automatizada de relatórios HTML visuais
- Script único `gerar_relatorios.bat` para gerar tudo
- Suporte para relatórios semanal e geral em HTML
