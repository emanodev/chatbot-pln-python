import nltk
from nltk.chat.util import Chat, reflections
from textblob import TextBlob
import tkinter as tk
from tkinter import scrolledtext, messagebox
import speech_recognition as sr
import pyttsx3
import threading

# Downloads necessários do NLTK (só na primeira execução)
nltk.download('stopwords')
nltk.download('punkt')

# Pares de perguntas e respostas
pares = [
    ['oi', ['Olá!', 'Oi, como posso ajudar?', 'E aí!', 'Fala comigo!', 'Oi oi!']],
    ['olá', ['Oi!', 'Olá, tudo bem?', 'Seja bem-vindo!', 'Como posso te ajudar hoje?']],
    ['e aí', ['E aí! Tudo certo?', 'Oi! No que posso te ajudar?', 'Fala, beleza?']],
    ['bom dia', ['Bom dia!', 'Bom dia! Preparado para aprender algo novo?']],
    ['boa tarde', ['Boa tarde!', 'Boa tarde! No que posso te ajudar?']],
    ['boa noite', ['Boa noite!', 'Boa noite! Está estudando até tarde?']],

    ['como você está?', ['Estou bem, obrigado. E você?', 'Tudo certo!', 'Melhor agora que você chegou.', 'Funcionando normalmente.']],
    ['tudo bem?', ['Tudo sim! E com você?', 'Tudo certo por aqui!', 'Sim, tudo em ordem!']],
    ['você está bem?', ['Sim, obrigado por perguntar!', 'Estou ótimo!', 'Sim, pronto pra te ajudar.']],
    ['tá bem?', ['Tô sim!', 'Estou bem, e você?', 'Sim, tudo certo.']],

    ['quem é você?', ['Sou seu professor virtual.', 'Me chame de Prof.', 'Sou uma IA pronta pra te ajudar.', 'Alguém que está aqui só por você.']],
    ['o que você é?', ['Sou um assistente virtual com inteligência artificial.', 'Um chatbot com conhecimento útil.', 'Uma mistura de tecnologia e boa vontade.']],
    ['você é um robô?', ['Mais ou menos! Sou uma IA, mas prefiro "professor digital".', 'Sou digital, mas tento ser o mais humano possível.', 'Sim, mas com bom coração de silício.']],

    ['qual é o seu objetivo?', ['Meu objetivo é ajudar a responder suas perguntas.', 'Estou aqui para te ensinar.', 'Quero te auxiliar no que você precisar.', 'Aprender junto com você.']],
    ['pra que você serve?', ['Sirvo para responder dúvidas, conversar e até te ouvir!', 'Pra te ajudar, oras!', 'Pra tornar sua vida mais fácil com conhecimento.']],
    ['o que você faz?', ['Respondo perguntas, analiso sentimentos, e às vezes escuto sua voz.', 'Ajudo você com informações e bom humor.', 'Posso conversar e até falar!']],

    ['sair', ['Até mais!', 'Encerrando o chat.', 'Tchau! Foi bom conversar com você.', 'Volte sempre que quiser.']],
    ['tchau', ['Tchau tchau!', 'Até logo!', 'Se cuida!', 'Nos vemos em breve!']],
    ['até mais', ['Até mais!', 'Fico por aqui. Te vejo depois.', 'Valeu! Até a próxima.']],
    ['adeus', ['Adeus é muito forte... prefiro um "até breve"!', 'Adeus, mas espero que volte.', 'Até logo então.']],

    ['estou triste', ['Poxa, se quiser conversar, estou aqui.', 'Sinto muito. Quer me contar mais?', 'Você não está sozinho.', 'Quer desabafar?']],
    ['estou feliz', ['Que bom! Fico feliz por você.', 'Isso é ótimo de ouvir!', 'Maravilha! Conte mais.']],
    ['estou bem', ['Que bom! Fico feliz por você.', 'Isso é ótimo de ouvir!', 'Maravilha! Conte mais.']],
    ['não estou bem', ['Sinto muito por isso. Quer conversar?', 'Se quiser, posso te distrair um pouco.', 'Estou aqui se precisar falar sobre isso.']],

    ['i am sad', ['Poxa, se quiser conversar, estou aqui.', 'Sinto muito. Quer me contar mais?', 'Você não está sozinho.', 'Quer desabafar?']],
    ['i am happy', ['Que bom! Fico feliz por você.', 'Isso é ótimo de ouvir!', 'Maravilha! Conte mais.']],
    ['i am fine', ['Que bom! Fico feliz por você.', 'Isso é ótimo de ouvir!', 'Maravilha! Conte mais.']],
    ['i am not well', ['Sinto muito por isso. Quer conversar?', 'Se quiser, posso te distrair um pouco.', 'Estou aqui se precisar falar sobre isso.']],

    ['você me escuta?', ['Escuto sim! Ou melhor, leio com atenção.', 'Claro! Pode falar.', 'Tô aqui, manda ver.']],
    ['você entende português?', ['Sim, entendo português perfeitamente.', 'Claro! É o idioma que melhor falo.']],
]

# Cria o chatbot com reflections
chatbot = Chat(pares, reflections)

# Inicializa o mecanismo de texto para fala
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def falar(texto):
    def run():
        engine.say(texto)
        engine.runAndWait()
    threading.Thread(target=run).start()

def analisar_sentimento(texto):
    try:
        blob = TextBlob(texto)
        texto_en = str(blob.translate(to='en'))
        blob_en = TextBlob(texto_en)
        polaridade = blob_en.sentiment.polarity
    except Exception:
        blob = TextBlob(texto)
        polaridade = blob.sentiment.polarity

    if polaridade > 0:
        return "Isso parece positivo! 😊"
    elif polaridade < 0:
        return "Isso parece negativo. 😔"
    else:
        return "Não consigo determinar o sentimento com certeza. 🤔"

def salvar_historico(texto):
    with open("historico_chat.txt", "a", encoding="utf-8", newline="\n") as f:
        f.write(texto)

def enviar_mensagem(mensagem=None):
    if mensagem is None:
        mensagem = entry_msg.get()
    if not mensagem.strip():
        return
    mensagem_limpa = mensagem.lower().strip()

    # Verifica se contém palavras de encerramento
    if any(p in mensagem_limpa for p in ['sair', 'tchau', 'até mais', 'adeus']):
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, "Chat encerrado.\n")
        chat_display.config(state=tk.DISABLED)
        falar("Até mais!")
        window.after(1000, window.destroy)
        return

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"Você: {mensagem}\n")

    resposta = chatbot.respond(mensagem_limpa)
    resposta = resposta if resposta else "Não entendi."

    chat_display.insert(tk.END, f"Chatbot: {resposta}\n")
    falar(resposta)

    sentimento = analisar_sentimento(mensagem)
    chat_display.insert(tk.END, f"[Análise de Sentimento] {sentimento}\n\n")
    chat_display.see(tk.END)
    chat_display.config(state=tk.DISABLED)

    salvar_historico(f"Você: {mensagem}\nChatbot: {resposta}\nSentimento: {sentimento}\n\n")
    entry_msg.delete(0, tk.END)

def reconhecer_fala():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, "Ouvindo...\n")
        chat_display.see(tk.END)
        chat_display.config(state=tk.DISABLED)
        try:
            audio = r.listen(source, timeout=5)
            mensagem = r.recognize_google(audio, language='pt-BR')
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"Você (voz): {mensagem}\n")
            chat_display.see(tk.END)
            chat_display.config(state=tk.DISABLED)
            enviar_mensagem(mensagem)
        except sr.WaitTimeoutError:
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, "Tempo esgotado. Não ouvi nada.\n")
            chat_display.see(tk.END)
            chat_display.config(state=tk.DISABLED)
            messagebox.showinfo("Tempo esgotado", "Não ouvi nada. Tente falar novamente.")
        except sr.UnknownValueError:
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, "Chatbot: Não entendi o que você falou.\n")
            chat_display.see(tk.END)
            chat_display.config(state=tk.DISABLED)
            messagebox.showinfo("Não entendi", "Não consegui entender o que você falou.")
        except sr.RequestError:
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, "Erro no reconhecimento de voz.\n")
            chat_display.see(tk.END)
            chat_display.config(state=tk.DISABLED)
            messagebox.showerror("Erro", "Erro no serviço de reconhecimento de voz.")

# Interface
window = tk.Tk()
window.title("Chatbot com Voz, Análise de Sentimento e Histórico")
window.geometry("600x500")
window.configure(bg="#1e1e1e")

frame_chat = tk.Frame(window, bg="#1e1e1e")
frame_chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_display = scrolledtext.ScrolledText(frame_chat, state='disabled', wrap=tk.WORD,
                                         font=("Consolas", 12), bg="#1e1e1e", fg="#d4d4d4",
                                         insertbackground="white", relief=tk.FLAT)
chat_display.pack(fill=tk.BOTH, expand=True)

frame_input = tk.Frame(window, bg="#1e1e1e")
frame_input.pack(fill=tk.X, padx=10, pady=(0, 10))

entry_msg = tk.Entry(frame_input, font=("Consolas", 14), bg="#252526", fg="white",
                     insertbackground="white", relief=tk.FLAT)
entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

btn_enviar = tk.Button(frame_input, text="Enviar", font=("Arial", 12, "bold"), bg="#808080",
                       fg="white", relief=tk.FLAT, activebackground="#808080",
                       command=lambda: enviar_mensagem())
btn_enviar.pack(side=tk.LEFT)

btn_fala = tk.Button(frame_input, text="🎤", font=("Arial", 14), bg="#808080",
                     fg="white", relief=tk.FLAT, activebackground="#808080",
                     command=lambda: threading.Thread(target=reconhecer_fala).start())
btn_fala.pack(side=tk.LEFT, padx=(5,0))

def on_enter(event):
    enviar_mensagem()
entry_msg.bind("<Return>", on_enter)

chat_display.config(state=tk.NORMAL)
chat_display.insert(tk.END, "Chatbot iniciado! Diga oi para começar.\n\n")
chat_display.config(state=tk.DISABLED)

window.mainloop()