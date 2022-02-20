from kivy.config import Config
#Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.core.window import Window
from functools import partial
import scraper
import re
Builder.load_file("design.kv")
#Window.size = (600,500)
class P(Screen):
    pass


class MainPage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.refresh()

    def refresh(self):
        global matches
        matches = scraper.get_games()
        self.ids.games.clear_widgets()
        layout = GridLayout(cols=1)
        for match in matches:
            layout = GridLayout(cols = 3)
            status = Label(text=match[0])

            if "завершен" in match[0]:
                color = (1,0,0, 1)

            elif "перерыв" in match[0]:
                color = (1,1,140/255, 1)
  
            elif "тайм" in match[0] or "время" in match[0]:
                color = (0,1,0,1)
            else:
                color = (1,0,0,1)
            first_team = match[1]
            second_team = match[3]
            if len(first_team) >= 12:
                first_team = first_team[:12]+"\n"+first_team[12:]
            if len(second_team) >=12:
                second_team = "      "+second_team[:12]+"\n"+"      "+second_team[12:]
            team1 = Label(text = first_team,font_size='15sp', size_hint=(0.45,0.45))
            team2 = Label(text = second_team,font_size='15sp', size_hint=(0.45,0.45))

            tournament = match[5]
            url = match[4]
            score = Button(text= match[2], on_release = partial(self.show_popup, team1, team2, url, tournament), background_color=color,size=(185,100))
            score_status = GridLayout(cols=1, size_hint=(0.2,0.2))
            score_status.add_widget(status)
            score_status.add_widget(score)
            #layout.add_widget(status)
            layout.add_widget(team1)
            layout.add_widget(score_status)
            layout.add_widget(team2)

            self.ids.games.add_widget(layout)
            self.ids.games.add_widget(Label())
        self.ids.games.height = 100*len(self.ids.games.children)
    def show_popup(self,team1,team2,url,event, score):

        show = P()
        main = GridLayout(cols = 3)
        info_ = scraper.get_scorers(url)
        info = info_[0]
        current_minute = info_[1]
        first_team = team1.text
        second_team = team2.text
        main.add_widget(Label())
        main.add_widget(Label())
        main.add_widget(Label())
        main.add_widget(Label(text = first_team))
        main.add_widget(Label(text = score.text))
        main.add_widget(Label(text = second_team))
        main.add_widget(Label())
        main.add_widget(Label(text=current_minute))
        main.add_widget(Label())
        goals_layout = GridLayout(cols = 2)
        first_scroll = ScrollView()
        first_team_col = GridLayout(cols = 1, text_size=(300, None),size_hint_y=None,spacing=(15,15))
        second_scroll = ScrollView()
        second_team_col = GridLayout(cols=1, text_size=(300,None), size_hint_y=None, spacing=(15,15))
        for i in range(len(info)):
            team_info = info[i]

            for goal in team_info:
                minute = goal[0]
                scorer = goal[1]
                assistant = goal[2]
                if assistant != "":
                    assistant = "("+assistant+")"
                goal_label = Label(text=minute+" "+scorer)
                if i == 0:
                    first_team_col.height = 60*len(info[i])
                    first_team_col.add_widget(Label())
                    first_team_col.add_widget(goal_label)
                    first_team_col.add_widget(Label(text=assistant))
                    first_team_col.add_widget(Label())
                else:
                    second_team_col.height = 60*len(info[i])
                    second_team_col.add_widget(Label())
                    second_team_col.add_widget(goal_label)
                    second_team_col.add_widget(Label(text=assistant))
                    second_team_col.add_widget(Label())
        first_scroll.add_widget(first_team_col)
        second_scroll.add_widget(second_team_col)
        goals_layout.add_widget(first_scroll)
        goals_layout.add_widget(second_scroll)
        main_layout = GridLayout(cols=1)
        main_layout.add_widget(main)
        main_layout.add_widget(goals_layout)

        # show.add_widget(goals_layout)
        # show.add_widget(main)
        show.add_widget(main_layout)
        popupWindow = Popup(title=event, content = show, size_hint=(None, None), size=(self.ids.main_layout.width,self.ids.main_layout.height-200))
        popupWindow.open()
# class RootWidget(ScreenManager):
#     pass
class MainApp(App):
    def build(self):
        return MainPage()

if __name__ == "__main__":
    MainApp().run()
