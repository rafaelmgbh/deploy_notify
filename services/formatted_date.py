from datetime import datetime

import pytz


class FormattedDate:
    @staticmethod
    def get_formatted_datetime():
        fuso_horario_brasil = pytz.timezone("America/Sao_Paulo")
        data_hora_local = datetime.now(fuso_horario_brasil)
        data_hora_utc = datetime.now(pytz.utc)
        data_hora_formatada_local = data_hora_local.strftime(
            "%d de %B de %Y %H:%M:%S"
        )
        data_hora_formatada_utc = data_hora_utc.strftime(
            "%d de %B de %Y %H:%M:%S"
        )
        mensagem = (
            f"Horário local (Brasil):  **{data_hora_formatada_local}"
            + f"**\n\n Horário do servidor (UTC):  **{data_hora_formatada_utc}"
        )
        return mensagem
