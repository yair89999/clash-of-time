import tkinter,json


profile_path = "user data/profile_info.json"

def save_profile(made_profile,profile_info):
    # saves in the json file
    
    what_to_save = {"made profile":made_profile,"profile info":[profile_info]}
    with open(profile_path, "w") as file:
        json.dump(what_to_save, file,  indent=4)

global placed_need_to_text
placed_need_to_text = False
def handle_text(window,text_box):
    global placed_need_to_text
    # save the text and close the window
    username = text_box.get(1.0, "end-1c")
    if username != "" and username.count(" ") != len(username):
        save_profile(True,{"username":username})
        window.destroy()
    else:
        if placed_need_to_text == False:
            text = tkinter.Label(window, text="You must enter a username", font=25,foreground="red")
            text.pack()
            placed_need_to_text = True

def set_profile():
    win = tkinter.Tk()
    
    # change the windown size
    win.geometry("300x150")

    text = tkinter.Label(win, text="Welcome to 'clash of time' ", font=25)
    text.pack()

    text = tkinter.Label(win, text="Username:", font=25)
    text.place(x=10,y=50)

    text_box = tkinter.Text(win, height = 1, width = 20, font=25)
    text_box.place(x=90,y=50)

    button = tkinter.Button(win,text = "Send",command=lambda: handle_text(win,text_box))
    button.place(relx=0.5,y=120, anchor=tkinter.CENTER)
    
    # mainloop, runs infinitely
    tkinter.mainloop()