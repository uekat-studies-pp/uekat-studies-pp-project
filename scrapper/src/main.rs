// extern crate job_scheduler;
// use job_scheduler::{Job, JobScheduler};
// use std::time::Duration;

use voyager::scraper::Selector;
use voyager::*;
use tokio::stream::StreamExt;

struct SteamScraper {
    title_selector: Selector,
    price_selector: Selector,
    price_after_discount_selector: Selector,
    genres_selector: Selector,
    max_page: usize,
}

#[derive(Debug)]
enum SteamState {
    Page(usize),
    Post,
}

struct Entry {
    url: String,
    title: String,
    price: f32,
    priceAfterDiscount: f32,
    genres: Vec<String>,
}

impl Scraper for SteamScraper {
    type Output = Entry;
    type State = SteamState;

    /// do your scraping
    fn scrape(
        &mut self,
        response: Response<Self::State>,
        crawler: &mut Crawler<Self>,
    ) -> Result<Option<Self::Output>> {
        let html = response.html();

        println!("Inside");

        // if let Some(state) = response.state {
        //     match state {
        //         HackernewsState::Page(page) => {
        //             // find all entries
        //             for id in html
        //                 .select(&self.post_selector)
        //                 .filter_map(|el| el.value().attr("id"))
        //             {
        //                 // submit an url to a post
        //                 crawler.visit_with_state(
        //                     &format!("https://news.ycombinator.com/item?id={}", id),
        //                     HackernewsState::Post,
        //                 );
        //             }
        //             if page < self.max_page {
        //                 // queue in next page
        //                 crawler.visit_with_state(
        //                     &format!("https://news.ycombinator.com/news?p={}", page + 1),
        //                     HackernewsState::Page(page + 1),
        //                 );
        //             }
        //         }

        //         HackernewsState::Post => {
        //             // scrape the entry
        //             let entry = Entry {
        //                 // ...
        //             };
        //             return Ok(Some(entry))
        //         }
        //     }
        // }

        Ok(None)
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let config = CrawlerConfig::default().allow_domain_with_delay(
        "store.steampowered.com",
        RequestDelay::Fixed(std::time::Duration::from_millis(2_000)),
    );
    
    let mut collector = Collector::new(SteamScraper::default(), config);

    collector.crawler_mut().visit_with_state(
        "https://store.steampowered.com/search/?filter=topsellers",
        SteamScraper::Page(1),
    );

    while let Some(output) = collector.next().await {
        let post = output?;
        dbg!(post);
    }
    
    Ok(())
}

// fn scrap() {
//     println!("Scrapping steam started");
//     println!("Scrapping steam ended");
//     println!("Scrapping gog started");
//     println!("Scrapping gog ended");
// }

// fn main() {
//     let mut sched = JobScheduler::new();

//     sched.add(Job::new("* * * * * *".parse().unwrap(), || scrap()));

//     loop {
//         sched.tick();

//         std::thread::sleep(Duration::from_millis(500));
//     }
// }
