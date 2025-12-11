# Relatório Semanal - Monitoramento de Conectividade AGHUSE
**Período**: 07/12/2025 a 13/12/2025

## Sumário Executivo

| Métrica | Valor |
|---------|-------|
| Total de Testes Executados | 1291 |
| Testes sem Perda | 1142 |
| Testes com Perda | 149 |
| Total de Pacotes Enviados | 25820 |
| Total de Pacotes Perdidos | 180 |
| **Disponibilidade** | **99.30%** |
| Latência Média | 52.7ms |
| Latência Mín/Máx | 8/282ms |

## Análise por Dia

| Data | Testes | Sem Perda / Com Perda | Pacotes Perdidos | Disponibilidade | AGHUSE (ms) | Rede Externa (ms) |
|------|--------|-----------------------|------------------|-----------------|-------------|-------------------|
| 07/12/2025 | 286 | 275 / 11 | 14 | 99.76% | 53.9ms | 35.0ms |
| 08/12/2025 | 288 | 254 / 34 | 40 | 99.31% | 51.1ms | 42.1ms |
| 09/12/2025 | 287 | 239 / 48 | 57 | 99.01% | 55.5ms | 50.0ms |
| 10/12/2025 | 288 | 247 / 41 | 49 | 99.15% | 52.8ms | 45.3ms |
| 11/12/2025 | 142 | 127 / 15 | 20 | 99.30% | 47.3ms | 39.4ms |
| 12/12/2025 | - | - | - | - | - | - |
| 13/12/2025 | - | - | - | - | - | - |

## Análise de Latência por Faixa Horária

> **Nota**: Esta análise consolida todos os testes realizados em cada faixa horária
> ao longo do período completo (07/12/2025 a 13/12/2025).
> Cada linha representa a média de todos os testes naquela hora em todos os dias.

| Horário | AGHUSE (ms) | Rede Externa (ms) | Status |
|---------|-------------|-------------------|--------|
| 00h | 51.1 (48-77) | 41.2 (30-51) | Regular [AG:1pkt] |
| 01h | 50.4 (48-55) | 40.8 (30-54) | Regular [AG:2pkt, EX:1pkt] |
| 02h | 50.5 (48-55) | 40.6 (30-50) | Regular [EX:1pkt] |
| 03h | 50.5 (48-56) | 40.6 (30-50) | Regular [AG:3pkt, EX:1pkt] |
| 04h | 50.4 (48-56) | 38.7 (30-49) | Regular [AG:1pkt] |
| 05h | 50.5 (48-55) | 37.8 (30-49) | Regular |
| 06h | 52.9 (49-71) | 37.2 (30-50) | Regular [AG:1pkt, EX:1pkt] |
| 07h | 52.6 (49-70) | 39.8 (30-82) | Ruim [AG:3pkt, EX:6pkt] |
| 08h | 52.6 (49-60) | 42.8 (34-72) | Ruim [AG:9pkt, EX:13pkt] |
| 09h | 53.3 (49-60) | 48.7 (33-100) | Ruim [AG:17pkt, EX:6pkt] |
| 10h | 53.2 (49-67) | 46.6 (33-127) | Ruim [AG:17pkt, EX:3pkt] |
| 11h | 47.4 (9-69) | 44.3 (34-71) | Regular [AG:19pkt, EX:5pkt] |
| 12h | 57.3 (49-69) | 41.5 (33-55) | Ruim [AG:7pkt, EX:4pkt] |
| 13h | 59.5 (49-80) | 39.9 (33-56) | Ruim [AG:13pkt, EX:7pkt] |
| 14h | 56.2 (48-76) | 42.1 (34-57) | Ruim [AG:9pkt, EX:6pkt] |
| 15h | 55.4 (48-73) | 44.2 (36-76) | Ruim [AG:8pkt, EX:3pkt] |
| 16h | 54.8 (47-71) | 44.4 (34-59) | Ruim [AG:6pkt, EX:7pkt] |
| 17h | 52.0 (48-71) | 44.8 (34-70) | Regular [AG:2pkt, EX:1pkt] |
| 18h | 52.6 (48-65) | 47.4 (33-79) | Ruim [AG:6pkt, EX:1pkt] |
| 19h | 53.1 (49-70) | 46.8 (33-81) | Regular [AG:1pkt, EX:3pkt] |
| 20h | 52.5 (49-58) | 45.1 (33-66) | Regular [AG:2pkt, EX:1pkt] |
| 21h | 52.6 (49-59) | 45.3 (33-65) | Regular [EX:1pkt] |
| 22h | 51.4 (48-58) | 45.2 (33-63) | Regular [AG:1pkt, EX:1pkt] |
| 23h | 49.6 (48-54) | 43.3 (33-72) | Regular [AG:3pkt, EX:2pkt] |

**Gráfico Comparativo de Latência:**

```
AGHUSE vs Rede Externa
00h │AG: ██████████████████████████████ 51.1ms
     │EX: ████████████████████████ 41.2ms
01h │AG: ██████████████████████████████ 50.4ms
     │EX: ████████████████████████ 40.8ms
02h │AG: ██████████████████████████████ 50.5ms
     │EX: ████████████████████████ 40.6ms
03h │AG: ██████████████████████████████ 50.5ms
     │EX: ████████████████████████ 40.6ms
04h │AG: ██████████████████████████████ 50.4ms
     │EX: ███████████████████████ 38.7ms
05h │AG: ██████████████████████████████ 50.5ms
     │EX: ██████████████████████ 37.8ms
06h │AG: ██████████████████████████████ 52.9ms
     │EX: █████████████████████ 37.2ms
07h │AG: ██████████████████████████████ 52.6ms
     │EX: ██████████████████████ 39.8ms
08h │AG: ██████████████████████████████ 52.6ms
     │EX: ████████████████████████ 42.8ms
09h │AG: ██████████████████████████████ 53.3ms
     │EX: ███████████████████████████ 48.7ms
10h │AG: ██████████████████████████████ 53.2ms
     │EX: ██████████████████████████ 46.6ms
11h │AG: ██████████████████████████████ 47.4ms
     │EX: ███████████████████████████ 44.3ms
12h │AG: ██████████████████████████████ 57.3ms
     │EX: █████████████████████ 41.5ms
13h │AG: ██████████████████████████████ 59.5ms
     │EX: ████████████████████ 39.9ms
14h │AG: ██████████████████████████████ 56.2ms
     │EX: ██████████████████████ 42.1ms
15h │AG: ██████████████████████████████ 55.4ms
     │EX: ███████████████████████ 44.2ms
16h │AG: ██████████████████████████████ 54.8ms
     │EX: ████████████████████████ 44.4ms
17h │AG: ██████████████████████████████ 52.0ms
     │EX: █████████████████████████ 44.8ms
18h │AG: ██████████████████████████████ 52.6ms
     │EX: ███████████████████████████ 47.4ms
19h │AG: ██████████████████████████████ 53.1ms
     │EX: ██████████████████████████ 46.8ms
20h │AG: ██████████████████████████████ 52.5ms
     │EX: █████████████████████████ 45.1ms
21h │AG: ██████████████████████████████ 52.6ms
     │EX: █████████████████████████ 45.3ms
22h │AG: ██████████████████████████████ 51.4ms
     │EX: ██████████████████████████ 45.2ms
23h │AG: ██████████████████████████████ 49.6ms
     │EX: ██████████████████████████ 43.3ms
```

## Análise de Horários Críticos

### Distribuição de Perda de Pacotes por Horário

| Faixa Horária | Ocorrências | Porcentagem do Total |
|---------------|-------------|---------------------|
| 09:00 - 09:59 | 25 | 16.8% |
| 10:00 - 10:59 | 20 | 13.4% |
| 11:00 - 11:59 | 16 | 10.7% |
| 13:00 - 13:59 | 13 | 8.7% |
| 14:00 - 14:59 | 10 | 6.7% |
| 15:00 - 15:59 | 8 | 5.4% |
| 12:00 - 12:59 | 7 | 4.7% |
| 23:00 - 23:59 | 7 | 4.7% |
| 08:00 - 08:59 | 6 | 4.0% |
| 18:00 - 18:59 | 5 | 3.4% |
| 07:00 - 07:59 | 5 | 3.4% |
| 06:00 - 06:59 | 4 | 2.7% |
| 20:00 - 20:59 | 4 | 2.7% |
| 22:00 - 22:59 | 4 | 2.7% |
| 03:00 - 03:59 | 3 | 2.0% |
| 19:00 - 19:59 | 2 | 1.3% |
| 16:00 - 16:59 | 2 | 1.3% |
| 17:00 - 17:59 | 2 | 1.3% |
| 21:00 - 21:59 | 2 | 1.3% |
| 00:00 - 00:59 | 2 | 1.3% |
| 04:00 - 04:59 | 1 | 0.7% |
| 01:00 - 01:59 | 1 | 0.7% |

### Distribuição de Latência Elevada (>20ms) por Horário

| Faixa Horária | Ocorrências |
|---------------|-------------|
| 00:00 - 00:59 | 60 |
| 01:00 - 01:59 | 60 |
| 02:00 - 02:59 | 60 |
| 03:00 - 03:59 | 60 |
| 04:00 - 04:59 | 60 |
| 05:00 - 05:59 | 60 |
| 06:00 - 06:59 | 60 |
| 07:00 - 07:59 | 60 |
| 08:00 - 08:59 | 60 |
| 10:00 - 10:59 | 60 |

## Registro de Incidentes

Total de 149 teste(s) com perda de pacotes:

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

*Exibindo 20 de 149 incidentes. Consulte relatórios diários para detalhes completos.*

## Score de Qualidade por Horário

| Horário | Score | Classificação | Componente Latência | Componente Perda |
|---------|-------|---------------|---------------------|------------------|
| 00h | 2.9 | Ruim | 0.8 | 2.1 |
| 01h | 4.0 | Ruim | 0.8 | 3.2 |
| 02h | 4.8 | Regular | 0.8 | 4.0 |
| 03h | 1.8 | Ruim | 0.8 | 1.0 |
| 04h | 4.0 | Ruim | 0.8 | 3.2 |
| 05h | 4.8 | Regular | 0.8 | 4.0 |
| 06h | 1.6 | Ruim | 0.7 | 0.8 |
| 07h | 1.4 | Ruim | 0.7 | 0.7 |
| 08h | 1.2 | Ruim | 0.7 | 0.5 |
| 09h | 0.7 | Ruim | 0.7 | 0 |
| 10h | 0.7 | Ruim | 0.7 | 0 |
| 11h | 0.9 | Ruim | 0.9 | 0 |
| 12h | 0.6 | Ruim | 0.6 | 0.0 |
| 13h | 0.5 | Ruim | 0.5 | 0 |
| 14h | 0.6 | Ruim | 0.6 | 0 |
| 15h | 0.7 | Ruim | 0.7 | 0 |
| 16h | 2.2 | Ruim | 0.7 | 1.6 |
| 17h | 2.3 | Ruim | 0.8 | 1.6 |
| 18h | 1.2 | Ruim | 0.7 | 0.5 |
| 19h | 2.3 | Ruim | 0.7 | 1.6 |
| 20h | 1.4 | Ruim | 0.7 | 0.7 |
| 21h | 2.3 | Ruim | 0.7 | 1.6 |
| 22h | 1.5 | Ruim | 0.8 | 0.7 |
| 23h | 0.9 | Ruim | 0.8 | 0.0 |

## Análise por Dia da Semana

| Dia | Latência Média | vs. Média Geral | Pior Horário | Testes |
|-----|----------------|-----------------|--------------|--------|
| Segunda | 51.1ms | -3.0% | 19h (70.0ms) | 288 |
| Terça | 55.5ms | +5.4% | 13h (83.0ms) | 287 |
| Quarta | 52.8ms | +0.2% | 09h (67.0ms) | 288 |
| Quinta | 47.3ms | -10.1% | 09h (55.0ms) | 142 |
| Sexta | - | - | - | 0 |
| Sábado | - | - | - | 0 |
| Domingo | 53.9ms | +2.4% | 21h (62.0ms) | 286 |

### Análise por Dia da Semana - Rede Externa (8.8.8.8)

| Dia | Latência Média | vs. Média Geral | Pior Horário | Testes |
|-----|----------------|-----------------|--------------|--------|
| Segunda | 42.3ms | -1.1% | 19h (81.0ms) | 287 |
| Terça | 50.0ms | +17.1% | 10h (127.0ms) | 287 |
| Quarta | 45.3ms | +6.0% | 10h (70.0ms) | 288 |
| Quinta | 39.4ms | -7.9% | 11h (55.0ms) | 142 |
| Sexta | - | - | - | 0 |
| Sábado | - | - | - | 0 |
| Domingo | 35.0ms | -18.2% | 08h (45.0ms) | 286 |

## Alertas de Anomalias

### Horários de Pico

Nenhum período de pico identificado. ✅

### Análise de Rotas (Tracert)

**Total de rotas detectadas**: 3

**Rota principal:** Rota 1 (Principal) = 10.17.201.254 -> 10.17.250.114 -> ... -> 10.2.222.220 -> 10.252.17.132 (6 saltos); perda 8.7% em 1283 testes.
**Alternativas:** 2 rota(s). Mais usada: Rota 2 = 10.17.201.254 -> 10.17.250.114 -> ... -> 10.252.17.132 -> 10.252.17.132 (7 saltos) (mesmos hops iniciais, 1 salto(s) a mais); perda 28.6% em 7 testes.

**Rotas identificadas**:

| Rota | Ocorrências | Com Perda | Sem Perda | Taxa de Perda |
|------|-------------|-----------|-----------|---------------|
| Rota 1 (Principal) - 10.17.201.254 -> 10.17.250.114 -> ... -> 10.2.222.220 -> 10.252.17.132 (6 saltos) | 1283 | 112 | 1171 | 8.7% |
| Rota 2 - 10.17.201.254 -> 10.17.250.114 -> ... -> 10.252.17.132 -> 10.252.17.132 (7 saltos) | 7 | 2 | 5 | 28.6% |
| Rota 3 - 10.17.201.254 -> 10.17.250.114 -> ... -> 10.2.222.220 -> 10.252.17.132 (7 saltos) | 1 | 0 | 1 | 0.0% |

**Correlação Rota vs Perda de Pacotes**: Rota principal: 8.7% de perda em 1283 testes. Alternativas: 25.0% em 8 testes. Mudanças: 2 de 16 (12%) tiveram perda. Rotas alternativas mais instáveis que a principal.

**Mudanças de rota detectadas**: 16 (2 associadas a perda de pacotes)

*O que mudou*:

- 10/12 às 00:24: Rota 3 -> Rota 1 (Principal) (sem perda registrada; diferente a partir do salto 5: 10.2.222.244 -> 10.2.222.220)
- 10/12 às 12:54: Rota 1 (Principal) -> Rota 2 (sem perda registrada; mesmos hops iniciais, 1 salto(s) a mais)
- 10/12 às 12:59: Rota 2 -> Rota 1 (Principal) (sem perda registrada; mesmos hops iniciais, 1 salto(s) a menos)
- 11/12 às 09:39: Rota 1 (Principal) -> Rota 2 (sem perda registrada; mesmos hops iniciais, 1 salto(s) a mais)
- 11/12 às 09:44: Rota 2 -> Rota 1 (Principal) (sem perda registrada; mesmos hops iniciais, 1 salto(s) a menos)

### Anomalias de Latência

Total de 50 anomalia(s) detectada(s):

⚠️ **04/12 às 13:44**: Latência 29ms (2.8σ acima do esperado 11.8ms) [Severidade: media]
⚠️ **04/12 às 20:04**: Latência 54ms (2.7σ acima do esperado 52.2ms) [Severidade: media]
⚠️ **04/12 às 21:29**: Latência 55ms (3.0σ acima do esperado 51.8ms) [Severidade: media]
⚠️ **05/12 às 04:49**: Latência 51ms (2.7σ acima do esperado 49.3ms) [Severidade: media]
⚠️ **05/12 às 05:24**: Latência 54ms (2.6σ acima do esperado 49.9ms) [Severidade: media]
⚠️ **05/12 às 16:19**: Latência 68ms (3.3σ acima do esperado 51.7ms) [Severidade: alta]
⚠️ **06/12 às 03:39**: Latência 52ms (2.9σ acima do esperado 50.2ms) [Severidade: media]
⚠️ **06/12 às 13:19**: Latência 51ms (2.9σ acima do esperado 49.2ms) [Severidade: media]
⚠️ **06/12 às 18:34**: Latência 57ms (3.0σ acima do esperado 54.4ms) [Severidade: media]
⚠️ **07/12 às 03:19**: Latência 56ms (2.6σ acima do esperado 50.5ms) [Severidade: media]
⚠️ **07/12 às 05:04**: Latência 56ms (2.5σ acima do esperado 50.6ms) [Severidade: media]
⚠️ **07/12 às 07:14**: Latência 55ms (3.3σ acima do esperado 54.1ms) [Severidade: alta]
⚠️ **07/12 às 08:39**: Latência 56ms (2.7σ acima do esperado 54.3ms) [Severidade: media]
⚠️ **07/12 às 09:34**: Latência 56ms (2.7σ acima do esperado 54.3ms) [Severidade: media]
⚠️ **07/12 às 12:19**: Latência 60ms (3.1σ acima do esperado 55.2ms) [Severidade: alta]
⚠️ **07/12 às 20:09**: Latência 59ms (3.3σ acima do esperado 58.1ms) [Severidade: alta]
⚠️ **07/12 às 21:49**: Latência 62ms (2.6σ acima do esperado 52.9ms) [Severidade: media]
⚠️ **08/12 às 00:44**: Latência 64ms (4.6σ acima do esperado 50.9ms) [Severidade: alta]
⚠️ **08/12 às 02:29**: Latência 50ms (3.3σ acima do esperado 49.1ms) [Severidade: alta]
⚠️ **08/12 às 05:44**: Latência 50ms (3.3σ acima do esperado 49.1ms) [Severidade: alta]
⚠️ **08/12 às 09:29**: Latência 68ms (3.8σ acima do esperado 54.3ms) [Severidade: alta]
⚠️ **08/12 às 10:59**: Latência 66ms (3.8σ acima do esperado 53.7ms) [Severidade: alta]
⚠️ **08/12 às 14:34**: Latência 57ms (2.7σ acima do esperado 51.1ms) [Severidade: media]
⚠️ **08/12 às 18:49**: Latência 57ms (3.1σ acima do esperado 51.9ms) [Severidade: alta]
⚠️ **08/12 às 19:44**: Latência 70ms (4.1σ acima do esperado 53.5ms) [Severidade: alta]
⚠️ **08/12 às 20:04**: Latência 52ms (3.3σ acima do esperado 51.1ms) [Severidade: alta]
⚠️ **08/12 às 23:39**: Latência 55ms (3.4σ acima do esperado 50.0ms) [Severidade: alta]
⚠️ **09/12 às 00:09**: Latência 56ms (3.3σ acima do esperado 51.4ms) [Severidade: alta]
⚠️ **09/12 às 01:54**: Latência 52ms (3.3σ acima do esperado 51.1ms) [Severidade: alta]
⚠️ **09/12 às 02:54**: Latência 52ms (3.3σ acima do esperado 51.1ms) [Severidade: alta]
⚠️ **09/12 às 05:59**: Latência 52ms (3.3σ acima do esperado 51.1ms) [Severidade: alta]
⚠️ **09/12 às 07:24**: Latência 65ms (3.1σ acima do esperado 53.0ms) [Severidade: alta]
⚠️ **09/12 às 07:34**: Latência 70ms (4.5σ acima do esperado 53.0ms) [Severidade: alta]
⚠️ **09/12 às 14:14**: Latência 76ms (2.9σ acima do esperado 55.9ms) [Severidade: media]
⚠️ **09/12 às 15:09**: Latência 79ms (2.8σ acima do esperado 56.3ms) [Severidade: media]
⚠️ **09/12 às 16:09**: Latência 73ms (2.5σ acima do esperado 54.9ms) [Severidade: media]
⚠️ **09/12 às 17:54**: Latência 72ms (5.4σ acima do esperado 51.9ms) [Severidade: alta]
⚠️ **09/12 às 21:39**: Latência 58ms (3.0σ acima do esperado 52.8ms) [Severidade: alta]
⚠️ **09/12 às 23:44**: Latência 52ms (2.8σ acima do esperado 49.0ms) [Severidade: media]
⚠️ **10/12 às 03:24**: Latência 51ms (2.7σ acima do esperado 48.8ms) [Severidade: media]
⚠️ **10/12 às 06:19**: Latência 65ms (2.7σ acima do esperado 52.8ms) [Severidade: media]
⚠️ **10/12 às 06:29**: Latência 65ms (2.7σ acima do esperado 52.8ms) [Severidade: media]
⚠️ **10/12 às 06:34**: Latência 64ms (2.5σ acima do esperado 52.8ms) [Severidade: media]
⚠️ **10/12 às 06:39**: Latência 65ms (2.7σ acima do esperado 52.8ms) [Severidade: media]
⚠️ **10/12 às 07:39**: Latência 60ms (3.2σ acima do esperado 56.4ms) [Severidade: alta]
⚠️ **10/12 às 09:29**: Latência 67ms (3.5σ acima do esperado 54.3ms) [Severidade: alta]
⚠️ **10/12 às 10:49**: Latência 62ms (2.6σ acima do esperado 53.7ms) [Severidade: media]
⚠️ **10/12 às 15:09**: Latência 64ms (3.0σ acima do esperado 55.6ms) [Severidade: media]
⚠️ **10/12 às 23:24**: Latência 55ms (3.4σ acima do esperado 50.0ms) [Severidade: alta]
⚠️ **11/12 às 00:44**: Latência 52ms (2.5σ acima do esperado 49.6ms) [Severidade: media]

## Distribuição de Latência

### AGHUSE (10.252.17.132)

| Faixa | Frequência | Percentual |
|-------|-----------|------------|
| 0-20ms | 10 | 0.8% |
| 20-40ms | 0 | 0.0% |
| 40-60ms | 1199 | 92.9% |
| 60-80ms | 72 | 5.6% |
| 80+ms | 10 | 0.8% |

### Rede Externa (8.8.8.8)

| Faixa | Frequência | Percentual |
|-------|-----------|------------|
| 0-20ms | 0 | 0.0% |
| 20-40ms | 635 | 49.2% |
| 40-60ms | 559 | 43.3% |
| 60-80ms | 92 | 7.1% |
| 80+ms | 4 | 0.3% |

## Análise e Conclusão

**Conexão**: 99.30% - Boa

**Qualidade por Faixa Horária no Período**: 14/24 regular | 10/24 ruim

