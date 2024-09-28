use crate::error::Result;
use ndarray::Array2;
use ort::Session;

pub fn predict(
    session: &Session,
    token_ids: Vec<i64>,
    attention_masks: Vec<i64>,
) -> Result<Array2<f32>> {
    let outputs = session.run(
        ort::inputs! {
            "input_ids" => Array2::from_shape_vec((1, token_ids.len()), token_ids).unwrap(),
            "attention_mask" => Array2::from_shape_vec((1, attention_masks.len()), attention_masks).unwrap(),
        }?
    )?;

    let output = outputs.get("output").unwrap();

    let content = output.try_extract_tensor::<f32>()?.to_owned();
    let (data, _) = content.clone().into_raw_vec_and_offset();

    Ok(Array2::from_shape_vec((content.shape()[0], content.shape()[1]), data).unwrap())
}
