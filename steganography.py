from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from PIL import ImageTk, Image
from tkinter import messagebox
from io import BytesIO
import os

class Stegno:
    output_image_size = 0

    def main(self, root):
        root.title('Image Steganography')
        root.geometry('500x600')
        root.resizable(width=False, height=False)
        root.configure(bg='#003366')  # Deep blue background

        f = Frame(root, bg='#003366')
        f.pack(fill=BOTH, expand=True)

        title = Label(f, text='Image Steganography', bg='#003366', fg='white')
        title.config(font=('Courier', 28))
        title.pack(pady=20)

        b_encode = Button(f, text="Encode", command=lambda: self.frame1_encode(f), padx=14, bg='#00509E', fg='white')
        b_encode.config(font=('Courier', 14))
        b_encode.pack(pady=10)

        b_decode = Button(f, text="Decode", command=lambda: self.frame1_decode(f), padx=14, bg='#00509E', fg='white')
        b_decode.config(font=('Courier', 14))
        b_decode.pack(pady=10)

    def home(self, frame):
        frame.destroy()
        self.main(root)

    def frame1_decode(self, f):
        f.destroy()
        d_f2 = Frame(root, bg='#003366')
        l1 = Label(d_f2, text='Select Image with Hidden Text:', bg='#003366', fg='white')
        l1.config(font=('Courier', 18))
        l1.pack(pady=10)

        bws_button = Button(d_f2, text='Select', command=lambda: self.frame2_decode(d_f2), bg='#00509E', fg='white')
        bws_button.config(font=('Courier', 18))
        bws_button.pack(pady=10)

        back_button = Button(d_f2, text='Cancel', command=lambda: Stegno.home(self, d_f2), bg='#00509E', fg='white')
        back_button.config(font=('Courier', 18))
        back_button.pack(pady=15)

        d_f2.pack(fill=BOTH, expand=True)

    def frame2_decode(self, d_f2):
        d_f3 = Frame(root, bg='#003366')
        myfile = tkinter.filedialog.askopenfilename(filetypes=[('PNG', '.png'), ('JPEG', '.jpeg'), ('JPG', '.jpg'), ('All Files', '.*')])
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            # Convert to RGB so we always get 3 channels for stego logic
            myimg = Image.open(myfile, 'r').convert('RGB')
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            l4 = Label(d_f3, text='Selected Image:', bg='#003366', fg='white')
            l4.config(font=('Courier', 18))
            l4.pack(pady=10)

            panel = Label(d_f3, image=img, bg='#003366')
            panel.image = img
            panel.pack()

            hidden_data = self.decode(myimg)
            l2 = Label(d_f3, text='Hidden Data is:', bg='#003366', fg='white')
            l2.config(font=('Courier', 18))
            l2.pack(pady=10)

            text_area = Text(d_f3, width=50, height=10, font=('Courier', 12))
            text_area.insert(INSERT, hidden_data)
            text_area.configure(state='disabled')
            text_area.pack(pady=10)

            back_button = Button(d_f3, text='Cancel', command=lambda: self.page3(d_f3), bg='#00509E', fg='white')
            back_button.config(font=('Courier', 11))
            back_button.pack(pady=15)

            show_info = Button(d_f3, text='More Info', command=self.info, bg='#00509E', fg='white')
            show_info.config(font=('Courier', 11))
            show_info.pack(pady=10)

            d_f3.pack(fill=BOTH, expand=True)
            d_f2.destroy()

    def decode(self, image):
        data = ''
        imgdata = iter(image.getdata())

        while True:
            pixels = [value for value in next(imgdata)[:3] +
                      next(imgdata)[:3] +
                      next(imgdata)[:3]]
            binstr = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'

            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                return data

    def frame1_encode(self, f):
        f.destroy()
        f2 = Frame(root, bg='#003366')
        l1 = Label(f2, text='Select the Image in which \nyou want to hide text:', bg='#003366', fg='white')
        l1.config(font=('Courier', 18))
        l1.pack(pady=10)

        bws_button = Button(f2, text='Select', command=lambda: self.frame2_encode(f2), bg='#00509E', fg='white')
        bws_button.config(font=('Courier', 18))
        bws_button.pack(pady=10)

        back_button = Button(f2, text='Cancel', command=lambda: Stegno.home(self, f2), bg='#00509E', fg='white')
        back_button.config(font=('Courier', 18))
        back_button.pack(pady=15)

        f2.pack(fill=BOTH, expand=True)

    def frame2_encode(self, f2):
        ep = Frame(root, bg='#003366')
        myfile = tkinter.filedialog.askopenfilename(filetypes=[('PNG', '.png'), ('JPEG', '.jpeg'), ('JPG', '.jpg'), ('All Files', '.*')])
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            # Convert to RGB so we always get 3 channels for stego logic
            myimg = Image.open(myfile).convert('RGB')
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            l3 = Label(ep, text='Selected Image:', bg='#003366', fg='white')
            l3.config(font=('Courier', 18))
            l3.pack(pady=10)

            panel = Label(ep, image=img, bg='#003366')
            panel.image = img
            self.output_image_size = os.stat(myfile)
            self.o_image_w, self.o_image_h = myimg.size
            panel.pack()

            l2 = Label(ep, text='Enter the Message:', bg='#003366', fg='white')
            l2.config(font=('Courier', 18))
            l2.pack(pady=10)

            text_area = Text(ep, width=50, height=10, font=('Courier', 12))
            text_area.pack(pady=10)

            encode_button = Button(ep, text='Cancel', command=lambda: Stegno.home(self, ep), bg='#00509E', fg='white')
            encode_button.config(font=('Courier', 11))
            encode_button.pack(pady=10)

            back_button = Button(ep, text='Encode', command=lambda: [self.enc_fun(text_area, myimg), Stegno.home(self, ep)], bg='#00509E', fg='white')
            back_button.config(font=('Courier', 11))
            back_button.pack(pady=15)

            ep.pack(fill=BOTH, expand=True)
            f2.destroy()

    def info(self):
        try:
            info_str = 'Original Image:\nSize: {:.2f} MB\nWidth: {}\nHeight: {}\n\n' \
                       'Decoded Image:\nSize: {:.2f} MB\nWidth: {}\nHeight: {}'.format(
                self.output_image_size.st_size / 1000000,
                self.o_image_w, self.o_image_h,
                self.d_image_size / 1000000,
                self.d_image_w, self.d_image_h
            )
            messagebox.showinfo('Info', info_str)
        except:
            messagebox.showinfo('Info', 'Unable to get the information')

    def genData(self, data):
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

    def modPix(self, pix, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)
        for i in range(lendata):
            pix = [value for value in next(imdata)[:3] +
                   next(imdata)[:3] +
                   next(imdata)[:3]]
            for j in range(0, 8):
                if (datalist[i][j] == '0') and (pix[j] % 2 != 0):
                    pix[j] -= 1
                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1

            if (i == lendata - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, newimg, data):
        w = newimg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modPix(newimg.getdata(), data):
            newimg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def enc_fun(self, text_area, myimg):
        data = text_area.get("1.0", "end-1c")
        if len(data) == 0:
            messagebox.showinfo("Alert", "Kindly enter text in TextBox")
        else:
            newimg = myimg.copy()
            self.encode_enc(newimg, data)
            save_path = tkinter.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[('PNG', '*.png')])
            if save_path:
                newimg.save(save_path)
                self.d_image_size = os.stat(save_path)
                self.d_image_w, self.d_image_h = newimg.size
                messagebox.showinfo("Success", "Encoding Successful\nFile saved successfully.")

    def page3(self, frame):
        frame.destroy()
        self.main(root)

root = Tk()
o = Stegno()
o.main(root)
root.mainloop()
