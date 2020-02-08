import argparse
from sys import platform

from models import *  # set ONNX_EXPORT in models.py
from utils.datasets import *
from utils.utils import *

import torch
import time
import datetime
import numpy
import boto3
s3 = boto3.client('s3')

def detect(save_img=False):
    img_size = (320, 192) if ONNX_EXPORT else opt.img_size  # (320, 192) or (416, 256) or (608, 352) for (height, width)
    out, source, weights, half, view_img, save_txt = opt.output, opt.source, opt.weights, opt.half, opt.view_img, opt.save_txt
    webcam = source == '0' or source.startswith('rtsp') or source.startswith('http') or source.endswith('.txt')

    # Initialize
    device = torch_utils.select_device(device='cpu' if ONNX_EXPORT else opt.device)
    if os.path.exists(out):
        shutil.rmtree(out)  # delete output folder
    os.makedirs(out)  # make new output folder

    # Initialize model
    model = Darknet(opt.cfg, img_size)

    # Load weights
    attempt_download(weights)
    if weights.endswith('.pt'):  # pytorch format
        model.load_state_dict(torch.load(weights, map_location=device)['model'])
    else:  # darknet format
        load_darknet_weights(model, weights)

    # Second-stage classifier
    classify = False
    if classify:
        modelc = torch_utils.load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model'])  # load weights
        modelc.to(device).eval()

    # Fuse Conv2d + BatchNorm2d layers
    # model.fuse()

    # Eval mode
    model.to(device).eval()

    # Export mode
    if ONNX_EXPORT:
        img = torch.zeros((1, 3) + img_size)  # (1, 3, 320, 192)
        torch.onnx.export(model, img, 'weights/export.onnx', verbose=False, opset_version=10)

        # Validate exported model
        import onnx
        model = onnx.load('weights/export.onnx')  # Load the ONNX model
        onnx.checker.check_model(model)  # Check that the IR is well formed
        print(onnx.helper.printable_graph(model.graph))  # Print a human readable representation of the graph
        return

    # Half precision
    half = half and device.type != 'cpu'  # half precision only supported on CUDA
    if half:
        model.half()

    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        view_img = True
        torch.backends.cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=img_size, half=half)
    else:
        save_img = True
        dataset = LoadImages(source, img_size=img_size, half=half)

    # Get names and colors
    names = load_classes(opt.names)
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]
    print("here are the things yolov3 can detect right now:  " + str(names))

    #set the start time before counting
    time_now = datetime.datetime.now()
    cooldown = datetime.datetime.now()
    oldc = 3
    c=23232
    pressbutton = 0

    # Run inference
    t0 = time.time()
    for path, img, im0s, vid_cap in dataset:
        t = time.time()

        # Get detections
        img = torch.from_numpy(img).to(device)
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        pred = model(img)[0]

        if opt.half:
            pred = pred.float()

        # Apply NMS
        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)

        # Apply Classifier
        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            if webcam:  # batch_size >= 1
                p, s, im0 = path[i], '%g: ' % i, im0s[i]
            else:
                p, s, im0 = path, '', im0s

            save_path = str(Path(out) / Path(p).name)
            s += '%gx%g ' % img.shape[2:]  # print string
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                #add detection class to  Print results, c is the class which can be detected, n is the number of that class which have detected
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections number per class
                    s += '%g %ss, ' % (n, names[int(c)])  # add to string   , names is the class name list, c is just the index of the class

                # # Write results
                # for *xyxy, conf, cls in det:
                #     if save_txt:  # Write to file
                #         with open(save_path + '.txt', 'a') as file:
                #             file.write(('%g ' * 6 + '\n') % (*xyxy, cls, conf))
                #
                #     if save_img or view_img:  # Add bbox to image
                #         label = '%s %.2f' % (names[int(cls)], conf)
                #         plot_one_box(xyxy, im0, label=label, color=colors[int(cls)])

            # Print time (inference + NMS)
            # print('%sDone. (%.3fs)' % (s, time.time() - t))


            # #when detect nothing, det will become none
            # det = torch.tensor(
            #     [
            #         [229.00000, 230.00000, 520.00000, 425.00000, 0.98815, 100.00000],
            #         [185.00000, 139.00000, 345.00000, 399.00000, 0.97173, 99.00000]
            #     ]
            #     , device='cuda:0')


            #when detect human
            if c != oldc:
                # print(int(c))
                #check the first class of the detection class,since if it
                oldc = c

            if cv2.waitKey(1) & 0xFF == ord("s"):
                pressbutton = 1
                print('press "s" ')
            elif cv2.waitKey(1) & 0xFF == ord("t"):
                pressbutton = 2
                print('press "t" ')

            #here is the condition we can upload photo to s3, when cooldown is finish and detect human
            # we need to compare the type first, since if compare with None or not, it will cause error, since the type is not from python origin
            #when type(det) == torch.Tensor mean we have detected something, but we doesn't sure what we have detected, so we change 'det' to list
            #when we detect human, mean we upload a photo, so we start cooldown
            if int((cooldown - time_now).total_seconds()) <= 1 and type(det) == torch.Tensor:
                detlist = det[:, -1].tolist()
                print(detlist)
                if 0 not in detlist:
                    print("we haven't detect human")
                elif (0 in detlist) and pressbutton == 0:
                    print("we detect human")
                    cooldown = time_now + datetime.timedelta(seconds=10)
                    key = 'frame-' + time.strftime("%Y%m%d-%H%M%S") + '.jpg'
                    # s3.upload_file(im0, 'bucket-for-upload-frame', key)
                    _, jpg_data = cv2.imencode('.jpg', im0)
                    s3.put_object(Body=jpg_data.tostring(), Bucket='bucket-for-upload-frame', Key=key)
                elif (0 in detlist) and pressbutton == 1:
                    print("we detect human after press button's' ")
                    cooldown = time_now + datetime.timedelta(seconds=10)
                    key = 'frame2-' + time.strftime("%Y%m%d-%H%M%S") + '.jpg'
                    # s3.upload_file(im0, 'bucket-for-upload-frame', key)
                    _, jpg_data = cv2.imencode('.jpg', im0)
                    s3.put_object(Body=jpg_data.tostring(), Bucket='bucket-for-upload-frame', Key=key)
                    pressbutton = 0
                elif (0 in detlist) and pressbutton == 2:
                    print("we detect human after press button't' ")
                    cooldown = time_now + datetime.timedelta(seconds=10)
                    key = 'frame3-' + time.strftime("%Y%m%d-%H%M%S") + '.jpg'
                    # s3.upload_file(im0, 'bucket-for-upload-frame', key)
                    _, jpg_data = cv2.imencode('.jpg', im0)
                    s3.put_object(Body=jpg_data.tostring(), Bucket='bucket-for-upload-frame', Key=key)
                    pressbutton = 0

                time_now = datetime.datetime.now()



            else:
                time_now = datetime.datetime.now()
                # print("we detect nothing or start cooldown")




            # put text to stream
            im1 = cv2.putText(im0, " press 's' to trigger detection ", (10,50), cv2.FONT_HERSHEY_COMPLEX, 1,(0,255,255),2,cv2.LINE_AA)
            im1 = cv2.putText(im1, " press 't' to trigger detection ", (10, 200), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 255, 255), 2, cv2.LINE_AA)

            # Stream results
            if view_img:
                cv2.imshow(p, im1)
                if cv2.waitKey(1) == ord('q'):  # q to quit
                    raise StopIteration


            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'images':
                    cv2.imwrite(save_path, im0)
                else:
                    if vid_path != save_path:  # new video
                        vid_path = save_path
                        if isinstance(vid_writer, cv2.VideoWriter):
                            vid_writer.release()  # release previous video writer

                        fps = vid_cap.get(cv2.CAP_PROP_FPS)
                        w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*opt.fourcc), fps, (w, h))
                    vid_writer.write(im0)

    if save_txt or save_img:
        print('Results saved to %s' % os.getcwd() + os.sep + out)
        if platform == 'darwin':  # MacOS
            os.system('open ' + out + ' ' + save_path)



    print('Done. (%.3fs)' % (time.time() - t0))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default='cfg/yolov3-spp.cfg', help='*.cfg path')
    parser.add_argument('--names', type=str, default='data/coco.names', help='*.names path')
    parser.add_argument('--weights', type=str, default='weights/yolov3-spp.weights', help='path to weights file')
    parser.add_argument('--source', type=str, default='data/samples', help='source')  # input file/folder, 0 for webcam
    parser.add_argument('--output', type=str, default='output', help='output folder')  # output folder
    parser.add_argument('--img-size', type=int, default=416, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.9, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.3, help='IOU threshold for NMS')
    parser.add_argument('--fourcc', type=str, default='mp4v', help='output video codec (verify ffmpeg support)')
    parser.add_argument('--half', action='store_true', help='half precision FP16 inference')
    parser.add_argument('--device', default='', help='device id (i.e. 0 or 0,1) or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    opt = parser.parse_args()
    print(opt)

    with torch.no_grad():
        detect()
