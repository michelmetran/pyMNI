"""
Módulo para manejar o WSDL

Michel Metran
Data: 17.01.2025
Atualizado em: 17.01.2025
"""

import pandas as pd
from caseconverter import snakecase
from zeep import Client, client
from zeep.cache import SqliteCache
from zeep.transports import Transport

import mni

# import zeep
# import xmltodict


class MNI(client.Client):
    def __init__(self, username, password, estado='sp', **kwargs):
        # Credenciais
        self.username = username
        self.password = password

        # # Parâmetros
        # self.list_operations = None
        # self.dict_operations = None
        # self.df_infos = None

        # Lista de WSDL
        self._dict_wsdl = {
            'sp': 'https://esaj.tjsp.jus.br/mniws/servico-intercomunicacao-2.2.2/intercomunicacao?wsdl',
            'rj': 'https://webserverseguro.tjrj.jus.br/MNI/Servico.svc?wsdl',
        }

        self.wsdl = self._dict_wsdl[estado]

        # Cache
        cache = SqliteCache(path='sqlite_pyMNI.db', timeout=60)
        transport = Transport(cache=cache)

        # Instância Client
        super().__init__(wsdl=self.wsdl, transport=transport)

    def consultar_processo(
        self,
        numero_processo: mni.NumeroProcesso,
        # Opcionais
        incluir_cabecalho: bool | None = True,
        incluir_movimentos: bool | None = True,
        incluir_documentos: bool | None = None,
    ):
        """

        :param numero_processo:
        :param incluir_cabecalho: Parâmetro apar
        :param incluir_movimentos:
        :param incluir_documentos:
        :return:
        """
        # Se "incluir_documentos" estiver habilitado,
        # não pode estar habilitado o "incluir_movimentos"
        result = self.service.consultarProcesso(
            idConsultante=self.username,
            senhaConsultante=self.password,
            numeroProcesso=numero_processo.texto,
            incluirCabecalho=incluir_cabecalho,
            incluirDocumentos=incluir_documentos,
            movimentos=incluir_movimentos,
            dataReferencia=None,
        )
        return result

    def consultar_documentos(
        self,
        numero_processo: mni.NumeroProcesso,
        # Opcionais
        # incluir_cabecalho: bool | None = None,
        # incluir_movimentos: bool | None = None,
        # incluir_documentos: bool | None = True
    ):
        """

        :param numero_processo:
        :param incluir_cabecalho: Parâmetro apar
        :param incluir_movimentos:
        :param incluir_documentos:
        :return:
        """
        # Se "incluir_documentos" estiver halibitado, não pode estar habilitado o "incluir_movimentos"
        result = self.service.consultarProcesso(
            idConsultante=self.username,
            senhaConsultante=self.password,
            numeroProcesso=numero_processo.texto,
            incluirCabecalho=None,
            incluirDocumentos=True,
            movimentos=None,
            # dataReferencia=None,
        )
        return result

    def obter_documentos(
        self,
        numero_processo: mni.NumeroProcesso,
        # Opcionais
        # incluir_cabecalho: bool | None = None,
        # incluir_movimentos: bool | None = None,
        # incluir_documentos: bool | None = True
        id_documento: str,
    ):
        """

        :param numero_processo: Número do processo judicial, completado com zeros na frente
        :param id_documento: No formato "278599514 - 4"

        :return:
        """
        # Se "incluir_documentos" estiver halibitado, não pode estar habilitado o "incluir_movimentos"
        result = self.service.consultarProcesso(
            idConsultante=self.username,
            senhaConsultante=self.password,
            numeroProcesso=numero_processo.texto,
            # incluirCabecalho=None,
            # incluirDocumentos=True,
            # movimentos=None,
            documento=id_documento,
            # dataReferencia=None,
        )
        return result

    def consultar_alteracao(self, numero_processo: mni.NumeroProcesso):
        """


        :param numero_processo:
        :return: hashCabecalho, hashMovimentacoes, hashDocumentos
        """
        try:
            result = self.service.consultarAlteracao(
                idConsultante=self.username,
                senhaConsultante=self.password,
                numeroProcesso=numero_processo.inteiro,
                # incluirCabecalho=True,
                # incluirDocumentos=True,
                # movimentos=True,
                # dataReferencia=None,
            )
        except Exception as e:
            raise e

        if result.sucesso:
            print(result.sucesso, 34232132132132)
            return result


if __name__ == '__main__':
    import os

    import mni
    from dotenv import load_dotenv

    # Credenciais
    load_dotenv()
    TJSP_MNI_USERNAME = os.getenv('TJSP_MNI_USERNAME')
    TJSP_MNI_PASSWORD = os.getenv('TJSP_MNI_PASSWORD')

    # Número do Processo
    # num = mni.NumeroProcesso(numero='1512315-89.2022.8.26.0268')
    num = mni.NumeroProcesso(
        numero='0139541-45.2007.8.26.0053'
    )  # MPSP não é parte
    num = mni.NumeroProcesso(numero='1503015-13.2023.8.26.0319')

    # MNI TJSP
    api = MNI(username=TJSP_MNI_USERNAME, password=TJSP_MNI_PASSWORD)
    resultado = api.consultar_processo(
        # Processo
        numero_processo=num,
        # Parâmetros
        incluir_cabecalho=True,
        incluir_movimentos=True,
        # incluir_documentos=True
    )

    resultado = api.consultar_documentos(numero_processo=num)
    resultado = api.obter_documentos(
        numero_processo=num, id_documento='278755780 - 1'
    )

    # # Se for pesquisar documento, precisa estar None
    # resultado = api.consultar_processo(
    #     # Processo
    #     numero_processo=num,
    #     # Parâmetros
    #     incluir_cabecalho=None,
    #     incluir_movimentos=None,
    #     incluir_documentos=True
    # )
    # resultado = api.consultar_alteracao(numero_processo=num)

    print(resultado)
