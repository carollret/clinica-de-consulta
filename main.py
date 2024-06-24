import mysql.connector
from datetime import datetime

class Paciente:
    def __init__(self, id, nome, telefone):
        self.id = id
        self.nome = nome
        self.telefone = telefone

class Consulta:
    def __init__(self, paciente, data, hora, especialidade):
        self.paciente = paciente
        self.data = data
        self.hora = hora
        self.especialidade = especialidade

class Agenda:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="30740055",
            database="clinica"
        )
        self.mycursor = self.mydb.cursor()

    def cadastrar_paciente(self):
        print("### Cadastro de Paciente ###")
        nome = input("Digite o nome do paciente: ")
        telefone = input("Digite o telefone do paciente: ")

        try:
            self.mycursor.execute("SELECT * FROM pacientes WHERE telefone = %s", (telefone,))
            paciente = self.mycursor.fetchone()
            if paciente:
                print("Paciente já cadastrado!")
                return
        except mysql.connector.Error as err:
            print(f"Erro ao verificar cadastro de paciente: {err}")
            return

        try:
            self.mycursor.execute("INSERT INTO pacientes (nome, telefone) VALUES (%s, %s)", (nome, telefone))
            self.mydb.commit()
            print("Paciente cadastrado com sucesso:", nome, telefone)
        except mysql.connector.Error as err:
            print(f"Erro ao cadastrar paciente: {err}")

    def listar_pacientes(self):
        print("### Lista de Pacientes ###")
        try:
            self.mycursor.execute("SELECT * FROM pacientes")
            pacientes = self.mycursor.fetchall()
            for paciente in pacientes:
                print(f"{paciente[0]}. {paciente[1]} - {paciente[2]}")
        except mysql.connector.Error as err:
            print(f"Erro ao listar pacientes: {err}")

    def marcar_consulta(self):
        print("### Marcar Consulta ###")
        self.listar_pacientes()
        paciente_id = input("Digite o ID do paciente para marcar a consulta: ")
        hora = input("Digite a hora da consulta (formato HH:MM): ")
        data = input("Digite a data da consulta (formato DD/MM/AAAA): ")
        especialidade = input("Digite a especialidade da consulta: ")

        try:
            dia_formatado = datetime.strptime(data, "%d/%m/%Y").strftime("%d")
            mes_formatado = datetime.strptime(data, "%d/%m/%Y").strftime("%m")
            ano_formatado = datetime.strptime(data, "%d/%m/%Y").strftime("%Y")
            self.mycursor.execute(
                "INSERT INTO consulta (pacienteId, hora, dia, mes, ano, especialidade) VALUES (%s, %s, %s, %s, %s, %s)",
                (paciente_id, hora, dia_formatado, mes_formatado, ano_formatado, especialidade))
            self.mydb.commit()
            print("Consulta marcada com sucesso!\n")
        except mysql.connector.Error as err:
            print(f"Erro ao marcar a consulta: {err}")

    def cancelar_consulta(self):
        print("### Cancelar Consulta ###")
        try:
            self.mycursor.execute("SELECT * FROM consulta")
            consultas = self.mycursor.fetchall()
            if not consultas:
                print("Não há nenhuma consulta marcada para cancelar.")
                return
            print("Consultas agendadas:\n")
            for consulta in consultas:
                print(f"{consulta[0]}. {consulta[1]} - {consulta[2]} - {consulta[3]} - {consulta[4]}")
            consulta_id = input("Digite o ID da consulta que deseja cancelar: ")
            self.mycursor.execute("DELETE FROM consulta WHERE id = %s", (consulta_id,))
            self.mydb.commit()
            print("Consulta cancelada com sucesso!\n")
        except mysql.connector.Error as err:
            print(f"Erro ao cancelar a consulta: {err}")

    def __del__(self):
        self.mydb.close()

def main():
    agenda = Agenda()
    while True:
        print("### Menu Principal ### \n",
              "1. Cadastrar Paciente\n",
              "2. Marcar Consulta\n",
              "3. Cancelar Consulta\n",
              "4. Sair\n")
        opcao = int(input("Escolha uma opção: "))
        if opcao == 1:
            agenda.cadastrar_paciente()
        elif opcao == 2:
            agenda.marcar_consulta()
        elif opcao == 3:
            agenda.cancelar_consulta()
        elif opcao == 4:
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
