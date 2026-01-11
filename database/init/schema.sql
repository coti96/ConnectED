CREATE TABLE `users` (
  `user_id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` datetime,
  `updated_at` datetime,
  `email` varchar(255) UNIQUE NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `auth_provider` varchar(255),
  `role` ENUM('etudiant','professionnel','encadrant')
);
CREATE TABLE `domains` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` datetime,
  `updated_at` datetime,
  `libelle` varchar(255)
);

CREATE TABLE `profiles` (
  `profile_id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` datetime,
  `updated_at` datetime,
  `user_id` int,
  `nom` varchar(255),
  `prenom` varchar(255),
  `ville` varchar(255),
  `bio_courte` text,
  `domain_id` int
);

CREATE TABLE `technologies` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` datetime,
  `updated_at` datetime,
  `libelle` varchar(255),
  `domain_id` int
);

CREATE TABLE `profile_techno` (
  `profile_id` int,
  `id_techno` int
);

CREATE TABLE `projects` (
  `project_id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` datetime,
  `updated_at` datetime,
  `titre` varchar(255),
  `description` text,
  `localisation` varchar(255),
  `statut` ENUM('pas_commence','en_cours','termine','annule'),
  `nombre_places` int,
  `deadline` datetime,
  `creator_id` int,
  `domain_id` int
);

CREATE TABLE `project_techno` (
  `id_project` int,
  `id_techno` int
);

CREATE TABLE `notifications` (
  `notification_id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` datetime,
  `updated_at` datetime,
  `user_id` int,
  `message` text,
  `date_sent` datetime,
  `project_id` int
);

CREATE TABLE `project_applications` (
  `application_id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` datetime,
  `updated_at` datetime,
  `project_id` int,
  `user_id` int,
  `motivation_message` text,
  `status` ENUM('en_attente','acceptee','refusee')
);

CREATE TABLE `project_members` (
  `member_id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` datetime,
  `updated_at` datetime,
  `project_id` int,
  `user_id` int,
  `joined_at` datetime
);

CREATE TABLE `profiles_student` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` datetime,
  `updated_at` datetime,
  `ecole` varchar(255),
  `filiere` varchar(255),
  `profile_id` int UNIQUE
);

CREATE TABLE `profiles_pro` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` datetime,
  `updated_at` datetime,
  `fonction` varchar(255),
  `entreprise` varchar(255),
  `profile_id` int UNIQUE
);

CREATE UNIQUE INDEX `profile_techno_index_0` ON `profile_techno` (`profile_id`, `id_techno`);

CREATE UNIQUE INDEX `project_techno_index_1` ON `project_techno` (`id_project`, `id_techno`);

CREATE UNIQUE INDEX `project_applications_index_2` ON `project_applications` (`project_id`, `user_id`);

CREATE UNIQUE INDEX `project_members_index_3` ON `project_members` (`project_id`, `user_id`);

ALTER TABLE `profiles` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `profiles` ADD FOREIGN KEY (`domain_id`) REFERENCES `domains` (`id`);

ALTER TABLE `technologies` ADD FOREIGN KEY (`domain_id`) REFERENCES `domains` (`id`);

ALTER TABLE `profile_techno` ADD FOREIGN KEY (`profile_id`) REFERENCES `profiles` (`profile_id`);

ALTER TABLE `profile_techno` ADD FOREIGN KEY (`id_techno`) REFERENCES `technologies` (`id`);

ALTER TABLE `projects` ADD FOREIGN KEY (`creator_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `projects` ADD FOREIGN KEY (`domain_id`) REFERENCES `domains` (`id`);

ALTER TABLE `project_techno` ADD FOREIGN KEY (`id_project`) REFERENCES `projects` (`project_id`);

ALTER TABLE `project_techno` ADD FOREIGN KEY (`id_techno`) REFERENCES `technologies` (`id`);

ALTER TABLE `notifications` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `notifications` ADD FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`);

ALTER TABLE `project_applications` ADD FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`);

ALTER TABLE `project_applications` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `project_members` ADD FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`);

ALTER TABLE `project_members` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `profiles_student` ADD FOREIGN KEY (`profile_id`) REFERENCES `profiles` (`profile_id`);

ALTER TABLE `profiles_pro` ADD FOREIGN KEY (`profile_id`) REFERENCES `profiles` (`profile_id`);

