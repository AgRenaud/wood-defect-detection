import grpc
import base64
import yolo_pb2
import yolo_pb2_grpc

from typing import List


def run(image_path: List[str]):

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = yolo_pb2_grpc.YoloStub(channel)

        # read list of images
        # transform each to bytes
        images = []

        for p in image_path:
            with open(p, "rb") as imageFile:
                img = imageFile.read()
                images.append(img)

        batch = yolo_pb2.DetectBatchRequest(
            batch=images
        )

        response = stub.DetectObjects(batch)

        print(response)


if __name__ == "__main__":
    run([
        "../datasets/wood-surface-defects/valid/images/106600051.jpg",
    ])
