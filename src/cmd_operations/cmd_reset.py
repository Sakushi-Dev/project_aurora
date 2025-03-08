import os
import time
import shutil
import errno

from globals import console, get_path, get_file


def execute_reset():
    
    # Get all paths for reset
    set_p   = get_path("set")
    slot_p  = get_path("hist")
    user_p  = get_path("user_spec")
    mem_p   = get_path("mem")
    costs_p = get_path("cost")
    last_p  = get_path("l_msg")
    cache   = get_path("cache_l")
    # Get all files for reset
    emo_f   = get_file("emo_score")

    os.system('cls' if os.name == 'nt' else 'clear')
    
    console.print(
        "[red]Warning! Do you really want to reset [orange1]Aurora[/orange1]?[/red]\n"
        "[orange1]Info:[/orange1] All dialogues and settings will be deleted.\n"
        "API key will be preserved, but can also be deleted if desired.\n"
        )
    reset = ""

    reset = console.input("[red]Do you want to perform a reset? (Y/N): [/red]")
    if reset.lower() == "y":

        # Safety confirmation
        reset = console.input("[red]Are you sure? (Y/N): [/red]")
        if reset.lower() == "y":

            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')


            route_map = {
                "Dialogue costs": costs_p, 
                "Times for 'Impatience'": last_p,
                "Emotion score data": emo_f,
                "Settings": set_p,
                "User data": user_p,
                "Chat history": slot_p,
                "Memories": mem_p,
            }
            
            # Deleting files
            for key, value in route_map.items():
                try:
                    if os.path.isdir(value):
                        # Use shutil.rmtree with error handler for Windows permission issues
                        def handle_remove_readonly(func, path, exc):
                            # Handle permission issues
                            if func in (os.rmdir, os.remove, os.unlink) and exc[1].errno == errno.EACCES:
                                # Change file to be readable, writable, and executable for all
                                os.chmod(path, 0o777)
                                # Retry
                                func(path)
                            else:
                                raise exc
                        
                        # Try to remove the directory tree
                        shutil.rmtree(value, onerror=handle_remove_readonly)
                    elif os.path.isfile(value):
                        try:
                            os.remove(value)
                        except PermissionError:
                            # If permission error, change permissions and try again
                            os.chmod(value, 0o777)
                            os.remove(value)

                    console.print(f"\n[orange1]Deleting {key} in progress[/orange1]", end="")
                    for i in range(0, 3):
                        console.print(f"[red].[/red]", end="")
                        time.sleep(0.7)
                    console.print(f"\n[green]{key} deleted.[/green]")
                except FileNotFoundError:
                    console.print(f"\n[red]{key} not found.[/red]")
                except Exception as e:
                    console.print(f"\n[red]Error deleting {key}: {str(e)}[/red]")

            # Deleting '__pycache__' with platform-specific commands
            try:
                for path in cache:
                    if os.name == 'nt':  # Windows
                        try:
                            # First try with Python's built-in methods for better error handling
                            if os.path.exists(path):
                                shutil.rmtree(path, onerror=handle_remove_readonly)
                        except Exception:
                            # Fallback to system command
                            os.system(f'rmdir /s /q "{path}"')
                    else:  # Unix/Linux/MacOS
                        os.system(f'rm -r "{path}"')
                
                console.print("\n[green]Cache deleted.[/green]")
            except FileNotFoundError:
                console.print("\n[red]Cache not found.[/red]")
            except Exception as e:
                console.print(f"\n[red]Error deleting cache: {str(e)}[/red]")

            console.print("[orange]Deletion process completed.[/orange]")
            
            #==================================================================================================

            # Ask if API key should be deleted

            api_key = console.input("[red]Do you want to delete the API key? (Y/N): [/red]")
            if api_key.lower() == "y":
                # Delete API key file
                try:
                    os.remove("./API/api_key.env")
                    os.rmdir("./API")
                    console.print("[orange]API key deleted.[/orange]")
                except Exception as e:
                    console.print(f"[red]Error deleting API key: {str(e)}[/red]")
            else:
                console.print("[green]API key preserved.[/green]")
                
            
            os.system('cls' if os.name == 'nt' else 'clear')

            while True:
                choice = console.input(
                    "[green]Enter [orange1]1[/orange1] to restart Aurora"
                    "\nIf you want to exit, enter [orange1]2[/orange1]: [/green]"
                    )
                if choice == "1":
                    return "reset"
                elif choice == "2":
                    os._exit(0)
                else:
                    console.print("[red]Invalid input![/red]")
                    continue
        else:
            return "cancel"
    else:
        return "cancel"