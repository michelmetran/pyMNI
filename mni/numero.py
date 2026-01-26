"""
Módulo para manipulação de números de processos judiciais,
conforme Resolução CNJ nº 65, de 16.12.2008

Michel Metran
Data: 16.01.2025
Atualizado em: 16.01.2025
"""

import re
import warnings


class NumeroProcesso:

    def __init__(self, numero: str | int, pad_zeros: bool = True):
        """
        Objeto para manipular o Número de Processos Judiciais, definido conforme Resolução CNJ n.º 65/2008

        :param numero: Número do Processo Judicial, em format string (`1512315-89.2022.8.26.0268`) ou inteiro.
        :param pad_zeros: Define se a função irá preencher com zeros na frente do número.
        """

        self.numero = numero

        # Define o padrão de formatação usando regex
        self.pattern = r'(\d{7})(\d{2})(\d{4})(\d{1})(\d{2})(\d{4})'

        self.dict_id_orgao = {
            1: 'Supremo Tribunal Federal',
            2: 'Conselho Nacional de Justiça',
            3: 'Superior Tribunal de Justiça',
            4: 'Justiça Federal',
            5: 'Justiça do Trabalho',
            6: 'Justiça Eleitoral',
            7: 'Justiça Militar da União',
            8: 'Justiça dos Estados e do Distrito Federal e Territórios',
            9: 'Justiça Militar Estadual',
        }

        self.dict_id_tribunal = {
            '1.00': 'Supremo Tribunal Federal',
            '2.00': 'Conselho Nacional de Justiça',
            '3.00': 'Superior Tribunal de Justiça',
            '5.00': 'Tribunal Superior do Trabalho',
            '6.00': 'Tribunal Superior Eleitoral',
            '7.00': 'Superior Tribunal Militar',
            # II, § 5º, Art. 1, Resolução CNJ 65/2008
            '4.90': 'Conselho da Justiça Federal',
            '5.90': 'Conselho Superior da Justiça do Trabalho',
            # III, § 5º, Art. 1, Resolução CNJ 65/2008
            '4.01': 'Tribunal Regional Federal da 1ª Região',
            '4.02': 'Tribunal Regional Federal da 2ª Região',
            '4.03': 'Tribunal Regional Federal da 3ª Região',
            '4.04': 'Tribunal Regional Federal da 4ª Região',
            '4.05': 'Tribunal Regional Federal da 5ª Região',
            '4.01.9001': 'Turma Recursal do Tribunal Regional Federal da 1ª Região',
            '4.02.9001': 'Turma Recursal do Tribunal Regional Federal da 2ª Região',
            '4.03.9001': 'Turma Recursal do Tribunal Regional Federal da 3ª Região',
            '4.04.9001': 'Turma Recursal do Tribunal Regional Federal da 4ª Região',
            '4.05.9001': 'Turma Recursal do Tribunal Regional Federal da 5ª Região',
            '4.01.0010': 'Subseção Judiciária do Tribunal Regional Federal da 1ª Região',
            '4.02.0010': 'Subseção Judiciária do Tribunal Regional Federal da 2ª Região',
            '4.03.0010': 'Subseção Judiciária do Tribunal Regional Federal da 3ª Região',
            '4.04.0010': 'Subseção Judiciária do Tribunal Regional Federal da 4ª Região',
            '4.05.0010': 'Subseção Judiciária do Tribunal Regional Federal da 5ª Região',
            # IV, § 5º, Art. 1, Resolução CNJ 65/2008
            '5.01': 'Tribunal Regional do Trabalho da 1ª Região',
            '5.02': 'Tribunal Regional do Trabalho da 2ª Região',
            '5.03': 'Tribunal Regional do Trabalho da 3ª Região',
            '5.04': 'Tribunal Regional do Trabalho da 4ª Região',
            '5.05': 'Tribunal Regional do Trabalho da 5ª Região',
            '5.06': 'Tribunal Regional do Trabalho da 6ª Região',
            '5.07': 'Tribunal Regional do Trabalho da 7ª Região',
            '5.08': 'Tribunal Regional do Trabalho da 8ª Região',
            '5.09': 'Tribunal Regional do Trabalho da 9ª Região',
            '5.10': 'Tribunal Regional do Trabalho da 10ª Região',
            '5.11': 'Tribunal Regional do Trabalho da 11ª Região',
            '5.12': 'Tribunal Regional do Trabalho da 12ª Região',
            '5.13': 'Tribunal Regional do Trabalho da 13ª Região',
            '5.14': 'Tribunal Regional do Trabalho da 14ª Região',
            '5.15': 'Tribunal Regional do Trabalho da 15ª Região',
            '5.16': 'Tribunal Regional do Trabalho da 16ª Região',
            '5.17': 'Tribunal Regional do Trabalho da 17ª Região',
            '5.18': 'Tribunal Regional do Trabalho da 18ª Região',
            '5.19': 'Tribunal Regional do Trabalho da 19ª Região',
            '5.20': 'Tribunal Regional do Trabalho da 20ª Região',
            '5.21': 'Tribunal Regional do Trabalho da 21ª Região',
            '5.22': 'Tribunal Regional do Trabalho da 22ª Região',
            '5.23': 'Tribunal Regional do Trabalho da 23ª Região',
            '5.24': 'Tribunal Regional do Trabalho da 24ª Região',
            '5.01.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 1ª Região',
            '5.02.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 2ª Região',
            '5.03.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 3ª Região',
            '5.04.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 4ª Região',
            '5.05.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 5ª Região',
            '5.06.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 6ª Região',
            '5.07.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 7ª Região',
            '5.08.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 8ª Região',
            '5.09.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 9ª Região',
            '5.10.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 10ª Região',
            '5.11.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 11ª Região',
            '5.12.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 11ª Região',
            '5.13.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 13ª Região',
            '5.14.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 14ª Região',
            '5.15.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 15ª Região',
            '5.16.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 16ª Região',
            '5.17.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 17ª Região',
            '5.18.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 18ª Região',
            '5.19.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 19ª Região',
            '5.20.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 20ª Região',
            '5.21.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 21ª Região',
            '5.22.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 22ª Região',
            '5.23.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 23ª Região',
            '5.24.0197': 'Vara do Trabalho do Tribunal Regional do Trabalho da 24ª Região',
            # V, § 5º, Art. 1, Resolução CNJ 65/2008
            '6.01': 'Tribunal Regional Eleitoral do Acre',
            '6.02': 'Tribunal Regional Eleitoral de Alagoas',
            '6.03': 'Tribunal Regional Eleitoral do Amapá',
            '6.04': 'Tribunal Regional Eleitoral do Amazonas',
            '6.05': 'Tribunal Regional Eleitoral da Bahia',
            '6.06': 'Tribunal Regional Eleitoral do Ceará',
            '6.07': 'Tribunal Regional Eleitoral do Distrito Federal e Territórios',
            '6.08': 'Tribunal Regional Eleitoral do Espírito Santo',
            '6.09': 'Tribunal Regional Eleitoral de Goiás',
            '6.10': 'Tribunal Regional Eleitoral do Maranhão',
            '6.11': 'Tribunal Regional Eleitoral do Mato Grosso',
            '6.12': 'Tribunal Regional Eleitoral do Mato Grosso do Sul',
            '6.13': 'Tribunal Regional Eleitoral de Minas Gerais',
            '6.14': 'Tribunal Regional Eleitoral do Pará',
            '6.15': 'Tribunal Regional Eleitoral da Paraíba',
            '6.16': 'Tribunal Regional Eleitoral do Paraná',
            '6.17': 'Tribunal Regional Eleitoral de Pernambuco',
            '6.18': 'Tribunal Regional Eleitoral do Piauí',
            '6.19': 'Tribunal Regional Eleitoral do Rio de Janeiro',
            '6.20': 'Tribunal Regional Eleitoral do Rio Grande do Norte',
            '6.21': 'Tribunal Regional Eleitoral do Rio Grande do Sul',
            '6.22': 'Tribunal Regional Eleitoral de Rondônia',
            '6.23': 'Tribunal Regional Eleitoral de Roraima',
            '6.24': 'Tribunal Regional Eleitoral de Santa Catarina',
            '6.25': 'Tribunal Regional Eleitoral de Sergipe',
            '6.26': 'Tribunal Regional Eleitoral de São Paulo',
            '6.27': 'Tribunal Regional Eleitoral do Tocantins',
            '6.01.0342': 'Zona Eleitoral do Acre',
            '6.02.0342': 'Zona Eleitoral do Alagoas',
            '6.03.0342': 'Zona Eleitoral do Amapá',
            '6.04.0342': 'Zona Eleitoral do Amazonas',
            '6.05.0342': 'Zona Eleitoral da Bahia',
            '6.06.0342': 'Zona Eleitoral do Ceará',
            '6.07.0342': 'Zona Eleitoral do Distrito Federal e Territórios',
            '6.08.0342': 'Zona Eleitoral do Espirito Santo',
            '6.09.0342': 'Zona Eleitoral de Goiás',
            '6.10.0342': 'Zona Eleitoral do  Maranhão',
            '6.11.0342': 'Zona Eleitoral do Mato Grosso ',
            '6.12.0342': 'Zona Eleitoral do  Mato Grosso do Sul',
            '6.13.0342': 'Zona Eleitoral de Minas Gerais',
            '6.14.0342': 'Zona Eleitoral do Pará',
            '6.15.0342': 'Zona Eleitoral da Paraíba',
            '6.16.0342': 'Zona Eleitoral do Paraná',
            '6.17.0342': 'Zona Eleitoral do Pernambuco',
            '6.18.0342': 'Zona Eleitoral do Piauí',
            '6.19.0342': 'Zona Eleitoral do Rio de Janeiro',
            '6.20.0342': 'Zona Eleitoral do Rio Grande do Norte ',
            '6.21.0342': 'Zona Eleitoral do Rio Grande do Sul',
            '6.22.0342': 'Zona Eleitoral de Rondônia',
            '6.23.0342': 'Zona Eleitoral de Roraima',
            '6.24.0342': 'Zona Eleitoral de Santa Catarina',
            '6.25.0342': 'Zona Eleitoral de Sergipe',
            '6.26.0342': 'Zona Eleitoral de São Paulo',
            '6.27.0342': 'Zona Eleitoral do Tocantins',
            # VI, § 5º, Art. 1, Resolução CNJ 65/2008
            '7.01': '1ª Circunscrição Judiciária Militar',
            '7.02': '2ª Circunscrição Judiciária Militar',
            '7.03': '3ª Circunscrição Judiciária Militar',
            '7.04': '4ª Circunscrição Judiciária Militar',
            '7.05': '5ª Circunscrição Judiciária Militar',
            '7.06': '6ª Circunscrição Judiciária Militar',
            '7.07': '7ª Circunscrição Judiciária Militar',
            '7.08': '8ª Circunscrição Judiciária Militar',
            '7.09': '9ª Circunscrição Judiciária Militar',
            '7.10': '10ª Circunscrição Judiciária Militar',
            '7.11': '11ª Circunscrição Judiciária Militar',
            '7.12': '12ª Circunscrição Judiciária Militar',
            '7.01.0072': 'Auditoria Militar da 1ª Circunscrição Judiciária Militar',
            '7.02.0072': 'Auditoria Militar da 2ª Circunscrição Judiciária Militar',
            '7.03.0072': 'Auditoria Militar da 3ª Circunscrição Judiciária Militar',
            '7.04.0072': 'Auditoria Militar da 4ª Circunscrição Judiciária Militar',
            '7.05.0072': 'Auditoria Militar da 5ª Circunscrição Judiciária Militar',
            '7.06.0072': 'Auditoria Militar da 6ª Circunscrição Judiciária Militar',
            '7.07.0072': 'Auditoria Militar da 7ª Circunscrição Judiciária Militar',
            '7.08.0072': 'Auditoria Militar da 8ª Circunscrição Judiciária Militar',
            '7.09.0072': 'Auditoria Militar da 9ª Circunscrição Judiciária Militar',
            '7.10.0072': 'Auditoria Militar da 10ª Circunscrição Judiciária Militar',
            '7.11.0072': 'Auditoria Militar da 11ª Circunscrição Judiciária Militar',
            '7.12.0072': 'Auditoria Militar da 12ª Circunscrição Judiciária Militar',
            # VII, § 5º, Art. 1, Resolução CNJ 65/2008
            '8.01': 'Tribunal de Justiça do Acre',
            '8.02': 'Tribunal de Justiça de Alagoas',
            '8.03': 'Tribunal de Justiça do Amapá',
            '8.04': 'Tribunal de Justiça do Amazonas',
            '8.05': 'Tribunal de Justiça da Bahia',
            '8.06': 'Tribunal de Justiça do Ceará',
            '8.07': 'Tribunal de Justiça do Distrito Federal e Territórios',
            '8.08': 'Tribunal de Justiça do Espírito Santo',
            '8.09': 'Tribunal de Justiça de Goiás',
            '8.10': 'Tribunal de Justiça do Maranhão',
            '8.11': 'Tribunal de Justiça do Mato Grosso',
            '8.12': 'Tribunal de Justiça do Mato Grosso do Sul',
            '8.13': 'Tribunal de Justiça de Minas Gerais',
            '8.14': 'Tribunal de Justiça do Pará',
            '8.15': 'Tribunal de Justiça da Paraíba',
            '8.16': 'Tribunal de Justiça do Paraná',
            '8.17': 'Tribunal de Justiça de Pernambuco',
            '8.18': 'Tribunal de Justiça do Piauí',
            '8.19': 'Tribunal de Justiça do Rio de Janeiro',
            '8.20': 'Tribunal de Justiça do Rio Grande do Norte',
            '8.21': 'Tribunal de Justiça do Rio Grande do Sul',
            '8.22': 'Tribunal de Justiça de Rondônia',
            '8.23': 'Tribunal de Justiça de Roraima',
            '8.24': 'Tribunal de Justiça de Santa Catarina',
            '8.25': 'Tribunal de Justiça de Sergipe',
            '8.26': 'Tribunal de Justiça de São Paulo',
            '8.27': 'Tribunal de Justiça do Tocantins',
            '8.01.9001': 'Turma Recursal do Tribunal de Justiça do Acre',
            '8.02.9001': 'Turma Recursal do Tribunal de Justiça de Alagoas',
            '8.03.9001': 'Turma Recursal do Tribunal de Justiça do Amapá',
            '8.04.9001': 'Turma Recursal do Tribunal de Justiça do Amazonas',
            '8.05.9001': 'Turma Recursal do Tribunal de Justiça da Bahia',
            '8.06.9001': 'Turma Recursal do Tribunal de Justiça do Ceará',
            '8.07.9001': 'Turma Recursal do Tribunal de Justiça do Distrito Federal e Territórios',
            '8.08.9001': 'Turma Recursal do Tribunal de Justiça do Espírito Santo',
            '8.09.9001': 'Turma Recursal do Tribunal de Justiça de Goiás',
            '8.10.9001': 'Turma Recursal do Tribunal de Justiça do Maranhão',
            '8.11.9001': 'Turma Recursal do Tribunal de Justiça do Mato Grosso',
            '8.12.9001': 'Turma Recursal do Tribunal de Justiça do Mato Grosso do Sul',
            '8.13.9001': 'Turma Recursal do Tribunal de Justiça de Mina Gerais',
            '8.14.9001': 'Turma Recursal do Tribunal de Justiça Pará',
            '8.15.9001': 'Turma Recursal do Tribunal de Justiça da Paraíba',
            '8.16.9001': 'Turma Recursal do Tribunal de Justiça do Paraná',
            '8.17.9001': 'Turma Recursal do Tribunal de Justiça do Pernambuco',
            '8.18.9001': 'Turma Recursal do Tribunal de Justiça do Piauí',
            '8.19.9001': 'Turma Recursal do Tribunal de Justiça do Rio de Janeiro',
            '8.20.9001': 'Turma Recursal do Tribunal de Justiça do Rio Grande do Norte',
            '8.21.9001': 'Turma Recursal do Tribunal de Justiça do Rio Grande do Sul',
            '8.22.9001': 'Turma Recursal do Tribunal de Justiça de Rondônia',
            '8.23.9001': 'Turma Recursal do Tribunal de Justiça de Roraima',
            '8.24.9001': 'Turma Recursal do Tribunal de Justiça de Santa Catarina',
            '8.25.9001': 'Turma Recursal do Tribunal de Justiça de Sergipe',
            '8.26.9001': 'Turma Recursal do Tribunal de Justiça de São Paulo',
            '8.27.9001': 'Turma Recursal do Tribunal de Justiça do Tocantins',
            '8.01.0235': 'Foro de Origem de Tramitação do Acre',
            '8.02.0235': 'Foro de Origem de Tramitação de Alagoas',
            '8.03.0235': 'Foro de Origem de Tramitação do Amapá',
            '8.04.0235': 'Foro de Origem de Tramitação do Amazonas',
            '8.05.0235': 'Foro de Origem de Tramitação da Bahia',
            '8.06.0235': 'Foro de Origem de Tramitação do Ceará',
            '8.07.0235': 'Foro de Origem de Tramitação do Distrito Federal e Territórios',
            '8.08.0235': 'Foro de Origem de Tramitação do Espirito Santo',
            '8.09.0235': 'Foro de Origem de Tramitação de Goiás',
            '8.10.0235': 'Foro de Origem de Tramitação do Maranhão',
            '8.11.0235': 'Foro de Origem de Tramitação do Mato Grosso',
            '8.12.0235': 'Foro de Origem de Tramitação do Mato Grosso do Sul',
            '8.13.0235': 'Foro de Origem de Tramitação de Minas Gerais',
            '8.14.0235': 'Foro de Origem de Tramitação do Pará',
            '8.15.0235': 'Foro de Origem de Tramitação da Paraíba',
            '8.16.0235': 'Foro de Origem de Tramitação do Paraná',
            '8.17.0235': 'Foro de Origem de Tramitação do Pernambuco',
            '8.18.0235': 'Foro de Origem de Tramitação do Piauí',
            '8.19.0235': 'Foro de Origem de Tramitação do Rio Janeiro',
            '8.20.0235': 'Foro de Origem de Tramitação do Rio Grande do Norte',
            '8.21.0235': 'Foro de Origem de Tramitação do Rio Grande do Sul',
            '8.22.0235': 'Foro de Origem de Tramitação de Rondônia',
            '8.23.0235': 'Foro de Origem de Tramitação de Roraima',
            '8.24.0235': 'Foro de Origem de Tramitação de Santa Catarina',
            '8.25.0235': 'Foro de Origem de Tramitação de Sergipe',
            '8.26.0235': 'Foro de Origem de Tramitação de São Paulo',
            '8.27.0235': 'Foro de Origem de Tramitação do Tocantins',
            # VIII, § 5º, Art. 1, Resolução CNJ 65/2008
            '9.13': 'Tribunal de Justiça Militar do Estado de Minas Gerais',
            '9.21': 'Tribunal de Justiça Militar do Estado do Rio Grande do Sul',
            '9.26': 'Tribunal de Justiça Militar do Estado de São Paulo',
            '9.13.0008': 'Auditoria Militar do Estado de Minas Gerais',
            '9.21.0008': 'Auditoria Militar do Estado do Rio Grande do Sul',
            '9.26.0008': 'Auditoria Militar do Estado de São Paulo',
        }

        if isinstance(self.numero, str):
            if len(self.numero) == 25:
                self.check_string_format()

            elif len(self.numero) == 20:
                pass

            else:
                raise Exception(
                    f'O número em formato texto deve ter 20 ou 25 caracteres, obrigatoriamente. Tem {len(self.numero)}'
                )

            #
            self.numero = self.texto

        elif isinstance(self.numero, int):
            if len(str(self.numero)) == 20:
                self.numero = f'{self.numero:020}'

            else:
                if pad_zeros:
                    self.numero = f'{self.numero:020}'

                else:
                    raise Exception(
                        f'O número não tem 20 caracteres, tem {len(str(self.numero))}.'
                    )

        else:
            raise Exception('Deve ser int ou string')

        self.check_digito_verificador()

    def check_string_format(self):
        """
        Se é string, avaliar se está no formato correto
        """
        if not re.match(
            pattern=r'\d{7}\-\d{2}\.\d{4}.\d{1}.\d{2}.\d{4}',
            # pattern=self.pattern,
            string=self.numero,
        ):
            raise Exception(
                f'O número não está na formatação definida na Resolução CNJ 65/2008\nNNNNNNN-DD.AAAA.J.TR.OOOO'
            )

    @property
    def texto(self) -> str:
        """
        Mantém apenas números na string
        """
        
        n_processo = [int(digito) for digito in self.numero if digito.isdigit()]
        # print(n_processo)
        return ''.join(map(str, n_processo))

    @property
    def formatado(self) -> str:
        return re.sub(
            self.pattern, repl=r'\1-\2.\3.\4.\5.\6', string=str(self.numero)
        )

    @property
    def inteiro(self) -> int:
        return int(self.texto)

    @property
    def sequencial(self) -> int:
        return int(
            re.sub(pattern=self.pattern, repl=r'\1', string=str(self.numero))
        )

    @property
    def dv(self) -> int:
        return int(
            re.sub(pattern=self.pattern, repl=r'\2', string=str(self.numero))
        )

    @property
    def ano(self) -> int:
        return int(
            re.sub(pattern=self.pattern, repl=r'\3', string=str(self.numero))
        )

    @property
    def id_orgao(self) -> int:
        return int(
            re.sub(pattern=self.pattern, repl=r'\4', string=str(self.numero))
        )

    @property
    def id_tribunal(self) -> int:
        return int(
            re.sub(pattern=self.pattern, repl=r'\5', string=str(self.numero))
        )

    @property
    def id_unidade_origem(self) -> int:
        return int(
            re.sub(pattern=self.pattern, repl=r'\6', string=str(self.numero))
        )

    @property
    def orgao(self):
        return self.dict_id_orgao[self.id_orgao]

    @property
    def tribunal(self) -> str:
        try:
            # Há casos que o id_unidade_origem específica a Unidade/Tribunal
            if (
                (self.id_orgao == 4 and self.id_unidade_origem in (9001, 10))
                or (self.id_orgao == 5 and self.id_unidade_origem in (197,))
                or (self.id_orgao == 6 and self.id_unidade_origem in (342,))
                or (self.id_orgao == 7 and self.id_unidade_origem in (72,))
                or (
                    self.id_orgao == 8 and self.id_unidade_origem in (9001, 235)
                )
                or (self.id_orgao == 9 and self.id_unidade_origem in (8,))
            ):
                return self.dict_id_tribunal[
                    f'{self.id_orgao:01}.{self.id_tribunal:02}.{self.id_unidade_origem:04}'
                ]

            # N'outros casos é só id_orgao e id_tribunal
            else:
                return self.dict_id_tribunal[
                    f'{self.id_orgao:01}.{self.id_tribunal:02}'
                ]

        #
        except Exception as e:
            raise ValueError(
                f'Não encontrou o Tribunal para "{self.id_orgao:01}.{self.id_tribunal:02}"'
            )

    def check_digito_verificador(self):
        """
        Confere dígito verificador, utilizando as definições da Resolução CNJ nº 65/2008,
        que envolve a aplicação do algoritmo módulo 97 base 10.
        """
        # Define dv como 00
        dv = '00'

        # Obtém número do processo em int
        numero_processo_ajustado = int(
            f'{self.sequencial:07}{self.ano:04}{self.id_orgao:01}{self.id_tribunal:02}{self.id_unidade_origem:04}{dv}'
        )

        # Calcula dígito verificador
        digito_verificador_calculado = 98 - (numero_processo_ajustado % 97)

        #  Confere
        if digito_verificador_calculado == self.dv:
            return True

        else:
            warnings.warn(
                f'O dígito verificador calculado deu "{digito_verificador_calculado:02}" e o dígito do número inserido pelo usuário é "{self.dv:02}"'
            )
            return False

    def __repr__(self):
        return f'Processo Judicial nº "{self.formatado}"'


if __name__ == '__main__':
    num = NumeroProcesso(numero='1512315-89.2022.8.26.0268')

    num = NumeroProcesso(numero='0139541-45.2007.8.26.0053')
    num = NumeroProcesso(numero=1395414520078260053)

    print(f'O dígito verificador é {num.check_digito_verificador()}')
    # num = NumeroProcesso(numero='1512315-89.2022.8.26.0235')
    # num = NumeroProcesso(numero='1512315-89.2022.7.12.0072')
    # num = NumeroProcesso(numero='1512315-89.2022.8.26.9001')
    # print(num)
    # print(num.formatado)

    # num = NumeroProcesso(numero=23965891020248260000)
    print(num)
    print(f'O número formatado é "{num.formatado}"')
    print(f'O número em formato texto é "{num.texto}"')
    print(f'O número inteiro é "{num.inteiro}"')

    # Partes do Número
    print(f'O número sequencial é "{num.sequencial}"')
    print(f'O dígito verificador é "{num.dv}"')
    print(f'O ano é "{num.ano}"')
    print(f'O id_orgao é "{num.id_orgao}" e "{num.orgao}"')
    print(f'O id_tribunal é "{num.id_tribunal}" e "{num.tribunal}"')
    print(f'O id_unidade_origem é "{num.id_unidade_origem}"')

    # num = NumeroProcesso(numero=3965891020248260000, pad_zeros=True)
    # print(num)
    # print(num.formatado)
