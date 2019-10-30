import datetime,pytz

class Event:
    def __init__(self,data):
        for key in data:
            setattr(self,key,data[key])
        self.data = data
        self.start = datetime.datetime.fromtimestamp(data['current_event']['starts_at']).astimezone(pytz.timezone(self.timezone))
        self.url = self.id
        self.month = self.start.strftime('%B')
        self.short_month = self.start.strftime('%b')
        self.day = self.start.day
