-- Кручинин Никита 22203 в4
USE master
GO
-- Создание базы данных Treatment
IF NOT EXISTS (
	SELECT name 
	FROM sys.databases 
	WHERE name  = N'Treatment'
)
CREATE DATABASE [Treatment]
GO
--Использовать нашу бд
USE [Treatment]

GO
-- Создание таблицы tblPatient
CREATE TABLE tblPatient
(
	intPatientId INT NOT NULL PRIMARY KEY IDENTITY(1,1), --Идентификатор пациента
	txtPatientSurname [NVARCHAR](30) NOT NULL, --Фамилия пациента
	txtPatientName [NVARCHAR](25) NOT NULL, --Имя пациента
	txtPatientSecondName [NVARCHAR](30) NOT NULL, --Отчество пациента
	datBirthday [DATE] NOT NULL, --Дата рождения	txtAddress [NVARCHAR](100) NOT NULL, --Адрес проживания
);
GO
-- Создание таблицы tblDoctor
GO
CREATE TABLE tblDoctor
(
	intDoctorId INT NOT NULL PRIMARY KEY IDENTITY(1,1), --Идентификатор доктора
	txtDoctorName [NVARCHAR](150) NOT NULL, --ФИО доктора	txtSpecialist [NVARCHAR](35) NOT NULL, --Специальность	datDoctorWork [DATE] NOT NULL, --Дата приема на работу
);
GO
-- Создание таблицы tblTreatmentType
GO
CREATE TABLE  tblTreatmentType
(
	intTreatmentTypeId  INT NOT NULL PRIMARY KEY IDENTITY(1,1), --Идентификатор вида процедуры
	txtTreatmentTypeName  [NVARCHAR](100) NOT NULL, --Название вида процедуры	txtTreatmentTypeDescription  [NVARCHAR](255) NOT NULL, --Описание вида процедуры	fltTreatmentPrice  DECIMAL(10,2) NOT NULL, --Стоимость
);
GO
-- Создание таблицы tblTreatmentSet
GO
CREATE TABLE  tblTreatmentSet
(
	intTreatmentSetId  INT NOT NULL PRIMARY KEY IDENTITY(1,1), --Идентификатор назначений курса процедур
	intDoctorId INT REFERENCES tblDoctor(intDoctorId) ON UPDATE CASCADE ON DELETE NO ACTION NOT NULL, -- Доктор
	intPatientId INT REFERENCES tblPatient(intPatientId) ON UPDATE CASCADE ON DELETE NO ACTION NOT NULL, -- Пациент
	datDateBegin DATE NOT NULL, -- Дата начала курса
	datDateEnd DATE NOT NULL, -- Дата окончания курса	txtTreatmentSetRoom [NVARCHAR](5) NOT NULL, -- Кабинет	intTreatmentSetCount INT  NOT NULL, -- Количество назначенных процедур	intTreatmentSetCountFact INT NOT NULL, --Количество проведенных процедур	intTreatmentTypeId INT REFERENCES tblTreatmentType(intTreatmentTypeId) ON UPDATE CASCADE ON DELETE NO ACTION NOT NULL, --Вид процедур
);
GO
-- Создание таблицы tblTreatmentVisit
GO
CREATE TABLE  tblTreatmentVisit
(
	intTreatmentVisitId INT NOT NULL PRIMARY KEY IDENTITY(1,1), --Идентификатор проведенной процедуры
	intTreatmentSetId INT REFERENCES tblTreatmentSet(intTreatmentSetId) ON UPDATE CASCADE ON DELETE NO ACTION NOT NULL, --Курс процедур	datTreatmentVisitDate DATE NOT NULL, --Дата проведения процедуры
)