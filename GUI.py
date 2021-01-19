from tkinter import * 
from tkinter import filedialog, ttk
from tkinter.filedialog import asksaveasfile 
import subprocess as sp
from PIL import Image, ImageTk, ImageOps, ImageFont, ImageDraw


class App(object):
    def __init__(self):
        self.root = Tk()
        self.root.title('Image To Ascii!')

        # Creating elements
        self.canvas = Canvas(self.root, width=1040, height=560)
        #self.ascii_canvas = Frame(self.canvas, width=700, height=450, bg = "SystemButtonFace", bd=2, relief=SUNKEN)
        self.picture_canvas = Frame(self.canvas, width=300, height=200, bg ="SystemButtonFace", bd=2, relief=SUNKEN)
        self.inputs = Frame(self.canvas, width=300, height=250)
        self.label = Label(self.canvas, text="Image to Ascii!", font=("forte", 32))
        self.convert_btn = Button(self.inputs, text = "Convert!", width=8, height=1, command = self.convert_image, font=("forte", 25))
        self.upld_btn = Button(self.inputs, text = "Uplode!", width=8, height=1, command = self.upload_image, font=("forte", 25))

        self.fields = {'Fontsize':[1,2,3,4,5,6,7,8,9,10],
                        'Image width':[160, 320, 480, 640, 800]}
                        #'Invert Image':['NO','YES']} # 'Background':['black', 'white', 'blue', 'green', 'red', 'yellow', 'orange'],
        
        self.attributes = []

    def main(self):

        self.canvas.pack()
        #self.label.place(x=380, y=30)
        #self.ascii_canvas.pack(side=RIGHT, padx=10, pady=10)
        self.picture_canvas.pack(side=TOP, padx=10, pady=10)
        self.inputs.pack(side=TOP, padx=10, pady=10)
        self.convert_btn.pack(side=BOTTOM)
        self.upld_btn.pack(side=BOTTOM)


        self.Menubar()

        entries = self.makeform()
        set_button = Checkbutton(self.inputs, text='Final?', width=8, height=1, font=("Helvetica", 15, 'bold'),command=(lambda e=entries: self.get_values(e, self.attributes)))
        set_button.pack(side=RIGHT, padx=10, pady=20, fill=Y)
        
        #loading = Label(self.canvas, text='converting image...', width=30, bg="SystemButtonFace")
        #loading.place(x=150, y=350)

        self.root.mainloop()


    def makeform(self):
        entries = []
        for field, value in self.fields.items():
            #print('values', value[0])
            row = Frame(self.inputs)
            n = StringVar()
            n.set(value[0])
            #print('n',n.get())
            label = Label(row, width=15, text=field, anchor=W, font=("Helvetica", 10, 'bold'))
            entry = ttk.Combobox(row, width = 20, text=n)
            entry['values'] = (value)
            row.pack(side=TOP, fill=X, padx=50, pady=10, anchor=E)
            entry.pack(side=RIGHT, expand=YES, fill=X)
            label.pack(side=LEFT)
            if entry == "":
                entries.append((field, n.get()))
            entries.append((field, entry))
        return entries

    def get_values(self, entries, attrs):
        for entry in entries:
            field = entry[0]
            value  = entry[1].get()
            attrs.append(value)

    def set_invert(self):
        print('invert button', is_invert.get())
        return is_invert.get()
    
    def set_greyscale(self):
        print('greyscale button', is_greyscale.get())
        return is_greyscale.get()

    def donothing(self):
        filewin = Toplevel(self.root)
        button = Button(filewin, text="Do nothing button")
        button.grid(row=0,column=0, padx=50, pady=50)

    def Menubar(self):
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Action", menu=filemenu) # the name at the top
        filemenu.add_command(label="Open", command=self.upload_image)
        filemenu.add_command(label="Save", command=self.save_image)
        filemenu.add_separator() # draws a line between
        filemenu.add_command(label="Exit", command=self.root.quit)

        global is_invert, is_greyscale
        is_invert = BooleanVar()
        is_invert.set(False)
        is_greyscale = BooleanVar()
        is_greyscale.set(False)
        
        effectsmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Effects", menu=effectsmenu)
        effectsmenu.add_checkbutton(label="Invert", onvalue=1, offvalue=0, variable=is_invert, command=self.set_invert)
        effectsmenu.add_checkbutton(label="Greysacle", onvalue=1, offvalue=0, variable=is_greyscale, command=self.set_greyscale)
        print(is_invert.get(), is_greyscale.get())
        helpmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="Help", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)

        self.root.config(menu=menubar)

    def upload_image(self):
        global filename
        #filename = "C:\Parth\Python\ImageToAsciiApp\images\elliot.jpg"
        self.root.filename = filedialog.askopenfilename(initialdir="/", title="choose a file", filetypes=(("all files", "*.*"),('JPEG', ('*.jpg', '*.jpeg', '*.jpe')), ('PNG', '*.png')))
        filename = self.root.filename
        print(filename)
        i = Image.open(filename)
        new_width = 300
        new_height = 200 #int(height/width * new_width * 0.5)
        i = i.resize((new_width, new_height))
        render = ImageTk.PhotoImage(i)
        img = Label(self.picture_canvas, image=render, bg='SystemButtonFace')
        img.image = render
        img.place(x=0, y=0)
            
    def convert_image(self):
        global textfilename
        
        imgpath = filename
        extension = imgpath.split('.')
        print(imgpath, filename, extension[-1])
        textfilename = imgpath[:-len(extension[1])]+'txt'
        print('text file', textfilename)

        img = Image.open(imgpath)
        if self.set_invert() == True:
            print('converting image to invert')
            inverted_img = ImageOps.invert(img)
            img = inverted_img        
        if self.set_greyscale() == True:
            print('converting image to greyscale')
            img = img.convert('L')

        width, height = img.size
        new_width = 300 #int(self.attributes[1])
        new_height = height/width * new_width * 0.5
        img = img.resize((new_width, int(new_height)))
        img = img.convert('L')
        pixels = img.getdata()
        #chars = 'X # % M $ S = . ` : , @ *'
        chars = '# h % X $ s , . ` " * +'
        chars = chars.split()
        #for p in range(10): print(pixels[p], pixels[p]//10, chars[pixels[p]//10])
        new_pixels = [chars[pixel//26] for pixel in pixels]
        new_pixels = ''.join(new_pixels)

        new_pixels_count = len(new_pixels)
        ascii_image = [new_pixels[index: index + new_width] for index in range(0, new_pixels_count, new_width)]
        ascii_image = '\n'.join(ascii_image)
        # imgpath[:-len(extension[1])] for getting the length of the extension and making a file removing the extension
        with open(textfilename, 'w') as f:
            f.write(ascii_image)

        programName = "notepad.exe"
        sp.call([programName, textfilename])

    def save_image(self):
        
        PIXEL_ON = 0  # PIL color to use for "on"
        PIXEL_OFF = 255  # PIL color to use for "off"
        def main():
            file_saveas_name = textfilename[:-4]
            print('file saveas name', str(file_saveas_name+'_ascii.jpg'))
            image = text2image()
            image.show()
            image.save(str(file_saveas_name+'_ascii.jpg'))
            

        def text2image(font_path=None):
            grayscale = 'L'
            
            with open(textfilename) as text_file:  # can throw FileNotFoundError
                lines = tuple(l.rstrip() for l in text_file.readlines())
           
            large_font = 10 #int(self.attributes[0])
            font_path = font_path or 'cour.ttf'
            try:
                font = ImageFont.truetype(font_path, size=large_font)
            except IOError:
                font = ImageFont.load_default()
                
            convert2pixel = lambda p: int(round(p * 96.0 / 72))  # convert points to pixels
            max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
            # max height is adjusted down because it's too large visually for spacing
            test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            max_height  = convert2pixel(font.getsize(test_string)[1])
            max_width   = convert2pixel(font.getsize(max_width_line)[0])
            height      = max_height * len(lines)  # perfect or a little oversized
            width       = int(round(max_width + 40))  # a little oversized
            image       = Image.new(grayscale, (width, height), color=PIXEL_OFF)
            draw        = ImageDraw.Draw(image)

            # draw each line of text
            vertical_position = 5
            horizontal_position = 5
            line_spacing = int(round(max_height*0.9))  # reduced spacing seems better
            for line in lines:
                draw.text((horizontal_position, vertical_position),line, fill=PIXEL_ON, font=font)
                vertical_position += line_spacing
            # crop the text
            c_box = ImageOps.invert(image).getbbox()
            image = image.crop(c_box)
            return image
        return main()

app = App()
if __name__  == "__main__":
    app.main()