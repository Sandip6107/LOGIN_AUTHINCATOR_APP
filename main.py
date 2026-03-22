import tkinter as tk
from tkinter import messagebox, ttk
import auth
from db import execute_query

class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Login Authentication System")
        self.root.geometry("450x600")
        self.root.configure(bg="#f0f2f5")
        self.current_user = None
        
        # UI Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", padding=6, relief="flat", background="#1877f2", foreground="white", font=("Arial", 10, "bold"))
        self.style.map("TButton", background=[('active', '#166fe5')])
        
        self.main_container = tk.Frame(root, bg="#ffffff", padx=40, pady=40, highlightbackground="#dddfe2", highlightthickness=1)
        self.main_container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=550)
        
        self.show_login()

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_container()
        
        tk.Label(self.main_container, text="Login", font=("Arial", 24, "bold"), bg="#ffffff", fg="#1c1e21").pack(pady=(0, 20))
        
        tk.Label(self.main_container, text="Email", bg="#ffffff", fg="#606770").pack(anchor="w")
        self.email_entry = tk.Entry(self.main_container, font=("Arial", 12), bd=1, relief="solid")
        self.email_entry.pack(fill="x", pady=(5, 15), ipady=8)
        
        tk.Label(self.main_container, text="Password", bg="#ffffff", fg="#606770").pack(anchor="w")
        self.password_entry = tk.Entry(self.main_container, font=("Arial", 12), bd=1, relief="solid", show="*")
        self.password_entry.pack(fill="x", pady=(5, 15), ipady=8)
        
        login_btn = ttk.Button(self.main_container, text="Log In", command=self.handle_login)
        login_btn.pack(fill="x", pady=10)
        
        tk.Button(self.main_container, text="Forgotten password?", bg="#ffffff", fg="#1877f2", bd=0, cursor="hand2", command=self.show_forgot_password).pack()
        
        tk.Frame(self.main_container, height=1, bg="#dddfe2").pack(fill="x", pady=20)
        
        reg_btn = tk.Button(self.main_container, text="Create new account", bg="#42b72a", fg="white", font=("Arial", 12, "bold"), 
                            padx=20, pady=10, bd=0, cursor="hand2", command=self.show_register)
        reg_btn.pack()

    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return
            
        user, msg = auth.login_user(email, password)
        if user:
            self.current_user = user
            messagebox.showinfo("Success", msg)
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", msg)

    def show_register(self):
        self.clear_container()
        
        tk.Label(self.main_container, text="Sign Up", font=("Arial", 24, "bold"), bg="#ffffff", fg="#1c1e21").pack(pady=(0, 10))
        tk.Label(self.main_container, text="It's quick and easy.", bg="#ffffff", fg="#606770").pack(pady=(0, 20))
        
        tk.Label(self.main_container, text="Full Name", bg="#ffffff", fg="#606770").pack(anchor="w")
        self.name_reg = tk.Entry(self.main_container, font=("Arial", 12), bd=1, relief="solid")
        self.name_reg.pack(fill="x", pady=(2, 10), ipady=5)
        
        tk.Label(self.main_container, text="Email", bg="#ffffff", fg="#606770").pack(anchor="w")
        self.email_reg = tk.Entry(self.main_container, font=("Arial", 12), bd=1, relief="solid")
        self.email_reg.pack(fill="x", pady=(2, 10), ipady=5)
        
        tk.Label(self.main_container, text="Mobile", bg="#ffffff", fg="#606770").pack(anchor="w")
        self.mobile_reg = tk.Entry(self.main_container, font=("Arial", 12), bd=1, relief="solid")
        self.mobile_reg.pack(fill="x", pady=(2, 10), ipady=5)
        
        tk.Label(self.main_container, text="Password", bg="#ffffff", fg="#606770").pack(anchor="w")
        self.pass_reg = tk.Entry(self.main_container, font=("Arial", 12), bd=1, relief="solid", show="*")
        self.pass_reg.pack(fill="x", pady=(2, 10), ipady=5)
        
        reg_btn = tk.Button(self.main_container, text="Sign Up", bg="#00a400", fg="white", font=("Arial", 12, "bold"), 
                            pady=10, bd=0, cursor="hand2", command=self.handle_register)
        reg_btn.pack(fill="x", pady=10)
        
        tk.Button(self.main_container, text="Already have an account?", bg="#ffffff", fg="#1877f2", bd=0, cursor="hand2", command=self.show_login).pack()

    def handle_register(self):
        name = self.name_reg.get()
        email = self.email_reg.get()
        mobile = self.mobile_reg.get()
        password = self.pass_reg.get()
        
        if not all([name, email, mobile, password]):
            messagebox.showerror("Error", "All fields are required")
            return
            
        success, msg = auth.register_user(name, email, mobile, password)
        if success:
            messagebox.showinfo("Success", msg)
            self.show_login()
        else:
            messagebox.showerror("Registration Failed", msg)

    def show_forgot_password(self):
        self.clear_container()
        tk.Label(self.main_container, text="Find Your Account", font=("Arial", 20, "bold"), bg="#ffffff", fg="#1c1e21").pack(pady=(0, 10))
        tk.Label(self.main_container, text="Enter your email to search for your account.", bg="#ffffff", fg="#606770", wraplength=300).pack(pady=(0, 20))
        
        self.forgot_email = tk.Entry(self.main_container, font=("Arial", 12), bd=1, relief="solid")
        self.forgot_email.pack(fill="x", pady=(0, 20), ipady=8)
        
        btn_frame = tk.Frame(self.main_container, bg="#ffffff")
        btn_frame.pack(fill="x")
        
        tk.Button(btn_frame, text="Cancel", bg="#e4e6eb", fg="#4b4f56", font=("Arial", 10, "bold"), bd=0, padx=15, pady=8, command=self.show_login).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Search", bg="#1877f2", fg="white", font=("Arial", 10, "bold"), bd=0, padx=15, pady=8, command=self.handle_forgot_password).pack(side="right", padx=5)

    def handle_forgot_password(self):
        email = self.forgot_email.get()
        # Simple simulation of forgot password for now as per requirements logic
        query = "SELECT * FROM users WHERE email = %s"
        user = execute_query(query, (email,), fetch=True)
        if user:
            messagebox.showinfo("Reset Sent", "If this email exists, a reset link will be simulated. (Feature in progress)")
            self.show_login()
        else:
            messagebox.showerror("Error", "No account found with that email.")

    def show_dashboard(self):
        self.clear_container()
        role = self.current_user['role']
        name = self.current_user['full_name']
        
        tk.Label(self.main_container, text=f"Welcome, {name}!", font=("Arial", 18, "bold"), bg="#ffffff", fg="#1c1e21").pack(pady=(0, 10))
        tk.Label(self.main_container, text=f"Role: {role.capitalize()}", font=("Arial", 12), bg="#ffffff", fg="#606770").pack(pady=(0, 20))
        
        if role == 'admin':
            tk.Label(self.main_container, text="Admin Actions:", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w")
            tk.Button(self.main_container, text="View All Users", bg="#e4e6eb", bd=0, pady=10, command=self.view_users).pack(fill="x", pady=5)
        
        tk.Button(self.main_container, text="Log Out", bg="#f02849", fg="white", font=("Arial", 12, "bold"), pady=10, bd=0, command=self.show_login).pack(fill="x", pady=20)

    def view_users(self):
        users = execute_query("SELECT full_name, email, role, status FROM users", fetch=True)
        user_list = "\n".join([f"{u['full_name']} ({u['email']}) - {u['role']}" for u in users])
        messagebox.showinfo("User List", user_list if user_list else "No users found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthApp(root)
    root.mainloop()
