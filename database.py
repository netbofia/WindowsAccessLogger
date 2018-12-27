import sqlite3



class Db:
	def __init__(self):
		self.conn = sqlite3.connect('SQL/nanodrop.db')
		self.c= self.conn.cursor()


	def getUser(self,username):
		username=(username,)
		self.c.execute('SELECT * FROM users WHERE user=?', username)
		return self.c.fetchone()
		
	def setUser(self,username,name,unit,passHash,admin):
		userData=(username,name,unit,passHash,admin)
		self.c.execute('INSERT INTO users (user,name,unit,hash,admin) VALUES (?,?,?,?,?)', userData)
		self.conn.commit()

	def listUsers(self):
		self.c.execute('SELECT user, name, unit, admin, enabled FROM users')
		return self.c.fetchall()

	def logActivity(self,usernameId):
		userData=(usernameId,)
		self.c.execute('INSERT INTO activity (user) VALUES (?)', userData)
		self.conn.commit()


	def getLogs(self,LIMIT=10000):
		self.c.execute('SELECT u.unit, u.user, a.start as date, a.samples FROM activity as a, users as u WHERE u.id=a.user')
		return self.c.fetchall()

	def getPath(self):
		self.c.execute('SELECT value FROM settings WHERE key="path"')
		return self.c.fetchone()

	def setPath(self,path):		
		path=(path,)
		self.c.execute('UPDATE settings SET value=? WHERE key="path"', path)		
		self.conn.commit()

	def setPassword(self,id,hash):
		data=(hash,id)
		self.c.execute('UPDATE users SET hash=? WHERE id=?', data)		
		self.conn.commit()