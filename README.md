# AIF-Project

## Struttura progetto

Intanto sappiamo che:
- Ci piace l'idea di fare 2 agenti (algoritmi comparati ✔️)
<!--
### Proposta 1
- Agente che gioca e apprende la mappa (sconosciuta) e deve reagire o evitare le trappole dell'altro
- Agente "antagonista" che cambia dinamicamente la mappa inserendo trappole etc.

### Proposta 2
- 2 agenti che gareggiano a chi finisce prima il gioco
- Differenze tra i 2 agenti (es. vantaggi diversi)
- Oppure, sono antagonisti tra loro: entrambi possono mettere un tot di trappole
- O anche: uno inizia prima e ha vantaggio, e l'altro invece può mettere trappole (e variazioni sul tema)

### Proposta 3
- Due agenti diversi che partono insieme ma con due algoritmi diversi (es. BFS e DFS) ➡️ magari hanno euristiche diverse
- Consideriamo a livello statistico chi performa meglio in base al tipo di mappa 

Consideriamo che **anche l'agente antagonista può essere ucciso dai mostri**

Incrementare difficoltà: ci mettiamo più antagonisti
-->
### Idea 1
- 2 agenti con **euristiche diverse** su istanze separate della stessa mappa
- Più livelli!
- Statistiche sui risultati 
### Idea 2 (per ora favorita ✔️)
- Agente1 **antagonista** che gioca in una mappa non modificabile 
- Agente1 aggiunge **modifiche alla mappa in cui giocherà agente2** per ostacolarlo
- Agente1 parte prima di agente2 
*Non è possibile far sì che si ostacolino a vicenda, c'è agente antagonista e agente protagonista. Però, dopo ogni livello si ostacolano*
Possiamo partire con questa situazione: agente1 **non** gioca, crea solo la mappa. Quando agente2 vince, gioca agente1 e agente2 diventa l'antagonista.
- Fine gioco: un agente perde

