# pyMNI

[![Repo](https://img.shields.io/badge/GitHub-repo-blue?logo=github&logoColor=f5f5f5)](https://github.com/michelmetran/pyMNI)
[![PyPI - Version](https://img.shields.io/pypi/v/mni?logo=pypi&label=PyPI&color=blue)](https://pypi.org/project/mni/)<br>
[![Read the Docs](https://img.shields.io/readthedocs/pyMNI?logo=ReadTheDocs&label=Read%20The%20Docs)](https://pyMNI.readthedocs.io/)
[![Publish Python to PyPI](https://github.com/michelmetran/pyMNI/actions/workflows/publish-to-pypipoetry.yml/badge.svg)](https://github.com/michelmetran/pyMNI/actions/workflows/publish-to-pypipoetry.yml)

O Modelo Nacional de Interoperabilidade ([MNI](https://www.cnj.jus.br/tecnologia-da-informacao-e-comunicacao/comite-nacional-de-gestao-de-tecnologia-da-informacao-e-comunicacao-do-poder-judiciario/modelo-nacional-de-interoperabilidade/)) do Conselho Nacional de Justiça ([CNJ](https://www.cnj.jus.br/)) é um padrão estabelecido para o intercâmbio de informações de processos judiciais entre os diversos órgãos do Poder Judiciário e outras instituições. Ele foi desenvolvido para garantir a integridade, inviolabilidade e segurança dos dados processuais, facilitando a comunicação e a troca de informações entre sistemas diferentes.

O MNI utiliza a tecnologia de _web service_ para permitir essa interoperabilidade, assegurando que os dados possam ser acessados e compartilhados de maneira segura e eficiente. A implementação dos serviços do MNI é responsabilidade dos tribunais, órgãos da justiça e instituições privadas que desejam aderir ao modelo.

<a href="https://esaj.tjsp.jus.br/mniws/servico-intercomunicacao-2.2.2/intercomunicacao?wsdl">
<img src="./docs/assets/sp.png" alt="WSDL de SP" width="35%">
</a> <a href="https://webserverseguro.tjrj.jus.br/MNI/Servico.svc?wsdl">
<img src="./docs/assets/rj.png" alt="WSDL de RJ" width="35%">
</a>

Imagens obtidas no [Atlas Escolar IBGE](https://atlasescolar.ibge.gov.br/images/bandeiras/ufs/rj.png).

<br>

---

## Resolução nº 65/2011

O pacote também provê uma classe chamada `NumeroProcesso` para lidar com as validações dos números de processos judiciais definidas na Resolução CNJ nº 65/2008, que _"dispõe sobre a uniformização do número dos processos nos órgãos do Poder Judiciário e dá outras providências"_.

A classe faz o cálculo do dígito verificador, para avaliar se o número está correto. Segundo o [TJRS](https://www.cnj.jus.br/wp-content/uploads/2011/02/tjrs.ppt), o algoritmo usado pelo CNJ acerta em 99,4% dos casos. Necessário avaliar os casos de erro.

<br>

---

## _TODO_

1. Desenvolver documentação para o pacote
2. Passei de _MNI_ para _pyMNI_ e... não publica o pacote... "HTTP Error 400: The name 'pyMNI' is too similar to an existing project. See https://pypi.org/help/#project-name for more information. | b"<html>\n <head>\n <title>400 The name 'pyMNI' is too similar to an existing project. See https://pypi.org/help/#project-name for more information.\n \n <body>\n <h1>400 The name 'pyMNI' is too similar to an existing project. See https://pypi.org/help/#project-name for more information.\n The server could not comply with the request since it is either malformed or otherwise incorrect.<br/><br/>\nThe name &#x27;pyMNI&#x27; is too similar to an existing project. See https://pypi.org/help/#project-name for more information.\n\n\n \n""
