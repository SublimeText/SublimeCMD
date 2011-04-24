import actions
import sublime


def starts_with_any(s, seq):
    return any(map(s.startswith, seq))


def ends_with_any(s, seq):
    return any(map(s.endswith, seq))


def parse_cmd(view, cmd):
    parsed_cmd = {}

    cmd_, _, predicate = cmd.partition(' ')
    if not predicate: raise ValueError("Bad command syntax.")

    is_query = is_forced = target_type = action_type = 0

    if cmd_.endswith('?'):
        is_query = True
        cmd_ = cmd_[:-1]
    
    if cmd_.endswith('!'):
        is_forced = True
        cmd_ = cmd_[:-1]
    
    if ends_with_any(cmd_, [':w', ':a']):
        if cmd_.endswith('w'):
            target_type = actions.CMD_TARGET_WINDOW
        else:
            target_type  = actions.CMD_TARGET_APPLICATION
        
        cmd_ = cmd_[:-2]
    else:
        target_type = actions.CMD_TARGET_VIEW
    
    if starts_with_any(cmd_, ['set', 'run', 'key']):
        if cmd_.startswith('set'):
            action_type = actions.CMD_SET
        elif cmd_.startswith('run'):
            action_type = actions.CMD_RUN
        else:
            action_type = actions.CMD_KEY
    
    if target_type == actions.CMD_TARGET_VIEW:
        target = view
    if target_type == actions.CMD_TARGET_WINDOW:
        target = view.window()
    if target_type == actions.CMD_TARGET_APPLICATION:
        target = sublime

    return {
        'cmd': action_type,
        'target_type': target_type,
        'forced': is_forced,
        'is_query': is_query,
        'predicate': predicate,
        'target': target
    }


def parse_and_dispatch(view, raw_cmd):
    """Parses a command and dispatches it.
    """

    if starts_with_any(raw_cmd, ('r!', '!')):
        if raw_cmd.startswith('!'):
            view.run_command("run_powershell", {"command": raw_cmd[1:],
                                                "as_filter": False})
        else:
            view.run_command("run_powershell", {"command": raw_cmd[2:]})
        return
    
    if not starts_with_any(raw_cmd, ['set', 'key', 'run']):
        view.run_command("uber_selection", {"command": raw_cmd})
        return

    try:
        parsed_cmd = parse_cmd(view, raw_cmd)
        cmd = getattr(actions, parsed_cmd['cmd'])
        cmd(parsed_cmd)
    except ValueError, e:
        sublime.status_message(e.message)