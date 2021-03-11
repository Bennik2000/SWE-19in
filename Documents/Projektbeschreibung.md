# SWE Projekt - VereinSWEbseite

### Beschreibung

Das Projekt soll eine Webanwendung werden, die ein Blog System für Vereine bietet. Angemeldete Benutzer können Beiträge schreiben und veröffentlichen. Unangemeldete Benutzer können die neusten Beiträge sehen. Für angemeldete Benutzer können Rollen mit entsprechenden Rechten zugewiesen werden. Beiträge können Kategorien zugeordnet werden.

Die Beiträge, Benutzer, Rollen werden in einer Datenbank gespeichert.

### Anforderungen an die Webanwendung

- Loginsystem für die Rechteverteilung
- Benutzer erhalten Rollen und Rechte
- Benutzer mit passenden Rechte können Beiträge schreiben und veröffentlichen
- Beiträge können Kategorien zugeordnet werden
- Beiträge können kommentiert werden
- Nicht angemeldete Benutzer sehen nur die Beiträge und können nichts bearbeiten
- Farbschema / Logo kann individuell festgelegt werden

### Verschiedene Ausbaustufen

  - Editor um Beiträge zu bearbeiten/formatieren
  - Angemeldete Benutzer können Termine anlegen, die in einem Kalender angezeigt werden
  - Funktion um Bilder hochzuladen
  - Funktion um Downloads anzubieten
  - Suchfunktion

### Umgebung

- Client Side
  - TypeScript
  - Vue.js
- Server Side:
  - Datenbank wird abstrahiert, sodass sie ausgetauscht werden kann. Vorerst: MariaDB in Docker. 
  - Python mit Flask



### Projektmitglieder

Marco von Rosenberg, Jannik Wellhäußer, Jonas Hille, Leonhard Siegmund, Daniel Christmann, Benedikt Sorge, Tom Kizler, Benedikt Kolb