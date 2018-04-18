# Uniwersytecka liga e-sportowa

# Vision Doc

Projekt ma na celu stworzenie systemu do obsługi turniejów e-sportowych. Gracze rejerstrują się przez Facebooka, następnie mogą dołączać do turniejów w konkretnych konkurencjach(grach). Mogą zakładać nowe zespoły i wysyłać zaproszenia do graczy, lub wyszukiwać istniejące i wysyłać prośby o dołączenie do nich. Każdy gracz może należeć tylko do jednego zespołu w obrębie jednej gry. Po rozpoczęciu sezonu drużyny wyzywają się wzajemnie na pojedynki (mecze), przez cały czas trwania sezonu. Każdy zespół może rozegrać z każdym tylko jeden mecz w trakcie trwania sezonu. Gracze nie mogą zmieniać zespołów podczas trwania sezonu. Każdy sezon trwa przez z góry określony czas, na początku sezonu wyniki są wyzerowane, po zakończeniu sezonu, wyłaniane są zwycięskie zespoły.

## Przykłady użycia
- Ogólne
  - Zaloguj użytkownika
- Zgłoszenia
  - Zarejestruj użytkownika
  - Załóż nowy zespół
  - Zaproś użytkownika do zespołu
  - Przyjmij zaproszenie do zespołu
  - Wyślij prośbę o dodanie do zespołu
  - Akceptuj prośbę o dodanie do zespołu
  - Opuść zespół
- Rozgrywki
  - Wyzwij zespół na mecz
  - Akceptuj wyzwanie na mecz
  - Wprowadź wynik meczu
  - Sprawdź ranking zespołów
  - Sprawdź historię wyników meczy
## Stos technologiczny

Baza danych: PostgreSQL
Serwer WWW: Nginx/Apache
Web framework: Django
WSGI: Gunicorn



# Model danych
![](https://d2mxuefqeaa7sj.cloudfront.net/s_D35B8BD49B5EB0D54BF7667047B5123D650932141AF033B432BFD1BC4DCD46A8_1513851537903_376a9eea-854b-47eb-a60d-fc20b8f7c39d.png)

## SQL

Generated for postgres:

    -- Created by Vertabelo (http://vertabelo.com)
    -- Last modification date: 2017-12-21 10:19:46.002
    
    -- tables
    -- Table: Faculty
    CREATE TABLE Faculty (
        id int  NOT NULL,
        name varchar(60)  NOT NULL,
        CONSTRAINT Faculty_pk PRIMARY KEY (id)
    );
    
    -- Table: Match
    CREATE TABLE Match (
        id int  NOT NULL,
        created_at timestamp  NOT NULL,
        expires_at timestamp  NOT NULL,
        suggested_at timestamp  NULL,
        inviting_team_id int  NOT NULL,
        guest_team_id int  NOT NULL,
        inviting_score int  NULL,
        guest_score int  NULL,
        CONSTRAINT Match_pk PRIMARY KEY (id)
    );
    
    -- Table: Player
    CREATE TABLE Player (
        id int  NOT NULL,
        Tournament_id int  NOT NULL,
        User_id int  NOT NULL,
        Team_id int  NULL,
        CONSTRAINT Player_pk PRIMARY KEY (id)
    );
    
    -- Table: PlayerInvite
    CREATE TABLE PlayerInvite (
        id int  NOT NULL,
        expire_date timestamp  NOT NULL,
        Player_id int  NOT NULL,
        Team_id int  NOT NULL,
        CONSTRAINT PlayerInvite_pk PRIMARY KEY (id)
    );
    
    -- Table: ScoreProposition
    CREATE TABLE ScoreProposition (
        id int  NOT NULL,
        inviting_score int  NULL,
        guest_score int  NULL,
        suggesting_team_id int  NOT NULL,
        Match_id int  NOT NULL,
        CONSTRAINT ScoreProposition_pk PRIMARY KEY (id)
    );
    
    -- Table: Team
    CREATE TABLE Team (
        id int  NOT NULL,
        is_public bool  NOT NULL,
        Tournament_id int  NOT NULL,
        CONSTRAINT Team_pk PRIMARY KEY (id)
    );
    
    -- Table: TeamRequest
    CREATE TABLE TeamRequest (
        id int  NOT NULL,
        expire_date timestamp  NOT NULL,
        Player_id int  NOT NULL,
        Team_id int  NOT NULL,
        CONSTRAINT TeamRequest_pk PRIMARY KEY (id)
    );
    
    -- Table: Tournament
    CREATE TABLE Tournament (
        id int  NOT NULL,
        game_name varchar(60)  NOT NULL,
        season_start timestamp  NULL,
        season_end timestamp  NULL,
        team_size int  NOT NULL,
        CONSTRAINT Tournament_pk PRIMARY KEY (id)
    );
    
    -- Table: User
    CREATE TABLE "User" (
        id int  NOT NULL,
        facebook_id int  NOT NULL,
        name varchar(60)  NOT NULL,
        surname varchar(60)  NOT NULL,
        mail varchar(60)  NOT NULL,
        faculty_id int  NOT NULL,
        CONSTRAINT User_pk PRIMARY KEY (id)
    );
    
    -- foreign keys
    -- Reference: Match_Team_Guest (table: Match)
    ALTER TABLE Match ADD CONSTRAINT Match_Team_Guest
        FOREIGN KEY (guest_team_id)
        REFERENCES Team (id)  
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    
    -- Reference: Match_Team_Inv (table: Match)
    ALTER TABLE Match ADD CONSTRAINT Match_Team_Inv
        FOREIGN KEY (inviting_team_id)
        REFERENCES Team (id)  
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    
    -- Reference: PlayerInvite_Player (table: PlayerInvite)
    ALTER TABLE PlayerInvite ADD CONSTRAINT PlayerInvite_Player
        FOREIGN KEY (Player_id)
        REFERENCES Player (id)  
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    
    -- Reference: PlayerInvite_Team (table: PlayerInvite)
    ALTER TABLE PlayerInvite ADD CONSTRAINT PlayerInvite_Team
        FOREIGN KEY (Team_id)
        REFERENCES Team (id)  
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    
    -- Reference: Player_Team (table: Player)
    ALTER TABLE Player ADD CONSTRAINT Player_Team
        FOREIGN KEY (Team_id)
        REFERENCES Team (id)  
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    
    -- Reference: Player_Tournament (table: Player)
    ALTER TABLE Player ADD CONSTRAINT Player_Tournament
        FOREIGN KEY (Tournament_id)
        REFERENCES Tournament (id)  
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    
    -- Reference: Player_User (table: Player)
    ALTER TABLE Player ADD CONSTRAINT Player_User
        FOREIGN KEY (User_id)
        REFERENCES "User" (id)  
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    
    -- Reference: ScoreProposition_Match (table: ScoreProposition)
    ALTER TABLE ScoreProposition ADD CONSTRAINT ScoreProposition_Match
        FOREIGN KEY (Match_id)
        REFERENCES Match (id)  
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    
    -- Reference: ScoreProposition_Team (table: ScoreProposition)
    ALTER TABLE ScoreProposition ADD CONSTRAINT ScoreProposition_Team
        FOREIGN KEY (suggesting_team_id)
        REFERENCES Team (id)  
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    
    -- Reference: TeamRequest_Player (table: TeamRequest)
    ALTER TABLE TeamRequest ADD CONSTRAINT TeamRequest_Player
        FOREIGN KEY (Player_id)
        REFERENCES Player (id)  
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    
    -- Reference: TeamRequest_Team (table: TeamRequest)
    ALTER TABLE TeamRequest ADD CONSTRAINT TeamRequest_Team
        FOREIGN KEY (Team_id)
        REFERENCES Team (id)  
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    
    -- Reference: Team_Tournament (table: Team)
    ALTER TABLE Team ADD CONSTRAINT Team_Tournament
        FOREIGN KEY (Tournament_id)
        REFERENCES Tournament (id)  
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    
    -- Reference: User_Faculty (table: User)
    ALTER TABLE "User" ADD CONSTRAINT User_Faculty
        FOREIGN KEY (faculty_id)
        REFERENCES Faculty (id)  
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    
    -- End of file.
    



