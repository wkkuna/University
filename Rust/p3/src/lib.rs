mod fractal;
mod utils;

use crate::fractal::Complex;
use crate::fractal::Fractal;
use wasm_bindgen::prelude::*;
use web_sys::CanvasRenderingContext2d;

// When the `wee_alloc` feature is enabled, use `wee_alloc` as the global
// allocator.
#[cfg(feature = "wee_alloc")]
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

#[wasm_bindgen]
extern "C" {
    fn alert(s: &str);
}

#[wasm_bindgen]
pub fn greet() {
    alert("Hello, projekt3!");
}

#[wasm_bindgen]
pub fn generate(ctx: &CanvasRenderingContext2d, width: u32, height: u32) {
    let g = Fractal::new(
        Complex::new(-2.2_f64, -1.2_f64),
        Complex::new(-2.2_f64, -1.2_f64),
        100,
        4.0,
    );
    g.generate(ctx, width as usize, height as usize);
}
