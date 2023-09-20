use image::imageops;
use image::load_from_memory;

use image::ImageBuffer;
use image::Rgb;
use onnxruntime::environment::Environment;
use onnxruntime::ndarray;

use onnxruntime::tensor::OrtOwnedTensor;
use onnxruntime::GraphOptimizationLevel;
use onnxruntime::LoggingLevel;
use tonic::{transport::Server, Request, Response, Status};
use yolo::yolo_server::{Yolo, YoloServer};
use yolo::{
    BoundingBox, ClassEnum, DetectBatchRequest, DetectBatchResponse, DetectResponse,
    ObjectDetection,
};

pub mod yolo {
    tonic::include_proto!("yolo");
}

pub struct YoloService {
    model_path: String,
}

impl YoloService {
    pub fn new(model_path: String) -> Self {
        Self { model_path }
    }
}

#[tonic::async_trait]
impl Yolo for YoloService {
    async fn detect_objects(
        &self,
        request: Request<DetectBatchRequest>,
    ) -> Result<Response<DetectBatchResponse>, Status> {
        let batch_request = request.into_inner();
        let mut batch_response = DetectBatchResponse::default();

        let environment = Environment::builder()
            .with_name("test")
            .with_log_level(LoggingLevel::Verbose)
            .build()
            .expect("Unable to create onnx env.");

        let mut session = environment
            .new_session_builder()
            .expect("Unable to create onnx session")
            .with_optimization_level(GraphOptimizationLevel::Basic)
            .expect("Unable to set opts")
            .with_number_threads(1)
            .expect("Unable to set threads")
            .with_model_from_file(&self.model_path)
            .expect("Can't read onnx file;");

        let mut input_tensors = Vec::new();

        let height = 480;
        let width = 480;
        let channels = 3;

        for image in batch_request.batch {
            let image_data = image.as_slice();

            let dynamic_image = image::io::Reader::new(std::io::Cursor::new(image_data))
                .with_guessed_format()
                .expect("Unable to guess image format")
                .decode()
                .expect("Unable to decode image");

            let rgb_image: ImageBuffer<Rgb<u8>, Vec<u8>> = dynamic_image.to_rgb8();

            let resized =
                imageops::resize(&rgb_image, width, height, imageops::FilterType::CatmullRom);

            let resized_data: Vec<f32> = resized
                .pixels()
                .map(|pixel| {
                    let c = pixel.0;
                    [
                        f32::from(c[0]) / 255.0,
                        f32::from(c[1]) / 255.0,
                        f32::from(c[2]) / 255.0,
                    ]
                })
                .flatten()
                .collect();

            let input_shape = (1, height as usize, width as usize, channels as usize);
            let input_tensor =
                ndarray::Array::from_shape_vec(input_shape, resized_data).expect("couldn'darray ");
            input_tensors.push(input_tensor);
        }

        let input_tensors: Vec<ndarray::ArrayBase<ndarray::ViewRepr<&f32>, _>> =
            input_tensors.iter().map(|arr| arr.view()).collect();
        let batched_input_tensor = ndarray::stack(ndarray::Axis(0), input_tensors.as_slice())
            .expect("Failed to stack arrays");

        // Run inference using ONNX Runtime
        let inputs = vec![batched_input_tensor];
        let output: Vec<OrtOwnedTensor<f32, _>> = session
            .run(inputs)
            .expect("Inference gone wrong. We're so done.");

        for (_i, _detect_request) in output.iter().enumerate() {

            let mut object_detection = ObjectDetection::default();
            object_detection.class = ClassEnum::LivelKnot.into();
            object_detection.confidence = 0.85;

            let mut bounding_box = BoundingBox::default();
            bounding_box.x_min = 0.1;
            bounding_box.y_min = 0.2;
            bounding_box.x_max = 0.9;
            bounding_box.y_max = 0.8;

            object_detection.bounding_box = Some(bounding_box);

            let mut detect_response = DetectResponse::default();

            detect_response.objects.push(object_detection);
            batch_response.requests.push(detect_response);
        }

        Ok(Response::new(batch_response))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "0.0.0.0:50051".parse()?;

    let model_path = "best.onnx";

    let yolo_service = YoloService::new(String::from(
        model_path,
    ));

    Server::builder()
        .add_service(YoloServer::new(yolo_service))
        .serve(addr)
        .await?;

    Ok(())
}
