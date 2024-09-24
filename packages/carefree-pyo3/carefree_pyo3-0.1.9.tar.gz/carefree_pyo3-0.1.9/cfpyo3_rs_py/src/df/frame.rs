use cfpyo3_core::df::{ColumnsDtype, IndexDtype};
use numpy::{PyArray1, PyArray2};
use pyo3::prelude::*;

mod meta;
mod ops;

#[pyclass]
pub struct DataFrameF64 {
    pub index: Py<PyArray1<IndexDtype>>,
    pub columns: Py<PyArray1<ColumnsDtype>>,
    pub data: Py<PyArray2<f64>>,
}
