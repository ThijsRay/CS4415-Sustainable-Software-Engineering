use std::fs;

pub fn start(){
    let enabled = fs::read_to_string("/sys/devices/virtual/powercap/intel-rapl/enabled").expect("File not accessable");
    if !enabled.starts_with("1") {
        println!("Powercap is not enabled!");
    }

    let current_measured_uj_string = fs::read_to_string("/sys/devices/virtual/powercap/intel-rapl/intel-rapl:0/energy_uj").expect("Unable to read ujs");
    //let current_measured_uj: i64 = current_measured_uj_string.parse::<i64>().unwrap();
    let max_measured_uj_string = fs::read_to_string("/sys/devices/virtual/powercap/intel-rapl/intel-rapl:0/max_energy_range_uj").expect("Unable to read max ujs");
    //let max_measured_uj: i64 = max_measured_uj_string.parse().unwrap();
    println!("measured: {} out of {}", current_measured_uj_string, max_measured_uj_string);
}