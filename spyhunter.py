import psutil
import time
import logging
import argparse

# Configurações de log
logging.basicConfig(filename='port_monitor.log', level=logging.INFO)

def parse_arguments():
    """Função para ler argumentos de linha de comando."""
    parser = argparse.ArgumentParser(description='Monitorar portas abertas e processos.')
    parser.add_argument('--interval', type=int, default=10, help='Intervalo entre as verificações em segundos.')
    return parser.parse_args()

def get_open_ports():
    """Captura todas as conexões de rede e seus processos associados."""
    open_ports = {}
    # Verificar todas as conexões de rede (não só "LISTEN")
    for conn in psutil.net_connections(kind='inet'):
        port = conn.laddr.port
        pid = conn.pid
        if pid:
            try:
                process_name = psutil.Process(pid).name()  # Nome do processo
                process_directory = psutil.Process(pid).cwd()  # Diretório de trabalho do processo
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                process_name = "Unknown"
                process_directory = "Unknown"
        else:
            process_name = "Unknown"
            process_directory = "Unknown"
        
        open_ports[port] = (process_name, pid, process_directory, conn.status)  # Incluir estado da conexão
    return open_ports

def risk_assessment(process_name):
    """Avalia o nível de risco de um processo."""
    risk_keywords = ["unknown", "suspicious", "malware", "trojan"]
    for keyword in risk_keywords:
        if keyword in process_name.lower():
            return "High Risk"
    return "Low Risk"

def monitor_ports(interval=10):
    """Monitora as portas abertas e os processos associados."""
    known_ports = get_open_ports()
    print(f"Portas abertas iniciais: {len(known_ports)} portas detectadas")
    
    while True:
        current_ports = get_open_ports()
        
        # Verificar novas portas abertas
        new_ports = set(current_ports) - set(known_ports)
        
        if new_ports:
            print(f"Novas portas abertas detectadas: {new_ports}")
            for port in new_ports:
                process_name, pid, process_directory, conn_status = current_ports[port]
                risk_level = risk_assessment(process_name)
                print(f"Porta {port}: {process_name} (PID: {pid}) - Diretório: {process_directory} - Estado: {conn_status} - Nível de Risco: {risk_level}")
        
        # Classificação das portas abertas atuais por risco
        print("\nClassificação das portas abertas atuais por risco:")
        for port, (process_name, pid, process_directory, conn_status) in current_ports.items():
            risk_level = risk_assessment(process_name)
            print(f"Porta {port}: {process_name} (PID: {pid}) - Diretório: {process_directory} - Estado: {conn_status} - Nível de Risco: {risk_level}")
        
        known_ports = current_ports
        print("-" * 40)
        time.sleep(interval)

if __name__ == "__main__":
    args = parse_arguments()
    monitor_ports(interval=args.interval)
