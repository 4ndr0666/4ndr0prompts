import npyscreen
class TestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', npyscreen.ActionForm, name="Test")
TestApp().run()

