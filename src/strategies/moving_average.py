
import pandas as pd

# Fallback strategy
# Se a estratégia de antecipação de média móvel não retornar nada
# Executamos a estratégia original de media móvel, para ter como referência.
def getMovingAverageTradeStrategy(stock_data: pd.DataFrame, fast_window = 7, slow_window = 70):
    # Calcula as Médias Moveis Rápida e Lenta
    stock_data["ma_fast"] = stock_data["close_price"].rolling(window=fast_window).mean()  # Média Rápida
    stock_data["ma_slow"] = stock_data["close_price"].rolling(window=slow_window).mean() # Média Lenta
    # Pega as últimas Moving Average
    last_ma_fast = stock_data["ma_fast"].iloc[-1] # iloc[-1] pega o último dado do array.
    last_ma_slow = stock_data["ma_slow"].iloc[-1]
    # Toma a decisão, baseada na posição da média movel
    # (False = Vender | True = Comprar)
    if last_ma_fast > last_ma_slow:
        ma_trade_decision = True # Compra
    else:
        ma_trade_decision = False # Vende
        
    print('-------')
    print('Estratégia executada: Moving Average')
    print(f' | {last_ma_fast:.3f} = Última Média Rápida \n | {last_ma_slow:.3f} = Última Média Lenta')
    print(f' | Decisão: {"Comprar" if ma_trade_decision == True else "Vender"}')
    print('-------')
    
    return ma_trade_decision;