# Critérios e Metodologia de Análise - Sistema AGHUSE

> **Documento de Referência**: Este documento explica todos os critérios utilizados para classificar e analisar a qualidade da conexão nos relatórios do sistema AGHUSE.

---

## 📊 Status da Disponibilidade

A **disponibilidade** mede o percentual de pacotes entregues com sucesso durante o período analisado.

| Status | Faixa | Descrição |
|--------|-------|-----------|
| **Ótimo** | ≥ 99.9% | Conexão extremamente estável, praticamente sem perdas |
| **Bom** | 99.0% - 99.9% | Conexão estável com raras interrupções |
| **Regular** | 95.0% - 99.0% | Conexão com perdas ocasionais, monitorar |
| **Ruim** | < 95.0% | Conexão instável, requer atenção imediata |

**Fórmula:**
```
Disponibilidade = [(Total de Pacotes - Pacotes Perdidos) / Total de Pacotes] × 100%
```

---

## ⚡ Classificação de Latência

**Latência** é o tempo de resposta da conexão em milissegundos (ms). Quanto menor, melhor.

| Classificação | Faixa | Descrição |
|---------------|-------|-----------|
| **Excelente** | ≤ 15ms | Baseline ideal - Resposta instantânea |
| **Boa** | 16-30ms | Ótima para uso geral e aplicações críticas |
| **Regular** | 31-50ms | Aceitável, pode haver lentidão leve em algumas aplicações |
| **Ruim** | > 50ms | Lentidão perceptível, requer análise e correção |

### Baseline Ideal
- **Referência**: 15ms
- Valor considerado ideal para sistemas críticos de saúde
- Usado como referência para cálculo de scores e anomalias

---

## 🎯 Score de Qualidade (0-10)

Score composto que avalia **latência** e **perda de pacotes** simultaneamente.

### Composição do Score
- **60%** - Componente de Latência (0-6 pontos)
- **40%** - Componente de Perda (0-4 pontos)

### Classificação

| Score | Classificação | Descrição |
|-------|---------------|-----------|
| **8.5 - 10.0** | Excelente | Qualidade superior, ideal para aplicações críticas |
| **7.0 - 8.4** | Muito Bom | Qualidade alta, adequada para uso geral |
| **5.5 - 6.9** | Bom | Qualidade satisfatória |
| **4.0 - 5.4** | Regular | Qualidade abaixo do ideal, monitorar |
| **< 4.0** | Ruim | Qualidade inadequada, requer ação |

### Cálculo do Score

**Fórmula:**
```
Score = (Score_Latência × 0.6) + (Score_Perda × 0.4)
```

**Componente Latência (0-6 pontos):**
- ≤ 15ms (baseline): 6.0 pontos
- 15-30ms: Decai linearmente de 6.0 para 3.0
- 30-45ms: Decai linearmente de 3.0 para 1.0
- > 45ms: Decai rapidamente para 0

**Componente Perda (0-4 pontos):**
- 0% perda: 4.0 pontos
- 0-2% perda: Decai linearmente de 4.0 para 3.0
- 2-5% perda: Decai linearmente de 3.0 para 1.0
- > 5% perda: Decai rapidamente para 0

---

## 📈 Horários de Pico

Períodos identificados **automaticamente** quando a latência está significativamente acima da média.

### Critérios de Detecção

| Critério | Valor | Descrição |
|----------|-------|-----------|
| **Threshold** | ≥ 10% acima da média | Latência deve estar 10% ou mais acima da média geral |
| **Duração mínima** | 3 horas consecutivas | Deve durar pelo menos 3 horas seguidas |

### Classificação por Período

- **Pico Matinal**: 8h-12h
- **Pico Vespertino**: 14h-18h
- **Pico Noturno**: 20h-6h

### Exemplo Prático
Se a média geral do dia é **50ms**, horários com **55ms ou mais** por **3 horas consecutivas** serão marcados como pico.

---

## ⚠️ Detecção de Anomalias

**Anomalias** são eventos **isolados** onde a latência está drasticamente fora do padrão esperado.

### Diferença: Pico vs. Anomalia

| Característica | Horário de Pico | Anomalia |
|----------------|-----------------|----------|
| Duração | Prolongada (3h+) | Pontual (minutos) |
| Natureza | Padrão recorrente | Evento isolado |
| Severidade | Moderada | Extrema |

### Métodos de Detecção

#### 1. Desvio Padrão (Método Estatístico)
- **Critério**: Latência > 2.5σ (desvios padrão) acima da média do horário
- **Quando usar**: Identifica outliers estatísticos

#### 2. Percentual (Método Absoluto)
- **Critério**: Latência > 200% do valor esperado para aquele horário
- **Quando usar**: Identifica picos extremos

### Níveis de Severidade

| Severidade | Desvio Padrão | Percentual | Ação |
|------------|---------------|------------|------|
| **Média** | 2.5-3.0σ | 200-300% | Monitorar |
| **Alta** 🔴 | > 3.0σ | > 300% | Investigar imediatamente |

### Exemplo Prático
- Se a média do horário 10h é normalmente **50ms**:
  - **Pico**: 55ms por 3 horas (alta demanda)
  - **Anomalia**: 150ms pontual (problema isolado)

---

## 🔬 Metodologia de Coleta de Dados

### Parâmetros de Teste

| Parâmetro | Valor | Descrição |
|-----------|-------|-----------|
| **Frequência** | A cada 5 minutos | 288 testes por dia (24h × 12 testes/hora) |
| **Protocolo** | ICMP Echo Request | Comando `ping` |
| **Pacotes/teste** | 20 pacotes | Garantir amostra estatística |
| **Timeout** | Padrão Windows | Geralmente 4 segundos |
| **Destino** | aghuse.saude.ba.gov.br | Servidor principal |

### Métricas Coletadas

1. **Latência Mínima** - Menor tempo de resposta no teste
2. **Latência Média** - Média aritmética dos pacotes respondidos
3. **Latência Máxima** - Maior tempo de resposta no teste
4. **Perda de Pacotes** - Percentual de pacotes não respondidos
5. **Timestamp** - Data/hora exata do teste

### Endpoints Comparativos

| Endpoint | IP/Host | Finalidade |
|----------|---------|------------|
| **AGHUSE** | aghuse.saude.ba.gov.br | Destino principal |
| **Interno** | 10.252.17.132 | Diagnóstico de rede local |
| **Externo** | 8.8.8.8 (Google DNS) | Diagnóstico de Internet |

---

## 📐 Fórmulas e Cálculos Detalhados

### 1. Disponibilidade
```
Disponibilidade = [(Total_Pacotes - Pacotes_Perdidos) / Total_Pacotes] × 100%

Onde:
- Total_Pacotes = Número_de_Testes × 20
- Pacotes_Perdidos = Soma das perdas em todos os testes
```

**Exemplo:**
- 288 testes/dia × 20 pacotes = 5.760 pacotes
- 58 pacotes perdidos
- Disponibilidade = [(5760 - 58) / 5760] × 100% = **98.99%**

---

### 2. Score de Qualidade
```
Score = (Score_Lat × 0.6) + (Score_Perda × 0.4)

Score_Lat (0-6):
  Se lat ≤ 15ms:
    Score_Lat = 6.0
  Se 15 < lat ≤ 30ms:
    Score_Lat = 6.0 - ((lat - 15) / 15) × 3.0
  Se 30 < lat ≤ 45ms:
    Score_Lat = 3.0 - ((lat - 30) / 15) × 2.0
  Se lat > 45ms:
    Score_Lat = max(0, 1.0 - ((lat - 45) / 15) × 0.5)

Score_Perda (0-4):
  Se perda = 0%:
    Score_Perda = 4.0
  Se 0 < perda ≤ 2%:
    Score_Perda = 4.0 - (perda / 2.0)
  Se 2 < perda ≤ 5%:
    Score_Perda = 3.0 - ((perda - 2.0) / 3.0) × 2.0
  Se perda > 5%:
    Score_Perda = max(0, 1.0 - ((perda - 5.0) / 5.0) × 0.5)
```

**Exemplo:**
- Latência = 25ms → Score_Lat = 6.0 - ((25-15)/15) × 3.0 = **4.0**
- Perda = 1% → Score_Perda = 4.0 - (1/2) = **3.5**
- **Score Final** = (4.0 × 0.6) + (3.5 × 0.4) = **3.8** (Regular)

---

### 3. Regressão Linear (Análise de Tendência)
```
y = a × x + b

Onde:
- y = latência prevista
- x = dias desde o início
- a = slope (inclinação da reta)
- b = intercept (ponto de partida)

Slope (a):
  a = [n × Σ(x×y) - Σx × Σy] / [n × Σ(x²) - (Σx)²]

Intercept (b):
  b = [Σy - a × Σx] / n

Coeficiente de Determinação (R²):
  R² = 1 - [Σ(y - ŷ)²] / [Σ(y - ȳ)²]
```

**Interpretação:**
- **R² > 0.5**: Previsão confiável
- **R² < 0.5**: Baixa confiabilidade ⚠️
- **Slope > 0.5**: Tendência de **alta** 📈
- **Slope < -0.5**: Tendência de **queda** 📉
- **-0.5 ≤ Slope ≤ 0.5**: Tendência **estável** →

---

### 4. Detecção de Anomalias (Z-Score)
```
Z-Score = (Latência_Observada - Média_do_Horário) / Desvio_Padrão_do_Horário

Se Z-Score > 2.5:
  → Anomalia detectada

Desvio Padrão:
  σ = √[Σ(x - μ)² / n]

Onde:
- σ = desvio padrão
- x = cada valor de latência
- μ = média
- n = número de amostras
```

**Exemplo:**
- Média 10h = 50ms, σ = 5ms
- Latência observada = 65ms
- Z-Score = (65 - 50) / 5 = **3.0** → Anomalia de severidade **alta** 🔴

---

## 📊 Distribuição de Latência

Histograma que mostra a frequência de latências em faixas:

| Faixa | Classificação | Ideal % |
|-------|---------------|---------|
| 0-20ms | Excelente | > 80% |
| 20-40ms | Boa | 10-20% |
| 40-60ms | Regular | < 5% |
| 60-80ms | Ruim | < 2% |
| 80+ms | Crítico | < 1% |

---

## 🔍 Análise por Dia da Semana

Identifica padrões semanais de desempenho:

```
Latência_Média_Dia = Σ(latências_do_dia) / n_testes_do_dia

Comparação vs. Média Geral:
  Diferença_% = [(Lat_Dia - Lat_Média_Geral) / Lat_Média_Geral] × 100%
```

**Critério de Confiabilidade:**
- **< 10 testes**: Dados insuficientes ⚠️
- **≥ 10 testes**: Amostra confiável

---

## 📅 Intervalos de Análise

| Relatório | Período | Atualização | Uso |
|-----------|---------|-------------|-----|
| **Diário** | 1 dia (00h-23h59) | Diário | Monitoramento operacional |
| **Semanal** | 7 dias | Toda segunda-feira | Análise de tendências |
| **Geral** | Todo histórico | Sob demanda | Visão estratégica |

---

## 🎨 Cores e Indicadores Visuais

### Status de Disponibilidade
- 🟢 Verde: Ótimo (≥99.9%)
- 🔵 Azul: Bom (99.0-99.9%)
- 🟡 Amarelo: Regular (95.0-99.0%)
- 🔴 Vermelho: Ruim (<95.0%)

### Badges de Classificação
- 🏆 Excelente: Verde escuro
- ✅ Muito Bom: Azul
- 👍 Bom: Amarelo
- ⚠️ Regular: Laranja
- ❌ Ruim: Vermelho

---

## 📚 Referências e Padrões

### SLA (Service Level Agreement) Padrões de Indústria
- **Tier 1** (99.9%): 43.2 minutos de downtime/mês
- **Tier 2** (99.5%): 3.6 horas de downtime/mês
- **Tier 3** (99.0%): 7.2 horas de downtime/mês

### Latência Recomendada (Saúde)
- **Aplicações críticas**: < 20ms
- **Sistemas gerenciais**: < 50ms
- **Internet geral**: < 100ms

---

## 🛠️ Arquivos de Configuração

Os critérios estão definidos em:
- **Arquivo**: `scripts/processar_relatorio.py`
- **Linhas**: 10-23 (Configurações de Análise Avançada)

### Valores Configuráveis

```python
# Baseline Ideal de Latência
LATENCIA_IDEAL = 15      # ms
LATENCIA_BOA = 30        # ms
LATENCIA_REGULAR = 50    # ms

# Detecção de Horários de Pico
THRESHOLD_PICO = 1.10    # 10% acima da média
MIN_DURACAO_PICO = 3     # 3 horas consecutivas

# Detecção de Anomalias
DESVIO_ANOMALIA = 2.5    # 2.5 desvios padrão
PERCENTUAL_ANOMALIA = 200  # 200% acima do horário
```

---

## 📞 Contato e Suporte

Para dúvidas sobre os critérios ou metodologia:
- **Repositório**: [Link do repositório Git]
- **Documentação**: Consulte os relatórios HTML na aba "Critérios e Metodologia"

---

**Última atualização**: 2025-12-09
**Versão do documento**: 1.0
