-- MySQL Script generated by MySQL Workbench
-- Fri Oct 27 19:28:22 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema IOT
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema IOT
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `IOT` DEFAULT CHARACTER SET utf8 ;
USE `IOT` ;

-- -----------------------------------------------------
-- Table `IOT`.`Utilisateur`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `IOT`.`Utilisateur` (
  `idUtilisateur` INT NOT NULL AUTO_INCREMENT,
  `Prénom` VARCHAR(45) NULL,
  `Nom` VARCHAR(45) NULL,
  `Numero_telephone` VARCHAR(13) NULL,
  `Email` VARCHAR(60) NULL,
  `Identifiant` VARCHAR(45) NULL,
  `Mot_de_passe` VARCHAR(45) NULL,
  PRIMARY KEY (`idUtilisateur`),
  UNIQUE INDEX `idUtilisateur_UNIQUE` (`idUtilisateur` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `IOT`.`Sonde`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `IOT`.`Sonde` (
  `idSonde` VARCHAR(8) NOT NULL,
  `Nom` VARCHAR(45) NULL,
  `Inactif` TINYINT NOT NULL,
  PRIMARY KEY (`idSonde`),
  UNIQUE INDEX `idSonde_UNIQUE` (`idSonde` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `IOT`.`Releve`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `IOT`.`Releve` (
  `idReleve` INT NOT NULL,
  `Date_releve` DATETIME NULL,
  PRIMARY KEY (`idReleve`),
  UNIQUE INDEX `idRelevé_UNIQUE` (`idReleve` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `IOT`.`Sonde_has_Releve`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `IOT`.`Sonde_has_Releve` (
  `Sonde_idSonde` VARCHAR(8) NOT NULL,
  `Releve_idReleve` INT NOT NULL,
  `Temperature` DOUBLE NULL,
  `Humidite` VARCHAR(5) NULL,
  `Niveau_batterie` DOUBLE NULL,
  `Signal_RSSI` INT NULL,
  PRIMARY KEY (`Sonde_idSonde`, `Releve_idReleve`),
  INDEX `fk_Sonde_has_Releve_Releve1_idx` (`Releve_idReleve` ASC) VISIBLE,
  INDEX `fk_Sonde_has_Releve_Sonde1_idx` (`Sonde_idSonde` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `IOT`.`Alerte`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `IOT`.`Alerte` (
  `idAlerte` INT NOT NULL AUTO_INCREMENT,
  `Niv` DOUBLE NULL,
  `Operateur` VARCHAR(2) NULL,
  `Type` VARCHAR(45) NULL,
  `Actif` TINYINT NULL,
  `Utilisateur_idUtilisateur` INT NOT NULL,
  `frequence_envoi_mail` VARCHAR(45) NULL,
  `Sonde_has_Releve_Sonde_idSonde` VARCHAR(8) NOT NULL,
  `Sonde_has_Releve_Releve_idReleve` INT NOT NULL,
  PRIMARY KEY (`idAlerte`),
  UNIQUE INDEX `idAlerte_UNIQUE` (`idAlerte` ASC) VISIBLE,
  INDEX `fk_Alerte_Utilisateur1_idx` (`Utilisateur_idUtilisateur` ASC) VISIBLE,
  INDEX `fk_Alerte_Sonde_has_Releve1_idx` (`Sonde_has_Releve_Sonde_idSonde` ASC, `Sonde_has_Releve_Releve_idReleve` ASC) VISIBLE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
