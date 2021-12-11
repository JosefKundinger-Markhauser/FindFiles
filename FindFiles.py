import os
import sys
import time
import progressbar

EXACT_SEARCH = 1
IN_WHOLE_NAME_SEARCH = 2
IN_FILE_NAME_SEARCH = 3


def search(dir, search_type):
    num_files = 0
    progressbar.streams.wrap_stderr()
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    list_of_files = []

    print("----------------------------------------------------------------------------------------")
    print("Searching: \'" + str(dir) + "\'")
    print()

    start_time = time.time()

    for subdir, dirs, files in os.walk(dir):
        for file in files:
            if search_type == EXACT_SEARCH:
                if searchvalue == file:
                    list_of_files.append(os.path.join(subdir, file))
            elif search_type == IN_WHOLE_NAME_SEARCH:
                if searchvalue in os.path.join(subdir, file):
                    list_of_files.append(os.path.join(subdir, file))
            elif search_type == IN_FILE_NAME_SEARCH:
                if searchvalue in file:
                    list_of_files.append(os.path.join(subdir, file))

            num_files += 1
            bar.update(num_files)

    progressbar.streams.flush()
    print()
    print("DONE Searching " + dir)
    print("Time Taken.............." + str(time.time() - start_time))
    print("Files Checked..........." + str(num_files))
    print("Files Found............." + str(len(list_of_files)))
    print()
    return num_files, list_of_files

def print_results(num_files_checked, list_of_files, start_time):
    print("----------------------------------------------------------------------------------------")
    print("FINISHED")
    print("Total Time Taken........" + str(time.time() - start_time))
    print("Files Checked..........." + str(num_files_checked))
    print("Files Found............." + str(len(list_of_files)))
    print("0. Exit")
    print("1. Print files")
    print("2. Export to File")
    print("3. Print and export to File")
    
    print_files = input(">>>")
    clear_screen()

    if print_files == "1" or print_files == "2" or print_files == "3":
        if print_files == "2" or print_files == "3":
            file_name = input("Please input file name without extension: ")
            f = open(file_name + ".txt", "w")

        for file in list_of_files:
            if print_files == "1" or print_files == "3":
                print(file)
            if print_files == "2" or print_files == "3":
                f.write(file + "\n")
        if print_files == "2" or print_files == "3":
            f.close()
        input(">>>")

    clear_screen()

def clear_screen():
    if os.name == "psix":
        _ = os.system('clear')
    else:
        _ = os.system('cls')
    
def get_search_type():
    clear_screen()
    while 1:
        print("SELECT SEARCH TYPE")
        print()
        print("1. Match the file name exactly")
        print("2. The search value is in the file name")
        print("3. The search value is in the path name")
        temp = input(">>>")
        if temp == "1":
            return EXACT_SEARCH
        elif temp == "2":
            return IN_FILE_NAME_SEARCH
        elif temp == "3":
            return IN_WHOLE_NAME_SEARCH
        else:
            clear_screen()
            print("Invalid type, try agian")

def print_main_menu(drives):
    clear_screen()
    print("MAIN MENU")
    print("0. Exit")
    print("1. Search Custom directory")
    print("2. Search All Hard Drives")
    i = 3
    for dir in drives:
        print(str(i) + ". Search Drive " + dir)
        i += 1
    temp = input(">>>")
    error = False
    try:
        int(temp)
    except:
        error = True

    if error:
        return print_main_menu(drives)
    else:
        if int(temp) - 2 > len(drives):
            return print_main_menu(drives)
        return int(temp)

def get_drives():
    drives = [ chr(x) + ":/" for x in range(65,91) if os.path.exists(chr(x) + ":") ]
    return drives


if __name__ == "__main__":
    root_dir = "C:/"
    exit_bool = False
    drives = get_drives()
    while(not exit_bool):
        clear_screen()
        main_menu = print_main_menu(drives)
        if main_menu == 0 :
            exit_bool = True
            continue
            
        elif main_menu == 1:
            root_dir = input("Enter the root search path: ")
            if os.path.isdir(root_dir):
                searchvalue = input("What would you like to search for: ")
                clear_screen()
                search_type = get_search_type()
                start_time = time.time()
                num_files, list_of_files = search(root_dir, search_type)
                print_results(num_files, list_of_files, start_time)
                
            else:
                print("Invalid Directory")
                input(">>>")
                continue

        elif main_menu == 2:

            searchvalue = input("What would you like to search for: ")
            clear_screen()

            search_type = get_search_type()

            start_time = time.time()
            num_files = 0
            list_of_files = []
            for dir in drives:
                temp_num_files, temp_list_of_files = search(dir, search_type)
                num_files += temp_num_files
                for file in temp_list_of_files:
                    list_of_files.append(file)

            print_results(num_files, list_of_files, start_time)
        elif main_menu > 2:
            root_dir = drives[main_menu-3]
            searchvalue = input("What would you like to search for: ")
            clear_screen()
            search_type = get_search_type()
            start_time = time.time()
            num_files, list_of_files = search(root_dir, search_type)
            print_results(num_files, list_of_files, start_time)