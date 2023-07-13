create database  UniversityLibraryManagement;

CREATE TABLE Admin (
  AdminID int identity(1,1),
  Password varchar(30) not null,
  Username varchar(30)not null,
  PRIMARY KEY (AdminID)
);

CREATE TABLE Category (
  CategoryID int identity(1,1),
  CategoryName varchar(50) not null,
  PRIMARY KEY (CategoryID)
);

CREATE TABLE Student (
  StudentID int identity(1,1),
  Username varchar(30) not null,
  Password varchar(30) not null,
  Email varchar(50) not null,
  Phone varchar(11) not null,
  PRIMARY KEY (StudentID)
);


CREATE TABLE Book (
  ISBN int,
  Title varchar(50) not null,
  Author varchar(50) not null,
  PublicationYear int not null,
  Quantity int not null,
  categoryID int ,
  PRIMARY KEY (ISBN),
  constraint book_category_FK foreign key (categoryID) references Category(categoryID)
);



CREATE TABLE BorrowedBook (
  BookID int ,
  StudentID int,
  BorrowDate Date not null,
  ReturnDate Date not null,
  PRIMARY KEY (BookID, StudentID),
  constraint Book_Borrowed_FK FOREIGN KEY (BookID) REFERENCES Book(ISBN),
  constraint student_Borrowed_FK FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
);



INSERT INTO Category VALUES ('Thriller');
INSERT INTO Category VALUES ('Romance');
INSERT INTO Category VALUES ('Science Fiction');
INSERT INTO Category VALUES ('Mystery');
INSERT INTO Category VALUES ('Fantasy');
INSERT INTO Category VALUES ('Biography');
INSERT INTO Category VALUES ('Historical Fiction');
INSERT INTO Category VALUES ('Self-Help');
INSERT INTO Category VALUES ('Horror');
INSERT INTO Category VALUES ('Comedy');
INSERT INTO Category VALUES ('Drama');
INSERT INTO Category VALUES ('Adventure');
INSERT INTO Category VALUES ('Fantasy');
INSERT INTO Category VALUES ('Science');
INSERT INTO Category VALUES ('Comics');
INSERT INTO Category VALUES ('Cooking');
INSERT INTO Category VALUES ('Travel');
INSERT INTO Category VALUES ('History');
INSERT INTO Category VALUES ('Sports');
INSERT INTO Category VALUES ('Art');
INSERT INTO Category VALUES ('Music');
INSERT INTO Category VALUES ('Education');
INSERT INTO Category VALUES ('Technology');
INSERT INTO Category VALUES ('Business');



-- Book.sql

-- Book 1
INSERT INTO Book VALUES ('971', 'The Thrilling Adventure', 'John Smith', '2022', 10, 1);

-- Book 2
INSERT INTO Book VALUES ('975902', 'A Love Story', 'Emily Johnson', '2021', 5, 2);

-- Book 3
INSERT INTO Book VALUES ('45552', 'Galactic Odyssey', 'Robert Adams', '2020', 8, 3);

-- Book 4
INSERT INTO Book VALUES ('9786704', 'The Mysterious Case', 'Sarah Thompson', '2019', 3, 4);

-- Book 7
INSERT INTO Book VALUES ('978535', 'Realm of Magic', 'Michael Anderson', '2023', 12, 5);

-- Book 6
INSERT INTO Book VALUES ('978346', 'The Remarkable Life', 'Jennifer Davis', '2018', 6, 6);

-- Book 7
INSERT INTO Book VALUES ('4757', 'Historical Chronicles', 'David Wilson', '2017', 9, 7);

-- Book 8
INSERT INTO Book VALUES ('978868', 'Self-Help Guide', 'Amy Roberts', '2021', 7, 8);

-- Book 9
INSERT INTO Book VALUES ('9789679', 'Tales of Horror', 'Thomas Miller', '2022', 4, 9);

-- Book 10
INSERT INTO Book VALUES ('978780', 'Comedy Nights', 'Jessica Brown', '2020', 2, 10);

-- Book 11
INSERT INTO Book VALUES ('978891', 'Action Packed', 'Daniel Thompson', '2023', 11, 11);

-- Book 12
INSERT INTO Book VALUES ('978202', 'Drama Unleashed', 'Sophia Anderson', '2019', 8, 12);

-- Book 13
INSERT INTO Book VALUES ('978313', 'The Culinary Journey', 'Alex Martin', '2021', 5, 13);

-- Book 14
INSERT INTO Book VALUES ('2452', 'Wanderlust', 'Olivia Parker', '2020', 7, 14);

-- Book 15
INSERT INTO Book VALUES ('4545', 'The History Book', 'William Davis', '2018', 3, 15);

-- Book 16
INSERT INTO Book VALUES ('972346', 'The Art of Music', 'Sarah Johnson', '2022', 6, 1);

-- Book 17
INSERT INTO Book VALUES ('973457', 'Science Explorations', 'Michael Thompson', '2021', 9, 2);

-- Book 18
INSERT INTO Book VALUES ('973568', 'Comics Galore', 'Emily Davis', '2020', 4, 3);

-- Book 19
INSERT INTO Book VALUES ('9734579', 'Cooking Delights', 'Daniel Wilson', '2019', 7, 4);

-- Book 20
INSERT INTO Book VALUES ('9756780', 'Travel Adventures', 'Jessica Martin', '2023', 3, 5);



-- Student.sql

-- Student 1
INSERT INTO Student VALUES ('johnsmith', 'password123', 'johnsmith@example.com', '01234567890');

-- Student 2
INSERT INTO Student VALUES ('emilyj', 'emily456', 'emilyj@example.com', '01112233445');

-- Student 3
INSERT INTO Student VALUES ('robertadams', 'pass1234', 'robertadams@example.com', '01998877665');

-- Student 4
INSERT INTO Student VALUES ('sarahthompson', 'sarahpass', 'sarahthompson@example.com', '01076543210');

-- Student 5
INSERT INTO Student VALUES ('michaela', 'michaelpassword', 'michaela@example.com', '01543210987');


-- Student 6
INSERT INTO Student VALUES ('jenniferd', 'jenniferpass', 'jenniferd@example.com', '01234567891');

-- Student 7
INSERT INTO Student VALUES ('davidw', 'david123', 'davidw@example.com', '01112233446');

-- Student 8
INSERT INTO Student VALUES ('amyroberts', 'amy456', 'amyroberts@example.com', '01998877666');

-- Student 9
INSERT INTO Student VALUES ('thomasm', 'thomaspwd', 'thomasm@example.com', '01076543211');

-- Student 10
INSERT INTO Student VALUES ('jessicabrown', 'jessicapass', 'jessicabrown@example.com', '01543210988');

-- Student 11
INSERT INTO Student VALUES ('danielth', 'danielpassword', 'danielth@example.com', '01234567892');

-- Student 12
INSERT INTO Student VALUES ('sophiaa', 'sophiapass', 'sophiaa@example.com', '01112233447');

-- Student 13
INSERT INTO Student VALUES ('alexmartin', 'alex567', 'alexmartin@example.com', '01998877667');

-- Student 14
INSERT INTO Student VALUES ('oliviap', 'oliviapass', 'oliviap@example.com', '01076543212');

-- Student 15
INSERT INTO Student VALUES ('williamdavis', 'williampwd', 'williamdavis@example.com', '01543210989');


-- Insert statements
INSERT INTO BorrowedBook 
VALUES
  (978891, 13, '2023-05-18', '2023-05-26');

INSERT INTO BorrowedBook 
VALUES
  (978891, 2, '2023-05-23', '2023-06-06');

INSERT INTO BorrowedBook 
VALUES
  (978891, 1, '2023-05-22', '2023-06-02');

INSERT INTO BorrowedBook 
VALUES
  (971, 3, '2023-05-19', '2023-05-22');

INSERT INTO BorrowedBook 
VALUES
  (978868, 11, '2023-05-21', '2023-06-03');

INSERT INTO BorrowedBook 
VALUES
  (9786704, 14, '2023-05-20', '2023-05-28');

INSERT INTO BorrowedBook 
VALUES
  (9786704, 13, '2023-05-18', '2023-05-29');

INSERT INTO BorrowedBook 
VALUES
  (4757, 15, '2023-05-22', '2023-06-04');

INSERT INTO BorrowedBook 
VALUES
  (978346, 15, '2023-05-21', '2023-06-01');

INSERT INTO BorrowedBook 
VALUES
  (4757, 11, '2023-05-20', '2023-05-30');

INSERT INTO BorrowedBook 
VALUES
  (978535, 14, '2023-05-17', '2023-05-27');

INSERT INTO BorrowedBook 
VALUES
  (978535, 15, '2023-05-19', '2023-05-31');

INSERT INTO BorrowedBook 
VALUES
  (978202, 8, '2023-05-18', '2023-05-28');

  select * from Student