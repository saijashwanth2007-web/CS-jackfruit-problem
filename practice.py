import wx
import wx.adv
import datetime

def normalize_date(wx_date):
    py_date = datetime.date(wx_date.GetYear(), wx_date.GetMonth() + 1, wx_date.GetDay())
    return py_date.strftime("%Y-%m-%d")

class EventCalendar(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Event Calendar", size=(400, 450))

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Calendar
        self.calendar = wx.adv.CalendarCtrl(panel)
        self.calendar.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.on_date_selected)
        vbox.Add(self.calendar, 0, wx.ALL | wx.CENTER, 10)

        # Event entry
        self.event_entry = wx.TextCtrl(panel)
        vbox.Add(self.event_entry, 0, wx.EXPAND | wx.ALL, 10)

        # Add event button
        add_btn = wx.Button(panel, label="Add Event")
        add_btn.Bind(wx.EVT_BUTTON, self.add_event)
        vbox.Add(add_btn, 0, wx.ALL | wx.CENTER, 10)

        # Event display
        self.events_box = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.events_box, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(vbox)

        self.events = {
            "2023-10-01": ["Meeting with Client", "Lunch with Team"],
            "2023-10-05": ["Project Deadline"],
            "2023-10-15": ["Birthday Party"]
        }

        self.update_display()

    def get_selected_date(self):
        return normalize_date(self.calendar.GetDate())

    def update_display(self):
        selected_date = self.get_selected_date()
        self.events_box.SetValue(f"Events on {selected_date}:\n\n")

        if selected_date in self.events:
            for event in self.events[selected_date]:
                self.events_box.AppendText(f"- {event}\n")

    def on_date_selected(self, event):
        self.update_display()

    def add_event(self, event):
        selected_date = self.get_selected_date()
        new_event = self.event_entry.GetValue().strip()

        if not new_event:
            return

        if selected_date not in self.events:
            self.events[selected_date] = []

        self.events[selected_date].append(new_event)
        self.event_entry.SetValue("")
        self.update_display()


if __name__ == "__main__":
    app = wx.App()
    frame = EventCalendar()
    frame.Show()
    app.MainLoop()