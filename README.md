# Uniwersytecka liga e-sportowa

# Project vision

This project aims to create a system for managing sport and e-sport leagues. Having been developed as a univeristy course assignemnt, it is not intended for commercial use.  

![screenshots](https://i.imgur.com/CtGjuHt.png)

## Features  
Application allows users to log in or register via Facebook. Registered users can join an existing tournament or create a new one. User becomes a player after joining a tournament. Each tournament represents one game. Before the tournament games begin, the tournament is in team forming period. During this period, players without a team can request joining a public team (that is, a team that is publicly visible), or accept a team invitation from any team, if they received one. In team forming period, players without a team can create a team, they are then automatically assignet to that team. Players that already have a team in this period can invite others to join their team, or accept a team join request from other players if team is public. After team forming phase is finished, the players can no longer change, create or remove their teams.  
  
After deadline for forming teams passes, the tournament enters the season phase. During this phase, teams can challenge each other by creating a match. In current version of the app, two teams can only play one match in one tournament. To complete a match, both teams have to enter their score propositions. If scores in both propositions are equal, both teams' scores are updated. In final version of the app, we want a tournament manager to be notified if two teams cannot agree on a score. Teams' scores can be previewed by team members on their team page, or by any other player on a tournament ranking page.  

# Stack  
Backend: Python3, Django + plugin: Django Social Auth  
DB: SQLite  
Front-end: Django templates + materialize.css  

# Data model  
![](https://d2mxuefqeaa7sj.cloudfront.net/s_D35B8BD49B5EB0D54BF7667047B5123D650932141AF033B432BFD1BC4DCD46A8_1513851537903_376a9eea-854b-47eb-a60d-fc20b8f7c39d.png)
  
## SQL schema
  
Generated for postgres as a requirement for database course, but never used - see django migrations instead.  
```
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
    
```


## Extending this project  

Here are some of the things that might be useful in the future:  
* add support for tournament admin (currently management can only be done via django admin, with access to all tournaments)  
* add API to allow use from mobile / 3rd party apps  
* re-write frontend in vue or react for easier embedding  
* create a mobile client - react native?  
* check application security  
