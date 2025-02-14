import threading
import time
from modules.BinanceRobot import BinanceTraderBot
from binance.client import Client
from Models.AssetStartModel import AssetStartModel
import logging

# Define o logger
logging.basicConfig(
    filename='src/logs/trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ------------------------------------------------------------------
# 🟢 CONFIGURAÇÕES - PODEM ALTERAR - INICIO 🟢


# Ajustes Técnicos
VOLATILITY_FACTOR           = 0.5       # Interfere na antecipação e nos lances de compra de venda limitados
ACCEPTABLE_LOSS_PERCENTAGE  = 0.5        # (Usar em base 100%) O quando o bot aceita perder de % (se for negativo, o bot só aceita lucro)
STOP_LOSS_PERCENTAGE        = 5         # (Usar em base 100%) % Máxima de loss que ele aceita para vender à mercado independente
FALLBACK_ACTIVATED          = True      # Define se a estratégia de Fallback será usada (ela pode entrar comprada em mercados subindo)


# Ajustes de Tempo
CANDLE_PERIOD = Client.KLINE_INTERVAL_1MINUTE # Périodo do candle análisado
TEMPO_ENTRE_TRADES          = 5 * 60    # Tempo que o bot espera para verificar o mercado (em segundos)
DELAY_ENTRE_ORDENS          = 3 * 60   # Tempo que o bot espera depois de realizar uma ordem de compra ou venda (ajuda a diminuir trades de borda)


# Ajustes de Execução
THREAD_LOCK = True # True = Executa 1 moeda por vez | False = Executa todas simultânemaente


# Moedas negociadas
LUNA_USDT = AssetStartModel(  stockCode = "LUNA",
                            operationCode = "LUNAUSDT",
                            tradedQuantity = 140,
                            candlePeriod = CANDLE_PERIOD, volatilityFactor = VOLATILITY_FACTOR, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ACTIVATED)

USTC_USDT = AssetStartModel(  stockCode = "USTC",
                            operationCode = "USTCUSDT",
                            tradedQuantity = 2500,
                            candlePeriod = CANDLE_PERIOD, volatilityFactor = VOLATILITY_FACTOR, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ACTIVATED)

FTT_USDT = AssetStartModel(  stockCode = "FTT",
                            operationCode = "FTTUSDT",
                            tradedQuantity = 5,
                            candlePeriod = CANDLE_PERIOD, volatilityFactor = VOLATILITY_FACTOR, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ACTIVATED)

BNX_USDT = AssetStartModel(  stockCode = "BNX",
                            operationCode = "BNXUSDT",
                            tradedQuantity = 50,
                            candlePeriod = CANDLE_PERIOD, volatilityFactor = VOLATILITY_FACTOR, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ACTIVATED)

XLM_USDT = AssetStartModel(  stockCode = "XLM",
                            operationCode = "XLMUSDT",
                            tradedQuantity = 0.1,
                            candlePeriod = CANDLE_PERIOD, volatilityFactor = VOLATILITY_FACTOR, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ACTIVATED)

XRP_USDT = AssetStartModel(  stockCode = "XRP",
                            operationCode = "XRPUSDT",
                            tradedQuantity = 0.1,
                            candlePeriod = CANDLE_PERIOD, volatilityFactor = VOLATILITY_FACTOR, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ACTIVATED)

OXT_USDT = AssetStartModel(  stockCode = "OXT",
                            operationCode = "OXTUSDT",
                            tradedQuantity = 0.1,
                            candlePeriod = CANDLE_PERIOD, volatilityFactor = VOLATILITY_FACTOR, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ACTIVATED)

ADA_USDT = AssetStartModel(  stockCode = "ADA",
                            operationCode = "ADAUSDT",
                            tradedQuantity = 15,
                            candlePeriod = CANDLE_PERIOD, volatilityFactor = VOLATILITY_FACTOR, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ACTIVATED)

# Array que DEVE CONTER as moedas que serão negociadas
assetsTraders = [FTT_USDT, LUNA_USDT] 

# assetsTraders = [XRP_USDT, SOL_BRL] # Exemplo com mais de uma moeda




# 🔴 CONFIGURAÇÕES - PODEM ALTERAR - FIM 🔴
# ---------------------------------------------------------------------------------------------
# LOOP PRINCIPAL

thread_lock = threading.Lock()

def trader_loop(assetStart: AssetStartModel):
    MaTrader = BinanceTraderBot(stock_code = assetStart.stockCode
                                , operation_code = assetStart.operationCode
                                , traded_quantity = assetStart.tradedQuantity
                                , traded_percentage = assetStart.tradedPercentage
                                , candle_period = assetStart.candlePeriod
                                , volatility_factor = assetStart.volatilityFactor
                                , time_to_trade = assetStart.tempoEntreTrades
                                , delay_after_order = assetStart.delayEntreOrdens
                                , acceptable_loss_percentage = assetStart.acceptableLossPercentage
                                , stop_loss_percentage = assetStart.stopLossPercentage
                                , fallback_activated = assetStart.fallBackActivated,)
    
    totalExecucao:int = 1
    
    while(True):
        if(THREAD_LOCK):
            with thread_lock:
                print(f"[{MaTrader.operation_code}][{totalExecucao}] '{MaTrader.operation_code}'")
                MaTrader.execute()
                print(f"^ [{MaTrader.operation_code}][{totalExecucao}] time_to_sleep = '{MaTrader.time_to_sleep/60:.2f} min'")
                print(f"------------------------------------------------")
                totalExecucao += 1
        else:
            print(f"[{MaTrader.operation_code}][{totalExecucao}] '{MaTrader.operation_code}'")
            MaTrader.execute()
            print(f"^ [{MaTrader.operation_code}][{totalExecucao}] time_to_sleep = '{MaTrader.time_to_sleep/60:.2f} min'")
            print(f"------------------------------------------------")
            totalExecucao += 1
        time.sleep(MaTrader.time_to_sleep)


# Criando e iniciando uma thread para cada objeto
threads = []

for asset in assetsTraders:
    thread = threading.Thread(target=trader_loop, args=(asset,))
    thread.daemon = True  # Permite finalizar as threads ao encerrar o programa
    thread.start()
    threads.append(thread)
    
print("Threads iniciadas para todos os ativos.")

# O programa principal continua executando sem bloquear
try:
    while True:
        time.sleep(1)  # Mantenha o programa rodando
except KeyboardInterrupt:
    print("\nPrograma encerrado pelo usuário.")


