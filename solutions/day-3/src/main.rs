extern crate regex;

fn main() {
    use data;

    let mut fabric = [[0; 1000]; 1000];
    let claims = data::get_data();
    for claim in claims {
        claim.cut(&mut fabric);
    }
    let mut counter = 0;
    for i in 0..fabric.len() {
        for j in 0..fabric[0].len() {
            if fabric[i][j] == -1 {
                counter += 1;
            }
        }
    }
    println!("The mumber of overlapping square inches is: {}", counter);
}

pub mod data {
    use std::fs::File;
    use std::io::Read;

    use regex::Regex;

    pub struct Claim {
        id: i32,
        left: usize,
        top: usize,
        width: usize,
        height: usize,
    }
    impl Claim {
        pub fn cut (&self, rect: &mut[[i32; 1000]; 1000]) {
            for i in self.left..self.left+self.width {
                for j in self.top..self.top+self.height {
                    if rect[i][j] == 0 {
                        // Claimed
                        rect[i][j] = self.id;
                    } else if rect[i][j] > 0 {
                        // Someone has already claimed it
                        rect[i][j] = -1;
                    }
                }
            }
        }
    }


//    pub fn get_data() -> Vec<Claim> {}

    pub fn get_data() -> Vec<Claim> {
        // example claim:
        //   #123 @ 3,2: 5x4
        let re = Regex::new(r"#(?P<id>\d+) @ (?P<left>\d+).(?P<top>\d+): (?P<width>\d+)x(?P<height>\d+)").unwrap();
        let mut claims: Vec<Claim> = Vec::new();
        for cap in re.captures_iter(get_raw_data().as_str()) {
            claims.push(Claim {
                id: cap["id"].parse().expect("Failed to convert ID"),
                left: cap["left"].parse().expect("Failed to convert left"),
                top: cap["top"].parse().expect("Failed to convert top"),
                width: cap["width"].parse().expect("Failed to convert width"),
                height: cap["height"].parse().expect("Failed to convert height"),
            });
        }
        return claims;

    }

    fn get_raw_data() -> String {
        let mut f = File::open("input.txt")
            .expect("File not found");
        let mut raw_data = String::new();
        f.read_to_string(&mut raw_data)
            .expect("Unable to read the file");
        return raw_data;
    }

}
