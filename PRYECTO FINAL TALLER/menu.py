from perfil import Perfil
from tweet import Tweet
from base_datos import BaseDatos
import bcrypt
from crear_tweet_gui import CrearTweetGUI

class Menu:
    def __init__(self):
        self.db = BaseDatos()
        self.tweet_manager = Tweet()
        self.usuario_actual = None
        self.perfil = Perfil(self.db)  # Instanciamos la clase Perfil
        self.opciones_menu_principal = {
            "1": self.visualizar_tweets,
            "2": self.crear_tweet,
            "3": self.ver_perfil,
            "4": self.eliminar_tweet,
            "5": self.eliminar_cuenta,
            "6": self.salir
        }

    def bienvenida(self):
        print("\n--- Bienvenido a Twitter ---")
        print("1. Iniciar Sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Elige una opción: ")
        if opcion == "1":
            self.iniciar_sesion()
        elif opcion == "2":
            self.registrarse()
        elif opcion == "3":
            print("Gracias por usar Twitter. ¡Hasta luego!")
            exit()
        else:
            print("❌ Opción no válida. Por favor, intenta de nuevo.")
            self.bienvenida()

    def iniciar_sesion(self):
        print("\n--- Iniciar Sesión ---")
        nombre_usuario = input("Nombre de Usuario: ")
        contrasena = input("Contraseña: ")

        conexion = self.db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT id_usuario, contraseña FROM usuarios WHERE nombre_usuario = %s",
                (nombre_usuario,)
            )
            resultado = cursor.fetchone()

            if resultado and bcrypt.checkpw(contrasena.encode('utf-8'), resultado[1].encode('utf-8')):
                print("✅ Inicio de sesión exitoso.")
                self.usuario_actual = resultado[0]
                self.menu_principal()
            else:
                print("❌ Usuario o contraseña incorrectos ")
                self.bienvenida()
        except Exception as e:
            print(f"❌ Error al iniciar sesión: {e}")
        finally:
            cursor.close()
            conexion.close()

    def registrarse(self):
        print("\n--- Registrarse ---")
        nombre_usuario = input("Nombre de Usuario: ")
        email = input("Correo Electrónico: ")
        contrasena = input("Contraseña: ")

        # Encriptar la contraseña
        contrasena_encriptada = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

        conexion = self.db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre_usuario, email, contraseña) VALUES (%s, %s, %s)",
                (nombre_usuario, email, contrasena_encriptada)
            )
            conexion.commit()
            print("✅ Registro exitoso. Ahora puedes iniciar sesión.")
            self.bienvenida()
        except Exception as e:
            print(f"❌ Error al registrar el usuario: {e}")
        finally:
            cursor.close()
            conexion.close()

    def mostrar_menu_principal(self):
        print("\n--- Menú Principal ---")
        print("1. Visualizar Tweets")
        print("2. Crear Tweet")
        print("3. Ver Perfil")
        print("4. Eliminar Tweet")
        print("5. Eliminar Cuenta")
        print("6. Salir")

    def ejecutar_opcion_principal(self, opcion):
        accion = self.opciones_menu_principal.get(opcion)
        if accion:
            accion()
        else:
            print("❌ Opción no válida. Por favor, elige una opción correcta.")

    def visualizar_tweets(self):
        """Muestra los tweets con el nombre del usuario y accede al menú 'Para ti'."""
        tweets = self.tweet_manager.obtener_tweets()
        print("\n========== Tweets ==========")
        if not tweets:
            print("No hay tweets disponibles.")
            return

        for tweet in tweets:
            id_publicacion, id_usuario, nombre_usuario, contenido, fecha = tweet
            print(f"\n📌 Tweet ID: {id_publicacion}")
            print(f"👤 Usuario: {nombre_usuario}")
            print(f"🕒 Fecha: {fecha}")
            print(f"✍️ Contenido: {contenido}")
            print("-" * 30)
        

    def ver_perfil(self):
        """Llama al método 'ver_perfil' de la clase Perfil"""
        self.perfil.ver_perfil(self.usuario_actual)

    def eliminar_tweet(self):
        id_tweet = input("Introduce el ID del tweet que deseas eliminar: ")
        self.db.eliminar_tweet(id_tweet)
    
    def eliminar_cuenta(self):
        confirmacion = input("¿Estás seguro de que deseas eliminar tu cuenta? (si/no): ").lower()
        
        if confirmacion == "si":
            self.db.eliminar_cuenta(self.usuario_actual)
            print("⚠ Tu cuenta ha sido eliminada. Cerrando sesión...")
            self.usuario_actual = None
            self.bienvenida()
        else:
            print("✅ Cancelaste la eliminación de tu cuenta.")
    def salir(self):
        print("Cerrando sesión...")
        self.usuario_actual = None
        self.bienvenida()

    def menu_principal(self):
        while True:
            self.mostrar_menu_principal()
            opcion = input("Elige una opción: ")
            self.ejecutar_opcion_principal(opcion)

    def iniciar(self):
        self.bienvenida()

    def crear_tweet(self):
        """Inicia la interfaz gráfica para crear un tweet."""
        gui = CrearTweetGUI(self.usuario_actual)
        gui.iniciar()
