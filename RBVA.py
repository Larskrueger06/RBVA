import cv2 as cv
import time
import numpy as np
from helper import psleep, time_func
import PySimpleGUI as sg

font = cv.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 1
color = (255, 255, 0)
thickness = 2

def capture_video(count, capture):
    frames = []
    for i in range(count):
        text_capture = "filling List"
        window["text"].update(text_capture)
        frames.append(0)

    while True:
        for i in range(count):
            ret, frame = capture.read()
            cv.imshow("name",frame)
            frames[i] = frame
            print(i)
            if cv.waitKey(1) & 0xFF == ord('q'):
                frames[i] = "end"
                capture.release()
                cv.destroyAllWindows()
                return frames

def process_frames(frames):
# TODO: overhaul algorithm
    text_capture = "processing frames"
    window["text"].update(text_capture)
    count = 0
    for frame in frames:
        if type(frame) != str:
            frames.append(frame)
            count += 1
        else:
            break
    for i in range(count+1):
        frames.pop(0)
        print(f"on frame {i} of {len(frames)}")
    for i, frame in enumerate(frames):
        print(f"on frame {i}")
        if type(frame) == int:
            frames.pop(0)
            print(f"pooped {i}")
        else:
            break
    text_capture = "finished"
    window["text"].update(text_capture)


def show_frames(frames):
    for frame in frames:
        cv.imshow("name",frame)
        cv.waitKey(20)
    time.sleep(3)
    cv.destroyWindow("name")


def capture_process(frame_count, capture_video, process_frames):
    frames = capture_video(frame_count, capture)
    process_frames(frames)


    for i, image in enumerate(frames):
        image = cv.putText(image, str(i), org, font, 
                           fontScale, color, thickness, cv.LINE_AA)
        frames[i] = image
    return frame_count, frames
    
def save_frames(capture, frames):
    print("set up saving")
    frame_width = int(capture.get(3)) 
    frame_height = int(capture.get(4)) 
    size = (frame_width, frame_height) 
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    result = cv.VideoWriter('output.avi', fourcc, 20.0, size)
    for frame in frames:
        if result.isOpened():
            result.write(frame)
        else:
            print("Could not start Saving thread")
    print(result.isOpened())
    print("Finished save")
    result.release()
def print_info(capture_info, frames, buffer_size):

    info_window = sg.Window("info", layout_info, size= (500,500), finalize=True)
    text_info = f"Info: Tried to buffer {capture_info} frames and {len(frames)} were captured, thats {(len(frames)/buffer_size)*100}%"
    info_window["info"].update(text_info)

text_capture = "Ready"
text_info = "Info: "
layout = [
    [sg.Button("Capture"), sg.Text(text_capture, key="text")],
    [sg.Button("Show!"), sg.Button("Info")],
    [sg.Button("Exit")],
    [sg.Text("currently not working:")],
    [sg.Button("save")]
]
layout_info = [
    [sg.Text(text_info, key = "info")]
]

window = sg.Window("help", layout, size=(400, 450))

print("Waiting for Capture")
capture = cv.VideoCapture(0)
print("Ready")


buffer_size = 200
while True:
    event, values = window.read()
    print(event, values)
    if event == "Capture":
        frame_count, frames = capture_process(buffer_size, capture_video, process_frames)
    if event == "Show!":
        try:
            show_frames(frames)
        except:
            print("no frames")
    if event == "Info":
        print_info(frame_count, frames, buffer_size)
    if event == "save":
        save_frames(capture, frames)
    if event == "Exit":
        capture.release()
        window.close()
    
    if event == sg.WIN_CLOSED:
        capture.release()
        window.close()
        break

