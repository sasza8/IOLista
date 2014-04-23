CREATE SCHEMA `list` CHARACTER SET utf8 COLLATE utf8_general_ci;
GRANT ALL ON `list`.* TO `username`@localhost IDENTIFIED BY 'password';
FLUSH PRIVILEGES;


CREATE TABLE `list`.`users` (
  `UserID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `Login` VARCHAR(100) NOT NULL,
  `Password` VARCHAR(100) NOT NULL,
  `Salt` VARCHAR(100) NOT NULL,
  `FirstName` VARCHAR(100) NOT NULL,
  `LastName` VARCHAR(150) NOT NULL,
  `Email` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE INDEX `UserID_UNIQUE` (`UserID` ASC),
  UNIQUE INDEX `Login_UNIQUE` (`Login` ASC),
  UNIQUE INDEX `Email_UNIQUE` (`Email` ASC));


CREATE TABLE `list`.`tasks` (
  `TaskID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `Description` TEXT NOT NULL,
  `Owner` INT UNSIGNED NOT NULL,
  `ParentID` BIGINT UNSIGNED NULL COMMENT 'wskazuje na nadrzednego Taska',
  `Parents` TEXT NULL COMMENT 'string zawierajacy liste id ojcow',
  `Done` BIT NOT NULL COMMENT '0 - trwa' /* comment truncated */ /*1 - zakonczone*/,
  `CreatedOn` DATETIME NOT NULL,
  `LastChange` DATETIME NOT NULL,
  PRIMARY KEY (`TaskID`),
  UNIQUE INDEX `TaskID_UNIQUE` (`TaskID` ASC),
  INDEX `Owner_idx` (`Owner` ASC),
  CONSTRAINT `Owner`
    FOREIGN KEY (`Owner`)
    REFERENCES `list`.`users` (`UserID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
COMMENT = 'opisuje drzewo konkretnego zadania ' /* comment truncated */ /*robiac zakonczenie konkretnego podzadania nalezy zakonczyc wszystkich jego synow
oraz wziac ojca, zmniejszyc mu ChildCounter, jesli ten spadnie do 0 to zakonczyc
dodawanie powiazania oczywiscie musi zwiększać ChildCounter
aktualizacja podzadania musi przejsc na sama gore drzewa i zaktualizowac czas zmiany*/;


CREATE TABLE `list`.`have_access` (
  `TaskID` BIGINT UNSIGNED NOT NULL,
  `UserID` INT UNSIGNED NOT NULL,
  `Permissions` INT UNSIGNED NOT NULL COMMENT 'Maska bitowa',
  INDEX `Task_idx` (`TaskID` ASC),
  INDEX `User_idx` (`UserID` ASC),
  CONSTRAINT `Task`
    FOREIGN KEY (`TaskID`)
    REFERENCES `list`.`tasks` (`TaskID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `User`
    FOREIGN KEY (`UserID`)
    REFERENCES `list`.`users` (`UserID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


