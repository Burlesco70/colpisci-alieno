from pgzero.actor import Actor
from pgzero.clock import clock
from random import randint
import pgzrun


# Funzione per nascondere il messaggio di feedback
def nascondi_messaggio():
    global messaggio
    messaggio = ""

# Funzione per il disegno su schermo
def draw():
    global messaggio, punteggio, vite, tempo, gioco_attivo

    screen.clear()
    screen.blit('earth_planet_shadow', (0, 0) )  # sfondo

    # Disegna l'alieno solo se il gioco è attivo
    if gioco_attivo:
        alieno.draw()
    else:
        # Se il tempo è scaduto o le vite sono finite, mostra il messaggio finale
        messaggio = ""
        screen.draw.text("Game Over", center=(WIDTH / 2, HEIGHT / 2 - 100), fontsize=80, color="red")
        screen.draw.text("Premi qualsiasi tasto per ricominciare", center=(WIDTH / 2, HEIGHT / 2 + 100), fontsize=40, color="white")

    # Mostra il punteggio
    screen.draw.text(f"Punteggio: {punteggio}", topleft=(10, 10), fontsize=30, color="white")
    # Mostra le vite
    screen.draw.text(f"Vite: {vite}", topleft=(10, 40), fontsize=30, color="cyan")
    # Mostra il timer
    screen.draw.text(f"Tempo: {tempo}", topright=(WIDTH - 10, 10), fontsize=30, color="green")

    # Messaggi di feedback (es: "Bel colpo!" o "Mancato...")
    #screen.draw.text(messaggio, center=(WIDTH / 2, HEIGHT / 2), fontsize=60, color="yellow")
    screen.draw.text(messaggio, center=(WIDTH / 2, HEIGHT - 40), fontsize=60, color="yellow")


# Funzione per posizionare l'alieno in una posizione casuale
def piazza_alieno():
    global alieno, punteggio, vite, gioco_attivo

    if tempo > 0 and vite > 0 and gioco_attivo:
        # Limita il movimento dell'alieno per evitare che esca dallo schermo
        alieno.x = randint(50, WIDTH - 50)
        alieno.y = randint(50, HEIGHT - 50)

        # L'alieno si muove più velocemente dopo 10 e 20 colpi riusciti
        if punteggio > 10 and punteggio < 20:
            clock.unschedule(piazza_alieno)
            clock.schedule_interval(piazza_alieno, 0.7)  # Riprende la pianificazione dell'alieno
        elif punteggio >= 20:
            clock.unschedule(piazza_alieno)
            clock.schedule_interval(piazza_alieno, 0.5)  # Riprende la pianificazione dell'alieno

        alieno.image = "alieno"  # Assicurati che l'immagine dell'alieno sia impostata correttamente

# Funzione per rilevare quando l'alieno viene colpito o mancato
def on_mouse_down(pos):
    global messaggio, punteggio, vite, gioco_attivo

    if gioco_attivo:
        # Se il clic è sopra l'alieno
        if alieno.collidepoint(pos):
            messaggio = "Bel colpo!"
            sounds.colpo.play()  # Suono quando colpisci l'alieno
            punteggio += 1  # Incrementa il punteggio
            alieno.image = "esplosione"  # Cambia l'immagine dell'alieno
        else:
            messaggio = "Mancato..."
            sounds.mancato.play()  # Suono quando fallisci
            vite -= 1  # Riduci una vita

        # Pianifica la scomparsa del messaggio dopo 0.5 secondi
        clock.schedule(nascondi_messaggio, 0.5)           

        # Se le vite sono 0 o il tempo è finito, termina il gioco
        if vite <= 0 or tempo <= 0:
            sounds.game_over.play()
            gioco_attivo = False
            clock.unschedule(piazza_alieno)  # Ferma la programmazione della funzione piazza_alieno
            clock.unschedule(aggiorna_timer)  # Ferma la programmazione del timer

# Funzione per aggiornare il timer
def aggiorna_timer():
    global tempo, vite, gioco_attivo
    if tempo > 0 and vite > 0 and gioco_attivo:
        tempo -= 1  # Decrementa il tempo ogni secondo
    if tempo <= 0 or vite <= 0:
        sounds.game_over.play()
        gioco_attivo = False
        clock.unschedule(piazza_alieno)  # Ferma il gioco quando il tempo o le vite finiscono
        clock.unschedule(aggiorna_timer)

# Funzione per ricominciare il gioco
def ricomincia_gioco():
    global punteggio, vite, tempo, messaggio, gioco_attivo
    punteggio = 0
    vite = 3
    tempo = 30
    messaggio = ""
    gioco_attivo = True  # Abilita il gioco
    clock.schedule_interval(piazza_alieno, 1.0)  # Riprende la pianificazione dell'alieno
    clock.schedule_interval(aggiorna_timer, 1.0)  # Riprende la pianificazione del timer

# Gestisci il riavvio del gioco quando si preme un tasto qualsiasi
def on_key_down(key):
    global gioco_attivo
    if not gioco_attivo:  # Se il gioco è finito
        ricomincia_gioco()  # Ricomincia il gioco


TITLE = "Colpisci l'alieno - DELUXE EDITION"
WIDTH = 800
HEIGHT = 600

# Variabili globali per punteggio, vite e tempo, gioco attivo, messaggio
punteggio = 0
vite = 3
tempo = 30
gioco_attivo = True  
messaggio = ""

# Crea l'alieno
alieno = Actor("alieno")
# Pianifica la chiamata della funzione per piazzare l'alieno ogni 1 secondo
clock.schedule_interval(piazza_alieno, 1.0)
clock.schedule_interval(aggiorna_timer, 1.0)
# Avvia il gioco
pgzrun.go()
