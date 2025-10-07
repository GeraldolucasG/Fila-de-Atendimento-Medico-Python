import sys

class PacienteNode:
    def _init_(self, nome, idade, prioridade):
        self.nome = nome
        self.idade = idade
        self.prioridade = prioridade
        self.proximo = None
        self.anterior = None
    
    def _sizeof_(self):
        return (sys.getsizeof(self.nome) + 
                sys.getsizeof(self.idade) + 
                sys.getsizeof(self.prioridade) + 
                super()._sizeof_())


class FilaDeAtendimento:
    def _init_(self):
        self.inicio = None
        self.fim = None
        self._ultimo_foi_P = False 

    def calcular_memoria_total(self):
        mem_total = sys.getsizeof(self)
        temp = self.inicio
        while temp:
            mem_total += temp._sizeof_()
            temp = temp.proximo
        return mem_total
    
    def log_memoria(self, operacao, mem_antes):
        mem_depois = self.calcular_memoria_total()
        diff = mem_depois - mem_antes
        
        print("\n--- MONITORAMENTO DE MEMÓRIA ---")
        print(f"Operação: {operacao}")
        print(f"Total ANTES: {mem_antes} bytes")
        print(f"Total DEPOIS: {mem_depois} bytes")
        print(f"DIFERENÇA: {'+' if diff >= 0 else ''}{diff} bytes")
        print("----------------------------------")

    def contar_pacientes(self):
        temp = self.inicio
        count_P = 0
        count_N = 0
        primeiro_normal = None
        while temp:
            if temp.prioridade == 2:
                count_P += 1
            else:
                count_N += 1
                if primeiro_normal is None:
                    primeiro_normal = temp
            temp = temp.proximo
        return count_P, count_N, primeiro_normal

    def adicionar_paciente(self, nome, idade, prioridade):
        mem_antes = self.calcular_memoria_total()
        novo_paciente = PacienteNode(nome, idade, prioridade)

        if self.inicio is None:
            self.inicio = self.fim = novo_paciente
        elif novo_paciente.prioridade == 1:
            self.fim.proximo = novo_paciente
            novo_paciente.anterior = self.fim
            self.fim = novo_paciente
        elif novo_paciente.prioridade == 2:
            temp = self.inicio
            while temp and temp.prioridade == 2:
                temp = temp.proximo
            
            if temp is None:
                self.fim.proximo = novo_paciente
                novo_paciente.anterior = self.fim
                self.fim = novo_paciente
            elif temp == self.inicio:
                novo_paciente.proximo = self.inicio
                self.inicio.anterior = novo_paciente
                self.inicio = novo_paciente
            else:
                no_anterior = temp.anterior
                no_anterior.proximo = novo_paciente
                novo_paciente.anterior = no_anterior
                novo_paciente.proximo = temp
                temp.anterior = novo_paciente
        
        self.log_memoria(f"Adicionar Paciente ({nome})", mem_antes)

    def remover_paciente(self):
        if self.inicio is None:
            print("\n-> Fila de atendimento já está vazia.")
            return

        mem_antes = self.calcular_memoria_total()
        count_P, count_N, primeiro_normal = self.contar_pacientes()

        paciente_a_remover = self.inicio
        regra_ativa = count_N > 0 and (count_P / count_N) >= (1/7)

        if regra_ativa:
            print("*** REGRA 1:7 ATIVA ***")
            if self._ultimo_foi_P:
                if primeiro_normal:
                    paciente_a_remover = primeiro_normal
                    print(f"Chamando paciente Normal mais antigo: {paciente_a_remover.nome}")
                else:
                    print("Apenas prioritários restantes. Atendendo o próximo P.")
            else:
                paciente_a_remover = self.inicio
                print(f"Chamando paciente Prioritário mais antigo: {paciente_a_remover.nome}")
        else:
            paciente_a_remover = self.inicio
        
        self._ultimo_foi_P = (paciente_a_remover.prioridade == 2)

        print(f"Paciente '{paciente_a_remover.nome}' ({'P' if paciente_a_remover.prioridade == 2 else 'N'}) atendido.")
        
        if paciente_a_remover == self.inicio and paciente_a_remover == self.fim:
            self.inicio = self.fim = None
        elif paciente_a_remover == self.inicio:
            self.inicio = paciente_a_remover.proximo
            if self.inicio: self.inicio.anterior = None
        elif paciente_a_remover == self.fim:
            self.fim = paciente_a_remover.anterior
            if self.fim: self.fim.proximo = None
        else:
            paciente_a_remover.anterior.proximo = paciente_a_remover.proximo
            paciente_a_remover.proximo.anterior = paciente_a_remover.anterior
        
        proximo_nome = "FILA VAZIA"
        if self.inicio:
            status = "(P)" if self.inicio.prioridade == 2 else "(N)"
            proximo_nome = f"{self.inicio.nome} {status}"
        print(f"Próximo na fila: '{proximo_nome}'.")
        
        del paciente_a_remover
        self.log_memoria("Remover Paciente", mem_antes)

    def buscar_paciente(self, nome):
        temp = self.inicio
        while temp:
            if temp.nome.lower() == nome.lower():
                return temp
            temp = temp.proximo
        return None

    def alterar_dados(self, nome_busca, novo_nome, nova_idade, nova_prioridade):
        mem_antes = self.calcular_memoria_total()
        paciente = self.buscar_paciente(nome_busca)

        if not paciente:
            print(f"Erro: Paciente '{nome_busca}' não encontrado.")
            return

        old_priority = paciente.prioridade
        priority_changed = (old_priority != nova_prioridade)

        paciente.nome = novo_nome
        paciente.idade = nova_idade
        paciente.prioridade = nova_prioridade
        
        if priority_changed:
            print("Prioridade alterada. Reposicionando paciente na fila...")
            
            if paciente == self.inicio and paciente == self.fim:
                self.inicio = self.fim = None
            elif paciente == self.inicio:
                self.inicio = paciente.proximo
                if self.inicio: self.inicio.anterior = None
            elif paciente == self.fim:
                self.fim = paciente.anterior
                if self.fim: self.fim.proximo = None
            else:
                paciente.anterior.proximo = paciente.proximo
                paciente.proximo.anterior = paciente.anterior
            
            self.adicionar_paciente(paciente.nome, paciente.idade, paciente.prioridade)
            
            self.log_memoria(f"Alterar Dados/Reposicionar ({nome_busca})", mem_antes)
            return

        print("Dados alterados com sucesso.")
        self.log_memoria(f"Alterar Dados ({nome_busca})", mem_antes)

    def display(self):
        print("\n--- Fila Atual (Início -> Fim) ---")
        if self.inicio is None:
            print("Fila vazia.")
            return
        temp = self.inicio
        while temp:
            status = "(P)" if temp.prioridade == 2 else "(N)"
            print(f"[ {temp.nome} ({status}) ] --> ", end="")
            temp = temp.proximo
        print("Final")

    def display_inverso(self):
        print("\n--- Fila Inversa (Fim <- Início) ---")
        if self.fim is None:
            print("Fila vazia.")
            return
        temp = self.fim
        while temp:
            status = "(P)" if temp.prioridade == 2 else "(N)"
            print(f"[ {temp.nome} ({status}) ] <-- ", end="")
            temp = temp.anterior
        print("Início")

def modo_interativo():
    fila = FilaDeAtendimento()

    print("\n--- Carregando fila inicial (10 pacientes) ---")
    
    pacientes_iniciais = [
        ("Teresa", 30, 1), ("Gabriel", 70, 2), ("Monica", 45, 1), 
        ("Helio", 65, 2), ("Irene", 22, 1), ("Pedro", 80, 2), 
        ("Felipe", 33, 1), ("Victor", 28, 1), ("Bruno", 90, 2), 
        ("Alice", 19, 1)
    ]
    for nome, idade, prioridade in pacientes_iniciais:
        fila.adicionar_paciente(nome, idade, prioridade)

    while True:
        fila.display()
        print("\n--- MENU --- Comandos: add | remover | alterar | inverso | sair")
        
        comando_str = input("Digite o comando: ").strip()
        partes = comando_str.split()
        if not partes: continue

        acao = partes[0].lower()
        try:
            if acao == "add":
                nome, idade_str, prio_str = partes[1], partes[2], partes[3]
                idade = int(idade_str)
                prioridade = 2 if prio_str.upper() in ('P', '2') else 1
                fila.adicionar_paciente(nome, idade, prioridade)
            
            elif acao == "remover":
                fila.remover_paciente()
            
            elif acao == "alterar":
                nome_busca = partes[1]
                
                paciente_existente = fila.buscar_paciente(nome_busca)
                if not paciente_existente:
                    print(f"Erro: Paciente '{nome_busca}' não encontrado.")
                    continue
                
                novo_nome = partes[2] if partes[2] != '-' else paciente_existente.nome
                
                nova_idade = paciente_existente.idade
                if partes[3] != '-':
                     nova_idade = int(partes[3])
                
                nova_prioridade = paciente_existente.prioridade
                if partes[4] != '-':
                    nova_prio_str = partes[4]
                    nova_prioridade = 2 if nova_prio_str.upper() in ('P', '2') else 1
                
                fila.alterar_dados(nome_busca, novo_nome, nova_idade, nova_prioridade)
            
            elif acao == "inverso":
                fila.display_inverso()
            
            elif acao == "sair":
                print("Encerrando o programa.")
                break
            
            else:
                print("Comando inválido. Tente novamente.")
        
        except (IndexError, ValueError) as e:
            print(f"Erro de comando/argumento: Verifique o formato: [alterar nome_antigo nome_novo idade_nova prioridade_nova] (use '-' para não alterar). Detalhe: {e}")

if __name__ == "_main_":
    modo_interativo()
