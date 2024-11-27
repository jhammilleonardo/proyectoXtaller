from base_datos import BaseDatos

class Tweet:
    def __init__(self):
        self.db = BaseDatos()

    def obtener_tweets(self):
        """Obtiene los tweets junto con el nombre del usuario que los publicó y el ID de la publicación."""
        conexion = self.db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                """
                SELECT p.id_publicacion, p.id_usuario, u.nombre_usuario, p.contenido, p.fecha_publicacion
                FROM publicaciones p
                INNER JOIN usuarios u ON p.id_usuario = u.id_usuario
                ORDER BY p.fecha_publicacion DESC
                """
            )
            tweets = cursor.fetchall()
            return tweets
        except Exception as e:
            print(f"❌ Error al obtener tweets: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    def obtener_tweet_por_id(self, id_tweet):
        """Obtiene un tweet específico por su ID."""
        conexion = self.db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                """
                SELECT p.id_publicacion, p.id_usuario, u.nombre_usuario, p.contenido, p.fecha_publicacion
                FROM publicaciones p
                INNER JOIN usuarios u ON p.id_usuario = u.id_usuario
                WHERE p.id_publicacion = %s
                """, (id_tweet,)
            )
            tweet = cursor.fetchone()
            return tweet
        except Exception as e:
            print(f"❌ Error al obtener el tweet: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()
