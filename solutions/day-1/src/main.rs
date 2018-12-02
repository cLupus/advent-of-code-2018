use std::fs::File;
use std::io::prelude::*;
use std::collections::HashSet;

fn main() {
    let ans = total_sum();
    println!("The resulting frequency is {}", ans);

    let ans = first_repeating();
    println!("The first frequency your device reaches twice is: {}", ans);

}

fn first_repeating() -> i32 {
    let mut found = false;
    let mut cumulative = 0;
    let mut seen_before: HashSet<i32> = HashSet::new();
    seen_before.insert(cumulative);

    let frequencies = get_frequencies();

    while !found {
        for frequency in frequencies.iter() {
            cumulative += frequency;
            if seen_before.contains(&cumulative) {
                found = true;
                break;
            } else {
                seen_before.insert(cumulative);
            }
        }
    }
    cumulative
}

fn total_sum() -> i32 {
    let frequencies = get_frequencies();
    let mut sum = 0;
    for frequency in frequencies {
        sum += frequency;
    }
    sum
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