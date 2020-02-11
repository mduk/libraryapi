import sqlite3

class ReservationModel():
    def __init__(self, row):
        self.reservation_id, self.timestamp, self.title, self.email = row


class LibraryService():
    def __init__(self, db_dsn=None):
        if db_dsn == None:
            self.db = sqlite3.connect(':memory:')
            self._initialise_database()
        else:
            self.db = sqlite3.connect(db_dsn)

    def _initialise_database(self):
        self.db.cursor().execute('''
            CREATE TABLE reservation (
                reservation_id INTEGER PRIMARY KEY,
                reserved_at TEXT,
                title TEXT,
                email TEXT
            )
        ''')

        self.db.cursor().execute('''
            CREATE TABLE book (
                book_id INTEGER PRIMARY KEY,
                title TEXT
            )
        ''')

        self.db.cursor().execute('''
            INSERT INTO book ( title )
            VALUES
                ( "The Hitchhiker's Guide to the Galaxy" ),
                ( "So Long And Thanks For All The Fish" ),
                ( "In the Land of Invented Languages" ),
                ( "The Enchiridion" )
        ''')


    def reserve_book(self, *, title, email):
        query = '''
            INSERT INTO reservation (reserved_at, title, email)
            VALUES (datetime("now"), ?, ?)
        '''
        result = self.db.cursor().execute(query, (title, email))
        reservation_id = result.lastrowid
        return self.get_reservation_by_id(reservation_id)

    def cancel_reservation(self, reservation_id):
        query = '''
            DELETE FROM reservation
            WHERE reservation_id = ?
        '''
        return self.db.cursor().execute(query, (reservation_id,))

    def list_reservations(self):
        query = '''
            SELECT reservation_id, reserved_at, title, email
            FROM reservation
        '''
        rows = self.db.cursor().execute(query).fetchall()
        return [ ReservationModel(r) for r in rows ]


    def get_reservation_by_id(self, reservation_id):
        query = '''
            SELECT reservation_id, reserved_at, title, email
            FROM reservation
            WHERE reservation_id = ?
        '''
        row = self.db.cursor().execute(query, (reservation_id,)).fetchone()
        return ReservationModel(row)

    def book_exists(self, title):
        query = '''
            SELECT COUNT(*)
            FROM book
            WHERE title = ?
        '''
        count = self.db.cursor().execute(query, (title,)).fetchone()
        return (count > 0)
