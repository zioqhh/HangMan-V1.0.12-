import sqlite3, os

class view_database():
  def view_database(file):
    if os.path.isfile(file):
      if file.endswith(".db"):
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        print("USER TABLE")
        for row in cursor.execute("SELECT * FROM users"):
          print(f"User {row[0]}")
          print(f"Wins {row[1]}")
          print(f"Losses {row[2]}")
          print(f"Games {row[3]}")
          print()
        print("GAMES TABLE")
        for row in cursor.execute("SELECT * FROM games"):
          print(f"Word {row[0]}")
          print(f"Solved {row[1]}")
          print(f"Letters {row[2]}")
          print(f"Mode {row[3]}")
          print(f"Hint {row[4]}")
          print(f"Owner {row[5]}")
          print()
      else:
        print("File must be a .db file.")
    else:
      print("File does not exist.")
