# 📋 Guia Rápido de Critérios - AGHUSE

> **Referência Visual Rápida** - Para documentação completa, consulte [CRITERIOS_E_METODOLOGIA.md](CRITERIOS_E_METODOLOGIA.md)

---

## 🎯 O que eu preciso saber?

### Status da Disponibilidade
```
100%  │ 🟢 ÓTIMO
      │
99.9% ├─────────────────
      │ 🔵 BOM
99.0% ├─────────────────
      │ 🟡 REGULAR
95.0% ├─────────────────
      │ 🔴 RUIM
  0%  │
```

### Latência (Tempo de Resposta)
```
 0ms  │ 🏆 EXCELENTE
      │
15ms  ├─────────────────  ← Baseline Ideal
      │ 👍 BOA
30ms  ├─────────────────
      │ ⚠️ REGULAR
50ms  ├─────────────────
      │ ❌ RUIM
+∞    │
```

---

## 📊 Hierarquia de Análise

```
┌─────────────────────────────────────────────┐
│           RELATÓRIO PRINCIPAL               │
│  (Diário, Semanal ou Geral)                │
└───────────────┬─────────────────────────────┘
                │
    ┌───────────┴───────────┐
    │                       │
┌───▼───────────┐   ┌──────▼──────────┐
│ DISPONIBILIDADE│   │    LATÊNCIA     │
│  (% pacotes)   │   │  (tempo ms)     │
└───────┬────────┘   └────────┬────────┘
        │                     │
        │    ┌────────────────┴──────────────┐
        │    │                               │
        ▼    ▼                               ▼
  ┌─────────────┐                   ┌─────────────┐
  │   SCORE     │                   │  ANÁLISES   │
  │ QUALIDADE   │                   │  AVANÇADAS  │
  │   (0-10)    │                   └──────┬──────┘
  └─────────────┘                          │
                                    ┌──────┴──────┐
                                    │             │
                          ┌─────────▼───┐  ┌─────▼─────────┐
                          │ HORÁRIOS    │  │   ANOMALIAS   │
                          │  DE PICO    │  │   (eventos)   │
                          └─────────────┘  └───────────────┘
```

---

## 🔢 Cálculos Rápidos

### Score de Qualidade
```
Score = (Latência × 60%) + (Perda × 40%)
         ▲                   ▲
         │                   │
      0-6 pts             0-4 pts
```

### Disponibilidade
```
Disp. = (Total - Perdidos) / Total × 100%
         ▲                    ▲
         │                    │
    Pacotes enviados    Pacotes recebidos
```

---

## ⚡ Diferenças Importantes

### Pico vs. Anomalia

| Característica | Horário de Pico | Anomalia |
|----------------|-----------------|----------|
| **Duração** | 3+ horas | Minutos |
| **Frequência** | Recorrente | Pontual |
| **Causa** | Padrão normal | Evento isolado |
| **Severidade** | Moderada | Extrema |
| **Ícone** | 📈 | ⚠️ |

**Exemplo Visual:**
```
Latência ao longo do dia:

60ms  │        📈 PICO (15h-18h)              ⚠️ ANOMALIA
      │      ╱────────────╲                    │
50ms  │    ╱              ╲                   │
      │  ╱                  ╲                 │
40ms  ├──────────────────────╲───────────────┼───────
      │                        ╲             ╱
30ms  │                         ╲──────────╱
      │
      └──────────────────────────────────────────────
      0h    6h     12h    18h         22h
```

---

## 🎨 Cores nos Gráficos

### Score de Qualidade
```
10.0 ┤ 🟢 Verde   (8.5-10)  → Excelente
 8.5 ├────────────────────
     │ 🔵 Azul    (7.0-8.4) → Muito Bom
 7.0 ├────────────────────
     │ 🟡 Amarelo (5.5-6.9) → Bom
 5.5 ├────────────────────
     │ 🟠 Laranja (4.0-5.4) → Regular
 4.0 ├────────────────────
     │ 🔴 Vermelho (< 4.0) → Ruim
 0.0 ┘
```

---

## 📈 Tendências (Regressão Linear)

### Como Interpretar

```
y = ax + b

a (slope) = Inclinação da linha
           ▲
           │  > 0.5    → 📈 ALTA
           │  -0.5 a 0.5 → → ESTÁVEL
           │  < -0.5   → 📉 QUEDA

R² = Confiabilidade
     ▲
     │  > 0.5  → ✅ Confiável
     │  < 0.5  → ⚠️ Pouco confiável
```

**Exemplo Visual:**
```
Latência
   │
60 │           ╱ ← Tendência de ALTA (slope > 0)
   │         ╱
55 │       ╱  ●
   │     ╱  ●
50 │   ╱  ●
   │ ╱  ●
45 ●───────────────────────────────────▶ Dias
   1    2    3    4    5    6    7
```

---

## 💡 Dicas de Uso

### Onde encontrar cada informação?

| O que procuro? | Onde está? |
|----------------|-----------|
| Status geral do dia | Relatório Diário → Topo |
| Problemas em horário específico | Relatório Diário → Tabela por Horário |
| Tendências da semana | Relatório Semanal → Aba "Tendências" |
| Score de qualidade | Relatório Semanal/Geral → Aba "Análise Avançada" |
| Anomalias detectadas | Relatório Semanal/Geral → Aba "Anomalias" |
| Explicação dos critérios | Qualquer relatório HTML → Aba "Critérios e Metodologia" |

---

## 🔍 Checklist Rápido

### Avaliar saúde da conexão em 3 passos

1. **Disponibilidade** ≥ 99%? ✅ / ❌
2. **Latência Média** ≤ 30ms? ✅ / ❌
3. **Score Geral** ≥ 7.0? ✅ / ❌

**3 ✅** = 🟢 Tudo ótimo
**2 ✅** = 🟡 Atenção
**≤1 ✅** = 🔴 Ação necessária

---

## 📞 Próximos Passos

- **Dúvida técnica?** → [CRITERIOS_E_METODOLOGIA.md](CRITERIOS_E_METODOLOGIA.md)
- **Quer ver fórmulas?** → [CRITERIOS_E_METODOLOGIA.md](CRITERIOS_E_METODOLOGIA.md) (seção Fórmulas)
- **Entender um termo?** → Relatório HTML → Aba "Critérios e Metodologia"

---

**Última atualização**: 2025-12-09
