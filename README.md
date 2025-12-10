# Sistema de Monitoramento AGHUSE

Sistema automatizado para monitorar conectividade com o servidor AGHUSE (10.252.17.132) e gerar relatórios simplificados de disponibilidade.

## 📁 Estrutura

```
├── aghuse.bat                  # Coleta de dados (executar a cada 5 min)
├── gerar_relatorios.bat        # Gera todos os relatórios (MD + HTML)
├── index.html                  # Central de Relatórios (página inicial)
├── atualizar_index.py          # Atualiza index.html automaticamente
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
4. **Atualizar index.html automaticamente**

**Ou executar manualmente:**
```bash
# Gerar apenas relatórios MD
python scripts\processar_relatorio.py

# Gerar apenas relatórios HTML
python scripts\gerar_relatorio_visual.py

# Atualizar index.html
python atualizar_index.py
```

### 3. Visualizar Relatórios

**🎯 Central de Relatórios (Recomendado):**
Abra `index.html` no navegador - você terá:
- **Calendário interativo** com todos os relatórios diários
- Dias com relatórios disponíveis destacados em verde
- Acesso rápido aos relatórios **Geral** e **Semanal**
- Interface moderna e fácil de navegar
- **Atualização automática** ao gerar novos relatórios

**Opção 2 - Relatórios Individuais:**
Abra os arquivos `.html` na pasta `relatorios_html/` em qualquer navegador web.
- Interface visual moderna
- Gráficos interativos
- Melhor para apresentações

**Opção 3 - Markdown:**
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
- **Análises Avançadas**: Regressão linear, horários de pico, scores de qualidade
- **Detecção de Anomalias**: Eventos isolados com latência extrema
- **Análise por Dia da Semana**: Padrões semanais
- **Distribuição de Latência**: Histograma de frequências
- Horários críticos da semana
- Incidentes principais

### Relatório Geral
- Visão completa de todo o período monitorado
- Estatísticas gerais e tendências de longo prazo
- Análise preditiva (previsão 7 dias)
- Todas as análises avançadas do relatório semanal

## 📈 Como Interpretar

> **📋 Documentação Completa**: Consulte [CRITERIOS_E_METODOLOGIA.md](CRITERIOS_E_METODOLOGIA.md) para explicação detalhada de **todos os critérios, fórmulas e metodologias** utilizadas nos relatórios.

### Status de Conexão (Disponibilidade)

| Percentual | Status | Descrição |
|------------|--------|-----------|
| ≥ 99.9% | 🟢 Ótimo | Conexão extremamente estável |
| 99.0-99.9% | 🔵 Bom | Raras interrupções |
| 95.0-99.0% | 🟡 Regular | Perdas ocasionais |
| < 95.0% | 🔴 Ruim | Conexão instável |

### Tempo de Resposta (Latência)

| Tempo | Qualidade | Uso |
|-------|-----------|-----|
| ≤ 15ms | 🏆 Excelente | Baseline ideal |
| 16-30ms | 👍 Boa | Ótima para uso geral |
| 31-50ms | ⚠️ Regular | Lentidão leve |
| > 50ms | ❌ Ruim | Requer análise |

### Score de Qualidade (0-10)

Score composto: **60% Latência** + **40% Perda de Pacotes**

| Score | Classificação | Cores no Gráfico |
|-------|---------------|------------------|
| 8.5-10 | Excelente | 🟢 Verde |
| 7.0-8.4 | Muito Bom | 🔵 Azul |
| 5.5-6.9 | Bom | 🟡 Amarelo |
| 4.0-5.4 | Regular | 🟠 Laranja |
| < 4.0 | Ruim | 🔴 Vermelho |

### Conceitos Avançados

- **Horários de Pico**: Períodos com latência ≥10% acima da média por 3h+ consecutivas
- **Anomalias**: Eventos isolados com latência >2.5σ ou >200% do esperado
- **Regressão Linear**: Análise de tendência (alta/queda/estável) com previsão 7 dias
- **Distribuição**: Histograma mostrando frequência de latências em diferentes faixas

**💡 Dica**: Na página principal ([index.html](index.html)), clique no card **"Critérios e Metodologia"** para ver explicações visuais detalhadas em um modal interativo.

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

## 📚 Documentação Adicional

- **[index.html](index.html)** - Central de Relatórios com Modal de Critérios
  - Clique no card "Critérios e Metodologia" (roxo, 📋)
  - Modal interativo com 6 seções explicativas
  - Tabelas visuais, badges coloridos e exemplos
  - Acesso rápido direto da página principal

- **[CRITERIOS_E_METODOLOGIA.md](CRITERIOS_E_METODOLOGIA.md)** - Documentação Técnica Completa
  - Explicação detalhada de cada métrica
  - Fórmulas matemáticas utilizadas
  - Exemplos práticos de cálculo
  - Referências e padrões da indústria

- **[GUIA_RAPIDO_CRITERIOS.md](GUIA_RAPIDO_CRITERIOS.md)** - Referência Visual Rápida
  - Diagramas ASCII ilustrativos
  - Checklist de 3 passos
  - Comparações lado a lado

---

**Versão**: 5.1
**Atualização**: Dezembro 2025
**Mudanças**:
- ✨ **NOVO**: Modal de "Critérios e Metodologia" integrado no [index.html](index.html)
  - Card dedicado na página principal (roxo, 📋)
  - Modal interativo com 6 seções explicativas
  - Design profissional com badges coloridos e tabelas
  - Sem duplicação - removido dos relatórios individuais
- ✨ **NOVO**: Documentação completa ([CRITERIOS_E_METODOLOGIA.md](CRITERIOS_E_METODOLOGIA.md))
  - Todos os critérios, fórmulas e metodologias
  - Exemplos práticos de cálculo
  - Referências e padrões da indústria
- ✨ **NOVO**: Guia visual rápido ([GUIA_RAPIDO_CRITERIOS.md](GUIA_RAPIDO_CRITERIOS.md))
  - Diagramas ASCII ilustrativos
  - Checklist de 3 passos
- Transparência total: Todos os critérios agora visíveis e acessíveis
- Central de Relatórios com calendário interativo
- Atualização automática do index.html ao gerar relatórios
- Design consistente com tema cinza escuro em todos os relatórios
