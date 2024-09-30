class DjangoDatabaseMixin:
    database: str = None
    def get_engine(self):
        return {
            "mysql": "django.db.backends.mysql",
            "postgresql": "django.db.backends.postgresql_psycopg2",
            "sqlite3": "django.db.backends.sqlite3"
        }[self.database]
    
    def as_django(self):
        if self.database == 'sqlite3':
            return {
                "ENGINE": self.get_engine(),
                "NAME": self.path
            }
        
        return {
            "ENGINE": self.get_engine(),
            "USER": self.username,
            "PASSWORD": self.password,
            "HOST": self.host,
            "PORT": str(self.port),
            "NAME": self.name,
        }