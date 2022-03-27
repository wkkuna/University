use std::ops;
use wasm_bindgen::Clamped;
use web_sys::CanvasRenderingContext2d;
use web_sys::ImageData;

#[derive(Clone, Debug)]
struct Colour {
    r: u8,
    g: u8,
    b: u8,
    a: u8,
}

impl Colour {
    fn to_arr(&self) -> [u8; 3] {
        [self.r, self.g, self.b]
    }

    fn new(r: u8, g: u8, b: u8) -> Colour {
        Colour { r, g, b, a: 255 }
    }
    pub fn to_vec(&self) -> Vec<u8> {
        vec![self.r, self.g, self.b, self.a]
    }
}

struct Image<'a> {
    ctx: &'a CanvasRenderingContext2d,
    width: usize,
    height: usize,
    pixels: Vec<Colour>,
}

impl<'a> Image<'a> {
    fn set_pixel_colour(&mut self, row: usize, column: usize, colour: Colour) {
        let idx = row * self.width + column;
        self.pixels[idx] = colour;
    }

    fn new(ctx: &CanvasRenderingContext2d, width: usize, height: usize) -> Image {
        Image {
            ctx,
            height,
            width,
            pixels: vec![Colour::new(255, 255, 255); height * width],
        }
    }

    fn save(&self) -> std::io::Result<()> {
        let mut pixels = self
            .pixels
            .iter()
            .flat_map(|x| x.to_vec())
            .collect::<Vec<u8>>();

        let data = ImageData::new_with_u8_clamped_array_and_sh(
            Clamped(pixels.as_mut_slice()),
            self.width as u32,
            self.height as u32,
        )
        .unwrap();

        self.ctx.put_image_data(&data, 0.0, 0.0).unwrap();

        Ok(())
    }
}

#[derive(Clone, Copy, Debug)]
pub struct Complex {
    im: f64,
    re: f64,
}

impl ops::Add<Complex> for Complex {
    type Output = Complex;
    fn add(self, b: Complex) -> Complex {
        Complex::new(self.re + b.re, self.im + b.im)
    }
}

impl ops::Mul<Complex> for Complex {
    type Output = Complex;
    fn mul(self, b: Complex) -> Complex {
        let re = self.re * b.re - self.im * b.im;
        let im = self.re * b.im + self.im * b.re;
        Complex::new(re, im)
    }
}

impl Complex {
    fn distance(&self) -> f64 {
        (self.re * self.re + self.im * self.im).sqrt()
    }
    pub fn new(re: f64, im: f64) -> Complex {
        Complex { re, im }
    }
}

fn scale(value: f64, min1: f64, max1: f64, min2: f64, max2: f64) -> f64 {
    min2 + (max2 - min2) * ((value - min1) / (max1 - min1))
}

pub struct Fractal {
    lower_bound: Complex,
    upper_bound: Complex,
    iter_bound: usize,
    max_value: f64,
}

impl Fractal {
    fn get_colour(&self, idx: usize) -> Colour {
        if idx == self.iter_bound {
            return Colour::new(255, 255, 255);
        }
        let brightness = scale(idx as f64, 0., self.iter_bound as f64, 0., 1.);
        let c = scale(brightness, 0., 1., 0., 255.) as u8;
        Colour::new(c, c, c)
    }

    fn calc_pixel_colour(&self, x: Complex, width: usize, height: usize) -> Colour {
        let mut z = Complex::new(
            scale(
                x.re,
                0.,
                width as f64,
                self.lower_bound.re,
                self.upper_bound.re,
            ),
            scale(
                x.im,
                0.,
                height as f64,
                self.lower_bound.im,
                self.upper_bound.im,
            ),
        );
        let c = z.clone();
        let mut i = 0;
        while i < self.iter_bound && z.distance() < self.max_value {
            z = z * z + c;
            i += 1;
        }
        self.get_colour(i)
    }

    pub fn generate(&self, ctx: &CanvasRenderingContext2d, width: usize, height: usize) {
        let mut img = Image::new(ctx, width, height);

        for y in 0..height {
            for x in 0..width {
                let c = self.calc_pixel_colour(Complex::new(x as f64, y as f64), width, height);
                img.set_pixel_colour(y, x, c);
            }
        }
        img.save().unwrap();
    }

    pub fn new(
        lower_bound: Complex,
        upper_bound: Complex,
        iter_bound: usize,
        max_value: f64,
    ) -> Fractal {
        Fractal {
            lower_bound,
            upper_bound,
            iter_bound,
            max_value,
        }
    }
}
