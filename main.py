#!/usr/bin/env python3
import os
import sys
from time import sleep
from tools import *  # استيراد جميع الأدوات

# تكوين الشاشة الرئيسية
os.system('clear')
os.system('figlet Fuck_Isreal | lolcat')
print("\033[1;31mFuck Isreal By  : Anonymous Jordan Team\033[0m")
print("\033[1;32mLink  : https://t.me/AnonymousJordan\033[0m\n")

def main_menu():
    # طباعة الخيارات من 1 إلى 50 بشكل منظم
    for i in range(1, 51):
        num = str(i).zfill(2)
        print(f"\033[1;33m[{num}]\033[0m Soon", end="\t" if i%5 !=0 else "\n")
    
    # زر الخروج
    print(f"\n\033[1;31m[99]\033[0m Exit\n")

def main():
    while True:
        main_menu()
        choice = input("\033[1;35mChoose an option: \033[0m")
        
        if choice == '99':
            print("\033[1;31mExiting...\033[0m")
            sleep(1)
            sys.exit()
            
        elif choice.isdigit() and 1 <= int(choice) <= 50:
            tool_num = int(choice)
            print(f"\033[1;33m\nYou selected tool {tool_num:02d}\033[0m")
            # هنا يمكنك إضافة منطق تحميل الأدوات من مجلد tools
            # مثال: tool = getattr(tools, f"tool{tool_num}")
            # tool.run()
            print("\033[1;34mThis tool will be available soon!\033[0m")
            sleep(2)
            os.system('clear')
            
        else:
            print("\033[1;31mInvalid choice! Please try again.\033[0m")
            sleep(1)
            os.system('clear')

if __name__ == "__main__":
    main()
