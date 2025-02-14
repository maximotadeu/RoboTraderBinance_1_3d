from dataclasses import dataclass
from typing import Optional

@dataclass
class AssetStartModel:        
    stockCode: str
    operationCode: str
    tradedQuantity: float
    candlePeriod: str

    # Ajustes técnicos    
    volatilityFactor: float = 0.5           # Interfere na antecipação e nos lances de compra de venda limitados
    acceptableLossPercentage: float = 0     # (Usar em base 100%) O quando o bot aceita perder de % (se for negativo, o bot só aceita lucro)
    stopLossPercentage: float = 5           # (Usar em base 100%) % Máxima de loss que ele aceita, em caso de não vender na ordem limitada
    fallBackActivated: bool = True          # Define se a estratégia de Fallback será usada (ela pode entrar comprada em mercados subindo)

    # Ajuste de tempos    
    tempoEntreTrades: int = 30 * 60    # Tempo que o bot espera para verificar o mercado (em segundos)
    delayEntreOrdens: int = 60 * 60    # Tempo que o bot espera depois de realizar uma ordem de compra ou venda (ajuda a diminuir trades de borda)

    buyPercentageProtection: float = 2 # (Não implementado) Quantos % abaixo do preço de compra será definida uma ordem de venda
    tradedPercentage: float = 100 # (Não implementado) Porcentagem do total da carteira, que será negociada
    