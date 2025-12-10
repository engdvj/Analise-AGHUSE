# Relatório Semanal - Monitoramento de Conectividade AGHUSE
**Período**: 07/12/2025 a 13/12/2025

## Sumário Executivo

| Métrica | Valor |
|---------|-------|
| Total de Testes Executados | 993 |
| Testes sem Perda | 884 |
| Testes com Perda | 109 |
| Total de Pacotes Enviados | 19860 |
| Total de Pacotes Perdidos | 131 |
| **Disponibilidade** | **99.34%** |
| Latência Média | 53.4ms |
| Latência Mín/Máx | 46/282ms |

## Análise por Dia

| Data | Testes | Sem Perda / Com Perda | Pacotes Perdidos | Disponibilidade | AGHUSE (ms) | Rede Externa (ms) |
|------|--------|-----------------------|------------------|-----------------|-------------|-------------------|
| 07/12/2025 | 286 | 275 / 11 | 14 | 99.76% | 53.9ms | 35.0ms |
| 08/12/2025 | 288 | 254 / 34 | 40 | 99.31% | 51.1ms | 42.1ms |
| 09/12/2025 | 287 | 239 / 48 | 57 | 99.01% | 55.5ms | 50.0ms |
| 10/12/2025 | 132 | 116 / 16 | 20 | 99.24% | 52.9ms | 49.7ms |
| 11/12/2025 | - | - | - | - | - | - |
| 12/12/2025 | - | - | - | - | - | - |
| 13/12/2025 | - | - | - | - | - | - |

## Análise de Latência por Faixa Horária

> **Nota**: Esta análise consolida todos os testes realizados em cada faixa horária
> ao longo do período completo (07/12/2025 a 13/12/2025).
> Cada linha representa a média de todos os testes naquela hora em todos os dias.

| Horário | AGHUSE (ms) | Rede Externa (ms) | Status |
|---------|-------------|-------------------|--------|
| 00h | 51.6 (48-77) | 39.7 (30-51) | Regular |
| 01h | 50.7 (48-55) | 39.0 (30-51) | Regular [AG:2pkt] |
| 02h | 50.8 (48-55) | 39.0 (30-50) | Regular [EX:1pkt] |
| 03h | 50.8 (48-56) | 39.0 (30-50) | Regular [AG:3pkt, EX:1pkt] |
| 04h | 50.7 (48-56) | 38.9 (30-49) | Regular [AG:1pkt] |
| 05h | 50.7 (48-55) | 39.0 (30-49) | Regular |
| 06h | 53.7 (49-71) | 38.2 (30-50) | Regular [AG:1pkt, EX:1pkt] |
| 07h | 53.3 (49-70) | 40.9 (30-82) | Ruim [AG:3pkt, EX:5pkt] |
| 08h | 53.2 (49-60) | 44.7 (34-72) | Ruim [AG:6pkt, EX:6pkt] |
| 09h | 53.7 (49-60) | 52.1 (34-100) | Ruim [AG:11pkt, EX:5pkt] |
| 10h | 53.8 (49-67) | 49.6 (36-127) | Ruim [AG:15pkt, EX:1pkt] |
| 11h | 54.7 (49-69) | 44.1 (36-71) | Ruim [AG:8pkt, EX:1pkt] |
| 12h | 58.0 (49-69) | 43.3 (36-55) | Ruim [AG:6pkt, EX:3pkt] |
| 13h | 61.3 (49-80) | 41.4 (36-56) | Ruim [AG:11pkt, EX:4pkt] |
| 14h | 56.8 (48-76) | 41.9 (36-56) | Ruim [AG:5pkt, EX:5pkt] |
| 15h | 55.6 (48-73) | 42.4 (36-76) | Ruim [AG:5pkt, EX:2pkt] |
| 16h | 54.8 (47-71) | 42.7 (34-59) | Ruim [AG:4pkt, EX:3pkt] |
| 17h | 51.3 (48-71) | 43.2 (34-70) | Regular [AG:2pkt, EX:1pkt] |
| 18h | 52.9 (48-65) | 46.9 (33-79) | Ruim [AG:3pkt, EX:1pkt] |
| 19h | 54.3 (51-70) | 49.7 (33-81) | Regular [AG:1pkt, EX:1pkt] |
| 20h | 53.7 (51-58) | 48.6 (33-66) | Regular [AG:2pkt, EX:1pkt] |
| 21h | 53.7 (51-59) | 48.9 (33-65) | Regular [EX:1pkt] |
| 22h | 52.0 (48-58) | 48.8 (33-63) | Regular [AG:1pkt, EX:1pkt] |
| 23h | 49.6 (48-54) | 45.4 (33-72) | Regular [AG:2pkt, EX:1pkt] |

**Gráfico Comparativo de Latência:**

```
AGHUSE vs Rede Externa
00h │AG: ██████████████████████████████ 51.6ms
     │EX: ███████████████████████ 39.7ms
01h │AG: ██████████████████████████████ 50.7ms
     │EX: ███████████████████████ 39.0ms
02h │AG: ██████████████████████████████ 50.8ms
     │EX: ███████████████████████ 39.0ms
03h │AG: ██████████████████████████████ 50.8ms
     │EX: ██████████████████████ 39.0ms
04h │AG: ██████████████████████████████ 50.7ms
     │EX: ███████████████████████ 38.9ms
05h │AG: ██████████████████████████████ 50.7ms
     │EX: ███████████████████████ 39.0ms
06h │AG: ██████████████████████████████ 53.7ms
     │EX: █████████████████████ 38.2ms
07h │AG: ██████████████████████████████ 53.3ms
     │EX: ███████████████████████ 40.9ms
08h │AG: ██████████████████████████████ 53.2ms
     │EX: █████████████████████████ 44.7ms
09h │AG: ██████████████████████████████ 53.7ms
     │EX: █████████████████████████████ 52.1ms
10h │AG: ██████████████████████████████ 53.8ms
     │EX: ███████████████████████████ 49.6ms
11h │AG: ██████████████████████████████ 54.7ms
     │EX: ████████████████████████ 44.1ms
12h │AG: ██████████████████████████████ 58.0ms
     │EX: ██████████████████████ 43.3ms
13h │AG: ██████████████████████████████ 61.3ms
     │EX: ████████████████████ 41.4ms
14h │AG: ██████████████████████████████ 56.8ms
     │EX: ██████████████████████ 41.9ms
15h │AG: ██████████████████████████████ 55.6ms
     │EX: ██████████████████████ 42.4ms
16h │AG: ██████████████████████████████ 54.8ms
     │EX: ███████████████████████ 42.7ms
17h │AG: ██████████████████████████████ 51.3ms
     │EX: █████████████████████████ 43.2ms
18h │AG: ██████████████████████████████ 52.9ms
     │EX: ██████████████████████████ 46.9ms
19h │AG: ██████████████████████████████ 54.3ms
     │EX: ███████████████████████████ 49.7ms
20h │AG: ██████████████████████████████ 53.7ms
     │EX: ███████████████████████████ 48.6ms
21h │AG: ██████████████████████████████ 53.7ms
     │EX: ███████████████████████████ 48.9ms
22h │AG: ██████████████████████████████ 52.0ms
     │EX: ████████████████████████████ 48.8ms
23h │AG: ██████████████████████████████ 49.6ms
     │EX: ███████████████████████████ 45.4ms
```

## Análise de Horários Críticos

### Distribuição de Perda de Pacotes por Horário

| Faixa Horária | Ocorrências | Porcentagem do Total |
|---------------|-------------|---------------------|
| 09:00 - 09:59 | 19 | 17.4% |
| 10:00 - 10:59 | 18 | 16.5% |
| 13:00 - 13:59 | 9 | 8.3% |
| 11:00 - 11:59 | 7 | 6.4% |
| 15:00 - 15:59 | 6 | 5.5% |
| 12:00 - 12:59 | 5 | 4.6% |
| 18:00 - 18:59 | 5 | 4.6% |
| 07:00 - 07:59 | 5 | 4.6% |
| 08:00 - 08:59 | 5 | 4.6% |
| 14:00 - 14:59 | 5 | 4.6% |
| 06:00 - 06:59 | 4 | 3.7% |
| 22:00 - 22:59 | 4 | 3.7% |
| 20:00 - 20:59 | 3 | 2.8% |
| 23:00 - 23:59 | 3 | 2.8% |
| 03:00 - 03:59 | 3 | 2.8% |
| 21:00 - 21:59 | 2 | 1.8% |
| 19:00 - 19:59 | 1 | 0.9% |
| 04:00 - 04:59 | 1 | 0.9% |
| 16:00 - 16:59 | 1 | 0.9% |
| 17:00 - 17:59 | 1 | 0.9% |
| 00:00 - 00:59 | 1 | 0.9% |
| 01:00 - 01:59 | 1 | 0.9% |

### Distribuição de Latência Elevada (>20ms) por Horário

| Faixa Horária | Ocorrências |
|---------------|-------------|
| 00:00 - 00:59 | 48 |
| 01:00 - 01:59 | 48 |
| 02:00 - 02:59 | 48 |
| 03:00 - 03:59 | 48 |
| 04:00 - 04:59 | 48 |
| 05:00 - 05:59 | 48 |
| 06:00 - 06:59 | 48 |
| 07:00 - 07:59 | 48 |
| 08:00 - 08:59 | 48 |
| 10:00 - 10:59 | 48 |

## Registro de Incidentes

Total de 109 teste(s) com perda de pacotes:

| Data | Horário | Latência (ms) | Perda (%) |
|------|---------|---------------|----------|
| 07/12 | 06:24:00 | 54 | 5 |
| 07/12 | 09:39:00 | 55 | 5 |
| 07/12 | 10:14:01 | 55 | 10 |
| 07/12 | 10:19:01 | 54 | 5 |
| 07/12 | 11:04:01 | 54 | 5 |
| 07/12 | 12:29:00 | 54 | 5 |
| 07/12 | 13:24:00 | 54 | 5 |
| 07/12 | 15:49:00 | 49 | 5 |
| 07/12 | 18:19:00 | 55 | 15 |
| 07/12 | 19:34:00 | 58 | 5 |
| 07/12 | 20:59:01 | 58 | 5 |
| 08/12 | 06:49:01 | 51 | 5 |
| 08/12 | 07:19:01 | 49 | 5 |
| 08/12 | 07:24:01 | 49 | 5 |
| 08/12 | 07:44:01 | 49 | 5 |
| 08/12 | 08:09:01 | 53 | 5 |
| 08/12 | 08:59:01 | 54 | 5 |
| 08/12 | 09:09:01 | 52 | 10 |
| 08/12 | 09:14:01 | 54 | 5 |
| 08/12 | 09:34:00 | 54 | 5 |

*Exibindo 20 de 109 incidentes. Consulte relatórios diários para detalhes completos.*

## Score de Qualidade por Horário

| Horário | Score | Classificação | Componente Latência | Componente Perda |
|---------|-------|---------------|---------------------|------------------|
| 00h | 3.7 | Ruim | 0.8 | 2.9 |
| 01h | 3.8 | Ruim | 0.8 | 2.9 |
| 02h | 4.8 | Regular | 0.8 | 4.0 |
| 03h | 1.7 | Ruim | 0.8 | 0.9 |
| 04h | 3.8 | Ruim | 0.8 | 2.9 |
| 05h | 4.8 | Regular | 0.8 | 4.0 |
| 06h | 1.4 | Ruim | 0.7 | 0.7 |
| 07h | 1.2 | Ruim | 0.7 | 0.5 |
| 08h | 1.2 | Ruim | 0.7 | 0.5 |
| 09h | 0.7 | Ruim | 0.7 | 0 |
| 10h | 0.7 | Ruim | 0.7 | 0 |
| 11h | 0.7 | Ruim | 0.7 | 0 |
| 12h | 0.7 | Ruim | 0.6 | 0.1 |
| 13h | 0.5 | Ruim | 0.5 | 0 |
| 14h | 0.7 | Ruim | 0.6 | 0.1 |
| 15h | 0.6 | Ruim | 0.6 | 0 |
| 16h | 3.2 | Ruim | 0.7 | 2.5 |
| 17h | 3.3 | Ruim | 0.8 | 2.5 |
| 18h | 0.8 | Ruim | 0.7 | 0.1 |
| 19h | 3.2 | Ruim | 0.7 | 2.5 |
| 20h | 1.4 | Ruim | 0.7 | 0.7 |
| 21h | 1.7 | Ruim | 0.7 | 0.9 |
| 22h | 1.2 | Ruim | 0.8 | 0.4 |
| 23h | 1.5 | Ruim | 0.8 | 0.7 |

## Análise por Dia da Semana

| Dia | Latência Média | vs. Média Geral | Pior Horário | Testes |
|-----|----------------|-----------------|--------------|--------|
| Segunda | 51.1ms | -4.4% | 19h (70.0ms) | 288 |
| Terça | 55.5ms | +3.9% | 13h (83.0ms) | 287 |
| Quarta | 52.9ms | -1.0% | 09h (67.0ms) | 132 |
| Quinta | - | - | - | 0 |
| Sexta | - | - | - | 0 |
| Sábado | - | - | - | 0 |
| Domingo | 53.9ms | +0.9% | 21h (62.0ms) | 286 |

## Alertas de Anomalias

### Horários de Pico

Nenhum período de pico identificado. ✅

### Análise de Rotas (Tracert)

**Total de rotas detectadas**: 3

**Rotas identificadas**:

| Rota | Ocorrências | Com Perda | Sem Perda | Taxa de Perda |
|------|-------------|-----------|-----------|---------------|
| Rota 1 (Principal) | 987 | 79 | 908 | 8.0% |
| Rota 2 | 5 | 2 | 3 | 40.0% |
| Rota 3 | 1 | 0 | 1 | 0.0% |

**Correlação Rota vs Perda de Pacotes**: Rotas alternativas apresentam 33.3% de perda vs 8.0% na rota principal. Possível instabilidade em rotas alternativas.

**Mudanças de rota detectadas**: 12 (2 associadas a perda de pacotes)

*Últimas mudanças de rota com perda*:

- 09/12 às 12:49
- 09/12 às 13:14

### Anomalias de Latência

Total de 11 anomalia(s) detectada(s):

⚠️ **08/12 às 00:44**: Latência 64ms (4.1σ acima do esperado 51.2ms) [Severidade: alta]
⚠️ **08/12 às 09:29**: Latência 68ms (3.4σ acima do esperado 54.9ms) [Severidade: alta]
⚠️ **08/12 às 10:59**: Latência 66ms (3.5σ acima do esperado 54.2ms) [Severidade: alta]
⚠️ **08/12 às 11:04**: Latência 66ms (3.0σ acima do esperado 54.8ms) [Severidade: alta]
⚠️ **08/12 às 11:09**: Latência 68ms (3.6σ acima do esperado 54.8ms) [Severidade: alta]
⚠️ **08/12 às 19:44**: Latência 70ms (3.8σ acima do esperado 54.8ms) [Severidade: alta]
⚠️ **08/12 às 23:39**: Latência 55ms (3.6σ acima do esperado 49.9ms) [Severidade: alta]
⚠️ **09/12 às 07:24**: Latência 65ms (2.8σ acima do esperado 53.6ms) [Severidade: media]
⚠️ **09/12 às 07:34**: Latência 70ms (4.1σ acima do esperado 53.6ms) [Severidade: alta]
⚠️ **09/12 às 17:54**: Latência 72ms (5.3σ acima do esperado 51.3ms) [Severidade: alta]

*Exibindo 10 de 11 anomalias. Anomalias indicam desvios significativos do padrão normal.*

## Distribuição de Latência

| Faixa | Frequência | Percentual |
|-------|-----------|------------|
| 0-20ms | 0 | 0.0% |
| 20-40ms | 0 | 0.0% |
| 40-60ms | 912 | 91.8% |
| 60-80ms | 71 | 7.2% |
| 80+ms | 10 | 1.0% |

## Análise e Conclusão

**Conexão**: 99.34% - Boa

**Qualidade por Faixa Horária no Período**: 13/24 regular | 11/24 ruim

