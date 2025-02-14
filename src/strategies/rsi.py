def getMovingAverageVergenceRSI(
        self, fast_window=7, slow_window=40, volatility_factor=0.7
    ):
        try:
            hysteresis = 0.001  # Define a histerese
            growth_threshold = 2.0  # Detectar crescimento quando o gradiente é duas vezes maior que o valor anterior
            correction_threshold = (
                0.3  # Detectar correção quando o gradiente diminui pelo menos 0.3
            )

            self.stock_data["ma_fast"] = (
                self.stock_data["close_price"].rolling(window=fast_window).mean()
            )
            self.stock_data["ma_slow"] = (
                self.stock_data["close_price"].rolling(window=slow_window).mean()
            )
            self.stock_data["volatility"] = (
                self.stock_data["close_price"].rolling(window=slow_window).std()
            )
            last_ma_fast = self.stock_data["ma_fast"].iloc[-1]
            last_ma_slow = self.stock_data["ma_slow"].iloc[-1]
            prev_ma_slow = self.stock_data["ma_slow"].iloc[-2]
            prev_ma_fast = self.stock_data["ma_fast"].iloc[-2]

            # instanciar a instância da classe RSICalculationClass
            # Após calcular o RSI
            self.indicators.calculate_rsi()

            # Verifique se a coluna 'rsi' existe e pegue o último valor
            if "rsi" in self.stock_data:
                last_rsi = self.stock_data["rsi"].iloc[-1]
            else:
                raise ValueError(
                    "Erro: a coluna 'rsi' não foi encontrada em 'self.stock_data' após o cálculo."
                )

            last_rsi = self.stock_data["rsi"].iloc[-1]

            last_volatility = self.stock_data["volatility"].iloc[-1]
            volatility = self.stock_data["volatility"][
                len(self.stock_data) - slow_window :
            ].mean()  # Média da volatilidade dos últimos n valores
            fast_gradient = last_ma_fast - prev_ma_fast
            slow_gradient = last_ma_slow - prev_ma_slow

            current_difference = last_ma_fast - last_ma_slow
            volatility_by_purshase = volatility * volatility_factor

            # Calcula a diferença do gradiente rápido e lento
            fast_gradient_diff = last_ma_fast - prev_ma_fast
            slow_gradient_diff = last_ma_slow - prev_ma_slow

            # CONDIÇÕES DE COMPRA
            if (
                current_difference > volatility * volatility_factor
                and last_volatility < volatility
                and last_rsi < self.rsi_upper
            ):
                ma_trade_decision = True  # Sinal de compra
                print(
                    "Compra: Diferença atual maior que volatilidade ajustada, última volatilidade menor e RSI abaixo do limite superior."
                )

            elif (
                last_ma_fast > last_ma_slow + hysteresis
                and fast_gradient > slow_gradient
            ):
                ma_trade_decision = True  # Sinal de compra
                print(
                    "Compra: MA rápida maior que MA lenta ajustada por histerese, e gradiente rápido maior que o lento."
                )

            elif (
                last_ma_fast > last_ma_slow + hysteresis
                and last_volatility > (volatility / 2)
                and fast_gradient > slow_gradient
            ):
                ma_trade_decision = True  # Sinal de compra
                print(
                    "Compra: MA rápida maior que MA lenta ajustada por histerese, volatilidade anterior maior que a metade da volatilidade atual, e gradiente rápido maior que o lento."
                )

            elif (
                current_difference > volatility * volatility_factor
                and last_volatility > volatility
                and fast_gradient > slow_gradient
                and last_rsi > self.rsi_lower
            ):
                ma_trade_decision = True  # Sinal de compra
                print(
                    "Compra: Diferença atual maior que volatilidade ajustada, última volatilidade maior, gradiente rápido maior que o lento, e RSI acima do limite inferior."
                )

            elif (
                volatility > last_volatility
                and last_rsi > 60
                and fast_gradient > slow_gradient
            ):
                ma_trade_decision = True  # Sinal de compra
                print(
                    "Compra: Volatilidade anterior maior que a atual, RSI acima de 60%, e gradiente rápido maior que o lento."
                )

            # CONDIÇÕES DE VENDA
            elif last_ma_fast < last_ma_slow - hysteresis:
                ma_trade_decision = False  # Sinal de venda
                print(
                    "Venda: MA rápida cruzou abaixo da MA lenta ajustada por histerese."
                )

            elif last_ma_fast > last_ma_slow:
                if last_volatility > volatility:
                    if fast_gradient < slow_gradient:
                        ma_trade_decision = False  # Sinal de venda
                        print(
                            "Venda: MA rápida maior que a lenta, mas a volatilidade anterior é maior que a atual, e o gradiente rápido menor que o lento."
                        )

            elif last_rsi < self.rsi_lower:
                if fast_gradient < slow_gradient:
                    ma_trade_decision = False  # Sinal de venda
                    print(
                        "Venda: RSI abaixo do limite inferior e gradiente rápido menor que o lento."
                    )

            # Detectar crescimento rápido no gradiente rápido
            elif fast_gradient_diff > growth_threshold * prev_ma_fast:
                print(
                    f"Crescimento Rápido Detectado: O gradiente rápido aumentou significativamente para {fast_gradient_diff}."
                )
                # Após o crescimento rápido, verificar se está começando a corrigir
                if fast_gradient < prev_ma_fast - correction_threshold:
                    ma_trade_decision = False  # Sinal de venda ou alerta
                    print(
                        f"Correção Detectada: O gradiente rápido começou a corrigir, caindo para {fast_gradient}."
                    )
                else:
                    print(
                        "Espera: O gradiente rápido ainda está subindo ou não começou a corrigir significativamente."
                    )
            else:
                print(
                    "Sem Crescimento Rápido: O gradiente rápido não cresceu significativamente."
                )

            print("-----")
            print(
                f"Estratégia executada: Moving Average com Volatilidade + Gradiente + RSI"
            )
            print(
                f"{self.operation_code}:\n {last_ma_fast:.3f} - Última Média Rápida \n {last_ma_slow:.3f} - Última Média Lenta"
            )
            print(f"Última Volatilidade: {last_volatility:.3f}")
            print(f"Média da Volatilidade: {volatility:.3f}")
            print(f"Diferença Atual das medias moveis: {current_difference:.3f}")
            print(f"volatibilidade * volatilidade_factor: {volatility_by_purshase:.3f}")
            print(f"Último RSI: {last_rsi:.3f}")
            print(
                f'Gradiente rápido: {fast_gradient:.3f} ({ "Subindo" if fast_gradient > 0 else "Descendo" })'
            )
            print(
                f'Gradiente lento: {slow_gradient:.3f} ({ "Subindo" if slow_gradient > 0 else "Descendo" })'
            )
            print(f'Decisão: {"Comprar" if ma_trade_decision == True else "Vender" }')
            print("-----")

            

        except IndexError:
            print(
                "Erro: Dados insuficientes para calcular a estratégia Moving Average Vergence."
            )
            return False

        return ma_trade_decision


import pandas as pd
from functions.logger import erro_logger


class TechnicalIndicators:
    """
    Classe para calcular indicadores técnicos.

    Attributes:
        stock_data (pd.DataFrame): DataFrame contendo os dados do ativo, com uma coluna 'close_price'.
        rsi_period (int): Período para o cálculo do RSI (padrão: 14).

    Methods:
        calculate_rsi(): Calcula o Índice de Força Relativa (RSI) e adiciona ao DataFrame.
    """

    def __init__(self, stock_data, rsi_period=14):
        """
        Inicializa a classe TechnicalIndicators.

        Args:
            stock_data (pd.DataFrame): DataFrame com os dados do ativo. Deve conter uma coluna 'close_price'.
            rsi_period (int): Período para cálculo do RSI. Padrão: 14.
        """
        self.stock_data = stock_data
        self.rsi_period = rsi_period

    def calculate_rsi(self):
        """
        Calcula o Índice de Força Relativa (RSI).

        Calcula o RSI usando a média móvel exponencial suavizada (SMMA) para ganhos e perdas.
        Adiciona uma nova coluna 'rsi' ao DataFrame stock_data.

        Returns:
            pd.DataFrame: O DataFrame stock_data com a coluna 'rsi' adicionada.
            None: se ocorrer algum erro.

        Raises:
            TypeError: Se stock_data não for um pandas DataFrame ou não contiver uma coluna 'close_price'.
            ValueError: se dados inválidos forem encontrados em 'close_price'
        """
        if not isinstance(self.stock_data, pd.DataFrame):
            raise TypeError("stock_data deve ser um pandas DataFrame.")

        if "close_price" not in self.stock_data.columns:
            raise TypeError("stock_data deve conter a coluna 'close_price'.")

        try:

            # Converte a coluna 'close_price' para numérico, substituindo erros por NaN
            self.stock_data["close_price"] = pd.to_numeric(
                self.stock_data["close_price"], errors="coerce"
            )

            # Calcula a diferença entre os preços de fechamento
            delta = self.stock_data["close_price"].diff()

            # Calcula os ganhos e perdas
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)

            # Calcula a SMMA dos ganhos e perdas
            avg_gain = gain.ewm(span=self.rsi_period, adjust=False).mean()
            avg_loss = loss.ewm(span=self.rsi_period, adjust=False).mean()

            # Calcula o RS e o RSI
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            # Adiciona o RSI ao DataFrame
            self.stock_data["rsi"] = rsi
            return self.stock_data

        except (ValueError, TypeError) as e:
            erro = f"Erro ao tentar executar calculate_rsi em Technical Indicator: {e}"
            erro_logger.error(erro)  # Registra a mensagem de erro no bot_logger.
            return None  # Retorna None em caso de erro.