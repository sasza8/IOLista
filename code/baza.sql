


CREATE TABLE Users
(
UserID INTEGER PRIMARY KEY,
Login VARCHAR2(100),
Password VARCHAR2(100),
Salt VARCHAR2(100),
FirstName VARCHAR2(100),
LastName VARCHAR2(150),
Email VARCHAR2(100)
);


CREATE TABLE Tasks
(
-- opisuje drzewo konkretnego zadania 
-- robiac zakonczenie konkretnego podzadania nalezy zakonczyc wszystkich jego synow
-- oraz wziac ojca, zmniejszyc mu ChildCounter, jesli ten spadnie do 0 to zakonczyc
-- dodawanie powiazania oczywiscie musi zwiększać ChildCounter
-- aktualizacja podzadania musi przejsc na sama gore drzewa i zaktualizowac czas zmiany
TaskID INTEGER PRIMARY KEY,
Description VARCHAR2(4000),
Owner INTEGER REFERENCES Users,
ParentID INTEGER,
ChildCounter Integer Not NULL, --TODEL? zawiera liczbe niezakonczonych synow tego zadania
Done INTEGER NOT NULL, --TODO poprawic typ
CreatedOn INTEGER NOT NULL,
LastChange INTEGER NOT NULL
);




CREATE TABLE Have_access
(
TaskID INTEGER REFERENCES Tasks,
UserID INTEGER REFERENCES Users,
Permissions INTEGER NOT NULL --maska bitowa zawierajaca uprawnienia
/*
-- & 1  - moze zobaczyc
-- & 2  - moze oznaczyc jako zakonczone
-- & 4  - moze zmienic opis
-- & 8  - moze pokazac innym
-- & 16 - moze dac prawo do zakonczenia
-- & 32 - moze dac prawo do zmiany opisu
-- & 64 - moze usunac zadanie
*/
);