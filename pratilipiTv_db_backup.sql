-- MySQL dump 10.13  Distrib 9.3.0, for macos15.4 (arm64)
--
-- Host: localhost    Database: pratilipiTv_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_user`
--

DROP TABLE IF EXISTS `app_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `mobile_number` varchar(15) NOT NULL,
  `password` varchar(128) NOT NULL,
  `terms_accepted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `mobile_number` (`mobile_number`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_user`
--

LOCK TABLES `app_user` WRITE;
/*!40000 ALTER TABLE `app_user` DISABLE KEYS */;
INSERT INTO `app_user` VALUES (1,'John Doe','john.doe@example.com','+919876543210','pbkdf2_sha256$1000000$k8rUiwV1J95jPNe2evL5Iw$yrESVyktUrRvvy9aGu29FDEPyB9jzmU01n1OR3EZAtc=',1),(2,'Jane Smith','jane.smith@example.com','+919123456789','pbkdf2_sha256$1000000$gTCl4uQr9fNgEuJgl4cebl$b04Lcnw2gji2Om5rmxugIdzzNboC7Hn2+BdXAr5w+14=',1),(3,'tarun dah','tarun@gmail.com','+919406702568','pbkdf2_sha256$1000000$LW3hW7EjVPca0dOukJbmtd$l/8DYW+SadUUJDaD3mgZJrkFUACPu0eFU69Bx5k4Vrg=',1),(4,'dada ji','dada@gmail.com','+919876543222','pbkdf2_sha256$1000000$by1MkAblFteG6Hzy0XuECY$DkeR4sOfx4flGBuuS8tVMwgk3xjbgLNf+eY7U77oB50=',1),(5,'vaishali daba','vaishali@gmail.com','9406702560','pbkdf2_sha256$1000000$DKy7C0chsmSiWeyJKQQbna$iMNxzyif4pOt+irVzNwbSTJLdBh8bEAhCo8Ambrp+vE=',1),(6,'suhagan bai','suhagan@gmail.com','+919090909090','pbkdf2_sha256$1000000$jWfvdD3QkBR8ZhGwsb81vd$FTj0ZyN1hD7rQFbCpDs5YUgc4IDBREz4+diLM8/uT+A=',1),(7,'Alice Brown','alice.brown@example.com','9234567890','pbkdf2_sha256$1000000$McvoePJWnR0HDH5JeelgWp$omMQdRfWsdkCDBhN3hSGu4D/zRK9IZWKQ1JxI9QeeT4=',1),(8,'vijay rao','vijay@gmail.com','9293949596','pbkdf2_sha256$1000000$sSh0r6hJORiIi4Ig6HQoN0$ZAyyhWoPMZnI6uNTC8rv55m4GNIrPm0S0v0W1Xr2h+M=',1),(9,'chitrarekha bai','bai@gmail.com','9897969594','pbkdf2_sha256$1000000$ggF1tuxkT62H3rcFIRD5XV$yvWYkpvlPeHGwJ6CqKAwTkYFTYFcKm5ZnOWxa9IrfPo=',1);
/*!40000 ALTER TABLE `app_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add App User',7,'add_appuser'),(26,'Can change App User',7,'change_appuser'),(27,'Can delete App User',7,'delete_appuser'),(28,'Can view App User',7,'view_appuser'),(29,'Can add episode',8,'add_episode'),(30,'Can change episode',8,'change_episode'),(31,'Can delete episode',8,'delete_episode'),(32,'Can view episode',8,'view_episode'),(33,'Can add page',9,'add_page'),(34,'Can change page',9,'change_page'),(35,'Can delete page',9,'delete_page'),(36,'Can view page',9,'view_page'),(37,'Can add social data',10,'add_socialdata'),(38,'Can change social data',10,'change_socialdata'),(39,'Can delete social data',10,'delete_socialdata'),(40,'Can view social data',10,'view_socialdata'),(41,'Can add comic',11,'add_comic'),(42,'Can change comic',11,'change_comic'),(43,'Can delete comic',11,'delete_comic'),(44,'Can view comic',11,'view_comic'),(45,'Can add Comic Uploader',12,'add_classiccomic'),(46,'Can change Comic Uploader',12,'change_classiccomic'),(47,'Can delete Comic Uploader',12,'delete_classiccomic'),(48,'Can view Comic Uploader',12,'view_classiccomic'),(49,'Can add Motion Comic Uploader',13,'add_moderncomic'),(50,'Can change Motion Comic Uploader',13,'change_moderncomic'),(51,'Can delete Motion Comic Uploader',13,'delete_moderncomic'),(52,'Can view Motion Comic Uploader',13,'view_moderncomic');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$ugq0vuPDGYYKojOdz48lg8$u62eTnfCoyOPw6dbTDyc90RVFOO9gIoe8M3vxO79QYk=','2025-06-12 05:53:54.523040',1,'admin','','','admin@gmail.com',1,1,'2025-06-12 05:53:40.910106');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-06-12 06:59:43.730614','1','test@example.com ()',1,'[{\"added\": {}}]',7,1),(2,'2025-06-12 07:06:10.647050','2','test2@example.com (test456)',1,'[{\"added\": {}}]',7,1),(3,'2025-06-12 07:08:47.131662','1','test@example.com ()',3,'',7,1),(4,'2025-06-12 07:09:12.982916','3','testuser@example.com (test123)',1,'[{\"added\": {}}]',7,1),(5,'2025-06-13 13:08:53.993153','1','ClassicComic object (1)',1,'[{\"added\": {}}, {\"added\": {\"name\": \"episode\", \"object\": \"Episode object (1)\"}}]',12,1),(6,'2025-06-13 13:12:07.469193','2','ModernComic object (2)',1,'[{\"added\": {}}, {\"added\": {\"name\": \"episode\", \"object\": \"Episode object (2)\"}}]',13,1),(7,'2025-06-13 14:17:37.175735','1','ClassicComic object (1)',1,'[{\"added\": {}}, {\"added\": {\"name\": \"episode\", \"object\": \"Episode object (1)\"}}]',12,1),(8,'2025-06-13 14:19:15.718241','2','ModernComic object (2)',1,'[{\"added\": {}}, {\"added\": {\"name\": \"episode\", \"object\": \"Episode object (2)\"}}]',13,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(7,'cms','appuser'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(12,'uploader','classiccomic'),(11,'uploader','comic'),(8,'uploader','episode'),(13,'uploader','moderncomic'),(9,'uploader','page'),(10,'uploader','socialdata');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-06-12 05:52:44.304011'),(2,'auth','0001_initial','2025-06-12 05:52:44.360379'),(3,'admin','0001_initial','2025-06-12 05:52:44.377454'),(4,'admin','0002_logentry_remove_auto_add','2025-06-12 05:52:44.379146'),(5,'admin','0003_logentry_add_action_flag_choices','2025-06-12 05:52:44.380861'),(6,'contenttypes','0002_remove_content_type_name','2025-06-12 05:52:44.390147'),(7,'auth','0002_alter_permission_name_max_length','2025-06-12 05:52:44.397100'),(8,'auth','0003_alter_user_email_max_length','2025-06-12 05:52:44.401858'),(9,'auth','0004_alter_user_username_opts','2025-06-12 05:52:44.403533'),(10,'auth','0005_alter_user_last_login_null','2025-06-12 05:52:44.409078'),(11,'auth','0006_require_contenttypes_0002','2025-06-12 05:52:44.409290'),(12,'auth','0007_alter_validators_add_error_messages','2025-06-12 05:52:44.410921'),(13,'auth','0008_alter_user_username_max_length','2025-06-12 05:52:44.418061'),(14,'auth','0009_alter_user_last_name_max_length','2025-06-12 05:52:44.424407'),(15,'auth','0010_alter_group_name_max_length','2025-06-12 05:52:44.427825'),(16,'auth','0011_update_proxy_permissions','2025-06-12 05:52:44.429334'),(17,'auth','0012_alter_user_first_name_max_length','2025-06-12 05:52:44.437196'),(18,'sessions','0001_initial','2025-06-12 05:52:44.440294'),(21,'cms','0001_initial','2025-06-12 08:54:05.166162'),(23,'uploader','0001_initial','2025-06-13 14:14:30.134675');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('dd9kka9qicqt5rn3scbmu07xfhh9cq90','.eJxVjMEOwiAQRP-FsyEsYAGP3v0GsrCLVA1NSnsy_rtt0oPeJvPezFtEXJca185zHElcBIjTb5cwP7ntgB7Y7pPMU1vmMcldkQft8jYRv66H-3dQsddtbYwmxSHpAipbXwaTMBgPwKjRIlLxyGT0WQ2wxRScdaxLIeBiwRnx-QLtFThT:1uPass:chDAB-0YnLLrkAs1WVP_J08j1RKFXHiDfeMCuAJ0V4Q','2025-06-26 05:53:54.524203');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uploader_comic`
--

DROP TABLE IF EXISTS `uploader_comic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uploader_comic` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `image_url` varchar(500) NOT NULL,
  `pdf_file` varchar(100) DEFAULT NULL,
  `video_file` varchar(100) DEFAULT NULL,
  `genre` varchar(100) NOT NULL,
  `category` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `uploader_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `uploader_comic_uploader_id_e73badf8_fk_auth_user_id` (`uploader_id`),
  CONSTRAINT `uploader_comic_uploader_id_e73badf8_fk_auth_user_id` FOREIGN KEY (`uploader_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uploader_comic`
--

LOCK TABLES `uploader_comic` WRITE;
/*!40000 ALTER TABLE `uploader_comic` DISABLE KEYS */;
INSERT INTO `uploader_comic` VALUES (1,'Test Classic Comic','hhhssnddf ffkfkkf fkfkkf kdkdk','https://example.com/cover.png','comics/pdfs/HVU_JvcZJmA.pdf','','Superhero','Classic','2025-06-13 14:17:37.173951',1),(2,'Test Modern Comic','description=\"A romantic story\"','https://example.com/thumbnail.jpg','','comics/videos/0f4415cd-8553-47df-8b63-db1a90f48e68.mp4','Fantasy','Modern','2025-06-13 14:19:15.716620',1);
/*!40000 ALTER TABLE `uploader_comic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uploader_episode`
--

DROP TABLE IF EXISTS `uploader_episode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uploader_episode` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `is_free` tinyint(1) NOT NULL,
  `is_unlocked` tinyint(1) NOT NULL,
  `comic_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `uploader_episode_comic_id_ff7b9f90_fk_uploader_comic_id` (`comic_id`),
  CONSTRAINT `uploader_episode_comic_id_ff7b9f90_fk_uploader_comic_id` FOREIGN KEY (`comic_id`) REFERENCES `uploader_comic` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uploader_episode`
--

LOCK TABLES `uploader_episode` WRITE;
/*!40000 ALTER TABLE `uploader_episode` DISABLE KEYS */;
INSERT INTO `uploader_episode` VALUES (1,'episode 1',1,1,1),(2,'episode 1',1,1,2);
/*!40000 ALTER TABLE `uploader_episode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uploader_page`
--

DROP TABLE IF EXISTS `uploader_page`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uploader_page` (
  `id` int NOT NULL AUTO_INCREMENT,
  `image_url` varchar(500) NOT NULL,
  `text` longtext NOT NULL,
  `episode_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `uploader_page_episode_id_a90aaef6_fk_uploader_episode_id` (`episode_id`),
  CONSTRAINT `uploader_page_episode_id_a90aaef6_fk_uploader_episode_id` FOREIGN KEY (`episode_id`) REFERENCES `uploader_episode` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uploader_page`
--

LOCK TABLES `uploader_page` WRITE;
/*!40000 ALTER TABLE `uploader_page` DISABLE KEYS */;
/*!40000 ALTER TABLE `uploader_page` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uploader_social_data`
--

DROP TABLE IF EXISTS `uploader_social_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uploader_social_data` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_liked` tinyint(1) NOT NULL,
  `like_count` int NOT NULL,
  `tags` json NOT NULL,
  `comments` json NOT NULL,
  `comic_id` int NOT NULL,
  `episode_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `uploader_social_data_comic_id_64be17e1_fk_uploader_comic_id` (`comic_id`),
  KEY `uploader_social_data_episode_id_608e11e8_fk_uploader_episode_id` (`episode_id`),
  KEY `uploader_social_data_user_id_faa28e6f_fk_app_user_id` (`user_id`),
  CONSTRAINT `uploader_social_data_comic_id_64be17e1_fk_uploader_comic_id` FOREIGN KEY (`comic_id`) REFERENCES `uploader_comic` (`id`),
  CONSTRAINT `uploader_social_data_episode_id_608e11e8_fk_uploader_episode_id` FOREIGN KEY (`episode_id`) REFERENCES `uploader_episode` (`id`),
  CONSTRAINT `uploader_social_data_user_id_faa28e6f_fk_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `app_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uploader_social_data`
--

LOCK TABLES `uploader_social_data` WRITE;
/*!40000 ALTER TABLE `uploader_social_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `uploader_social_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-14 10:51:50
