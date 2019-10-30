import datetime,pytz


class Event:
    def __init__(self,data):
        self.current_event = None
        for key in data:
            setattr(self,key,data[key])
        self.data = data
        if self.current_event:
            self.start = datetime.datetime.fromtimestamp(data['current_event']['starts_at']).astimezone(pytz.timezone(self.timezone))
            self.month = self.start.strftime('%B')
            self.short_month = self.start.strftime('%b')
            self.day = self.start.day
            self.year = self.start.strftime('%Y')
        self.url = self.id
