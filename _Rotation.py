from tkinter import font as tkFont
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
from datetime import datetime
from datetime import timedelta
import sys

import vlc


class MainApp:
    def __init__(self, parent):

        self.Frames = []
        self.AchieveFrames = []
        self.Labels = []
        self.Buttons = []
        self.root = parent
        self.fontSize = 40
        self.fontSizeSmall = 30
        self.fontSizeTiny = 20

        # Load the end times
        self.ending = False
        self.loadEndTimes()
        self.player = vlc.MediaPlayer('Wrapup.mp3')

        '''
        Parent frame, the main window, has
            the 1 column stretches,
            row 0 - title
            row 1 - seperator
            row 2 - content stretches
            row 3 - seperator
            row 4 - achieve
        '''
        parent.columnconfigure(0, weight=1)

        # title frame
        row = 0
        parent.rowconfigure(row, weight=0)
        frame_title = tk.Frame(parent)
        frame_title.grid(
            row=row, column=0, sticky='ew')
        self.Frames.append(frame_title)

        self.Title(frame_title)

        # seperator
        row += 1
        parent.rowconfigure(row, weight=0)
        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(
            row=row, column=0, sticky='ew', padx=10)

        # content frame
        row += 1
        parent.rowconfigure(row, weight=1)
        frame_description = tk.Frame(parent)
        frame_description.grid(
            row=row, column=0, sticky='nsew')
        self.Frames.append(frame_description)

        self.Description(frame_description)

        # seperator
        row += 1
        parent.rowconfigure(row, weight=0)
        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(
            row=row, column=0, sticky='ew', padx=10)

        # achieve frame
        row += 1
        self.AchieveRow = row
        parent.rowconfigure(row, weight=0)
        frame_achieve = tk.Frame(parent)
        frame_achieve.grid(
            row=row, column=0, sticky='ew')
        self.AchieveFrame = frame_achieve
        self.AchieveFrames.append(frame_achieve)

        # load the initial state
        self.LoadState()

        # start the clocks!!!
        self.update_clock()

    def loadEndTimes(self):
        '''
        Loads the current days end times

        Gets the current day of the week

        Catch to see for the TEST day first, else
            loads the current day
        '''
        currentWeekday = datetime.strftime(datetime.now(), "%A")

        with open('./EndTimes.txt', 'r') as endTimes:
            # loop through all of the sections of the file
            for section in endTimes.read().split('\n\n'):
                [weekday, *times] = section.split()
                self.endTimes = []

                # parse the times into datetime objects
                for time in times:
                    date = datetime.now().date()
                    time = datetime.strptime(time, '%H:%M').time()
                    tmp = datetime.combine(date, time)
                    self.endTimes.append(tmp)

                # break the for loop if it is a test OR
                # if it is the proper day
                if 'EndLength' in section:
                    minutes, seconds = [int(i) for i in times[0].split(':')]
                    self.endDuration = timedelta(
                        minutes=minutes, seconds=seconds)

                elif 'TEST' in section:
                    if '#TEST' not in section:
                        print('Test active')
                        print('End times:', self.endTimes)
                        return

                elif currentWeekday in section:
                    return

    def Title(self, parent):
        '''
        All columns, 1 row
        '''
        parent.rowconfigure(0, weight=0)

        # advance button
        col = 0
        parent.columnconfigure(col, weight=0)
        font = tkFont.Font(family='Times', size=self.fontSize)
        advance = tk.Button(text='Advance', font=font,
                            command=self.Advance)
        advance.grid(row=0, column=col, sticky='nsw')
        self.Buttons.append(advance)

        # title
        col += 1
        parent.columnconfigure(col, weight=2)
        font = tkFont.Font(family='Times', size=60,
                           weight=tkFont.BOLD)
        title = tk.Label(parent, text='Title', font=font)
        title.grid(row=0, column=col, sticky='ew')
        self.Title = title
        self.Labels.append(title)

    def Description(self, parent):
        parent.rowconfigure(0, weight=1)

        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)
        parent.columnconfigure(2, weight=0)

        # description box
        font = tkFont.Font(family='Times', size=self.fontSize)
        description = tk.Label(parent, text='Description',
                               font=font, justify='left')
        description.grid(row=0, column=0, sticky='nw',
                         padx=20, pady=20)
        self.Description = description
        self.Labels.append(description)

        ttk.Separator(parent, orient=tk.VERTICAL
                      ).grid(row=0, column=1, sticky='ns')

        # create a seperate frame for all times
        time_frame = tk.Frame(parent)
        time_frame.grid(row=0, column=2, sticky='ns')
        self.Frames.append(time_frame)

        t_row = 0
        font = tkFont.Font(family='Times', size=self.fontSize)
        tmp = tk.Label(time_frame, font=font,
                       text='Time Remaining')
        tmp.grid(row=t_row, column=0, padx=10, sticky='ew')
        self.Labels.append(tmp)

        t_row += 1
        font = tkFont.Font(family='Times', size=100)
        tmp = tk.Button(time_frame, font=font,
                        text='00:00', command=self.timerPause)
        tmp.grid(row=t_row, column=0, sticky='ew')
        self.Buttons.append(tmp)
        self.timerButton = tmp
        self.timerActive = False

        t_row += 1
        tmp = ttk.Separator(time_frame, orient=tk.HORIZONTAL)
        tmp.grid(row=t_row, column=0, sticky='ew')

        t_row += 1
        image1 = Image.open("evil_pup_1.gif")
        photo1 = ImageTk.PhotoImage(image1)
        image2 = Image.open("evil_pup_2.gif")
        photo2 = ImageTk.PhotoImage(image2)
        tmp = tk.Label(time_frame, image=photo1)
        tmp.grid(row=t_row, column=0)
        time_frame.rowconfigure(t_row, weight=1)
        self.Labels.append(tmp)

        tmp.image = photo1

        self.Photo1 = photo1
        self.Photo2 = photo2
        self.PhotoLabel = tmp

        t_row += 1
        tmp = ttk.Separator(time_frame, orient=tk.HORIZONTAL)
        tmp.grid(row=t_row, column=0, sticky='ew')

        t_row += 1
        font = tkFont.Font(family='Times', size=self.fontSize)
        date = datetime.strftime(datetime.now(), "%d %b %H:%M")
        tmp = tk.Label(time_frame, font=font,
                       text=date)
        tmp.grid(row=t_row, column=0)
        self.Labels.append(tmp)
        self.Current_Time = tmp

        # padded seperator
        t_row += 1
        tmp = ttk.Separator(time_frame, orient=tk.HORIZONTAL)
        tmp.grid(row=t_row, column=0, sticky='nsew')

        t_row += 1
        font = tkFont.Font(family='Times', size=self.fontSizeSmall)
        tmp = tk.Label(time_frame, font=font,
                       text='Class ends at: 00:00')
        tmp.grid(row=t_row, column=0)
        self.Labels.append(tmp)
        self.Class_End = tmp

    def Achieve(self, parent, AchieveList):
        # for widget in parent.winfo_children():
        #     widget.destroy()
        self.AchieveFrame.destroy()
        parent = tk.Frame(self.root)
        parent.grid(row=self.AchieveRow, column=0, sticky='ew')

        self.AchieveFrame = parent
        self.AchieveFrames = [parent]

        col = -1

        for stuff in AchieveList:
            [short_name, long_name, description] = stuff
            col += 1
            if col != 0:
                ttk.Separator(parent, orient=tk.VERTICAL).grid(
                    row=0, rowspan=3, column=col, sticky='ns')
                col += 1

            self.Achieve_Column(parent, col,
                                short_name, long_name, description)

        for frame in self.AchieveFrames:
            frame.config(bg=self.Color)

    def Achieve_Column(self, parent, column,
                       short, long, description):

        parent.columnconfigure(column, weight=1)

        font = tkFont.Font(family='Times', size=self.fontSize,
                           weight=tkFont.BOLD)
        tmp = tk.Label(parent, text=short, font=font)
        tmp.grid(row=0, column=column)
        self.AchieveFrames.append(tmp)

        font = tkFont.Font(family='Times', size=self.fontSizeTiny)
        tmp = tk.Label(parent, text=long, font=font)
        tmp.grid(row=1, column=column, sticky='ew')
        self.AchieveFrames.append(tmp)

        font = tkFont.Font(family='Times', size=self.fontSizeSmall)
        tmp = tk.Label(parent, text=description.strip(), font=font)
        tmp.grid(row=2, column=column, sticky='nsew')
        self.AchieveFrames.append(tmp)

    def Advance(self, *events):
        self.timerActive = False
        self.ending = False

        if self.currentStep is 'Bellwork.txt':
            self.LoadState('DistractionFree.txt')
            self.filePlay('DistractionFree.mp3')
            self.timerPause()
        elif self.currentStep is 'DistractionFree.txt':
            self.LoadState('Question.txt')
            self.timerPause()
            self.filePlay('Question.mp3')
            self.player.set_time(26000)
        elif self.currentStep is 'Question.txt':
            self.LoadState('FlexTime.txt')
            self.filePlay('FlexTime.mp3')
            self.timerPause()
        elif self.currentStep is 'Wrapup.txt':
            self.LoadState('Bellwork.txt')
            self.timerPause()
        else:
            self.LoadState('DistractionFree.txt')
            self.filePlay('DistractionFree.mp3')
            self.timerPause()

        self.timerUpdate()

    def LoadState(self, File='Bellwork.txt'):
        self.currentStep = File
        with open(File, 'r') as state_file:
            sections = state_file.read().split(
                '\n--------------------\n')

            for section in sections:
                label, content = section.split(':', 1)

                if label == 'title':
                    self.Title.config(text=content)

                if label == 'duration':
                    self.timerDuration = timedelta(
                        minutes=float(content))
                    self.timerRemaining = self.timerDuration
                    self.timerEnd = (datetime.now()
                                     + self.timerRemaining)
                    self.timerDisplayUpdate(self.timerDuration)

                if label == 'text_color':
                    pass

                if label == 'Achieve':
                    tmp = content.split('\n\n')
                    AchieveList = [i.split('~') for i in tmp[1:]]

                    self.Achieve(self.AchieveFrame,
                                 AchieveList=AchieveList)

                if label == 'Description':
                    self.Description.config(text=content.strip())

                # must set colors last
                if label == 'frame_color':
                    self.Color = content
                    for frame in self.Frames:
                        frame.config(bg=content)
                    for label in self.Labels:
                        label.config(bg=content)
                    for button in self.Buttons:
                        button.config(highlightbackground=content)

    def update_clock(self):
        '''Updates the clock for the current time'''
        date = datetime.strftime(datetime.now(), "%d %b %H:%M")
        self.Current_Time.configure(text=date)

        # update the end time:
        if len(self.endTimes) > 1:
            for endTime in self.endTimes:
                tmp = str(endTime - datetime.now())
                # print('End time tested: ', tmp)
                if '-1 day' in tmp:
                    pass
                else:
                    self.endTime = endTime
                    break
        else:
            self.endTime = self.endTimes[0]

        try:
            self.endTime
        except:
            self.endTime = self.endTimes[0]

        tmp = datetime.strftime(self.endTime, '%H:%M')
        self.Class_End.configure(text='Class ends at: {}'.format(tmp))

        self.root.after(1000, self.update_clock)

        if not self.ending:
            # print('Not ending yet')
            timeLeft = self.endTime - datetime.now()

            # test to see if time left is positive
            cond1 = '-1 Day' not in str(timeLeft)
            # print(str(timeLeft))
            # print('Timeleft positive? ', cond1)

            # test to see if timeLeft is < endDuration
            cond2 = timeLeft.seconds < self.endDuration.seconds
            # print('TimeLeft < endDuration? ', cond2)

            if cond1 and cond2:
                print('Wrapping up!!!')
                self.ending = True
                self.LoadState('Wrapup.txt')
                self.timerPause()
                self.filePlay('Wrapup.mp3')

    def filePlay(self, file):
        self.player.pause()
        self.player = vlc.MediaPlayer(file)
        self.player.play()

    def timerPause(self, *events):
        if self.timerActive == False:
            # start the timer
            self.timerActive = True
            self.timerEnd = datetime.now() + self.timerRemaining
            self.timerUpdate()

        else:
            # stop the timer
            self.timerRemaining = self.timerEnd - datetime.now()
            self.timerActive = False

        # self.timerUpdate()

    def timerUpdate(self):
        self.timerRemaining = self.timerEnd - datetime.now()
        self.timerDisplayUpdate(self.timerRemaining)

        if self.PhotoLabel.image is self.Photo1:
            self.PhotoLabel.config(image=self.Photo2)
            self.PhotoLabel.image = self.Photo2
        else:
            self.PhotoLabel.config(image=self.Photo1)
            self.PhotoLabel.image = self.Photo1

        if '-1 day' in str(self.timerRemaining):
            self.Advance()

        if self.timerActive:
            self.root.after(200, self.timerUpdate)

    def timerDisplayUpdate(self, td):
        text = ' {} '.format(self.timerFormat(td))
        self.timerButton.configure(
            text=text)

    def timerFormat(self, seconds):
        '''Returns a MM:SS string from the seconds
         OR time delta value value given'''
        minutes = str(seconds).split(':')[1]
        seconds = float(str(seconds).split(':')[2])
        text = '{}:{:02.0f}'.format(minutes, seconds)
        return text

    def key(self, event):
        print(event.keysym)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1024x768')
    MainApp(root)
    root.mainloop()

    if sys.platform == 'darwin':
        import resource

        usage = resource.getrusage(
            resource.RUSAGE_SELF).ru_maxrss / 1E6
        print('The memory usage was: {:.0f} mb'.format(usage))
