from random import randint
import os

"""
    Define o atual diretório onde se encontra o programa,
    e define o tipo de barra a ser utilizada no terminal
    de acordo com o sistem operacional
"""
diretorio = os.getcwd()
barras = "\\" if os.name == 'nt' else "/"

"""
    Verifica se o numero é primo
"""


def isPrimo(numero):
    if numero % 2 == 1:
        return numero
    else:
        raise Exception(f"O numero {numero} não é primo")


"""
    Função que auxilia em salvar os arquivos no disco do computador,
    a função verifica se o arquivo existe, e nesse caso questiona se
    o usuário deseja sobrescreve-lo. Foram utilizadas exceções para
    lidar com possiveis erros de arquivos.
"""


def arquivoExiste(arquivo):
    if not os.path.exists(arquivo):
        return False
    return True


def salvar_no_disco(nome, conteudo):
    try:
        arquivo = open(nome, 'w')
        for byte in conteudo:
            arquivo.write(str(byte) + " ")
        arquivo.close()
        print("\nArquivo salvo em: " + diretorio + barras + nome)
    except (IOError, FileExistsError):
        print("\n\nErro: Não foi possível salvar o arquivo!")


def salvar(nome, conteudo):
    if not arquivoExiste(nome):
        salvar_no_disco(nome, conteudo)
    else:
        print("\nO arquivo já existe!")
        escolha = input("\nDeseja sobrescrever o arquivo S/N: ")
        if escolha == "S" or escolha == "s":
            salvar_no_disco(nome, conteudo)
        if escolha == "n" or escolha == "N":
            print("Atenção: O arquivo não foi salvo no computador")


"""
    Função que tem por objetivo realizar a leitura de arquivos salvos
    em disco, bem como lidar com possiveis exceções que possam ocorrer.
"""


def ler_mensagem_do_arquivo(nome):
    try:
        temp = []
        content = open(nome, 'r')
        for number in content:
            temp.append(number)
        content.close()
        return number
    except FileNotFoundError:
        print("\nErro: O arquivo não existe.")
        input("Pressione ENTER para voltar ao menu inicial...")
        main()


"""
    Função de criptografia dos dados inseridos pelo usuario. Possui
    dois argumentos que por padrão são definidos como False.
    Deixando o usuario decidir qual o procedimento mais adequado a situação
"""


def criptografar(mensagem=False, arquivo=False):
    # Caso os dois parametros sejam Falsos a aplicação retorna ao menu
    if (mensagem == False) and (arquivo == False) or (arquivo == ""):
        raise Exception("Não há parametros suficientes para criptografar")

    p = isPrimo(int(input("Digite um numero primo para (p):")))
    q = isPrimo(int(input("Digite um numero primo para (q):")))

    # Define-se o produto de P e Q e as Chaves de Decodificação
    n = p * q
    totiente_de_n = (p - 1) * (q - 1)
    e = 1
    d = 0

    # Gera-se um numero aleatorio para "e", sendo que "e" não pode ser um divisor
    # totiente de N, mas tenha um inverso negativo de "d" que deve ser diferente "e"
    while totiente_de_n % e == 0 or n % e == 0 or d == 0 or d == e:
        e = randint(1, totiente_de_n)
        for i in range(2, totiente_de_n):
            if (i * e) % totiente_de_n == 1:
                d = i

    cifra = []
    if arquivo:
        conteudo = []
        texto = ler_mensagem_do_arquivo(arquivo)
        if len(texto) > 0:
            for char in ler_mensagem_do_arquivo(arquivo):
                # Realiza a substituição das letras por numeros ascii
                conteudo.append(ord(char))

            for i in range(len(conteudo)):
                # Realiza o calculo tendo como base os numeros asccii convertidos
                cifra.append((conteudo[i] ** e) % n)
        else:
            print("O arquivo não pode ser encontrado.")

    else:
        alfab_para_int = []
        if len(mensagem) > 128 or mensagem is False:
            raise Exception("O texto excede o limite de 128 caracteres ou não é válido!")
        for char in mensagem:
            alfab_para_int.append(ord(char))

        for i in range(len(alfab_para_int)):
            cifra.append((alfab_para_int[i] ** e) % n)

    escolha = input("\nDeseja salvar o arquivo criptografado S/N: ")
    if escolha == "S" or escolha == "s":
        nome = input("Digite o nome do arquivo: ")
        salvar(nome, cifra)

        """
            Os pares de chaves publicas e privadas são salvas no computar,
            a fim de evitar a perda das mesmo em casos de mal funcionamento
            do programa ou quedas de energia. As chaves se não salvas são 
            eliminadas ao se encerrar a aplicação.
            Por padrão são salvas no mesmo diretório do programa.
        """
        arquivo_chaves_publicas = open('chaves_publicas.txt', 'w')
        arquivo_chaves_publicas.write("N: " + str(n) + "\n" + "E: " + str(e))
        arquivo_chaves_publicas.close()

        arquivo_chaves_privadas = open('chaves_privadas.txt', 'w')
        arquivo_chaves_privadas.write("N: " + str(n) + '\n' + "D: " + str(d) + '\n')
        arquivo_chaves_privadas.close()

        print("\n\nFoi feito um backup de suas chaves publicas e privadas em seu computador.")
        print("Por segurança as mantenha longe de pessoas não autorizadas!\n\n")

    print(f"\nChaves Públicas: e: {e} n: {n}")
    print(f"Chaves Privadas: d: {d} n: {n}")
    print("\nA cifra gerada foi: \n")
    for i in cifra:
        print(i, end=" ")

    print("\n\n")


"""
  Função que tem por objetivo descriptografar a cifra inserida ou 
  carregada de um arquivo de text. A função possui dois parametros
  que deixam o usuario decidir como ele ira descriptografar o arquivo.
"""


def descriptografar(cifra=False, arquivo=False):
    cifra = []
    mensagem = []
    d = int(input("\nInsira a chave privada (d): "))
    n = int(input("\nInsira a chave publica (n): "))

    # Se o usuario decidir inserir as informações
    if cifra:
        for i in range(len(cifra)):
            cifra.append((cifra[i] ** d) % n)
        for i in cifra:
            mensagem.append(chr(i))

    # Se decidir carregar um arquivo contendo a mensagen
    if arquivo:
        tmp_int = ler_mensagem_do_arquivo(arquivo).split(' ')
        integers = []
        for i in tmp_int:
            if i != "":
                integers.append(int(i))
        for i in range(len(integers)):
            cifra.append((integers[i] ** d) % n)
        for i in cifra:
            mensagem.append(chr(i))

    # Pergunta ao usuario se ele deseja salvar o arquivo de texto no computador
    escolha = input("Deseja salvar a mensagem decodificada em um arquivo? (S/N):")
    if escolha == "S" or escolha == "s":
        nome = input("Nome do arquivo: ")
        salvar(nome, mensagem)

    # A mensagem decodificada é exibida mesmo se o usuario salvar o arquivo
    print("\n\nA mensagem decodificada é: ")
    for i in mensagem:
        print(i, end="")

    input("\n\nPressione ENTER para voltar ao menu inicial...")


"""
    Função auxiliar que tem por objetivo limpar a tela,
    a função possui uma condição que determina o tipo de 
    sistema operacional que o usuario usa e aplica o comando
    correto.
"""


def limpar_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


"""
    Função principal onde se encontra os menus do programa,
    foi dado o nome de "main()" por convenção do Python. 
    O programa possui exceções que ajudam a evitar entradas erradas
    do usuário
"""


def main():
    saida = False
    while not saida:
        try:
            limpar_console()
            print("O que deseja fazer ?")
            print("""
                [1] Criptografar mensagem
                [2] Descriptografar mensagem
                [0] Sair
            """)
            escolha = int(input(">"))
            if escolha == "":
                main()
            if escolha == 1:
                limpar_console()
                print("""
                    Escolha uma opção:
                    [1] Carregar arquivo de texto
                    [2] Digitar manualmente
                    [0] Sair
                    """)
                escolha = int(input(">"))
                if escolha == 1:
                    arquivo = input("Digite o nome do arquivo (Deve estar no mesmo diretório da aplicação): \n> ")
                    criptografar(False, arquivo)
                    input("Pressione ENTER para voltar ao menu inicial...")
                elif escolha == 2:
                    print("Insira a mensagem a ser criptografada: \n")
                    mensagem = str(input("> "))
                    criptografar(mensagem)
                    input("Pressione ENTER para voltar ao menu inicial...")
            elif escolha == 2:
                limpar_console()
                print("""
                    Escolha uma opção:
                    [1] Carregar arquivo criptogrado
                    [2] Digitar manualmente
                    [0] Sair
                    """)
                escolha = int(input(">"))
                if escolha == 1:
                    arquivo = input("Digite o nome do arquivo (Deve estar no mesmo diretório da aplicação): \n> ")
                    if arquivo == "":
                        raise Exception("O nome de arquivo não pode estar vazio!")
                    descriptografar(False, arquivo)
                elif escolha == 2:
                    print("Insira a mensagem a ser decodificada: \n")
                    codificado = [int(x) for x in input().split()]
                    descriptografar(codificado, False)
            elif escolha == 0:
                print("Encerrando...")
                input("Pressione ENTER para sair...")
                exit(1)
            else:
                main()
        except ValueError:
            limpar_console()
            print("Ocorreu um erro ao processar a sua entrada!")
            input("Pressione ENTER para voltar ao menu inicial...")
            main()
        except Exception as msg:
            print("\n\nErro:", msg)
            input("Pressione ENTER para voltar ao menu incial...")
            main()
        except KeyboardInterrupt:
            print("Encerrando...")
            exit(1)


# Auxilia o compilador a enxergar qual o comando principal do script
if __name__ == '__main__':
    main()
