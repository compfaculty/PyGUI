__author__ = 'AlexM'

from Tkinter import *
import tkMessageBox
from ttk import *
from re import match
#local modules
from dsearch import get_asb9_ip
from telnet_asb import *
from scr import DB_PATH, ICON_PATH


logger = logging.getLogger('asb_setup')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s > %(message)s')

# handler to print info from console output to Text widget
class WidgetLogger(logging.Handler):
    def __init__(self, widget):
        logging.Handler.__init__(self)
        self.setLevel(logging.INFO)
        self.widget = widget
        # self.widget.config(state='disabled')

    def emit(self, record):
        self.widget.config(state='normal')
        # Append message (record) to the widget
        self.widget.insert(END, self.format(record) + '\n')
        self.widget.see(END)  # Scroll to the bottom
        # self.widget.config(state='disabled')


class ASB9GUI(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()


    def message(self, title, msg):
        tkMessageBox.showinfo(title, msg)

    def save_last_to_file(self, data, filename=DB_PATH):
        with open(filename, 'a') as storage:
            storage.write(data)

    def read_last_from_file(self, filename=DB_PATH):
        with open(filename, 'a+') as storage:
            lines = storage.readlines()
            if lines:
                for line in reversed(lines):
                    if match(r'^[0-9]{1,3}(?:\.[0-9]{1,3}){3}:[0-9]+$', line):
                        return line.split(":")

    def check_ip_is_correct(self, evn):

        if not match(r'^[0-9]{1,3}(?:\.[0-9]{1,3}){3}$', self.entry_new_IP.get()):
            self.message("IP Error", "You IP is not correct IP!")


    def initialize(self):
        """
        build GUI and widgets
        :return:void
        """

        self.grid()

        # vars
        self.entry_new_IP = StringVar()
        self.entry_port_variable = StringVar()
        self.entry_latronix_IP_variable = StringVar()
        self.textInfo = StringVar()

        # device new IP label
        self.labelIP = Label(self, text="New IP", justify=LEFT)
        self.labelIP.grid(column=0, row=0, padx=3, pady=3)

        #device new IP textfield
        self.entryIP = Entry(self, textvariable=self.entry_new_IP, justify=LEFT)
        self.entryIP.grid(column=1, row=0, padx=3, pady=3, sticky=W + E)
        self.entryIP.bind("<Return>", self.OnPressEnter)
        self.entryIP.bind("<FocusOut>", self.check_ip_is_correct)

        self.entry_new_IP.set(self.read_last_from_file()[0].strip() if self.read_last_from_file() else u"172.27.64.***")

        #device new port label
        self.labelPort = Label(self, text="Port", justify=LEFT)
        self.labelPort.grid(column=0, row=1, padx=3, pady=3)
        #device new textfield
        self.entryPORT = Entry(self, textvariable=self.entry_port_variable)
        self.entryPORT.grid(column=1, row=1, padx=3, pady=3, sticky=W + E)
        self.entry_port_variable.set(self.read_last_from_file()[1].strip() if self.read_last_from_file() else u"12***")

        #device IP in latronix XPort label
        self.labelPortX = Label(self, text="XPort IP", justify=LEFT)
        self.labelPortX.grid(column=0, row=2, padx=3, pady=3)
        #device IP in latronix XPort textfield
        self.entry_latronix_IP = Entry(self, textvariable=self.entry_latronix_IP_variable)
        self.entry_latronix_IP.grid(column=1, row=2, padx=3, pady=3, sticky=W + E)
        # self.entry_latronix_IP_variable.set(u"***.***.***.**")

        #run button
        button = Button(self, text=u"Run", command=self.OnButtonClick)
        button.grid(column=0, row=4, columnspan=2, sticky=W + E)

        #text info panel
        self.text = Text(self, fg="light green", bg="black")
        self.text.grid(column=0, row=3, columnspan=2)

        #self.grid_columnconfigure(0, weight=2)
        self.resizable(False, False)
        self.update()

        #self.geometry(self.geometry())
        self.entryIP.focus_set()
        self.entryIP.selection_range(0, END)

    def OnButtonClick(self):

        res1 = '''Start ASB9 setup -  IP : {0}, port: {1}\n Please wait...\n'''
        res2 = '''{0} is DONE!\n New IP is {1}, port {2}\n'''
        new_ip = self.entry_new_IP.get()
        new_port = self.entry_port_variable.get()
        self.text.insert(END, res1.format(new_ip, new_port))
        self.text.update()
        # logger.info(res1.format(new_ip, new_port))
        dsearch_out = get_asb9_ip()
        latronix_ip = self.entry_latronix_IP_variable.get() or dsearch_out[1].strip()
        self.entry_latronix_IP_variable.set(latronix_ip)

        logger.info(dsearch_out[0])
        # self.entryIP.focus_set()
        # self.entryIP.selection_range(0, END)
        # ####SETUP ASB9#####
        asb9 = ASB9Telnet(latronix_ip, DEFAULT_TELNET_PORT, new_ip, new_port)
        asb9.start_session()
        asb9.set_ip()
        asb9.set_channel1()
        asb9.save()
        ####################


        # self.text.insert(END, res2.format(latronix_ip, new_ip, new_port))


        self.text.see(END)  #makes autoscroll
        self.message("DONE", res2.format(latronix_ip, new_ip, new_port))
        self.save_last_to_file("{0}:{1}\n".format(new_ip, new_port))

    def OnPressEnter(self, event):
        pass
        # self.OnButtonClick()
        # self.lblInfo.set(self.entry_new_IP.get())
        #     self.entryIP.focus_set()
        #     self.entryIP.selection_range(0, END)


if __name__ == "__main__":
    app = ASB9GUI(None)
    w = app.text
    lh = WidgetLogger(w)
    lh.setFormatter(formatter)
    logger.addHandler(lh)
    app.title('ASB9 Setup')
    app.iconbitmap(default=ICON_PATH)
    app.mainloop()

