-- Drop any if already present
drop table if exists OrderItems CASCADE;
drop table if exists Orders CASCADE;
drop table if exists Customers CASCADE;
drop table if exists Books CASCADE;
drop table if exists Category CASCADE;
drop table if exists Author CASCADE;
drop table if exists Publisher CASCADE;


-- Create the Tables

Create table Publisher(
    Publisher_id varchar(3) primary key,
    Pub_Name varchar(124) not null,
    Headquarter varchar(24) not null,
    Phone varchar(10) not null
);

--Publisher
INSERT INTO Publisher(Publisher_id,Pub_Name,Headquarter,Phone) VALUES ('P01','Penguin House','New York','8901234567');
INSERT INTO Publisher(Publisher_id,Pub_Name,Headquarter,Phone) VALUES ('P02','Macmillan','Dallas','8921671098');
INSERT INTO Publisher(Publisher_id,Pub_Name,Headquarter,Phone) VALUES ('P03','Scholastic','Charlotte','7623458901');
INSERT INTO Publisher(Publisher_id,Pub_Name,Headquarter,Phone) VALUES ('P04','Kensington','Florida','9560330400');
INSERT INTO Publisher(Publisher_id,Pub_Name,Headquarter,Phone) VALUES ('P05','B&H Publishing House','Dallas','9013987149');


Create table Author(
    Author_id varchar(4) primary key,
    Last_Name varchar(24) not null,
    First_Name varchar(24) not null
);

--Author
INSERT INTO Author(Author_id,Last_Name,First_Name) VALUES ('AU01','Christie','Agatha');
INSERT INTO Author(Author_id,Last_Name,First_Name) VALUES ('AU02','Rowling','J. K.');
INSERT INTO Author(Author_id,Last_Name,First_Name) VALUES ('AU03','Shakespeare','William');
INSERT INTO Author(Author_id,Last_Name,First_Name) VALUES ('AU04','Sparks','Nicholas');
INSERT INTO Author(Author_id,Last_Name,First_Name) VALUES ('AU05','Green','John');
INSERT INTO Author(Author_id,Last_Name,First_Name) VALUES ('AU06','Herbert','Frank');
INSERT INTO Author(Author_id,Last_Name,First_Name) VALUES ('AU07','Collins','Suzanne');
INSERT INTO Author(Author_id,Last_Name,First_Name) VALUES ('AU08','Crichton','Michael');
INSERT INTO Author(Author_id,Last_Name,First_Name) VALUES ('AU09','Kardashian','Khloe');
INSERT INTO Author(Author_id,Last_Name,First_Name) VALUES ('AU10','Smith','William');
INSERT INTO Author(Author_id,Last_Name,First_Name) VALUES ('AU11','Tyson','Neil');
INSERT INTO Author(Author_id,Last_Name,First_Name) VALUES ('AU12','Kuhn','Karl');
INSERT INTO Author(Author_id,Last_Name,First_Name) VALUES ('AU13','Rovelli','Carlo');

Create table Category(
    Category_id varchar(3) primary key,
    Category_name varchar(24) not null
);

--Category
INSERT INTO Category(Category_id,Category_name) VALUES ('PHY','Physics');
INSERT INTO Category(Category_id,Category_name) VALUES ('ENT','Entertainment');
INSERT INTO Category(Category_id,Category_name) VALUES ('SFI','Science Fiction');
INSERT INTO Category(Category_id,Category_name) VALUES ('FIC','Fiction');
INSERT INTO Category(Category_id,Category_name) VALUES ('ROM','Romance');


Create table Books(
    ISBN varchar(50) primary key,
    Author_id varchar(4) not null,
    Title varchar(300) not null,
    PublishDate date not null,
    Publisher_id varchar(3) not null,
    Price integer not null,
    Category_id varchar(3) not null,
    foreign key (Publisher_id) references Publisher(Publisher_id),
    foreign key (Category_id) references Category(Category_id),
    foreign key (Author_id) references Author(Author_id)
);

-- Books
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-2901-3184-7','AU03','Romeo and Juliet','1897-09-13','P01',34,'ROM');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-5743-0759-1','AU05','The Fault in Our Stars','2012-01-10','P04',29,'ROM');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-1341-0425-0','AU04','The Notebook','1996-10-01','P01',99,'ROM');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-3558-8408-9','AU06','Dune','1965-08-06','P01',29,'SFI');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-5900-4190-8','AU07','The Hunger Games','2008-09-12','P03',49,'SFI');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-4895-4548-3','AU08','State of Fear','2004-12-07','P03',20,'SFI');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-1820-8894-4','AU08','The Rising Sun','1992-01-27','P01',123,'SFI');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-8139-6106-8','AU01','Murder on the Orient Express','1934-01-24','P04',45,'FIC');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-6664-4477-3','AU02','Harry Potter and the Prisoner of Azkaban','1999-06-08','P02',50,'FIC');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-6744-2294-5','AU02','Harry Potter and the Order of Phoenix','2003-05-21','P03',89,'FIC');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-2906-9429-9','AU13','The Order of Time','2017-05-25','P02',125,'PHY');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-6420-1674-7','AU12','Basic Physics','1996-04-12','P02',23,'PHY');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-7805-3256-2','AU11','Astrophysics for People in a Hurry','2017-05-02','P03',13,'PHY');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-2379-7100-3','AU11','Cosmic Queries','2019-03-02','P03',33,'PHY');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-5301-5439-0','AU09','Dollhouse','2018-01-29','P01',132,'ENT');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-3427-6907-3','AU10','Will','2021-11-06','P02',167,'ENT');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('0-9900-9293-3','AU09','Kardashian Konfidential','2020-11-01','P04',80,'ENT');
INSERT INTO Books(ISBN,Author_id,Title,PublishDate,Publisher_id,Price,Category_id) VALUES ('1-2313-0981-1','AU02','Harry Potter and the Castle of Doom','2009-12-17','P01',53,'FIC');


Create table Customers(
    Customer_id varchar(3) primary key,
    Customer_Last_Name varchar(124) not null,
    Customer_First_Name varchar(124) not null,
    City varchar(30) not null,
    State varchar(2) not null,
    Zip integer not null
);

--Customers
INSERT INTO Customers(Customer_id,Customer_Last_Name,Customer_First_Name,City,State,Zip) VALUES ('C01','Scherbatsky','Robin','Los Angeles','CA',90005);
INSERT INTO Customers(Customer_id,Customer_Last_Name,Customer_First_Name,City,State,Zip) VALUES ('C02','Stinson','Barney','New York','NY',11219);
INSERT INTO Customers(Customer_id,Customer_Last_Name,Customer_First_Name,City,State,Zip) VALUES ('C03','Aldrin','Lily','Austin','TX',43112);
INSERT INTO Customers(Customer_id,Customer_Last_Name,Customer_First_Name,City,State,Zip) VALUES ('C04','Eriksen','Marshall','Seattle','WA',98104);
INSERT INTO Customers(Customer_id,Customer_Last_Name,Customer_First_Name,City,State,Zip) VALUES ('C05','Lane','Robert','Buffalo','NY',12109);
INSERT INTO Customers(Customer_id,Customer_Last_Name,Customer_First_Name,City,State,Zip) VALUES ('C06','Mosby','Ted','Hampton','VA',76123);
INSERT INTO Customers(Customer_id,Customer_Last_Name,Customer_First_Name,City,State,Zip) VALUES ('C07','Pierson','Zoey','Boston','MA',12127);

create table Orders(
    Order_id varchar(3) primary key,
    Customer_id varchar(3) not null,
    OrderDate date not null,
    ShipDate date,
    ShipStreet varchar(124) not null,
    ShipCity varchar(24) not null,
    ShipState varchar(2) not null,
    ShipZip integer not null,
    ShipCost integer not null,
    foreign key (Customer_id) references Customers(Customer_id)
);

-- Orders
INSERT INTO Orders(Order_id,Customer_id,OrderDate,ShipDate,ShipStreet,ShipCity,ShipState,ShipZip,ShipCost) VALUES (1,'C04','2018-01-29','2018-02-02','Jackson Boulevard','Jersey City','NJ',11219,9);
INSERT INTO Orders(Order_id,Customer_id,OrderDate,ShipDate,ShipStreet,ShipCity,ShipState,ShipZip,ShipCost) VALUES (2,'C06','2009-10-10','2010-01-29','Reddington Avenue','Buffalo','NY',11056,3);
INSERT INTO Orders(Order_id,Customer_id,OrderDate,ShipDate,ShipStreet,ShipCity,ShipState,ShipZip,ShipCost) VALUES (3,'C03','2021-12-03',NULL,'5th Street','Austin','TX',43112,12);
INSERT INTO Orders(Order_id,Customer_id,OrderDate,ShipDate,ShipStreet,ShipCity,ShipState,ShipZip,ShipCost) VALUES (4,'C02','2019-04-05','2019-10-01','Broadway','Los Angeles','CA',90005,18);
INSERT INTO Orders(Order_id,Customer_id,OrderDate,ShipDate,ShipStreet,ShipCity,ShipState,ShipZip,ShipCost) VALUES (5,'C01','2021-12-28',NULL,'9th Avenue','Los Angeles','CA',90005,18);
INSERT INTO Orders(Order_id,Customer_id,OrderDate,ShipDate,ShipStreet,ShipCity,ShipState,ShipZip,ShipCost) VALUES (6,'C07','2020-12-31','2021-07-09','Myrtle Avenue','Hampton','VA',76123,9);
INSERT INTO Orders(Order_id,Customer_id,OrderDate,ShipDate,ShipStreet,ShipCity,ShipState,ShipZip,ShipCost) VALUES (7,'C05','2021-09-23','2022-03-28','Bleecker Street','Brooklyn','NY',12109,15);

create table OrderItems(
    Order_id varchar(3),
    Item_id varchar(3),
    ISBN varchar(50) not null,
    Quantity integer not null,
    Price_Per_Item integer not null,
    primary key(Order_id,Item_id),
    foreign key (ISBN) references Books(ISBN)
);

-- OrderItems
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (1,1,'0-5743-0759-1',2,58);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (1,2,'0-2906-9429-9',1,120);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (2,1,'0-3558-8408-9',1,25);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (3,1,'0-9900-9293-3',1,80);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (3,2,'0-5301-5439-0',1,130);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (3,3,'0-6664-4477-3',1,50);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (3,4,'0-6744-2294-5',1,89);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (4,1,'0-1341-0425-0',1,95);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (4,2,'0-2379-7100-3',1,30);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (4,3,'0-2901-3184-7',1,32);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (4,4,'0-1341-0425-0',1,99);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (4,5,'0-6664-4477-3',2,100);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (5,1,'0-5743-0759-1',2,58);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (5,2,'0-3427-6907-3',1,165);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (5,3,'0-6664-4477-3',2,100);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (5,4,'0-8139-6106-8',1,45);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (6,1,'0-8139-6106-8',3,135);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (7,1,'0-6420-1674-7',1,23);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (7,2,'0-7805-3256-2',2,10);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (7,3,'0-2379-7100-3',1,30);
INSERT INTO OrderItems(Order_id,Item_id,ISBN,Quantity,Price_Per_Item) VALUES (7,4,'0-6664-4477-3',1,50);








