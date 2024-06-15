import flet as ft
import requests
session = requests.Session()
server = "https://graptis.pythonanywhere.com/"  # Update with the actual server URL
 
class LoginPage(ft.UserControl):
    def __init__(self, controller):
        ft.UserControl.__init__(self)
        self.controller = controller

    def login(self, event):
        if not self.name.value or not self.passw.value:
            self.message.value, self.message.color = "Give your name and password", "red"
            self.update()
            return
        else:
            data = {"name": self.name.value, "passw": self.passw.value}
            try:
                result = session.post(server + "login", json=data, timeout=5)
                if result.status_code == 200 and 'error' not in result.json():
                    self.controller.user = self.name.value
                    self.controller.start_questions(result.json())
                elif 'error' in result.json().keys():
                    self.message.value, self.message.color = "Wrong Password", "red"
                    self.update()
                    return
                else:
                    self.message.value, self.message.color = "failed connection", "red"
                    self.update()
                    return
            except:
                result=[{'correct': 2, 'id': 'T5', 'question': 'Τι επιστρέφει ο παρακάτω κώδικας:\n<pre>\ndef func(a, b, c, d):\n    print (a+d)\nfunc(1,2,3,4)\n</pre>\n', 'replies': {'1': '1 4', '2': '5', '3': 'error', '4': '3', '5': 'Δεν γνωρίζω'}},
{'correct': 3, 'id': 'Q6', 'question': 'Τι ορίζουμε με τον παρακάτω κώδικα;\n<pre>\ndef a(b,c,d,e):\n    pass\n</pre>\n', 'replies': {'1': 'μία λίστα και την αρχικοποίησή της', '2': 'μια κλάση', '3': 'μια συνάρτηση που δεν κάνει κάτι', '4': 'τίποτα από τα παραπάνω', '5': 'Δεν γνωρίζω'},
{'correct': 3, 'id': 'T7', 'question': 'Τι θα επιστρέψει ο παρακάτω κώδικας;\n<pre>\ndef func(*a):\n\treturn sum([x for x in a if x%2 == 0])\nprint(func(2,3,4,5))\n</pre>\n', 'replies': {'1': 'error', '2': '14', '3': '6', '4': '8', '5': '[2,4]', '6': 'Δεν γνωρίζω'}},
{'correct': 3, 'id': 'T8', 'question': 'Τι θα επιστρέψει ο κώδικας;\n<pre>\ndef d(x = 0, y = 0):\n\treturn (x**2 + y**2)**0.5\nd(3)\n</pre>\n', 'replies': {'1': 'error', '2': '3', '3': '3.0', '4': '9.0', '5': 'Δεν γνωρίζω'}},
{'correct': 2, 'id': 'Q4', 'question': 'Kαθολικές μεταβλητές είναι ...\n', 'replies': {'1': 'εκείνες που ορίζονται ως global εντός συναρτήσεων', '2': 'οι μεταβλητές που παίρνουν τιμή εκτός συναρτήσεων', '3': 'οι μεταβλητές που περνάνε ως ορίσματα συναρτήσεων', '4': 'Δεν γνωρίζω'}},
{'correct': 4, 'id': 'Q2', 'question': "Τι θα τυπώσει το πρόγραμμα;\n<pre>\ndef f():\n\ta = a + 7\n\tprint(a, end = ' ')\na = 5\nf()\nprint(a, end = ' ')\n</pre>\n", 'replies': {'1': '12 5', '2': '12 12', '3': '7 5', '4': 'UnboundLocalError', '5': 'Δεν γνωρίζω'}}]
                self.update()
                return

    def build(self):
        self.name = ft.TextField(label='Name:', width='300')
        self.passw = ft.TextField(label="Password:", password=True, width='300', can_reveal_password=True)
        self.message = ft.Text("")
        self.controls = [ft.Text("Quiz", color="black200", size=30),ft.Text("Sign in or Start", width='300'),
        self.name,self.passw,ft.FilledButton("Start", on_click=self.login),self.message]
        return ft.Column(self.controls)

class StatsPage(ft.UserControl):
    def __init__(self, controller):
        ft.UserControl.__init__(self)
        self.controller = controller

    def build(self):
        self.controls = [ft.Text(f"Name: {self.controller.user}", size=30, color="yellow900"),ft.Text(f'Score: {100 * self.controller.score / self.controller.displayed_question:.1f}%', size=40),
            ft.Row([ft.FilledButton("Restart", on_click=self.controller.new_game),
            ft.OutlinedButton("Exit", icon=ft.icons.EXIT_TO_APP, icon_color="black900", on_click=self.controller.login)])]
        return ft.Column(self.controls)

class QuizPage(ft.UserControl):
    def __init__(self, controller, label, question, user):
        ft.UserControl.__init__(self)
        self.controller,self.label,self.question,self.user = controller,label,question,user
        self.answered = False

    def submit_handler(self, event):
        if(self.question['id'][0]=='Q'):
            if self.submit.text == "Next": self.controller.update_question()
            if not self.replies.value:self.message.value,self.message.color = "Choose answer","red"
            else: 
                if self.replies.value == str(self.question["correct"]): self.message.value,self.message.color,self.answered="Correct!","green",True
                else:self.message.value,self.message.color = f"The answer is: \n{self.question['replies'][str(self.question['correct'])]}","red"
                self.replies.disabled = True
                self.submit.text = "Next"
            try:self.update()
            except:pass
        else:
            if self.submit.text == "Next": self.controller.update_question()
            if not self.reply.value:self.message.value,self.message.color = "Write answer","red"
            else: 
                if self.reply.value == self.question['replies'][str(self.question['correct'])]: self.message.value,self.message.color,self.answered="Correct!","green",True
                else:self.message.value,self.message.color = f"The answer is: \n{self.question['replies'][str(self.question['correct'])]}","red"
                self.reply.disabled = True
                self.submit.text = "Next"
            try:self.update()
            except:pass
    def build(self):#more in controls
        self.controls = [ft.Text(f"Quiz for:{self.user}", size=30, color="black900")]
        if(self.question['id'][0]=='Q'):
            self.controls.append(ft.Markdown(f"{self.question['question'].replace('<pre>', '```').replace('</pre>', '```')}",extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            code_style= ft.TextStyle(font_family="Roboto Mono", ),code_theme="atom-one-dark"))
            self.controls.append(ft.Text("Choose:"))
            self.replies = ft.RadioGroup(content=ft.Column(ft.Radio(value= str(x[0]), label= x[1]) for x in self.question['replies'].items()))
            self.controls.append(self.replies )
        else:
            self.controls.append(ft.Markdown(f"{self.question['question'].replace('<pre>', '```').replace('</pre>', '```')}",extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            code_style= ft.TextStyle(font_family="Roboto Mono", ),code_theme="atom-one-dark"))
            
            self.reply = ft.TextField(label='Complete:', width='300')
            self.controls.append(self.reply)
        self.submit = ft.FilledButton(f"Υποβολή", on_click=self.submit_handler)
        self.controls.append (self.submit)
        self.message = ft.Text("")
        self.controls.append(self.message)
        return ft.Column(self.controls)

class Controller:
    def __init__(self, page):
        self.page = page
        self.login()

    def login(self, event=None):
        self.user = None
        self.score = 0
        self.displayed_question = 0
        while self.page.controls:
            self.page.controls.pop()
        self.page.add(LoginPage(self))

    def start_questions(self, questions=None):
        self.score = 0
        self.displayed_question = 0
        while self.page.controls:
            self.page.controls.pop()
        self.questions = questions
        for i in self.questions:print(i)
        self.update_question()

    def new_game(self, event):
        try:
            result = session.post(server + "newgame", timeout=5)
            if result.status_code==200:self.start_questions(result.json())
            else:self.restart()
        except:self.restart()

    def restart(self):
        while self.page.controls:
            self.page.controls.pop()
        self.login()

    def update_question(self):
        label = f"{self.displayed_question + 1}/{len(self.questions)}"
        if self.displayed_question < len(self.questions):
            if self.page.controls:
                done_question = self.page.controls.pop()
                if done_question.answered:
                    self.score += 1
            self.page.add(QuizPage(self, label, self.questions[self.displayed_question], self.user))
            self.displayed_question += 1
        else:
            if self.page.controls:
                done_question = self.page.controls.pop()
                if done_question.answered:
                    self.score += 1
            data = {"score": self.score / self.displayed_question}
            try:
                result = session.post(server + "end", json=data, timeout=5)
                print(result.json())
                if result.status_code != 200:
                    print("Failed to connect to the end route")
            except Exception as error:
                print("Failed to connect to the end route", error)
            self.page.add(StatsPage(self))

def main(page: ft.Page):
    page.title = "Quiz"
    Controller(page)
ft.app(target=main)
