# Transcrever áudio
# -----------------

import speech_recognition as sr
from pydub import AudioSegment
import os

def transcrever_audio_varios_formatos(arquivo_audio):
    # Verifica a extensão do arquivo
    folder = "media\\"
    arquivo_audio = folder + arquivo_audio
    formato = arquivo_audio.split('.')[-1].lower()

    # Converte para WAV se o formato não for compatível diretamente com SpeechRecognition
    if formato != 'wav':
        audio = AudioSegment.from_file(arquivo_audio, format=formato)
        arquivo_audio = "temp_audio.wav"
        audio.export(arquivo_audio, format="wav")

    # Inicia o recognizer
    recognizer = sr.Recognizer()

    with sr.AudioFile(arquivo_audio) as source:
        audio = recognizer.record(source)  # Lê o arquivo de áudio

    # Transcreve o áudio
    try:
        texto = recognizer.recognize_google(audio,
                                            language="pt-BR")  # Transcrição em português
        print("Transcrição:", texto)
        return texto
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio.")
    except sr.RequestError as e:
        print(f"Erro na requisição: {e}")
    finally:
        # Remove o arquivo temporário, se criado
        if formato != 'wav' and os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")

def salvar_txt(arquivo, nome):
    texto = transcrever_audio_varios_formatos(arquivo)

    with open(f'transcriptions\\{nome}.txt', 'w') as f:
        f.write(texto)

def criar_pasta_armazenamento():
    pasta = '.\\transcriptions'
    # Verifica se a pasta não existe e a cria
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        print(f"Pasta '{pasta}' criada com sucesso!")
    else:
        print(f"A pasta '{pasta}' já existe.")


if __name__ == 'main':
    criar_pasta_armazenamento()
    salvar_txt('audio.ogg', 'audio_transcrito')
    salvar_txt('video.mp4', 'video_transcrito')
