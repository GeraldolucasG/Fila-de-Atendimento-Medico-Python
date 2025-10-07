import sys

class PacienteNode:
    def __init__(self, nome: str, idade: int, prioridade: int):
        self.nome = nome
        self.idade = idade
        self.prioridade = prioridade
        self.proximo = None
        self.anterior = None

class FilaDeAtendimento:
    def __init__(self):
        self.inicio = None
        self.fim = None
        self.ultimo_atendido_prioritario = None

    def calcular_memoria_total(self):
        """Estimativa simples usando sys.getsizeof para o container e nós."""
        mem_total = sys.getsizeof(self)
        temp = self.inicio
        seen = set()
        while temp:
            obj_id = id(temp)
            if obj_id not in seen:
                mem_total += sys.getsizeof(temp)
                seen.add(obj_id)
            temp = temp.proximo
        return mem_total

    def _print_memoria(self, antes, depois):
        print(f"Memória antes:  {antes} bytes")
        print(f"Memória depois: {depois} bytes")
        print(f"Diferença:      {depois - antes} bytes")

    def iter_nodes(self):
        cur = self.inicio
        while cur:
            yield cur
            cur = cur.proximo

    def contar_pacientes(self):
        temp = self.inicio
        count_P = 0
        count_N = 0
        while temp:
            if temp.prioridade == 2:
                count_P += 1
            else:
                count_N += 1
            temp = temp.proximo
        return count_P, count_N

    def encontrar_ultimo_prioritario(self):
        """Retorna o último nó cujo prioridade == 2 (ou None)."""
        cur = self.inicio
        ultimo = None
        while cur:
            if cur.prioridade == 2:
                ultimo = cur
            cur = cur.proximo
        return ultimo

    def display(self):
        print("\n--- Fila Atual ---")
        if self.inicio is None:
            print("(vazia)")
            return
        partes = []
        temp = self.inicio
        while temp:
            etiqueta = "(P)" if temp.prioridade == 2 else "(N)"
            partes.append(f"[ {temp.nome} {etiqueta} ]")
            temp = temp.proximo
        print(" --> ".join(partes))

    def display_inverso(self):
        print("\n--- Fila Inversa ---")
        if self.fim is None:
            print("(vazia)")
            return
        partes = []
        temp = self.fim
        while temp:
            etiqueta = "(P)" if temp.prioridade == 2 else "(N)"
            partes.append(f"[ {temp.nome} {etiqueta} ]")
            temp = temp.anterior
        print(" --> ".join(partes))

    def adicionar_paciente(self, nome: str, idade: int, prioridade: int):
        print(f"\n-> Adicionando '{nome}' (idade {idade}) [{'P' if prioridade==2 else 'N'}] ...")
        mem_antes = self.calcular_memoria_total()

        novo = PacienteNode(nome, idade, prioridade)

        if self.inicio is None:
            self.inicio = self.fim = novo
        else:
            if prioridade == 2:
                ultimo_p = self.encontrar_ultimo_prioritario()
                if ultimo_p is None:
                    novo.proximo = self.inicio
                    self.inicio.anterior = novo
                    self.inicio = novo
                else:
                    novo.proximo = ultimo_p.proximo
                    novo.anterior = ultimo_p
                    ultimo_p.proximo = novo
                    if novo.proximo:
                        novo.proximo.anterior = novo
                    else:
                        self.fim = novo
            else:
                self.fim.proximo = novo
                novo.anterior = self.fim
                self.fim = novo

        mem_depois = self.calcular_memoria_total()
        self._print_memoria(mem_antes, mem_depois)

    def remover_paciente(self):
        if self.inicio is None:
            print("\n-> Fila de atendimento já está vazia.")
            return

        print("\n-> Removendo paciente...")
        mem_antes = self.calcular_memoria_total()
        count_P, count_N = self.contar_pacientes()
        print(f"Status da fila: {count_P} prioritários (P) e {count_N} normais (N).")

        regra_ativa = (count_P > 0 and count_N > 0 and (count_P / count_N) >= (1/7))

        paciente_a_remover = None

        if not regra_ativa:
            paciente_a_remover = self.inicio
        else:
            print("Regra 1:7 ATIVADA. Aplicando alternância P <-> N na chamada.")
            preferir_prioritario = True
            if self.ultimo_atendido_prioritario is True:
                preferir_prioritario = False
            if preferir_prioritario:
                temp = self.inicio
                while temp:
                    if temp.prioridade == 2:
                        paciente_a_remover = temp
                        break
                    temp = temp.proximo
                if paciente_a_remover is None:
                    paciente_a_remover = self.inicio
            else:
                temp = self.inicio
                while temp:
                    if temp.prioridade == 1:
                        paciente_a_remover = temp
                        break
                    temp = temp.proximo
                if paciente_a_remover is None:
                    paciente_a_remover = self.inicio

        if paciente_a_remover is None:
            print("Erro inesperado: nenhum paciente encontrado para remoção.")
            return

        print(f"Paciente atendido: '{paciente_a_remover.nome}' ({'P' if paciente_a_remover.prioridade==2 else 'N'}).")

        proximo_nome = "FILA VAZIA"
        if paciente_a_remover == self.inicio:
            if paciente_a_remover.proximo:
                proximo_nome = paciente_a_remover.proximo.nome
        else:
            if self.inicio:
                proximo_nome = self.inicio.nome

        print(f"Próximo da fila: '{proximo_nome}'.")

        if paciente_a_remover == self.inicio and paciente_a_remover == self.fim:
            self.inicio = None
            self.fim = None
        elif paciente_a_remover == self.inicio:
            self.inicio = paciente_a_remover.proximo
            if self.inicio:
                self.inicio.anterior = None
        elif paciente_a_remover == self.fim:
            self.fim = paciente_a_remover.anterior
            if self.fim:
                self.fim.proximo = None
        else:
            ant = paciente_a_remover.anterior
            prox = paciente_a_remover.proximo
            ant.proximo = prox
            prox.anterior = ant

        self.ultimo_atendido_prioritario = (paciente_a_remover.prioridade == 2)

        del paciente_a_remover

        mem_depois = self.calcular_memoria_total()
        self._print_memoria(mem_antes, mem_depois)

    def buscar_paciente(self, nome: str):
        temp = self.inicio
        while temp:
            if temp.nome.lower() == nome.lower():
                return temp
            temp = temp.proximo
        return None

    def alterar_dados(self, nome_busca: str, novo_nome: str, nova_idade: int, nova_prioridade: int):
        print(f"\n-> Alterando dados de '{nome_busca}' ...")
        mem_antes = self.calcular_memoria_total()

        paciente = self.buscar_paciente(nome_busca)
        if not paciente:
            print(f"Erro: Paciente '{nome_busca}' não encontrado.")
            return

        prioridade_original = paciente.prioridade
        if prioridade_original == nova_prioridade:
            paciente.nome = novo_nome
            paciente.idade = nova_idade
            print("Dados alterados com sucesso (mesma prioridade).")
        else:
            print("Prioridade alterada. Reposicionando paciente na fila...")
            if paciente == self.inicio and paciente == self.fim:
                self.inicio = self.fim = None
            elif paciente == self.inicio:
                self.inicio = paciente.proximo
                if self.inicio:
                    self.inicio.anterior = None
            elif paciente == self.fim:
                self.fim = paciente.anterior
                if self.fim:
                    self.fim.proximo = None
            else:
                paciente.anterior.proximo = paciente.proximo
                paciente.proximo.anterior = paciente.anterior
            self.adicionar_paciente(novo_nome, nova_idade, nova_prioridade)
            mem_depois = self.calcular_memoria_total()
            print("Reposicionamento concluído.")
            self._print_memoria(mem_antes, mem_depois)
            return

        mem_depois = self.calcular_memoria_total()
        self._print_memoria(mem_antes, mem_depois)

    def carregar_amostra_inicial(self):
        amostra = [
            ("Alessandro", 58, 2),
            ("Bianca", 24, 1),
            ("Diego", 67, 2),
            ("Elisa", 31, 1),
            ("Fernando", 72, 2),
            ("Gabriela", 28, 1),
            ("Henrique", 49, 2),
            ("Isabela", 36, 1),
            ("Joana", 83, 2),
            ("Kleber", 22, 1),
        ]
        for nome, idade, pr in amostra:
            self.adicionar_paciente(nome, idade, pr)


def modo_interativo():
    fila = FilaDeAtendimento()
    print("--- Carregando fila inicial com 10 pacientes de exemplo ---")
    fila.carregar_amostra_inicial()

    while True:
        print("\n--- Menu de Opções ---")
        fila.display()
        print("\nComandos disponíveis:")
        print("  add <nome> <idade> <P/N>      - ex: add Beatriz 25 P")
        print("  remover                       - atender próximo paciente")
        print("  alterar <nome> <novo_nome> <nova_idade> <P/N>")
        print("  inverso                       - mostrar fila invertida")
        print("  sair                          - encerrar")
        comando_str = input("\nDigite o comando: ").strip()
        partes = comando_str.split()
        if not partes:
            continue
        acao = partes[0].lower()
        try:
            if acao == "add":
                nome, idade_str, prio_str = partes[1], partes[2], partes[3]
                idade = int(idade_str)
                prioridade = 2 if prio_str.upper() == 'P' else 1
                fila.adicionar_paciente(nome, idade, prioridade)
            elif acao == "remover":
                fila.remover_paciente()
            elif acao == "alterar":
                nome_busca = partes[1]
                novo_nome = partes[2]
                nova_idade = int(partes[3])
                nova_prio = 2 if partes[4].upper() == 'P' else 1
                fila.alterar_dados(nome_busca, novo_nome, nova_idade, nova_prio)
            elif acao == "inverso":
                fila.display_inverso()
            elif acao == "sair":
                print("Encerrando o programa.")
                break
            else:
                print("Comando inválido. Tente novamente.")
        except (IndexError, ValueError):
            print("Erro: argumentos inválidos. Verifique o formato do comando.")

if __name__ == "__main__":
    modo_interativo()
