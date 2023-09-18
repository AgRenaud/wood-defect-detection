import grpc

import yolo_pb2
import yolo_pb2_grpc


def run():

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = yolo_pb2_grpc.YoloStub(channel)

        # read list of images
        # transform each to bytes
        images = []

        batch = yolo_pb2.DetectBatchRequest(
            batch=images
        )

        response = stub.DetectObjects(batch)

        print(response)


if __name__ == "__main__":
    run()
