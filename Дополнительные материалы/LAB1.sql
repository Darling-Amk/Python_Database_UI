-- �������� ������ 22203 �4
USE master
GO
-- �������� ���� ������ Treatment
IF NOT EXISTS (
	SELECT name 
	FROM sys.databases 
	WHERE name  = N'Treatment'
)
CREATE DATABASE [Treatment]
GO
--������������ ���� ��
USE [Treatment]

GO
-- �������� ������� tblPatient
CREATE TABLE tblPatient
(
	intPatientId INT NOT NULL PRIMARY KEY IDENTITY(1,1), --������������� ��������
	txtPatientSurname [NVARCHAR](30) NOT NULL, --������� ��������
	txtPatientName [NVARCHAR](25) NOT NULL, --��� ��������
	txtPatientSecondName [NVARCHAR](30) NOT NULL, --�������� ��������
	datBirthday [DATE] NOT NULL, --���� ��������	txtAddress [NVARCHAR](100) NOT NULL, --����� ����������
);
GO
-- �������� ������� tblDoctor
GO
CREATE TABLE tblDoctor
(
	intDoctorId INT NOT NULL PRIMARY KEY IDENTITY(1,1), --������������� �������
	txtDoctorName [NVARCHAR](150) NOT NULL, --��� �������	txtSpecialist [NVARCHAR](35) NOT NULL, --�������������	datDoctorWork [DATE] NOT NULL, --���� ������ �� ������
);
GO
-- �������� ������� tblTreatmentType
GO
CREATE TABLE  tblTreatmentType
(
	intTreatmentTypeId  INT NOT NULL PRIMARY KEY IDENTITY(1,1), --������������� ���� ���������
	txtTreatmentTypeName  [NVARCHAR](100) NOT NULL, --�������� ���� ���������	txtTreatmentTypeDescription  [NVARCHAR](255) NOT NULL, --�������� ���� ���������	fltTreatmentPrice  DECIMAL(10,2) NOT NULL, --���������
);
GO
-- �������� ������� tblTreatmentSet
GO
CREATE TABLE  tblTreatmentSet
(
	intTreatmentSetId  INT NOT NULL PRIMARY KEY IDENTITY(1,1), --������������� ���������� ����� ��������
	intDoctorId INT REFERENCES tblDoctor(intDoctorId) ON UPDATE CASCADE ON DELETE NO ACTION NOT NULL, -- ������
	intPatientId INT REFERENCES tblPatient(intPatientId) ON UPDATE CASCADE ON DELETE NO ACTION NOT NULL, -- �������
	datDateBegin DATE NOT NULL, -- ���� ������ �����
	datDateEnd DATE NOT NULL, -- ���� ��������� �����	txtTreatmentSetRoom [NVARCHAR](5) NOT NULL, -- �������	intTreatmentSetCount INT  NOT NULL, -- ���������� ����������� ��������	intTreatmentSetCountFact INT NOT NULL, --���������� ����������� ��������	intTreatmentTypeId INT REFERENCES tblTreatmentType(intTreatmentTypeId) ON UPDATE CASCADE ON DELETE NO ACTION NOT NULL, --��� ��������
);
GO
-- �������� ������� tblTreatmentVisit
GO
CREATE TABLE  tblTreatmentVisit
(
	intTreatmentVisitId INT NOT NULL PRIMARY KEY IDENTITY(1,1), --������������� ����������� ���������
	intTreatmentSetId INT REFERENCES tblTreatmentSet(intTreatmentSetId) ON UPDATE CASCADE ON DELETE NO ACTION NOT NULL, --���� ��������	datTreatmentVisitDate DATE NOT NULL, --���� ���������� ���������
)