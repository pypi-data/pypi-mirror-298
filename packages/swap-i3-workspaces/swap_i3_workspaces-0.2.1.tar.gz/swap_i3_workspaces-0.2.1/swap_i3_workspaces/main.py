#!/usr/bin/env python3
import i3ipc
import argparse

def swap_i3_workspaces_with_current(other_workspace_name, current_workspace_name=None):
    i3 = i3ipc.Connection()

    def get_current_workspace():
        return i3.get_tree().find_focused().workspace()

    def focus_ws(ws):
        currentWS = get_current_workspace()
        # Note: If a WS is already in focus trying to focus on it again will actually move the focus to another window!
        if currentWS.name != ws:
            i3.command(f'workspace {ws}')

    # If current_workspace_name is provided, switch to that workspace first
    focus_ws(current_workspace_name)
    current_workspace = get_current_workspace()

    # Get windows in the current workspace
    windows_current = [leaf.window for leaf in current_workspace.leaves()]

    # Get all nodes in the tree and find the target workspace
    tree = i3.get_tree()
    other_workspace = None
    for workspace in tree.workspaces():
        if workspace.name == other_workspace_name:
            other_workspace = workspace
            break

    if not other_workspace:
        print(f"Target workspace {other_workspace_name} not found.")
        return

    # Get windows in the other workspace
    windows_other = [leaf.window for leaf in other_workspace.leaves()]

    def move_windows(windows, to_ws):
        for window in windows:
            i3.command(f'[id={window}] move workspace {to_ws}')

    move_windows(windows_current, other_workspace_name)
    focus_ws(other_workspace_name)
    move_windows(windows_other, current_workspace.name)
    focus_ws(current_workspace.name)

def main():
    parser = argparse.ArgumentParser(description="Swap i3 workspaces.")
    parser.add_argument('--other-workspace', required=True, nargs='+', help="Space-separated list of workspaces to swap with.")
    parser.add_argument('--current-workspace', nargs='+', help="Space-separated list of current workspaces to swap from.")
    args = parser.parse_args()

    other_workspaces = args.other_workspace
    current_workspaces = args.current_workspace

    if len(other_workspaces) >= 1 and len(current_workspaces) >= 1:
        if len(other_workspaces) != len(current_workspaces):
            print("Error: The number of workspaces in --other-workspace and --current-workspace must match when using workspace lists.")
            return

        for other_ws, current_ws in zip(other_workspaces, current_workspaces):
            swap_i3_workspaces_with_current(other_ws.strip(), current_ws.strip())
    elif len(other_workspaces) == 1 and len(current_workspaces) == 0:
        swap_i3_workspaces_with_current(other_workspaces[0].strip(), None)
    else:
        print("Error: The number of workspaces in --current-workspace must be 0 or 1 for specified --other-workspaces.")
        return

if __name__ == "__main__":
    main()
