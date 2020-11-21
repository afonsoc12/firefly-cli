from datetime import datetime
from cmd import Cmd
from pprint import pprint

from configs_manager import *
from api_driver import FireflyAPI
from io import StringIO
import pandas as pd


def parse_transaction_to_df(input):
    if isinstance(input, str):
        cols = ['amount', 'description', 'source_name', 'destination_name', 'category', 'budget']
        data = pd.read_csv(StringIO(input), header=None)

        # Add remaining columns None
        data.columns = cols[:data.shape[1]]
        data = pd.concat([data, pd.DataFrame([[None for _ in cols[data.shape[1]:]]], columns=cols[data.shape[1]:])], axis=1)
        data.index = [datetime.now()]

        # Convert all to string and strip edges
        data = data.astype(str).apply(lambda x: x.str.strip())
        return data


class FireflyPrompt(Cmd):
    prompt = '🐷 ➜ '
    configs = load_configs()
    api = FireflyAPI(configs['URL'], configs['API_TOKEN'])

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
Copyright 2020 Afonso Costa

Licensed under the Apache License, Version 2.0 (the "License");
Type \"license\" for more information.


Welcome to FireflyIII Command Line Interface!
Created by Afonso Costa (@afonsoc12)

===== Status =====
  - URL: {}
  - API Token: {}
  - Connection: {}
  
{}
Type \"help\" to list commands.
    '''.format(configs['URL'] if is_url_set else '(not set)',
               '*****' + configs['API_TOKEN'][-5:] if is_api_token_set else '(not set)',
               'OK!' if api.api_test else 'No connection!',
               opt_text)


    @classmethod
    def refresh_api(cls):
        cls.configs = load_configs()
        cls.api = FireflyAPI(cls.configs['URL'], cls.configs['API_TOKEN'])
        print('API refreshed. Current Status: {}'.format('OK!' if cls.api.api_test else 'No connection!'))

    def do_exit(self, input):
        print('Bye! Come store new transactions soon!')
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    def do_license(self, input):
        print('''
Copyright 2020 Afonso Costa

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
''')

    def help_license(self):
        print('Displays License information')

    def do_refresh(self, input):
        FireflyPrompt.refresh_api()

    def help_refresh(self):
        print('Refreshes API connection')

    def do_edit(self, input):
        input_split = input.split(' ')
        if len(input_split) != 2:
            print(f'The command \"edit\" takes exactly two arguments. Provided: {input}')
        else:
            if input_split[0] == 'URL' or input_split[0] == 'API_TOKEN':
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

    def do_accounts(self, input):
        # TODO: Implement with pagination based
        budgets = self.api.get_budgets()
        pprint(budgets)

    def help_accounts(self):
        print('Shows your accounts.')

    def do_budgets(self, input):
        # TODO: Implement with pagination based
        budgets = self.api.get_budgets()
        pprint(budgets)

    def help_budgets(self):
        print('Shows your budgets.')

    def do_add(self, input):
        try:
            data = parse_transaction_to_df(input)
            self.api.create_transaction(data)
        except:
            print(f'An error has occurred. Your input is not valid.\nInput: {input}')


    def help_add(self):
        print('''
Adds a transaction to Firefly in a comma-separated fashion.

Fields are \"Amount, Description, Source account, Destination account, Category, Budget"
The three first fields can't be omitted.
Examples:
    - A simple one:
        -> `5, Large Mocha, Cash`
    - One with all the fields being used:
        -> `5, Large Mocha, Cash, Starbucks, Coffee Category, Food Budget`
    - You can skip specfic fields by leaving them empty (except the first two):
        -> `5, Large Mocha, Cash, , , UCO Bank`
''')


    def default(self, input):
        if input == 'x' or input == 'q':
            return self.do_exit(input)

        print('{} not recognized. Please type \"help\" to list the available commands'.format(input))

    do_EOF = do_exit
    help_EOF = help_exit


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        FireflyPrompt().onecmd(' '.join(sys.argv[1:]))
    else:
        FireflyPrompt().cmdloop()
