class Library(object):

  # Constructor
  def __init__(self,name="Centennial College (Progress)"):
    self.__name=name
    self.__loans = []
    self.__books={1001: {'title': 'Introduction to Programming', 'author': 'Farell', 'copies': 2}, 
                  1002: {'title': 'Database Concepts', 'author': 'Morris', 'copies': 5}, 
                  1003: {'title': 'Object Oriented Analysis', 'author': 'Farell', 'copies': 4}, 
                  1004: {'title': 'Linux Operating System', 'author': 'Palmer', 'copies': 2}, 
                  1005: {'title': 'Data Science using Python', 'author': 'Russell', 'copies': 4}, 
                  1006: {'title': 'Functional Programming with Python', 'author': 'Babcock', 'copies': 6}}
 
  # Instance properties
  @property
  def books(self):
    x=self.__books.copy()
    return x

  # Instance Method
  def __str__(self):
    x=self.__name+"Book List"
    for key,value in self.__books.items():
      x+=('\n %s - ')%(key)
      for key,value in value.items():
        if isinstance(value,str):
         x+=('%s ')%(value)
        else:
         x+=('(%s)')%(str(value))

    x+="\nLoans\n"+str(self.__loans)+"\n"
    return x

  # Method
  def add(self,book_info:dict)-> None:     
        newBook={book_info.get('isbn') :{'title': book_info.get('book').get('title'), 'author': book_info.get('book').get('author'),'copies': book_info.get('book').get('copies')}}
        if book_info.get('isbn') in self.__books.keys():
          self.__books[book_info.get('isbn')]['copies']+=book_info.get('book').get('copies')
        else:      
          self.__books.update(newBook)

  def loan(self, loan_info: tuple) -> None:
    # If it is not present an Exception is raised.
    if (loan_info[1] in self.__books):
      # If it is present but there are no copies available, then also raise an Exception.
      if (self.__books[loan_info[1]]['copies'])<1:
        raise ValueError('No more copies of %s\n'%(loan_info[1]))
      # If it is present and at least one copy is available in the library.
      else:
              self.__books[loan_info[1]]['copies']-=1
              print('Loaning one copy of %s' %(self.__books[loan_info[1]]['title']))
           
      newLoan = tuple(list(loan_info))
      self.__loans.append(newLoan)
     
    else:
      raise ValueError('%s not available in the library'%(loan_info[1]))

  def take_back(self, book_info: tuple) -> None:
    # If it is present    
    # That tuple is deleted from the __loans collection. Then the number of copies is increased by one.
    searchResult=0
    temp=()
    for x in self.__loans:
      if (book_info[0] in x[0]):
        if (book_info[1] == x[1]):
         searchResult = 1
         temp=x
         break
      else:
        searchResult = 0

    if (searchResult==1):
      self.__loans.remove(temp)
      self.__books[book_info[1]]['copies']+=1
    # If it is not present, then an Exception is raised.
    else:
      raise ValueError (book_info,' is not valid loan')

#-----------------------------
#        Test harness 
#-----------------------------

# Testing the __init__ and the __str__ methods of the Library class
progress = Library()
print(f'\nActual books in the library')
print(progress) #shows 6 books

# Verifying that the books property returns a copy and not the actual
# Book collection items of the class
print('Testing the books property')
local = progress.books
print(local)

# Creating a new book
isbn = 1007    # Add one value to the dic
book = {'title': 'Client-Side Javascript', 'author': 'Vodkin', 'copies': 6}
print(f'\nAdding {isbn} {book} to the local copy')
local[isbn] = book
print(local)

print(f'\nActual books in the library')
print(progress) # Still show 6 books

abook = {}              # Create an empty dic
abook['isbn'] = isbn    # Add an isbn key-value to the dic
abook['book'] = book    # Add an book key-value to the dic
print(f'\nAdding a new book {abook}')
progress.add(abook)
print(progress)         # Show 7 books

abook.clear()
abook ['isbn'] = 1001
abook['book'] = {'title': 'Introduction to Programming', 'author': 'Farell', 'copies': 1}
print(f'\nAdding a single copy of an existing book {abook}')
progress.add(abook)
print(progress)       # Number of copies of '1001' goes up by 1

abook.clear()
abook ['isbn'] = 1002
abook['book'] = {'title': 'Database Concepts', 'author': 'Morris', 'copies': 5}
print(f'\nAdding multiple copies of an existing book {abook}')
progress.add(abook)
print(progress)       # Number of copies of '1002' goes up by 5

# Borrowing a book
info = ('Arielle', 1001, 'may-03-2021')
print(f'\n\nLoaning {info} from library')
progress.loan(info)
print(progress)

# Trying to borrow a non-existent book
try:
  print(f'Trying to borrow non-existent isbn')
  info = ('Arielle', 1009, 'may-03-2021')
  progress.loan(info)
except Exception as e:
  print(e)
print(progress)

# Safe Borrowing book
info = [('Mohini', 1001, 'may-01-2021'), ('Viktoria', 1001, 'may-02-2021'), ('Gurvir', 1002, 'may-03-2021'), ('Heesoo', 1007, 'may-05-2021')]
for x in info:
  progress.loan(x)
print(progress)

# Trying to borrow a zero copy book
try:
  print(f'Trying to borrow a zero copy book')
  info = ('Arielle', 1001, 'may-03-2021')
  progress.loan(info)
except Exception as e:
  print(e)

# Return book
ret_info = ('Mohini', 1001)
print(f'Returning {ret_info} to library')
progress.take_back(ret_info)

# Return book with non-exsisted value
try:
  ret_info = ('Arielle', 1009)
  print(f'Trying to return a non-existent loan')
  print(f'\n\nReturning {ret_info} to library')

  progress.take_back(ret_info)
except Exception as e:
  print(e)
  print(progress)