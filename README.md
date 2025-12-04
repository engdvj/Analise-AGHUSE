# Sistema de Monitoramento AGHUSE

Sistema automatizado para monitorar conectividade com o servidor AGHUSE (10.252.17.132) e gerar relatórios de disponibilidade.

## 📁 Estrutura

```
├── aghuse.bat                  # Coleta de dados (executar a cada 5 min)
├── gerar_relatorios.bat        # Gera relatórios
├── processar_relatorio.py      # Processa dados
├── arquivos/                   # Dados de testes (.txt)
│   ├── 2025-12-03/            # Arquivos organizados por dia
│   └── 2025-12-04/
└── relatorios/                 # Relatórios gerados (.md)
```

## 🚀 Como Usar

### 1. Coletar Dados

Execute `aghuse.bat` a cada 5 minutos (manualmente ou via Agendador de Tarefas):
- Testa conectividade com AGHUSE
- Salva resultados em `arquivos/YYYY-MM-DD/`

### 2. Gerar Relatórios

Duplo clique em `gerar_relatorios.bat` ou execute:
```bash
python processar_relatorio.py
```

### 3. Visualizar Relatórios

Abra os arquivos `.md` na pasta `relatorios/` com qualquer editor de texto ou visualizador Markdown.

## 📊 Tipos de Relatórios

- **Diário**: Análise detalhada de cada dia
- **Semanal**: Comparativo do período
- **Geral**: Visão completa com horários críticos

## 📈 Métricas

### Disponibilidade
```
Disponibilidade = (Pacotes Enviados - Perdidos) / Enviados × 100
```

| Faixa | Classificação |
|-------|---------------|
| ≥ 99.9% | Excelente |
| ≥ 99.0% | Boa |
| ≥ 95.0% | Aceitável |
| < 95.0% | Crítica |

### Latência (ms)

| Faixa | Classificação |
|-------|---------------|
| < 10ms | Excelente |
| < 20ms | Adequada |
| < 50ms | Aceitável |
| ≥ 50ms | Requer investigação |

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

- O script agora suporta arquivos em subpastas organizadas por data
- Arquivos podem estar diretamente em `arquivos/` ou em `arquivos/YYYY-MM-DD/`
- Recomenda-se manter dados dos últimos 30 dias

---

**Versão**: 2.0
**Atualização**: Dezembro 2025
