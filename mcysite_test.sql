-- MySQL dump 10.13  Distrib 5.6.30, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: mcysite_test
-- ------------------------------------------------------
-- Server version	5.6.30-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Iserlab_delivery`
--

DROP TABLE IF EXISTS `Iserlab_delivery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_delivery` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delivery_time` datetime(6) NOT NULL,
  `exp_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `start_time` date DEFAULT NULL,
  `stop_time` date DEFAULT NULL,
  `desc` longtext,
  `name` varchar(100) NOT NULL,
  `average_score` decimal(5,2),
  `average_time` varchar(100),
  `doing_count` int(11) NOT NULL,
  `done_count` int(11) NOT NULL,
  `total_stu` int(11) NOT NULL,
  `undo_count` int(11) NOT NULL,
  `update_time` datetime(6),
  PRIMARY KEY (`id`),
  KEY `Iserlab_delivery_6a8b84a6` (`exp_id`),
  KEY `Iserlab_delivery_60f3008a` (`group_id`),
  KEY `Iserlab_delivery_4304cd8f` (`teacher_id`),
  CONSTRAINT `Iserlab_delivery_exp_id_a1a16b06_fk_Iserlab_experiment_id` FOREIGN KEY (`exp_id`) REFERENCES `Iserlab_experiment` (`id`),
  CONSTRAINT `Iserlab_delivery_group_id_708ffd81_fk_Iserlab_group_id` FOREIGN KEY (`group_id`) REFERENCES `Iserlab_group` (`id`),
  CONSTRAINT `Iserlab_delivery_teacher_id_4612e266_fk_Iserlab_user_id` FOREIGN KEY (`teacher_id`) REFERENCES `Iserlab_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_delivery`
--

LOCK TABLES `Iserlab_delivery` WRITE;
/*!40000 ALTER TABLE `Iserlab_delivery` DISABLE KEYS */;
INSERT INTO `Iserlab_delivery` VALUES (6,'2017-03-02 08:10:12.026886',24,4,11,'2017-03-02','2017-03-06','erwersdfsdf909090','delivery_record1',NULL,'',0,0,0,0,'2017-03-08 09:17:07.476391'),(20,'2017-03-08 08:41:49.652501',24,17,11,'2017-03-08','2017-03-08','Replace with your description','trtrtrtrtrt3',NULL,'',0,0,2,0,'2017-03-08 09:37:16.248890'),(21,'2017-03-09 07:10:50.761297',24,13,11,'2017-01-01','2017-01-01','Replace with your description','32sdfsdfsdf',NULL,NULL,0,0,2,0,'2017-03-09 07:10:50.761328'),(22,'2017-03-09 07:16:32.276418',26,4,11,'2017-01-01','2017-01-14','Replace with your description','323sdsdsdsd',NULL,NULL,0,0,6,0,'2017-03-09 07:16:32.276481');
/*!40000 ALTER TABLE `Iserlab_delivery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_experiment`
--

DROP TABLE IF EXISTS `Iserlab_experiment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_experiment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exp_name` varchar(150) NOT NULL,
  `exp_description` longtext NOT NULL,
  `exp_createtime` datetime(6) NOT NULL,
  `exp_updatetime` datetime(6) NOT NULL,
  `exp_guide` longtext,
  `exp_result` varchar(500) DEFAULT NULL,
  `exp_reportDIR` varchar(150) DEFAULT NULL,
  `exp_owner_id` int(11) NOT NULL,
  `exp_image_count` int(11),
  `is_shared` tinyint(1) NOT NULL,
  `shared_time` datetime(6),
  PRIMARY KEY (`id`),
  KEY `Iserlab_experiment_c4e139bc` (`exp_owner_id`),
  CONSTRAINT `Iserlab_experiment_exp_owner_id_a2a1aa7e_fk_Iserlab_user_id` FOREIGN KEY (`exp_owner_id`) REFERENCES `Iserlab_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_experiment`
--

LOCK TABLES `Iserlab_experiment` WRITE;
/*!40000 ALTER TABLE `Iserlab_experiment` DISABLE KEYS */;
INSERT INTO `Iserlab_experiment` VALUES (1,'exptest1','this is a test exp contains 2 cirros','2016-12-27 04:25:56.265496','2016-12-27 08:08:11.003189','hello','you can ping each other between these two hosts','',1,2,0,NULL),(2,'exp000','contains one image','2016-12-27 05:45:22.171723','2016-12-27 05:45:22.171784','','','',1,1,0,NULL),(4,'copy of exptest1','this is a test exp contains 2 cirros','2016-12-28 09:51:40.827806','2016-12-28 09:51:40.827844','hello','you can ping each other between these two hosts','',2,2,0,'2016-12-28 09:51:40.827889'),(5,'copy of exp','this is a test exp contains 2 cirros','2016-12-28 09:57:12.901060','2016-12-28 09:57:12.901099','hello','you can ping each other between these two hosts','',2,2,0,'2016-12-28 09:57:12.901158'),(6,'copy of exp','this is a test exp contains 2 cirros','2016-12-28 10:11:47.527157','2016-12-28 10:11:47.527198','hello','you can ping each other between these two hosts','',2,2,0,'2016-12-28 10:11:47.527259'),(7,'copy of exp','this is a test exp contains 2 cirros','2016-12-28 10:16:22.207384','2016-12-28 10:16:22.207425','hello','you can ping each other between these two hosts','',2,2,0,'2016-12-28 10:16:22.207494'),(8,'copy of exp','this is a test exp contains 2 cirros','2016-12-28 10:19:09.123077','2016-12-28 10:19:09.123119','hello','you can ping each other between these two hosts','',2,2,0,'2016-12-28 10:19:09.123184'),(9,'copy of exp','this is a test exp contains 2 cirros','2016-12-28 10:19:59.103722','2016-12-28 10:19:59.103806','hello','you can ping each other between these two hosts','',2,2,0,'2016-12-28 10:19:59.103993'),(10,'copy of exp','this is a test exp contains 2 cirros','2016-12-28 10:20:27.273517','2016-12-28 10:20:27.273547','hello','you can ping each other between these two hosts','',2,2,0,'2016-12-28 10:20:27.273593'),(12,'copy of exp','this is a test exp contains 2 cirros','2016-12-29 06:49:37.176692','2016-12-29 06:49:37.176724','hello','you can ping each other between these two hosts','',2,2,0,'2016-12-29 06:49:37.176770'),(13,'copy of exp','this is a test exp contains 2 cirros','2016-12-29 06:51:45.232592','2016-12-29 06:51:45.232623','hello','you can ping each other between these two hosts','',2,2,0,'2016-12-29 06:51:45.232671'),(14,'copy of exp','this is a test exp contains 2 cirros','2016-12-29 06:53:01.071601','2016-12-29 06:53:01.071649','hello','you can ping each other between these two hosts','',2,2,0,'2016-12-29 06:53:01.071729'),(15,'copy of exp','this is a test exp contains 2 cirros','2016-12-29 06:54:30.754559','2016-12-29 06:54:30.754602','hello','you can ping each other between these two hosts','',2,2,0,'2016-12-29 06:54:30.754670'),(16,'copy of exp','this is a test exp contains 2 cirros','2016-12-29 07:24:30.355195','2016-12-29 07:24:30.355243','hello','you can ping each other between these two hosts','',2,2,0,'2016-12-29 07:24:30.355301'),(17,'copy of exp','this is a test exp contains 2 cirros','2016-12-29 07:27:27.999473','2016-12-29 07:27:27.999500','hello','you can ping each other between these two hosts','',2,2,0,'2016-12-29 07:27:27.999543'),(18,'copy of exp','this is a test exp contains 2 cirros','2016-12-29 07:29:18.659348','2016-12-29 07:29:18.659384','hello','you can ping each other between these two hosts','',2,2,0,'2016-12-29 07:29:18.659444'),(20,'new_create_exp333','this is a copy one','2016-12-29 07:33:17.255644','2016-12-29 08:17:54.316674','hello','hello','hello',1,2,0,'2016-12-29 07:33:17.255739'),(21,'new_create_exp444','this is a copy one','2016-12-29 07:37:03.562388','2017-03-08 10:50:54.983938','hello','hello','hello',11,2,1,'2017-03-08 10:53:58.111584'),(23,'copy of exp','this is a test exp contains 2 cirros','2016-12-29 07:47:28.611146','2016-12-29 07:47:28.611174','hello','you can ping each other between these two hosts','',2,2,0,'2016-12-29 07:47:28.611213'),(24,'exp00000','43erftesrfsdfsf','2017-03-02 07:54:56.296690','2017-03-07 01:42:14.864608','tsdfsdfdsfdsf','sdfdsfds','sdfsdfdsf',11,2,1,'2017-03-02 07:54:56.296749'),(25,'new_create_exp555','this is a copy one','2017-03-08 11:09:22.194889','2017-03-08 11:09:22.194915','hello','hello','hello',1,2,0,NULL),(26,'mcy-exp1111','test exp_create and exp_edit function!!!!!!','2017-03-09 03:00:08.743544','2017-03-09 06:45:51.653736','Step1:lkjsdflsdjfslkfsdfj\r\nStep2:dlkfjd;lkf;lf\r\nStep3:porewljfldsf','password=123456',NULL,11,2,1,'2017-03-09 07:00:50.974506'),(27,'mcy-exp1111_copy','test exp_create and exp_edit function!!!!!!','2017-03-09 06:58:16.830369','2017-03-09 06:58:16.830397','Step1:lkjsdflsdjfslkfsdfj\r\nStep2:dlkfjd;lkf;lf\r\nStep3:porewljfldsf','password=123456',NULL,11,2,1,'2017-03-09 06:58:55.418480');
/*!40000 ALTER TABLE `Iserlab_experiment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_experiment_exp_images`
--

DROP TABLE IF EXISTS `Iserlab_experiment_exp_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_experiment_exp_images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `experiment_id` int(11) NOT NULL,
  `vmimage_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Iserlab_experiment_exp_images_experiment_id_19cbabac_uniq` (`experiment_id`,`vmimage_id`),
  KEY `Iserlab_experiment_exp_vmimage_id_fc56594b_fk_Iserlab_vmimage_id` (`vmimage_id`),
  CONSTRAINT `Iserlab_experime_experiment_id_c79e95c2_fk_Iserlab_experiment_id` FOREIGN KEY (`experiment_id`) REFERENCES `Iserlab_experiment` (`id`),
  CONSTRAINT `Iserlab_experiment_exp_vmimage_id_fc56594b_fk_Iserlab_vmimage_id` FOREIGN KEY (`vmimage_id`) REFERENCES `Iserlab_vmimage` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_experiment_exp_images`
--

LOCK TABLES `Iserlab_experiment_exp_images` WRITE;
/*!40000 ALTER TABLE `Iserlab_experiment_exp_images` DISABLE KEYS */;
INSERT INTO `Iserlab_experiment_exp_images` VALUES (1,1,1),(3,1,3),(2,2,1),(7,4,1),(6,4,3),(9,5,1),(8,5,3),(11,6,1),(10,6,3),(13,7,1),(12,7,3),(15,8,1),(14,8,3),(17,9,1),(16,9,3),(19,10,1),(18,10,3),(23,12,1),(22,12,3),(25,13,1),(24,13,3),(27,14,1),(26,14,3),(29,15,1),(28,15,3),(31,16,1),(30,16,3),(33,17,1),(32,17,3),(36,20,1),(37,20,3),(38,21,1),(39,21,3),(43,23,1),(42,23,3),(44,24,2),(45,24,3),(46,25,1),(47,25,3),(48,26,1),(50,26,3),(51,27,1),(52,27,3);
/*!40000 ALTER TABLE `Iserlab_experiment_exp_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_experiment_exp_network`
--

DROP TABLE IF EXISTS `Iserlab_experiment_exp_network`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_experiment_exp_network` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `experiment_id` int(11) NOT NULL,
  `network_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Iserlab_experiment_exp_network_experiment_id_29ffed74_uniq` (`experiment_id`,`network_id`),
  KEY `Iserlab_experiment_exp_network_id_7b7a9aea_fk_Iserlab_network_id` (`network_id`),
  CONSTRAINT `Iserlab_experime_experiment_id_7278c5a9_fk_Iserlab_experiment_id` FOREIGN KEY (`experiment_id`) REFERENCES `Iserlab_experiment` (`id`),
  CONSTRAINT `Iserlab_experiment_exp_network_id_7b7a9aea_fk_Iserlab_network_id` FOREIGN KEY (`network_id`) REFERENCES `Iserlab_network` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_experiment_exp_network`
--

LOCK TABLES `Iserlab_experiment_exp_network` WRITE;
/*!40000 ALTER TABLE `Iserlab_experiment_exp_network` DISABLE KEYS */;
INSERT INTO `Iserlab_experiment_exp_network` VALUES (1,1,1),(2,2,2),(4,20,1),(5,21,1),(7,23,1),(8,24,2),(9,25,1),(10,26,2),(12,27,2);
/*!40000 ALTER TABLE `Iserlab_experiment_exp_network` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_expinstance`
--

DROP TABLE IF EXISTS `Iserlab_expinstance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_expinstance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `expInstance_id` varchar(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `createtime` datetime(6) NOT NULL,
  `updatetime` datetime(6) DEFAULT NULL,
  `servers` varchar(100) NOT NULL,
  `sourceExpTemplate_id` int(11) NOT NULL,
  `creator` varchar(201) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Iserlab_expinstance_6485e74c` (`sourceExpTemplate_id`),
  CONSTRAINT `Iserlab_e_sourceExpTemplate_id_9bb65aa9_fk_Iserlab_experiment_id` FOREIGN KEY (`sourceExpTemplate_id`) REFERENCES `Iserlab_experiment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_expinstance`
--

LOCK TABLES `Iserlab_expinstance` WRITE;
/*!40000 ALTER TABLE `Iserlab_expinstance` DISABLE KEYS */;
/*!40000 ALTER TABLE `Iserlab_expinstance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_group`
--

DROP TABLE IF EXISTS `Iserlab_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `desc` longtext,
  `stuCount` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Iserlab_group_d9614d40` (`teacher_id`),
  CONSTRAINT `Iserlab_group_teacher_id_ab0dbd73_fk_Iserlab_user_id` FOREIGN KEY (`teacher_id`) REFERENCES `Iserlab_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_group`
--

LOCK TABLES `Iserlab_group` WRITE;
/*!40000 ALTER TABLE `Iserlab_group` DISABLE KEYS */;
INSERT INTO `Iserlab_group` VALUES (3,'group2','hello',2,'2017-01-03 07:51:00.828522',1),(4,'group1','',4,'2017-03-01 04:48:48.998799',11),(13,'group3','hello',2,'2017-03-01 06:06:23.375308',11),(15,'group4','hello',2,'2017-03-01 09:40:07.545355',11),(17,'class111qqqqq0000','testtest9999999999999999999999999999qqqqqq00000000000000000000',2,'2017-03-01 09:50:35.574053',11);
/*!40000 ALTER TABLE `Iserlab_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_group_student`
--

DROP TABLE IF EXISTS `Iserlab_group_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_group_student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Iserlab_group_student_group_id_fc2db9da_uniq` (`group_id`,`student_id`),
  KEY `Iserlab_group_student_student_id_bd64bc19_fk_Iserlab_student_id` (`student_id`),
  CONSTRAINT `Iserlab_group_student_group_id_b738ed78_fk_Iserlab_group_id` FOREIGN KEY (`group_id`) REFERENCES `Iserlab_group` (`id`),
  CONSTRAINT `Iserlab_group_student_student_id_bd64bc19_fk_Iserlab_student_id` FOREIGN KEY (`student_id`) REFERENCES `Iserlab_student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_group_student`
--

LOCK TABLES `Iserlab_group_student` WRITE;
/*!40000 ALTER TABLE `Iserlab_group_student` DISABLE KEYS */;
INSERT INTO `Iserlab_group_student` VALUES (5,3,1),(4,3,4),(6,4,1),(7,4,2),(8,4,3),(46,4,4),(44,4,5),(45,4,6),(27,13,1),(26,13,4),(31,15,1),(30,15,4),(43,17,1),(42,17,2);
/*!40000 ALTER TABLE `Iserlab_group_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_imagecart`
--

DROP TABLE IF EXISTS `Iserlab_imagecart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_imagecart` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `createtime` datetime(6) NOT NULL,
  `image_id_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Iserlab_imagecart_16ee04f8` (`image_id_id`),
  KEY `Iserlab_imagecart_18624dd3` (`user_id`),
  CONSTRAINT `Iserlab_imagecart_image_id_id_b6214d04_fk_Iserlab_vmimage_id` FOREIGN KEY (`image_id_id`) REFERENCES `Iserlab_vmimage` (`id`),
  CONSTRAINT `Iserlab_imagecart_user_id_5b3cfb66_fk_Iserlab_user_id` FOREIGN KEY (`user_id`) REFERENCES `Iserlab_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_imagecart`
--

LOCK TABLES `Iserlab_imagecart` WRITE;
/*!40000 ALTER TABLE `Iserlab_imagecart` DISABLE KEYS */;
/*!40000 ALTER TABLE `Iserlab_imagecart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_network`
--

DROP TABLE IF EXISTS `Iserlab_network`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_network` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `network_id` varchar(50) DEFAULT NULL,
  `network_name` varchar(100) NOT NULL,
  `network_description` longtext NOT NULL,
  `gateway_ip` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `subnet_name` varchar(50) DEFAULT NULL,
  `cidr` varchar(40),
  `ip_version` varchar(2),
  `owner_id` int(11),
  `is_shared` tinyint(1) NOT NULL,
  `shared_time` datetime(6),
  `subnet_id` varchar(50),
  `allocation_pools_end` varchar(30),
  `allocation_pools_start` varchar(30),
  `enable_dhcp` varchar(10),
  `tenant_id` varchar(50),
  PRIMARY KEY (`id`),
  KEY `Iserlab_network_5e7b1936` (`owner_id`),
  CONSTRAINT `Iserlab_network_owner_id_5463a734_fk_Iserlab_user_id` FOREIGN KEY (`owner_id`) REFERENCES `Iserlab_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_network`
--

LOCK TABLES `Iserlab_network` WRITE;
/*!40000 ALTER TABLE `Iserlab_network` DISABLE KEYS */;
INSERT INTO `Iserlab_network` VALUES (1,'336e9e6e-4a1a-4a80-95ce-197e989e71a8','private_alice','','172.16.2.1','2016-12-27 04:03:19.027511','2017-03-09 02:58:52.475231','private_alice_subnet','172.16.2.0/24','4',11,0,'2017-03-09 02:58:52.475244','','','','',''),(2,'0822a491-0575-4e8f-abd3-55d2d3475236','private_exp1','','192.168.230.1','2016-12-27 04:22:31.904980','2017-03-09 02:58:44.452935','private_exp1_subnet','192.168.230.0/24','4',11,0,'2017-03-09 02:58:44.452943','','','','',''),(3,'','test-net111','this is a network to test whether launch_exp function works','10.0.4.1','2016-12-30 06:40:44.761308','2016-12-30 06:40:44.761374','test-net111-subnet','10.0.4.0/24','4',1,0,'2016-12-30 06:40:44.761425','','','','',NULL),(4,NULL,'mcy-network222','test network','10.0.5.1','2016-12-30 07:36:50.591206','2016-12-30 07:36:50.591238','mcy-subnet222','10.0.5.0/24','4',2,0,'2016-12-30 07:36:50.591265',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Iserlab_network` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_networkcart`
--

DROP TABLE IF EXISTS `Iserlab_networkcart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_networkcart` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `createtime` datetime(6) NOT NULL,
  `network_id_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Iserlab_networkcart_network_id_id_03f50b2a_fk_Iserlab_network_id` (`network_id_id`),
  KEY `Iserlab_networkcart_user_id_ddd96f05_fk_Iserlab_user_id` (`user_id`),
  CONSTRAINT `Iserlab_networkcart_network_id_id_03f50b2a_fk_Iserlab_network_id` FOREIGN KEY (`network_id_id`) REFERENCES `Iserlab_network` (`id`),
  CONSTRAINT `Iserlab_networkcart_user_id_ddd96f05_fk_Iserlab_user_id` FOREIGN KEY (`user_id`) REFERENCES `Iserlab_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_networkcart`
--

LOCK TABLES `Iserlab_networkcart` WRITE;
/*!40000 ALTER TABLE `Iserlab_networkcart` DISABLE KEYS */;
/*!40000 ALTER TABLE `Iserlab_networkcart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_score`
--

DROP TABLE IF EXISTS `Iserlab_score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_score` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `score` int(11) NOT NULL,
  `comment` longtext,
  `times` int(11) NOT NULL,
  `situation` varchar(10) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `result` varchar(500) DEFAULT NULL,
  `result_exp_id` varchar(10) DEFAULT NULL,
  `reportUrl` varchar(200) DEFAULT NULL,
  `exp_id` int(11) NOT NULL,
  `scorer_id` int(11) NOT NULL,
  `stu_id` int(11) NOT NULL,
  `scoreTime` datetime(6) DEFAULT NULL,
  `finishedTime` datetime(6),
  `delivery_id` int(11),
  `startTime` datetime(6),
  PRIMARY KEY (`id`),
  KEY `Iserlab_score_exp_id_8d03471f_fk_Iserlab_experiment_id` (`exp_id`),
  KEY `Iserlab_score_scorer_id_a8779782_fk_Iserlab_user_id` (`scorer_id`),
  KEY `Iserlab_score_stu_id_310e4097_fk_Iserlab_student_id` (`stu_id`),
  CONSTRAINT `Iserlab_score_exp_id_8d03471f_fk_Iserlab_experiment_id` FOREIGN KEY (`exp_id`) REFERENCES `Iserlab_experiment` (`id`),
  CONSTRAINT `Iserlab_score_scorer_id_a8779782_fk_Iserlab_user_id` FOREIGN KEY (`scorer_id`) REFERENCES `Iserlab_user` (`id`),
  CONSTRAINT `Iserlab_score_stu_id_310e4097_fk_Iserlab_student_id` FOREIGN KEY (`stu_id`) REFERENCES `Iserlab_student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_score`
--

LOCK TABLES `Iserlab_score` WRITE;
/*!40000 ALTER TABLE `Iserlab_score` DISABLE KEYS */;
INSERT INTO `Iserlab_score` VALUES (1,94,'dgdfsgsdffvcsssssssssssfg',1,'scored','2017-03-06 08:36:21.000000','','21','http://info.ruc.edu.cn/userfiles/upload/f20170307064512387.doc',24,11,2,'2017-03-07 01:59:44.000000','2017-03-02 02:54:07.000000',6,NULL),(2,60,'432rewrfwsf',2,'scored','2017-03-06 10:03:13.000000','','22','http://info.ruc.edu.cn/userfiles/upload/f20170307064512387.doc',24,11,3,'2017-03-07 09:56:36.000000','2017-03-01 02:54:24.000000',6,NULL),(3,89,'good',2,'scored','2017-03-06 10:03:43.000000','','23','http://info.ruc.edu.cn/userfiles/upload/f20170307064512387.doc',24,11,1,'2017-03-07 02:01:33.000000','2017-03-03 02:54:33.000000',6,NULL),(5,0,'',0,'paused','2017-03-07 10:10:44.483548','hello','23','http://info.ruc.edu.cn/userfiles/upload/f20170307064512387.doc',24,11,5,NULL,'2017-03-08 03:05:19.000000',6,'2017-03-07 04:29:40.000000'),(6,0,'',0,'doing','2017-03-08 04:28:31.647327','','','',24,11,6,NULL,NULL,6,'2017-03-08 04:28:17.000000'),(7,0,'',4,'done','2017-03-08 08:41:49.797914','password=o123456','20','',24,11,2,NULL,'2017-03-08 09:40:22.000000',20,'2017-03-07 09:40:20.000000'),(8,0,NULL,0,'undo','2017-03-08 08:41:49.936769',NULL,NULL,NULL,24,11,1,NULL,NULL,20,NULL),(9,0,NULL,0,'undo','2017-03-09 07:10:52.125002',NULL,NULL,NULL,24,11,1,NULL,NULL,21,NULL),(10,0,NULL,0,'undo','2017-03-09 07:10:52.174176',NULL,NULL,NULL,24,11,4,NULL,NULL,21,NULL),(11,0,NULL,0,'undo','2017-03-09 07:16:33.621188',NULL,NULL,NULL,26,11,2,NULL,NULL,22,NULL),(12,0,NULL,0,'undo','2017-03-09 07:16:33.649072',NULL,NULL,NULL,26,11,3,NULL,NULL,22,NULL),(13,0,NULL,0,'undo','2017-03-09 07:16:33.715818',NULL,NULL,NULL,26,11,1,NULL,NULL,22,NULL),(14,0,NULL,0,'undo','2017-03-09 07:16:33.849457',NULL,NULL,NULL,26,11,5,NULL,NULL,22,NULL),(15,0,NULL,0,'undo','2017-03-09 07:16:33.958297',NULL,NULL,NULL,26,11,4,NULL,NULL,22,NULL),(16,0,NULL,0,'undo','2017-03-09 07:16:33.999874',NULL,NULL,NULL,26,11,6,NULL,NULL,22,NULL);
/*!40000 ALTER TABLE `Iserlab_score` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_student`
--

DROP TABLE IF EXISTS `Iserlab_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stu_username` varchar(50) NOT NULL,
  `stu_password` varchar(50) NOT NULL,
  `stu_email` varchar(254) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_student`
--

LOCK TABLES `Iserlab_student` WRITE;
/*!40000 ALTER TABLE `Iserlab_student` DISABLE KEYS */;
INSERT INTO `Iserlab_student` VALUES (1,'lilei','123','machenyi2011@163.com'),(2,'alice','123','ken911121@126.com'),(3,'Bob','123','machenyi2014@ruc.edu.cn'),(4,'mcy','os62511279','machenyi2011@163.com'),(5,'lyj','os62511279','zsyz_lyj@163.com'),(6,'stu11','123','stu1@126.com'),(7,'stu12','123','stu12@126.com');
/*!40000 ALTER TABLE `Iserlab_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_tag`
--

DROP TABLE IF EXISTS `Iserlab_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `createtime` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_tag`
--

LOCK TABLES `Iserlab_tag` WRITE;
/*!40000 ALTER TABLE `Iserlab_tag` DISABLE KEYS */;
INSERT INTO `Iserlab_tag` VALUES (1,'cirros','2016-12-25 07:37:48.827785'),(2,'Windows7','2016-12-25 08:04:51.156219'),(3,'Ubuntu14','2016-12-25 08:04:58.452043');
/*!40000 ALTER TABLE `Iserlab_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_user`
--

DROP TABLE IF EXISTS `Iserlab_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(254) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_user`
--

LOCK TABLES `Iserlab_user` WRITE;
/*!40000 ALTER TABLE `Iserlab_user` DISABLE KEYS */;
INSERT INTO `Iserlab_user` VALUES (1,'teacher1','111',''),(2,'teacher2','111',''),(3,'teacher5','123','teacher5@163.com'),(4,'teacher3','123','123@126.com'),(5,'teacher4','123','234@126.com'),(6,'teacher6','123','111@126.com'),(7,'haha','123','haha@126.com'),(8,'wan','123','ken911121@126.com'),(9,'kai','123','kai@126.com'),(10,'yuan','123','yuan@126.com'),(11,'111','111','1@126.com'),(12,'222','111','2@126.com'),(13,'333','111','ken911121@126.com'),(14,'444','111','ken911121@126.com'),(15,'555','123','ken911121@126.com'),(16,'777','111','111@126.com'),(17,'jing','123','jing@126.com');
/*!40000 ALTER TABLE `Iserlab_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_vmimage`
--

DROP TABLE IF EXISTS `Iserlab_vmimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_vmimage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `image_id` varchar(36) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `is_public` varchar(10) NOT NULL,
  `description` longtext NOT NULL,
  `status` varchar(30) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `size` bigint(20) NOT NULL,
  `min_disk` int(11) NOT NULL,
  `min_ram` int(11) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `own_project` varchar(32),
  `is_shared` tinyint(1) NOT NULL,
  `shared_time` datetime(6),
  `flavor` varchar(10),
  `keypair` varchar(20),
  PRIMARY KEY (`id`),
  KEY `Iserlab_vmimage_owner_id_a20c2908_fk_Iserlab_user_id` (`owner_id`),
  CONSTRAINT `Iserlab_vmimage_owner_id_a20c2908_fk_Iserlab_user_id` FOREIGN KEY (`owner_id`) REFERENCES `Iserlab_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_vmimage`
--

LOCK TABLES `Iserlab_vmimage` WRITE;
/*!40000 ALTER TABLE `Iserlab_vmimage` DISABLE KEYS */;
INSERT INTO `Iserlab_vmimage` VALUES (1,'70122065-a0ed-4975-8ba3-1740cdaf3722','cirros','YES','rererererertest image','active','2016-12-25 07:37:58.327967','2016-12-26 09:13:34.527013',13287936,0,0,1,'2f1bc8c34f094d049a201819732537a3',0,NULL,NULL,NULL),(2,'63831167-8dfb-401e-93f9-0a17ae6ba464','webserver_ubuntu14.04','YES','','active','2016-12-26 09:13:22.366151','2016-12-27 08:03:05.452001',5168168960,0,0,1,'2f1bc8c34f094d049a201819732537a3',0,NULL,NULL,NULL),(3,'c038649a-04e9-4603-8fc9-83a92d0f835e','cirros-111','YES','','active','2016-12-27 08:01:51.384296','2016-12-27 08:01:51.384321',13287936,0,0,1,'bd9dc26b524143339cad03c0ee048429',0,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Iserlab_vmimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_vmimage_tags`
--

DROP TABLE IF EXISTS `Iserlab_vmimage_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_vmimage_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vmimage_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Iserlab_vmimage_tags_vmimage_id_3956a9b2_uniq` (`vmimage_id`,`tag_id`),
  KEY `Iserlab_vmimage_tags_tag_id_dad1e1ec_fk_Iserlab_tag_id` (`tag_id`),
  CONSTRAINT `Iserlab_vmimage_tags_tag_id_dad1e1ec_fk_Iserlab_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `Iserlab_tag` (`id`),
  CONSTRAINT `Iserlab_vmimage_tags_vmimage_id_40323ac9_fk_Iserlab_vmimage_id` FOREIGN KEY (`vmimage_id`) REFERENCES `Iserlab_vmimage` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_vmimage_tags`
--

LOCK TABLES `Iserlab_vmimage_tags` WRITE;
/*!40000 ALTER TABLE `Iserlab_vmimage_tags` DISABLE KEYS */;
INSERT INTO `Iserlab_vmimage_tags` VALUES (1,1,1),(2,2,3),(3,3,1);
/*!40000 ALTER TABLE `Iserlab_vmimage_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Iserlab_vminstance`
--

DROP TABLE IF EXISTS `Iserlab_vminstance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Iserlab_vminstance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_id` varchar(100) NOT NULL,
  `name` varchar(255) NOT NULL,
  `createtime` datetime(6) NOT NULL,
  `updatetime` datetime(6) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `ip` varchar(20) NOT NULL,
  `vncurl` varchar(200) NOT NULL,
  `owner` varchar(20) NOT NULL,
  `exp_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Iserlab_vminstance_fe4f53fa` (`exp_id`),
  CONSTRAINT `Iserlab_vminstance_exp_id_ee07a44d_fk_Iserlab_expinstance_id` FOREIGN KEY (`exp_id`) REFERENCES `Iserlab_expinstance` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Iserlab_vminstance`
--

LOCK TABLES `Iserlab_vminstance` WRITE;
/*!40000 ALTER TABLE `Iserlab_vminstance` DISABLE KEYS */;
/*!40000 ALTER TABLE `Iserlab_vminstance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(22,'Can add user',8,'add_user'),(23,'Can change user',8,'change_user'),(24,'Can delete user',8,'delete_user'),(46,'Can add student',16,'add_student'),(47,'Can change student',16,'change_student'),(48,'Can delete student',16,'delete_student'),(49,'Can add author',17,'add_author'),(50,'Can change author',17,'change_author'),(51,'Can delete author',17,'delete_author'),(52,'Can add article',18,'add_article'),(53,'Can change article',18,'change_article'),(54,'Can delete article',18,'delete_article'),(55,'Can add tag',19,'add_tag'),(56,'Can change tag',19,'change_tag'),(57,'Can delete tag',19,'delete_tag'),(58,'Can add blog',20,'add_blog'),(59,'Can change blog',20,'change_blog'),(60,'Can delete blog',20,'delete_blog'),(61,'Can add person',21,'add_person'),(62,'Can change person',21,'change_person'),(63,'Can delete person',21,'delete_person'),(64,'Can add vm image',22,'add_vmimage'),(65,'Can change vm image',22,'change_vmimage'),(66,'Can delete vm image',22,'delete_vmimage'),(67,'Can add tag',23,'add_tag'),(68,'Can change tag',23,'change_tag'),(69,'Can delete tag',23,'delete_tag'),(70,'Can add network',24,'add_network'),(71,'Can change network',24,'change_network'),(72,'Can delete network',24,'delete_network'),(73,'Can add experiment',25,'add_experiment'),(74,'Can change experiment',25,'change_experiment'),(75,'Can delete experiment',25,'delete_experiment'),(82,'Can add vm instance',28,'add_vminstance'),(83,'Can change vm instance',28,'change_vminstance'),(84,'Can delete vm instance',28,'delete_vminstance'),(85,'Can add exp instance',29,'add_expinstance'),(86,'Can change exp instance',29,'change_expinstance'),(87,'Can delete exp instance',29,'delete_expinstance'),(88,'Can add delivery',30,'add_delivery'),(89,'Can change delivery',30,'change_delivery'),(90,'Can delete delivery',30,'delete_delivery'),(91,'Can add publisher',31,'add_publisher'),(92,'Can change publisher',31,'change_publisher'),(93,'Can delete publisher',31,'delete_publisher'),(94,'Can add author2',32,'add_author2'),(95,'Can change author2',32,'change_author2'),(96,'Can delete author2',32,'delete_author2'),(97,'Can add book',33,'add_book'),(98,'Can change book',33,'change_book'),(99,'Can delete book',33,'delete_book'),(100,'Can add image cart',34,'add_imagecart'),(101,'Can change image cart',34,'change_imagecart'),(102,'Can delete image cart',34,'delete_imagecart'),(103,'Can add network cart',35,'add_networkcart'),(104,'Can change network cart',35,'change_networkcart'),(105,'Can delete network cart',35,'delete_networkcart'),(106,'Can add group',36,'add_group'),(107,'Can change group',36,'change_group'),(108,'Can delete group',36,'delete_group'),(109,'Can add catagory',37,'add_catagory'),(110,'Can change catagory',37,'change_catagory'),(111,'Can delete catagory',37,'delete_catagory'),(112,'Can add tag',38,'add_tag'),(113,'Can change tag',38,'change_tag'),(114,'Can delete tag',38,'delete_tag'),(115,'Can add blog',39,'add_blog'),(116,'Can change blog',39,'change_blog'),(117,'Can delete blog',39,'delete_blog'),(118,'Can add comment',40,'add_comment'),(119,'Can change comment',40,'change_comment'),(120,'Can delete comment',40,'delete_comment'),(124,'Can add score',42,'add_score'),(125,'Can change score',42,'change_score'),(126,'Can delete score',42,'delete_score');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$24000$LQVG8DBYmGvo$FjuQoALpioFdneNnpmvAF7dU4ywVfs4sRF6Sk4jXLww=','2017-02-24 02:37:35.113846',1,'admin','','','admin@163.com',1,1,'2016-12-14 03:29:21.996154');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blog_blog`
--

DROP TABLE IF EXISTS `blog_blog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog_blog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  `author` varchar(16) NOT NULL,
  `content` longtext NOT NULL,
  `created` datetime(6) NOT NULL,
  `catagory_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `blog_blog_cbd024a9` (`catagory_id`),
  CONSTRAINT `blog_blog_catagory_id_09567507_fk_blog_catagory_id` FOREIGN KEY (`catagory_id`) REFERENCES `blog_catagory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_blog`
--

LOCK TABLES `blog_blog` WRITE;
/*!40000 ALTER TABLE `blog_blog` DISABLE KEYS */;
INSERT INTO `blog_blog` VALUES (1,'hello world','mcy','shfpsafsldfkjldsafjadskncsdfjkweflkdsaaaaaacfccxfca','2017-03-01 07:39:23.433281',1),(2,'C++','ken','1243243223333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333','2017-03-01 07:39:41.657078',2);
/*!40000 ALTER TABLE `blog_blog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blog_blog_tags`
--

DROP TABLE IF EXISTS `blog_blog_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog_blog_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `blog_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `blog_blog_tags_blog_id_211c6be5_uniq` (`blog_id`,`tag_id`),
  KEY `blog_blog_tags_tag_id_36a3abc6_fk_blog_tag_id` (`tag_id`),
  CONSTRAINT `blog_blog_tags_blog_id_e4cd5f6a_fk_blog_blog_id` FOREIGN KEY (`blog_id`) REFERENCES `blog_blog` (`id`),
  CONSTRAINT `blog_blog_tags_tag_id_36a3abc6_fk_blog_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `blog_tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_blog_tags`
--

LOCK TABLES `blog_blog_tags` WRITE;
/*!40000 ALTER TABLE `blog_blog_tags` DISABLE KEYS */;
INSERT INTO `blog_blog_tags` VALUES (1,1,1),(2,2,2);
/*!40000 ALTER TABLE `blog_blog_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blog_catagory`
--

DROP TABLE IF EXISTS `blog_catagory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog_catagory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_catagory`
--

LOCK TABLES `blog_catagory` WRITE;
/*!40000 ALTER TABLE `blog_catagory` DISABLE KEYS */;
INSERT INTO `blog_catagory` VALUES (1,'c1'),(2,'c2');
/*!40000 ALTER TABLE `blog_catagory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blog_comment`
--

DROP TABLE IF EXISTS `blog_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  `email` varchar(254) NOT NULL,
  `content` varchar(240) NOT NULL,
  `created` datetime(6) NOT NULL,
  `blog_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `blog_comment_blog_id_c664fb0d_fk_blog_blog_id` (`blog_id`),
  CONSTRAINT `blog_comment_blog_id_c664fb0d_fk_blog_blog_id` FOREIGN KEY (`blog_id`) REFERENCES `blog_blog` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_comment`
--

LOCK TABLES `blog_comment` WRITE;
/*!40000 ALTER TABLE `blog_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `blog_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blog_tag`
--

DROP TABLE IF EXISTS `blog_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_tag`
--

LOCK TABLES `blog_tag` WRITE;
/*!40000 ALTER TABLE `blog_tag` DISABLE KEYS */;
INSERT INTO `blog_tag` VALUES (1,'A'),(2,'B');
/*!40000 ALTER TABLE `blog_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=160 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2016-12-14 03:30:36.363803','1','Blog object',1,'Added.',20,1),(2,'2016-12-14 03:30:50.295673','2','Blog object',1,'Added.',20,1),(3,'2016-12-14 03:31:02.644516','3','Blog object',1,'Added.',20,1),(4,'2016-12-14 03:31:58.565663','3','Blog object',2,'Changed content.',20,1),(5,'2016-12-14 03:34:22.632541','3','Blog object',2,'Changed content and author.',20,1),(6,'2016-12-14 06:24:35.852368','3','Blog object',2,'Changed type.',20,1),(7,'2016-12-14 06:53:23.450790','1','Person object',1,'Added.',21,1),(8,'2016-12-14 07:25:46.919172','2','iserlab',2,'Changed type and author.',20,1),(9,'2016-12-14 07:36:00.335608','2','Person object',1,'Added.',21,1),(10,'2016-12-14 07:37:45.231519','4','errererer',1,'Added.',20,1),(11,'2016-12-25 06:42:53.860228','1','shanshan Lu',1,'Added.',32,1),(12,'2016-12-25 06:46:40.731886','1','shanshan Lu',2,'Changed address.',32,1),(13,'2016-12-25 07:12:20.147320','1','django book',1,'Added.',33,1),(14,'2016-12-25 07:21:18.293380','2','Chenyi Ma',1,'Added.',32,1),(15,'2016-12-25 07:27:33.269063','1','lilei',1,'Added.',16,1),(16,'2016-12-25 07:32:17.281198','1','teacher1',1,'Added.',8,1),(17,'2016-12-25 07:32:29.667085','2','teacher2',1,'Added.',8,1),(18,'2016-12-25 07:33:25.606657','2','alice',1,'Added.',16,1),(19,'2016-12-25 07:37:48.828207','1','cirros',1,'Added.',23,1),(20,'2016-12-25 07:37:58.330626','1','id=70122065-a0ed-4975-8ba3-1740cdaf3722,name=cirros',1,'Added.',22,1),(21,'2016-12-25 08:04:51.156557','2','Windows7',1,'Added.',23,1),(22,'2016-12-25 08:04:58.452430','3','Ubuntu14',1,'Added.',23,1),(23,'2016-12-26 08:13:47.526900','3','Bob',1,'Added.',16,1),(24,'2016-12-26 09:11:28.997499','1','id=70122065-a0ed-4975-8ba3-1740cdaf3722,name=cirros',2,'Changed own_project.',22,1),(25,'2016-12-26 09:13:22.369486','2','id=63831167-8dfb-401e-93f9-0a17ae6ba464,name=webserver_ubuntu14.04',1,'Added.',22,1),(26,'2016-12-26 09:13:34.529086','1','id=70122065-a0ed-4975-8ba3-1740cdaf3722,name=cirros',2,'Changed is_public.',22,1),(27,'2016-12-27 04:03:19.028119','1','id=336e9e6e-4a1a-4a80-95ce-197e989e71a8,name=private_alice',1,'Added.',24,1),(28,'2016-12-27 04:07:51.597176','1','id=336e9e6e-4a1a-4a80-95ce-197e989e71a8,name=private_alice',2,'Changed ip_version and cidr.',24,1),(29,'2016-12-27 04:18:26.169591','1','id=336e9e6e-4a1a-4a80-95ce-197e989e71a8,name=private_alice',2,'Changed owner.',24,1),(30,'2016-12-27 04:22:31.905892','2','id=0822a491-0575-4e8f-abd3-55d2d3475236,name=private_exp1',1,'Added.',24,1),(31,'2016-12-27 04:25:56.269905','1','id=1,name=exptest1',1,'Added.',25,1),(32,'2016-12-27 04:31:00.912018','1','id=1,name=exptest1',2,'Changed exp_image_count.',25,1),(33,'2016-12-27 05:45:22.306932','2','id=2,name=exp000',1,'Added.',25,1),(34,'2016-12-27 08:01:51.542618','3','id=c038649a-04e9-4603-8fc9-83a92d0f835e,name=cirros-111',1,'Added.',22,1),(35,'2016-12-27 08:03:05.453996','2','id=63831167-8dfb-401e-93f9-0a17ae6ba464,name=webserver_ubuntu14.04',2,'Changed is_public.',22,1),(36,'2016-12-27 08:08:11.007785','1','id=1,name=exptest1',2,'Changed exp_images.',25,1),(37,'2016-12-29 08:16:13.700433','11','id=11,name=copy of exp,creater=teacher2',3,'',25,1),(38,'2016-12-29 08:16:41.582002','3','id=3,name=new_create_exp222,creater=teacher1',3,'',25,1),(39,'2016-12-29 08:17:16.456498','19','id=19,name=copy of exp,creater=teacher2',3,'',25,1),(40,'2016-12-29 08:17:35.084915','22','id=22,name=new_create_exp555,creater=teacher1',2,'Changed is_shared.',25,1),(41,'2016-12-29 08:17:46.264219','21','id=21,name=new_create_exp444,creater=teacher1',2,'Changed is_shared.',25,1),(42,'2016-12-29 08:17:54.319451','20','id=20,name=new_create_exp333,creater=teacher1',2,'Changed is_shared.',25,1),(43,'2016-12-30 06:40:44.762961','3','network_id=,name=test-net111,creator=teacher1,is_shared=False',1,'Added.',24,1),(44,'2016-12-30 06:41:14.122185','2','network_id=0822a491-0575-4e8f-abd3-55d2d3475236,name=private_exp1,creator=teacher1,is_shared=False',2,'Changed subnet_name.',24,1),(45,'2016-12-30 06:41:31.190482','1','network_id=336e9e6e-4a1a-4a80-95ce-197e989e71a8,name=private_alice,creator=teacher1,is_shared=False',2,'Changed subnet_name.',24,1),(46,'2017-01-03 06:21:24.299822','4','mcy',1,'Added.',16,1),(47,'2017-01-03 06:22:18.166388','5','lyj',1,'Added.',16,1),(48,'2017-01-03 07:28:33.100662','1','gname=info_sec,teacher=teacher1',1,'Added.',36,1),(49,'2017-01-03 07:51:25.885362','2','gname=group2,teacher=teacher1',3,'',36,1),(50,'2017-01-03 08:13:26.623505','1','gname=info_sec,teacher=teacher2',2,'Changed teacher.',36,1),(51,'2017-03-01 03:07:20.164059','2','000',1,'Added.',4,1),(52,'2017-03-01 03:08:14.942813','2','000',3,'',4,1),(53,'2017-03-01 04:48:49.001185','4','gname=group1,teacher=111',1,'Added.',36,1),(54,'2017-03-01 05:38:17.843627','5','gname=group3,teacher=111',2,'Changed name.',36,1),(55,'2017-03-01 06:06:02.585549','10','gname=group3,teacher=111',3,'',36,1),(56,'2017-03-01 07:38:08.396179','1','c1',1,'Added.',37,1),(57,'2017-03-01 07:38:13.650374','2','c2',1,'Added.',37,1),(58,'2017-03-01 07:38:22.746325','1','??',1,'Added.',38,1),(59,'2017-03-01 07:38:40.682565','1','A',2,'Changed name.',38,1),(60,'2017-03-01 07:38:46.886388','2','B',1,'Added.',38,1),(61,'2017-03-01 07:39:23.435370','1','hello world',1,'Added.',39,1),(62,'2017-03-01 07:39:41.949750','2','C++',1,'Added.',39,1),(63,'2017-03-01 10:43:46.663177','22','id=22,name=new_create_exp555,creater=111,is_shared=True',2,'Changed exp_owner.',25,1),(64,'2017-03-01 10:43:58.098626','21','id=21,name=new_create_exp444,creater=111,is_shared=True',2,'Changed exp_owner.',25,1),(65,'2017-03-02 04:18:22.979098','17','gname=class111qqqqq,teacher=111',2,'Changed student.',36,1),(66,'2017-03-02 07:54:56.322636','24','id=24,name=exp00000,creater=111,is_shared=False',1,'Added.',25,1),(67,'2017-03-02 08:10:12.027368','6','delivery_record1',1,'Added.',30,1),(68,'2017-03-02 08:11:10.446654','6','delivery_record1',2,'Changed stop_time.',30,1),(69,'2017-03-02 08:28:23.367077','6','delivery_record1',2,'Changed exp.',30,1),(70,'2017-03-02 09:54:48.938556','24','id=24,name=exp00000,creater=111,is_shared=True',2,'Changed is_shared.',25,1),(71,'2017-03-06 06:07:22.502486','1','Score object',1,'Added.',NULL,1),(72,'2017-03-06 07:11:05.564914','6','delivery_record1',2,'Changed stop_time.',30,1),(73,'2017-03-06 08:36:40.632087','1','Score object',1,'Added.',42,1),(74,'2017-03-06 10:03:15.175689','2','Score object',1,'Added.',42,1),(75,'2017-03-06 10:03:25.256150','1','Score object',2,'Changed times and situation.',42,1),(76,'2017-03-06 10:03:48.782452','3','Score object',1,'Added.',42,1),(77,'2017-03-06 10:09:00.615085','1','Score object',2,'No fields changed.',42,1),(78,'2017-03-06 10:16:10.950773','2','Score object',2,'Changed result_exp_id.',42,1),(79,'2017-03-06 10:16:17.760884','3','Score object',2,'Changed result_exp_id.',42,1),(80,'2017-03-06 10:21:09.716953','4','Score object',1,'Added.',42,1),(81,'2017-03-06 10:21:36.178230','4','Score object',2,'Changed situation.',42,1),(82,'2017-03-06 10:22:29.791206','4','Score object',2,'Changed situation.',42,1),(83,'2017-03-06 11:16:39.952946','4','Score object',2,'Changed situation.',42,1),(84,'2017-03-06 11:17:59.258423','4','Score object',2,'Changed situation.',42,1),(85,'2017-03-06 11:18:46.666412','4','Score object',2,'Changed situation.',42,1),(86,'2017-03-07 01:42:14.866672','24','id=24,name=exp00000,creater=111,is_shared=True',2,'Changed is_shared.',25,1),(87,'2017-03-07 01:42:27.157651','21','id=21,name=new_create_exp444,creater=111,is_shared=True',2,'Changed is_shared.',25,1),(88,'2017-03-07 01:59:44.969282','1','Score object',2,'No fields changed.',42,1),(89,'2017-03-07 02:01:18.530106','4','Score object',3,'',42,1),(90,'2017-03-07 02:01:33.947429','3','Score object',2,'Changed score and comment.',42,1),(91,'2017-03-07 09:22:57.618088','4','gname=group1,teacher=111',2,'Changed student.',36,1),(92,'2017-03-07 09:40:59.882086','3','Score object',2,'Changed situation.',42,1),(93,'2017-03-07 09:41:15.454115','3','Score object',2,'Changed situation.',42,1),(94,'2017-03-07 09:41:29.919770','3','Score object',2,'Changed situation.',42,1),(95,'2017-03-07 09:46:14.701257','1','Score object',2,'Changed situation.',42,1),(96,'2017-03-07 09:46:24.581974','3','Score object',2,'Changed situation.',42,1),(97,'2017-03-07 10:10:44.483936','5','Score object',1,'Added.',42,1),(98,'2017-03-07 10:10:58.675497','4','gname=group1,teacher=111',2,'Changed student.',36,1),(99,'2017-03-08 01:46:34.155037','5','Score object',2,'Changed delivery_id.',42,1),(100,'2017-03-08 01:46:39.009232','3','Score object',2,'Changed delivery_id.',42,1),(101,'2017-03-08 01:46:47.767470','2','Score object',2,'Changed delivery_id.',42,1),(102,'2017-03-08 01:46:52.580829','1','Score object',2,'Changed delivery_id.',42,1),(103,'2017-03-08 02:54:09.617521','1','Score object',2,'Changed finishedTime.',42,1),(104,'2017-03-08 02:54:25.575735','2','Score object',2,'Changed finishedTime.',42,1),(105,'2017-03-08 02:54:35.052102','3','Score object',2,'Changed finishedTime.',42,1),(106,'2017-03-08 03:05:49.659340','5','Score object',2,'Changed finishedTime, situation, result and result_exp_id.',42,1),(107,'2017-03-08 03:06:49.361316','5','Score object',2,'Changed reportUrl.',42,1),(108,'2017-03-08 03:07:15.518748','5','Score object',2,'Changed reportUrl.',42,1),(109,'2017-03-08 03:07:31.838475','3','Score object',2,'Changed reportUrl.',42,1),(110,'2017-03-08 03:07:37.261580','1','Score object',2,'Changed reportUrl.',42,1),(111,'2017-03-08 03:07:42.771229','2','Score object',2,'Changed reportUrl.',42,1),(112,'2017-03-08 04:28:31.647732','6','Score object',1,'Added.',42,1),(113,'2017-03-08 04:28:53.057365','4','gname=group1,teacher=111',2,'Changed student.',36,1),(114,'2017-03-08 04:29:43.950864','5','Score object',2,'Changed startTime.',42,1),(115,'2017-03-08 04:44:16.556309','6','Score object',2,'Changed situation.',42,1),(116,'2017-03-08 04:44:57.846389','6','Score object',2,'Changed situation.',42,1),(117,'2017-03-08 04:46:09.866743','5','Score object',2,'No fields changed.',42,1),(118,'2017-03-08 04:46:37.386301','5','Score object',2,'Changed situation.',42,1),(119,'2017-03-08 08:13:37.221915','5','gname=group3,teacher=111',3,'',36,1),(120,'2017-03-08 08:13:55.223669','12','gname=group3,teacher=111',3,'',36,1),(121,'2017-03-08 08:14:00.589097','11','gname=group3,teacher=111',3,'',36,1),(122,'2017-03-08 08:14:06.457951','9','gname=group3,teacher=111',3,'',36,1),(123,'2017-03-08 08:14:24.178963','7','dffgdet',3,'',30,1),(124,'2017-03-08 08:17:17.983193','12','mcy-delivery',3,'',30,1),(125,'2017-03-08 08:17:21.724491','11','mcy-delivery',3,'',30,1),(126,'2017-03-08 08:17:25.512368','10','mcy-delivery',3,'',30,1),(127,'2017-03-08 08:17:29.664025','9','mcy-delivery',3,'',30,1),(128,'2017-03-08 08:17:33.768769','8','delivery8',3,'',30,1),(129,'2017-03-08 08:21:56.683406','14','dsgfdsfds',3,'',30,1),(130,'2017-03-08 08:22:01.129056','13','delivery-hehe',3,'',30,1),(131,'2017-03-08 08:37:39.726013','15','546545454delivery',3,'',30,1),(132,'2017-03-08 08:37:43.577496','18','43434',3,'',30,1),(133,'2017-03-08 08:37:47.763183','17','546545454delivery',3,'',30,1),(134,'2017-03-08 08:37:51.527653','16','546545454delivery',3,'',30,1),(135,'2017-03-08 08:43:20.011867','19','999999999',3,'',30,1),(136,'2017-03-08 09:15:55.233413','20','trtrtrtrtrt',2,'No fields changed.',30,1),(137,'2017-03-08 09:17:07.477218','6','delivery_record1',2,'Changed desc.',30,1),(138,'2017-03-08 09:41:21.222675','7','Score object',2,'Changed startTime, finishedTime, times, situation, result and result_exp_id.',42,1),(139,'2017-03-08 10:50:54.986198','21','id=21,name=new_create_exp444,creater=111,is_shared=False',2,'Changed is_shared.',25,1),(140,'2017-03-09 02:58:44.453642','2','name=private_exp1,creator=111,is_shared=False',2,'Changed owner.',24,1),(141,'2017-03-09 02:58:52.476248','1','name=private_alice,creator=111,is_shared=False',2,'Changed owner.',24,1),(142,'2017-03-09 07:01:53.969761','1','lilei',2,'Changed stu_email.',16,1),(143,'2017-03-09 07:04:51.972731','2','alice',2,'Changed stu_email.',16,1),(144,'2017-03-09 07:05:45.434282','3','Bob',2,'Changed stu_email.',16,1),(145,'2017-03-09 07:07:55.112025','4','gname=group1,teacher=111',2,'Changed student.',36,1),(146,'2017-03-09 07:17:08.813043','23','323sdsdsdsd',3,'',30,1),(147,'2017-03-09 07:17:49.958447','28','Score object',3,'',42,1),(148,'2017-03-09 07:17:54.223319','27','Score object',3,'',42,1),(149,'2017-03-09 07:17:58.429076','26','Score object',3,'',42,1),(150,'2017-03-09 07:18:09.445171','25','Score object',3,'',42,1),(151,'2017-03-09 07:18:13.598219','24','Score object',3,'',42,1),(152,'2017-03-09 07:18:17.122958','23','Score object',3,'',42,1),(153,'2017-03-09 07:18:20.843520','22','Score object',3,'',42,1),(154,'2017-03-09 07:18:27.823569','21','Score object',3,'',42,1),(155,'2017-03-09 07:18:31.775090','20','Score object',3,'',42,1),(156,'2017-03-09 07:18:37.342089','19','Score object',3,'',42,1),(157,'2017-03-09 07:18:41.302623','18','Score object',3,'',42,1),(158,'2017-03-09 07:18:45.838432','17','Score object',3,'',42,1),(159,'2017-03-09 07:44:29.147386','1','lilei',2,'Changed stu_email.',16,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(39,'blog','blog'),(37,'blog','catagory'),(40,'blog','comment'),(38,'blog','tag'),(5,'contenttypes','contenttype'),(30,'Iserlab','delivery'),(25,'Iserlab','experiment'),(29,'Iserlab','expinstance'),(36,'Iserlab','group'),(34,'Iserlab','imagecart'),(24,'Iserlab','network'),(35,'Iserlab','networkcart'),(42,'Iserlab','score'),(16,'Iserlab','student'),(23,'Iserlab','tag'),(8,'Iserlab','user'),(22,'Iserlab','vmimage'),(28,'Iserlab','vminstance'),(18,'people','article'),(17,'people','author'),(32,'people','author2'),(20,'people','blog'),(33,'people','book'),(21,'people','person'),(31,'people','publisher'),(19,'people','tag'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-12-13 07:42:40.622092'),(2,'auth','0001_initial','2016-12-13 07:42:49.393373'),(3,'admin','0001_initial','2016-12-13 07:42:51.270335'),(4,'admin','0002_logentry_remove_auto_add','2016-12-13 07:42:51.379497'),(5,'contenttypes','0002_remove_content_type_name','2016-12-13 07:42:52.366815'),(6,'auth','0002_alter_permission_name_max_length','2016-12-13 07:42:53.202569'),(7,'auth','0003_alter_user_email_max_length','2016-12-13 07:42:53.898106'),(8,'auth','0004_alter_user_username_opts','2016-12-13 07:42:53.940436'),(9,'auth','0005_alter_user_last_login_null','2016-12-13 07:42:54.450253'),(10,'auth','0006_require_contenttypes_0002','2016-12-13 07:42:54.491967'),(11,'auth','0007_alter_validators_add_error_messages','2016-12-13 07:42:54.540075'),(12,'sessions','0001_initial','2016-12-13 07:42:55.119018'),(13,'people','0001_initial','2016-12-13 07:58:54.512030'),(14,'Iserlab','0001_initial','2016-12-13 08:08:48.541990'),(15,'Iserlab','0002_auto_20161213_0805','2016-12-13 08:08:49.310831'),(16,'people','0002_article','2016-12-13 08:51:19.344835'),(17,'people','0003_delete_article','2016-12-13 09:01:27.196538'),(18,'people','0004_article','2016-12-13 09:02:10.022450'),(19,'people','0005_remove_article_labels','2016-12-13 09:02:52.346077'),(20,'people','0006_article_labels','2016-12-13 09:06:07.756548'),(21,'people','0007_author_blog_entry','2016-12-13 09:23:20.010163'),(22,'Iserlab','0003_auto_20161213_1029','2016-12-13 10:29:30.820928'),(23,'people','0002_auto_20161213_1032','2016-12-13 10:37:00.302702'),(24,'people','0003_blog','2016-12-14 03:14:05.111414'),(25,'people','0004_blog_author','2016-12-14 03:33:53.357386'),(26,'people','0005_blog_type','2016-12-14 06:24:21.488427'),(27,'people','0006_delete_person','2016-12-14 06:43:59.022712'),(28,'people','0007_person','2016-12-14 06:53:03.704395'),(29,'Iserlab','0004_auto_20161225_0527','2016-12-25 05:28:38.550319'),(30,'people','0008_auto_20161225_0527','2016-12-25 05:28:42.600475'),(31,'Iserlab','0005_auto_20161225_0535','2016-12-25 05:36:08.307731'),(32,'Iserlab','0006_auto_20161225_0613','2016-12-25 06:13:07.651613'),(33,'people','0009_auto_20161225_0613','2016-12-25 06:13:07.789762'),(34,'Iserlab','0007_auto_20161225_0639','2016-12-25 06:39:09.926527'),(35,'people','0010_auto_20161225_0642','2016-12-25 06:42:28.292807'),(36,'people','0011_author2_address','2016-12-25 06:44:44.577551'),(37,'Iserlab','0008_auto_20161225_0653','2016-12-25 06:53:32.355214'),(38,'people','0012_remove_author2_address','2016-12-25 06:53:33.115964'),(39,'Iserlab','0009_auto_20161225_0655','2016-12-25 06:55:38.472680'),(40,'Iserlab','0010_auto_20161225_0710','2016-12-25 07:10:33.504826'),(41,'people','0013_auto_20161225_0710','2016-12-25 07:10:34.123681'),(42,'Iserlab','0011_auto_20161225_0858','2016-12-25 08:58:48.158807'),(43,'Iserlab','0012_auto_20161226_0910','2016-12-26 09:10:57.924944'),(44,'Iserlab','0013_auto_20161227_0401','2016-12-27 04:01:23.574476'),(45,'Iserlab','0014_auto_20161227_0407','2016-12-27 04:07:23.377570'),(46,'Iserlab','0015_auto_20161227_0418','2016-12-27 04:18:12.195184'),(47,'Iserlab','0016_experiment_exp_image_count','2016-12-27 04:30:15.558873'),(48,'Iserlab','0017_auto_20161227_0815','2016-12-27 08:15:42.218679'),(49,'Iserlab','0018_auto_20161230_0241','2016-12-30 02:41:51.506625'),(50,'Iserlab','0019_auto_20161230_0244','2016-12-30 02:44:29.586913'),(51,'Iserlab','0020_auto_20161230_0516','2016-12-30 05:16:09.194820'),(52,'Iserlab','0021_auto_20161230_0538','2016-12-30 05:38:44.924412'),(53,'Iserlab','0022_network_subnet_id','2016-12-30 06:09:06.889201'),(54,'Iserlab','0023_auto_20161230_0637','2016-12-30 06:37:36.325424'),(55,'Iserlab','0024_auto_20161230_0706','2016-12-30 07:06:57.555768'),(56,'Iserlab','0025_auto_20170103_0709','2017-01-03 07:10:48.302645'),(57,'Iserlab','0026_remove_user_role','2017-01-03 07:10:48.863586'),(58,'Iserlab','0027_auto_20170103_0712','2017-03-01 07:10:22.363433'),(59,'Iserlab','0028_expinstance_creator','2017-03-01 07:10:23.042351'),(60,'Iserlab','0029_auto_20170301_0710','2017-03-01 07:10:23.936533'),(61,'blog','0001_initial','2017-03-01 07:35:49.246401'),(62,'Iserlab','0030_auto_20170302_0751','2017-03-02 07:52:00.153336'),(63,'Iserlab','0031_auto_20170302_0756','2017-03-02 07:56:19.692725'),(64,'Iserlab','0032_auto_20170302_0803','2017-03-02 08:03:46.452250'),(65,'Iserlab','0033_auto_20170302_0804','2017-03-02 08:04:40.642325'),(66,'Iserlab','0034_auto_20170302_0809','2017-03-02 08:09:58.003095'),(67,'Iserlab','0035_auto_20170302_0810','2017-03-02 08:10:47.626892'),(68,'Iserlab','0036_auto_20170303_0722','2017-03-03 07:22:53.187749'),(69,'Iserlab','0037_score','2017-03-06 03:30:31.443905'),(70,'Iserlab','0038_score_times','2017-03-06 06:26:36.215722'),(71,'Iserlab','0039_auto_20170306_0637','2017-03-06 06:37:37.219698'),(72,'Iserlab','0040_auto_20170306_0710','2017-03-06 07:10:46.956483'),(73,'Iserlab','0041_auto_20170306_0834','2017-03-06 08:34:26.763869'),(74,'Iserlab','0042_score','2017-03-06 08:35:03.941523'),(75,'Iserlab','0043_score_socre_time','2017-03-06 08:42:11.808612'),(76,'Iserlab','0044_auto_20170306_0956','2017-03-06 09:56:05.979548'),(77,'Iserlab','0045_auto_20170306_1006','2017-03-06 10:07:00.054188'),(78,'Iserlab','0046_auto_20170306_1113','2017-03-06 11:13:03.183483'),(79,'Iserlab','0047_auto_20170306_1113','2017-03-06 11:13:37.167959'),(80,'Iserlab','0048_auto_20170307_0141','2017-03-07 01:41:57.300011'),(81,'Iserlab','0049_auto_20170307_0158','2017-03-07 01:59:04.125434'),(82,'Iserlab','0050_auto_20170307_0316','2017-03-07 03:16:37.954179'),(83,'Iserlab','0051_auto_20170307_0325','2017-03-07 03:26:01.313319'),(84,'Iserlab','0052_auto_20170307_0331','2017-03-07 03:31:22.970159'),(85,'Iserlab','0053_auto_20170307_0932','2017-03-07 09:32:16.206291'),(86,'Iserlab','0054_score_delivery_id','2017-03-08 01:45:58.218440'),(87,'Iserlab','0055_score_starttime','2017-03-08 03:23:19.279248'),(88,'Iserlab','0056_auto_20170308_0329','2017-03-08 03:29:10.105048'),(89,'Iserlab','0057_auto_20170308_0804','2017-03-08 08:04:37.029774'),(90,'Iserlab','0058_auto_20170308_0819','2017-03-08 08:19:37.126110'),(91,'Iserlab','0059_auto_20170308_0845','2017-03-08 08:45:16.167101'),(92,'Iserlab','0060_delivery_update_time','2017-03-08 09:15:15.233325'),(93,'Iserlab','0061_auto_20170309_1031','2017-03-09 10:31:18.330382');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('4gykefmzl3ccgzim35i9jqos7id4z6ts','ZTBmZTM2MTU3ODc2NmY3NTkyNDk4NmM3MjQ1N2MxMzQ5Y2ExYWMzODp7InVzZXJuYW1lIjoiMTExIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJkZWxpdmVyeV9pZCI6IjIwIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJyb2xlIjoidGVhY2hlciIsIl9hdXRoX3VzZXJfaGFzaCI6ImJjMjIwYmZkY2RiZDY0ZjFiOTEzNmM1OTM2YTJjNTI0MTExYjdmZjkifQ==','2017-03-24 01:42:43.352945'),('glhxqmsli4w3dtmi3txgh8bfoo4i5ist','MjdhODRjMmQxNTkwODQ1NmNjMzFkOWNkNDExNmVkOWE4N2FlN2NkMTp7Il9hdXRoX3VzZXJfaGFzaCI6ImJjMjIwYmZkY2RiZDY0ZjFiOTEzNmM1OTM2YTJjNTI0MTExYjdmZjkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2017-01-11 09:30:17.453955'),('wawvqtkfds7e45qdvm1f13eslm1acuvf','MjdhODRjMmQxNTkwODQ1NmNjMzFkOWNkNDExNmVkOWE4N2FlN2NkMTp7Il9hdXRoX3VzZXJfaGFzaCI6ImJjMjIwYmZkY2RiZDY0ZjFiOTEzNmM1OTM2YTJjNTI0MTExYjdmZjkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-12-28 03:29:39.156302'),('z86e1imqsgcl37nqudn5l2v058u5fkrv','ZGU5OTVjMWY0NzZmYzVkMzJlZGYxZTE5MmQzMzI0OWE1NzlkOTYwNjp7InVzZXJuYW1lIjoiMTExIiwicm9sZSI6InRlYWNoZXIifQ==','2017-03-23 09:29:11.265020');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_article`
--

DROP TABLE IF EXISTS `people_article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(30) NOT NULL,
  `content` longtext NOT NULL,
  `score` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `people_article_4f331e2f` (`author_id`),
  CONSTRAINT `people_article_author_id_aed44ecc_fk_people_author_id` FOREIGN KEY (`author_id`) REFERENCES `people_author` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_article`
--

LOCK TABLES `people_article` WRITE;
/*!40000 ALTER TABLE `people_article` DISABLE KEYS */;
/*!40000 ALTER TABLE `people_article` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_article_tags`
--

DROP TABLE IF EXISTS `people_article_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_article_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `people_article_tags_article_id_645d8ba7_uniq` (`article_id`,`tag_id`),
  KEY `people_article_tags_tag_id_5201adec_fk_people_tag_id` (`tag_id`),
  CONSTRAINT `people_article_tags_article_id_1fa1328f_fk_people_article_id` FOREIGN KEY (`article_id`) REFERENCES `people_article` (`id`),
  CONSTRAINT `people_article_tags_tag_id_5201adec_fk_people_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `people_tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_article_tags`
--

LOCK TABLES `people_article_tags` WRITE;
/*!40000 ALTER TABLE `people_article_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `people_article_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_author`
--

DROP TABLE IF EXISTS `people_author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_author` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `qq` varchar(10) NOT NULL,
  `addr` longtext NOT NULL,
  `email` varchar(254) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_author`
--

LOCK TABLES `people_author` WRITE;
/*!40000 ALTER TABLE `people_author` DISABLE KEYS */;
/*!40000 ALTER TABLE `people_author` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_author2`
--

DROP TABLE IF EXISTS `people_author2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_author2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(40) NOT NULL,
  `email` varchar(254) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_author2`
--

LOCK TABLES `people_author2` WRITE;
/*!40000 ALTER TABLE `people_author2` DISABLE KEYS */;
INSERT INTO `people_author2` VALUES (1,'shanshan','Lu','lss@163.com'),(2,'Chenyi','Ma',''),(3,'Garming','Chen','555555@qq.com'),(4,'Daniel','Lee','423232@qq.com'),(5,'Mark','Blue','fds23@gmail.com');
/*!40000 ALTER TABLE `people_author2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_blog`
--

DROP TABLE IF EXISTS `people_blog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_blog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(256) NOT NULL,
  `content` longtext NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `author` varchar(256),
  `type` varchar(256),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_blog`
--

LOCK TABLES `people_blog` WRITE;
/*!40000 ALTER TABLE `people_blog` DISABLE KEYS */;
INSERT INTO `people_blog` VALUES (1,'hello world','this is a hello world test passage!','2016-12-14 03:30:36.363435','2016-12-14 03:30:36.363462',NULL,NULL),(2,'iserlab','welcome to our platform!','2016-12-14 03:30:50.295207','2016-12-14 07:25:46.918492','wan','xiaoshuo'),(3,'1112323123','efdasgff dsfadsssssssgfdgdfgdgdg','2016-12-14 03:31:02.644222','2016-12-14 06:24:35.851542','mcy','suibi'),(4,'errererer','ddfasdfssss23242424','2016-12-14 07:37:45.231231','2016-12-14 07:37:45.231250','lyj','poet');
/*!40000 ALTER TABLE `people_blog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_book`
--

DROP TABLE IF EXISTS `people_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `publication_date` date DEFAULT NULL,
  `publisher_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `people_book_2604cbea` (`publisher_id`),
  CONSTRAINT `people_book_publisher_id_041fb2c0_fk_people_publisher_id` FOREIGN KEY (`publisher_id`) REFERENCES `people_publisher` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_book`
--

LOCK TABLES `people_book` WRITE;
/*!40000 ALTER TABLE `people_book` DISABLE KEYS */;
INSERT INTO `people_book` VALUES (1,'django book','2016-12-25',1),(2,'Java coding','2016-12-27',1),(3,'Python core coding','2013-04-01',2),(4,'Think in C++','2011-10-01',1);
/*!40000 ALTER TABLE `people_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_book_authors`
--

DROP TABLE IF EXISTS `people_book_authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_book_authors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) NOT NULL,
  `author2_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `people_book_authors_book_id_42791a08_uniq` (`book_id`,`author2_id`),
  KEY `people_book_authors_author2_id_eac793ed_fk_people_author2_id` (`author2_id`),
  CONSTRAINT `people_book_authors_author2_id_eac793ed_fk_people_author2_id` FOREIGN KEY (`author2_id`) REFERENCES `people_author2` (`id`),
  CONSTRAINT `people_book_authors_book_id_3d8aa3ec_fk_people_book_id` FOREIGN KEY (`book_id`) REFERENCES `people_book` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_book_authors`
--

LOCK TABLES `people_book_authors` WRITE;
/*!40000 ALTER TABLE `people_book_authors` DISABLE KEYS */;
INSERT INTO `people_book_authors` VALUES (1,1,1),(2,2,1),(5,2,3),(3,3,2),(4,4,3);
/*!40000 ALTER TABLE `people_book_authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_person`
--

DROP TABLE IF EXISTS `people_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `age` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_person`
--

LOCK TABLES `people_person` WRITE;
/*!40000 ALTER TABLE `people_person` DISABLE KEYS */;
INSERT INTO `people_person` VALUES (1,'ma','chenyi',24),(2,'wan','kaiyuan',25);
/*!40000 ALTER TABLE `people_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_publisher`
--

DROP TABLE IF EXISTS `people_publisher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_publisher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(60) NOT NULL,
  `state_province` varchar(30) NOT NULL,
  `country` varchar(50) NOT NULL,
  `website` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_publisher`
--

LOCK TABLES `people_publisher` WRITE;
/*!40000 ALTER TABLE `people_publisher` DISABLE KEYS */;
INSERT INTO `people_publisher` VALUES (1,'Addison-Wesley','75 Arlington Street','Boston','MA','U.S.A.','http://www.apress.com/'),(2,'O\'Reilly','10 Fawcett St.','Cambridge','MA','U.S.A.','http://www.oreilly.com/');
/*!40000 ALTER TABLE `people_publisher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_tag`
--

DROP TABLE IF EXISTS `people_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_tag`
--

LOCK TABLES `people_tag` WRITE;
/*!40000 ALTER TABLE `people_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `people_tag` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-10 10:15:12
