# import pymysql

# try:
#     conexao = pymysql.connect(
#     host='localhost',       #endereço do banco de dados
#     user= 'root',           #usuário
#     password='123456',      #senha do seu MySQL
#     database='sistema_escolar',     #nome do banco de dados
#     charset='utf8mb4',      #padrão de acentuação
#     cursorclass=pymysql.cursors.DictCursor      #retorma linhas como dicionário (chave:coluna)
# )
#     with conexao.cursor() as cursor:
#         cursor.execute("SELECT * FROM alunos")
#         print(cursor.fetchall())
# except Exception as erro:
#     print("Erro ao acessar o banco de dados: ", erro)
# finally:
#     print("Conectado com sucesso!")
#     conexao.close()

# conexao = pymysql.connect(
#     host='localhost',       #endereço do banco de dados
#     user= 'root',           #usuário
#     password='123456',      #senha do seu MySQL
#     database='sistema_escolar',     #nome do banco de dados
#     charset='utf8mb4',      #padrão de acentuação
#     cursorclass=pymysql.cursors.DictCursor      #retorma linhas como dicionário (chave:coluna)
# )
# print("Conectado com sucesso!")
# conexao.close()

# # #enviando um select para o BD
# # with conexao.cursor() as cursor:
# #     cursor.execute("SELECT * FROM alunos")
# #     alunos = cursor.fetchall() #retorna todas os alunos
# #     #alunos = cursor.fetchmany(20) #retorna 20 alunos
# #     #alunos = cursor.fetchone() #retorna todas os alunos
    
# #     #Mostrar os dados
# #     for aluno in alunos:
# #         print(f"Alunos: {aluno['nome']} - Email: {aluno['email']} - Semestre: {aluno['semestre_atual']}")
        
# # #esse codigo é para inserir um novo usuário
# # with conexao.cursor()as cursor:
# #     sql = "INSERT INTO alunos (nome, email, telefone, data_nascimento, curso_id, semestre_atual, status_aluno, data_matricula) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
# #     valores = ("Luciana Souza","luciana@melo.com","4999999999","2001-03-12",1,2,"Ativo","2024-08-01")
# #     cursor.execute(sql,valores)
# #     conexao.commit() # salvando no banco

# #Atualizar um usuario
# with conexao.cursor() as cursor:
#     sql = "UPDATE alunos SET telefone = %s WHERE aluno_id = %s"
#     valores = ("(49) 9999-4587", 601)
#     cursor.execute(sql, valores)
#     conexao.commit()

# print("Aluno atualizado com sucesso!")

# import pymysql

# try:
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
#         sql = "UPDATE alunos SET telefone = %s WHERE aluno_id = %s"
#         valores = ("(49) 9999-4587", 1251)  # Usa o ID que realmente existe
#         cursor.execute(sql, valores)
#         conexao.commit()
#         print(f"{cursor.rowcount} aluno(s) atualizado(s).")

# except Exception as erro:
#     print("Erro ao acessar o banco de dados:", erro)

# finally:
#     if conexao:
#         conexao.close()
#         print("Conexão encerrada.")

# #Deletar dados do banco de dados
# try:
#     with conexao.cursor() as cursor:
#         sql = "DELETE FROM alunos WHERE aluno_id = %s"
#         cursor.execute(sql,(1251,))
#         conexao.commit()
# except Exception as erro:
#     print("Deu um erro no BD", erro)
# finally:
#     conexao.close()

import pymysql

try:
    conexao = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='sistema_escolar',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Conectado com sucesso!")

    with conexao.cursor() as cursor:
        sql = "DELETE FROM alunos WHERE aluno_id = %s"
        cursor.execute(sql, (1251,))  # <<< vírgula para ser tupla
        conexao.commit()
        print(f"{cursor.rowcount} aluno(s) deletado(s).")

except Exception as erro:
    print("Deu um erro no BD:", erro)

finally:
    # Só fecha se a conexão ainda estiver aberta
    try:
        if conexao.open:
            conexao.close()
            print("Conexão encerrada.")
    except NameError:
        pass
