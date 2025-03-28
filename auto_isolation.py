import os

def isolate_network():
    """ Disables all network interfaces to isolate the system """
    print("\n🚨 Auto-Isolation Activated!\n❌ Disabling all active network interfaces...\n")
    
    os.system("netsh interface set interface name=\"Wi-Fi\" admin=disable")
    os.system("netsh interface set interface name=\"Ethernet\" admin=disable")
    
    print("\n✅ Network has been isolated.\n")

def restore_network():
    """ Restores all disabled network interfaces """
    print("\n🔄 Restoring network interfaces...\n")
    
    os.system("netsh interface set interface name=\"Wi-Fi\" admin=enable")
    os.system("netsh interface set interface name=\"Ethernet\" admin=enable")
    
    print("\n✅ Network has been restored.\n")

def main():
    while True:
        print("""
🔥 Ransomware Defense Toolkit 🔥
---------------------------------
1️⃣  Isolate Network
2️⃣  Restore Network
3️⃣  Exit
        """)

        choice = input("\n🔹 Select an option: ").strip()

        if choice == '1':
            isolate_network()
        elif choice == '2':
            restore_network()
        elif choice == '3':
            print("\n👋 Exiting... Stay safe!\n")
            exit()
        else:
            print("\n⚠️ Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
