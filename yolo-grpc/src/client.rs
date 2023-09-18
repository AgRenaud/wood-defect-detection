// CLIENT
//
//
//

use yolo::{yolo_client::YoloClient, DetectBatchRequest};

pub mod yolo {
    tonic::include_proto!("yolo");
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let _client = YoloClient::connect("http://[::1]:50051").await?;

    let _request = tonic::Request::new(DetectBatchRequest { batch: Vec::new() });

    Ok(())
}
