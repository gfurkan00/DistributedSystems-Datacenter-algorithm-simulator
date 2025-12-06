# Protocollo Paxos (Basic Version)

## Introduzione
Paxos è un algoritmo di consenso distribuito che permette a un insieme di processi di accordarsi su un singolo valore, anche in presenza di fallimenti dei nodi (crash failures) o ritardi nella rete. È considerato uno dei protocolli più robusti e fondamentali nei sistemi distribuiti.

In questa spiegazione ci concentreremo sulla versione **Basic Paxos** (o Single-Decree Paxos), che mira a raggiungere il consenso su un *singolo* valore.

## Ruoli dei Nodi
In Paxos, i nodi possono assumere uno o più dei seguenti ruoli logici:

1.  **Proposer (Proponente)**:
    *   Riceve le richieste dai client.
    *   Propone un valore da concordare agli Acceptor.
    *   Guida il processo di consenso.
2.  **Acceptor (Accettatore)**:
    *   Vota le proposte ricevute dai Proposer.
    *   Mantiene lo stato del protocollo (es. il numero di proposta più alto visto finora) per garantire la consistenza.
    *   Costituiscono la "memoria" del sistema. Per prendere una decisione, è necessario il consenso della maggioranza (Quorum) degli Acceptor.
3.  **Learner (Apprendista)**:
    *   Apprende il valore che è stato deciso (scelto) dalla maggioranza degli Acceptor.
    *   Comunica il risultato ai client o esegue l'azione concordata.

*Nota: In molte implementazioni reali, un singolo nodo fisico svolge tutti e tre i ruoli contemporaneamente.*

## Concetti Chiave

### Proposal Number (Numero di Proposta)
Ogni proposta è identificata da un numero univoco `n`.
*   I numeri devono essere **monotoni crescenti**.
*   Se due Proposer tentano di proporre contemporaneamente, il numero di proposta serve a risolvere i conflitti (vince chi ha il numero più alto).
*   Spesso formattato come `(round_number, node_id)` per garantire unicità e ordinamento.

### Quorum
Un Quorum è un sottoinsieme di Acceptor che rappresenta la maggioranza stretta (N/2 + 1). Affinché una proposta proceda, deve essere approvata da un Quorum. Questo garantisce che non possano essere scelti due valori diversi, poiché due maggioranze hanno sempre almeno un nodo in comune.

## Il Protocollo (Fasi)

Il protocollo si svolge in due fasi principali.

### Fase 1: Prepare (Preparazione)
L'obiettivo di questa fase è ottenere la "leadership" temporanea per un numero di proposta `n` e scoprire se è già stato scelto o parzialmente accettato un valore in precedenza.

1.  **Phase 1a: Prepare Request**
    *   Il **Proposer** sceglie un numero di proposta `n` (più alto di qualsiasi `n` abbia usato prima).
    *   Invia un messaggio `PREPARE(n)` a un Quorum di Acceptor.

2.  **Phase 1b: Promise (Promessa)**
    *   L'**Acceptor** riceve `PREPARE(n)`.
    *   Controlla se `n` è maggiore di qualsiasi numero di proposta a cui ha già risposto (`min_proposal`).
    *   **SE** `n > min_proposal`:
        *   Aggiorna il suo `min_proposal = n`.
        *   Risponde con `PROMISE(n, accepted_proposal, accepted_value)`.
            *   Promette di non accettare più proposte con numero inferiore a `n`.
            *   Se aveva già accettato un valore in passato (in Fase 2), lo restituisce (`accepted_value`) insieme al numero di quella proposta (`accepted_proposal`). Altrimenti restituisce null.
    *   **ALTRIMENTI** (se `n <= min_proposal`):
        *   Ignora la richiesta o risponde con un `NACK` (opzionale, per ottimizzazione).

### Fase 2: Accept (Accettazione)
Se il Proposer riceve promesse dalla maggioranza, può procedere a proporre un valore.

1.  **Phase 2a: Accept Request (Proponi)**
    *   Il **Proposer** raccoglie le risposte `PROMISE`.
    *   Deve decidere quale valore `v` proporre:
        *   **SE** qualche Acceptor ha restituito un `accepted_value` nella Fase 1b, il Proposer **DEVE** adottare il valore associato al numero di proposta più alto tra quelli ricevuti.
        *   **SE** nessuno ha restituito un valore (tutti null), il Proposer può scegliere liberamente il valore `v` (es. quello richiesto dal client).
    *   Invia un messaggio `ACCEPT(n, v)` al Quorum di Acceptor.

2.  **Phase 2b: Accepted**
    *   L'**Acceptor** riceve `ACCEPT(n, v)`.
    *   Controlla se ha promesso di non accettare proposte > `n`. In pratica, accetta SE `n >= min_proposal`.
    *   **SE** la condizione è vera:
        *   Registra il valore: `accepted_proposal = n`, `accepted_value = v`.
        *   Invia un messaggio `ACCEPTED(n, v)` ai Learner (o al Proposer che poi notifica i Learner).

### Fase 3: Learning (Apprendimento)
Quando un **Learner** riceve messaggi `ACCEPTED(n, v)` da un Quorum di Acceptor per lo stesso `n` e `v`, considera il valore **DECISO** (Chosen).

## Scenari Verificabili ed Esempi Dettagliati

## Scenari Verificabili ed Esempi Dettagliati (Exhaustive)

Questa sezione elenca tutti gli scenari critici verificabili per testare la correttezza di un'implementazione Paxos. Ogni scenario descrive la condizione iniziale, gli eventi e il comportamento atteso.

### Categoria A: Funzionamento Normale e Tolleranza ai Guasti Semplice

#### Scenario 1: Consenso Semplice (Happy Path)
*   **Condizione**: 1 Proposer (P1), 3 Acceptor (A1, A2, A3), Nessun guasto.
*   **Eventi**:
    1.  P1 invia `PREPARE(1)`.
    2.  A1, A2, A3 rispondono `PROMISE(1, null, null)`.
    3.  P1 invia `ACCEPT(1, "ValoreA")`.
    4.  A1, A2, A3 accettano e inviano `ACCEPTED(1, "ValoreA")`.
*   **Risultato Atteso**: "ValoreA" viene deciso.

#### Scenario 2: Tolleranza a Guasto di Minoranza (1 Acceptor Offline)
*   **Condizione**: A3 è offline/crashing.
*   **Eventi**:
    1.  P1 invia `PREPARE(1)` a tutti. Riceve risposte solo da A1, A2 (Maggioranza).
    2.  P1 invia `ACCEPT(1, "ValoreA")` a A1, A2.
    3.  A1, A2 accettano e notificano i Learner.
*   **Risultato Atteso**: "ValoreA" viene deciso (2 su 3 è maggioranza). Il sistema non si blocca.

#### Scenario 3: Stallo per Guasto di Maggioranza (2 Acceptor Offline)
*   **Condizione**: A2 e A3 sono offline.
*   **Eventi**:
    1.  P1 invia `PREPARE(1)`. Riceve risposta solo da A1.
    2.  P1 attende ma non raggiunge mai il Quorum.
*   **Risultato Atteso**: P1 non invia mai `ACCEPT`. Nessun valore viene deciso. **Safety preservata** (nessuna decisione errata).

### Categoria B: Gestione dei Fallimenti del Proposer (Switching)

#### Scenario 4: Proposer Fallisce dopo Fase 1 (Nessun Valore)
*   **Condizione**: P1 completa Fase 1 ma crasha prima di inviare ACCEPT.
*   **Eventi**:
    1.  P1 riceve promesse per `n=1` da A1, A2, A3. Crasha.
    2.  P2 inizia con `n=2`. Invia `PREPARE(2)`.
    3.  A1, A2, A3 rispondono `PROMISE(2, null, null)` (nessun valore era stato accettato).
    4.  P2 è libero di proporre "ValoreB".
*   **Risultato Atteso**: "ValoreB" viene accettato e deciso.

#### Scenario 5: Proposer Fallisce con Valore Parzialmente Accettato (Visibile)
*   **Condizione**: P1 fa accettare "ValoreA" a A1, poi crasha. P2 consulta A1.
*   **Eventi**:
    1.  P1 invia `ACCEPT(1, "ValoreA")` solo a A1. A1 accetta. P1 crasha.
    2.  P2 invia `PREPARE(2)` a A1, A2.
    3.  A1 risponde `PROMISE(2, 1, "ValoreA")`.
    4.  A2 risponde `PROMISE(2, null, null)`.
    5.  P2 vede che A1 ha accettato "ValoreA".
*   **Risultato Atteso**: P2 **DEVE** adottare "ValoreA". Invia `ACCEPT(2, "ValoreA")`. "ValoreA" viene deciso.

#### Scenario 6: Proposer Fallisce con Valore Parzialmente Accettato (Nascosto/Sovrascrittura)
*   **Condizione**: P1 fa accettare "ValoreA" a A1, poi crasha. P2 consulta A2, A3 (non A1).
*   **Eventi**:
    1.  P1 invia `ACCEPT(1, "ValoreA")` solo a A1. A1 accetta. P1 crasha.
    2.  P2 invia `PREPARE(2)` a A2, A3 (Quorum valido).
    3.  A2, A3 rispondono `PROMISE(2, null, null)` (non hanno visto P1).
    4.  P2 non vede nessun valore. Propone "ValoreB".
    5.  A2, A3 accettano "ValoreB".
*   **Risultato Atteso**: "ValoreB" viene deciso. Questo è corretto perché "ValoreA" non era mai stato deciso (maggioranza non raggiunta). A1 eventualmente si aggiornerà o verrà ignorato.

#### Scenario 7: Proposer Fallisce dopo Decisione (Valore Già Scelto)
*   **Condizione**: "ValoreA" è già deciso (su A1, A2). P2 subentra.
*   **Eventi**:
    1.  A1, A2 hanno accettato `(1, "ValoreA")`.
    2.  P2 invia `PREPARE(2)` a A2, A3.
    3.  A2 risponde `PROMISE(2, 1, "ValoreA")`.
    4.  P2 vede "ValoreA".
*   **Risultato Atteso**: P2 **DEVE** adottare "ValoreA". Il valore deciso non cambia mai.

### Categoria C: Concorrenza

#### Scenario 8: Preemption (Sorpasso)
*   **Condizione**: P1 lento, P2 veloce.
*   **Eventi**:
    1.  P1 invia `PREPARE(1)` -> A1, A2 rispondono OK.
    2.  P2 invia `PREPARE(2)` -> A1, A2 rispondono OK (e aggiornano `min_proposal` a 2).
    3.  P1 invia `ACCEPT(1, "ValoreA")`.
*   **Risultato Atteso**: A1, A2 **RIFIUTANO** (o ignorano) la richiesta di P1 perché `1 < 2`. P1 deve riprovare con `n > 2`.

#### Scenario 9: Livelock (Duello Infinito)
*   **Condizione**: P1 e P2 continuano a superarsi nella Fase 1 senza mai completare la Fase 2.
*   **Eventi**:
    1.  P1: `PREPARE(1)` OK.
    2.  P2: `PREPARE(2)` OK.
    3.  P1: `ACCEPT(1)` FALLISCE. Riprova `PREPARE(3)`.
    4.  P2: `ACCEPT(2)` FALLISCE (causa `n=3` di P1). Riprova `PREPARE(4)`.
    5.  ...ripetizione...
*   **Risultato Atteso**: Il sistema non decide nulla (Liveness failure). Test per verificare la necessità di backoff casuale.

### Categoria D: Rete e Messaggi

#### Scenario 10: Messaggi Ritardati (Old Messages)
*   **Condizione**: Un messaggio `PREPARE(1)` arriva dopo che `n=5` è già stato processato.
*   **Eventi**:
    1.  A1 ha `min_proposal = 5`.
    2.  Arriva `PREPARE(1)` (vecchio pacchetto ritardato).
*   **Risultato Atteso**: A1 ignora il messaggio o risponde NACK. Non deve decrementare `min_proposal`.

#### Scenario 11: Perdita di Pacchetti (Packet Loss)
*   **Condizione**: `PREPARE` o `ACCEPT` persi nella rete.
*   **Eventi**:
    1.  P1 invia `PREPARE(1)`. Messaggio verso A2 perso.
    2.  P1 riceve risposta solo da A1 (non maggioranza).
*   **Risultato Atteso**: P1 va in timeout e ritrasmette (o incrementa `n` e riprova). Il protocollo non deve bloccarsi indefinitamente.

#### Scenario 12: Learner Disconnesso
*   **Condizione**: Un Learner non riceve i messaggi `ACCEPTED`.
*   **Eventi**:
    1.  Consenso raggiunto su "ValoreA". Acceptor inviano messaggi.
    2.  Learner L1 perde i messaggi.
*   **Risultato Atteso**: L1 non apprende il valore. (In implementazioni avanzate, L1 dovrebbe chiedere periodicamente lo stato agli Acceptor o agli altri Learner).

## Proprietà Garantite
*   **Safety (Validità e Accordo)**: Non verranno mai decisi due valori diversi. Solo un valore proposto può essere scelto.
*   **Liveness (Progresso)**: Sebbene Paxos teoricamente possa stallare (livelock) se due Proposer continuano a superarsi a vicenda con i numeri di proposta (duello di Proposer), nella pratica si usano timeout casuali o un Leader eletto per garantire che qualcuno riesca a finire le due fasi.
