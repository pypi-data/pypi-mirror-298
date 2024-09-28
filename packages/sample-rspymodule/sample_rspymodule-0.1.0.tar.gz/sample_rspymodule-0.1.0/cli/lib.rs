use pyo3::prelude::*;

/// Prints a message.
#[pyfunction]
fn hello() -> PyResult<String> {
    println!("Hello function called from Rust!");
    Ok("Hello from sample-rspymodule!".into())
}

#[pyfunction]
fn sum_as_string(a: i32, b: i32) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn _lowlevel(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello, m)?)?;
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hello() {
        let result = hello();
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "Hello from sample-rspymodule!");
    }

    #[test]
    fn test_sum_as_string() {
        let result = sum_as_string(2, 3);
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "5");

        let result = sum_as_string(-1, 1);
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "0");
    }
}
