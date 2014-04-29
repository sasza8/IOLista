CREATE SCHEMA `list` CHARACTER SET utf8 COLLATE utf8_general_ci;
GRANT ALL ON `list`.* TO `username`@localhost IDENTIFIED BY 'password';
FLUSH PRIVILEGES;

CREATE TABLE `list`.`users` (
  `UserID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `Login` VARCHAR(100) NOT NULL,
  `Password` VARCHAR(100) NOT NULL,
  `Salt` VARCHAR(100) NOT NULL,
  `Email` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE INDEX `UserID_UNIQUE` (`UserID` ASC),
  UNIQUE INDEX `Login_UNIQUE` (`Login` ASC),
  UNIQUE INDEX `Email_UNIQUE` (`Email` ASC));

CREATE TABLE `list`.`tasks` (
  `TaskID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(100) NOT NULL,
  `Description` TEXT NULL,
  `Owner` INT UNSIGNED NOT NULL,
  `ParentID` BIGINT UNSIGNED NULL,
  `Done` INT UNSIGNED NOT NULL,
  `CreatedAt` DATETIME NOT NULL,
  `LastChange` DATETIME NOT NULL,
  PRIMARY KEY (`TaskID`),
  UNIQUE INDEX `TaskID_UNIQUE` (`TaskID` ASC),
  INDEX `user_idx` (`Owner` ASC),
  CONSTRAINT `user`
    FOREIGN KEY (`Owner`)
    REFERENCES `list`.`users` (`UserID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `list`.`have_access` (
  `TaskID` BIGINT UNSIGNED NOT NULL,
  `UserID` INT UNSIGNED NOT NULL,
  `CanSee` INT UNSIGNED NOT NULL,
  `CanEdit` INT UNSIGNED NOT NULL,
  INDEX `Task_idx` (`TaskID` ASC),
  INDEX `User_idx` (`UserID` ASC),
  CONSTRAINT `access_task`
    FOREIGN KEY (`TaskID`)
    REFERENCES `list`.`tasks` (`TaskID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `access_user`
    FOREIGN KEY (`UserID`)
    REFERENCES `list`.`users` (`UserID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);