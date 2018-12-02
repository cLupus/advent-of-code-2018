use std::fs::File;
use std::io::Read;
use std::collections::HashMap;

fn main() {
    let number_to_look_for = [2, 3];
    let mut counter: HashMap<&i32, i32> = HashMap::new();

    for id in get_ids() {
        let counts = get_counts(&id[..]);
        for num in number_to_look_for.iter() {
            let count = counter.entry(num).or_insert(0);
            *count += num_letters(&counts, *num);
        }
    }
    let mut hash = 1;
    for (num, count) in counter {
        hash *= count;
    }
    println!("The hash of all IDs is: {}", hash)
}

fn num_letters(counts: &HashMap<char, i32>, count: i32) -> i32{
    for (_, num_occurrences) in counts {
        if *num_occurrences == count {
            return 1;
        }
    }
    return 0;
}

fn get_counts(word: &str) -> HashMap<char, i32> {
    let mut letters: HashMap<char, i32> = HashMap::new();
    for letter in word.chars() {
        let num_occurrences = letters.entry(letter).or_insert(0);
        *num_occurrences += 1;
    }
    letters
}

fn get_ids() -> Vec<String> {
    let mut f = File::open("input.txt")
        .expect("File not found");
    let mut data = String::new();
    f.read_to_string(&mut data)
        .expect("Unable to read the file");
    let mut ids: Vec<String> = Vec::new();
    for id in data.split("\n") {
        ids.push(id.trim().to_string());
    }
    return ids;
}
