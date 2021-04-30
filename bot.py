import telebot
import time
import threading

#Variables Globales
enviados = 0
recibidos = 0


#Decoradores
def controlador_mensajes(cant_enviar):
    """
        controlador_mensajes:
        Cuenta cuantos mensajes recibe y envia, si recibe o envia mas de 20 entonces duerme por un segundo

        sacado de la documentacion de telegram:
            My bot is hitting limits, how do I avoid this?
            When sending messages inside a particular chat, avoid sending more than one message per second. 
            We may allow short bursts that go over this limit, but eventually you'll begin receiving 429 errors.
            If you're sending bulk notifications to multiple users, the API will not allow more than 30 messages 
            per second or so. Consider spreading out notifications over large intervals of 8—12 hours for best results.
            Also note that your bot will not be able to send more than 20 messages per minute to the same group.
    """
    def Decorador(funcion):
        def wrapper(*args, **kwargs):
            global recibidos,enviados
            recibidos +=1
            enviados += cant_enviar
            if enviados >= 20 or recibidos >= 20:
                time.sleep(1)
                enviados  = 0
                recibidos  = 0
            funcion(*args,**kwargs)
        return wrapper
    return Decorador

class Bot(telebot.Telebot):

    def __init__(self,token, threaded=True, skip_pending=False, num_threads=2):
        super().__init__(token, threaded=True, skip_pending=False, num_threads=2)

        #messages_handler
        """
            diccionario de todos los metodos de mensajes que reciba el bot
        """
        messages_handler={
            'start':dict(
                function=lambda msg, obj= self: obj.start(msg),
                filters = dict(
                    commands=["start"]
                )
            ),
        }

        #callback_query_answers
        """
            diccionario de todos los metodso de callback query answers que reciba el bot
        """
        callback_query_handler={
            'start':dict(
                function=lambda msg, obj= self: obj.start(msg),
                filters = dict(
                    commands=["start"]
                )
            ),
        }

        """
            para agregar cada comando se debe usar estos metodos
        """
        for comando in messages_handler.values():
            self.add_message_handler(comando)
        for comando in messages_handler.values():
            self.add_callback_query_handler(comando)


def bot_polling(token):
    while True:
        bot = None
        try:
            bot = Bot(token,threaded=False)
            bot.polling(none_stop=True,interval=0,timeout=0)
        except Exception as ex: #Error in polling
            bot.stop_polling()
        else: #Clean exit
            bot.stop_polling()
            break #End loop

polling_thread = threading.Thread(target=bot_polling)
polling_thread.daemon = True
polling_thread.start()


if __name__ == "__main__":
    while True:
        try:
            time.sleep(120)
        except KeyboardInterrupt:
            break    