import flet as fl
def main(page:fl.Page):
    page.bgcolor="red"
    page.add(fl.Column([fl.Text("a",size=30,weight="bold")]))
fl.app(target=main)