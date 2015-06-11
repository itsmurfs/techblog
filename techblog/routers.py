#We need just one router because when None is returned the router manager follows the default behavior: sends
#  the operations to the default database. That is what we want.

class TechblogRouter(object):
    """
    A router to control all database operations on models in the
    techblog application.
    """

    def _go_mongo(self, model, **hints):
        return model._meta.app_label == 'techblog'

    def db_for_read(self, model, **hints):
        """
        Attempts to read techblog models go to techblog_db.
        """
        if self._go_mongo(model, **hints):
            return 'techblog_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write techblog models go to techblog_db.
        """
        if self._go_mongo(model, **hints):
            return 'techblog_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the techblog app is involved.
        """
        if self._go_mongo(obj1, **hints) or \
           self._go_mongo(obj2, **hints):
           return True
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the auth techblog only appears in the 'techblog_db'
        database.
        """
        #Maybe we can use: if db=='techblog_db' return False because, since it is a non-rel db,
        #  syncdb is no longer needed
        if db == 'techblog_db':
            return self._go_mongo(model)
        elif model._meta.app_label == 'techblog':
            return False
        return None

