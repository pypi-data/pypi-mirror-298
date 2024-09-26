#!/usr/bin/env python3
import i3ipc
import argparse

def swap_i3_workspaces_with_current(other_workspace_name, current_workspace_name=None):
    i3 = i3ipc.Connection()

    # If current_workspace_name is provided, switch to that workspace first
    if current_workspace_name:
        i3.command(f'workspace {current_workspace_name}')

    # Get the current workspace
    current_workspace = i3.get_tree().find_focused().workspace()

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
        print("Target workspace not found.")
        return

    # Get windows in the other workspace
    windows_other = [leaf.window for leaf in other_workspace.leaves()]

    def move_windows(windows, to_ws):
        for window in windows:
            i3.command(f'[id={window}] move workspace {to_ws}')

    def focus_ws(ws):
        i3.command(f'workspace {ws}')

    move_windows(windows_current, other_workspace_name)
    focus_ws(other_workspace_name)
    move_windows(windows_other, current_workspace.name)
    focus_ws(current_workspace.name)

def main():
    parser = argparse.ArgumentParser(description="Swap workspaces with the current workspace.")
    parser.add_argument('--other-workspace', required=True, help="The name of the workspace to swap with.")
    parser.add_argument('--current-workspace', help="The name of the workspace to make current before the swap.")
    args = parser.parse_args()

    swap_i3_workspaces_with_current(args.other_workspace, args.current_workspace)

if __name__ == "__main__":
    main()
