import env

from common import OpenWithBackup, Logger
from pisettings import PassThrough, SettingClassFactory


class ConfigFileInterface(Logger):

    def __init__(self, location='/boot/config.txt'):

        self.location = location

    def _clean_this_line(self, original_line):

        if original_line is None:
            return ''

        clean_line = str(original_line)

        clean_line = clean_line.strip()

        if not clean_line:
            return ''

        # # ignore commented out lines
        # if clean_line.startswith('#'):
        #     return ''
        # THESE SHOULD JUST BE PASSED THROUGH AS IS

        # strip the line of any inline comments
        if '#' in clean_line.strip()[1:]:
            clean_line = clean_line[:clean_line.index('#')]

            # restrip the line
            clean_line = clean_line.strip()

        return clean_line

    def _clean_this_doc(self, doc):

        # reverse the lines in the doc.
        # the config.txt needs to be read from the bottom up
        doc = doc[::-1]

        clean_doc = []
        for original_line in doc:

            clean = self._clean_this_line(original_line)

            clean_doc.append({'original': original_line, 'clean': clean, 'setting': None})

        return clean_doc

    def _append_unmatched_setting_classes_to_doc(self, clean_doc, _setting_classes):
        # run through the settings again and add any that have not been assigned
        #  to the document with their default values
        for setting in _setting_classes:

            if setting.foundinDoc:
                continue

            setting.set_current_value_to_default()

            clean_doc.append({'original': 'NULL', 'clean': 'NULL', 'setting': setting})

        return clean_doc

    def _assign_setting_classes_to_doc(self, clean_doc, _setting_classes):
        '''
        Goes through the clean doc, assigns a piSetting to each line.
        Settings that are not added to a line are added to the end of the document
        with their default values.
        This ensures that all settings in MASTERSETTINGS are represented in the final doc.
        '''

        for config_line in clean_doc:
            self.log('#' + config_line['clean'])

            # check the config_line against all the settings, exiting loop on first valid find
            for setting in _setting_classes:
                try:
                    setting = setting.extract_setting_from_line(config_line)
                    config_line['setting'] = setting

                    symbol = '==' if str(setting.default_value) == str(setting.current_config_value) else '!='

                    self.log('Assigning -- %s %s %s \n' % (setting.default_value, symbol, setting.current_config_value))

                    break  # go to the next config_line
                except ValueError:
                    pass

            else:  # if no break
                # passthrough the original line to the final document
                self.log('passing through\n')
                config_line['setting'] = PassThrough(name='passthrough')

        return clean_doc

    def extract_setting_classes_from_doc(self, final_doc):

        return {config_line['setting'].name: config_line['setting'].current_config_value for config_line in final_doc}

    def read_config_txt(self):
        '''
        Reads the config.txt found at the provided location and produces a list of config_lines.
        config_lines are dicts containing:
        - the original line from the config.txt
        - a cleaned up version of that line
        - the order the line is found in the config
        - a piSetting instance that has the retrieved validated value

        The final doc contains what will eventually be written to the new config.txt
        '''

        # first step is to use the Master_Setting_classes information to create a list of piSetting instances
        _setting_classes = SettingClassFactory()

        with open(self.location, 'r') as f:
            dirty_doc = f.readlines()

        clean_doc = self._clean_this_doc(dirty_doc)

        clean_doc = self._assign_setting_classes_to_doc(clean_doc, _setting_classes)

        final_doc = self._append_unmatched_setting_classes_to_doc(clean_doc, _setting_classes)

        return final_doc

    def write_config_txt(self, final_doc):
        ''' Backs up the existing config.txt
        Runs through the final doc producing a list of lines to write back to a new config.txt
        '''

        new_lines = []

        for config_line in final_doc:
            setting = config_line['setting']

            # settings that are the default values, and where defaults are suppressed should be ignored
            # (i.e. dont write them to the new config.txt)
            if setting.isDefault and setting.suppress_defaults:
                continue

            # settings that are not changed should just have the original line replicated in the new config.txt
            if not setting.isChanged:
                new_lines.append(config_line['original'])

            # lines for which the values have changed should have the final_line brought in from the piSetting
            new_lines.append(setting.final_line)

        # reverse the lines back to the original order
        new_lines = new_lines[::-1]

        with OpenWithBackup(self.location, 'w') as f:
            f.writelines(new_lines)

    def update_setting_classes(self, final_doc, new_setting_classes):

        for config_line in final_doc:

            setting = config_line['setting']

            setting.set_new_value(new_setting_classes[setting.name])

        return final_doc


if __name__ == "__main__":

    c = ConfigFileInterface('samples\\config_05.txt')

    # doc = c.read_config_txt()

    # res = c.extract_setting_classes_from_doc(doc)

    # self.log('\n\n')

    # pprint(res)
    # self.log('\n\n')

    # for x in doc:
    #     self.log(x['clean'])
    #     pprint(x['setting'].__dict__)
    #     self.log('\n')
