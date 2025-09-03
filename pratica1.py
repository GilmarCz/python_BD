import pymysql


#Minha Resolução !!!

# try:
#     # 1) Conectar a BD
#     conexao = pymysql.connect(
#         host='localhost',
#         user='root',
#         password='123456',
#         database='sistema_escolar',
#         charset='utf8mb4',
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     print("Conectado com sucesso!")

#     with conexao.cursor() as cursor:
#         # 2) Listar todos os alunos
#         cursor.execute("SELECT nome, email, semestre_atual, status_aluno FROM alunos")
#         alunos = cursor.fetchall()

#         print("\n--- Lista de Alunos ---")
#         for aluno in alunos:
#             print(f"Aluno: {aluno['nome']} | Email: {aluno['email']} | Semestre: {aluno['semestre_atual']} | Status: {aluno['status_aluno']}")

#         # 3) Cadastrar novo aluno
#         while True:
#             print("\n--- Cadastro de Novo Aluno ---")
#             nome = input("Nome (ou digite SAIR para encerrar): ")
#             if nome.strip().upper() == "SAIR":
#                 break

#             email = input("Email: ")
#             telefone = input("Telefone: ")
#             data_nascimento = input("Data de nascimento (AAAA-MM-DD): ")
#             curso_id = int(input("ID do curso: "))
#             semestre_atual = int(input("Semestre atual: "))
#             status_aluno = input("Status (Ativo/Inativo/Formado): ")
#             data_matricula = input("Data de matrícula (AAAA-MM-DD): ")

#             sql = """
#                 INSERT INTO alunos 
#                 (nome, email, telefone, data_nascimento, curso_id, semestre_atual, status_aluno, data_matricula)
#                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
#             """
#             valores = (nome, email, telefone, data_nascimento, curso_id, semestre_atual, status_aluno, data_matricula)

#             cursor.execute(sql, valores)
#             conexao.commit()
#             print(f"\nAluno {nome} cadastrado com sucesso!")

# except Exception as erro:
#     print("Erro ao acessar o banco de dados:", erro)

# finally:
#     if conexao and conexao.open:
#         conexao.close()
#         print("Conexão encerrada.")
        

#Resolução John!!!

conexao = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='sistema_escolar',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
print("Conectado com sucesso!")

while True:
    nome = input("Qual nome você quer cadastrar: ")
    email = input("Qual o email você quer cadastrar: ")
    
    with conexao.cursor() as cursor:
        sql = "INSERT INTO alunos (nome, email, telefone, data_nascimento, curso_id, semestre_atual, status_aluno, data_matricula) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        valores = (nome, email,"(49)99983-2018","2001-03-12",1,2,"Ativo","2024-08-01")
        cursor.execute(sql,valores)
        conexao.commit()
        break

