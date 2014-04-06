CREATE TABLE Users
(
UserID INTEGER NOT NULL,
Login VARCHAR(100),
Password VARCHAR(100),

FirstName VARCHAR(100),
LastName VARCHAR(150),
Email VARCHAR(100),

PRIMARY KEY (UserID)
);


CREATE TABLE Sub_tasks
(
SubTaskID BIGINT UNSIGNED NOT NULL,

Description Text,
Owner INTEGER NOT NULL,

ChildCounter Integer Not NULL, --TODEL? zawiera liczbe niezakonczonych synow tego zadania
Done BIT NOT NULL,
CreatedOn SMALLDATETIME NOT NULL,
LastChange SMALLDATETIME NOT NULL,

PRIMARY KEY (SubTaskID),
FOREIGN KEY (Owner) REFERENCES Users (UserID)
);


CREATE TABLE Tasks
(
-- opisuje drzewo konkretnego zadania 
-- robiac zakonczenie konkretnego podzadania nalezy zakonczyc wszystkich jego synow
-- oraz wziac ojca, zmniejszyc mu ChildCounter, jesli ten spadnie do 0 to zakonczyc
-- dodawanie powiazania oczywiscie musi zwiększać ChildCounter
-- aktualizacja podzadania musi przejsc na sama gore drzewa i zaktualizowac czas zmiany
TaskID BIGINT UNSIGNED NOT NULL,
ChildTaskID BIGINT UNSIGNED NOT NULL,

FOREIGN KEY (TaskID) REFERENCES Sub_tasks (SubTaskID),
FOREIGN KEY (ChildTaskID) REFERENCES Sub_tasks (SubTaskID)
);


CREATE TABLE Have_access
(
TaskID BIGINT UNSIGNED NOT NULL,
UserID INTEGER NOT NULL,
Permissions INTEGER UNNSIGNED NOT NULL, --maska bitowa zawierajaca uprawnienia
-- & 1  - moze zobaczyc
-- & 2  - moze oznaczyc jako zakonczone
-- & 4  - moze zmienic opis
-- & 8  - moze pokazac innym
-- & 16 - moze dac prawo do zakonczenia
-- & 32 - moze dac prawo do zmiany opisu
-- & 64 - moze usunac zadanie

FOREIGN KEY (TaskID) REFERENCES Sub_tasks (SubTaskID),
FOREIGN KEY (Owner) REFERENCES Users (UserID)
);