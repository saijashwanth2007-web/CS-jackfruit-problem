import wx
import json
import os
import wx.adv
from datetime import datetime

class EventCalendar(wx.Frame):
    def _init_(self):
        super()._init_(None, title="Event Calendar", size=(500, 600))
        
        self.events = self.load_events()
        self.notified_dates = set()  # Track dates already notified today
        
        self.init_ui()
        self.show_selected_date()
        
        # Set up timer for checking event notifications every minute (60000 ms)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.check_for_notifications, self.timer)
        self.timer.Start(60000)  # Check every 60 seconds
        
        # Initial check on startup
        self.check_for_notifications(None)
    
    def load_events(self):
        if os.path.exists("events.json"):
            with open("events.json", "r") as f:
                return json.load(f)
        return {
            "2025-12-01": ["Meeting with Client", "Lunch with Team"],
            "2025-12-05": ["Project Deadline"],
            "2025-12-15": ["Birthday Party"]
        }
    
    def save_events(self):
        with open("events.json", "w") as f:
            json.dump(self.events, f)
    
    def init_ui(self):
        panel = wx.Panel(self)
        
        # Calendar
        self.calendar = wx.adv.CalendarCtrl(panel, wx.ID_ANY, 
                                               wx.DefaultDateTime,
                                               pos=(10, 10), size=(450, 200))
        self.calendar.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.on_date_selected)
        
        # Event entry
        wx.StaticText(panel, label="Event:", pos=(10, 220))
        self.event_entry = wx.TextCtrl(panel, wx.ID_ANY, size=(300, -1), pos=(70, 218))
        
        # Buttons
        self.add_btn = wx.Button(panel, label="Add Event", pos=(10, 250))
        self.add_btn.Bind(wx.EVT_BUTTON, self.add_event)
        
        self.edit_btn = wx.Button(panel, label="Edit Event", pos=(100, 250))
        self.edit_btn.Bind(wx.EVT_BUTTON, self.edit_event)
        
        self.delete_btn = wx.Button(panel, label="Delete Event", pos=(190, 250))
        self.delete_btn.Bind(wx.EVT_BUTTON, self.delete_event)
        
        # Events listbox
        wx.StaticText(panel, label="Events for selected date:", pos=(10, 290))
        self.events_listbox = wx.ListBox(panel, wx.ID_ANY, 
                                       size=(450, 250), pos=(10, 320), 
                                       style=wx.LB_SINGLE)
        self.events_listbox.Bind(wx.EVT_LISTBOX, self.on_event_selected)
    
    def on_date_selected(self, event):
        self.show_selected_date()
    
    def show_selected_date(self):
        date = self.calendar.GetDate()
        date_str = date.FormatISODate()
        self.events_listbox.Clear()
        
        if date_str in self.events:
            for event in self.events[date_str]:
                self.events_listbox.Append(event)
    
    def add_event(self, event):
        date = self.calendar.GetDate()
        date_str = date.FormatISODate()
        event_text = self.event_entry.GetValue().strip()
        
        if not event_text:
            return
        
        if date_str not in self.events:
            self.events[date_str] = []
        self.events[date_str].append(event_text)
        
        self.event_entry.Clear()
        self.save_events()
        self.show_selected_date()
    
    def on_event_selected(self, event):
        index = event.GetSelection()
        if index != wx.NOT_FOUND:
            event_text = self.events_listbox.GetString(index)
            self.event_entry.SetValue(event_text)
    
    def edit_event(self, event):
        date = self.calendar.GetDate()
        date_str = date.FormatISODate()
        
        try:
            index = self.events_listbox.GetSelection()
            if index == wx.NOT_FOUND:
                return
            
            new_event = self.event_entry.GetValue().strip()
            if not new_event:
                return
            
            self.events[date_str][index] = new_event
            self.save_events()
            self.show_selected_date()
            self.event_entry.Clear()
        except (KeyError, IndexError):
            pass
    
    def delete_event(self, event):
        date = self.calendar.GetDate()
        date_str = date.FormatISODate()
        
        try:
            index = self.events_listbox.GetSelection()
            if index == wx.NOT_FOUND:
                return
            
            self.events[date_str].pop(index)
            
            if not self.events[date_str]:
                del self.events[date_str]
            
            self.save_events()
            self.show_selected_date()
            self.event_entry.Clear()
        except (KeyError, IndexError):
            pass
    
    def check_for_notifications(self, event):
        today_str = datetime.now().strftime("%Y-%m-%d")
        if today_str in self.events and today_str not in self.notified_dates:
            events_today = self.events[today_str]
            if events_today:
                message = "Events today:\n" + "\n".join(events_today)
                wx.MessageBox(message, "Event Reminder", wx.OK | wx.ICON_INFORMATION)
                self.notified_dates.add(today_str)

if __name__ == "__main__":
    app = wx.App()
    frame = EventCalendar()
    frame.Show()
    app.MainLoop()
    


def highlight_event_dates(self):
    # First clear previous attributes
    self.calendar.ResetAttr()
    
    for date_str in self.events:
        try:
            # Convert string date to wx.DateTime
            date = wx.adv.CalendarDateAttr()
            y, m, d = map(int, date_str.split('-'))
            wx_date = wx.DateTime.FromDMY(d, m - 1, y)  # month is 0-based
            
            # Create a custom attr: red background with white text
            attr = wx.adv.CalendarDateAttr()
            attr.SetBackgroundColour(wx.Colour(255, 180, 180))
            attr.SetTextColour(wx.Colour(255, 0, 0))
            attr.SetBold(True)
            
            # Set attribute for this date
            self.calendar.SetAttr(wx_date, attr)
        except Exception as e:
            pass  # ignore invalid dates
    
    self.calendar.Refresh()  # Refresh calendar to apply changes
    
def add_event(self, event):
    # existing add event code ...
    self.save_events()
    self.highlight_event_dates()  # update highlights
    self.show_selected_date()
 
