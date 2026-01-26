"""
Módulo para manejar o WSDL
De maneira bem genérica
Similar ao usado em SCCNMP
br_cnmp

Michel Metran
Data: 17.01.2025
Atualizado em: 17.01.2025
"""

import pandas as pd
from caseconverter import snakecase
from zeep import Client, client
from zeep.transports import Transport

import mni

# import zeep
# import xmltodict


class WSDL(client.Client):
    def __init__(self, username, password, estado='sp', **kwargs):

        # Credenciais
        self.username = username
        self.password = password

        # Parâmetros
        self.list_operations = None
        self.dict_operations = None
        self.df_infos = None

        # Lista de WSDL
        self._dict_wsdl = {
            'sp': 'https://esaj.tjsp.jus.br/mniws/servico-intercomunicacao-2.2.2/intercomunicacao?wsdl',
            'rj': 'https://webserverseguro.tjrj.jus.br/MNI/Servico.svc?wsdl',
        }
        self.wsdl2 = self._dict_wsdl[estado]
        # self.client = Client(wsdl=self.wsdl2)
        super().__init__(
            wsdl=self.wsdl2,
            # transport=Transport(session=session)
        )

    def get_infos(self) -> pd.DataFrame:
        """
        Cria uma tabela com todas as operações (funções),
        bem como parâmetros necessários,
        disponíveis no servidor SOAP do CNMP.

        :return: dataframe com todas informações do servidor SOAP.
        """
        list_rows = []
        dict_rows = {}

        # Services
        for service in self.wsdl.services.values():
            dict_rows.update({'service': service.name})

            # Port
            for port in service.ports.values():
                dict_rows.update({'port': port.name})

                # Operations (Functions)
                operations = port.binding._operations.values()
                for operation in operations:
                    dict_rows.update({'method': operation.name})

                    # Parameters
                    parameters = operation.input.body.type.elements
                    for param in parameters:
                        dict_rows.update({'param name': param[1].name})
                        dict_rows.update({'param type': param[1].type.name})
                        dict_rows.update({'param optl': param[1].is_optional})
                        list_rows.append(dict_rows.copy())

        self.df_infos = pd.DataFrame(list_rows)
        return self.df_infos

    def get_operations(self) -> list:
        """
        Lista todas as operações (funções)
        disponíveis no servidor SOAP do CNMP

        :return: lista, em snake case, das operações possíveis
        """
        if self.df_infos is None:
            self.get_infos()

        dict_operations = {}
        for item in list(set(self.df_infos['method'])):
            dict_operations.update({snakecase(item): item})

        # Operations
        self.dict_operations = dict_operations
        self.list_operations = [k for k, v in dict_operations.items()]
        return self.list_operations

    def request(
        self,
        method: str,
        params_ignore: list,
        param_print: bool = False,
        *args,
        **kwargs,
    ):
        """
        Faz a solicitação para o servidor SOAP.
        kwargs: print_out

        :param method: Qual a operação (função) se será solicitada.
        :param params_ignore: Lista de parâmetros que deverão ser ignorados na verificação se estão listados, como kwargs, ou não.
        :param param_print: Define se será "printado" o output com informações dos parâmetros
        :return: Retorna os dados da requisição, que deverão ser trabalhados posteriormente.
        """
        if self.df_infos is None:
            self.get_infos()

        if self.list_operations is None:
            self.get_operations()

        if method not in self.list_operations:
            raise NameError(
                f'O método precisa estar entre {self.list_operations}'
            )

        # Convert Snake Case do Camel Case
        method_camelcase = self.dict_operations[method]

        # Create Dataframe Filtered
        df = self.df_infos[self.df_infos['method'] == method_camelcase]
        df = df.reset_index(inplace=False, drop=True)
        if param_print:
            print(df[['param name', 'param type', 'param optl']])

        # Exclui os parâmetros ignorados pelo usuário
        # Feito para excluir usuário e senha
        list_params = list(df['param name'])
        for item_del in params_ignore:
            while item_del in list_params:
                list_params.remove(item_del)

        # Avalia se os parâmetros necessários, após a exclusão dos ignorados,
        # constam nos kwargs
        list_kwargs = list(kwargs.keys())
        list_params_user = [x for x in list_params if x not in list_kwargs]
        if len(list_params_user) > 0:
            raise NameError(f'Está faltando o parâmetro: {list_params_user}')

        # Results
        return self.service[method_camelcase](
            # idConsultante=self.username,
            # senhaConsultante=self.password,
            *args,
            **kwargs,
        )


if __name__ == '__main__':
    import os

    import mni
    from dotenv import load_dotenv

    # Credenciais
    load_dotenv()
    TJSP_MNI_USERNAME = os.getenv('TJSP_MNI_USERNAME')
    TJSP_MNI_PASSWORD = os.getenv('TJSP_MNI_PASSWORD')

    # Número do Processo
    num = mni.NumeroProcesso(numero='1512315-89.2022.8.26.0268')

    # MNI TJSP
    api = WSDL(username=TJSP_MNI_USERNAME, password=TJSP_MNI_PASSWORD)
    # resultado = api.consultar_processo(numero_processo=num)
    # resultado = api.consultar_alteracao(numero_processo=num)
    # resultado = api.get_infos()
    # resultado = api.get_operations()
    resultado = api.request(
        method='consultar_processo',
        idConsultante=TJSP_MNI_USERNAME,
        senhaConsultante=TJSP_MNI_PASSWORD,
        numeroProcesso=num.texto,
        param_print=True,
        params_ignore=[
            'dataReferencia',
            'movimentos',
            'incluirCabecalho',
            'incluirDocumentos',
            'documento',
        ],
    )

    print(resultado)
