import sys
sys.path.insert(0, 'scripts')
from processar_relatorio import processar_arquivos_teste

# Processar dados
dados_lista = processar_arquivos_teste()

# Agrupar por hora (consolidado de todos os dias)
latencia_por_hora = {}
for dado in dados_lista:
    if not dado.get('datetime') or dado.get('ping_aghuse', {}).get('media') is None:
        continue

    hora = dado['datetime'].hour
    lat = dado['ping_aghuse']['media']

    if hora not in latencia_por_hora:
        latencia_por_hora[hora] = {'latencias': [], 'count': 0}

    latencia_por_hora[hora]['latencias'].append(lat)
    latencia_por_hora[hora]['count'] += 1

# Calcular médias
for hora in latencia_por_hora:
    lats = latencia_por_hora[hora]['latencias']
    latencia_por_hora[hora]['media'] = sum(lats) / len(lats)

# Calcular média geral
todas_lats = [h['media'] for h in latencia_por_hora.values()]
media_geral = sum(todas_lats) / len(todas_lats)

print(f"Média geral: {media_geral:.1f}ms")
print(f"Threshold 15%: {media_geral * 1.15:.1f}ms")
print(f"Threshold 10%: {media_geral * 1.10:.1f}ms")
print()
print("Latências por hora:")
print("Hora | Média (ms) | É Pico (15%)? | Testes")
print("-----|------------|---------------|-------")

for hora in sorted(latencia_por_hora.keys()):
    media = latencia_por_hora[hora]['media']
    is_pico_15 = media >= media_geral * 1.15
    count = latencia_por_hora[hora]['count']
    print(f"{hora:02d}h | {media:6.1f}     | {'SIM' if is_pico_15 else 'NÃO':^13} | {count:5d}")
