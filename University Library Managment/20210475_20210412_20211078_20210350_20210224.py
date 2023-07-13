from datetime import datetime, timedelta
import tkinter as tk
import pyodbc
import re # for regex
from tkinter import ttk
import tkinter.messagebox as messagebox

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

cnxn_str = ("Driver={SQL Server};"
            "Server=DESKTOP-3PAA221;"
            "Database=UniversityLibraryManagement;"
            "Trusted_Connection=yes;")
cnxn = pyodbc.connect(cnxn_str)
my_cursor = cnxn.cursor()

class Book():
    
    def __init__(self,ISBN, Title, Author, PublicationYear , Quantity,categoryID):
        self.Title = Title
        self.Author = Author
        self.categoryID = categoryID
        self.ISBN = ISBN
        self.PublicationYear = PublicationYear
        self.Quantity = Quantity
    

    def show_book_info(self):
        print("ISBN             :" + str(self.ISBN))
        print("Book's title     :" + self.Title)
        print("Book's Author    :" + self.Author)
        print("Publication Year :" + str(self.PublicationYear))
        print("available copies :" + str(self.Quantity))
        print("Book's Category  :" + str(self.categoryID))
        print("\n")

    
    


class User():
    def __init__(self,user_name, password,ID):
        self.user_name = user_name
        self.password = password
        self.ID = ID

    def displayInfo(self):
        print("username     : " + self.user_name)
        print("password     : " + self.password)
        print("ID           : " + str(self.ID))


class Admin(User):
    def __init__(self,user_name, password,ID):
        super().__init__(user_name, password,ID)

    def add_book(self, new_book ,my_cursor):
        my_cursor.execute(f"INSERT INTO Book (ISBN,Title,Author,PublicationYear,Quantity,categoryID) VALUES ('{new_book.ISBN}','{new_book.Title}','{new_book.Author}','{new_book.PublicationYear}','{new_book.Quantity}','{new_book.categoryID}')")
        my_cursor.commit()
    
    # this function has 5 update statments
    def modify_book_details(self , book , my_cursor):
        print("Which field do you want to modify? ")
        print("1- Title")
        print("2- Author")
        print("3- Publication Year")
        print("4- Quantity")
        print("5- Category ID")
        
        choice = int(input("Enter your choice: "))

        if choice == 1:
            new_title = input("Enter new title: ")
            my_cursor.execute(f"UPDATE Book SET Title = '{new_title}' WHERE ISBN = '{book.ISBN}'")

        elif choice == 2:
            new_author = input("Enter new author: ")
            my_cursor.execute(f"UPDATE Book SET Author = '{new_author}' WHERE ISBN = '{book.ISBN}'")

        elif choice == 3:
            new_publication_year = int(input("Enter new publication year: "))
            my_cursor.execute(f"UPDATE Book SET PublicationYear = '{new_publication_year}' WHERE ISBN = '{book.ISBN}'")

        elif choice == 4:
            new_quantity = int(input("Enter new quantity: "))
            if (new_quantity>-1 and new_quantity<2000):
                my_cursor.execute(f"UPDATE Book SET Quantity = '{new_quantity}' WHERE ISBN = '{book.ISBN}'")
            else:
                print("this can't be a real quantity")

        elif choice == 5:
            validate = True
            #  select statment to get all category IDs and verify a new category ID 
            my_cursor.execute("SELECT categoryID FROM category")
            category_ids = [row[0] for row in my_cursor.fetchall()] # pu all IDs in a list

            while validate:
                new_categoryID = int(input("Enter new category ID: "))
                for i in category_ids:
                    if (i==new_categoryID):
                        my_cursor.execute(f"UPDATE Book SET categoryID = '{new_categoryID}' WHERE ISBN = '{book.ISBN}';")
                        my_cursor.commit()
                        print(book.Title + " category has been modified\n")
                        validate = False
                        break
    
                if validate:
                    print("This category doesn't exist.")

        else:
            print("Invalid choice")
    
        
class Student(User):
    def __init__(self, ID, user_name, password ,email , phone):
        super().__init__(user_name, password, ID)
        self.Email = email
        self.Phone = phone
    
    def displayInfo(self):
        super().displayInfo()
        print("email address : " + self.Email)
        print("Phone number  : " + self.Phone)


    
class category():
    def __init__(self,category_id , category_name):
        self.Category_ID = category_id
        self.Category_Name = category_name
    
    def show_categories(self,new_cursor):
        new_cursor.execute(f"select * from category;")
        print("category ID\tcategory name")
        for row in new_cursor:
            print (row[0] +"\t"+ row[1])
        
    
    
class BorrowedBook():
    def __init__(self, book_id, studnet_id,borrowing_date, returning_date):
        self.book_ID = book_id
        self.student_ID = studnet_id
        self.return_date = returning_date
        self.return_date = borrowing_date


    
    def displayInfo(self):
        super().displayInfo()
        print("email address : " + self.Email)
        print("Phone number  : " + self.Phone)

#end classes

def generate_pdf_report():
#  groub by category name and count books in each category
    my_cursor.execute("select CategoryName , count(book.isbn) As books from category inner join book on Category.CategoryID = book.categoryID group by (CategoryName)")
    category_data = my_cursor.fetchall()
        # get most 3 borrowed books from borrow table
    my_cursor.execute("SELECT TOP 3 book.title AS BookTitle, COUNT(book.isbn) AS BorrowCount FROM book inner JOIN BorrowedBook ON book.isbn = BorrowedBook.bookid GROUP BY book.title ORDER BY BorrowCount DESC")
    book_data = my_cursor.fetchall()
    # get top 3 users who borrowed most books
    my_cursor.execute("SELECT TOP 3 student.Username As username, COUNT(book.isbn) AS BorrowCount FROM student LEFT JOIN BorrowedBook ON student.StudentID = BorrowedBook.StudentID LEFT JOIN book ON BorrowedBook.bookid = book.isbn GROUP BY Student.Username ORDER BY BorrowCount DESC")
    user_data = my_cursor.fetchall()
    # Create a new PDF document
    doc = SimpleDocTemplate("DBstats.pdf", pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["Normal"]
    table_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),  # Header background color
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Center alignment for all cells
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Header font
        ("FONTSIZE", (0, 0), (-1, 0), 12),  # Header font size
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),  # Header bottom padding
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),  # Content background color
        ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Grid lines
        ("FONTSIZE", (0, 1), (-1, -1), 10),  # Content font size
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),  # Content bottom padding
    ])

    # Create the story (content elements) for the PDF
    story = []

    # Add report title
    title = Paragraph("Library System Report", title_style)
    story.append(title)
    story.append(Paragraph("<br/><br/>", normal_style))

    # Add category details to the PDF
    story.append(Paragraph("Books of each Category:", heading_style))
    story.append(Paragraph("<br/>", normal_style))

    category_table_data = [["Category", "Book Count"]]
    for category in category_data:
        category_table_data.append([category.CategoryName, str(category.books)])

    category_table = Table(category_table_data, style=table_style)
    story.append(category_table)
    story.append(Paragraph("<br/><br/>", normal_style))

    # Add book details to the PDF
    story.append(Paragraph("Top 3 Borrowed Books:", heading_style))
    story.append(Paragraph("<br/>", normal_style))

    book_table_data = [["Book Title", "Borrow Count"]]
    for book in book_data:
        book_table_data.append([book.BookTitle, str(book.BorrowCount)])

    book_table = Table(book_table_data, style=table_style)
    story.append(book_table)
    story.append(Paragraph("<br/><br/>", normal_style))

    # Add user details to the PDF
    story.append(Paragraph("Top 3 Users who borrowed books:", heading_style))
    story.append(Paragraph("<br/>", normal_style))

    user_table_data = [["UserName", "Borrow Count"]]
    for user in user_data:
        user_table_data.append([user.username, str(user.BorrowCount)])

    user_table = Table(user_table_data, style=table_style)
    story.append(user_table)

    # Build the PDF document
    doc.build(story)

#validate data 
def verify_Student(username , password):
    my_cursor.execute(f"select * from Student where Username = '{username}' and password='{password}'")
    row = my_cursor.fetchone()
    if row:
        student = Student(row[0],row[1],row[2],row[3],row[4])
        return student
    else:
        return None

def verify_admin(username , password):
    my_cursor.execute(f"select * from Admin where Username = '{username}' and password='{password}'")
    row = my_cursor.fetchone()
    if row:
        admin = Admin(row[2],row[1],row[0])
        return admin
    else:
        return None


def is_username_valid(username):
    # Username length validation: Minimum length of 3 and maximum length of 30
    if 3 <= len(username) < 31:
        return True
    return False

def is_password_strong(password):
    # Password strength criteria: At least 8 characters, contains at least one uppercase letter, one lowercase letter, and one digit
    if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password):
        return False
    return True

def is_email_valid(email):
    # Email format validation using a simple regular expression
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return True
    return False

def is_phone_valid(phone):
    # Phone number validation: Length is 11 and starts with "011", "010", "012", or "015"
    if len(phone) == 11 and re.match(r'^(011|010|012|015)', phone):
        return True
    return False
#end validation 


def main_window():
    #all functions and windows 
    def sign_up_student():
        root.destroy()
        def register():
            username = username_entry.get()
            password = password_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()

            if not is_username_valid(username):
                message_label.config(text="Invalid Username", fg="red")
                return False
            
            if not is_password_strong(password):
                message_label.config(text="Try a stronger password", fg="red")
                return False
                    
            if not is_email_valid(email):
                message_label.config(text="Invalid email", fg="red")
                return False
            
            if not is_phone_valid(phone):
                message_label.config(text="Invalid phone", fg="red")
                return False
            
            if verify_Student(username,password):
                print("this user already exists\n")
                message_label.config(text="this user already exists", fg="red")
                return False
            
            else:
                my_cursor.execute(f"INSERT INTO Student (username , password,email, phone) VALUES('{username}' , '{password}','{email}','{phone}');")
                my_cursor.commit()
                print("new admin has been added to the database\n")
            
            # Insert the student data into the database
            my_cursor.execute(f"INSERT INTO Student (Username, Password, Email, Phone) VALUES('{username}','{password}','{email}','{phone}');")
            my_cursor.commit()
            print("New student has been added to the database\n")

            message_label.config(text="Registration completed", fg="green")


        StudentSignUpPage = tk.Tk()
        StudentSignUpPage.title("Student Registration")
        StudentSignUpPage.title("Student Sign Up Page")
        StudentSignUpPage.configure(bg="white")
        StudentSignUpPage.geometry("1200x600")
        # Create a frame with padding
        frame = tk.Frame(StudentSignUpPage, pady=20, bg="white")
        frame.pack(anchor="center")

        # Create username label and entry
        username_label = tk.Label(frame, text="Username:", font=("Arial", 16))
        username_label.pack()
        username_entry = tk.Entry(frame, font=("Arial", 14),width=30)
        username_entry.pack(fill=tk.BOTH, expand=True,pady=20)

        # Create password label and entry
        password_label = tk.Label(frame, text="Password:", font=("Arial", 16))
        password_label.pack()
        password_entry = tk.Entry(frame, show="*", font=("Arial", 14),width=30)
        password_entry.pack(fill=tk.BOTH, expand=True,pady=20)


        # Create email label and entry
        email_label = tk.Label(frame, text="Email:", font=("Arial", 16))
        email_label.pack()
        email_entry = tk.Entry(frame, font=("Arial", 14),width=30)
        email_entry.pack(fill=tk.BOTH, expand=True,pady=20)


        # Create phone label and entry
        phone_label = tk.Label(frame, text="Phone:", font=("Arial", 16))
        phone_label.pack()
        phone_entry = tk.Entry(frame, font=("Arial", 14),width=30)
        phone_entry.pack(fill=tk.BOTH, expand=True,pady=20)

        def back():
            StudentSignUpPage.destroy()
            main_window()
        # Create register button
        register_button = tk.Button(frame, text="Register", command=register, font=("Arial", 12), bg="#4CAF50", fg="white", bd=0, highlightthickness=0, padx=20, pady=10, relief=tk.RAISED)
        register_button.pack(pady=10)

        message_label = tk.Label(frame, bg="white")
        message_label.pack()

        return_button = tk.Button(StudentSignUpPage, text='Return to Home', command=back, bg='green',fg = 'white')
        return_button.place(x=StudentSignUpPage.winfo_screenwidth() - return_button.winfo_reqwidth() - 10, y=10)
        return_button.pack()

        # Start the GUI event loop
        StudentSignUpPage.mainloop()

        
    def sign_up_Admin():
        root.destroy()

        def register():
            username = username_entry.get()
            password = password_entry.get()

            if not is_username_valid(username):
                message_label.config(text="Invalid Username", fg="red")
                return False
            
            if not is_password_strong(password):
                message_label.config(text="Try a stronger password", fg="red")
                return False
                    
            if verify_admin(username, password):
                print("This user already exists\n")
                message_label.config(text="This user already exists", fg="red")
                return False
            
            else:
                my_cursor.execute(f"INSERT INTO Admin (Password, Username) VALUES('{password}', '{username}');")
                my_cursor.commit()
                print("New admin has been added to the database\n")

            message_label.config(text="Registration completed", fg="green")


        def back():
            AdminSignUpPage.destroy()
            main_window()

        AdminSignUpPage = tk.Tk()
        AdminSignUpPage.title("Login")
        AdminSignUpPage.configure(bg="white")
        AdminSignUpPage.geometry("1200x600")

        # Create header label
        header_label = tk.Label(AdminSignUpPage, text="Admin Register Page", font=("Arial", 24, "bold"), bg="white")
        header_label.pack(pady=20)
        # Create a frame with padding
        frame = tk.Frame(AdminSignUpPage, pady=20, bg="white")
        frame.pack(anchor="center")

        # Create username label and entry
        username_label = tk.Label(frame, text="Username:", bg="white",font=("Arial", 16))
        username_label.pack()
        username_entry = tk.Entry(frame, font=("Arial", 14),width=30)
        username_entry.pack(fill=tk.BOTH, expand=True,pady=20)

        # Create password label and entry
        password_label = tk.Label(frame, text="Password:", bg="white",font=("Arial", 16))
        password_label.pack()
        password_entry = tk.Entry(frame, show="*", font=("Arial", 14),width=30)
        password_entry.pack(fill=tk.BOTH, expand=True,pady=20)

        # Create login button
        login_button = tk.Button(frame, text="Login", command=register, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), bd=0, highlightthickness=0, padx=20, pady=10, relief=tk.RAISED)
        login_button.pack(pady=10)

        # Create message label for displaying login status
        message_label = tk.Label(frame, bg="white")
        message_label.pack()

        return_button = tk.Button(AdminSignUpPage, text='Return to Home', command=back, bg='green',fg = 'white')
        return_button.place(x=AdminSignUpPage.winfo_screenwidth() - return_button.winfo_reqwidth() - 10, y=10)
        return_button.pack()
        # Start the Tkinter event loop
        AdminSignUpPage.mainloop()
        

    #search functions
    def search_by_year(year):
        my_cursor.execute(f"SELECT * FROM Book WHERE PublicationYear LIKE '%{year}%'")
        SrachYearWindow = tk.Tk()
        SrachYearWindow.title("category by year List")

        # Create a Treeview widget
        table = ttk.Treeview(SrachYearWindow)

        # Define the columns
        table['columns'] = ('isbn', 'title', 'author', 'year', 'quantity', 'category_id')

        # Format the columns
        table.column('isbn', width=150)
        table.column('title', width=200)
        table.column('author', width=150)
        table.column('year', width=100)
        table.column('quantity', width=100)
        table.column('category_id', width=100)

        # Create headings
        table.heading('#0', text='', anchor=tk.CENTER)
        table.heading('isbn', text='ISBN', anchor=tk.CENTER)
        table.heading('title', text='Title', anchor=tk.CENTER)
        table.heading('author', text='Author', anchor=tk.CENTER)
        table.heading('year', text='Year', anchor=tk.CENTER)
        table.heading('quantity', text='Quantity', anchor=tk.CENTER)
        table.heading('category_id', text='Category ID', anchor=tk.CENTER)

        for book in my_cursor:
            table.insert(parent='', index='end', iid=book[0], text='', values=(book[0], book[1], book[2], book[3], book[4], book[5]))

        table.pack()

        SrachYearWindow.mainloop()

    def search_by_author(author):
        my_cursor.execute(f"SELECT * FROM Book WHERE Author LIKE '%{author}%'")
        SearchAuthorWindow = tk.Tk()
        SearchAuthorWindow.title("category by author List")

        # Create a Treeview widget
        table = ttk.Treeview(SearchAuthorWindow)

        # Define the columns
        table['columns'] = ('isbn', 'title', 'author', 'year', 'quantity', 'category_id')

        # Format the columns
        table.column('isbn', width=150)
        table.column('title', width=200)
        table.column('author', width=150)
        table.column('year', width=100)
        table.column('quantity', width=100)
        table.column('category_id', width=100)

        # Create headings
        table.heading('#0', text='', anchor=tk.CENTER)
        table.heading('isbn', text='ISBN', anchor=tk.CENTER)
        table.heading('title', text='Title', anchor=tk.CENTER)
        table.heading('author', text='Author', anchor=tk.CENTER)
        table.heading('year', text='Year', anchor=tk.CENTER)
        table.heading('quantity', text='Quantity', anchor=tk.CENTER)
        table.heading('category_id', text='Category ID', anchor=tk.CENTER)

        for book in my_cursor:
            table.insert(parent='', index='end', iid=book[0], text='', values=(book[0], book[1], book[2], book[3], book[4], book[5]))

        table.pack()

        SearchAuthorWindow.mainloop()

    def search_by_title(title):
        my_cursor.execute(f"SELECT * FROM Book WHERE Title LIKE '%{title}%'")
        SearchTitleWindow = tk.Tk()
        SearchTitleWindow.title("category by title List")

        # Create a Treeview widget
        table = ttk.Treeview(SearchTitleWindow)

        # Define the columns
        table['columns'] = ('isbn', 'title', 'author', 'year', 'quantity', 'category_id')

        # Format the columns
        table.column('isbn', width=150)
        table.column('title', width=200)
        table.column('author', width=150)
        table.column('year', width=100)
        table.column('quantity', width=100)
        table.column('category_id', width=100)

        # Create headings
        table.heading('#0', text='', anchor=tk.CENTER)
        table.heading('isbn', text='ISBN', anchor=tk.CENTER)
        table.heading('title', text='Title', anchor=tk.CENTER)
        table.heading('author', text='Author', anchor=tk.CENTER)
        table.heading('year', text='Year', anchor=tk.CENTER)
        table.heading('quantity', text='Quantity', anchor=tk.CENTER)
        table.heading('category_id', text='Category ID', anchor=tk.CENTER)

        for book in my_cursor:
            table.insert(parent='', index='end', iid=book[0], text='', values=(book[0], book[1], book[2], book[3], book[4], book[5]))

        table.pack()

        SearchTitleWindow.mainloop()

    def search_by_isbn(isbn):
        my_cursor.execute(f"SELECT * FROM Book WHERE ISBN LIKE '{isbn}%' ")
        SearchISBNWindow = tk.Tk()
        SearchISBNWindow.title("category by ISBN List")

        # Create a Treeview widget
        table = ttk.Treeview(SearchISBNWindow)

        # Define the columns
        table['columns'] = ('isbn', 'title', 'author', 'year', 'quantity', 'category_id')

        # Format the columns
        table.column('isbn', width=150)
        table.column('title', width=200)
        table.column('author', width=150)
        table.column('year', width=100)
        table.column('quantity', width=100)
        table.column('category_id', width=100)

        # Create headings
        table.heading('#0', text='', anchor=tk.CENTER)
        table.heading('isbn', text='ISBN', anchor=tk.CENTER)
        table.heading('title', text='Title', anchor=tk.CENTER)
        table.heading('author', text='Author', anchor=tk.CENTER)
        table.heading('year', text='Year', anchor=tk.CENTER)
        table.heading('quantity', text='Quantity', anchor=tk.CENTER)
        table.heading('category_id', text='Category ID', anchor=tk.CENTER)

        for book in my_cursor:
            table.insert(parent='', index='end', iid=book[0], text='', values=(book[0], book[1], book[2], book[3], book[4], book[5]))

        table.pack()

        SearchISBNWindow.mainloop()

    def search_by_category_id(cat_id):
        my_cursor.execute(f"SELECT * FROM Book WHERE categoryID = '{cat_id}'")
        SearchCategoryIDWindow = tk.Tk()
        SearchCategoryIDWindow.title("category by ID List")

        # Create a Treeview widget
        table = ttk.Treeview(SearchCategoryIDWindow)

        # Define the columns
        table['columns'] = ('isbn', 'title', 'author', 'year', 'quantity', 'category_id')

        # Format the columns
        table.column('isbn', width=150)
        table.column('title', width=200)
        table.column('author', width=150)
        table.column('year', width=100)
        table.column('quantity', width=100)
        table.column('category_id', width=100)

        # Create headings
        table.heading('#0', text='', anchor=tk.CENTER)
        table.heading('isbn', text='ISBN', anchor=tk.CENTER)
        table.heading('title', text='Title', anchor=tk.CENTER)
        table.heading('author', text='Author', anchor=tk.CENTER)
        table.heading('year', text='Year', anchor=tk.CENTER)
        table.heading('quantity', text='Quantity', anchor=tk.CENTER)
        table.heading('category_id', text='Category ID', anchor=tk.CENTER)

        for book in my_cursor:
            table.insert(parent='', index='end', iid=book[0], text='', values=(book[0], book[1], book[2], book[3], book[4], book[5]))

        table.pack()

        SearchCategoryIDWindow.mainloop()



    def search_by_category():
        # Create the main window
        SearchWindow = tk.Tk()
        SearchWindow.geometry("1200x600")

        # Create the labels
        category_id_label = tk.Label(SearchWindow, text="Category ID", font=("Arial", 16))
        isbn_label = tk.Label(SearchWindow, text="ISBN", font=("Arial", 16))
        author_label = tk.Label(SearchWindow, text="Author", font=("Arial", 16))
        title_label = tk.Label(SearchWindow, text="Title", font=("Arial", 16))
        year_label = tk.Label(SearchWindow, text="Year", font=("Arial", 16))

        # Create the text boxes
        category_id_entry = tk.Entry(SearchWindow, font=("Arial", 16))
        isbn_entry = tk.Entry(SearchWindow, font=("Arial", 16))
        author_entry = tk.Entry(SearchWindow, font=("Arial", 16))
        title_entry = tk.Entry(SearchWindow, font=("Arial", 16))
        year_entry = tk.Entry(SearchWindow, font=("Arial", 16))

        def search_by_cat_id():
            category_id = category_id_entry.get()
            search_by_category_id(category_id)

        def search_title():
            title = title_entry.get()
            search_by_title(title)
        
        def search_isbn():
            isbn = isbn_entry.get()
            search_by_isbn(isbn)
        
        def search_author():
            author = author_entry.get()
            search_by_author(author)

        def search_year():
            year = year_entry.get()
            search_by_year(year)

        category_id_label.grid(row=0, column=0)
        category_id_entry.grid(row=0, column=1)

        isbn_label.grid(row=1, column=0)
        isbn_entry.grid(row=1, column=1)

        author_label.grid(row=2, column=0)
        author_entry.grid(row=2, column=1)

        title_label.grid(row=3, column=0)
        title_entry.grid(row=3, column=1)

        year_label.grid(row=4, column=0)
        year_entry.grid(row=4, column=1)

        # Create the buttons
        search_by_category_id_button = tk.Button(SearchWindow, text="Search by Category ID", command=search_by_cat_id, bg="green", fg="white", font=("Arial", 12), width=20, height=2)
        search_by_isbn_button = tk.Button(SearchWindow, text="Search by ISBN", command=search_isbn, bg="green", fg="white", font=("Arial", 12), width=20, height=2)
        search_by_author_button = tk.Button(SearchWindow, text="Search by Author", command=search_author, bg="green", fg="white", font=("Arial", 12), width=20, height=2)
        search_by_title_button = tk.Button(SearchWindow, text="Search by Title", command=search_title, bg="green", fg="white", font=("Arial", 12), width=20, height=2)
        search_by_year_button = tk.Button(SearchWindow, text="Search by Year", command=search_year, bg="green", fg="white", font=("Arial", 12), width=20, height=2)

        search_by_category_id_button.grid(row=5, column=0, padx=10, pady=10)
        search_by_isbn_button.grid(row=5, column=1, padx=10, pady=10)
        search_by_author_button.grid(row=5, column=2, padx=10, pady=10)
        search_by_title_button.grid(row=5, column=3, padx=10, pady=10)
        search_by_year_button.grid(row=5, column=4, padx=10, pady=10)

        # Start the main loop
        SearchWindow.mainloop()


    #view books for both students and Admins    
    def view_books():
        my_cursor.execute("SELECT * FROM Book")
        viewBooksWindow = tk.Tk()
        viewBooksWindow.title("Book List")

        # Create a Treeview widget
        table = ttk.Treeview(viewBooksWindow)

        # Define the columns
        table['columns'] = ('isbn', 'title', 'author', 'year', 'quantity', 'category_id')

        # Format the columns
        table.column('isbn', width=150)
        table.column('title', width=200)
        table.column('author', width=150)
        table.column('year', width=100)
        table.column('quantity', width=100)
        table.column('category_id', width=100)

        # Create headings
        table.heading('#0', text='', anchor=tk.CENTER)
        table.heading('isbn', text='ISBN', anchor=tk.CENTER)
        table.heading('title', text='Title', anchor=tk.CENTER)
        table.heading('author', text='Author', anchor=tk.CENTER)
        table.heading('year', text='Year', anchor=tk.CENTER)
        table.heading('quantity', text='Quantity', anchor=tk.CENTER)
        table.heading('category_id', text='Category ID', anchor=tk.CENTER)

        for book in my_cursor:
            table.insert(parent='', index='end', iid=book[0], text='', values=(book[0], book[1], book[2], book[3], book[4], book[5]))

        table.pack()

        viewBooksWindow.mainloop()
        



    def viewBorrowedBooks(student_ID):

        my_cursor.execute(f"""SELECT Book.ISBN, Book.Title, Book.Author, BorrowedBook.BorrowDate, BorrowedBook.ReturnDate
        FROM BorrowedBook JOIN Book
        ON BorrowedBook.BookID = Book.ISBN WHERE BorrowedBook.StudentID = '{student_ID}';""")

        viewBorrowedBooksWindow = tk.Tk()
        viewBorrowedBooksWindow.title("Book List")

        # Create a Treeview widget
        table = ttk.Treeview(viewBorrowedBooksWindow)

        # Define the columns
        table['columns'] = ('isbn', 'title', 'author', 'Borrowed Date', 'Return Date')

        # Format the columns
        table.column('isbn', width=150)
        table.column('title', width=200)
        table.column('author', width=150)
        table.column('Borrowed Date', width=100)
        table.column('Return Date', width=100)

        # Create headings
        table.heading('#0', text='', anchor=tk.CENTER)
        table.heading('isbn', text='ISBN', anchor=tk.CENTER)
        table.heading('title', text='Title', anchor=tk.CENTER)
        table.heading('author', text='Author', anchor=tk.CENTER)
        table.heading('Borrowed Date', text='Borrowed Date', anchor=tk.CENTER)
        table.heading('Return Date', text='Return Date', anchor=tk.CENTER)

        for book in my_cursor:
            table.insert(parent='', index='end', iid=book[0], text='', values=(book[0], book[1], book[2], book[3], book[4]))

        table.pack()

        viewBorrowedBooksWindow.mainloop()


    def admin_menu():
        #menu functions 
        def delete_book():
            def delete():
                isbn = isbn_entry.get()

                if not isbn:
                    message_label.config(text="ISBN field is required", fg="red")
                    return False

                # Implement your database deletion code here
                # Check if the book exists before deleting it
                # Replace the placeholder with your actual database deletion code
                my_cursor.execute(f"SELECT * FROM Book WHERE ISBN='{isbn}'")
                book = my_cursor.fetchone()
                if not book:
                    message_label.config(text="Book with this ISBN does not exist", fg="red")
                    return False
                my_cursor.execute(f"DELETE FROM Book WHERE ISBN='{isbn}'")
                my_cursor.commit()
                print("Book has been deleted\n")

                # Display appropriate message based on book existence
                if book:
                    message_label.config(text="Book has been deleted", fg="green")
                else:
                    message_label.config(text="Book with this ISBN does not exist", fg="red")

            DeleteBookwindow = tk.Tk()
            DeleteBookwindow.title("Delete Book")
            DeleteBookwindow.geometry("1200x600")

            frame = tk.Frame(DeleteBookwindow, pady=20, bg="white")
            frame.pack(anchor="center")

            isbn_label = tk.Label(frame, text="ISBN:", font=("Arial", 16))
            isbn_label.pack()
            isbn_entry = tk.Entry(frame, font=("Arial", 14))
            isbn_entry.pack()

            delete_button = tk.Button(frame, text="Delete", command=lambda: delete(isbn_entry.get()), font=("Arial", 12), bg="green", fg="white", bd=0, highlightthickness=0, padx=20, pady=10, relief=tk.RAISED)
            delete_button.pack(pady=10)

            message_label = tk.Label(frame, bg="white")
            message_label.pack()

            DeleteBookwindow.mainloop()
        def add_book():
            AdminMenuPage.destroy()
            def check_existing_book(isbn):
                my_cursor.execute(f"select isbn from book where isbn = '{isbn}'")
                row = my_cursor.fetchall()
                if row:
                    return True
                else:
                    return False

            def add():
                isbn = isbn_entry.get()
                title = title_entry.get()
                author = author_entry.get()
                year = year_entry.get()
                quantity = quantity_entry.get()
                category_id = category_entry.get()

                if not isbn:
                    message_label.config(text="ISBN field is required", fg="red")
                    return False

                if not title:
                    message_label.config(text="Title field is required", fg="red")
                    return False

                if not author:
                    message_label.config(text="Author field is required", fg="red")
                    return False

                if not year:
                    message_label.config(text="Publication Year field is required", fg="red")
                    return False

                if not quantity:
                    message_label.config(text="Quantity field is required", fg="red")
                    return False

                if not category_id:
                    message_label.config(text="Category ID field is required", fg="red")
                    return False

                if check_existing_book(isbn):
                    message_label.config(text="Book already exists", fg="red")
                    return False

                my_cursor.execute(f"INSERT INTO Book (ISBN, Title, Author, PublicationYear, Quantity, CategoryID) VALUES ('{isbn}', '{title}', '{author}', '{year}', '{quantity}', '{category_id}')")
                my_cursor.commit()
                print("New book has been added to the database\n")

                message_label.config(text="Book added successfully", fg="green")

            AddBookWindow = tk.Tk()
            AddBookWindow.title("Add Book")
            AddBookWindow.geometry("1200x600")
            AddBookWindow.configure(bg="white")

            frame = tk.Frame(AddBookWindow, pady=20, bg="white")
            frame.pack(anchor="center")

            isbn_label = tk.Label(frame, text="ISBN:", font=("Arial", 16))
            isbn_label.pack()
            isbn_entry = tk.Entry(frame, font=("Arial", 14))
            isbn_entry.pack()

            title_label = tk.Label(frame, text="Title:", font=("Arial", 16))
            title_label.pack()
            title_entry = tk.Entry(frame, font=("Arial", 14))
            title_entry.pack()

            author_label = tk.Label(frame, text="Author:", font=("Arial", 16))
            author_label.pack()
            author_entry = tk.Entry(frame, font=("Arial", 14))
            author_entry.pack()

            year_label = tk.Label(frame, text="Publication Year:", font=("Arial", 16))
            year_label.pack()
            year_entry = tk.Entry(frame, font=("Arial", 14))
            year_entry.pack()

            quantity_label = tk.Label(frame, text="Quantity:", font=("Arial", 16))
            quantity_label.pack()
            quantity_entry = tk.Entry(frame, font=("Arial", 14))
            quantity_entry.pack()

            category_label = tk.Label(frame, text="Category ID:", font=("Arial", 16))
            category_label.pack()
            category_entry = tk.Entry(frame, font=("Arial", 14))
            category_entry.pack()

            add_button = tk.Button(frame, text="Add", command=add, font=("Arial", 12), bg="#4CAF50", fg="white", bd=0, highlightthickness=0, padx=20, pady=10, relief=tk.RAISED)
            add_button.pack(pady=10)
            def back():
                AddBookWindow.destroy()
                admin_menu()    

            return_button = tk.Button(AddBookWindow, text='Return to Home', command=back, bg='green',fg = 'white')
            return_button.place(x=AddBookWindow.winfo_screenwidth() - return_button.winfo_reqwidth() - 10, y=10)
            return_button.pack()
            message_label = tk.Label(frame, bg="white")
            message_label.pack()







        def open_modify_window():
            AdminMenuPage.destroy()
            def modify(isbn):
                modify_book(isbn)

            def take_ispn():
                isbn = (isbn_entry.get())
                if check_book_exists(isbn):
                    message_label.config(text="book found", fg='green')
                    modify(isbn)
                else:
                    message_label.config(text="No book found", fg='red')

            def check_book_exists(isbn):
                my_cursor.execute(f"SELECT COUNT(*) FROM Book WHERE ISBN='{isbn}';")
                count = my_cursor.fetchone()[0]

                return count > 0
                
            # Create the modify window
            modify_window = tk.Tk()
            modify_window.title("Enter ISBN")
            modify_window.geometry("600x600")
            modify_window.configure(bg="white")

            # Create a frame with padding
            frame = tk.Frame(modify_window, pady=20, bg="white")
            frame.pack(anchor="center")

            # Create and pack the ISBN label and entry
            isbn_label = tk.Label(frame, text="ISBN:", font=("Arial", 16), bg="white")
            isbn_label.pack()
            isbn_entry = tk.Entry(frame, font=("Arial", 14), width=30)
            isbn_entry.pack(fill=tk.BOTH, expand=True, padx=20)



            # Create the button to trigger the modification
            modify_button = tk.Button(frame, text="Modify Book", font=("Arial", 14), command=take_ispn, bg="green", fg="white", width=15, height=2)
            modify_button.pack(pady=10)

            message_label = tk.Label(frame, bg="white")
            message_label.pack()

            modify_window.mainloop()


        def modify_book(isbn):

            def update_book():
                # Get the updated values from the entries
                title = title_entry.get()
                author = author_entry.get()
                year = year_entry.get()
                quantity = quantity_entry.get()
                category_id = category_entry.get()

                if(year.isdigit() and quantity.isdigit() and category_id.isdigit()):
                    my_cursor.execute(f"select count(*) from Category where CategoryID = '{category_id}';")
                    found = my_cursor.fetchone()[0]
                    if found:
                        message_label.config(text="Data modified succsessfuly", fg="green")
                        my_cursor.execute(f"UPDATE Book SET title='{title}', Author='{author}', PublicationYear='{year}', Quantity='{quantity}', CategoryID='{category_id}' WHERE ISBN='{isbn}';")
                        my_cursor.commit()
                    else:
                        message_label.config(text="Category not found", fg="red")
                        return
                else:
                    message_label.config(text="Input is not correct", fg="red")

            modify_bookWindow = tk.Tk()
            modify_bookWindow.title("Modify Book")
            modify_bookWindow.geometry("1200x600")
            modify_bookWindow.configure(bg="white")

            # Create a frame with padding
            frame = tk.Frame(modify_bookWindow, pady=20, bg="white")
            frame.pack(anchor="center")

            # Create and pack the Title label and entry
            title_label = tk.Label(frame, text="Title:", font=("Arial", 16), bg="white", borderwidth=0, highlightthickness=0)
            title_label.pack()
            title_entry = tk.Entry(frame, font=("Arial", 14), width=30)
            title_entry.pack(expand=True)

            # Create and pack the Author label and entry
            author_label = tk.Label(frame, text="Author:", font=("Arial", 16), bg="white", borderwidth=0, highlightthickness=0)
            author_label.pack()
            author_entry = tk.Entry(frame, font=("Arial", 14), width=30)
            author_entry.pack(expand=True)

            # Create and pack the Publication Year label and entry
            year_label = tk.Label(frame, text="Publication Year:", font=("Arial", 16), bg="white", borderwidth=0, highlightthickness=0)
            year_label.pack()
            year_entry = tk.Entry(frame, font=("Arial", 14), width=30)
            year_entry.pack(expand=True)

            # Create and pack the Quantity label and entry
            quantity_label = tk.Label(frame, text="Quantity:", font=("Arial", 16), bg="white", borderwidth=0, highlightthickness=0)
            quantity_label.pack()
            quantity_entry = tk.Entry(frame, font=("Arial", 14), width=30)
            quantity_entry.pack(expand=True)

            # Create and pack the Category ID label and entry
            category_label = tk.Label(frame, text="Category ID:", font=("Arial", 16), bg="white", borderwidth=0, highlightthickness=0)
            category_label.pack()
            category_entry = tk.Entry(frame, font=("Arial", 14), width=30)
            category_entry.pack(expand=True)

            def populate_book_data():
                # Fetch book data from the database
                my_cursor.execute(f"SELECT Title, Author, PublicationYear, Quantity, CategoryID FROM Book WHERE ISBN='{isbn}'")
                book_data = my_cursor.fetchone()

                # Populate the entry fields with the existing data
                if book_data:
                    title_entry.insert(tk.END, str(book_data[0]))
                    author_entry.insert(tk.END, book_data[1])
                    year_entry.insert(tk.END, book_data[2])
                    quantity_entry.insert(tk.END, str(book_data[3]))
                    category_entry.insert(tk.END, str(book_data[4]))

            # Call the populate_book_data function to populate the entry fields
            populate_book_data()

            # Create the button to trigger the validation
            update_button = tk.Button(frame, text="Update Book", font=("Arial", 14), command=update_book, bg="green", fg="white", width=15, height=2)
            update_button.pack(pady=10)

            message_label = tk.Label(frame, bg="white")
            message_label.pack()
            def back():
                modify_bookWindow.destroy()
                admin_menu()    

            return_button = tk.Button(modify_bookWindow, text='Return to Home', command=back, bg='green',fg = 'white')
            return_button.place(x=modify_bookWindow.winfo_screenwidth() - return_button.winfo_reqwidth() - 10, y=10)
            return_button.pack()
            modify_bookWindow.mainloop()


    



        AdminMenuPage = tk.Tk()
        AdminMenuPage.title("Admin Menu")
        AdminMenuPage.geometry("1200x600")
        AdminMenuPage.configure(bg="white")

        # Create a frame for the buttons
        button_frame = tk.Frame(AdminMenuPage, bg="white")
        button_frame.pack(pady=50)

        # Create the buttons
        button_font = ("Arial", 14, "bold")
        button_width = 15
        button_height = 4
        button_padx = 20
        button_pady = 10

        add_book_button = tk.Button(button_frame, text="Add Book", command=add_book, bg="green", fg="white", font=button_font, width=button_width, height=button_height)
        browse_books_button = tk.Button(button_frame, text="Browse Books", command=view_books, bg="green", fg="white", font=button_font, width=button_width, height=button_height)
        show_category_button = tk.Button(button_frame, text="Search Books", command=search_by_category, bg="green", fg="white", font=button_font, width=button_width, height=button_height)
        modify_book_button = tk.Button(button_frame, text="Modify Book", command=open_modify_window, bg="green", fg="white", font=button_font, width=button_width, height=button_height)
        deleteBook = tk.Button(button_frame, text="Delete Book", command=delete_book, bg="green", fg="white", font=button_font, width=button_width, height=button_height)



        add_book_button.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)
        browse_books_button.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)
        show_category_button.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)
        modify_book_button.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)
        deleteBook.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)

        # Start the main loop
        AdminMenuPage.mainloop()





    def student_login_window():

        #functions after login 
        def student_menu(student_ID):
            # menu functions
            def BorrowOrReturnBook(student_ID):
                StudentMenuPage.destroy()
                def borrow_book():
                    book_id = book_id_entry.get()
                    my_cursor.execute(f"select * from BorrowedBook where BookID = '{book_id}' AND StudentID = '{student_ID}'")
                    tmp = my_cursor.fetchone()
                    if tmp:
                        message_label.config(text="You have already borrowed this book",fg= 'red')
                    else:
                        my_cursor.execute(f"select * from Book where ISBN = '{book_id}'")
                        check = my_cursor.fetchone()
                        if check:
                            #get now amount 
                            my_cursor.execute(f"select Quantity from Book where ISBN = '{book_id}'")
                            now = my_cursor.fetchone()
                            
                            if now[0] == 0:
                                message_label.config(text="Book quantity is 0. Try another Book this week.",fg = 'red')
                                return None
                            else:
                                message_label.config(text="Borrow Book Successfully.",fg = 'green')
                                message_label.config(text="Book ID: " + book_id + ", You borrowed this book from " + str(datetime.today()) + " to " + str(datetime.today() + timedelta(weeks=1)) + '\n')
                                my_cursor.execute(f"update Book set Quantity = '{int(now[0]-1)}' where ISBN = '{book_id}'")
                                my_cursor.execute(f"insert into BorrowedBook (BookID,StudentID,BorrowDate,ReturnDate) values ('{book_id}','{student_ID}','{datetime.today()}','{datetime.today() + timedelta(weeks=1)}')")
                                my_cursor.commit()
                        else:
                            message_label.config("No such book.",fg ='red')

                def return_book():
                    BOOkID = book_id_entry.get()
                    my_cursor.execute(f"select * from BorrowedBook where BookID = '{BOOkID}' AND StudentID = '{student_ID}'")
                    tmp = my_cursor.fetchone()
                    #found book
                    if tmp:
                        message_label.config(text="Book Returned successfully\n", fg='green')
                        my_cursor.execute(f"DELETE FROM BorrowedBook WHERE BookID = '{BOOkID}' AND StudentID = '{student_ID}';")
                        my_cursor.execute(f"select Quantity from Book where ISBN = '{BOOkID}'")
                        now = my_cursor.fetchone()


                        my_cursor.execute(f"update Book set Quantity = '{int(now[0]+1)}' where ISBN = '{BOOkID}'")
                        my_cursor.commit()
                    else:
                        message_label.config(text="You don't borrowed this book yet.\n", fg='red')

                # Create the main window
                BorrowOrReturnBookWindow = tk.Tk()
                BorrowOrReturnBookWindow.geometry("600x600")
                BorrowOrReturnBookWindow.title("Book Borrowing System")
                BorrowOrReturnBookWindow.configure(bg="white")

                # Create a label for ISBN
                isbn_label = tk.Label(BorrowOrReturnBookWindow, text="ISBN:", font=("Arial", 16), bg="white")
                isbn_label.pack()

                # Create an entry field for book ID
                book_id_entry = tk.Entry(BorrowOrReturnBookWindow, font=("Arial", 16))
                book_id_entry.pack()

                # Create a frame with padding
                frame = tk.Frame(BorrowOrReturnBookWindow, pady=20, bg="white")
                frame.pack(anchor="center")

                # Create buttons for borrowing and returning books
                borrow_button = tk.Button(frame, text="Borrow", command=borrow_book, bg="green", fg="white", font=("Arial", 14), width=10)
                return_button = tk.Button(frame, text="Return", command=return_book, bg="green", fg="white", font=("Arial", 14), width=10)

                # Grid layout for buttons
                borrow_button.grid(row=0, column=0, padx=10)
                return_button.grid(row=0, column=1, padx=10)

                # Create a label to display the status
                message_label = tk.Label(BorrowOrReturnBookWindow, bg="white")
                message_label.pack()

                def back():
                    BorrowOrReturnBookWindow.destroy()
                    main_window()   

                return_button = tk.Button(BorrowOrReturnBookWindow, text='Return to Student menu', command=back, bg='green',fg = 'white')
                return_button.place(x=BorrowOrReturnBookWindow.winfo_screenwidth() - return_button.winfo_reqwidth() - 10, y=10)
                return_button.pack() 

                # Start the main event loop
                BorrowOrReturnBookWindow.mainloop()     
            def modify_user(user_id):
                #close last window 
                StudentMenuPage.destroy()
                def update():
                    username = username_entry.get()
                    password = password_entry.get()
                    email = email_entry.get()
                    phone = phone_entry.get()

                    if(username):
                        if not is_username_valid(username):
                            message_label.config(text="Invalid Username", fg="red")
                            return False
                    
                    if(password):
                        if not is_password_strong(password):
                            message_label.config(text="Try a stronger password", fg="red")
                            return False

                    if(email):    
                        if not is_email_valid(email):
                            message_label.config(text="Invalid email", fg="red")
                            return False
                    
                    if(phone):
                        if not is_phone_valid(phone):
                            message_label.config(text="Invalid phone", fg="red")
                            return False
                        
                    if(phone or username or email or password):
                        if(username):
                            my_cursor.execute(f"UPDATE student SET username = '{username}' where StudentID = {user_id};")
                        if(password):
                            my_cursor.execute(f"UPDATE student SET password = '{password}' where StudentID = {user_id};")
                        if(email):  
                            my_cursor.execute(f"UPDATE student SET email = '{email}' where StudentID = {user_id};")
                        if(phone):
                            my_cursor.execute(f"UPDATE student SET phone = '{phone}' where StudentID = {user_id};")
                        my_cursor.commit()
                        message_label.config(text="Account information updated", fg="green")
                        
                    else:
                        message_label.config(text="No data entered", fg="red")
                        return False
                        

                # Create the modify book window
                ModifyUserWindow = tk.Tk()
                ModifyUserWindow.title("Modify User")
                ModifyUserWindow.geometry("1200x600")

                # Create a frame with padding
                frame = tk.Frame(ModifyUserWindow, pady=20)
                frame.pack(anchor="center")

                # Create username label and entry
                username_label = tk.Label(frame, text="Username:", font=("Arial", 16))
                username_label.pack()
                username_entry = tk.Entry(frame, font=("Arial", 14),width=30)
                username_entry.pack(fill=tk.BOTH, expand=True,pady=20)

                # Create password label and entry
                password_label = tk.Label(frame, text="Password:", font=("Arial", 16))
                password_label.pack()
                password_entry = tk.Entry(frame, show="*", font=("Arial", 14),width=30)
                password_entry.pack(fill=tk.BOTH, expand=True,pady=20)


                # Create email label and entry
                email_label = tk.Label(frame, text="Email:", font=("Arial", 16))
                email_label.pack()
                email_entry = tk.Entry(frame, font=("Arial", 14),width=30)
                email_entry.pack(fill=tk.BOTH, expand=True,pady=20)


                # Create phone label and entry
                phone_label = tk.Label(frame, text="Phone:", font=("Arial", 16))
                phone_label.pack()
                phone_entry = tk.Entry(frame, font=("Arial", 14),width=30)
                phone_entry.pack(fill=tk.BOTH, expand=True,pady=20)


                # Create register button
                register_button = tk.Button(frame, text="Update", command=update, font=("Arial", 12), bg="#4CAF50", fg="white", bd=0, highlightthickness=0, padx=20, pady=10, relief=tk.RAISED)
                register_button.pack(pady=10)

                message_label = tk.Label(frame, bg="white")
                message_label.pack()

                def back():
                    ModifyUserWindow.destroy()
                    main_window()  

                return_button = tk.Button(ModifyUserWindow, text='Return to Student menu', command=back, bg='green',fg = 'white')
                return_button.place(x=ModifyUserWindow.winfo_screenwidth() - return_button.winfo_reqwidth() - 10, y=10)
                return_button.pack() 

                ModifyUserWindow.mainloop()


            StudentLoginPage.destroy()
            # Create the main window
            StudentMenuPage = tk.Tk()
            StudentMenuPage.configure(bg="white")
            StudentMenuPage.geometry("1200x600") 

            def account_modify():
                modify_user(student_ID)
            
            def borrow_or_return():
                BorrowOrReturnBook(student_ID)

            def book_view():
                view_books()

            def search_books():
                search_by_category()
            
            def viewBorrowed():
                viewBorrowedBooks(student_ID)

            # Create the buttons
            update_account_details_button = tk.Button(StudentMenuPage, text="Update Account Details", command=account_modify, bg="green", fg="white",width=36,height=4)
            browse_books_button = tk.Button(StudentMenuPage, text="Browse Books", command=book_view, bg="green", fg="white",width=36,height=4)
            search_books_button = tk.Button(StudentMenuPage, text="Search Books", command=search_books, bg="green", fg="white",width=36,height=4)
            borrow_book_button = tk.Button(StudentMenuPage, text="Borrow & return book", command=borrow_or_return, bg="green", fg="white",width=36,height=4)
            show_borrowed_books_button = tk.Button(StudentMenuPage, text="Show Borrowed Books", command=viewBorrowed, bg="green", fg="white",width=36,height=4)

            update_account_details_button.pack( pady=20)
            browse_books_button.pack(  pady=20)
            search_books_button.pack( pady=20)
            borrow_book_button.pack(  pady=20)
            show_borrowed_books_button.pack(  pady=20)

            # Start the main loop
            StudentMenuPage.mainloop()    
    
    
    
    #close main and open new window         
        root.destroy()
    # Create the main window
        StudentLoginPage = tk.Tk()
        StudentLoginPage.title("Login")
        StudentLoginPage.configure(bg="white")
        StudentLoginPage.geometry("1200x600")
        def login():
            username = username_entry.get()
            password = password_entry.get()
            student = verify_Student(username, password)
            if not student:
                message_label.config(text="Wrong Username or Password", fg="red")
                return
            else:
                message_label.config(text="Login successful", fg="green")
                student_menu(student.ID)
        def back():
            StudentLoginPage.destroy()
            main_window()        
        # Create header label
        header_label = tk.Label(StudentLoginPage, text="Student Log In Page", font=("Arial", 24, "bold"), bg="white")
        header_label.pack(pady=20)
        # Create a frame with padding
        frame = tk.Frame(StudentLoginPage, pady=20, bg="white")
        frame.pack(anchor="center")

        # Create username label and entry
        username_label = tk.Label(frame, text="Username:", bg="white",font=("Arial", 16))
        username_label.pack()
        username_entry = tk.Entry(frame, font=("Arial", 14),width=30)
        username_entry.pack(fill=tk.BOTH, expand=True,pady=20)

        # Create password label and entry
        password_label = tk.Label(frame, text="Password:", bg="white",font=("Arial", 16))
        password_label.pack()
        password_entry = tk.Entry(frame, show="*", font=("Arial", 14),width=30)
        password_entry.pack(fill=tk.BOTH, expand=True,pady=20)

        # Create login button
        login_button = tk.Button(frame, text="Login", command=login, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), bd=0, highlightthickness=0, padx=20, pady=10, relief=tk.RAISED)
        login_button.pack(pady=10)

        # Create message label for displaying login status
        message_label = tk.Label(frame, bg="white")
        message_label.pack()

        return_button = tk.Button(StudentLoginPage, text='Return to Home', command=back, bg='green',fg = 'white')
        return_button.place(x=StudentLoginPage.winfo_screenwidth() - return_button.winfo_reqwidth() - 10, y=10)
        return_button.pack()

        # Start the Tkinter event loop
        StudentLoginPage.mainloop()

    def admin_login_window():
        root.destroy()
        
    # Create the main window
        adminLoginPage = tk.Tk()
        adminLoginPage.title("Login")
        adminLoginPage.configure(bg="white")
        adminLoginPage.geometry("1200x600")
        def back():
            adminLoginPage.destroy()
            main_window()
        def login():
            username = username_entry.get()
            password = password_entry.get()
            student = verify_admin(username, password)
            if not student:
                message_label.config(text="Wrong Username or Password", fg="red")
            else:
                message_label.config(text="Login successful", fg="green")
                admin_menu()
        # Create header label
        header_label = tk.Label(adminLoginPage, text="Admin Log In Page", font=("Arial", 24, "bold"), bg="white")
        header_label.pack(pady=20)
        # Create a frame with padding
        frame = tk.Frame(adminLoginPage, pady=20, bg="white")
        frame.pack(anchor="center")

        # Create username label and entry
        username_label = tk.Label(frame, text="Username:", bg="white",font=("Arial", 16))
        username_label.pack()
        username_entry = tk.Entry(frame, font=("Arial", 14),width=30)
        username_entry.pack(fill=tk.BOTH, expand=True,pady=20)

        # Create password label and entry
        password_label = tk.Label(frame, text="Password:", bg="white",font=("Arial", 16))
        password_label.pack()
        password_entry = tk.Entry(frame, show="*", font=("Arial", 14),width=30)
        password_entry.pack(fill=tk.BOTH, expand=True,pady=20)

        # Create login button
        login_button = tk.Button(frame, text="Login", command=login, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), bd=0, highlightthickness=0, padx=20, pady=10, relief=tk.RAISED)
        login_button.pack(pady=10)

        # Create message label for displaying login status
        message_label = tk.Label(frame, bg="white")
        message_label.pack()
        return_button = tk.Button(adminLoginPage, text='Return to Home', command=back, bg='green',fg = 'white')
        return_button.place(x=adminLoginPage.winfo_screenwidth() - return_button.winfo_reqwidth() - 10, y=10)
        return_button.pack()

        # Start the Tkinter event loop
        adminLoginPage.mainloop()


    # Create the main window
    root = tk.Tk()
    root.title("Home Page")

    # Set the root size
    root.geometry("1200x600")

    # Set the background color
    root.configure(bg="white")

    # Print hello to our system
    label = tk.Label(root, text="Welcome to the university library system", font=("Arial", 33), bg="white")
    label.pack(pady=50)

    # Create the buttons
    viewStatsButton = tk.Button( text="view Statistics(PDF)", command=generate_pdf_report, width=25, height=4, bg="green", fg="white", font=("Arial", 14))
    viewStatsButton.pack(anchor='center')

    button_frame = tk.Frame(root, bg="white")
    button_frame.pack()

    student_button = tk.Button(button_frame, text="Sign in as a Student", command=student_login_window, width=25, height=4, bg="green", fg="white", font=("Arial", 14))
    student_button.grid(row=0, column=0, padx=50, pady=10)

    admin_button = tk.Button(button_frame, text="Sign in as an Admin", command=admin_login_window, width=25, height=4, bg="green", fg="white", font=("Arial", 14))
    admin_button.grid(row=0, column=1, padx=50, pady=10)

    student_signup_button = tk.Button(button_frame, text="Sign Up for New Students", command=sign_up_student, width=25, height=4, bg="green", fg="white", font=("Arial", 14))
    student_signup_button.grid(row=1, column=0, padx=50, pady=10)

    admin_signup_button = tk.Button(button_frame, text="Sign Up for New Admins", command=sign_up_Admin, width=25, height=4, bg="green", fg="white", font=("Arial", 14))
    admin_signup_button.grid(row=1, column=1, padx=50, pady=10)



    # Start the GUI event loop
    root.mainloop()

main_window()
