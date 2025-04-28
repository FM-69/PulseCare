-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: pulsecare_db
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS auth_group;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_group (
  id int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES auth_group WRITE;
/*!40000 ALTER TABLE auth_group DISABLE KEYS */;
/*!40000 ALTER TABLE auth_group ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS auth_group_permissions;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_group_permissions (
  id bigint NOT NULL AUTO_INCREMENT,
  group_id int NOT NULL,
  permission_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY auth_group_permissions_group_id_permission_id_0cd325b0_uniq (group_id,permission_id),
  KEY auth_group_permissio_permission_id_84c5c92e_fk_auth_perm (permission_id),
  CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission (id),
  CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES auth_group_permissions WRITE;
/*!40000 ALTER TABLE auth_group_permissions DISABLE KEYS */;
/*!40000 ALTER TABLE auth_group_permissions ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS auth_permission;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_permission (
  id int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  content_type_id int NOT NULL,
  codename varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY auth_permission_content_type_id_codename_01ab375a_uniq (content_type_id,codename),
  CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type (id)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES auth_permission WRITE;
/*!40000 ALTER TABLE auth_permission DISABLE KEYS */;
INSERT INTO auth_permission VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add medical company',6,'add_medicalcompany'),(22,'Can change medical company',6,'change_medicalcompany'),(23,'Can delete medical company',6,'delete_medicalcompany'),(24,'Can view medical company',6,'view_medicalcompany'),(25,'Can add product',7,'add_product'),(26,'Can change product',7,'change_product'),(27,'Can delete product',7,'delete_product'),(28,'Can view product',7,'view_product'),(29,'Can add specialty',8,'add_specialty'),(30,'Can change specialty',8,'change_specialty'),(31,'Can delete specialty',8,'delete_specialty'),(32,'Can view specialty',8,'view_specialty'),(33,'Can add custom user',9,'add_customuser'),(34,'Can change custom user',9,'change_customuser'),(35,'Can delete custom user',9,'delete_customuser'),(36,'Can view custom user',9,'view_customuser'),(37,'Can add cart',10,'add_cart'),(38,'Can change cart',10,'change_cart'),(39,'Can delete cart',10,'delete_cart'),(40,'Can view cart',10,'view_cart'),(41,'Can add doctor',11,'add_doctor'),(42,'Can change doctor',11,'change_doctor'),(43,'Can delete doctor',11,'delete_doctor'),(44,'Can view doctor',11,'view_doctor'),(45,'Can add appointment',12,'add_appointment'),(46,'Can change appointment',12,'change_appointment'),(47,'Can delete appointment',12,'delete_appointment'),(48,'Can view appointment',12,'view_appointment'),(49,'Can add doctor availability',13,'add_doctoravailability'),(50,'Can change doctor availability',13,'change_doctoravailability'),(51,'Can delete doctor availability',13,'delete_doctoravailability'),(52,'Can view doctor availability',13,'view_doctoravailability'),(53,'Can add doctor schedule',14,'add_doctorschedule'),(54,'Can change doctor schedule',14,'change_doctorschedule'),(55,'Can delete doctor schedule',14,'delete_doctorschedule'),(56,'Can view doctor schedule',14,'view_doctorschedule'),(57,'Can add experience',15,'add_experience'),(58,'Can change experience',15,'change_experience'),(59,'Can delete experience',15,'delete_experience'),(60,'Can view experience',15,'view_experience'),(61,'Can add message request',16,'add_messagerequest'),(62,'Can change message request',16,'change_messagerequest'),(63,'Can delete message request',16,'delete_messagerequest'),(64,'Can view message request',16,'view_messagerequest'),(65,'Can add chat message',17,'add_chatmessage'),(66,'Can change chat message',17,'change_chatmessage'),(67,'Can delete chat message',17,'delete_chatmessage'),(68,'Can view chat message',17,'view_chatmessage'),(69,'Can add order',18,'add_order'),(70,'Can change order',18,'change_order'),(71,'Can delete order',18,'delete_order'),(72,'Can view order',18,'view_order'),(73,'Can add patient',19,'add_patient'),(74,'Can change patient',19,'change_patient'),(75,'Can delete patient',19,'delete_patient'),(76,'Can view patient',19,'view_patient'),(77,'Can add payment',20,'add_payment'),(78,'Can change payment',20,'change_payment'),(79,'Can delete payment',20,'delete_payment'),(80,'Can view payment',20,'view_payment'),(81,'Can add prescription',21,'add_prescription'),(82,'Can change prescription',21,'change_prescription'),(83,'Can delete prescription',21,'delete_prescription'),(84,'Can view prescription',21,'view_prescription'),(85,'Can add order item',22,'add_orderitem'),(86,'Can change order item',22,'change_orderitem'),(87,'Can delete order item',22,'delete_orderitem'),(88,'Can view order item',22,'view_orderitem'),(89,'Can add cart item',23,'add_cartitem'),(90,'Can change cart item',23,'change_cartitem'),(91,'Can delete cart item',23,'delete_cartitem'),(92,'Can view cart item',23,'view_cartitem'),(93,'Can add service provided',24,'add_serviceprovided'),(94,'Can change service provided',24,'change_serviceprovided'),(95,'Can delete service provided',24,'delete_serviceprovided'),(96,'Can view service provided',24,'view_serviceprovided'),(97,'Can add user profile',25,'add_userprofile'),(98,'Can change user profile',25,'change_userprofile'),(99,'Can delete user profile',25,'delete_userprofile'),(100,'Can view user profile',25,'view_userprofile');
/*!40000 ALTER TABLE auth_permission ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_appointment`
--

DROP TABLE IF EXISTS core_appointment;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_appointment (
  id bigint NOT NULL AUTO_INCREMENT,
  appointment_type varchar(20) NOT NULL,
  `date` date NOT NULL,
  `time` time(6) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  consultation_link varchar(255) DEFAULT NULL,
  patient_id bigint NOT NULL,
  doctor_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY core_appointment_patient_id_960b1d60_fk_core_customuser_id (patient_id),
  KEY core_appointment_doctor_id_c3a00eba_fk_core_doctor_id (doctor_id),
  CONSTRAINT core_appointment_doctor_id_c3a00eba_fk_core_doctor_id FOREIGN KEY (doctor_id) REFERENCES core_doctor (id),
  CONSTRAINT core_appointment_patient_id_960b1d60_fk_core_customuser_id FOREIGN KEY (patient_id) REFERENCES core_customuser (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_appointment`
--

LOCK TABLES core_appointment WRITE;
/*!40000 ALTER TABLE core_appointment DISABLE KEYS */;
INSERT INTO core_appointment VALUES (1,'ONLINE','2025-04-29','11:30:00.000000','2025-04-28 15:03:52.541305','2025-04-28 15:03:52.541335',NULL,6,1),(2,'ONLINE','2025-04-29','18:00:00.000000','2025-04-28 15:16:23.431194','2025-04-28 15:16:23.431229',NULL,6,1);
/*!40000 ALTER TABLE core_appointment ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_cart`
--

DROP TABLE IF EXISTS core_cart;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_cart (
  id bigint NOT NULL AUTO_INCREMENT,
  patient_id bigint NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY patient_id (patient_id),
  CONSTRAINT core_cart_patient_id_ee2d1410_fk_core_customuser_id FOREIGN KEY (patient_id) REFERENCES core_customuser (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_cart`
--

LOCK TABLES core_cart WRITE;
/*!40000 ALTER TABLE core_cart DISABLE KEYS */;
INSERT INTO core_cart VALUES (1,6);
/*!40000 ALTER TABLE core_cart ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_cartitem`
--

DROP TABLE IF EXISTS core_cartitem;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_cartitem (
  id bigint NOT NULL AUTO_INCREMENT,
  quantity int unsigned NOT NULL,
  cart_id bigint NOT NULL,
  product_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY core_cartitem_cart_id_5256d769_fk_core_cart_id (cart_id),
  KEY core_cartitem_product_id_2640c4a2_fk_core_product_id (product_id),
  CONSTRAINT core_cartitem_cart_id_5256d769_fk_core_cart_id FOREIGN KEY (cart_id) REFERENCES core_cart (id),
  CONSTRAINT core_cartitem_product_id_2640c4a2_fk_core_product_id FOREIGN KEY (product_id) REFERENCES core_product (id),
  CONSTRAINT core_cartitem_chk_1 CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_cartitem`
--

LOCK TABLES core_cartitem WRITE;
/*!40000 ALTER TABLE core_cartitem DISABLE KEYS */;
/*!40000 ALTER TABLE core_cartitem ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_chatmessage`
--

DROP TABLE IF EXISTS core_chatmessage;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_chatmessage (
  id bigint NOT NULL AUTO_INCREMENT,
  message longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  sender_id bigint NOT NULL,
  message_request_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY core_chatmessage_sender_id_c9992722_fk_core_customuser_id (sender_id),
  KEY core_chatmessage_message_request_id_bebe2e26_fk_core_mess (message_request_id),
  CONSTRAINT core_chatmessage_message_request_id_bebe2e26_fk_core_mess FOREIGN KEY (message_request_id) REFERENCES core_messagerequest (id),
  CONSTRAINT core_chatmessage_sender_id_c9992722_fk_core_customuser_id FOREIGN KEY (sender_id) REFERENCES core_customuser (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_chatmessage`
--

LOCK TABLES core_chatmessage WRITE;
/*!40000 ALTER TABLE core_chatmessage DISABLE KEYS */;
/*!40000 ALTER TABLE core_chatmessage ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_customuser`
--

DROP TABLE IF EXISTS core_customuser;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_customuser (
  id bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  last_login datetime(6) DEFAULT NULL,
  is_superuser tinyint(1) NOT NULL,
  email varchar(254) NOT NULL,
  username varchar(150) NOT NULL,
  is_staff tinyint(1) NOT NULL,
  is_active tinyint(1) NOT NULL,
  date_joined datetime(6) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY email (email),
  UNIQUE KEY username (username)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_customuser`
--

LOCK TABLES core_customuser WRITE;
/*!40000 ALTER TABLE core_customuser DISABLE KEYS */;
INSERT INTO core_customuser VALUES (1,'pbkdf2_sha256$1000000$AJT0mqvOBDaOHuZLymmMwq$yXscLxVk9R6okvZQtV7j6vfwdRXlN/xtaVSh750TuSc=','2025-04-28 14:34:39.475606',1,'admin@gmail.com','admin',1,1,'2025-04-28 14:34:00.129870'),(2,'pbkdf2_sha256$1000000$1784q4e8h6NkweGzIaEAu2$idIbgKdimS60SMHomNziyCSJJxipxFRYdtZxki1ntW8=','2025-04-28 14:53:44.990338',0,'doctor1@gmail.com','dr_rahman',0,1,'2025-04-28 14:47:34.078128'),(3,'pbkdf2_sha256$1000000$6yudyYqXkuadSTlpKZKpZd$Qx4XppUKZ1NTtXG6oscyq3FrIY4RfYM6lytPH48QE+A=',NULL,0,'doctor2@gmail.com','dr_samia',0,1,'2025-04-28 14:48:40.686912'),(4,'pbkdf2_sha256$1000000$aR1cQjIn3BdCBPksvLTSJU$nFn6vL+nlWLd0VZMswL0EJAdwX+07VNyk4bQW+L9pB8=',NULL,0,'doctor3@gmail.com','dr_tanvir',0,1,'2025-04-28 14:49:40.079694'),(5,'pbkdf2_sha256$1000000$OZMqYlEr7Xn95hmOr0uwOw$xtNBfbauavGgzwggFuEUpn6kSBq3+vUUWhzUbmT6/So=',NULL,0,'doctor4@gmail.com','dr_sharmin',0,1,'2025-04-28 14:50:34.108388'),(6,'pbkdf2_sha256$1000000$nrURMiWyI0RiukcpD1L73y$nX6Iyyud2g/G0qwDPFfrbGq+CIORlHj4ZvZ9fknW9xQ=','2025-04-28 14:56:45.701897',0,'patient1@gmail.com','patient_rahim',0,1,'2025-04-28 14:51:58.855159'),(7,'pbkdf2_sha256$1000000$9NfJep0TpJBbj7icLzJiiE$s/kliE4XbzZ4ZGMbblQhvzf/Ihss3XFEYhuiHM1OFII=','2025-04-28 14:53:08.032917',0,'patient2@gmail.com','patient_salma',0,1,'2025-04-28 14:52:57.952266');
/*!40000 ALTER TABLE core_customuser ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_customuser_groups`
--

DROP TABLE IF EXISTS core_customuser_groups;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_customuser_groups (
  id bigint NOT NULL AUTO_INCREMENT,
  customuser_id bigint NOT NULL,
  group_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY core_customuser_groups_customuser_id_group_id_7990e9c6_uniq (customuser_id,group_id),
  KEY core_customuser_groups_group_id_301aeff4_fk_auth_group_id (group_id),
  CONSTRAINT core_customuser_grou_customuser_id_976bc4d7_fk_core_cust FOREIGN KEY (customuser_id) REFERENCES core_customuser (id),
  CONSTRAINT core_customuser_groups_group_id_301aeff4_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_customuser_groups`
--

LOCK TABLES core_customuser_groups WRITE;
/*!40000 ALTER TABLE core_customuser_groups DISABLE KEYS */;
/*!40000 ALTER TABLE core_customuser_groups ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_customuser_user_permissions`
--

DROP TABLE IF EXISTS core_customuser_user_permissions;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_customuser_user_permissions (
  id bigint NOT NULL AUTO_INCREMENT,
  customuser_id bigint NOT NULL,
  permission_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY core_customuser_user_per_customuser_id_permission_49ea742a_uniq (customuser_id,permission_id),
  KEY core_customuser_user_permission_id_80ceaab9_fk_auth_perm (permission_id),
  CONSTRAINT core_customuser_user_customuser_id_ebd2ce6c_fk_core_cust FOREIGN KEY (customuser_id) REFERENCES core_customuser (id),
  CONSTRAINT core_customuser_user_permission_id_80ceaab9_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_customuser_user_permissions`
--

LOCK TABLES core_customuser_user_permissions WRITE;
/*!40000 ALTER TABLE core_customuser_user_permissions DISABLE KEYS */;
/*!40000 ALTER TABLE core_customuser_user_permissions ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_doctor`
--

DROP TABLE IF EXISTS core_doctor;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_doctor (
  id bigint NOT NULL AUTO_INCREMENT,
  email varchar(254) NOT NULL,
  username varchar(150) DEFAULT NULL,
  designation varchar(100) NOT NULL,
  full_name varchar(255) NOT NULL,
  `number` varchar(20) DEFAULT NULL,
  address longtext,
  details longtext NOT NULL,
  photo varchar(100) NOT NULL,
  qualification varchar(255) NOT NULL,
  consultation_fee double NOT NULL,
  certificate_url varchar(200) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  user_id bigint NOT NULL,
  specialty_id bigint NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY email (email),
  UNIQUE KEY user_id (user_id),
  UNIQUE KEY username (username),
  KEY core_doctor_specialty_id_d17e3ebe_fk_core_specialty_id (specialty_id),
  CONSTRAINT core_doctor_specialty_id_d17e3ebe_fk_core_specialty_id FOREIGN KEY (specialty_id) REFERENCES core_specialty (id),
  CONSTRAINT core_doctor_user_id_e7476eac_fk_core_customuser_id FOREIGN KEY (user_id) REFERENCES core_customuser (id)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_doctor`
--

LOCK TABLES core_doctor WRITE;
/*!40000 ALTER TABLE core_doctor DISABLE KEYS */;
INSERT INTO core_doctor VALUES (1,'doctor1@gmail.com','dr_rahman','Senior Consultant','Arif Rahman',NULL,'','15 years of experience in treating common and chronic diseases','myimage/doctor-thumb-01_eOb0l28.jpg','MBBS, FCPS (Medicine)',20,'http://127.0.0.1:8000/doctors/edit-profile/','2025-04-28 14:47:35.278283','2025-04-28 14:56:24.068145',2,11),(2,'doctor2@gmail.com','dr_samia','Consultant','Dr. Samia Islam',NULL,NULL,'Specialist in urinary tract diseases and male reproductive health.','myimage/blank.png','MBBS, MS (Urology)',100,'','2025-04-28 14:48:41.856672','2025-04-28 14:48:41.856730',3,12),(3,'doctor3@gmail.com','dr_tanvir','Associate Professor','Tanvir Hasan',NULL,NULL,'Expert in kidney diseases and dialysis management.','myimage/blank.png','MBBS, MD (Nephrology)',1200,'','2025-04-28 14:49:41.267837','2025-04-28 14:49:41.267874',4,13),(4,'doctor4@gmail.com','dr_sharmin','Consultant','Sharmin Akter',NULL,NULL,'Specialist in cataract surgery and eye care treatments.','myimage/blank.png','MBBS, DO (Diploma in Ophthalmology)',100,'','2025-04-28 14:50:35.278423','2025-04-28 14:50:35.278465',5,14);
/*!40000 ALTER TABLE core_doctor ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_doctoravailability`
--

DROP TABLE IF EXISTS core_doctoravailability;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_doctoravailability (
  id bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  start_time time(6) NOT NULL,
  end_time time(6) NOT NULL,
  appointment_type varchar(20) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  doctor_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY core_doctoravailability_doctor_id_b9babf20_fk_core_doctor_id (doctor_id),
  CONSTRAINT core_doctoravailability_doctor_id_b9babf20_fk_core_doctor_id FOREIGN KEY (doctor_id) REFERENCES core_doctor (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_doctoravailability`
--

LOCK TABLES core_doctoravailability WRITE;
/*!40000 ALTER TABLE core_doctoravailability DISABLE KEYS */;
INSERT INTO core_doctoravailability VALUES (1,'2025-04-29','10:00:00.000000','18:30:00.000000','ONLINE','2025-04-28 14:55:12.790274','2025-04-28 14:55:12.790306',1);
/*!40000 ALTER TABLE core_doctoravailability ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_doctorschedule`
--

DROP TABLE IF EXISTS core_doctorschedule;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_doctorschedule (
  id bigint NOT NULL AUTO_INCREMENT,
  day_of_week varchar(10) NOT NULL,
  start_time time(6) NOT NULL,
  end_time time(6) NOT NULL,
  notes longtext,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  doctor_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY core_doctorschedule_doctor_id_b60b51ff_fk_core_doctor_id (doctor_id),
  CONSTRAINT core_doctorschedule_doctor_id_b60b51ff_fk_core_doctor_id FOREIGN KEY (doctor_id) REFERENCES core_doctor (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_doctorschedule`
--

LOCK TABLES core_doctorschedule WRITE;
/*!40000 ALTER TABLE core_doctorschedule DISABLE KEYS */;
INSERT INTO core_doctorschedule VALUES (1,'MONDAY','09:56:00.000000','14:01:00.000000','','2025-04-28 14:55:42.650183','2025-04-28 14:55:42.650210',1);
/*!40000 ALTER TABLE core_doctorschedule ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_experience`
--

DROP TABLE IF EXISTS core_experience;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_experience (
  id bigint NOT NULL AUTO_INCREMENT,
  designation varchar(100) NOT NULL,
  department varchar(100) NOT NULL,
  employment_status varchar(20) NOT NULL,
  start_date date NOT NULL,
  end_date date DEFAULT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  doctor_id bigint NOT NULL,
  medical_company_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY core_experience_doctor_id_8dcedfdf_fk_core_doctor_id (doctor_id),
  KEY core_experience_medical_company_id_5bc017ea_fk_core_medi (medical_company_id),
  CONSTRAINT core_experience_doctor_id_8dcedfdf_fk_core_doctor_id FOREIGN KEY (doctor_id) REFERENCES core_doctor (id),
  CONSTRAINT core_experience_medical_company_id_5bc017ea_fk_core_medi FOREIGN KEY (medical_company_id) REFERENCES core_medicalcompany (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_experience`
--

LOCK TABLES core_experience WRITE;
/*!40000 ALTER TABLE core_experience DISABLE KEYS */;
/*!40000 ALTER TABLE core_experience ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_medicalcompany`
--

DROP TABLE IF EXISTS core_medicalcompany;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_medicalcompany (
  id bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_medicalcompany`
--

LOCK TABLES core_medicalcompany WRITE;
/*!40000 ALTER TABLE core_medicalcompany DISABLE KEYS */;
INSERT INTO core_medicalcompany VALUES (1,'Square Pharmaceuticals Ltd.','2025-04-28 14:35:21.169002','2025-04-28 14:35:21.169050'),(2,'Beximco Pharmaceuticals Ltd.','2025-04-28 14:35:26.643396','2025-04-28 14:35:26.643434'),(3,'Incepta Pharmaceuticals Ltd.','2025-04-28 14:35:32.805588','2025-04-28 14:35:32.805623'),(4,'Renata Limited','2025-04-28 14:35:36.629252','2025-04-28 14:35:36.629397'),(5,'ACI Limited (Advanced Chemical Industries)','2025-04-28 14:35:41.439464','2025-04-28 14:35:41.439497'),(6,'GlaxoSmithKline (GSK)','2025-04-28 14:35:46.502800','2025-04-28 14:35:46.502831'),(7,'AstraZeneca','2025-04-28 14:35:50.036887','2025-04-28 14:35:50.036923'),(8,'Smith & Nephew','2025-04-28 14:35:55.313920','2025-04-28 14:35:55.313956'),(9,'Hikma Pharmaceuticals (UK Branch)','2025-04-28 14:35:59.904376','2025-04-28 14:35:59.904424'),(10,'Alliance Pharma plc','2025-04-28 14:36:04.493936','2025-04-28 14:36:04.493989');
/*!40000 ALTER TABLE core_medicalcompany ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_messagerequest`
--

DROP TABLE IF EXISTS core_messagerequest;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_messagerequest (
  id bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) NOT NULL,
  created_at datetime(6) NOT NULL,
  doctor_id bigint NOT NULL,
  patient_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY core_messagerequest_doctor_id_70a6bbb0_fk_core_doctor_id (doctor_id),
  KEY core_messagerequest_patient_id_576d88d6_fk_core_customuser_id (patient_id),
  CONSTRAINT core_messagerequest_doctor_id_70a6bbb0_fk_core_doctor_id FOREIGN KEY (doctor_id) REFERENCES core_doctor (id),
  CONSTRAINT core_messagerequest_patient_id_576d88d6_fk_core_customuser_id FOREIGN KEY (patient_id) REFERENCES core_customuser (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_messagerequest`
--

LOCK TABLES core_messagerequest WRITE;
/*!40000 ALTER TABLE core_messagerequest DISABLE KEYS */;
INSERT INTO core_messagerequest VALUES (1,'PENDING','2025-04-28 15:04:03.636865',1,6);
/*!40000 ALTER TABLE core_messagerequest ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_order`
--

DROP TABLE IF EXISTS core_order;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_order (
  id bigint NOT NULL AUTO_INCREMENT,
  total_amount decimal(10,2) NOT NULL,
  payment_method varchar(50) NOT NULL,
  payment_date datetime(6) NOT NULL,
  delivery_date date NOT NULL,
  `status` varchar(20) NOT NULL,
  patient_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY core_order_patient_id_29675ab7_fk_core_customuser_id (patient_id),
  CONSTRAINT core_order_patient_id_29675ab7_fk_core_customuser_id FOREIGN KEY (patient_id) REFERENCES core_customuser (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_order`
--

LOCK TABLES core_order WRITE;
/*!40000 ALTER TABLE core_order DISABLE KEYS */;
INSERT INTO core_order VALUES (1,25.00,'PayPal','2025-04-28 15:16:02.473539','2025-05-01','PENDING',6);
/*!40000 ALTER TABLE core_order ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_orderitem`
--

DROP TABLE IF EXISTS core_orderitem;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_orderitem (
  id bigint NOT NULL AUTO_INCREMENT,
  quantity int unsigned NOT NULL,
  price decimal(10,2) NOT NULL,
  order_id bigint NOT NULL,
  product_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY core_orderitem_order_id_30929c10_fk_core_order_id (order_id),
  KEY core_orderitem_product_id_0c2047cd_fk_core_product_id (product_id),
  CONSTRAINT core_orderitem_order_id_30929c10_fk_core_order_id FOREIGN KEY (order_id) REFERENCES core_order (id),
  CONSTRAINT core_orderitem_product_id_0c2047cd_fk_core_product_id FOREIGN KEY (product_id) REFERENCES core_product (id),
  CONSTRAINT core_orderitem_chk_1 CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_orderitem`
--

LOCK TABLES core_orderitem WRITE;
/*!40000 ALTER TABLE core_orderitem DISABLE KEYS */;
INSERT INTO core_orderitem VALUES (1,1,25.00,1,2);
/*!40000 ALTER TABLE core_orderitem ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_patient`
--

DROP TABLE IF EXISTS core_patient;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_patient (
  id bigint NOT NULL AUTO_INCREMENT,
  email varchar(254) NOT NULL,
  username varchar(150) DEFAULT NULL,
  full_name varchar(255) NOT NULL,
  `number` varchar(20) DEFAULT NULL,
  gender varchar(10) NOT NULL,
  dob date NOT NULL,
  address longtext,
  photo varchar(100) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  user_id bigint NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY email (email),
  UNIQUE KEY user_id (user_id),
  UNIQUE KEY username (username),
  CONSTRAINT core_patient_user_id_96d54e7e_fk_core_customuser_id FOREIGN KEY (user_id) REFERENCES core_customuser (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_patient`
--

LOCK TABLES core_patient WRITE;
/*!40000 ALTER TABLE core_patient DISABLE KEYS */;
INSERT INTO core_patient VALUES (1,'patient1@gmail.com','patient_rahim','Md. Rahim Uddin','01710001111','MALE','1999-05-14','12/A, Dhanmondi, Dhaka','myimage/blank.png','2025-04-28 14:52:00.080545','2025-04-28 14:52:00.080581',6),(2,'patient2@gmail.com','patient_salma','Salma Khatun','01811002233','FEMALE','1994-06-16','34, North Badda, Dhaka','myimage/blank.png','2025-04-28 14:52:59.152681','2025-04-28 14:52:59.152720',7);
/*!40000 ALTER TABLE core_patient ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_payment`
--

DROP TABLE IF EXISTS core_payment;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_payment (
  id bigint NOT NULL AUTO_INCREMENT,
  amount decimal(10,2) NOT NULL,
  payment_method varchar(50) NOT NULL,
  payment_date datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  appointment_id bigint NOT NULL,
  patient_id bigint NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY appointment_id (appointment_id),
  KEY core_payment_patient_id_379302b3_fk_core_customuser_id (patient_id),
  CONSTRAINT core_payment_appointment_id_4b8c4994_fk_core_appointment_id FOREIGN KEY (appointment_id) REFERENCES core_appointment (id),
  CONSTRAINT core_payment_patient_id_379302b3_fk_core_customuser_id FOREIGN KEY (patient_id) REFERENCES core_customuser (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_payment`
--

LOCK TABLES core_payment WRITE;
/*!40000 ALTER TABLE core_payment DISABLE KEYS */;
INSERT INTO core_payment VALUES (1,100.00,'credit_card','2025-04-28 15:03:52.549303','SUCCESS',1,6),(2,100.00,'mobile_banking','2025-04-28 15:16:23.439835','SUCCESS',2,6);
/*!40000 ALTER TABLE core_payment ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_prescription`
--

DROP TABLE IF EXISTS core_prescription;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_prescription (
  id bigint NOT NULL AUTO_INCREMENT,
  prescription_text longtext NOT NULL,
  recommended_tests longtext,
  created_at datetime(6) NOT NULL,
  appointment_id bigint NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY appointment_id (appointment_id),
  CONSTRAINT core_prescription_appointment_id_61c87719_fk_core_appointment_id FOREIGN KEY (appointment_id) REFERENCES core_appointment (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_prescription`
--

LOCK TABLES core_prescription WRITE;
/*!40000 ALTER TABLE core_prescription DISABLE KEYS */;
/*!40000 ALTER TABLE core_prescription ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_product`
--

DROP TABLE IF EXISTS core_product;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_product (
  id bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  category varchar(20) NOT NULL,
  price decimal(10,2) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_product`
--

LOCK TABLES core_product WRITE;
/*!40000 ALTER TABLE core_product DISABLE KEYS */;
INSERT INTO core_product VALUES (1,'24 Hours Urinary Cortisol','LAB_TEST',65.00,'Measures cortisol levels in a 24-hour urine sample to evaluate adrenal gland function and diagnose conditions like Cushing’s syndrome or Addison’s disease.'),(2,'Complete Blood Count (CBC)','LAB_TEST',25.00,'Evaluates overall health and detects a wide range of disorders, including anemia, infection, and leukemia.'),(3,'Lipid Profile','LAB_TEST',35.00,'Measures cholesterol and triglyceride levels to assess cardiovascular risk.'),(4,'Liver Function Test (LFT)','LAB_TEST',45.00,'Checks for liver damage or disease by measuring the levels of enzymes, proteins, and bilirubin in your blood.'),(5,'Kidney Function Test (KFT)','LAB_TEST',40.00,'Evaluates kidney performance by analyzing creatinine, urea, and other indicators in the blood.'),(6,'Thyroid Profile (T3, T4, TSH)','LAB_TEST',50.00,'Assesses thyroid gland function and helps diagnose hypothyroidism or hyperthyroidism.'),(7,'Vitamin D Test','LAB_TEST',55.00,'Determines vitamin D levels to help detect deficiencies linked to bone health and immune function.'),(8,'Fasting Blood Sugar (FBS)','LAB_TEST',20.00,'Measures blood glucose after fasting to screen for diabetes or prediabetes.'),(9,'Hemoglobin A1c (HbA1c)','LAB_TEST',30.00,'Reflects average blood sugar levels over the past 2–3 months, used in diabetes monitoring.'),(10,'Prostate-Specific Antigen (PSA) Test','LAB_TEST',60.00,'Screens for prostate gland issues, including prostate cancer and benign prostatic hyperplasia.'),(11,'Paracetamol 500mg Tablets','MEDICINE',5.00,'Common pain reliever and fever reducer used for headaches, muscle aches, arthritis, and colds.'),(12,'Amoxicillin 500mg Capsules','MEDICINE',12.00,'Broad-spectrum antibiotic used to treat bacterial infections such as pneumonia, bronchitis, and ENT infections.'),(13,'Cetirizine 10mg Tablets','MEDICINE',6.00,'Antihistamine used to relieve allergy symptoms like runny nose, sneezing, and itchy eyes.'),(14,'Omeprazole 20mg Capsules','MEDICINE',10.00,'Proton pump inhibitor used to reduce stomach acid, treat ulcers, and manage GERD symptoms.'),(15,'Metformin 500mg Tablets','MEDICINE',15.00,'Oral diabetes medication used to control blood sugar levels in people with type 2 diabetes.'),(16,'Ibuprofen 400mg Tablets','MEDICINE',8.00,'Non-steroidal anti-inflammatory drug (NSAID) used to relieve pain, inflammation, and fever.'),(17,'Losartan 50mg Tablets','MEDICINE',18.00,'Used to treat high blood pressure and help protect the kidneys from damage due to diabetes.'),(18,'Salbutamol Inhaler (100 mcg/dose)','MEDICINE',22.00,'Fast-acting bronchodilator used to relieve symptoms of asthma and other breathing disorders.'),(19,'Atorvastatin 20mg Tablets','MEDICINE',25.00,'Statin used to lower cholesterol and reduce the risk of heart disease and stroke.'),(20,'Lorazepam 1mg Tablets','MEDICINE',30.00,'Benzodiazepine used to treat anxiety disorders, insomnia, and seizures.'),(21,'Complete Blood Count (CBC)','LAB_TEST',10.00,'A routine blood test that evaluates overall health by measuring red blood cells, white blood cells, hemoglobin, hematocrit, and platelets.'),(22,'Serum Creatinine','MEDICINE',4.00,'Tests the level of creatinine in the blood to evaluate kidney function.'),(23,'Thyroid Stimulating Hormone (TSH)','LAB_TEST',8.00,'Measures TSH levels to screen for thyroid gland problems like hypothyroidism or hyperthyroidism.');
/*!40000 ALTER TABLE core_product ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_serviceprovided`
--

DROP TABLE IF EXISTS core_serviceprovided;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_serviceprovided (
  id bigint NOT NULL AUTO_INCREMENT,
  appointment_type varchar(20) NOT NULL,
  `date` date NOT NULL,
  `time` time(6) NOT NULL,
  prescription_text longtext NOT NULL,
  recommended_tests longtext,
  consultation_link varchar(255) DEFAULT NULL,
  rating int DEFAULT NULL,
  review longtext,
  completed_at datetime(6) NOT NULL,
  doctor_id bigint NOT NULL,
  patient_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY core_serviceprovided_doctor_id_ddcb45bc_fk_core_doctor_id (doctor_id),
  KEY core_serviceprovided_patient_id_5143f573_fk_core_customuser_id (patient_id),
  CONSTRAINT core_serviceprovided_doctor_id_ddcb45bc_fk_core_doctor_id FOREIGN KEY (doctor_id) REFERENCES core_doctor (id),
  CONSTRAINT core_serviceprovided_patient_id_5143f573_fk_core_customuser_id FOREIGN KEY (patient_id) REFERENCES core_customuser (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_serviceprovided`
--

LOCK TABLES core_serviceprovided WRITE;
/*!40000 ALTER TABLE core_serviceprovided DISABLE KEYS */;
/*!40000 ALTER TABLE core_serviceprovided ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_specialty`
--

DROP TABLE IF EXISTS core_specialty;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_specialty (
  id bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  slug varchar(150) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY slug (slug)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_specialty`
--

LOCK TABLES core_specialty WRITE;
/*!40000 ALTER TABLE core_specialty DISABLE KEYS */;
INSERT INTO core_specialty VALUES (1,'Cardiologist','cardiologist','2025-04-28 14:36:18.859264','2025-04-28 14:36:18.859311'),(2,'Dermatologist','dermatologist','2025-04-28 14:36:24.511042','2025-04-28 14:36:24.511085'),(3,'Neurologist','neurologist','2025-04-28 14:36:28.941976','2025-04-28 14:36:28.942015'),(4,'Pediatrician','pediatrician','2025-04-28 14:36:35.399101','2025-04-28 14:36:35.399158'),(5,'Orthopedic Surgeon','orthopedic-surgeon','2025-04-28 14:36:39.955573','2025-04-28 14:36:39.955610'),(6,'Endocrinologist','endocrinologist','2025-04-28 14:36:44.013974','2025-04-28 14:36:44.014031'),(7,'Gastroenterologist','gastroenterologist','2025-04-28 14:36:48.472916','2025-04-28 14:36:48.472951'),(8,'Psychiatrist','psychiatrist','2025-04-28 14:36:53.145505','2025-04-28 14:36:53.145555'),(9,'Obstetrician/Gynecologist (OB/GYN)','obstetriciangynecologist-obgyn','2025-04-28 14:36:58.741376','2025-04-28 14:36:58.741415'),(10,'Pulmonologist','pulmonologist','2025-04-28 14:37:03.420370','2025-04-28 14:37:03.420421'),(11,'General Physician','general-physician','2025-04-28 14:44:54.398338','2025-04-28 14:44:54.398375'),(12,'Urologist','urologist','2025-04-28 14:44:59.826305','2025-04-28 14:44:59.826343'),(13,'Nephrologist','nephrologist','2025-04-28 14:45:03.413316','2025-04-28 14:45:03.413361'),(14,'Ophthalmologist','ophthalmologist','2025-04-28 14:45:06.668905','2025-04-28 14:45:06.668941'),(15,'Oncologist','oncologist','2025-04-28 14:45:10.723850','2025-04-28 14:45:10.723897'),(16,'ENT Specialist (Otolaryngologist)','ent-specialist-otolaryngologist','2025-04-28 14:45:16.196955','2025-04-28 14:45:16.196991'),(17,'Rheumatologist','rheumatologist','2025-04-28 14:45:19.939072','2025-04-28 14:45:19.939105'),(18,'Hematologist','hematologist','2025-04-28 14:45:23.557999','2025-04-28 14:45:23.558034'),(19,'Anesthesiologist','anesthesiologist','2025-04-28 14:45:27.359742','2025-04-28 14:45:27.359786'),(20,'Radiologist','radiologist','2025-04-28 14:45:30.734677','2025-04-28 14:45:30.734732');
/*!40000 ALTER TABLE core_specialty ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_userprofile`
--

DROP TABLE IF EXISTS core_userprofile;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE core_userprofile (
  id bigint NOT NULL AUTO_INCREMENT,
  `role` varchar(20) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  user_id bigint NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY user_id (user_id),
  CONSTRAINT core_userprofile_user_id_5141ad90_fk_core_customuser_id FOREIGN KEY (user_id) REFERENCES core_customuser (id)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_userprofile`
--

LOCK TABLES core_userprofile WRITE;
/*!40000 ALTER TABLE core_userprofile DISABLE KEYS */;
INSERT INTO core_userprofile VALUES (1,'DOCTOR','2025-04-28 14:47:35.272869','2025-04-28 14:47:35.272909',2),(2,'DOCTOR','2025-04-28 14:48:41.847078','2025-04-28 14:48:41.847115',3),(3,'DOCTOR','2025-04-28 14:49:41.263512','2025-04-28 14:49:41.263549',4),(4,'DOCTOR','2025-04-28 14:50:35.273889','2025-04-28 14:50:35.273930',5),(5,'PATIENT','2025-04-28 14:52:00.075386','2025-04-28 14:52:00.075420',6),(6,'PATIENT','2025-04-28 14:52:59.143619','2025-04-28 14:52:59.143683',7);
/*!40000 ALTER TABLE core_userprofile ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS django_admin_log;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_admin_log (
  id int NOT NULL AUTO_INCREMENT,
  action_time datetime(6) NOT NULL,
  object_id longtext,
  object_repr varchar(200) NOT NULL,
  action_flag smallint unsigned NOT NULL,
  change_message longtext NOT NULL,
  content_type_id int DEFAULT NULL,
  user_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY django_admin_log_content_type_id_c4bce8eb_fk_django_co (content_type_id),
  KEY django_admin_log_user_id_c564eba6_fk_core_customuser_id (user_id),
  CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type (id),
  CONSTRAINT django_admin_log_user_id_c564eba6_fk_core_customuser_id FOREIGN KEY (user_id) REFERENCES core_customuser (id),
  CONSTRAINT django_admin_log_chk_1 CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES django_admin_log WRITE;
/*!40000 ALTER TABLE django_admin_log DISABLE KEYS */;
INSERT INTO django_admin_log VALUES (1,'2025-04-28 14:35:21.175133','1','Square Pharmaceuticals Ltd.',1,'[{\"added\": {}}]',6,1),(2,'2025-04-28 14:35:26.644986','2','Beximco Pharmaceuticals Ltd.',1,'[{\"added\": {}}]',6,1),(3,'2025-04-28 14:35:32.807158','3','Incepta Pharmaceuticals Ltd.',1,'[{\"added\": {}}]',6,1),(4,'2025-04-28 14:35:36.631921','4','Renata Limited',1,'[{\"added\": {}}]',6,1),(5,'2025-04-28 14:35:41.441310','5','ACI Limited (Advanced Chemical Industries)',1,'[{\"added\": {}}]',6,1),(6,'2025-04-28 14:35:46.504745','6','GlaxoSmithKline (GSK)',1,'[{\"added\": {}}]',6,1),(7,'2025-04-28 14:35:50.038420','7','AstraZeneca',1,'[{\"added\": {}}]',6,1),(8,'2025-04-28 14:35:55.316017','8','Smith & Nephew',1,'[{\"added\": {}}]',6,1),(9,'2025-04-28 14:35:59.906300','9','Hikma Pharmaceuticals (UK Branch)',1,'[{\"added\": {}}]',6,1),(10,'2025-04-28 14:36:04.496054','10','Alliance Pharma plc',1,'[{\"added\": {}}]',6,1),(11,'2025-04-28 14:36:18.860807','1','Cardiologist',1,'[{\"added\": {}}]',8,1),(12,'2025-04-28 14:36:24.512606','2','Dermatologist',1,'[{\"added\": {}}]',8,1),(13,'2025-04-28 14:36:28.943183','3','Neurologist',1,'[{\"added\": {}}]',8,1),(14,'2025-04-28 14:36:35.401168','4','Pediatrician',1,'[{\"added\": {}}]',8,1),(15,'2025-04-28 14:36:39.957230','5','Orthopedic Surgeon',1,'[{\"added\": {}}]',8,1),(16,'2025-04-28 14:36:44.016163','6','Endocrinologist',1,'[{\"added\": {}}]',8,1),(17,'2025-04-28 14:36:48.474030','7','Gastroenterologist',1,'[{\"added\": {}}]',8,1),(18,'2025-04-28 14:36:53.146705','8','Psychiatrist',1,'[{\"added\": {}}]',8,1),(19,'2025-04-28 14:36:58.743132','9','Obstetrician/Gynecologist (OB/GYN)',1,'[{\"added\": {}}]',8,1),(20,'2025-04-28 14:37:03.422443','10','Pulmonologist',1,'[{\"added\": {}}]',8,1),(21,'2025-04-28 14:37:50.322747','1','24 Hours Urinary Cortisol (LAB_TEST)',1,'[{\"added\": {}}]',7,1),(22,'2025-04-28 14:38:11.055298','2','Complete Blood Count (CBC) (LAB_TEST)',1,'[{\"added\": {}}]',7,1),(23,'2025-04-28 14:38:24.092986','3','Lipid Profile (LAB_TEST)',1,'[{\"added\": {}}]',7,1),(24,'2025-04-28 14:38:37.088001','4','Liver Function Test (LFT) (LAB_TEST)',1,'[{\"added\": {}}]',7,1),(25,'2025-04-28 14:38:52.172326','5','Kidney Function Test (KFT) (LAB_TEST)',1,'[{\"added\": {}}]',7,1),(26,'2025-04-28 14:39:08.421373','6','Thyroid Profile (T3, T4, TSH) (LAB_TEST)',1,'[{\"added\": {}}]',7,1),(27,'2025-04-28 14:39:27.596419','7','Vitamin D Test (LAB_TEST)',1,'[{\"added\": {}}]',7,1),(28,'2025-04-28 14:39:40.611848','8','Fasting Blood Sugar (FBS) (LAB_TEST)',1,'[{\"added\": {}}]',7,1),(29,'2025-04-28 14:39:53.790109','9','Hemoglobin A1c (HbA1c) (LAB_TEST)',1,'[{\"added\": {}}]',7,1),(30,'2025-04-28 14:40:08.371827','10','Prostate-Specific Antigen (PSA) Test (LAB_TEST)',1,'[{\"added\": {}}]',7,1),(31,'2025-04-28 14:40:35.352999','11','Paracetamol 500mg Tablets (MEDICINE)',1,'[{\"added\": {}}]',7,1),(32,'2025-04-28 14:40:47.879651','12','Amoxicillin 500mg Capsules (MEDICINE)',1,'[{\"added\": {}}]',7,1),(33,'2025-04-28 14:41:01.422746','13','Cetirizine 10mg Tablets (MEDICINE)',1,'[{\"added\": {}}]',7,1),(34,'2025-04-28 14:41:16.587092','14','Omeprazole 20mg Capsules (MEDICINE)',1,'[{\"added\": {}}]',7,1),(35,'2025-04-28 14:41:31.924367','15','Metformin 500mg Tablets (MEDICINE)',1,'[{\"added\": {}}]',7,1),(36,'2025-04-28 14:41:46.800723','16','Ibuprofen 400mg Tablets (MEDICINE)',1,'[{\"added\": {}}]',7,1),(37,'2025-04-28 14:41:59.985225','17','Losartan 50mg Tablets (MEDICINE)',1,'[{\"added\": {}}]',7,1),(38,'2025-04-28 14:42:13.721772','18','Salbutamol Inhaler (100 mcg/dose) (MEDICINE)',1,'[{\"added\": {}}]',7,1),(39,'2025-04-28 14:42:28.448208','19','Atorvastatin 20mg Tablets (MEDICINE)',1,'[{\"added\": {}}]',7,1),(40,'2025-04-28 14:42:46.468121','20','Lorazepam 1mg Tablets (MEDICINE)',1,'[{\"added\": {}}]',7,1),(41,'2025-04-28 14:43:26.126546','21','Complete Blood Count (CBC) (LAB_TEST)',1,'[{\"added\": {}}]',7,1),(42,'2025-04-28 14:43:56.239619','22','Serum Creatinine (MEDICINE)',1,'[{\"added\": {}}]',7,1),(43,'2025-04-28 14:44:10.045572','23','Thyroid Stimulating Hormone (TSH) (LAB_TEST)',1,'[{\"added\": {}}]',7,1),(44,'2025-04-28 14:44:54.399234','11','General Physician',1,'[{\"added\": {}}]',8,1),(45,'2025-04-28 14:44:59.827744','12','Urologist',1,'[{\"added\": {}}]',8,1),(46,'2025-04-28 14:45:03.414923','13','Nephrologist',1,'[{\"added\": {}}]',8,1),(47,'2025-04-28 14:45:06.670044','14','Ophthalmologist',1,'[{\"added\": {}}]',8,1),(48,'2025-04-28 14:45:10.725590','15','Oncologist',1,'[{\"added\": {}}]',8,1),(49,'2025-04-28 14:45:16.198174','16','ENT Specialist (Otolaryngologist)',1,'[{\"added\": {}}]',8,1),(50,'2025-04-28 14:45:19.940362','17','Rheumatologist',1,'[{\"added\": {}}]',8,1),(51,'2025-04-28 14:45:23.559004','18','Hematologist',1,'[{\"added\": {}}]',8,1),(52,'2025-04-28 14:45:27.360951','19','Anesthesiologist',1,'[{\"added\": {}}]',8,1),(53,'2025-04-28 14:45:30.736316','20','Radiologist',1,'[{\"added\": {}}]',8,1);
/*!40000 ALTER TABLE django_admin_log ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS django_content_type;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_content_type (
  id int NOT NULL AUTO_INCREMENT,
  app_label varchar(100) NOT NULL,
  model varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY django_content_type_app_label_model_76bd3d3b_uniq (app_label,model)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES django_content_type WRITE;
/*!40000 ALTER TABLE django_content_type DISABLE KEYS */;
INSERT INTO django_content_type VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(12,'core','appointment'),(10,'core','cart'),(23,'core','cartitem'),(17,'core','chatmessage'),(9,'core','customuser'),(11,'core','doctor'),(13,'core','doctoravailability'),(14,'core','doctorschedule'),(15,'core','experience'),(6,'core','medicalcompany'),(16,'core','messagerequest'),(18,'core','order'),(22,'core','orderitem'),(19,'core','patient'),(20,'core','payment'),(21,'core','prescription'),(7,'core','product'),(24,'core','serviceprovided'),(8,'core','specialty'),(25,'core','userprofile'),(5,'sessions','session');
/*!40000 ALTER TABLE django_content_type ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS django_migrations;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_migrations (
  id bigint NOT NULL AUTO_INCREMENT,
  app varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  applied datetime(6) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES django_migrations WRITE;
/*!40000 ALTER TABLE django_migrations DISABLE KEYS */;
INSERT INTO django_migrations VALUES (1,'contenttypes','0001_initial','2025-04-28 14:33:31.466370'),(2,'contenttypes','0002_remove_content_type_name','2025-04-28 14:33:31.633697'),(3,'auth','0001_initial','2025-04-28 14:33:32.159028'),(4,'auth','0002_alter_permission_name_max_length','2025-04-28 14:33:32.324049'),(5,'auth','0003_alter_user_email_max_length','2025-04-28 14:33:32.336268'),(6,'auth','0004_alter_user_username_opts','2025-04-28 14:33:32.352451'),(7,'auth','0005_alter_user_last_login_null','2025-04-28 14:33:32.374257'),(8,'auth','0006_require_contenttypes_0002','2025-04-28 14:33:32.379405'),(9,'auth','0007_alter_validators_add_error_messages','2025-04-28 14:33:32.392262'),(10,'auth','0008_alter_user_username_max_length','2025-04-28 14:33:32.403943'),(11,'auth','0009_alter_user_last_name_max_length','2025-04-28 14:33:32.418722'),(12,'auth','0010_alter_group_name_max_length','2025-04-28 14:33:32.459510'),(13,'auth','0011_update_proxy_permissions','2025-04-28 14:33:32.475226'),(14,'auth','0012_alter_user_first_name_max_length','2025-04-28 14:33:32.485677'),(15,'core','0001_initial','2025-04-28 14:33:36.245896'),(16,'admin','0001_initial','2025-04-28 14:33:36.489911'),(17,'admin','0002_logentry_remove_auto_add','2025-04-28 14:33:36.510647'),(18,'admin','0003_logentry_add_action_flag_choices','2025-04-28 14:33:36.549461'),(19,'sessions','0001_initial','2025-04-28 14:33:36.619306');
/*!40000 ALTER TABLE django_migrations ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS django_session;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_session (
  session_key varchar(40) NOT NULL,
  session_data longtext NOT NULL,
  expire_date datetime(6) NOT NULL,
  PRIMARY KEY (session_key),
  KEY django_session_expire_date_a5c62663 (expire_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES django_session WRITE;
/*!40000 ALTER TABLE django_session DISABLE KEYS */;
INSERT INTO django_session VALUES ('hbxkpzgqttmt1lftnrlfvvebj4hm76yt','.eJxVjEEOwiAQRe_C2hCgwFCX7j0DGZipVA0kpV0Z765NutDtf-_9l4i4rSVunZc4kzgLL06_W8L84LoDumO9NZlbXZc5yV2RB-3y2oifl8P9OyjYy7c2bIgTJPaKQHPQPqDVJtgMzmYKCHmE0eXJMJNSk3EMgwqDCwZQEYr3B-3SN90:1u9PuX:L8nOxkbeGP3tlnrqhD_l7sYmWgqa0RKfEJVu3tGhOf0','2025-05-12 14:56:45.710117');
/*!40000 ALTER TABLE django_session ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-28 21:24:13
