CREATE TABLE List_node
(
ID BIGINT UNSIGNED NOT NULL,
Val BIGINT NOT NULL,
NextNd BIGINT UNSIGNED,

PRIMARY KEY (ID),
FOREIGN KEY (NextNd) REFERENCES List_node (ID)
);

CREATE TABLE List
(
ID BIGINT UNSIGNED NOT NULL,
ListFirst BIGINT UNSIGNED,
ListLast BIGINT UNSIGNED,

PRIMARY KEY (ID),
FOREIGN KEY (ListFirst) REFERENCES List_node (ID),
FOREIGN KEY (ListLast) REFERENCES List_node (ID)
)


CREATE TABLE Users
(
UserID INTEGER NOT NULL,
Login VARCHAR(100),
Password VARCHAR(100),
Salt VARCHAR(100),

FirstName VARCHAR(100),
LastName VARCHAR(150),
Email VARCHAR(100),

PRIMARY KEY (UserID)
);


CREATE TABLE Tasks
(
-- opisuje drzewo konkretnego zadania 
-- robiac zakonczenie konkretnego podzadania nalezy zakonczyc wszystkich jego synow
-- oraz wziac ojca, zmniejszyc mu ChildCounter, jesli ten spadnie do 0 to zakonczyc
-- dodawanie powiazania oczywiscie musi zwiększać ChildCounter
-- aktualizacja podzadania musi przejsc na sama gore drzewa i zaktualizowac czas zmiany
TaskID BIGINT UNSIGNED NOT NULL,

Description TEXT,
Owner INTEGER NOT NULL,

AncListID INTEGER NOT NULL, --pierwszy jest najstaszy przodek

ChildCounter Integer Not NULL, --TODEL? zawiera liczbe niezakonczonych synow tego zadania
Done BIT NOT NULL,
CreatedOn SMALLDATETIME NOT NULL,
LastChange SMALLDATETIME NOT NULL,

PRIMARY KEY (TaskID),
FOREIGN KEY (Owner) REFERENCES Users (UserID),
FOREIGN KEY (AncListID) REFERENCES List (ID)
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