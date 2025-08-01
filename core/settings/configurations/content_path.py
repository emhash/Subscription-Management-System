class UserContentPath:
    def __init__(self, subfolder, include_date=False, date_format='%Y/%m/%d', user_path=None):
        self.subfolder = subfolder
        self.include_date = include_date
        self.date_format = date_format
        self.user_path = user_path

    def _get_user(self, instance):
        # If a user_path is given, follow it
        if self.user_path:
            obj = instance
            for attr in self.user_path.split('.'):
                obj = getattr(obj, attr, None)
                if obj is None:
                    return None
            return obj
        # Otherwise, just check for 'user' attr
        return getattr(instance, 'user', None)

    def __call__(self, instance, filename):
        from datetime import datetime

        user = self._get_user(instance)
        username = getattr(user, 'username', None) or 'unknown'

        path = f"{username}/content/"

        if self.subfolder:
            subfolder = self.subfolder
            if not subfolder.endswith('/'):
                subfolder += '/'
            path += subfolder

        if self.include_date:
            date_path = datetime.now().strftime(self.date_format).replace('/', '-')
            if not date_path.endswith('/'):
                date_path += '/'
            path += date_path

        return f"{path}{filename}"

    def __eq__(self, other):
        if isinstance(other, UserContentPath):
            return (
                self.subfolder == other.subfolder and
                self.include_date == other.include_date and
                self.date_format == other.date_format and
                self.user_path == other.user_path
            )
        return False

    def deconstruct(self):
        path = 'core.settings.configurations.content_path.UserContentPath'
        args = [self.subfolder]
        kwargs = {}
        if self.include_date:
            kwargs['include_date'] = self.include_date
        if self.date_format != '%Y/%m/%d':
            kwargs['date_format'] = self.date_format
        if self.user_path is not None:
            kwargs['user_path'] = self.user_path
        return path, args, kwargs
