from elemental_tools.logger import Logger

logger = Logger(app_name='elemental', owner='exceptions').log


def GetDuplicatedKey(exception):
    try:
        return str(exception.details['keyValue'])
    except:
        return None


class DependenciesNotFound(Exception):

    def __init__(self, *args):
        super().__init__()
        Exception(args)


class ScriptModuleMissing:

    def __init__(self, title):
        print(f'Script module missing when validating: {title}')


class ParameterMissing(Exception):

    def __init__(self, title):
        Exception.__init__(self, f"The argument {title} is missing.")


class SettingMissing(Exception):

    def __init__(self, title):
        Exception.__init__(self, f"The Setting: {title} cannot be found on the database\n"
                                 f"If you want to create a custom Setting, you must add to your code:\n\t"
                                 f"""from elemental_tools.api.settings import SettingsController, Setting

                                    _new_setting = Setting(
                                        sub= # user id,
                                        name= # setting name,
                                        value= # setting value
                                    )
                                    _settings = SettingsController()
                                    _settings.create(
                                        _new_setting
                                    )
                                """
                                 
                                 f"\n\n\tIf it was not your intent, try to run: python3 -m elemental_tools.Jarvis.install")


class ThreadTimeout(Exception):
    pass


class ThreadLimitExceeded(Exception):
    pass


class SkipExecution:

    def __init__(self, msg: str = "", app: str = None):
        logger('skip-execution', msg, app_name='scripts')


class InvalidCSV(Exception):

    def __init__(self, link):
        super().__init__(f"Cannot find csv on the provided link: {link}")
