# pyMNI

[![Repo](https://img.shields.io/badge/GitHub-repo-blue?logo=github&logoColor=f5f5f5)](https://github.com/michelmetran/pyMNI)
[![PyPI - Version](https://img.shields.io/pypi/v/mni?logo=pypi&label=PyPI&color=blue)](https://pypi.org/project/mni/)

O Modelo Nacional de
Interoperabilidade ([MNI](https://www.cnj.jus.br/tecnologia-da-informacao-e-comunicacao/comite-nacional-de-gestao-de-tecnologia-da-informacao-e-comunicacao-do-poder-judiciario/modelo-nacional-de-interoperabilidade/))
do Conselho Nacional de Justiça ([CNJ](https://www.cnj.jus.br/)) é um padrão estabelecido para o intercâmbio de
informações de processos judiciais entre os diversos órgãos do Poder Judiciário e outras instituições. Ele foi
desenvolvido para garantir a integridade, inviolabilidade e segurança dos dados processuais, facilitando a comunicação e
a troca de informações entre sistemas diferentes.

O MNI utiliza a tecnologia de _WebService_ para permitir essa interoperabilidade, assegurando que os dados possam ser
acessados e compartilhados de maneira segura e eficiente. A implementação dos serviços do MNI é responsabilidade dos
tribunais, órgãos da justiça e instituições privadas que desejam aderir ao modelo.

| Wsdl                                                                                      | Fonte |
|-------------------------------------------------------------------------------------------|-------|
| [RJ](https://webserverseguro.tjrj.jus.br/MNI/Servico.svc?wsdl)                            | ...   |
| [SP](https://esaj.tjsp.jus.br/mniws/servico-intercomunicacao-2.2.2/intercomunicacao?wsdl) | ...   |

<br>

---

## Funções / Objetivo

- Validação dos números de processos judiciais, definidos por meio da Resolução CNJ nº 65/2008.
    - O cálculo do dígito verificador, segundo o TJRS, acerta em 99,4% dos casos. Avaliar os casos de
      erro. [TJRS](https://www.cnj.jus.br/wp-content/uploads/2011/02/tjrs.ppt)

<br>

---

## Referência

- https://github.com/ScurFelipe/validacao

<br>

---

## _TODO_

1. ...
