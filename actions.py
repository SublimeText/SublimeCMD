import os

import sublime


CMD_TARGET_APPLICATION = 0
CMD_TARGET_WINDOW = 1
CMD_TARGET_VIEW = 2

CMD_RUN = 'run_'
CMD_KEY = 'key_'
CMD_SET = 'set_'


def str_to_dict(s):
    """Converts a string like 'one:two three:4' into a dict with parsed values
    that's suitable to pass as args to obj.run_command.
    """
    d = {}
    els = s.split(' ')
    for el in els:
        key, value = el.split(':')
        try:
            d['key'] = eval(value, {}, {})
        except NameError:
            d['key'] = value
        
    return d


def run_(cmd):
    target, predicate = cmd['target'], cmd['predicate']

    if cmd['is_query']:
        if cmd['forced']:
            target.run_command('get_all_commands')
        return

    cmd_, _, args = predicate.partition(' ')
    if args:
        args = str_to_dict(args)
    else:
        args = {}

    if not cmd['is_query']:
        target.run_command(str(cmd_), args)


def set_(cmd):
    target, predicate = cmd['target'], cmd['predicate']
    # query
    if cmd['is_query']:
        
        # Plot all settings to new buffer and exit.
        if cmd['forced']:
            syntax = os.path.basename(target.settings().get('syntax'))
            target.run_command('inspect_file_settings', {
                                                'syntax': syntax,
                                                'pattern': predicate
                                                })
            return

        # No setting by that name.
        if not target.settings().has(predicate):
            sublime.status_message('No setting named "%s" found for this object.' % predicate)
            return

        # Print single setting.
        msg = "%s = %s" % (predicate, target.settings().get(predicate))
        sublime.status_message(msg)
        return
    
    # execute
    try:
        name, _, value = predicate.partition(' ')
        target.settings().set(name, eval(value, {}, {}))
        msg = "%s = %s" % (name, target.settings().get(name))
        sublime.status_message(msg)
    except ValueError, e:
        sublime.status_message('Invalid syntax for "set" command.')
        raise e


def key_(args):
    print "Not implemented."