import psutil
import os

class ProcessInfo:
    def __init__(self, pid):
        """
        Inicializa a classe com o PID informado e obtém o objeto do processo.
        """
        try:
            self.process = psutil.Process(pid)
        except psutil.NoSuchProcess:
            raise ValueError("Processo não encontrado.")
        
        self.name = self.process.name()
        try:
            self.exe_path = self.process.exe()
        except Exception as e:
            print("Erro ao obter o caminho do executável:", e)
            self.exe_path = None

    def get_executable_details(self):
        """
        Retorna o diretório e o nome do arquivo do executável.
        """
        if self.exe_path:
            directory = os.path.dirname(self.exe_path)
            file_name = os.path.basename(self.exe_path)
            return directory, file_name
        return None, None

    def update(self):
        """
        Atualiza e retorna os dados do processo (status e informações de memória).
        """
        try:
            status = self.process.status()
            memory = self.process.memory_info()
            return {"status": status, "memory": memory}
        except Exception as e:
            print("Erro ao atualizar dados do processo:", e)
            return None

    def display_info(self):
        """
        Exibe as informações coletadas do processo.
        """
        print("Nome do processo:", self.name)
        if self.exe_path:
            print("Caminho do executável:", self.exe_path)
            directory, file_name = self.get_executable_details()
            print("Diretório do executável:", directory)
            print("Arquivo do executável:", file_name)
        else:
            print("Não foi possível obter o caminho do executável.")
        
        updated_data = self.update()
        if updated_data is not None:
            print("Dados atualizados:")
            print("Status:", updated_data["status"])
            print("Memória:", updated_data["memory"])

def main():
    pid_input = input("Digite o PID do processo: ")
    try:
        pid = int(pid_input)
    except ValueError:
        print("PID inválido. Deve ser um número inteiro.")
        return

    try:
        process_info = ProcessInfo(pid)
    except ValueError as e:
        print(e)
        return

    process_info.display_info()

if __name__ == "__main__":
    main()
