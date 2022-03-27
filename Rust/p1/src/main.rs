use std::fs::OpenOptions;
use std::io::Write;
use std::ops;

#[derive(Clone, Debug)]
struct Colour {
    r: u8,
    g: u8,
    b: u8,
}

impl Colour {
    fn to_arr(&self) -> [u8; 3] {
        [self.r, self.g, self.b]
    }

    fn new(r: u8, g: u8, b: u8) -> Colour {
        Colour { r, g, b }
    }
}

struct Image {
    magic: String,
    width: usize,
    height: usize,
    pixels: Vec<Colour>,
}

impl Image {
    fn set_pixel_colour(&mut self, row: usize, column: usize, colour: Colour) {
        let idx = row * self.width + column;
        self.pixels[idx] = colour;
    }

    fn new(width: usize, height: usize) -> Image {
        Image {
            height,
            width,
            magic: String::from("P6"),
            pixels: vec![Colour::new(255, 255, 255); height * width],
        }
    }

    fn save_to_file(&self, filename: &str) -> std::io::Result<()> {
        let mut file = OpenOptions::new().write(true).create(true).open(filename)?;
        file.write_all(
            format!("{}\n{} {}\n255\n", self.magic, self.width, self.height).as_bytes(),
        )?;
        for p in self.pixels.iter() {
            file.write_all(&p.to_arr())?;
        }
        Ok(())
    }
}

#[derive(Clone, Copy, Debug)]
struct Complex {
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
    fn new(re: f64, im: f64) -> Complex {
        Complex { re, im }
    }
}

fn scale(value: f64, min1: f64, max1: f64, min2: f64, max2: f64) -> f64 {
    min2 + (max2 - min2) * ((value - min1) / (max1 - min1))
}

struct Fractal {
    filename: String,
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

    fn generate(&self, width: usize, height: usize) {
        let mut img = Image::new(width, height);
        for y in 0..height {
            for x in 0..width {
                let c = self.calc_pixel_colour(Complex::new(x as f64, y as f64), width, height);
                img.set_pixel_colour(y, x, c);
            }
        }
        img.save_to_file(self.filename.as_str()).unwrap();
    }

    fn new(
        filename: String,
        lower_bound: Complex,
        upper_bound: Complex,
        iter_bound: usize,
        max_value: f64,
    ) -> Fractal {
        Fractal {
            filename,
            lower_bound,
            upper_bound,
            iter_bound,
            max_value,
        }
    }
}

fn main() {
    let filename = String::from("fractal.ppm");
    let lower_bound = Complex::new(-2., -1.12);
    let upper_bound = Complex::new(0.47, 1.12);
    let iter_bound = 100;
    let max_value = 2.;

    let f = Fractal::new(filename, lower_bound, upper_bound, iter_bound, max_value);
    f.generate(800, 600);
}
