import random, time, os, sqlite3
from random_word import RandomWords
from view_database import view_database
1
r = RandomWords()
owner = os.environ['REPL_OWNER']

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS games 
              (
              word TEXT PRIMARY KEY,
              solved TEXT,
              letters TEXT,
              mode TEXT,
              hint INTEGER,
              owner TEXT
              )""")
cursor.execute("""CREATE TABLE IF NOT EXISTS users 
              (
              owner TEXT PRIMARY KEY,
              wins INTEGER,
              losses INTEGER,
              games INTEGER
              )""")


hangman = [
"""
-----
|   |
|
|
|
|
|
|
|
--------
""",
"""
-----
|   |
|   0
|
|
|
|
|
|
--------
""",
"""
-----
|   |
|   0
|  -+-
|
|
|
|
|
--------
""",
"""
-----
|   |
|   0
| /-+-
|
|
|
|
|
--------
""",
"""
-----
|   |
|   0
| /-+-\ 
|
|
|
|
|
--------
""",
"""
-----
|   |
|   0
| /-+-\ 
|   | 
|
|
|
|
--------
""",
"""
-----
|   |
|   0
| /-+-\ 
|   | 
|   | 
|
|
|
--------
""",
"""
-----
|   |
|   0
| /-+-\ 
|   | 
|   | 
|  |
|
|
--------
""",
"""
-----
|   |
|   0
| /-+-\ 
|   | 
|   | 
|  | 
|  | 
|
--------
""",
"""
-----
|   |
|   0
| /-+-\ 
|   | 
|   | 
|  | | 
|  | 
|
--------
""",
"""
-----
|   |
|   0
| /-+-\ 
|   | 
|   | 
|  | | 
|  | | 
|
--------
"""]

def main():
  cursor.execute("SELECT * FROM users WHERE owner = ?", (owner,))
  result = cursor.fetchone()
  if not result:
    cursor.execute("INSERT INTO users (owner, wins, losses, games) VALUES (?, ?, ?, ?)", (owner, 0, 0, 0))
    conn.commit()
  cursor.execute("SELECT * FROM users WHERE owner = ?", (owner,))
  result = cursor.fetchone()
  os.system("clear")
  mode = ""
  m = input(f"User: {result[0]}\nWins: {result[1]}\nLosses: {result[2]}\nGames: {result[3]}\n\nDificulty:\n  [1]: Easy (6 Letters)\n  [2]: Medium (8 Letters)\n  [3]: Hard (10 Letters)\n  [4]: Extreme (12 Letters)\nYour Choice: ")
  if m == "1":
    mode = "easy"
  elif m == "2":
    mode = "medium"
  elif m == "3":
    mode = "hard"
  elif m == "4":
    mode = "extreme"
  elif m == "5":
    for row in cursor.execute("SELECT * FROM games"):
      print(row)
    print()
    for row in cursor.execute("SELECT * FROM users"):
      print(row)
  level = 0
  letters = []
  word = ""
  while True:
    word = r.get_random_word()
    if mode == "easy" and len(word) > 6:
      word = r.get_random_word()
    elif mode == "easy" and len(word) < 7 and len(word) > 1:
      word = word
      break
    if mode == "medium" and len(word) > 8:
      word = r.get_random_word()
    elif mode == "medium" and len(word) < 9 and len(word) > 3:
      word = word
      break
    elif mode == "hard" and len(word) > 10:
      word = r.get_random_word()
    elif mode == "hard" and len(word) < 11 and len(word) > 5:
      word = word
      break
    if mode == "extreme" and len(word) > 12:
      word = r.get_random_word()
    elif mode == "extreme" and len(word) < 13 and len(word) > 7:
      word = word
      break
      
  hint = 0
  true_level = 0
  while True:
    os.system("clear")
    true_level = level
    if level > 9 and mode == "easy" and level < 17:
      true_level = 9
    elif level > 16 and mode == "easy":
      print(f"You Lost!\nThe Word Was {word}")
      cursor.execute("INSERT INTO games VALUES (?, ?, ?, ?, ?, ?)", (word, "false", str(letters), mode, hint, owner))
      conn.commit()
      cursor.execute("UPDATE users SET losses = losses + 1, games = games + 1 WHERE owner = ?", (owner,))
      conn.commit()
      time.sleep(2)
      main()
    if level > 9 and mode == "medium" and level < 13:
      true_level = 9
    elif level > 12 and mode == "medium":
      print(f"You Lost!\nThe Word Was {word}")
      cursor.execute("INSERT INTO games VALUES (?, ?, ?, ?, ?, ?)", (word, "false", str(letters), mode, hint, owner))
      conn.commit()
      cursor.execute("UPDATE users SET losses = losses + 1, games = games + 1 WHERE owner = ?", (owner,))
      conn.commit()
      time.sleep(2)
      main()
    if level > 9 and mode == "easy" and level < 17:
      true_level = 9
    elif level > 16 and mode == "easy":
      print(f"You Lost!\nThe Word Was {word}")
      cursor.execute("INSERT INTO games VALUES (?, ?, ?, ?, ?, ?)", (word, "false", str(letters), mode, hint, owner))
      conn.commit()
      cursor.execute("UPDATE users SET losses = losses + 1, games = games + 1 WHERE owner = ?", (owner,))
      conn.commit()
      time.sleep(2)
      main()
    if level > 9 and mode == "medium" and level < 13:
      true_level = 9
    elif level > 12 and mode == "medium":
      print(f"You Lost!\nThe Word Was {word}")
      cursor.execute("INSERT INTO games VALUES (?, ?, ?, ?, ?, ?)", (word, "false", str(letters), mode, hint, owner))
      conn.commit()
      cursor.execute("UPDATE users SET losses = losses + 1, games = games + 1 WHERE owner = ?", (owner,))
      conn.commit()
      time.sleep(2)
      main()
    
    print_word = []
    length = len(word)
    for e in word:
      if e.lower() in letters:
        print_word.append(e)
      else:
        print_word.append("_")
    if "".join(print_word) == word:
      print("You Win!")
      print(f"The Word Was {word}")
      cursor.execute("UPDATE users SET wins = wins + 1, games = games + 1 WHERE owner = ?", (owner,))
      conn.commit()
      cursor.execute("INSERT OR REPLACE INTO games VALUES (?, ?, ?, ?, ?, ?)", (word, "true", str(letters), mode, hint, owner))
      conn.commit()
      time.sleep(2)
      index = 0
      t = 8
      while t > 1:
        if index > 6:
          index = 0
        elif index == 0:
          print("Rebooting |", end="\r")
        elif index == 1:
          print("Rebooting /", end="\r")
        elif index == 2:
          print("Rebooting —", end="\r")
        elif index == 3:
          print("Rebooting \\", end="\r")
        elif index == 4:
          print("Rebooting |", end="\r")
        elif index == 5:
          print("Rebooting /", end="\r")
        elif index == 6:
          print("Rebooting -", end="\r")
        time.sleep(0.25)
        index+=1
        t-=1
      main()
    print("".join(print_word))
    print(hangman[true_level])
    if hint == 0:
      print("Hint Availible.")
    else:
      print("No Hint Availible.")
    print(f"Letters Used: {', '.join(sorted(letters))}")
    choice = input("Letter (or hint): ")
    cancel = 0
    if bool(choice) == False:
      print("Invalid Choice.")
      time.sleep(2)
    elif len(choice) > 1 and choice != "hint":
      print("Invalid Choice.")
      time.sleep(2)
    
    elif choice.lower() == "hint":
      if hint == 0:
        w = "".join(word.split())
        w2 = []
        for e in w:
          w2.append(e)
        letter = random.choice(w2)
        while True:
          if letter in letters:
            letter = random.choice(w2)
          else:
            letters.append(letter)
            break
        print(f"Hint Revealed {letter} 🫣")
        
        hint = 1
        time.sleep(2)
      else:
        print("You Already Used A Hint.")
        time.sleep(2)
    elif choice.lower() in letters:
      print("Letter Already In Use.")
      time.sleep(2)
      cancel = 1
    elif choice.lower() not in letters and choice.lower() in word.lower() and choice != None:
      print("Correct Guess!")
      letters.append(choice.lower())
      time.sleep(2)
    elif choice.lower() not in letters and choice.lower() not in word.lower():
      print("Incorrect Guess!")
      letters.append(choice.lower())
      level += 1
      time.sleep(2)
    
    
    elif choice == "hint":
      pass
    elif cancel == 0:
      letters.append(choice)
    else:
      pass

main()
#view_database.view_database("data.db")