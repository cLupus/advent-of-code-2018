use std::fs::File;
use std::io::prelude::*;

fn main() {
    part_1();
    part_2();  // FIXME: Takes 'forever' (but works)
}

fn part_2() {
    let mut found = false;
    let mut cumulative = 0;
    let mut seen_before: Vec<i32> = Vec::new();
    seen_before.push(cumulative);

    let frequencies = get_frequencies();

    while !found {
        for frequency in frequencies.iter() {
            cumulative += frequency;
            if seen_before.contains(&cumulative) {
                found = true;
                break;
            } else {
                seen_before.push(cumulative);
            }
        }
    }
    println!("The first frequency your device reaches twice is: {}", cumulative);
}

fn part_1() {
    let frequencies = get_frequencies();
    let mut sum = 0;
    for frequency in frequencies {
        sum += frequency;
    }
    println!("The resulting frequency is {}", sum);
}

fn get_frequencies() -> Vec<i32> {
    let mut f = File::open("input.txt")
        .expect("File not found");
    let mut numbers = String::new();
    f.read_to_string(&mut numbers)
        .expect("Unable to read the file");
    let mut frequencies: Vec<i32> = Vec::new();
    for num in numbers.split("\n") {
        frequencies.push(num.trim().parse().expect("Invalid number"));
    }
    return frequencies;
}