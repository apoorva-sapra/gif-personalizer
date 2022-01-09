from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import cv2
import glob
import numpy as np
import os, sys
import shutil
from PIL import Image
from azure.storage.blob import BlobClient, BlobServiceClient, ContentSettings
from PythonApi import settings

blob = BlobClient.from_connection_string(conn_str=settings.CONNECT_STR, container_name="media", blob_name="output")
blob_service_client =  BlobServiceClient.from_connection_string(settings.CONNECT_STR)

def AddGraphicAfterObjectDetection(gifImagePath,reciever_name):
    image = cv2.imread(gifImagePath, -1)
    ret, thresh_gray = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
                                     200, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    for c in contours:
        area = cv2.contourArea(c)
        rect = cv2.minAreaRect(c)
        center = rect[0]
        width, height = rect[1]
        halfWidth = width / 2
        halfHeight = height / 2
        # ( center (x,y), (width, height), angle of rotation ).
        if area > 5000:
            img1 = Image.open(gifImagePath)
            img2 = Image.open('background3.jpg')
            text_on_image = f"Hi {reciever_name}!"
            fontsize = 30
            font = ImageFont.truetype("arial.ttf", fontsize)
            image_editable = ImageDraw.Draw(img2)
            image_editable.text((153, 153), text_on_image, (255, 255, 255), font=font)
            img1.paste(
                img2,
                (round(center[0] - halfWidth), round(center[1] - halfHeight)))
            img1.save(gifImagePath, quality=20, optimize=True)

file_types = [("MP4 (*.mp4)", "*.mp4"), ("All files (*.*)", "*.*")]


def ConvertVideoToJpgFramesAndSave(path):
    video_capture = cv2.VideoCapture(path)
    still_reading, image = video_capture.read()
    frame_count = 0

#     image[image != np.array(None)]
    imageFrame = Image.fromarray(image)

    if blob.exists():
        # remove previous GIF frame files
        # blob.delete_blob("media","output",snapshot=None)
        # blob.delete_blob()
        # shutil.rmtree("output")
        pass
    # try:
    #     os.mkdir("output")
    # except IOError:
    #     sg.popup("Error occurred creating output folder")
    #     return

    # image_content_setting = ContentSettings(content_type='')
    while still_reading:
        # blob.upload_blob(f"output/frame_{frame_count:05d}.jpg", image)
        # image_stream = BytesIO()

        # cv2.imwrite(image_stream, image)
        blob_client = blob_service_client.get_blob_client(container='media', blob=f"output/frame_{frame_count:05d}.jpg")
        blob_client.upload_blob(imageFrame)

        # filename=ds.save(video.name,image)
        # fileurl=ds.open(filename)
        # templateurl=ds.url(filename)

        # blob_client.upload_blob(image,overwrite=True,content_settings=image_content_setting)
        # read next image
        still_reading, image = video_capture.read()
        frame_count += 1


# def make_gif(gif_path, reciever_name, frame_folder="output"):
#     images = glob.glob(f"{frame_folder}/*.jpg")
#     images.sort()
#     for image in images:
#         AddGraphicAfterObjectDetection(image,reciever_name)
#     frames = [Image.open(image) for image in images]
#     frame_one = frames[0]
#     # gif_path += ".gif"
#     frame_one.save(gif_path,
#                    append_images=frames,
#                    save_all=True,
#                    duration=50,
#                    loop=0)


def main():
    video_fullpath = sys.argv[1]
    video_name = sys.argv[2]
    reciever_name=sys.argv[3]
    # img = Image.open(str(video_fullpath))
    # print("img-------->",img)
    gif_name="temp.gif"
    gif_save_path = video_fullpath.replace(video_name, gif_name)
    ConvertVideoToJpgFramesAndSave(video_fullpath)
    # make_gif(gif_save_path,reciever_name)
    return gif_save_path


if __name__ == "__main__":
    gif_save_path=main()
    print(gif_save_path)
