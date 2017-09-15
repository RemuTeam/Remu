from project.Main import RemuApp


def before_all(context):
    app = RemuApp()
    context.app = app
    app.run()


def after_all(context):
    context.app.stop()