import pandas as pd
import datetime as dt

class DateUtil:
    def get_isoweek_range(self, isoweek, year=dt.date.today().year):
        first_day_of_year = dt.date(year, 1, 1)
        first_monday = first_day_of_year + dt.timedelta(days=(7 - first_day_of_year.weekday()))
        
        start_date = first_monday + dt.timedelta(weeks=isoweek-2)
        end_date = start_date + dt.timedelta(days=6)
        return (start_date, end_date)
    
    def get_start_of_timeframe(self, date, timeframe='year'):
        date = pd.to_datetime(date).date()
        
        if timeframe == 'week':
            return (date - pd.DateOffset(days=date.weekday())).date()
        
        elif timeframe == 'month':
            return dt.date(date.year, date.month, 1)
        
        elif timeframe == 'quarter':
            month = ((date.month - 1) // 3) * 3 + 1
            return dt.date(date.year, month, 1)
        
        return dt.date(date.year, 1, 1)
    
    def get_end_of_timeframe(self, date, timeframe='year'):
        date = pd.to_datetime(date).date()
        
        if timeframe == 'week':
            return (date - pd.DateOffset(days=date.weekday()) + pd.DateOffset(days=6)).date()
        
        if timeframe == 'month':
            next_month = (date.month + 1) % 12 if (date.month + 1) % 12 != 0 else 0
            return (dt.date(date.year + 1, next_month, 1) - pd.DateOffset(days=1)).date()
        
        if timeframe == 'quarter':
            month = ((date.month - 1) // 3) * 3 + 3
            day = 30 if month == 6 or month == 9 else 31
            return dt.date(date.year, month, day)
        
        return dt.date(date.year, 12, 31)
    
    def get_start_and_end_of_timeframe(self, date, timeframe='year'):
        return (self.get_start_of_timeframe(date, timeframe), self.get_end_of_timeframe(date, timeframe))
    
    def get_till_date_df(self, df, date_col, date_today=dt.date.today(), timeframe='week'):
        date_today = pd.to_datetime(date_today).date()
        start_date = self.get_start_of_timeframe(date_today, timeframe)
        return df[(df[date_col].dt.date >= start_date) & (df[date_col].dt.date <= date_today)]
    
    def get_outlook_df(self, df, date_col, date_today=dt.date.today(), timeframe='week'):
        date_today = pd.to_datetime(date_today).date()
        start_date = self.get_start_of_timeframe(date_today, timeframe)
        end_date = self.get_end_of_timeframe(date_today, timeframe)
        return df[(df[date_col].dt.date >= start_date) & (df[date_col].dt.date <= end_date)]
        
dateutil = DateUtil()