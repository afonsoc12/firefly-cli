from cmd import Cmd
from pprint import pprint

from configs_manager import *
from firefly import Firefly


class FireflyPrompt(Cmd):
    prompt = '🐷 ➜ '
    configs = load_configs()
    api = Firefly(configs['URL'], configs['API_TOKEN'])

    is_url_set = True if configs['URL'] is not None else False
    is_api_token_set = True if configs['API_TOKEN'] is not None else False

    # Display information to update URL or API token, if not already set
    opt_text = ''
    if not (is_url_set and is_api_token_set):
        if is_url_set and not is_api_token_set:
            opt_text += 'It appears that you have not set your API token yet.\nType \"edit API_TOKEN <TOKEN>\" to do so.'
        elif not is_url_set and is_api_token_set:
            opt_text += 'It appears that you have not set your URL yet.\nType \"edit URL <URL>\" to do so.'
        elif not (is_url_set and is_api_token_set):
            opt_text += 'It appears that you have not set neither of your URL or API token yet.\nType \"edit URL <URL>\" or \"edit API_TOKEN <TOKEN>\" to do so.'


    intro = '''
Welcome to FireflyIII Command Line Interface!
Created by Afonso Costa (@afonsoc12)

===== Status =====
  - URL: {}
  - API Token: {}
  - Connection: {}
  
{}
Type \"help\" to list commands.
    '''.format(configs['URL'] if is_url_set else '(not set)',
               configs['API_TOKEN'] if is_api_token_set else '(not set)',
               'OK!' if api.api_test else 'No connection!',
               opt_text)


    @classmethod
    def refresh_api(cls):
        cls.api = Firefly(cls.configs['URL'], cls.configs['API_TOKEN'])

    def do_exit(self, input):
        print('Bye! Come store new transactions soon!')
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    def do_edit(self, input):
        input_split = input.split(' ')
        if len(input_split) != 2:
            print(f'The command \"edit\" takes exactly two arguments. Provided: {input}')
        else:
            if input_split[0] == 'URL' or input_split == 'API_TOKEN':
                self.configs[input_split[0]] = input_split[1]
                save_configs_to_file(self.configs)
                FireflyPrompt.refresh_api()
            else:
                print(f'The argument \"{input_split[0]}\" is not recognised.')

    def complete_edit(self, text, line, begidx, endidx):
        if not text:
            completions = self.configs.keys()
        else:
            completions = [f
                           for f in self.configs.keys()
                           if f.startswith(text)
                           ]
        return completions

    def help_edit(self):
        print('Shows your available budgets.')

    def do_budgets(self, input):
        budgets = api.get_budgets()
        pprint(budgets)

    def help_budgets(self):
        print('Shows your available budgets.')

    def default(self, input):
        if input == 'x' or input == 'q':
            return self.do_exit(input)

        print('{} not recognized. Please type \"help\" to list the available commands'.format(input))

    do_EOF = do_exit
    help_EOF = help_exit


def load_configs():
    try:
        with open(config_file_path, 'r') as f:
            configs = json.loads(f.read())
    except FileNotFoundError:
        print('File not found, creating the file..')

        with open(config_file_path, 'w') as f:
            configs = {'URL': None, 'URL_TOKEN': None}
            save_configs_to_file(configs)
    return configs


def save_configs_to_file(configs):
    try:
        with open(config_file_path, 'w') as f:
            json.dump(configs, f)
            print('Config file saved at {}'.format(str(config_file_path)))
    except:
        print('An error has occurred while saving file to {}'.format(str(config_file_path)))


if __name__ == '__main__':
    FireflyPrompt().cmdloop()
