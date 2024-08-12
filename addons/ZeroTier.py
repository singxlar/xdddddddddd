import subprocess
import json
import re
import os
import sys
import time
import threading

RGB = [(255, 255, 255), (110, 74, 255), (106, 0, 255)]

def gradient_text(text, colors):
    length = len(text)
    num_colors = len(colors)
    result = ""
    for i, char in enumerate(text):
        color_index = (i * (num_colors - 1)) // length
        t = (i * (num_colors - 1)) / length - color_index
        color1 = colors[color_index]
        color2 = colors[color_index + 1] if color_index + 1 < num_colors else colors[color_index]
        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)
        result += f'\033[38;2;{r};{g};{b}m{char}'
    return result + '\033[0m'

def ocultar_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def mostrar_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def silencioso(comando):
    try:
        resultado = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT)
        return resultado.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return None

def mostrar_progreso():
    for i in range(1, 11):
        sys.stdout.write(f"\033[2;0H{gradient_text('〘' + '◼ ' * i + '〙', RGB)}")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\033[2;0H" + " " * 80 + "\r")
    sys.stdout.flush()

def instalar_chafa():
    ocultar_cursor()
    print(gradient_text("〚☰ 〛Verificando instalación de chafa...", RGB))
    chafa_instalado = subprocess.call(['which', 'chafa'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
    if not chafa_instalado:
        ocultar_cursor()
        print(gradient_text("〚☰ 〛Chafa no está instalado. Instalando...", RGB))
        subprocess.run(['sudo', 'apt-get', 'update'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'chafa'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print(gradient_text("〚✔ 〛Chafa ya está instalado.", RGB))

def instalar_zerotier():
    progreso_thread = threading.Thread(target=mostrar_progreso)
    progreso_thread.start()

    subprocess.run('curl -s https://install.zerotier.com | sudo bash', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run('sudo chmod 755 /usr/sbin/zerotier-one && sudo pkill zerotier-one && echo "9993" | sudo tee /var/lib/zerotier-one/zerotier-one.port && sudo service zerotier-one restart', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run('sudo service zerotier-one start', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run('sudo chown root:root /var/lib/zerotier-one/authtoken.secret && sudo chmod 600 /var/lib/zerotier-one/authtoken.secret', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    progreso_thread.join()
    sys.stdout.write("\033[2;0H" + " " * 80 + "\r") 
    sys.stdout.flush()
    print(gradient_text("〚✔ 〛ZeroTier instalado y configurado.", RGB))

def obtener_ip_zerotier():
    print(gradient_text("〚☰ 〛Obteniendo IP de ZeroTier...", RGB))
    intentos = 10
    ip = None
    
    for _ in range(intentos):
        redes = silencioso('sudo zerotier-cli listnetworks')
        if redes:
            ip_Zero = re.search(r'(\d+\.\d+\.\d+\.\d+)', redes)
            if ip_Zero:
                ip = ip_Zero.group(1)
                break
        time.sleep(3)
    
    if ip:
        os.system('clear')
        print(gradient_text(f"〚✔ 〛IP de ZeroTier obtenida ", RGB))
    else:
        print(gradient_text("〚✖ 〛No se pudo obtener la IP de ZeroTier.", RGB))
    
    return ip

def Menu():
    while True:
        os.system('clear')
        menu = [
            gradient_text("〚1〛Instalar ZeroTier", RGB),
            gradient_text("〚2〛Desactivar ZeroTier", RGB),
            gradient_text("〚3〛Salir", RGB),
        ]
        for line in menu:
            ocultar_cursor()
            print(line)
            mostrar_cursor()
        
        print(gradient_text("   \n〚➥ 〛Seleccioná una opción ❱ ", RGB), end='')
        opcion = input()

        if opcion == "1":
            os.system('clear')
            ocultar_cursor()
            print(gradient_text("〚☰ 〛Iniciando instalación de ZeroTier...", RGB))

            instalar_chafa()

            os.system('clear')
            print(gradient_text("〚☰ 〛Si no sabés utilizar este servicio leé:", RGB))
            print(gradient_text("〚⠸ 〛━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", RGB))
            print(gradient_text("〚⏎ 〛Si ya lo leíste apretá Enter para continuar...", RGB))
            print(gradient_text("    ", RGB))

            chafa_command = "chafa --size=20x10 --dither=diffusion --colors=truecolor sapo.jpg"
            ascii_image = os.popen(chafa_command).read()
            input(ascii_image)
            os.system('clear')
            print(gradient_text('〚🡻 〛Descargando e instalando ZeroTier...', RGB))

            sys.stdout.write("\033[2;0H")
            sys.stdout.flush()

            progreso_thread = threading.Thread(target=mostrar_progreso)
            progreso_thread.start()
            instalar_zerotier()
            progreso_thread.join()
            sys.stdout.write("\033[2;0H" + " " * 80 + "\r") 
            sys.stdout.flush()
            print(gradient_text("〚✔ 〛ZeroTier instalado!", RGB))
            time.sleep(2)
            os.system('clear')

            print(gradient_text("〚✔ 〛ZeroTier instalado!\n〚⠸ 〛━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n〚☰ 〛Network ID\n  \n〚➥ 〛Colocá la ID de tu Network ❱ ", RGB), end='')
            mostrar_cursor()
            network_id = input()
            ocultar_cursor()
            join_command = f'sudo zerotier-cli join {network_id}'
            subprocess.run(join_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.system('clear')

            ocultar_cursor()
            print(gradient_text("〚☰ 〛Configurando tu ID...", RGB))
            time.sleep(2)
            os.system('clear')
            ip = obtener_ip_zerotier()
            if ip:
                config_path = "configuracion.json"
                try:
                    if os.path.exists(config_path):
                        with open(config_path, 'r') as file:
                            config = json.load(file)
                    else:
                        config = {}

                    config["servicio_a_usar"] = " "                
                    addons_dir = 'addons'
                    os.makedirs(addons_dir, exist_ok=True) 
                    with open(os.path.join(addons_dir, 'Ip-de-servidor.json'), 'w') as file:
                        json.dump({"ip": ip}, file)
                    with open(os.path.join(addons_dir, 'ZeroTier.json'), 'w') as file:
                        json.dump({"Activo": True}, file)
                    with open(config_path, 'w') as file:
                        json.dump(config, file)
                    
                    print(gradient_text(f"〚✔ 〛Servidor configurado en: ZeroTier", RGB))
                    print(gradient_text(f"〚⠸ 〛━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n〚❯❱〛 La IP de tu servidor es: {ip}", RGB))
                    print(gradient_text(f"                                             ", RGB))
                    input(gradient_text("〚⏎ 〛Apretá enter boludito si querés que se te prenda el server sapo de mierda...", RGB))
                    mostrar_cursor()
                except (IOError, json.JSONDecodeError) as e:
                    print(gradient_text(f"〚✖ 〛Error al procesar el archivo de configuración: {e}", RGB))
            else:
                print(gradient_text("〚✖ 〛No se pudo obtener la IP de ZeroTier. Por favor, intentálo de nuevo.", RGB))
            break

        elif opcion == "2":
            os.system('clear')
            ocultar_cursor()
            print('〚⛒ 〛Desactivando ZeroTier...', RGB)
            sys.stdout.write("\033[2;0H")
            sys.stdout.flush()

            for i in range(1, 11):    
                sys.stdout.write(f"\033[2;0H{gradient_text('〘' + '◼ ' * i + '〙', RGB)}")
                sys.stdout.flush()
                time.sleep(1)
            sys.stdout.write("\033[2;0H" + " " * 80 + "\r") 
            print(gradient_text("〚✔ 〛ZeroTier desactivado!", RGB))
            sys.stdout.write("\033[?25h")

            archivo_zero_tier = 'addons/ZeroTier.json'
            if os.path.exists(archivo_zero_tier):
                os.remove(archivo_zero_tier)
            break

        elif opcion == "3":
            ocultar_cursor()
            sys.stdout.write("\r" + " " * 80 + "\r")
            sys.stdout.flush()
            print(gradient_text("〚❮❰ 〛Saliendo al menu...", RGB))
            time.sleep(2)
            break

        else:
            ocultar_cursor()
            print(gradient_text("〚✖ 〛Opción inválida. Por favor, seleccioná una opción válida.. ", RGB))

def verificar_activo():
    archivo_zero_tier = 'addons/ZeroTier.json'
    if os.path.exists(archivo_zero_tier):
        with open(archivo_zero_tier, 'r') as file:
            datos = json.load(file)
        datos["Activo"] = True
        with open(archivo_zero_tier, 'w') as file:
            json.dump(datos, file)
        comandos = [
            'sudo service zerotier-one start',
            'sudo chown root:root /var/lib/zerotier-one/authtoken.secret',
            'sudo chmod 600 /var/lib/zerotier-one/authtoken.secret',
            'sudo zerotier-cli listnetworks'
        ]
        for comando in comandos:
            silencioso(comando)

verificar_activo()