import pandas as pd

# Principal
# Executa a estratégia de antecipação de média movel
# Ela leva em consideração as médias moveis o desvio padrão e o gradiente de inclinação das médias 
# Por enquanto nossa estratégia principal
def getMovingAverageAntecipationTradeStrategy(stock_data: pd.DataFrame, volatility_factor: float, fast_window=7, slow_window=40):
    # Calcula as Médias Moveis Rápida e Lenta
    stock_data["ma_fast"] = stock_data["close_price"].rolling(window=fast_window).mean()  # Média Rápida
    stock_data["ma_slow"] = stock_data["close_price"].rolling(window=slow_window).mean()  # Média Lenta
    # Pega as últimas Médias Móveis e as penúltimas para calcular o gradiente
    last_ma_fast = stock_data["ma_fast"].iloc[-1]  # Última Média Rápida
    prev_ma_fast = stock_data["ma_fast"].iloc[-3]  # Penúltima Média Rápida
    last_ma_slow = stock_data["ma_slow"].iloc[-1]  # Última Média Lenta
    prev_ma_slow = stock_data["ma_slow"].iloc[-3]  # Penúltima Média Lenta
    # Última volatilidade
    last_volatility = stock_data["volatility"].iloc[-2]
    # Calcula o gradiente (mudança) das médias móveis
    fast_gradient = last_ma_fast - prev_ma_fast
    slow_gradient = last_ma_slow - prev_ma_slow
    # Calcula a diferença atual entre as médias
    current_difference = abs(last_ma_fast - last_ma_slow)
    # Inicializa a decisão
    ma_trade_decision = None
    # Toma a decisão com base em volatilidade + gradiente
    if current_difference < last_volatility * volatility_factor:
        # Comprar se a média rápida está convergindo para cruzar de baixo para cima
        # if fast_gradient > 0 and fast_gradient > slow_gradient and last_ma_fast < last_ma_slow:
        if fast_gradient > 0 and fast_gradient > slow_gradient:
            ma_trade_decision = True  # Comprar
        # Vender se a média rápida está convergindo para cruzar de cima para baixo
        # elif fast_gradient < 0 and fast_gradient < slow_gradient and last_ma_fast > last_ma_slow:
        elif fast_gradient < 0 and fast_gradient < slow_gradient:
            ma_trade_decision = False  # Vender
    # Log da estratégia e decisão
    # Corrigir isso para log
    print('-------')
    print('Estratégia executada: Moving Average Antecipation')
    print(f' | Última Média Rápida: {last_ma_fast:.3f}')
    print(f' | Última Média Lenta: {last_ma_slow:.3f}')
    print(f' | Última Volatilidade: {last_volatility:.3f}')
    print(f' | Diferença Atual: {current_difference:.3f}')
    print(f' | Diferença para antecipação: {volatility_factor * last_volatility:.3f}')
    print(f' | Gradiente Rápido: {fast_gradient:.3f} ({ "Subindo" if fast_gradient > 0 else "Descendo" })')
    print(f' | Gradiente Lento: {slow_gradient:.3f} ({ "Subindo" if slow_gradient > 0 else "Descendo" })')
    print(f' | Decisão: {"Comprar" if ma_trade_decision == True else "Vender" if ma_trade_decision == False else "Nenhuma"}')
    print('-------')
    return ma_trade_decision