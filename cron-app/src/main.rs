extern crate job_scheduler;
use job_scheduler::{JobScheduler, Job};
use std::time::Duration;

fn main() {
    let mut sched = JobScheduler::new();

    sched.add(Job::new("0 * * * * *".parse().unwrap(), || {
        println!("Crawl started");
        println!("Crawl ended");
    }));

    loop {
        sched.tick();

        std::thread::sleep(Duration::from_millis(500));
    }
}