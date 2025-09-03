import pymysql

def buscar_alunos():
    try:
        conexao = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='sistema_escolar',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conexao.cursor() as cursor:
            while True:
                print("\n--- Sistema de Busca de Alunos ---")
                print("1 - Buscar por Nome")
                print("2 - Buscar por Email")
                print("3 - Buscar por Status")
                print("4 - Buscar por Curso")
                print("0 - Sair")
                opcao = input("Escolha uma opção: ")

                if opcao == "0":
                    print("Saindo do sistema de busca...")
                    break

                if opcao == "1":
                    nome = input("Digite parte do nome: ")
                    sql = """
                        SELECT a.aluno_id, a.nome, a.email, a.status_aluno, c.nome_curso
                        FROM alunos a
                        JOIN cursos c ON a.curso_id = c.curso_id
                        WHERE a.nome LIKE %s;
                    """
                    cursor.execute(sql, ("%" + nome + "%",))

                elif opcao == "2":
                    email = input("Digite o email: ")
                    sql = """
                        SELECT a.aluno_id, a.nome, a.email, a.status_aluno, c.nome_curso
                        FROM alunos a
                        JOIN cursos c ON a.curso_id = c.curso_id
                        WHERE a.email = %s;
                    """
                    cursor.execute(sql, (email,))

                elif opcao == "3":
                    status = input("Digite o status (Ativo/Inativo/Formado/Trancado): ")
                    sql = """
                        SELECT a.aluno_id, a.nome, a.email, a.status_aluno, c.nome_curso
                        FROM alunos a
                        JOIN cursos c ON a.curso_id = c.curso_id
                        WHERE a.status_aluno = %s;
                    """
                    cursor.execute(sql, (status,))

                elif opcao == "4":
                    curso = input("Digite o nome do curso: ")
                    sql = """
                        SELECT a.aluno_id, a.nome, a.email, a.status_aluno, c.nome_curso
                        FROM alunos a
                        JOIN cursos c ON a.curso_id = c.curso_id
                        WHERE c.nome_curso = %s;
                    """
                    cursor.execute(sql, (curso,))

                else:
                    print("Opção inválida!")
                    continue

                # Mostrar resultados
                resultados = cursor.fetchall()
                if resultados:
                    print("\n--- Resultados da Busca ---")
                    for aluno in resultados:
                        print(f"ID: {aluno['aluno_id']} | "
                              f"Nome: {aluno['nome']} | "
                              f"Email: {aluno['email']} | "
                              f"Status: {aluno['status_aluno']} | "
                              f"Curso: {aluno['nome_curso']}")
                else:
                    print("Nenhum aluno encontrado.")

    except Exception as erro:
        print("Erro ao acessar o banco de dados:", erro)

    finally:
        if conexao and conexao.open:
            conexao.close()

# Teste do sistema de busca
buscar_alunos()
