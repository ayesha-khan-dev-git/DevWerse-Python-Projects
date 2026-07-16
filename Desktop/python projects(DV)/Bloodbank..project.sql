-- =====================================================
-- COMPLETE BLOOD BANK MANAGEMENT SYSTEM DATABASE
-- Ek hi query mein: Database + Tables + Data + Views
-- =====================================================

-- =====================================================
-- PART 1: DATABASE CREATE KARO
-- =====================================================

-- Pehle master database mein jao
USE master;
GO

-- Agar purana database hai toh delete karo
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'BloodBank_Project')
BEGIN
    ALTER DATABASE BloodBank_Project SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE BloodBank_Project;
END
GO

-- Naya database banao
CREATE DATABASE BloodBank_Project;
GO

-- Naye database mein jao
USE BloodBank_Project;
GO

PRINT '==========================================';
PRINT 'Database "BloodBank_Project" created!';
PRINT '==========================================';
GO

-- =====================================================
-- PART 2: TABLES CREATE KARO
-- =====================================================

PRINT 'Creating tables...';
GO

-- 1. DONORS TABLE
CREATE TABLE DONORS (
    Donor_ID INT IDENTITY(1,1) PRIMARY KEY,
    Donor_Name VARCHAR(100) NOT NULL,
    Father_Name VARCHAR(100),
    Blood_Group VARCHAR(3) NOT NULL,
    Gender VARCHAR(10) CHECK (Gender IN ('Male', 'Female', 'Other')),
    DOB DATE NOT NULL,
    CNIC VARCHAR(15) UNIQUE NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Alternate_Phone VARCHAR(15),
    Address VARCHAR(500),
    City VARCHAR(50),
    Email VARCHAR(100),
    Last_Donation_Date DATE NULL,
    Total_Donations INT DEFAULT 0,
    Eligibility_Status VARCHAR(20) DEFAULT 'ELIGIBLE',
    Registration_Date DATETIME DEFAULT GETDATE(),
    Is_Active BIT DEFAULT 1
);
GO

PRINT '✓ DONORS table created';
GO

-- 2. HOSPITALS TABLE
CREATE TABLE HOSPITALS (
    Hospital_ID INT IDENTITY(1,1) PRIMARY KEY,
    Hospital_Name VARCHAR(200) NOT NULL,
    Registration_No VARCHAR(50) UNIQUE NOT NULL,
    Hospital_Type VARCHAR(50) DEFAULT 'Private',
    City VARCHAR(50),
    Phone VARCHAR(15) NOT NULL,
    Email VARCHAR(100),
    Contact_Person VARCHAR(100),
    Authorized_Status VARCHAR(20) DEFAULT 'PENDING',
    Is_Active BIT DEFAULT 1
);
GO

PRINT '✓ HOSPITALS table created';
GO

-- 3. BLOOD_STOCK TABLE
CREATE TABLE BLOOD_STOCK (
    Bag_ID INT IDENTITY(1,1) PRIMARY KEY,
    Donor_ID INT FOREIGN KEY REFERENCES DONORS(Donor_ID),
    Blood_Group VARCHAR(3) NOT NULL,
    Component_Type VARCHAR(30) DEFAULT 'Whole Blood',
    Quantity_ML INT DEFAULT 450,
    Collection_Date DATE NOT NULL,
    Expiry_Date DATE NOT NULL,
    Inventory_Status VARCHAR(20) DEFAULT 'AVAILABLE',
    Screening_Result VARCHAR(20) DEFAULT 'PENDING'
);
GO

PRINT '✓ BLOOD_STOCK table created';
GO

-- 4. EMERGENCY_REQUESTS TABLE
CREATE TABLE EMERGENCY_REQUESTS (
    Request_ID INT IDENTITY(1,1) PRIMARY KEY,
    Hospital_ID INT FOREIGN KEY REFERENCES HOSPITALS(Hospital_ID),
    Required_Blood_Group VARCHAR(3) NOT NULL,
    Units_Requested INT NOT NULL,
    Urgency_Level VARCHAR(20) DEFAULT 'NORMAL',
    Patient_Name VARCHAR(100),
    Request_Timestamp DATETIME DEFAULT GETDATE(),
    Fulfillment_Status VARCHAR(20) DEFAULT 'PENDING',
    Allocated_Bags INT DEFAULT 0
);
GO

PRINT '✓ EMERGENCY_REQUESTS table created';
GO

-- 5. DONATION_HISTORY TABLE
CREATE TABLE DONATION_HISTORY (
    History_ID INT IDENTITY(1,1) PRIMARY KEY,
    Donor_ID INT FOREIGN KEY REFERENCES DONORS(Donor_ID),
    Donation_Date DATE NOT NULL,
    Volume_ML INT DEFAULT 450,
    Hemoglobin_Level DECIMAL(4,1),
    HIV_Test VARCHAR(20) DEFAULT 'Pending',
    Hepatitis_B_Test VARCHAR(20) DEFAULT 'Pending',
    Status VARCHAR(20) DEFAULT 'Completed'
);
GO

PRINT '✓ DONATION_HISTORY table created';
GO

-- =====================================================
-- PART 3: DATA INSERT KARO
-- =====================================================

PRINT 'Inserting data...';
GO

-- Donors Data (10 donors)
INSERT INTO DONORS (Donor_Name, Father_Name, Blood_Group, Gender, DOB, CNIC, Phone, City, Email, Last_Donation_Date, Total_Donations) VALUES
('Ayesha Khan', 'Ahmed Khan', 'O+', 'Female', '1995-03-15', '35201-1234567-1', '03001234567', 'Lahore', 'ayesha@gmail.com', '2024-10-01', 3),
('Fatima Ali', 'Ali Raza', 'A+', 'Female', '1998-07-22', '35201-2345678-2', '03002345678', 'Karachi', 'fatima@gmail.com', '2024-09-15', 2),
('Sara Ahmed', 'Ahmed Saeed', 'B+', 'Female', '2000-01-10', '35201-3456789-3', '03003456789', 'Islamabad', 'sara@gmail.com', '2024-10-10', 1),
('Usman Chaudhry', 'Mohammad Chaudhry', 'AB+', 'Male', '1992-11-05', '35201-4567890-4', '03004567890', 'Lahore', 'usman@gmail.com', '2024-08-20', 5),
('Hamza Malik', 'Tariq Malik', 'O-', 'Male', '1997-04-18', '35201-5678901-5', '03005678901', 'Rawalpindi', 'hamza@gmail.com', '2024-10-05', 2),
('Zara Tariq', 'Tariq Mehmood', 'A-', 'Female', '1999-09-30', '35201-6789012-6', '03006789012', 'Multan', 'zara@gmail.com', '2024-07-12', 1),
('Omar Farooq', 'Farooq Ahmed', 'B-', 'Male', '1994-12-12', '35201-7890123-7', '03007890123', 'Faisalabad', 'omar@gmail.com', '2024-06-25', 4),
('Hina Naeem', 'Naeem Anwar', 'AB-', 'Female', '1996-05-28', '35201-8901234-8', '03008901234', 'Peshawar', 'hina@gmail.com', '2024-09-01', 2),
('Bilal Akhtar', 'Akhtar Hussain', 'O+', 'Male', '1993-08-17', '35201-9012345-9', '03009012345', 'Quetta', 'bilal@gmail.com', '2024-09-28', 3),
('Sadia Anwar', 'Anwar Ali', 'A+', 'Female', '2001-02-14', '35201-0123456-0', '03000123456', 'Lahore', 'sadia@gmail.com', NULL, 0);
GO

PRINT '✓ 10 Donors inserted';
GO

-- Hospitals Data (5 hospitals)
INSERT INTO HOSPITALS (Hospital_Name, Registration_No, Hospital_Type, City, Phone, Email, Contact_Person, Authorized_Status) VALUES
('Mayo Hospital', 'HOS-001', 'Government', 'Lahore', '04211111111', 'mayo@gmail.com', 'Dr. Ali', 'APPROVED'),
('Jinnah Hospital', 'HOS-002', 'Government', 'Lahore', '04222222222', 'jinnah@gmail.com', 'Dr. Sana', 'APPROVED'),
('Aga Khan Hospital', 'HOS-003', 'Private', 'Karachi', '02133333333', 'agakhan@gmail.com', 'Dr. Farhan', 'APPROVED'),
('Shifa International', 'HOS-004', 'Private', 'Islamabad', '05144444444', 'shifa@gmail.com', 'Dr. Nida', 'APPROVED'),
('CMH Rawalpindi', 'HOS-005', 'Military', 'Rawalpindi', '05155555555', 'cmh@gmail.com', 'Dr. Ahmed', 'APPROVED');
GO

PRINT '✓ 5 Hospitals inserted';
GO

-- Blood Stock Data (20 bags)
INSERT INTO BLOOD_STOCK (Donor_ID, Blood_Group, Collection_Date, Expiry_Date, Inventory_Status, Screening_Result) VALUES
(1, 'O+', '2024-10-01', DATEADD(DAY, 35, '2024-10-01'), 'AVAILABLE', 'CLEAR'),
(2, 'A+', '2024-09-15', DATEADD(DAY, 35, '2024-09-15'), 'AVAILABLE', 'CLEAR'),
(3, 'B+', '2024-10-10', DATEADD(DAY, 35, '2024-10-10'), 'AVAILABLE', 'CLEAR'),
(4, 'AB+', '2024-08-20', DATEADD(DAY, 35, '2024-08-20'), 'EXPIRED', 'CLEAR'),
(5, 'O-', '2024-10-05', DATEADD(DAY, 35, '2024-10-05'), 'AVAILABLE', 'CLEAR'),
(6, 'A-', '2024-07-12', DATEADD(DAY, 35, '2024-07-12'), 'EXPIRED', 'REACTIVE'),
(7, 'B-', '2024-06-25', DATEADD(DAY, 35, '2024-06-25'), 'DISCARDED', 'CLEAR'),
(8, 'AB-', '2024-09-01', DATEADD(DAY, 35, '2024-09-01'), 'AVAILABLE', 'CLEAR'),
(9, 'O+', '2024-09-28', DATEADD(DAY, 35, '2024-09-28'), 'AVAILABLE', 'CLEAR'),
(1, 'O+', '2024-08-15', DATEADD(DAY, 35, '2024-08-15'), 'AVAILABLE', 'CLEAR'),
(2, 'A+', '2024-10-02', DATEADD(DAY, 35, '2024-10-02'), 'AVAILABLE', 'CLEAR'),
(3, 'B+', '2024-09-20', DATEADD(DAY, 35, '2024-09-20'), 'AVAILABLE', 'CLEAR'),
(5, 'O-', '2024-09-10', DATEADD(DAY, 35, '2024-09-10'), 'AVAILABLE', 'CLEAR'),
(8, 'AB-', '2024-08-28', DATEADD(DAY, 35, '2024-08-28'), 'AVAILABLE', 'CLEAR'),
(9, 'O+', '2024-10-12', DATEADD(DAY, 35, '2024-10-12'), 'AVAILABLE', 'PENDING'),
(1, 'O+', '2024-07-20', DATEADD(DAY, 35, '2024-07-20'), 'AVAILABLE', 'CLEAR'),
(2, 'A+', '2024-08-10', DATEADD(DAY, 35, '2024-08-10'), 'AVAILABLE', 'CLEAR'),
(3, 'B+', '2024-10-08', DATEADD(DAY, 35, '2024-10-08'), 'AVAILABLE', 'CLEAR'),
(5, 'O-', '2024-08-25', DATEADD(DAY, 35, '2024-08-25'), 'AVAILABLE', 'CLEAR'),
(4, 'AB+', '2024-07-15', DATEADD(DAY, 35, '2024-07-15'), 'AVAILABLE', 'CLEAR');
GO

PRINT '✓ 20 Blood bags inserted';
GO

-- Emergency Requests Data (8 requests)
INSERT INTO EMERGENCY_REQUESTS (Hospital_ID, Required_Blood_Group, Units_Requested, Urgency_Level, Patient_Name, Request_Timestamp, Fulfillment_Status) VALUES
(1, 'O+', 2, 'EMERGENCY', 'Ahmed Raza', '2024-10-15 09:30:00', 'APPROVED'),
(2, 'A+', 1, 'HIGH', 'Sana Tariq', '2024-10-16 14:20:00', 'APPROVED'),
(3, 'O-', 3, 'EMERGENCY', 'Bilal Ahmed', '2024-10-17 11:00:00', 'PENDING'),
(4, 'B+', 2, 'NORMAL', 'Fatima Khan', '2024-10-18 08:15:00', 'PENDING'),
(1, 'AB+', 1, 'EMERGENCY', 'Usman Ali', '2024-10-18 16:45:00', 'APPROVED'),
(5, 'O+', 2, 'HIGH', 'Hina Naeem', '2024-10-19 10:30:00', 'PENDING'),
(2, 'A-', 1, 'EMERGENCY', 'Omar Farooq', '2024-10-19 13:00:00', 'PENDING'),
(3, 'B-', 2, 'NORMAL', 'Zara Tariq', '2024-10-20 09:00:00', 'PENDING');
GO

PRINT '✓ 8 Emergency requests inserted';
GO

-- Donation History Data
INSERT INTO DONATION_HISTORY (Donor_ID, Donation_Date, Volume_ML, Hemoglobin_Level, HIV_Test, Hepatitis_B_Test) VALUES
(1, '2024-10-01', 450, 13.5, 'NEGATIVE', 'NEGATIVE'),
(2, '2024-09-15', 450, 12.8, 'NEGATIVE', 'NEGATIVE'),
(3, '2024-10-10', 450, 14.0, 'NEGATIVE', 'NEGATIVE'),
(4, '2024-08-20', 450, 13.2, 'NEGATIVE', 'NEGATIVE'),
(5, '2024-10-05', 450, 14.5, 'NEGATIVE', 'NEGATIVE'),
(6, '2024-07-12', 450, 12.0, 'NEGATIVE', 'NEGATIVE'),
(7, '2024-06-25', 450, 13.8, 'NEGATIVE', 'NEGATIVE'),
(8, '2024-09-01', 450, 13.0, 'NEGATIVE', 'NEGATIVE'),
(9, '2024-09-28', 450, 14.2, 'NEGATIVE', 'NEGATIVE'),
(1, '2024-08-15', 450, 13.4, 'NEGATIVE', 'NEGATIVE');
GO

PRINT '✓ Donation history inserted';
GO

-- =====================================================
-- PART 4: INDEXES CREATE KARO (Fast Search Ke Liye)
-- =====================================================

PRINT 'Creating indexes...';
GO

CREATE INDEX idx_blood_group ON BLOOD_STOCK(Blood_Group, Inventory_Status);
GO
CREATE INDEX idx_request_status ON EMERGENCY_REQUESTS(Fulfillment_Status);
GO
CREATE INDEX idx_donor_phone ON DONORS(Phone);
GO

PRINT '✓ Indexes created';
GO

-- =====================================================
-- PART 5: VIEWS CREATE KARO (Reports Ke Liye)
-- =====================================================

PRINT 'Creating views...';
GO

-- View 1: Current Blood Stock
CREATE VIEW vw_BloodStock AS
SELECT 
    Blood_Group,
    COUNT(*) AS Total_Bags,
    SUM(CASE WHEN Inventory_Status = 'AVAILABLE' AND Expiry_Date > GETDATE() THEN 1 ELSE 0 END) AS Available_Bags,
    SUM(CASE WHEN Expiry_Date <= GETDATE() THEN 1 ELSE 0 END) AS Expired_Bags
FROM BLOOD_STOCK
GROUP BY Blood_Group;
GO

-- View 2: Pending Requests
CREATE VIEW vw_PendingRequests AS
SELECT 
    r.Request_ID,
    h.Hospital_Name,
    r.Required_Blood_Group,
    r.Units_Requested,
    r.Urgency_Level,
    r.Patient_Name,
    r.Request_Timestamp
FROM EMERGENCY_REQUESTS r
JOIN HOSPITALS h ON r.Hospital_ID = h.Hospital_ID
WHERE r.Fulfillment_Status = 'PENDING';
GO

-- View 3: Donor Summary
CREATE VIEW vw_DonorSummary AS
SELECT 
    Donor_ID,
    Donor_Name,
    Blood_Group,
    City,
    Total_Donations,
    Last_Donation_Date,
    Eligibility_Status
FROM DONORS;
GO

PRINT '✓ 3 Views created';
GO

-- =====================================================
-- PART 6: STORED PROCEDURES
-- =====================================================

PRINT 'Creating stored procedures...';
GO

-- Procedure 1: Check Blood Stock
CREATE PROCEDURE sp_CheckStock
    @Blood_Group VARCHAR(3) = NULL
AS
BEGIN
    IF @Blood_Group IS NULL
    BEGIN
        SELECT * FROM vw_BloodStock ORDER BY Blood_Group;
    END
    ELSE
    BEGIN
        SELECT * FROM vw_BloodStock WHERE Blood_Group = @Blood_Group;
    END
END;
GO

-- Procedure 2: Process Emergency Request
CREATE PROCEDURE sp_ApproveRequest
    @Request_ID INT
AS
BEGIN
    DECLARE @Required_Group VARCHAR(3);
    DECLARE @Units_Needed INT;
    
    SELECT @Required_Group = Required_Blood_Group, @Units_Needed = Units_Requested
    FROM EMERGENCY_REQUESTS
    WHERE Request_ID = @Request_ID AND Fulfillment_Status = 'PENDING';
    
    IF EXISTS (
        SELECT 1 FROM BLOOD_STOCK 
        WHERE Blood_Group = @Required_Group 
        AND Inventory_Status = 'AVAILABLE' 
        AND Expiry_Date > GETDATE()
        HAVING COUNT(*) >= @Units_Needed
    )
    BEGIN
        UPDATE EMERGENCY_REQUESTS 
        SET Fulfillment_Status = 'APPROVED', Allocated_Bags = @Units_Needed
        WHERE Request_ID = @Request_ID;
        
        UPDATE TOP (@Units_Needed) BLOOD_STOCK
        SET Inventory_Status = 'ALLOCATED'
        WHERE Blood_Group = @Required_Group 
        AND Inventory_Status = 'AVAILABLE'
        AND Expiry_Date > GETDATE();
        
        PRINT 'Request approved!';
    END
    ELSE
    BEGIN
        PRINT 'Insufficient stock available!';
    END
END;
GO

-- Procedure 3: Register New Donor
CREATE PROCEDURE sp_RegisterDonor
    @Name VARCHAR(100),
    @Blood_Group VARCHAR(3),
    @DOB DATE,
    @CNIC VARCHAR(15),
    @Phone VARCHAR(15),
    @City VARCHAR(50)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM DONORS WHERE CNIC = @CNIC OR Phone = @Phone)
    BEGIN
        INSERT INTO DONORS (Donor_Name, Blood_Group, DOB, CNIC, Phone, City)
        VALUES (@Name, @Blood_Group, @DOB, @CNIC, @Phone, @City);
        PRINT 'Donor registered successfully!';
    END
    ELSE
    BEGIN
        PRINT 'Donor already exists!';
    END
END;
GO

PRINT '✓ 3 Stored procedures created';
GO

-- =====================================================
-- PART 7: FINAL VERIFICATION
-- =====================================================

PRINT '==========================================';
PRINT 'FINAL VERIFICATION';
PRINT '==========================================';
GO

-- Check all tables data count
SELECT 'DONORS' AS Table_Name, COUNT(*) AS Total_Records FROM DONORS
UNION ALL
SELECT 'HOSPITALS', COUNT(*) FROM HOSPITALS
UNION ALL
SELECT 'BLOOD_STOCK', COUNT(*) FROM BLOOD_STOCK
UNION ALL
SELECT 'EMERGENCY_REQUESTS', COUNT(*) FROM EMERGENCY_REQUESTS
UNION ALL
SELECT 'DONATION_HISTORY', COUNT(*) FROM DONATION_HISTORY;
GO

-- Show current blood stock
PRINT '==========================================';
PRINT 'CURRENT BLOOD STOCK STATUS';
PRINT '==========================================';
SELECT * FROM vw_BloodStock;
GO

-- Show pending requests
PRINT '==========================================';
PRINT 'PENDING EMERGENCY REQUESTS';
PRINT '==========================================';
SELECT * FROM vw_PendingRequests;
GO

-- Final message
PRINT '==========================================';
PRINT '✅ DATABASE SETUP COMPLETE!';
PRINT '✅ Database Name: BloodBank_Project';
PRINT '✅ Total Tables: 5';
PRINT '✅ Total Views: 3';
PRINT '✅ Total Procedures: 3';
PRINT '✅ Total Donors: 10';
PRINT '✅ Total Hospitals: 5';
PRINT '✅ Total Blood Bags: 20';
PRINT '✅ Total Requests: 8';
PRINT '==========================================';
PRINT '';
PRINT 'You can now:';
PRINT '1. Run: EXEC sp_CheckStock; - to check blood stock';
PRINT '2. Run: EXEC sp_ApproveRequest 3; - to approve request';
PRINT '3. Run: SELECT * FROM vw_PendingRequests; - to see pending requests';
PRINT '==========================================';
GO