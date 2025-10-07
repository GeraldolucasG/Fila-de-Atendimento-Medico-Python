# Fila-de-Atendimento-Medico-Python
Implementar em Python, uma estrutura de dados baseada em listas encadeadas para simular o gerenciamento de uma fila de espera em um consultório médico. O sistema permitirá a inclusão, alteração e remoção de pacientes na fila, além de monitorar o consumo de memória a cada operação realizada.

# Descrição do Projeto

Este projeto implementa um sistema de fila de atendimento hospitalar em Python, utilizando listas duplamente encadeadas para o gerenciamento dinâmico de pacientes.  
Cada paciente possui prioridade e o sistema segue regras específicas de atendimento (como a regra 1:7), além de monitorar o uso de memória durante todas as operações (adição, remoção e alteração).

# Colaboradores
Matheus de Sousa Evangelista.

Geraldo Lucas Guimarães Santiago da Silva.

Davi Luíz Marques Alves.

# Estrutura de Dados

Classe PacienteNode
Representa cada nó da lista duplamente encadeada.

Atributos:
- nome: nome do paciente (string)
- idade: idade (int)
- prioridade: 1 = Normal | 2 = Prioritário

A classe também redefine __sizeof__() para cálculo detalhado de memória.

Classe FilaDeAtendimento
Gerencia toda a lista de pacientes e suas operações.

*Principais atributos:*
- inicio: primeiro paciente da fila
- fim: último paciente da fila
- _ultimo_foi_P: flag booleana usada na regra de alternância de atendimento

---
Funcionalidades Principais

1. Adicionar Paciente
fila.adicionar_paciente(nome, idade, prioridade)
- Insere um novo paciente na posição correta da fila.  
- Pacientes *prioritários (P)* sempre ficam *antes* dos *normais (N)*.  
- O programa mostra o consumo de memória *antes e depois da inserção*.

---
2. Remover Paciente (Atendimento)
fila.remover_paciente()
- Remove o paciente a ser atendido, considerando:
  - *Regra 1:7* — Para cada 7 pacientes prioritários atendidos, 1 paciente normal é chamado.
  - Alternância entre P e N quando a regra está ativa.
---

3. Alterar Dados de um Paciente
fila.alterar_dados(nome_antigo, novo_nome, nova_idade, nova_prioridade)
- Permite alterar nome, idade ou prioridade.
- Caso a *prioridade seja alterada, o paciente é **reposicionado automaticamente* na fila.
- Também exibe o log de memória.

---
4. *Visualizar Fila*
fila.display()
Mostra a fila do *início ao fim*, indicando a prioridade (P/N).

5. Visualizar Fila Inversa
fila.display_inverso()
Mostra a fila do *fim ao início*.
---
6. Monitoramento de Memória
Cada operação (adição, remoção, alteração)

Operação: Adicionar Paciente (Maria)
Total ANTES: 8752 bytes
Total DEPOIS: 9540 bytes
DIFERENÇA: +788 bytes
----------------------------------
Essas informações ajudam a acompanhar o uso de memória em tempo real.

Em seguida, o programa entra em modo interativo com o seguinte menu:
--- MENU --- Comandos: add | remover | alterar | inverso | sair
Comandos disponíveis

| Comando | Exemplo | Descrição |
|----------|----------|-----------|
| add | add Maria 50 P | Adiciona paciente (nome, idade, prioridade) |
| remover | remover | Remove o próximo paciente da fila |
| alterar | alterar Gabriel Gabi 71 N | Altera nome, idade ou prioridade |
| alterar | alterar Monica - - P | Mantém dados com - e altera apenas a prioridade |
| inverso | inverso | Mostra a fila do fim para o início |
| sair | sair | Encerra o programa |

---
Exemplo de Execução
--- Fila Atual (Início -> Fim) ---
[ Gabriel (P) ] --> [ Helio (P) ] --> [ Pedro (P) ] --> [ Bruno (P) ] --> [ Teresa (N) ] --> [ Monica (N) ] --> [ Irene (N) ] --> [ Felipe (N) ] --> [ Victor (N) ] --> [ Alice (N) ] --> Final

Digite o comando: remover

Regra 1:7 ATIVA
Chamando paciente Prioritário mais antigo: Gabriel
Paciente 'Gabriel' (P) atendido.
Próximo na fila: 'Helio (P)'.
----
Conceitos Utilizados
- Estruturas dinâmicas (lista duplamente encadeada)  
- Regras condicionais e alternância lógica  
- Encapsulamento e orientação a objetos  
- Monitoramento de memória com sys.getsizeof()  
- Manipulação de nós (inserção, remoção e reposicionamento)
