from cryptography.fernet import Fernet




class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}



    def create_key(self,path):
        """
        Create a new encryption key and save it to a file.
        """
        self.key = Fernet.generate_key()
        # print(self.key)
        with open(path, "wb") as f:
            f.write(self.key)


    def load_key(self, path):
        """
        Load the encryption key from a file.
        """
        with open(path, "rb") as f:
            self.key = f.read()



    def create_password_file(self,path,initial_values=None):
        """
        Create a new password file and save it to a file.
        """
        self.password_file = path
        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)


    def load_password_file(self, path):
        """
        Load the password file from a file.
        """
        self.password_file = path
        with open(path,'r') as f:
            for line in f:
                site,encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()



    def add_password(self,site,password):
        """
        Add a new password to the password file.
        """
        self.password_dict[site] = password
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                f.write(f"{site}:{encrypted}\n")
                             
    def get_password(self,site):
        """
        Get the password for a given site.
        """
        return self.password_dict[site]
    

 

def main():

    password = {
        "email": "myemailpassword",
        "facebook": "myfacebookpassword",
        "twitter": "mytwitterpassword",
        "github": "mygithubpassword"
    }

    pm = PasswordManager()


    print("""

    1. Create a new key
          2. Load an existing key
          3. Create a new password file
          4. Load an existing password file
          5. Add a new password
          6. Get a password
          q. Quit
          
          
        """)
    
    done = False

    while not done:

        choice = input("Enter your choice: ")

        if choice == "1":
            path = input("Enter the path to save the key:   ")
            
            pm.create_key(path)

        elif choice == "2":
            path = input("Enter the path to load the key:   ")

            pm.load_key(path)

        elif choice == "3":
            path = input("Enter the path to save the password file:   ")

            pm.create_password_file(path,initial_values=password)
        elif choice == "4":
            path = input("Enter the path to load the password file:   ")

            pm.load_password_file(path)

        elif choice == "5":
            site = input("Enter the site name:   ")
            password = input("Enter the password:   ")

            pm.add_password(site,password)

        elif choice == "6":
            site = input("Enter the site name:   ")

            print(f"The password for {site} is: {pm.get_password(site)}")   

        elif choice == "q":
            done = True
            print("Exiting...")

        else:
            print("Invalid choice. Please try again.")    






if __name__ == "__main__":
    main()

