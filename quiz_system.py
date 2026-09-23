import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
con=sqlite3.connect("quiz.db");cur=con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT,question TEXT,a TEXT,b TEXT,c TEXT,d TEXT,answer TEXT)""");con.commit()
def refresh():
    for i in tree.get_children():tree.delete(i)
    for r in cur.execute("SELECT question,a,b,c,d,answer FROM questions"):tree.insert("", "end", values=r)
def add():
    if not all([q.get(),a.get(),b.get(),c.get(),d.get(),ans.get()]):return messagebox.showwarning("Input","Fill all fields.")
    cur.execute("INSERT INTO questions(question,a,b,c,d,answer) VALUES(?,?,?,?,?,?)",(q.get(),a.get(),b.get(),c.get(),d.get(),ans.get().upper()));con.commit();refresh()
def quiz():
    rows=cur.execute("SELECT question,a,b,c,d,answer FROM questions").fetchall()
    if not rows:return messagebox.showinfo("Quiz","No questions available.")
    score=0
    for row in rows:
        answer=messagebox.askquestion("Quiz",row[0]+f"\nA. {row[1]}\nB. {row[2]}\nC. {row[3]}\nD. {row[4]}\n\nClick Yes for A/B/C/D? This demo expects the stored answer letter via the input box.")
        # Use a simple input dialog for the actual answer.
        import tkinter.simpledialog as sd
        user=sd.askstring("Answer","Enter A, B, C or D:")
        if user and user.upper()==row[5].upper():score+=1
    messagebox.showinfo("Result",f"Score: {score}/{len(rows)}")
root=tk.Tk();root.title("Quiz Management System");root.geometry("950x560")
q=tk.StringVar();a=tk.StringVar();b=tk.StringVar();c=tk.StringVar();d=tk.StringVar();ans=tk.StringVar()
f=tk.Frame(root);f.pack(pady=8)
for lab,var in [("Question",q),("A",a),("B",b),("C",c),("D",d),("Answer",ans)]:
    tk.Label(f,text=lab).pack(side="left");tk.Entry(f,textvariable=var,width=12).pack(side="left",padx=2)
tk.Button(f,text="Add Question",command=add).pack(side="left");tk.Button(f,text="Start Quiz",command=quiz).pack(side="left")
tree=ttk.Treeview(root,columns=("Question","A","B","C","D","Answer"),show="headings")
for c0 in ("Question","A","B","C","D","Answer"):tree.heading(c0,text=c0)
tree.pack(fill="both",expand=True,padx=10,pady=10);refresh();root.mainloop()
