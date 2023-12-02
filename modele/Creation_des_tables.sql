SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : iot
--

-- --------------------------------------------------------

--
-- Structure de la table alerte
--

DROP TABLE IF EXISTS alerte;
CREATE TABLE alerte (
  idAlerte int NOT NULL,
  Niv double DEFAULT NULL,
  Operateur varchar(2) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  Type varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  Active tinyint DEFAULT NULL,
  Utilisateur_idUtilisateur int NOT NULL,
  frequence_envoi_mail varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  dernier_envoi datetime DEFAULT NULL,
  Sonde_idSonde varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table releve
--

DROP TABLE IF EXISTS releve;
CREATE TABLE releve (
  idReleve int NOT NULL,
  Date_releve datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table sonde
--

DROP TABLE IF EXISTS sonde;
CREATE TABLE sonde (
  idSonde varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  Nom varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  Active tinyint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table sonde
--

INSERT INTO sonde (idSonde, Nom, Active) VALUES
('06190485', 'Salon', 1),
('62182233', 'Cour', 1),
('62190434', 'Jardin', 1);

-- --------------------------------------------------------

--
-- Structure de la table sonde_has_releve
--

DROP TABLE IF EXISTS sonde_has_releve;
CREATE TABLE sonde_has_releve (
  Sonde_idSonde varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  Releve_idReleve int NOT NULL,
  Temperature double DEFAULT NULL,
  Humidite varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  Niveau_batterie double DEFAULT NULL,
  Signal_RSSI int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table utilisateur
--

DROP TABLE IF EXISTS utilisateur;
CREATE TABLE utilisateur (
  idUtilisateur int NOT NULL,
  Prenom varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  Nom varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  Numero_telephone varchar(13) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  Email varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  Identifiant varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  Mot_de_passe varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  account_API varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  mdp_appli varchar(48) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table utilisateur
--

INSERT INTO utilisateur (idUtilisateur, Prenom, Nom, Numero_telephone, Email, Identifiant, Mot_de_passe, account_API, mdp_appli) VALUES
(1, 'Jack', 'THIEM', 'jackthiem311@gmail.com', NULL, NULL, NULL, '16L1SPQZS3', NULL);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table alerte
--
ALTER TABLE alerte
  ADD PRIMARY KEY (idAlerte),
  ADD UNIQUE KEY idAlerte_UNIQUE (idAlerte),
  ADD KEY fk_Alerte_Utilisateur1_idx (Utilisateur_idUtilisateur),
  ADD KEY fk_Alerte_Sonde1_idx (Sonde_idSonde);

--
-- Index pour la table releve
--
ALTER TABLE releve
  ADD PRIMARY KEY (idReleve),
  ADD UNIQUE KEY idRelevé_UNIQUE (idReleve);

--
-- Index pour la table sonde
--
ALTER TABLE sonde
  ADD PRIMARY KEY (idSonde),
  ADD UNIQUE KEY idSonde_UNIQUE (idSonde);

--
-- Index pour la table sonde_has_releve
--
ALTER TABLE sonde_has_releve
  ADD PRIMARY KEY (Sonde_idSonde,Releve_idReleve),
  ADD KEY fk_Sonde_has_Releve_Releve1_idx (Releve_idReleve),
  ADD KEY fk_Sonde_has_Releve_Sonde1_idx (Sonde_idSonde);

--
-- Index pour la table utilisateur
--
ALTER TABLE utilisateur
  ADD PRIMARY KEY (idUtilisateur),
  ADD UNIQUE KEY idUtilisateur_UNIQUE (idUtilisateur);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table alerte
--
ALTER TABLE alerte
  MODIFY idAlerte int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table utilisateur
--
ALTER TABLE utilisateur
  MODIFY idUtilisateur int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table alerte
--
ALTER TABLE alerte
  ADD CONSTRAINT fk_Alerte_Sonde1 FOREIGN KEY (Sonde_idSonde) REFERENCES sonde (idSonde),
  ADD CONSTRAINT fk_Alerte_Utilisateur1 FOREIGN KEY (Utilisateur_idUtilisateur) REFERENCES utilisateur (idUtilisateur);

--
-- Contraintes pour la table sonde_has_releve
--
ALTER TABLE sonde_has_releve
  ADD CONSTRAINT fk_Sonde_has_Releve_Releve1 FOREIGN KEY (Releve_idReleve) REFERENCES releve (idReleve),
  ADD CONSTRAINT fk_Sonde_has_Releve_Sonde1 FOREIGN KEY (Sonde_idSonde) REFERENCES sonde (idSonde);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
